"""
Main FastAPI application module for the Agentic Dossier.
Sets up the API routing and mounts the static frontend.
"""

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import os
import logging

from app.api.endpoints import router as endpoints_router

# Configure basic logging
logging.basicConfig(level=logging.INFO)

app = FastAPI(
    title="Agentic Dossier",
    description="Air-gapped, privacy-first document analysis system. Strict data isolation.",
    version="0.1.0"
)

# Include API routers
app.include_router(endpoints_router)

# Define paths for frontend static files
FRONTEND_DIR: str = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "frontend")

# Ensure the frontend directory exists before mounting
if os.path.isdir(FRONTEND_DIR):
    app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")
    logging.info(f"Frontend successfully mounted from {FRONTEND_DIR}")
else:
    logging.warning(f"Frontend directory not found at {FRONTEND_DIR}. Please make sure it exists.")
