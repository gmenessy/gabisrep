from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.api.endpoints import router as api_router
import os

app = FastAPI(title="Agentic Dossier", description="Air-gapped, privacy-first document analysis system")

# Include API Router
app.include_router(api_router, prefix="/api")

# Mount frontend as static files at root
# Calculate dynamic absolute path relative to this file's location
# backend/app/main.py -> backend/app -> backend -> root -> frontend
base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
frontend_path = os.path.join(base_dir, "frontend")

app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")
