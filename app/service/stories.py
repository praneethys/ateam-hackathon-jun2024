import json
import os
from typing import Dict
import uuid
from app.api.openai import get_gpt_response, get_tts_response, get_stt_response
from app.schema.index import RecipeListLLMResponse, StoryLLMResponse


def generate_story_text(recipe: RecipeListLLMResponse) -> Dict:

    system_context_str = """
        You are a great story teller. You tell the best kids stories ever.
        The stories you tell are both engaging and entertaining while also providing education to kids.
    """.strip()

    user_context_str = f"""
        Using the following recipe, create a kid friendlystory. Return the list in JSON format.
        The output JSON should be in the following format:
        title: story title, story: story text, recipe_uuid: uuid of recipe

        Recipe: {recipe.model_dump()}
    """.strip()

    try:
        story = get_gpt_response(system_prompt=system_context_str, user_prompt=user_context_str, is_json=True)
    except Exception as e:
        print("Exception while generating recipes: ", str(e))
        raise e

    return story


async def generate_story_audio(story: StoryLLMResponse) -> None:
    data_dir = os.path.abspath("./data/story")
    story_json = story.model_dump()
    story_audio_file = os.path.join(data_dir, f"{story_json['recipe_uuid']}.mp3")

    # Generate the audio file for the story if it doesn't exist
    if not os.path.exists(story_audio_file):
        get_tts_response(story_json["story"], output_file_path=story_audio_file)


async def generate_story(recipe: RecipeListLLMResponse) -> StoryLLMResponse:
    data_dir = os.path.abspath("./data/story")
    recipe_json = recipe.model_dump()

    story_file = os.path.join(data_dir, f"{recipe_json['recipe_uuid']}.json")
    if os.path.exists(story_file):
        with open(story_file, "r") as f:
            story = json.load(f)

            await generate_story_audio(
                StoryLLMResponse(
                    title=story["title"],
                    story=story["story"],
                    recipe_uuid=story["recipe_uuid"],
                    story_uuid=story["story_uuid"],
                ),
            )
            return story

    story_llm_response = generate_story_text(recipe)
    story_llm_response_json = json.loads(story_llm_response)
    story_llm_response_json["story_uuid"] = str(uuid.uuid4())
    print(story_llm_response_json)

    with open(story_file, "w") as f:
        json.dump(story_llm_response_json, f, indent=4)

    story_response = StoryLLMResponse(
        title=story_llm_response_json["title"],
        story=story_llm_response_json["story"],
        recipe_uuid=story_llm_response_json["recipe_uuid"],
        story_uuid=story_llm_response_json["story_uuid"],
    )

    await generate_story_audio(story_response)

    return story_response


async def respond_to_user(audio_file_bytes):
    transcription = get_stt_response(audio_file_bytes)
    # TODO: LLM stuff
    response = "placeholder"
    data_dir = os.path.abspath("./data/story")
    response_audio_file = os.path.join(data_dir, f"response.mp3")

    # Generate the audio file for the story if it doesn't exist
    get_tts_response(response, output_file_path=response_audio_file)

    return response_audio_file
