from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import os
from app.api.endpoints import router as api_router

app = FastAPI(title="Agentic Dossier", description="Air-gapped, privacy-first document analysis system")

# Include the API router
app.include_router(api_router, prefix="/api")

# Mount the frontend directory as static files
# Calculate the absolute path to the frontend directory
current_dir = os.path.dirname(os.path.abspath(__file__))
# app/ is inside backend/, frontend/ is a sibling of backend/
frontend_dir = os.path.join(current_dir, "..", "..", "frontend")

app.mount("/", StaticFiles(directory=frontend_dir, html=True), name="frontend")
