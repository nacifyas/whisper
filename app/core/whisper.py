import whisper
from config.env import Settings


model = whisper.load_model(Settings().model, in_memory=Settings().in_memory)
