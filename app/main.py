from fastapi import FastAPI, File, Query, UploadFile, status
from fastapi.responses import RedirectResponse, StreamingResponse
from core.transcriptor import transcribe
from config.env import Settings
import uvicorn
import logging
from whisper.tokenizer import LANGUAGES
import os


app = FastAPI()


@app.on_event("startup")
async def logging_setup() -> None:
    logger = logging.getLogger("uvicorn.access")
    console_formatter = uvicorn.logging.ColourizedFormatter(
        "{levelprefix} {asctime} {message}",
        style="{",
        use_colors=True)
    logger.handlers[0].setFormatter(console_formatter)


@app.on_event("startup")
async def audio_dir_setup() -> None:
    audio_dir = Settings().audio_dir
    os.makedirs(audio_dir, exist_ok=True)


@app.get("/", response_class=RedirectResponse, include_in_schema=False, status_code=status.HTTP_308_PERMANENT_REDIRECT)
async def index() -> str:
    return "/docs"


@app.post("/asr", status_code=status.HTTP_200_OK)
def automatic_speech_recognition(
    output_language: str | None = Query(default=None, enum=[*LANGUAGES.keys()]),
    description: str | None = None,
    file: UploadFile = File(...),
    output_format: str = Query(default="txt", enum=["txt", "vtt", "srt", "tsv", "json"]),
    word_timestamps: bool = False
) -> StreamingResponse:
    res = transcribe(file, language=output_language, word_timestamps=word_timestamps, initial_prompt=description, output_format=output_format)
    return StreamingResponse(
        res,
        media_type="text/plain",
        headers={
                'Asr-Engine': "openai/whisper",
                'Content-Disposition': f'attachment; filename="{file.filename}.{output_format}"'
        }
    )





if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=Settings().dev_mode)
