import whisper
from config.env import Settings


model = whisper.load_model(Settings().model, device=Settings().device, in_memory=Settings().in_memory, download_root=Settings().model_dir)
