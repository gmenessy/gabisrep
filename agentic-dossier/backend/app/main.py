from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.api.endpoints import router as api_router
import os

app = FastAPI(title="Agentic Dossier")

app.include_router(api_router)

# Mount the frontend directory as static files on the root
# Ensure that the frontend directory path is resolved properly
frontend_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "frontend")
app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")
