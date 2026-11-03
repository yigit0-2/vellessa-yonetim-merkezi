import os
import uuid
import shutil
import subprocess
import threading
import time
from pathlib import Path
from typing import List

import trimesh
from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from PIL import Image

DATA = Path(os.getenv("DATA_DIR", "/data/jobs"))
DATA.mkdir(parents=True, exist_ok=True)
MAX_BYTES = int(os.getenv("MAX_UPLOAD_MB", "250")) * 1024 * 1024
ALLOWED = {".jpg", ".jpeg", ".png", ".webp"}
jobs = {}
lock = threading.Lock()

app = FastAPI(title="Vellessa 3D Studio API", version="1.0.0")
origins = os.getenv("CORS_ORIGINS", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

def run(cmd, cwd, timeout=7200):
    p = subprocess.run(cmd, cwd=str(cwd), capture_output=True, text=True, timeout=timeout)
    if p.returncode:
        raise RuntimeError((p.stderr or p.stdout or "COLMAP işlem hatası")[-5000:])
    return p.stdout

def process_job(job_id: str):
    root = DATA / job_id
    images = root / "images"
    work = root / "work"
    sparse = work / "sparse"
    dense = work / "dense"
    work.mkdir(exist_ok=True)
    sparse.mkdir(exist_ok=True)
    dense.mkdir(exist_ok=True)
    try:
        with lock:
            jobs[job_id]["status"] = "processing"
            jobs[job_id]["progress"] = 5
        db = work / "database.db"
        run(["colmap", "feature_extractor", "--database_path", str(db),
             "--image_path", str(images), "--ImageReader.single_camera", "1"], work)
        with lock:
            jobs[job_id]["progress"] = 20
        run(["colmap", "exhaustive_matcher", "--database_path", str(db)], work)
        with lock:
            jobs[job_id]["progress"] = 35
        run(["colmap", "mapper", "--database_path", str(db),
             "--image_path", str(images), "--output_path", str(sparse)], work, 7200)
        models = [p for p in sparse.iterdir() if p.is_dir()]
        if not models:
            raise RuntimeError("Fotoğraflardan kamera eşlemesi çıkarılamadı. Daha fazla açıdan, net ve örtüşen fotoğraf gerekli.")
        model = models[0]
        run(["colmap", "image_undistorter", "--image_path", str(images),
             "--input_path", str(model), "--output_path", str(dense),
             "--output_type", "COLMAP"], work)
        with lock:
            jobs[job_id]["progress"] = 55
        run(["colmap", "patch_match_stereo", "--workspace_path", str(dense),
             "--workspace_format", "COLMAP"], work, 14400)
        run(["colmap", "stereo_fusion", "--workspace_path", str(dense),
             "--workspace_format", "COLMAP", "--input_type", "geometric",
             "--output_path", str(dense / "fused.ply")], work, 7200)
        with lock:
            jobs[job_id]["progress"] = 80
        run(["colmap", "poisson_mesher", "--input_path", str(dense / "fused.ply"),
             "--output_path", str(root / "model.ply")], work, 7200)
        mesh = trimesh.load(root / "model.ply", force="mesh")
        if mesh.is_empty:
            raise RuntimeError("3D yüzey üretilemedi; fotoğraf seti yetersiz olabilir.")
        mesh.export(root / "model.glb")
        with lock:
            jobs[job_id].update(status="completed", progress=100,
                                model_url=f"/jobs/{job_id}/model",
                                finished_at=time.time())
    except Exception as exc:
        with lock:
            jobs[job_id].update(status="failed", error=str(exc)[-2000:],
                                finished_at=time.time())

@app.get("/health")
def health():
    return {"ok": True, "service": "vellessa-3d-api", "engine": "COLMAP"}

@app.post("/jobs")
async def create_job(background_tasks: BackgroundTasks, photos: List[UploadFile] = File(...)):
    if len(photos) < 12:
        raise HTTPException(400, "Gerçek 3D için en az 12 farklı açı fotoğrafı yükleyin.")
    if len(photos) > 100:
        raise HTTPException(400, "Tek işte en fazla 100 fotoğraf yüklenebilir.")
    job_id = uuid.uuid4().hex
    folder = DATA / job_id / "images"
    folder.mkdir(parents=True)
    total = 0
    try:
        for i, upload in enumerate(photos):
            suffix = Path(upload.filename or "").suffix.lower()
            if suffix not in ALLOWED:
                raise HTTPException(400, f"Desteklenmeyen dosya: {upload.filename}")
            dest = folder / f"{i:04d}{suffix}"
            with dest.open("wb") as out:
                while chunk := await upload.read(1024 * 1024):
                    total += len(chunk)
                    if total > MAX_BYTES:
                        raise HTTPException(413, "Fotoğraf toplam boyutu sunucu sınırını aşıyor.")
                    out.write(chunk)
            try:
                with Image.open(dest) as im:
                    im.verify()
            except Exception:
                raise HTTPException(400, f"Geçersiz görsel: {upload.filename}")
        with lock:
            jobs[job_id] = {"id": job_id, "status": "queued", "progress": 0,
                            "photo_count": len(photos), "created_at": time.time()}
        background_tasks.add_task(process_job, job_id)
        return jobs[job_id]
    except Exception:
        shutil.rmtree(DATA / job_id, ignore_errors=True)
        raise

@app.get("/jobs/{job_id}")
def job_status(job_id: str):
    with lock:
        job = jobs.get(job_id)
    if not job:
        raise HTTPException(404, "İş bulunamadı veya sunucu yeniden başlatıldı.")
    return job

@app.get("/jobs/{job_id}/model")
def get_model(job_id: str):
    path = DATA / job_id / "model.glb"
    if not path.exists():
        raise HTTPException(404, "Model henüz hazır değil.")
    return FileResponse(path, media_type="model/gltf-binary", filename="vellessa-model.glb")
