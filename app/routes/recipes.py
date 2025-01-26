from bson import ObjectId
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.models.recipe import Recipe, RecipeUpdate
from app.db.mongodb import db
from app.services.cloudinary_service import upload_image_to_cloudinary
from dotenv import load_dotenv
import os

load_dotenv()

router = APIRouter()

@router.post("/recipes/")
async def create_recipe(recipe: Recipe):
    recipe_dict = recipe.dict()
    result = await db.recipes.insert_one(recipe_dict)
    # Convert ObjectId to string
    recipe_dict["_id"] = str(result.inserted_id)
    return {"message": "Recipe created", "recipe": recipe_dict}

@router.get("/recipes/")
async def get_recipes():
    recipes = []
    async for recipe in db.recipes.find():
        recipe["_id"] = str(recipe["_id"])  # Convert ObjectId to string
        recipes.append(recipe)
    return recipes

@router.get("/recipes/{recipe_id}")
async def get_recipe(recipe_id: str):
    recipe = await db.recipes.find_one({"_id": ObjectId(recipe_id)})  # Convert string to ObjectId
    if recipe:
        recipe["_id"] = str(recipe["_id"])  # Convert ObjectId to string
        return recipe
    raise HTTPException(status_code=404, detail="Recipe not found")

@router.put("/recipes/{recipe_id}")
async def update_recipe(recipe_id: str, recipe: RecipeUpdate):
    update_data = recipe.dict(exclude_unset=True)
    result = await db.recipes.update_one({"_id": ObjectId(recipe_id)}, {"$set": update_data})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return {"message": "Recipe updated"}

@router.delete("/recipes/{recipe_id}")
async def delete_recipe(recipe_id: str):
    result = await db.recipes.delete_one({"_id": ObjectId(recipe_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return {"message": "Recipe deleted"}

@router.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    file_url = upload_image_to_cloudinary(file)
    if file_url:
        return {"file_url": file_url}
    raise HTTPException(status_code=500, detail="File upload failed")