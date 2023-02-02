import os
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import markdown
from app.helpers import parseMarkdown, getMetadata

app = FastAPI()
app.mount("/static", StaticFiles(directory="app/static"), name="static")

templates = Jinja2Templates(
        directory="app/templates",
        lstrip_blocks=True, trim_blocks=True # Whitespace control
    )

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    posts = []

    for post_id in os.listdir("posts"):
        try:
            post_id = int(post_id)
            post = getMetadata(post_id)
            posts.append(post)
        except ValueError:
            pass

    context = {
        "request": request,
        "post_list": sorted(posts, key=lambda x: x["id"]),
        "message": "Hello World"
    }

    return templates.TemplateResponse("components/postlist.html", context)

@app.get("/post/{id}", response_class=HTMLResponse)
async def read_post(request: Request, id: int):
    try:
        with open(f"posts/{id}/content.md", "r") as f:
            content = f.read()
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Post not found")

    metadata, body = parseMarkdown(content)
    body = markdown.Markdown().convert(body)

    context = {
        "request": request,
        "id": id,
        **metadata,
        "body": body
    }

    return templates.TemplateResponse("components/article.html", context)
