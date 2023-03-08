import os
from fastapi import FastAPI, Request, Path, Header, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from app.helpers import parseMarkdown, convertMarkdown, getMetadata
from app.settings import settings
from app.hotreload import initHotreload

app = FastAPI()
app.mount("/static", StaticFiles(directory="app/static"), name="static")

templates = Jinja2Templates(
    directory="app/templates",
    lstrip_blocks=True, trim_blocks=True # Whitespace control
)
initHotreload(app, templates)

# TODO: Add lru cache on settings
if settings.DEBUG == 1:
    print(settings.dict())

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
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

    return templates.TemplateResponse("components/postlist.html", context)

@app.get("/posts")
async def read_post_list(hx_request: str | None = Header(None)):

    if hx_request:
        return {"response": "htmx"}
    else:
        return {"response": "json"}

@app.get("/post/{id}", response_class=HTMLResponse)
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
