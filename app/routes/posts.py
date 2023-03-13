import os
from fastapi import APIRouter, Request, Path, Header, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from app.helpers import parseMarkdown, convertMarkdown, getMetadata
from app.hotreload import initHotreload

post_router = APIRouter(tags=["posts"])

templates = Jinja2Templates(
    directory="app/templates",
    lstrip_blocks=True, trim_blocks=True # Whitespace control
)
initHotreload(post_router, templates)

@post_router.get("/posts")
async def read_post_list(
    request: Request,
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
        "post_list": sorted(posts, key=lambda x: x["id"]),
    }

    if hx_request:
        return templates.TemplateResponse("components/postlist.html", context)
    else:
        return context["post_list"]

@post_router.get("/post/{id}", response_class=HTMLResponse)
async def read_post(request: Request, id: int = Path(gt=0)):
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
