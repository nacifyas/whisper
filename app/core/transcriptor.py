from core.whisper import model
from fastapi import UploadFile
from utils.files import load_file, clean_file
from utils.formatters import write_result
from io import StringIO


async def transcribe(
    file: UploadFile,
    language: str | None = None,
    initial_prompt: str | None = None,
    word_timestamps: bool = False,
    output_format: str = "txt"
) -> StringIO:
    file_route = await load_file(file)
    output = model.transcribe(file_route, initial_prompt=initial_prompt, word_timestamps=word_timestamps, language=language)
    clean_file(file_route)

    result = StringIO()
    write_result(output, result, output_format)
    result.seek(0)

    return result
