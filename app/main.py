from fastapi import FastAPI, File, Query, UploadFile, status
from fastapi.responses import RedirectResponse, Response
from core.transcriptor import transcribe
from config.env import Settings
import uvicorn
import logging
from whisper.tokenizer import LANGUAGES

app = FastAPI()


@app.on_event("startup")
async def logging_setup():
    logger = logging.getLogger("uvicorn.access")
    console_formatter = uvicorn.logging.ColourizedFormatter(
        "{levelprefix} {asctime} {message}",
        style="{",
        use_colors=True)
    logger.handlers[0].setFormatter(console_formatter)


@app.get("/", response_class=RedirectResponse, include_in_schema=False, status_code=status.HTTP_307_TEMPORARY_REDIRECT)
async def index():
    return "/docs"


@app.post("/asr", status_code=status.HTTP_200_OK)
async def automatic_speech_recognition(
    language: str | None = Query(default=None, enum=[*LANGUAGES.keys()]),
    description: str = None,# = Query(default=None),
    file: UploadFile = File(...),
    text_only: bool = False
):
    res = await transcribe(file, language=language, initial_prompt=description, word_timestamps=not text_only)
    if text_only:
        return res["text"]
    else:
        return res


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=Settings().port, reload=Settings().dev_mode)
