from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import os
from .api.endpoints import router as api_router

app = FastAPI(title="Agentic Dossier API")

# Add CORS middleware if needed
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(api_router, prefix="/api/v1")

# Mount frontend as static files
# Compute dynamic absolute path for static files mounting
base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
frontend_dir = os.path.join(base_dir, "frontend")

app.mount("/", StaticFiles(directory=frontend_dir, html=True), name="frontend")
