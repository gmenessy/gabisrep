from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import os
from .api import endpoints

app = FastAPI()

app.include_router(endpoints.router)

frontend_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "frontend")
app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")
