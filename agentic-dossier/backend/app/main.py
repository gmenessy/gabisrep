from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import os

from app.api.endpoints import router as endpoints_router
import logging

# Configure basic logging
logging.basicConfig(level=logging.INFO)

app = FastAPI(title="Agentic Dossier", description="Air-gapped, privacy-first document analysis system")

# Include routers
app.include_router(endpoints_router)

# Mount the frontend directory using a relative path
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")
