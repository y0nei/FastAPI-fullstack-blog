from typing import Annotated
from fastapi import APIRouter, Request, Path, HTTPException, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from src.utils.hotreload import initHotreload
from src.utils.helpers.markdown import parseMarkdown, convertMarkdown
from src.core.database.database import get_route_views, add_view
from src.core.database.session import database
from src.core.logging import logger
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
    db: Annotated[AsyncIOMotorDatabase, Depends(database.get_database)],
    id: int = Path(gt=0)
):
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
    route_views = await get_route_views(f"/posts/{id}", db)

    context = {
        "id": id,
        **metadata,
        "views": route_views,
        "body": convertMarkdown(body)
    }

    return templates.TemplateResponse("components/article.html", {"request": request, **context})
