from typing import List
from fastapi import APIRouter

from app.service.ingredients import get_ingredients_from_db

ingredient_router = r = APIRouter(prefix="/api/v1/ingredients", tags=["ingredients"])


@r.get(
    "/",
    response_model=List[str],
    responses={
        200: {"description": "Ingredients found"},
        500: {"description": "Internal server error"},
    },
)
def get_ingredients():
    """
    Retrieves a list of ingredients from the database.

    This function makes a GET request to the "/api/v1/ingredients" endpoint and returns a list of ingredients. It uses the `get_ingredients_from_db` function to fetch the ingredients from the database.

    Returns:
        List[str]: A list of strings representing the ingredients.

    Raises:
        None

    Example Usage:
        response = get_ingredients()
        print(response)
    """
    ingredients_list = get_ingredients_from_db()
    return ingredients_list
