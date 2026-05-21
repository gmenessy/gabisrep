import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.api import endpoints

app = FastAPI(title="Agentic Dossier API", description="Privacy-first document analysis system")

# Include the endpoints router
app.include_router(endpoints.router, prefix="/api/v1")

# Mount the frontend static files
frontend_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "frontend")

# Make sure frontend directory exists (it should, as we created it)
os.makedirs(frontend_dir, exist_ok=True)

app.mount("/", StaticFiles(directory=frontend_dir, html=True), name="frontend")
