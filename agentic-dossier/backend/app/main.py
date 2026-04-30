from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.api import endpoints

app = FastAPI(title="Agentic Dossier API", description="Air-gapped, privacy-first document analysis system")

# Include the endpoints router
app.include_router(endpoints.router, prefix="/api/v1/dossier", tags=["dossier"])

# Mount the frontend directory as static files so the UI is served at /
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")
