# from fastapi import FastAPI
# from app.api.routes import router as api_router

# app = FastAPI()

# app.include_router(api_router)
# app.title = "ReconX Web API"
# app.description = "A web API for the ReconX tool, providing endpoints for web crawling and reconnaissance tasks."

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()

# Serve static files (CSS, JS)
app.mount("/static", StaticFiles(directory="frontend"), name="static")

# HTML templates
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def get_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

