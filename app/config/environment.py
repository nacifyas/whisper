from pydantic import BaseSettings, validator
import whisper


class Settings(BaseSettings):
    model: str
    memory: bool = True

    @validator('model')
    def username_alphanumeric(cls, v):
        models = whisper.available_models()
        if not v in models:
            raise ValueError(f'Model not available. Possible options: {models}')
        return v

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'
