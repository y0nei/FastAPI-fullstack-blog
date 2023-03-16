from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.settings import settings
from app.routes import home, posts, article

app = FastAPI()
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# TODO: Add lru cache on settings
if settings.DEBUG == 1:
    print(settings.dict())

app.include_router(home.home_router)
app.include_router(posts.post_router)
app.include_router(article.article_router)
