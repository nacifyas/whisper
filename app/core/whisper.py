from config.env import Settings
from faster_whisper import WhisperModel, available_models
import torch
import os

if torch.cuda.is_available():
    device = "cuda"
    model_quantization = os.getenv("ASR_QUANTIZATION", "float32")
else:
    device = "cpu"
    model_quantization = os.getenv("ASR_QUANTIZATION", "int8")

print(f"Available models: {available_models()}")

print(f"Loading model {Settings().model}")

# model = whisper.load_model(Settings().model,
#                            device=Settings().device,
#                            in_memory=Settings().in_memory,
#                            download_root=Settings().model_dir
#                         ).cuda() if torch.cuda.is_available() else whisper.load_model(Settings().model,
#                                                                                       device=Settings().device,
#                                                                                       in_memory=Settings().in_memory,
#                                                                                       download_root=Settings().model_dir)
model = WhisperModel(
    model_size_or_path=Settings().model,
    device=device,
    compute_type=model_quantization,
    download_root=Settings().model_dir
)

print(f"Model {Settings().model} loaded")