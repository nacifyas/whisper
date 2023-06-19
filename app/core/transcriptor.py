from core.whisper import model, whisper
from fastapi import UploadFile
from utils.files import load_file, clean_file


async def transcribe(file: UploadFile, language: str = None, initial_prompt: str = None, word_timestamps: bool = False):
    file_route = await load_file(file)
    result = model.transcribe(file_route, initial_prompt=initial_prompt, word_timestamps=word_timestamps, language=language)
    clean_file(file_route)
    return result
