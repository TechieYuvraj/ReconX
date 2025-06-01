from fastapi import FastAPI
from app.api.routes import router as api_router

app = FastAPI()

app.include_router(api_router)
app.title = "ReconX Web API"
app.description = "A web API for the ReconX tool, providing endpoints for web crawling and reconnaissance tasks."