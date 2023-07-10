from fastapi import APIRouter
from fastapi.responses import JSONResponse

about_router = APIRouter()

@about_router.get("/about")
async def about():
    return JSONResponse({"detail": "not implemented"}, 501)
