import os
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from app.helpers import parseMarkdown, convertMarkdown, getMetadata
from app.settings import settings

app = FastAPI()
app.mount("/static", StaticFiles(directory="app/static"), name="static")

templates = Jinja2Templates(
    directory="app/templates",
    lstrip_blocks=True, trim_blocks=True # Whitespace control
)

if settings.DEBUG == 1 and settings.ENVIROMENT == "development":
    try:
        import arel

        async def reload_data():
            print("Reloading server data...")

        # TODO: Read Arel reload dirs to settings
        app.add_middleware(arel.HotReloadMiddleware, paths=[
            arel.Path("posts", on_reload=[reload_data]),
            arel.Path("app/templates")
        ])
    except ImportError:
        print(">Arel could not be successfully imported",
              "\n>Make sure your docker build args match the enviroment")
else:
    print(">DEBUG env variable is set to:", settings.DEBUG,
          "\n>To enable browser hotreloading set it to 1")

# TODO: Add lru cache on settings
if settings.DEBUG == 1:
    print(settings.dict())

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

    context = {
        "request": request,
        "id": id,
        **metadata,
        "body": convertMarkdown(body)
    }

    return templates.TemplateResponse("components/article.html", context)
