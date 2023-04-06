from typing import Annotated
from fastapi import APIRouter, Request, Path, HTTPException, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from app.hotreload import initHotreload
from app.helpers import parseMarkdown, convertMarkdown
from app.database import get_route_views, add_view, get_prod_db
from motor.motor_asyncio import AsyncIOMotorCollection as MotorCollection

article_router = APIRouter(tags=["posts"])

templates = Jinja2Templates(
    directory="app/templates",
    lstrip_blocks=True, trim_blocks=True # Whitespace control
)
initHotreload(article_router, templates)

@article_router.get("/posts/{id}", response_class=HTMLResponse)
async def article(
        request: Request,
        database: Annotated[MotorCollection, Depends(get_prod_db)],
        id: int = Path(gt=0)
):
    await add_view(request, database)
    try:
        with open(f"posts/{id}/content.md", "r") as f:
            content = f.read()
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Post not found")

    metadata, body = parseMarkdown(content)

    context = {
        "id": id,
        **metadata,
        "views": await get_route_views(f"/posts/{id}", database),
        "body": convertMarkdown(body)
    }

    return templates.TemplateResponse("components/article.html", {"request": request, **context})
