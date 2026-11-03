# Vellessa Meshy 3D Proxy

This Worker keeps the Meshy API key off the public GitHub Pages frontend.

## Deploy
1. Open the `worker` folder in a local copy of this repository.
2. Install Wrangler: `npm install -g wrangler`
3. Run `wrangler login`
4. From the worker folder, set the secret: `wrangler secret put MESHY_API_KEY`
5. Paste your Meshy API key when prompted. Never put it in HTML/JavaScript or commit it.
6. Deploy: `wrangler deploy`
7. Copy the deployed Worker URL (for example `https://vellessa-3d-api.<account>.workers.dev`) into the 3D production server field in Reels Atölyesi.

The frontend sends 2-4 compressed image data URLs to `POST /create` and checks `GET /status/:id`. The Worker calls Meshy's Multi-Image to 3D API and returns the GLB URL after completion.

## Cost and limitations
- Meshy generation is not guaranteed free. Its API requires a valid API key and sufficient credits/eligible plan. Check the current quote/balance in Meshy before submitting.
- Each generation sends product photos to Meshy's external service.
- AI reconstruction can alter small details. Inspect the GLB before publishing.
- The Worker currently allows browser CORS requests from any origin; restrict `Access-Control-Allow-Origin` to the Vellessa Pages domain before production if desired.
