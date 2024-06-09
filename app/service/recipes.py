import json
import os
from typing import List
import uuid
from llama_index.core import PromptTemplate
from fastapi import HTTPException

from app.api.openai import get_dall_e_response, get_gpt_response
from app.schema.index import RecipeListLLMResponse
from app.service.user_preferences import get_user_preferences_from_db


def generate_recipe_text(ingredients: List[str]):

    user_preferences = get_user_preferences_from_db()
    ingredients_list = ", ".join(ingredients)

    system_context_str = """
        You are a helpful master chef that can generate recipes based on ingredients.
        The recipes should be simple and easy to prepare. They also have to be kid friendly.
        Take user preferences also into account.
    """.strip()

    user_context_str = f"""
        Using the following ingredients, generate a list of 3 recipes. Return the list in JSON format.
        {RecipeListLLMResponse.model_json_schema()}

        Ingredients: {ingredients_list}
        User preferences: {user_preferences}
    """.strip()

    try:
        recipes = get_gpt_response(system_prompt=system_context_str, user_prompt=user_context_str, is_json=True)
    except Exception as e:
        print("Exception while generating recipes: ", str(e))
        raise e

    return recipes


def generate_recipes(ingredients: List[str]):
    # Check if data/recipe_output.json exists and return cached data
    data_dir = os.path.abspath("./data")
    recipe_output_path = os.path.join(data_dir, "recipe_output.json")
    if os.path.exists(recipe_output_path):
        with open(recipe_output_path, "r") as f:
            recipes_list = json.load(f)
        return recipes_list

    # 1. Generate recipe text
    recipes_llm_response = generate_recipe_text(ingredients)
    print(recipes_llm_response)
    recipes_list = json.loads(recipes_llm_response)["recipes"]

    # 2. Generate image for each recipe
    for recipe in recipes_list:
        dalle_response_img_urls = get_dall_e_response(
            f"Make an interesting image that is practical to cook for kids for the recipe: {recipe['title']}",
            size=1024,
            model="dall-e-2",
            n_images=4,
        )
        recipe["image_url"] = dalle_response_img_urls
        recipe["recipe_uuid"] = str(uuid.uuid4())

    # Write recipe_list to data/recipe_output.json
    with open(recipe_output_path, "w") as f:
        json.dump(recipes_list, f, indent=4)

    return recipes_list


def generate_ingredients_facts(ingredients: List[str]):
    data_dir = os.path.abspath("./data")
    ingredients_output_path = os.path.join(data_dir, "ingredient-facts.txt")
    ingredients_list = ", ".join(ingredients)

    system_context_str = """
        You are a helpful nutritionist that can generate nutrition facts based on ingredients.
        The nutrition facts should be accurate and informative and a single paragraph.
    """.strip()

    user_context_str = f"""
        Using the following ingredients, generate the nutrition facts. Write a single paragraph.

        Ingredients: {ingredients_list}
    """.strip()

    try:
        facts = get_gpt_response(system_prompt=system_context_str, user_prompt=user_context_str, is_json=True)

        with open(ingredients_output_path, "w") as f:
            f.write(facts)
    except Exception as e:
        print("Exception while generating ingredients facts: ", str(e))
        raise e

    return facts


def get_ingredient_facts():
    data_dir = os.path.abspath("./data")
    ingredients_output_path = os.path.join(data_dir, "ingredient-facts.txt")

    if not os.path.exists(ingredients_output_path):
        return HTTPException(status_code=404, detail="Ingredients facts not found")

    with open(ingredients_output_path, "r") as f:
        facts = f.read()

    return facts
