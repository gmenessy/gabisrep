import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from backend.app.api.endpoints import router as api_router

app = FastAPI(title="Agentic Dossier API")

# Include the API routes
app.include_router(api_router)

# Mount frontend as static files at root
# Compute absolute path to ensure portability
frontend_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "frontend")
app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")
