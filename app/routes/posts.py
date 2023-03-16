import os
from fastapi import APIRouter, Request, Header
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

    context = {
        "request": request,
        "post_list": sortPosts(posts, sort, order)
    }

    if hx_request:
        return templates.TemplateResponse("components/postlist.html", context)
    else:
        return context["post_list"]
