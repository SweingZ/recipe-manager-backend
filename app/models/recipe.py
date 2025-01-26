from pydantic import BaseModel
from typing import Optional

class Recipe(BaseModel):
    title: str
    ingredients: list[str]
    instructions: str
    image_url: Optional[str] = None

class RecipeUpdate(BaseModel):
    title: Optional[str] = None
    ingredients: Optional[list[str]] = None
    instructions: Optional[str] = None
    image_url: Optional[str] = None