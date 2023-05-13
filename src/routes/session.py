from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

session_router = APIRouter()

@session_router.get("/createsession")
async def set_session(request: Request):
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
