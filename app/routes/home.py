from typing import Annotated
from fastapi import APIRouter, Depends, Request
from app.hotreload import initHotreload
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.database import add_view, get_prod_db
from motor.motor_asyncio import AsyncIOMotorCollection as MotorCollection

home_router = APIRouter(tags=["home"])
templates = Jinja2Templates(
    directory="app/templates",
    lstrip_blocks=True, trim_blocks=True  # Whitespace control
)
initHotreload(home_router, templates)

@home_router.get("/", response_class=HTMLResponse)
async def home(request: Request, database: Annotated[MotorCollection, Depends(get_prod_db)]):
    await add_view(request, database)
    return templates.TemplateResponse("home.html", {"request": request})
