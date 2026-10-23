import os
import time
import torch
from transformers import AutoModel

MODEL_ID = "ARTPARK-IISc/SraVaani-1.0"
AUDIO_PATH = "..\\data\\English.mpeg"

token = os.getenv("HF_TOKEN")

if not token:
    raise RuntimeError("HF_TOKEN is not set.")

if not os.path.exists(AUDIO_PATH):
    raise FileNotFoundError(f"Audio file not found: {AUDIO_PATH}")

device = "cpu"

print("Loading SraVaani on CPU...")
start = time.perf_counter()

model = AutoModel.from_pretrained(
    MODEL_ID,
    trust_remote_code=True,
    token=token,
).to(device).eval()

print(f"Model loaded in {time.perf_counter() - start:.1f}s")

print("Transcribing audio...")
start = time.perf_counter()

with torch.inference_mode():
    hypotheses = model.transcribe(
        AUDIO_PATH,
        return_hypotheses=True,
    )

print(f"Transcription completed in {time.perf_counter() - start:.1f}s")

for hypothesis in hypotheses:
    print("Transcript:", hypothesis.text)