import os
from fastapi import APIRouter, Request, Header, Query, HTTPException
from fastapi.templating import Jinja2Templates
from app.helpers import getMetadata, sortPosts
from app.schemas.sorting import SortChoices, OrderChoices

post_router = APIRouter(tags=["posts"])

templates = Jinja2Templates(
    directory="app/templates",
    lstrip_blocks=True, trim_blocks=True  # Whitespace control
)

@post_router.get("/posts")
async def post_list(
    request: Request,
    sort: SortChoices = SortChoices.id,
    order: OrderChoices = OrderChoices.ascending,
    page: int = Query(1, gt=0),
    page_items: int = Query(2, gt=0),
    hx_request: str | None = Header(None)
):
    posts = []

    def getPost(post_id: int):
        metadata = getMetadata(post_id)
        return {"id": post_id, **metadata}

    for post_id in os.listdir("posts"):
        try:
            post_id = int(post_id)
            post = getPost(post_id)
            posts.append(post)
        except ValueError:
            pass

    posts = sortPosts(posts, sort, order)

    # Simple pagination
    start_index = (page - 1) * page_items
    end_index = start_index + page_items
    current_page_items = posts[start_index:end_index]

    if not current_page_items:
        raise HTTPException(status_code=404, detail="Page doesent exist")

    # next and previous pages
    pagination = {}
    if page > 1:
        pagination["prev"] = f"/posts?sort={sort.value}&order={order.value}&page={page-1}&page_items={page_items}"
    else:
        pagination["prev"] = None

    if end_index >= len(posts):
        pagination["next"] = None
    else:
        pagination["next"] = f"/posts?sort={sort.value}&order={order.value}&page={page+1}&page_items={page_items}"

    # Total pages
    if len(posts) <= page_items:
        total_pages = 1
    else:
        total_pages = (len(posts) + page_items - 1) // page_items

    context = {
        "post_list": current_page_items,
        "total_pages": total_pages,
        "current_page": page,
        "total": len(posts),
        "pagination": pagination
    }

    if hx_request:
        return templates.TemplateResponse("components/postlist.html", {"request": request, **context})
    else:
        return context
