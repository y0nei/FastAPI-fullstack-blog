from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from pymongo.errors import OperationFailure, ServerSelectionTimeoutError
from src.core.settings import settings
from src.core.logging import logger
from src.core.database.session import database
from starlette.middleware.sessions import SessionMiddleware
from src.routes.home import home_router
from src.routes.posts import post_router
from src.routes.article import article_router
from src.routes.session import session_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.debug(f"Settings: {settings.dict()}")

    if settings.ENABLE_METRICS:
        Instrumentator().expose(app)
    else:
        logger.warning("Failed to expose instrumentator.")

    logger.info("Connecting to database...")
    try:
        await database.get_database().command("ping")
        logger.info("Pinged your deployment. You successfully connected to MongoDB!")
    except OperationFailure:
        logger.exception("Database Authentication failed.")
    except ServerSelectionTimeoutError:
        logger.exception("Database is unreachable.")

    yield

    database.client.close()
    logger.info("Connection to MongoDB closed.")

app = FastAPI(lifespan=lifespan)
app.mount("/static", StaticFiles(directory="src/static"), name="static")
app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)

# Set the Instrumentator and add middleware to app
if settings.ENABLE_METRICS:
    from prometheus_fastapi_instrumentator import Instrumentator
    Instrumentator().instrument(app)
else:
    logger.warning("Could not add instrumentator middleware.")

app.include_router(home_router)
app.include_router(post_router)
app.include_router(article_router)
app.include_router(session_router)
