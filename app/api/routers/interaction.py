from fastapi import APIRouter, HTTPException, UploadFile
from fastapi.responses import FileResponse

import os
from uuid import uuid4

from app.service.stories import respond_to_user

interaction_router = r = APIRouter(prefix="/api/v1/interaction", tags=["story"])


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

    data_dir = os.path.abspath("./data/interaction")
    file_id = uuid4()
    interaction_audio_file = os.path.join(data_dir, f"{file_id}.mp3")

    os.makedirs(os.path.dirname(interaction_audio_file), exist_ok=True)

    with open(interaction_audio_file, "wb+") as file_object:
        file_object.write(await audio_file.read())

    audio_file = await respond_to_user(interaction_audio_file)

    return FileResponse(path=audio_file, filename="response.mp3", media_type="audio/mpeg")
