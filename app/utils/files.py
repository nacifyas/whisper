from config.env import Settings
from fastapi import UploadFile
from utils.formatters import prepend_unique_name
from pathlib import Path
import shutil
import os


def clean_file(file_route: str) -> None:
    if Settings().delete_on_finish:
        os.remove(file_route)


def load(upload_file: UploadFile) -> None:
    destination = Path(f"{Settings().audio_dir}/{prepend_unique_name(upload_file.filename)}")
    try:
        with destination.open("wb") as buffer:
            shutil.copyfileobj(upload_file.file, buffer)
        return destination.as_posix()
    finally:
        upload_file.file.close()
