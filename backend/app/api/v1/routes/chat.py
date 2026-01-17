from fastapi import APIRouter
from app.schemas.chat_schema import ChatRequest, ChatResponse
from app.services.ai_service import AIService

router = APIRouter(prefix="/chat", tags=["Chat"])

ai_service = AIService()


@router.post("/", response_model=ChatResponse)
def chat(request: ChatRequest):
    result = ai_service.parse_message(request.message)

    return {
        "intent": result.get("intent"),
        "data": result
    }
