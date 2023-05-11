from typing import Annotated
from fastapi import APIRouter, Request, Path, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.exceptions import HTTPException

from src.core.logging import logger
from src.utils.hotreload import initHotreload
from src.utils.helpers.markdown import parseMarkdown, convertMarkdown
from src.core.database.database import get_route_views, add_view
from src.core.database.session import DataBase
from motor.motor_asyncio import AsyncIOMotorDatabase

article_router = APIRouter(tags=["posts"])
templates = Jinja2Templates(
    directory="src/templates",
    lstrip_blocks=True, trim_blocks=True  # Whitespace control
)
initHotreload(article_router, templates)

@article_router.get("/posts/{id}", response_class=HTMLResponse)
async def article(
    request: Request,
    db: Annotated[AsyncIOMotorDatabase | None, Depends(DataBase().get_database)],
    id: int = Path(gt=0)
):
    if isinstance(db, AsyncIOMotorDatabase):
        ssid = request.session.get("ssid")
        if ssid:
            await add_view(request.url.path, ssid, db)
        else:
            logger.debug(f"Ssid not found in session, {request.session}")

    try:
        with open(f"posts/{id}/content.md", "r") as f:
            content = f.read()
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Post not found")

    metadata, body = parseMarkdown(content)

    context = {
        "id": id,
        **metadata,
        "body": convertMarkdown(body)
    }

    if isinstance(db, AsyncIOMotorDatabase):
        route_views = await get_route_views(f"/posts/{id}", db)
        context.update({"views": route_views})

    return templates.TemplateResponse("components/article.html", {"request": request, **context})
