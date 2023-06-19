import os
import aiofiles
from fastapi import UploadFile


async def load_file(file: UploadFile) -> str:
    os.makedirs("audio", exist_ok=True)
    file_route = f"audio\\{file.filename}"
    async with aiofiles.open(file_route, 'wb') as out_file:
        while content := await file.read(1024):
            await out_file.write(content)
    return file_route

def clean_file(file_route: str) -> None:
    os.remove(file_route)
