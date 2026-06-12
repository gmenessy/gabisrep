import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.api.endpoints import router

app = FastAPI(title="Agentic Dossier", description="Privacy-first document analysis system")

# Include the API routes
app.include_router(router)

# Mount frontend as static files
# Calculate absolute path to the frontend directory relative to this file
current_dir = os.path.dirname(os.path.abspath(__file__))
# current_dir is agentic-dossier/backend/app
# frontend is at agentic-dossier/frontend
frontend_dir = os.path.join(current_dir, "..", "..", "frontend")
frontend_dir = os.path.abspath(frontend_dir)

app.mount("/", StaticFiles(directory=frontend_dir, html=True), name="frontend")
