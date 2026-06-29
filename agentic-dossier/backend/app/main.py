import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.api import endpoints

app = FastAPI(title="Agentic Dossier", description="Air-gapped privacy-first document analysis system")

app.include_router(endpoints.router, prefix="/api/v1")

# Mount frontend as static files at root
frontend_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "frontend")
app.mount("/", StaticFiles(directory=frontend_dir, html=True), name="frontend")
