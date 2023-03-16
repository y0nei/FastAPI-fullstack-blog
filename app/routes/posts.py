import os
from fastapi import APIRouter, Request, Path, Header, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from app.helpers import parseMarkdown, convertMarkdown, getMetadata, sortPosts
from app.hotreload import initHotreload
from app.schemas.sorting import SortChoices, OrderChoices

post_router = APIRouter(tags=["posts"])

templates = Jinja2Templates(
    directory="app/templates",
    lstrip_blocks=True, trim_blocks=True # Whitespace control
)
initHotreload(post_router, templates)

@post_router.get("/")
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

@post_router.get("/{id}", response_class=HTMLResponse)
async def article(request: Request, id: int = Path(gt=0)):
    try:
        with open(f"posts/{id}/content.md", "r") as f:
            content = f.read()
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Post not found")

    metadata, body = parseMarkdown(content)

    context = {
        "request": request,
        "id": id,
        **metadata,
        "body": convertMarkdown(body)
    }

    return templates.TemplateResponse("components/article.html", context)
