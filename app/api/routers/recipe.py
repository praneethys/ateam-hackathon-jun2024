from typing import List
from fastapi import APIRouter

from app.schema.index import IngredientList
from app.service.recipes import generate_recipes

recipe_router = r = APIRouter(prefix="/api/v1/recipes", tags=["recipes"])


@r.post(
    "/",
    responses={
        200: {"description": "Recipes generated"},
        500: {"description": "Internal server error"},
    },
)
def post_recipes(ingredients: IngredientList):
    """
    This function is an API endpoint that accepts a list of ingredients as input and generates a list of recipes.

    Parameters:
    - ingredients (List[str]): A list of strings representing the ingredients for the recipes.

    Returns:
    - recipes (List[str]): A list of strings representing the generated recipes.

    The function uses the `generate_recipes` function to generate the recipes based on the provided ingredients. The generated recipes are then returned as a list of strings.

    The API endpoint responds with a status code of 200 if the recipes are generated successfully, and a status code of 500 if there is an internal server error.
    """

    ingredients_list = ingredients.model_dump()["ingredients"]

    recipes = generate_recipes(ingredients_list)

    return recipes
