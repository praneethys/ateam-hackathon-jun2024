from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def get_gpt_response(system_prompt, user_prompt, prev_msgs=[], temperature=0.5, model="gpt-4o", is_json=False):
    msgs = []
    for prev_msg in prev_msgs:
        user_msg, ai_msg = prev_msg
        msgs.append({"role": "user", "content": user_msg})
        msgs.append({"role": "assistant", "content": ai_msg})

    messages = [
        {"role": "system", "content": system_prompt},
        *msgs,
        {"role": "user", "content": user_prompt},
    ]

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=1024,
        top_p=0.3,
        frequency_penalty=0.0,
        response_format={"type": "json_object"} if is_json else None,
    )

    return response.choices[0].message.content


def get_dall_e_response(prompt, size=256, model="dall-e-3", n_images=1):
    response = client.images.generate(
        model=model, prompt=prompt, size=f"{size}x{size}", quality="standard", n=n_images
    )

    return response.data[0].url


def get_tts_response(text, output_file_path="output.mp3", model="tts-1", voice="nova"):
    response = client.audio.speech.create(model=model, voice=voice, input=text)

    return response.write_to_file(output_file_path)


def get_stt_response(audio_bytes, model="whisper-1"):
    response = client.audio.transcriptions.create(model=model, file=audio_bytes)

    return response.text
