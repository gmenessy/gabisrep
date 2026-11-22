from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.api import endpoints
import os
import logging

# Configure basic logging
logging.basicConfig(level=logging.INFO)

app = FastAPI(title="Agentic Dossier")

# Set up CORS if needed (good practice for local dev)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API routes
app.include_router(endpoints.router, prefix="/api/v1")

# Mount frontend directory as static files using absolute path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
frontend_path = os.path.join(BASE_DIR, "frontend")
app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")
