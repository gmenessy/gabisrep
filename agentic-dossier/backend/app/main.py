from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.api.endpoints import router as api_router
import os

app = FastAPI(title="Agentic Dossier API")

# Mount API routes
app.include_router(api_router, prefix="/api/v1")

# Mount frontend as static files
frontend_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "frontend")
app.mount("/", StaticFiles(directory=frontend_dir, html=True), name="frontend")
