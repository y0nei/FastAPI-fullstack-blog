import uvicorn
from app.settings import settings

if __name__ == "__main__":
    uvicorn.run(
        app="app.api:app",
        host=settings.APP_HOST,
        port=settings.APP_PORT,
        log_level=settings.LOG_LEVEL,
        use_colors=True,
        reload=True if settings.ENVIRONMENT != "production" else False
    )
