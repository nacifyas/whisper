from core.whisper import model
from fastapi import UploadFile
from utils.files import clean_file, load
from utils.formatters import write_result
from io import StringIO
from threading import Lock

model_lock = Lock()

def transcribe(
    file: UploadFile,
    language: str | None = None,
    initial_prompt: str | None = None,
    word_timestamps: bool = False,
    output_format: str = "txt"
) -> StringIO:
    file_route = load(file)

    # with model_lock:
    #     output = model.transcribe(file_route, initial_prompt=initial_prompt, word_timestamps=word_timestamps, language=language)
    with model_lock:
        segments = []
        text = ""
        segment_generator, info = model.transcribe(file_route,
                                                   language=language,
                                                   initial_prompt=initial_prompt,
                                                   word_timestamps=word_timestamps
                                                   )
        for segment in segment_generator:
            
            print(segment.text)

            segments.append(segment)
            text = text + segment.text
        result = {
            "language": language if language else info.language,
            "segments": segments,
            "text": text
        }


    clean_file(file_route)

    output_file = StringIO()
    write_result(result, output_file, output_format)
    output_file.seek(0)

    return output_file
