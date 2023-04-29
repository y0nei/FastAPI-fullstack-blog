from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.settings import settings, logger
from app.routes import home, posts, article, session
from starlette.middleware.sessions import SessionMiddleware

app = FastAPI()
app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)

# Set the Instrumentator and add middleware to app
if settings.ENABLE_METRICS:
    from prometheus_fastapi_instrumentator import Instrumentator
    instrumentator = Instrumentator().instrument(app)
else:
    logger.warning("App metrics are disabled")

@app.on_event("startup")
async def startup():
    logger.debug(f"Settings: {settings.dict()}")
    if settings.ENABLE_METRICS:
        instrumentator.expose(app)
    else:
        logger.warning("App metrics are disabled")

app.include_router(home.home_router)
app.include_router(posts.post_router)
app.include_router(article.article_router)
app.include_router(session.session_router)
