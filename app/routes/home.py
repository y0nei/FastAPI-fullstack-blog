from fastapi import APIRouter
from fastapi import Request
from fastapi.responses import HTMLResponse

from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(
    directory="app/templates",
    lstrip_blocks=True, trim_blocks=True  # Whitespace control
)

home_router = APIRouter(tags=["home"])

@home_router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})
