from pydantic import BaseSettings


class Settings(BaseSettings):
    in_memory: bool = False
    dev_mode: bool = False
    delete_on_finish: bool = True
    audio_dir: str = "audio"
    model_dir: str | None = None
    device: str | None = None
    model: str = "small"

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'
