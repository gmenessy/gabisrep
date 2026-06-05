import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.api import endpoints

app = FastAPI(title="Agentic Dossier API", version="1.0.0")

# Include API router
app.include_router(endpoints.router, prefix="/api/v1")

# Mount frontend directory dynamically
frontend_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "frontend")

# Serve the static files from /frontend at the root "/"
app.mount("/", StaticFiles(directory=frontend_dir, html=True), name="frontend")
