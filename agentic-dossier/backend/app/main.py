import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.api.endpoints import router as api_router

app = FastAPI(title="Agentic Dossier", description="Air-gapped privacy-first document analysis system")

app.include_router(api_router, prefix="/api/v1")

# Mount frontend directory as static files dynamically based on __file__
current_dir = os.path.dirname(os.path.abspath(__file__))
# current_dir is agentic-dossier/backend/app. So frontend is ../../frontend
frontend_dir = os.path.join(current_dir, "..", "..", "frontend")
app.mount("/", StaticFiles(directory=frontend_dir, html=True), name="frontend")
