from typing import Annotated
from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from src.core.logging import logger
from src.utils.hotreload import initHotreload
from src.utils.helpers.version import get_git_version, get_git_url_and_branch
from src.core.database.database import add_view
from src.core.database.session import DataBase
from motor.motor_asyncio import AsyncIOMotorDatabase

home_router = APIRouter(tags=["home"])
# TODO: Dont define templates per route. Move this somewhere else
templates = Jinja2Templates(
    directory="src/templates",
    lstrip_blocks=True, trim_blocks=True  # Whitespace control
)
initHotreload(templates)
templates.env.globals["git_version"] = get_git_version()
templates.env.globals["git_url"] = get_git_url_and_branch().get("url")

@home_router.get("/", response_class=HTMLResponse)
async def home(
    request: Request,
    db: Annotated[AsyncIOMotorDatabase | None, Depends(DataBase().get_database)]
):
    if isinstance(db, AsyncIOMotorDatabase):
        ssid = request.session.get("ssid")
        if ssid:
            await add_view(request.url.path, ssid, db)
        else:
            logger.debug("Ssid not found in session")

    return templates.TemplateResponse("home.html", {"request": request})
