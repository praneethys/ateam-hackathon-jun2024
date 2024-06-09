from enum import Enum
from typing import List

from app.schema.base import BaseModel, PydanticBaseModel


class TransactionType(str, Enum):
    INCOME = "income"
    EXPENSE = "expense"


class UserCreate(PydanticBaseModel):
    name: str
    email: str
    hashed_password: str


class UserUpdate(PydanticBaseModel):
    name: str
    email: str
    hashed_password: str


class UserResponse(PydanticBaseModel):
    id: int
    name: str
    email: str
    is_deleted: bool


class User(BaseModel):
    name: str
    email: str
    hashed_password: str
    is_deleted: bool = False


class IngredientList(BaseModel):
    ingredients: List[str]


class RecipeListLLMResponse(PydanticBaseModel):
    title: str
    ingredients: List[str]
    instructions: List[str]


class Recipe(RecipeListLLMResponse):
    recipe_uuid: str
    image_url: str


class StoryLLMResponse(PydanticBaseModel):
    title: str
    story: str
    recipe_uuid: str
    story_uuid: str
