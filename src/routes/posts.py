import os
from typing import Annotated
import httpx
from fastapi import APIRouter, Request, Header, Query
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from pydantic import BaseModel

from src.utils.helpers.postsorting import sortPosts
from src.utils.helpers.markdown import parseMarkdown
from src.schemas.sorting import SortChoices, OrderChoices
from src.core.templates import templates

post_router = APIRouter(tags=["posts"])

class PostList(BaseModel):
    post_list: dict
    total_pages: int
    current_page: int
    total: int
    pagination: dict[str, str | None]
    tags: list[str]

@post_router.get(
    "/posts",
    response_model=PostList,
    summary="Article listing with pagination functionality",
)
async def post_list(
    request: Request,
    sort: Annotated[SortChoices, Query(
        description="Sort key to order the posts by"
    )] = SortChoices.id,
    order: Annotated[OrderChoices, Query(
        description="Order to sort the post list by"
    )] = OrderChoices.ascending,
    page: int = Query(1, gt=0,
        description="The page of the post listing to view"
    ),
    page_items: int = Query(2, gt=0,
        description="Post items displayed per page"
    ),
    tag: str | None = Query(None,
        description="Display only the posts containing the given tag"
    ),
    hx_request: str | None = Header(None,
        description="""The `hx-request` header is sent automatically by the
        HTMX framework whenever an request is made. It is used to determine
        if this route should return a post list in JSON format or in raw HTML  
        See: [HTMX Request Headers](https://htmx.org/docs/#request-headers)"""
    )
):
    """
    This route handles all the nescessary logic in order to return a (ordered)
    post list with pagination functionality.  
    It either returns the list in a JSON format, or one in HTML if the
    hx-request header is present (Indicates that the response is made by
    HTMX)

    It shows:
    - a list of posts ordered by the selected sort key
    - a list of all avalible tags
    - number of total posts
    - number of total posts displayed on the current page
    - total count of pages
    """

    posts = []
    taglist = []

    def getPost(post_id: int):
        try:
            with open(f"posts/{post_id}/content.md", "r") as f:
                content = f.read()
        except FileNotFoundError:
            raise HTTPException(status_code=404, detail="Post not found")

        metadata, _ = parseMarkdown(content)
        return {"id": post_id, **metadata}

    for post_id in os.listdir("posts"):
        try:
            post_id = int(post_id)
            post = getPost(post_id)
            if post.get("tags"):
                [taglist.append(tag) for tag in post["tags"] if tag not in taglist]
            posts.append(post)
        except ValueError:
            pass

    if tag in taglist:
        posts = [post for post in posts if post.get("tags") and tag in post["tags"]]
    elif tag is not None:
        raise HTTPException(status_code=400, detail=f"The tag [{tag}] does not exist.")

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
        url = httpx.URL(
            path="/posts",
            params={
                "sort": sort.value,
                "order": order.value,
                "page": page-1,
                "page_items": page_items,
            }
        )
        if tag:
            url = url.copy_with(params={"tag": tag})
        pagination["prev"] = str(url)
    else:
        pagination["prev"] = None

    if end_index >= len(posts):
        pagination["next"] = None
    else:
        url = httpx.URL(
            path="/posts",
            params={
                "sort": sort.value,
                "order": order.value,
                "page": page+1,
                "page_items": page_items,
            }
        )
        if tag:
            url = url.copy_with(params={"tag": tag})
        pagination["next"] = str(url)

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
        "pagination": pagination,
        "tags": taglist
    }

    if hx_request:
        return templates.TemplateResponse("components/postlist.html", {"request": request, **context})
    else:
        return JSONResponse(context)
