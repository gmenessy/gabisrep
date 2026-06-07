from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from backend.app.api.endpoints import router as api_router
import os

app = FastAPI(title="Agentic Dossier", description="Air-gapped, privacy-first document analysis system")

# Include API endpoints
app.include_router(api_router, prefix="/api")

# Mount frontend directory as static files
# Calculate path dynamically
current_dir = os.path.dirname(os.path.abspath(__file__))
# current_dir is /app/agentic-dossier/backend/app
# we want /app/agentic-dossier/frontend
frontend_dir = os.path.join(current_dir, "..", "..", "frontend")
frontend_dir = os.path.abspath(frontend_dir)

app.mount("/", StaticFiles(directory=frontend_dir, html=True), name="frontend")
