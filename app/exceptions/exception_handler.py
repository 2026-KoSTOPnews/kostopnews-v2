from fastapi import Request
from fastapi.responses import JSONResponse

from app.exceptions.custom_exception import CustomException

async def custom_exception_handler(request: Request, exc: CustomException) -> JSONResponse:
    content = {
        "status": exc.status.value,
        "code": exc.error.code,
        "message": exc.error.message,
    }

    if exc.detail:
        content["detail"] = exc.detail

    return JSONResponse(
        status_code=exc.status.value,
        content=content,
    )

async def global_exception_handler(request: Request, exc: Exception,) -> JSONResponse:
    return JSONResponse(
        status_code=500,
        content={
            "status": 500,
            "code": "INTERNAL_SERVER_ERROR",
            "message": "Internal server error.",
        },
    )