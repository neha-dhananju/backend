from fastapi import FastAPI
from app.api.v1.router import api_router
from app.core.config import settings
from app.core.logging import setup_logging

from fastapi.responses import JSONResponse
from fastapi import Request
from app.utils.exceptions import AppException



setup_logging()

app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0"
)

app.include_router(api_router, prefix="/api")

@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "environment": settings.ENV
    }
@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail}
    )
