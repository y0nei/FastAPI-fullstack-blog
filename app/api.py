from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from app.settings import settings
from app.routes import home, posts, article
from starlette.middleware.sessions import SessionMiddleware

app = FastAPI()
app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)

# Set the Instrumentator and add middleware to app
if settings.ENABLE_METRICS:
    from prometheus_fastapi_instrumentator import Instrumentator
    instrumentator = Instrumentator().instrument(app)
else:
    print("App metrics are disabled")

@app.on_event("startup")
async def startup():
    if settings.ENABLE_METRICS:
        instrumentator.expose(app)
    else:
        print("App metrics are disabled")

@app.get("/createsession")
async def set_session(request: Request):
    ssid = request.session.get("ssid")
    if not ssid:
        from uuid import uuid4
        ssid = str(uuid4())
        request.session["ssid"] = ssid
        return JSONResponse({"detail": "ssid set sucessfully"}, 200)
    else:
        return JSONResponse({"detail": "ssid already exists in the session"}, 409)

if settings.DEBUG == 1:
    print(settings.dict())

app.include_router(home.home_router)
app.include_router(posts.post_router)
app.include_router(article.article_router)
