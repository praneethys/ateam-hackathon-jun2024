from typing import List
from fastapi import APIRouter

recipe_router = r = APIRouter(prefix="/api/v1/recipes", tags=["recipes"])


@r.post(
    "/",
    response_model=List[str],
    responses={
        200: {"description": "Recipes generated"},
        500: {"description": "Internal server error"},
    },
)
def generate_recipes(ingredients: List[str]):
    