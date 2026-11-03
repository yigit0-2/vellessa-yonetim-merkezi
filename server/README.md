# Vellessa 3D Studio API

This is the backend for the single-screen Vellessa Reels Studio. It accepts shoe photos, runs COLMAP photogrammetry, creates a mesh, and returns a GLB for the existing Three.js viewer.

## Run locally
```bash
docker build -t vellessa-3d-api -f server/Dockerfile .
docker run --rm -p 8000:8000 -v vellessa-data:/data vellessa-3d-api
```

Health: `GET /health`  
Create reconstruction: `POST /jobs` with multipart field `photos` repeated for each JPG/PNG/WEBP image (minimum 12, maximum 100).  
Poll: `GET /jobs/{id}`  
Download GLB: `GET /jobs/{id}/model`

## Deployment
The Render blueprint is at `server/render.yaml`. Deploying it requires connecting the GitHub repository to a Docker-capable hosting account and approving a paid compute/disk plan. COLMAP dense reconstruction is CPU/RAM intensive; a small free web instance is not a reliable production host. The app must use the deployed API base URL, configured as `VELLessa_API_URL` / `VELLessa_API_URL` in the frontend integration.

## Important limitations
- Photogrammetry reconstructs only surfaces visible in the photos. It cannot infer hidden shoe geometry or guarantee exact logos, textures, or sole details.
- Use 30–80 sharp photos with substantial overlap, consistent lighting, and a full walk-around of the shoe. Avoid motion blur, reflective backgrounds, and changing exposure.
- Jobs and status are currently held in process memory. Use a persistent queue/database and object storage before multi-worker or public production use.
- This API creates the GLB model. Cinematic 9:16 rendering remains in the browser-side Three.js studio and needs a compatible browser/recording implementation.
- Add authentication, rate limiting, quotas, and cleanup policies before exposing this endpoint publicly.
