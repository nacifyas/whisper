from pydantic import BaseSettings, validator
import whisper


class Settings(BaseSettings):
    model: str
    in_memory: bool = True
    dev_mode: bool = False
    port: int = 9900
    delete_on_finish: bool = True

    @validator('model')
    def username_alphanumeric(cls, v: str):
        models = whisper.available_models()
        if v not in models:
            raise ValueError(f'Model not available. Possible options: {models}')
        return v

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'
