from typing import Annotated
from fastapi import APIRouter, Request, Path, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.exceptions import HTTPException

from src.core.logging import logger
from src.utils.hotreload import initHotreload
from src.utils.helpers.version import get_git_version, get_git_url_and_branch
from src.utils.helpers.markdown import parseMarkdown, convertMarkdown
from src.utils.word_counter import count_words_in_markdown
from src.core.database.database import get_route_views, add_view
from src.core.database.session import DataBase
from motor.motor_asyncio import AsyncIOMotorDatabase

article_router = APIRouter(tags=["posts"])
# TODO: Dont define templates per route. Move this somewhere else
templates = Jinja2Templates(
    directory="src/templates",
    lstrip_blocks=True, trim_blocks=True  # Whitespace control
)
initHotreload(templates)
templates.env.globals["git_version"] = get_git_version()
templates.env.globals["git_url"] = get_git_url_and_branch().get("url")

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
    word_count = count_words_in_markdown(body)

    context = {
        "id": id,
        **metadata,
        "word_count": word_count,
        "body": convertMarkdown(body)
    }

    if isinstance(db, AsyncIOMotorDatabase):
        route_views = await get_route_views(f"/posts/{id}", db)
        context.update({"views": route_views})

    return templates.TemplateResponse("components/article.html", {"request": request, **context})
