from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.api.endpoints import router as api_router
import os

app = FastAPI(title="Agentic Dossier", description="Privacy-first document analysis system")

# Mount API routes
app.include_router(api_router, prefix="/api")

# Mount frontend static files
# Calculate the absolute path to the frontend directory
base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
frontend_dir = os.path.join(base_dir, "frontend")

@app.get("/")
async def serve_index():
    return FileResponse(os.path.join(frontend_dir, "index.html"))

app.mount("/", StaticFiles(directory=frontend_dir, html=True), name="frontend")
