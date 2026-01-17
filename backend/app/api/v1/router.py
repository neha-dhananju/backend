from fastapi import APIRouter
from app.api.v1.routes import chat
from app.api.v1.routes import chat, recipes




api_router = APIRouter()

api_router.include_router(chat.router)

api_router.include_router(recipes.router)