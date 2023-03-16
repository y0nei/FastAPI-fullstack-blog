import os
from fastapi import APIRouter, Request, Header, Query, HTTPException
from fastapi.templating import Jinja2Templates
from app.helpers import getMetadata, sortPosts
from app.hotreload import initHotreload
from app.schemas.sorting import SortChoices, OrderChoices

post_router = APIRouter(tags=["posts"])

templates = Jinja2Templates(
    directory="app/templates",
    lstrip_blocks=True, trim_blocks=True # Whitespace control
)
initHotreload(post_router, templates)

@post_router.get("/posts")
async def post_list(
    request: Request,
    sort: SortChoices = SortChoices.id,
    order: OrderChoices = OrderChoices.ascending,
    page: int = Query(1, gt=0),
    page_items: int = Query(5, gt=0),
    hx_request: str | None = Header(None)
):
    posts = []

    def getPost(post_id: int):
        metadata = getMetadata(post_id)
        return {"id": post_id, **metadata}

    for post_id in os.listdir("posts"):
        try:
            post_id = int(post_id)
            post = getPost(post_id)
            posts.append(post)
        except ValueError:
            pass

    posts = sortPosts(posts, sort, order)

    # Simple pagination
    start_index = (page - 1) * page_items
    end_index = start_index + page_items
    current_page_items = posts[start_index:end_index]

    if not current_page_items:
        raise HTTPException(status_code=404, detail="Page doesent exist")

    context = {
        "request": request,
        "post_list": current_page_items
    }

    if hx_request:
        return templates.TemplateResponse("components/postlist.html", context)
    else:
        return context["post_list"]
