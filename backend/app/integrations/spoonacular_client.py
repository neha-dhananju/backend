import httpx
from app.core.config import settings


class SpoonacularClient:
    BASE_URL = "https://api.spoonacular.com/recipes"

    def __init__(self):
        self.api_key = settings.SPOONACULAR_API_KEY

    def search(
        self,
        query: str | None,
        ingredients: list[str] | None,
        offset: int,
        limit: int,
        filters: dict
    ):
        params = {
            "apiKey": self.api_key,
            "number": limit,
            "offset": offset,
        }

        if query:
            params["query"] = query

        if ingredients:
            params["includeIngredients"] = ",".join(ingredients)

        if filters.get("max_time"):
            params["maxReadyTime"] = filters["max_time"]

        if filters.get("diet"):
            params["diet"] = filters["diet"]

        if filters.get("cuisine"):
            params["cuisine"] = filters["cuisine"]

        response = httpx.get(
            f"{self.BASE_URL}/complexSearch",
            params=params,
            timeout=10
        )
        response.raise_for_status()
        return response.json()

    def get_recipe_details(self, recipe_id: int):
        params = {
        "apiKey": self.api_key,
        "includeNutrition": False
        }

        response = httpx.get(
        f"{self.BASE_URL}/{recipe_id}/information",
        params=params,
        timeout=10
        )
        response.raise_for_status()
        return response.json()