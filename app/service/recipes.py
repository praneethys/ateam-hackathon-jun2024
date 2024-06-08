from typing import List
from llama_index.core import PromptTemplate

from app.api.openai import get_gpt_response
from app.schema.index import RecipeListLLMResponse
from app.service.user_preferences import get_user_preferences_from_db


def generate_recipes(ingredients: List[str]):
    user_preferences = get_user_preferences_from_db()
    ingredients_list = ", ".join(ingredients)

    system_context_str = """
        You are a helpful master chef that can generate recipes based on ingredients.
        The recipes should be simple and easy to prepare. They also have to be kid friendly.
        Take user preferences also into account.
    """.strip()

    user_context_str = f"""
        Using the following ingredients, generate a list of 5 recipes. Return the list in JSON format.
        {RecipeListLLMResponse.model_json_schema()}

        Ingredients: {ingredients_list}
        User preferences: {user_preferences}
    """.strip()

    try:
        recipes = get_gpt_response(system_prompt=system_context_str, user_prompt=user_context_str, is_json=True)

    except Exception as e:
        print("Exception while generating recipes: ", str(e))
        raise e
    print(recipes)

    return recipes
