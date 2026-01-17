from app.integrations.spoonacular_client import SpoonacularClient
from app.services.nutrition_service import NutritionService
from app.services.video_service import VideoService
from app.services.cache_service import CacheService

# Initialize shared services
cache = CacheService()
client = SpoonacularClient()
nutrition_service = NutritionService()
video_service = VideoService()


class RecipeService:
    """
    Handles recipe search and recipe detail logic
    """

    def search_recipes(
        self,
        query: str | None,
        ingredients: list[str] | None,
        page: int,
        page_size: int,
        filters: dict
    ):
        # -------------------------
        # 1. Cache lookup
        # -------------------------
        cache_key = f"recipes:list:{query}:{ingredients}:{page}:{page_size}:{filters}"
        cached = cache.get(cache_key)
        if cached:
            return cached

        # -------------------------
        # 2. Fetch from Spoonacular
        # -------------------------
        offset = (page - 1) * page_size

        data = client.search(
            query=query,
            ingredients=ingredients,
            offset=offset,
            limit=page_size,
            filters=filters
        )

        # -------------------------
        # 3. Normalize response
        # -------------------------
        recipes = []
        for r in data.get("results", []):
            recipes.append({
                "id": r.get("id"),
                "title": r.get("title"),
                "image": r.get("image"),
                "ready_in_minutes": r.get("readyInMinutes")
            })

        # -------------------------
        # 4. Build response object
        # -------------------------
        response = {
            "page": page,
            "page_size": page_size,
            "total": data.get("totalResults", 0),
            "recipes": recipes
        }

        # -------------------------
        # 5. Cache result (10 mins)
        # -------------------------
        cache.set(cache_key, response, ttl=600)

        return response

    def get_recipe_detail(self, recipe_id: int):
        # -------------------------
        # 1. Cache lookup
        # -------------------------
        cache_key = f"recipe:detail:{recipe_id}"
        cached = cache.get(cache_key)
        if cached:
            return cached

        # -------------------------
        # 2. Fetch recipe details
        # -------------------------
        data = client.get_recipe_details(recipe_id)

        # -------------------------
        # 3. Enrich data
        # -------------------------
        video = video_service.get_video(data.get("title"))
        nutrition = nutrition_service.get_nutrition(data.get("title"))

        ingredients = [
            i.get("original")
            for i in data.get("extendedIngredients", [])
        ]

        steps = []
        instructions = data.get("analyzedInstructions", [])
        if instructions:
            steps = [
                step.get("step")
                for step in instructions[0].get("steps", [])
            ]

        # -------------------------
        # 4. Build response
        # -------------------------
        response = {
            "id": data.get("id"),
            "title": data.get("title"),
            "image": data.get("image"),
            "ready_in_minutes": data.get("readyInMinutes"),
            "ingredients": ingredients,
            "steps": steps,
            "nutrition": nutrition,
            "source_url": data.get("sourceUrl"),
            "video": video
        }

        # -------------------------
        # 5. Cache result (1 hour)
        # -------------------------
        cache.set(cache_key, response, ttl=3600)

        return response
