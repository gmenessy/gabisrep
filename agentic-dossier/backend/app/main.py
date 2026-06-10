from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.api.endpoints import router as api_router
import os

app = FastAPI(title="Agentic Dossier", description="Air-gapped privacy-first document analysis system")

app.include_router(api_router)

frontend_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "frontend")

app.mount("/", StaticFiles(directory=frontend_dir, html=True), name="frontend")
