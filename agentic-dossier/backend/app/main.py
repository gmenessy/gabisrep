from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.api.endpoints import router as api_router
import os

app = FastAPI(title="Agentic Dossier")

# Include API router
app.include_router(api_router)

# Mount frontend directory
# We use dynamic absolute paths computed via __file__ as per memory guidelines
current_dir = os.path.dirname(os.path.abspath(__file__))
# Navigate up to backend then to frontend
frontend_dir = os.path.abspath(os.path.join(current_dir, "../../frontend"))
app.mount("/", StaticFiles(directory=frontend_dir, html=True), name="frontend")
