import whisper
from config.env import Settings
import torch

model = whisper.load_model(Settings().model, device=Settings().device, in_memory=Settings().in_memory, download_root=Settings().model_dir).cuda() if torch.cuda.is_available() else whisper.load_model(Settings().model, device=Settings().device, in_memory=Settings().in_memory, download_root=Settings().model_dir)