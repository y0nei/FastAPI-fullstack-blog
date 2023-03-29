from fastapi import APIRouter
from fastapi import Request
from app.hotreload import initHotreload
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.database import add_view

home_router = APIRouter(tags=["home"])
templates = Jinja2Templates(
    directory="app/templates",
    lstrip_blocks=True, trim_blocks=True  # Whitespace control
)
initHotreload(home_router, templates)

@home_router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    await add_view(request)
    return templates.TemplateResponse("home.html", {"request": request})
