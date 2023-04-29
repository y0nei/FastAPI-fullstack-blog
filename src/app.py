from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from src.core.settings import settings
from src.core.logging import logger
from starlette.middleware.sessions import SessionMiddleware
from src.routes.home import home_router
from src.routes.posts import post_router
from src.routes.article import article_router
from src.routes.session import session_router

app = FastAPI()
app.mount("/static", StaticFiles(directory="src/static"), name="static")
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

app.include_router(home_router)
app.include_router(post_router)
app.include_router(article_router)
app.include_router(session_router)
