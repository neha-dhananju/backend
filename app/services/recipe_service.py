from app.integrations.spoonacular_client import SpoonacularClient
from app.services.nutrition_service import NutritionService
from app.services.video_service import VideoService
from app.services.cache_service import CacheService

cache = CacheService()
video_service = VideoService()
client = SpoonacularClient()
nutrition_service = NutritionService()


class RecipeService:

    def search_recipes(
        self,
        query: str | None,
        ingredients: list[str] | None,
        page: int,
        page_size: int,
        filters: dict
    ):
        offset = (page - 1) * page_size

        data = client.search(
            query=query,
            ingredients=ingredients,
            offset=offset,
            limit=page_size,
            filters=filters
        )

        recipes = []
        for r in data.get("results", []):
            recipes.append({
                "id": r["id"],
                "title": r["title"],
                "image": r.get("image"),
                "ready_in_minutes": r.get("readyInMinutes")
            })

        return {
            "page": page,
            "page_size": page_size,
            "total": data.get("totalResults", 0),
            "recipes": recipes
        }

    def get_recipe_detail(self, recipe_id: int):
        # ✅ 1. Check cache first
        cache_key = f"recipe_detail:{recipe_id}"
        cached = cache.get(cache_key)
        if cached:
            return cached

        # ✅ 2. Fetch from Spoonacular
        data = client.get_recipe_details(recipe_id)

        # ✅ 3. Enrich data (best-effort)
        video = video_service.get_video(data["title"])
        nutrition = nutrition_service.get_nutrition(data["title"])

        ingredients = [
            i["original"]
            for i in data.get("extendedIngredients", [])
        ]

        steps = []
        instructions = data.get("analyzedInstructions", [])
        if instructions:
            steps = [
                step["step"]
                for step in instructions[0].get("steps", [])
            ]

        # ✅ 4. Build response
        response = {
            "id": data["id"],
            "title": data["title"],
            "image": data.get("image"),
            "ready_in_minutes": data.get("readyInMinutes"),
            "ingredients": ingredients,
            "steps": steps,
            "nutrition": nutrition,
            "source_url": data.get("sourceUrl"),
            "video": video
        }

        # ✅ 5. Store in cache (CRITICAL)
        cache.set(cache_key, response, ttl=3600)

        return response
