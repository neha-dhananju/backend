from fastapi import APIRouter
from app.schemas.chat_schema import ChatRequest, ChatResponse

router = APIRouter(prefix="/chat", tags=["Chat"])


@router.post("/", response_model=ChatResponse)
def chat(request: ChatRequest):
    """
    Temporary mock response.
    AI integration will come later.
    """
    return {
        "intent": "unknown",
        "data": {
            "message": request.message
        }
    }
