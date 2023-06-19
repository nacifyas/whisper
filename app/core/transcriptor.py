from core.whisper import model
from fastapi import UploadFile
from utils.files import load_file, clean_file


async def transcribe(file: UploadFile, language: str = None, initial_prompt: str = "", word_timestamps: bool = True):
    file_route = await load_file(file)
    result = model.transcribe(file_route, initial_prompt=initial_prompt, word_timestamps=word_timestamps)
    clean_file(file_route) # Background
    return result
