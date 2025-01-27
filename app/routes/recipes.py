from bson import ObjectId
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.models.recipe import Recipe, RecipeUpdate
from app.db.mongodb import db
from app.services.cloudinary_service import upload_image_to_cloudinary
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Create an APIRouter instance to group related endpoints
router = APIRouter()

@router.post("/recipes/")
async def create_recipe(recipe: Recipe):
    """
    Create a new recipe in the database.

    Args:
        recipe (Recipe): A Pydantic model representing the recipe data.

    Returns:
        dict: A dictionary containing a success message and the created recipe data.
              The `_id` field is converted from ObjectId to a string for JSON compatibility.
    """
    recipe_dict = recipe.dict()
    result = await db.recipes.insert_one(recipe_dict)
    # Convert ObjectId to string
    recipe_dict["_id"] = str(result.inserted_id)
    return {"message": "Recipe created", "recipe": recipe_dict}

@router.get("/recipes/")
async def get_recipes():
    """
    Retrieve all recipes from the database.

    Returns:
        list: A list of dictionaries, each representing a recipe.
              The `_id` field is converted from ObjectId to a string for JSON compatibility.
    """
    recipes = []
    async for recipe in db.recipes.find():
        recipe["_id"] = str(recipe["_id"])  # Convert ObjectId to string
        recipes.append(recipe)
    return recipes

@router.get("/recipes/{recipe_id}")
async def get_recipe(recipe_id: str):
    """
    Retrieve a single recipe by its ID.

    Args:
        recipe_id (str): The ID of the recipe to retrieve.

    Returns:
        dict: A dictionary representing the recipe.
              The `_id` field is converted from ObjectId to a string for JSON compatibility.

    Raises:
        HTTPException: 404 error if the recipe with the specified ID is not found.
    """
    recipe = await db.recipes.find_one({"_id": ObjectId(recipe_id)})  # Convert string to ObjectId
    if recipe:
        recipe["_id"] = str(recipe["_id"])  # Convert ObjectId to string
        return recipe
    raise HTTPException(status_code=404, detail="Recipe not found")

@router.put("/recipes/{recipe_id}")
async def update_recipe(recipe_id: str, recipe: RecipeUpdate):
    """
    Update an existing recipe by its ID.

    Args:
        recipe_id (str): The ID of the recipe to update.
        recipe (RecipeUpdate): A Pydantic model representing the fields to update.

    Returns:
        dict: A dictionary containing a success message.

    Raises:
        HTTPException: 404 error if the recipe with the specified ID is not found.
    """
    update_data = recipe.dict(exclude_unset=True)
    result = await db.recipes.update_one({"_id": ObjectId(recipe_id)}, {"$set": update_data})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return {"message": "Recipe updated"}

@router.delete("/recipes/{recipe_id}")
async def delete_recipe(recipe_id: str):
    """
    Delete a recipe by its ID.

    Args:
        recipe_id (str): The ID of the recipe to delete.

    Returns:
        dict: A dictionary containing a success message.

    Raises:
        HTTPException: 404 error if the recipe with the specified ID is not found.
    """
    result = await db.recipes.delete_one({"_id": ObjectId(recipe_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return {"message": "Recipe deleted"}

@router.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    """
    Upload an image file to Cloudinary and return the file URL.

    Args:
        file (UploadFile): The image file to upload.

    Returns:
        dict: A dictionary containing the URL of the uploaded file.

    Raises:
        HTTPException: 500 error if the file upload fails.

    Example:
        Response:
            {
                "file_url": "https://res.cloudinary.com/demo/image/upload/v1631234567/image.jpg"
            }
    """
    file_url = upload_image_to_cloudinary(file)
    if file_url:
        return {"file_url": file_url}
    raise HTTPException(status_code=500, detail="File upload failed")