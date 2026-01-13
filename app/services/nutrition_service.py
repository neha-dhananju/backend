from app.integrations.fatsecret_client import FatSecretClient

client = FatSecretClient()


class NutritionService:

    def get_nutrition(self, recipe_title: str):
        """
        Best-effort nutrition lookup.
        Returns None if nutrition not found.
        """
        query = self._normalize_title(recipe_title)
        result = client.search_food(query)

        foods = result.get("foods", {}).get("food", [])
        if not foods:
            return None

        food = foods[0]

        return {
            "name": food.get("food_name"),
            "calories": food.get("food_description"),
            "source": "fatsecret"
        }

    def _normalize_title(self, title: str) -> str:
        """
        Normalize recipe title to improve FatSecret match rate
        """
        words_to_remove = [
            "instant", "pot", "easy", "homemade",
            "authentic", "style", "recipe"
        ]

        cleaned = title.lower()
        for word in words_to_remove:
            cleaned = cleaned.replace(word, "")

        return cleaned.strip()
