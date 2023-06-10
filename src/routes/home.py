from typing import Annotated
from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse

from src.core.logging import logger
from src.core.database.database import add_view
from src.core.database.session import DataBase
from src.core.templates import templates
from motor.motor_asyncio import AsyncIOMotorDatabase

home_router = APIRouter(tags=["home"])

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
