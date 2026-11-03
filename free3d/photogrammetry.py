#!/usr/bin/env python3
"""Vellessa free photogrammetry helper. Requires Meshroom and Blender installed locally."""
from pathlib import Path
import argparse, shutil, subprocess, sys

def run(cmd):
    print("\n>", " ".join(map(str, cmd)), flush=True)
    subprocess.run(list(map(str, cmd)), check=True)

def main():
    p=argparse.ArgumentParser(description="Create a textured GLB from shoe photos using free Meshroom + Blender.")
    p.add_argument("photos", help="Folder containing 8+ overlapping shoe photos")
    p.add_argument("--output", default="vellessa-output", help="Output folder")
    p.add_argument("--meshroom", default="meshroom_batch", help="Path to meshroom_batch executable")
    p.add_argument("--blender", default="blender", help="Path to Blender executable")
    a=p.parse_args()
    photos=Path(a.photos).expanduser().resolve()
    out=Path(a.output).expanduser().resolve()
    cache=out/"meshroom-cache"
    if not photos.is_dir(): sys.exit("Photo folder not found.")
    imgs=[x for x in photos.iterdir() if x.suffix.lower() in {".jpg",".jpeg",".png",".webp"}]
    if len(imgs)<8: sys.exit(f"Need at least 8 photos; found {len(imgs)}.")
    meshroom=shutil.which(a.meshroom) or (a.meshroom if Path(a.meshroom).exists() else None)
    blender=shutil.which(a.blender) or (a.blender if Path(a.blender).exists() else None)
    if not meshroom: sys.exit("Meshroom not found. Install Meshroom and add meshroom_batch to PATH.")
    if not blender: sys.exit("Blender not found. Install Blender and add blender to PATH.")
    out.mkdir(parents=True,exist_ok=True)
    run([meshroom,"--input",photos,"--output",out/"meshroom-output","--cache",cache])
    candidates=list(cache.rglob("texturedMesh.obj"))+list((out/"meshroom-output").rglob("texturedMesh.obj"))
    if not candidates:
        candidates=list(cache.rglob("*.obj"))+list((out/"meshroom-output").rglob("*.obj"))
    if not candidates: sys.exit("Meshroom finished but no OBJ mesh was found. Inspect Meshroom output/cache.")
    mesh=max(candidates,key=lambda x:x.stat().st_mtime)
    script=Path(__file__).with_name("export_glb.py")
    run([blender,"--background","--python",script,"--",str(mesh),str(out/"vellessa-ayakkabi.glb")])
    print("\nGLB ready:",out/"vellessa-ayakkabi.glb")

if __name__=="__main__": main()
