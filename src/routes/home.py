from typing import Annotated
from fastapi import APIRouter, Depends, Request
from src.utils.hotreload import initHotreload
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from src.core.database.database import add_view
from src.core.database.session import database
from src.core.logging import logger
from motor.motor_asyncio import AsyncIOMotorDatabase

home_router = APIRouter(tags=["home"])
templates = Jinja2Templates(
    directory="src/templates",
    lstrip_blocks=True, trim_blocks=True  # Whitespace control
)
initHotreload(home_router, templates)

@home_router.get("/", response_class=HTMLResponse)
async def home(request: Request, db: Annotated[AsyncIOMotorDatabase, Depends(database.get_database)]):
    ssid = request.session.get("ssid")
    if ssid:
        await add_view(request.url.path, ssid, db)
    else:
        logger.debug("Ssid not found in session")

    return templates.TemplateResponse("home.html", {"request": request})