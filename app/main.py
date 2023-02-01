from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()

templates = Jinja2Templates(
        directory="app/templates",
        lstrip_blocks=True, trim_blocks=True # Whitespace control
    )

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):

    context = {
        "request": request,
        "message": "Hello World"
    }

    return templates.TemplateResponse("base.html", context)
