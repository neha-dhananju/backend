def intent_prompt(user_message: str) -> str:
    return f"""
You are an API, not a chatbot.

You MUST return valid JSON.
You MUST follow the schema exactly.
DO NOT add explanations or text.

Decide intent:
- ingredient_search → if user mentions ingredients they have
- recipe_search → if user asks to cook or make a dish

If intent = ingredient_search:
- extract ingredient names only (singular, lowercase)

If intent = recipe_search:
- extract recipe name only

User message:
"{user_message}"

Return EXACTLY this JSON schema:

{{
  "intent": "ingredient_search | recipe_search | unknown",
  "ingredients": [],
  "recipe": ""
}}
"""
