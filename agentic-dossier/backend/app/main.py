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

# Define paths
FRONTEND_DIR = "frontend"

# Ensure the frontend directory exists before mounting
if os.path.isdir(FRONTEND_DIR):
    app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")
else:
    logging.warning(f"Frontend directory not found at {FRONTEND_DIR}. Please make sure it exists.")
