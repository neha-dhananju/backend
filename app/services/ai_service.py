import json
import re
import logging
from app.core.config import settings
from app.integrations.gemini_client import GeminiClient
from app.integrations.openai_client import OpenAIClient
from app.utils.ai_prompt import intent_prompt

logger = logging.getLogger(__name__)


class AIService:
    def __init__(self):
        self.client = (
            GeminiClient()
            if settings.AI_PROVIDER == "gemini"
            else OpenAIClient()
        )
    def _fallback_intent(self, message: str) -> dict:
        msg = message.lower()

        if any(word in msg for word in ["have", "only", "ingredients"]):
            return {
                "intent": "ingredient_search",
                "ingredients": []
            }
        if any(word in msg for word in ["cook", "make", "prepare"]):
            return {
                "intent": "recipe_search",
                "recipe": message
            }
        return {"intent": "unknown"}


    
    def parse_message(self, message: str) -> dict:
        try:
            prompt = intent_prompt(message)
            raw_response = self.client.parse(prompt)

            import re, json
            json_match = re.search(r"\{.*\}", raw_response, re.DOTALL)

            if not json_match:
                return self._fallback_intent(message)

            parsed = json.loads(json_match.group())

        # 🔒 Final validation
            if parsed.get("intent") not in ["ingredient_search", "recipe_search"]:
                return self._fallback_intent(message)

            return parsed

        except Exception:
            return self._fallback_intent(message)