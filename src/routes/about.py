from fastapi import APIRouter
from fastapi.responses import JSONResponse

about_router = APIRouter()

@about_router.get(
    "/about",
    summary="About page, TOS, privacy policy etc.",
)
async def about():
    """
    Not Yet Implemented
    """

    return JSONResponse({"detail": "not implemented"}, 501)
