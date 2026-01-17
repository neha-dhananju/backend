from fastapi import APIRouter, Query
from app.services.recipe_service import RecipeService
from fastapi import Depends, Request
from app.core.rate_limiter import rate_limit


router = APIRouter(prefix="/recipes", tags=["Recipes"])

service = RecipeService()

@router.get("/{recipe_id}")
def recipe_detail(
    recipe_id: int,
    request: Request,
    _: None = Depends(rate_limit)
):
    return service.get_recipe_detail(recipe_id)


@router.get("/")
def search_recipes(
    query: str | None = None,
    ingredients: str | None = None,
    page: int = 1,
    page_size: int = 10,
    max_time: int | None = None,
    cuisine: str | None = None,
    diet: str | None = None
):
    ingredient_list = ingredients.split(",") if ingredients else None

    filters = {
        "max_time": max_time,
        "cuisine": cuisine,
        "diet": diet,
    }

    return service.search_recipes(
        query=query,
        ingredients=ingredient_list,
        page=page,
        page_size=page_size,
        filters=filters
    )
@router.get("/{recipe_id}")
def recipe_detail(recipe_id: int):
    return service.get_recipe_detail(recipe_id)
