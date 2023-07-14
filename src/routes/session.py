from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

session_router = APIRouter()

@session_router.get("/createsession", summary="Create a cookie session")
async def set_session(request: Request):
    """
    This route is used to generate a UUID4 session token, if the user
    already has a session token, return a **409** error.  
    If the post statistics functionality is not enabled, return a **501**

    **This route is needed in order to identify the user as a view for article
    statistics.**
    """

    try:
        ssid = request.session.get("ssid")
        if not ssid:
            from uuid import uuid4
            ssid = str(uuid4())
            request.session["ssid"] = ssid
            return JSONResponse({"detail": "ssid set sucessfully"})
        else:
            return JSONResponse({"detail": "ssid already exists in the session"}, 409)
    except AssertionError as e:
        return JSONResponse({
            "error": f"{e}",
            "detail": "Post statistics functionality not enabled"
        }, 501)
