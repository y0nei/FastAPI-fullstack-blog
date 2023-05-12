from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from pymongo.errors import OperationFailure, ServerSelectionTimeoutError

from src.core.logging import logger
from src.core.settings import settings
from src.core.database.session import DataBase
from src.routes.home import home_router
from src.routes.posts import post_router
from src.routes.article import article_router
from src.routes.session import session_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.debug(f"Settings: {settings.dict()}")

    if settings.HOTRELOAD:
        await hotreload.startup()
        logger.info("Hotreloading started.")

    if settings.ENABLE_METRICS:
        Instrumentator().expose(app)
    else:
        logger.warning("Failed to expose instrumentator.")

    if settings.POST_STATISTICS:
        try:
            logger.info("Connecting to database...")
            await DataBase().get_database().command("ping")
            logger.info("Pinged your deployment. You are connected to MongoDB!")
        except OperationFailure:
            logger.exception("Database Authentication failed.")
        except ServerSelectionTimeoutError:
            logger.exception("Database is unreachable.")
    yield
    if settings.HOTRELOAD:
        await hotreload.shutdown()
        logger.info("Hotreloading shutdown.")

    if settings.POST_STATISTICS:
        DataBase().client.close()
        logger.info("Connection to MongoDB closed.")

app = FastAPI(lifespan=lifespan)
app.mount("/static", StaticFiles(directory="src/static"), name="static")

if settings.HOTRELOAD:
    from src.utils.hotreload import hotreload
    from starlette.routing import WebSocketRoute
    app.routes.append(WebSocketRoute("/hot-reload", hotreload, name="hot-reload"))
else:
    logger.warning("Could not initialize hotreloading.")

if settings.POST_STATISTICS:
    from starlette.middleware.sessions import SessionMiddleware
    app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)
else:
    logger.warning("Could not add cookie session middleware.")

if settings.ENABLE_METRICS:
    from prometheus_fastapi_instrumentator import Instrumentator
    Instrumentator().instrument(app)  # NOTE: Adds middleware
else:
    logger.warning("Could not add instrumentator middleware.")

app.include_router(home_router)
app.include_router(post_router)
app.include_router(article_router)
app.include_router(session_router)
