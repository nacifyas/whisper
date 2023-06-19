import whisper
from config.environment import Settings


model = whisper.load_model(Settings.model, in_memory=Settings.memory)