from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .api.endpoints import router as endpoints_router
import os

app = FastAPI(title="Agentic Dossier API", version="1.0.0")

# Include the API router
app.include_router(endpoints_router)

# Ensure frontend path is absolute or relative to the working directory
frontend_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "frontend")

# Mount frontend static files
# We mount static files but also handle the root path to serve index.html explicitly
# if not handled by StaticFiles html=True (which it does, but we want to be safe)
app.mount("/", StaticFiles(directory=frontend_dir, html=True), name="frontend")
