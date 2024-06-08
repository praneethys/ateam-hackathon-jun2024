from typing import List
from llama_index.core import PromptTemplate

from app.api.openai import get_gpt_response

async def generate_recipes(ingredients: List[str]):
    system_context_str = """
        You are a helpful master chef that can generate recipes based on ingredients.
        Using the following ingredients, generate a list of 5 recipes. The recipes
        should be simple and easy to prepare. They also have to be kid friendly.
        Take user preferences also into account.

        Ingredients: {ingredients}
        User preferences: {preferences}
    """.strip()

    system_prompt = PromptTemplate(system_context_str, input_variables=["ingredients", "preferences"])
    recipes = get_gpt_response(system_prompt)
    print(recipes)

    return recipes