import json
import os
from typing import List
from fastapi import APIRouter, HTTPException, UploadFile
from fastapi.responses import FileResponse

from app.schema.index import IngredientList, Recipe, RecipeListLLMResponse
from app.service.recipes import generate_recipes
from app.service.stories import generate_story, respond_to_user

story_router = r = APIRouter(prefix="/api/v1/story", tags=["story"])


@r.post(
    "/{recipe_id}",
    responses={
        200: {"description": "Recipes generated"},
        500: {"description": "Internal server error"},
    },
)
async def post_story(recipe_id: str):
    data_dir = os.path.abspath("./data")
    with open(os.path.join(data_dir, "recipe_output.json"), "r") as f:
        recipes_list = json.load(f)

    if recipes_list is None or len(recipes_list) == 0:
        return HTTPException(status_code=404, detail="Recipes not found")

    for recipe in recipes_list:
        if recipe["recipe_uuid"] == recipe_id:
            story = await generate_story(
                Recipe(
                    title=recipe["title"],
                    ingredients=recipe["ingredients"],
                    instructions=recipe["instructions"],
                    image_url=recipe["image_url"],
                    recipe_uuid=recipe["recipe_uuid"],
                )
            )

            return story

    return HTTPException(status_code=404, detail="Recipe not found")


@r.get(
    "/audio/{recipe_id}",
    responses={
        200: {"description": "Recipe found"},
        404: {"description": "Recipe not found"},
        500: {"description": "Internal server error"},
    },
)
def get_story_audio(recipe_id: str):
    data_dir = os.path.abspath(f"./data/story/recipe_{recipe_id}")
    story_audio_path = os.path.join(data_dir, f"story_audio.mp3")
    if not os.path.exists(story_audio_path):
        return HTTPException(status_code=404, detail="Story audio not found")

    return FileResponse(story_audio_path, media_type="audio/mpeg")


@r.get(
    "/text/{recipe_id}",
    responses={
        200: {"description": "Recipe found"},
        404: {"description": "Recipe not found"},
        500: {"description": "Internal server error"},
    },
)
def get_story(recipe_id: str):
    data_dir = os.path.abspath(f"./data/story/recipe_{recipe_id}")
    file_path = os.path.join(data_dir, f"story.json")

    if not os.path.exists(file_path):
        return HTTPException(status_code=404, detail="Story not found")

    with open(file_path) as f:
        story = json.load(f)
        return story


@r.get(
    "/image/{recipe_id}",
    responses={
        200: {"description": "Recipe found"},
        404: {"description": "Recipe not found"},
        500: {"description": "Internal server error"},
    },
)
def get_story(recipe_id: str):
    data_dir = os.path.abspath(f"./data/story/recipe_{recipe_id}")
    file_path = os.path.join(data_dir, f"story_image.json")

    if not os.path.exists(file_path):
        return HTTPException(status_code=404, detail="Story not found")

    with open(file_path, "r") as f:
        story = json.load(f)
        return story


@r.post(
    "/user-input",
    responses={
        200: {"description": "Text found"},
        404: {"description": "Text not found"},
        400: {"description": "Invalid file type"},
        500: {"description": "Internal server error"},
    },
)
async def get_user_voice_input(audio_file: UploadFile):
    if not audio_file.content_type.startswith("audio/"):
        return HTTPException(status_code=400, detail="Invalid file type")

    audio_data_bytes = await audio_file.read()

    response = await respond_to_user(audio_data_bytes)

    return FileResponse(path=response, filename="response.mp3", media_type="audio/mpeg")


@r.get(
    "/title/{recipe_id}",
    responses={
        200: {"description": "Recipe found"},
        404: {"description": "Recipe not found"},
        500: {"description": "Internal server error"},
    },
)
def get_title(recipe_id: str):
    data_dir = os.path.abspath("./data")
    with open(os.path.join(data_dir, "recipe_output.json"), "r") as f:
        recipes_list = json.load(f)

    if recipes_list is None or len(recipes_list) == 0:
        return HTTPException(status_code=404, detail="Recipes not found")

    for recipe in recipes_list:
        if recipe["recipe_uuid"] == recipe_id:
            return {"title": recipe["title"]}

    return HTTPException(status_code=404, detail="Recipe not found")
