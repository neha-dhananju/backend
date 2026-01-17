from pydantic import BaseModel
from typing import List, Optional


class RecipeFilter(BaseModel):
    max_calories: Optional[int] = None
    max_time: Optional[int] = None
    cuisine: Optional[str] = None
    diet: Optional[str] = None


class RecipeResponse(BaseModel):
    id: int
    title: str
    image: str
    ready_in_minutes: Optional[int] = None
    calories: Optional[int] = None
