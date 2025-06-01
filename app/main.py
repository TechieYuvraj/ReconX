# # app/main.py
# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from app.api.routes import router as api_router

# app = FastAPI(title="ReconX Web API")

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# app.include_router(api_router, prefix="/api")

from fastapi import FastAPI
from app.api.routes import router as api_router

app = FastAPI()

app.include_router(api_router)
app.title = "ReconX Web API"
app.description = "A web API for the ReconX tool, providing endpoints for web crawling and reconnaissance tasks."