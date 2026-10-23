import asyncio
import os
from functools import lru_cache
from app.core.config import settings

import torch
from transformers import AutoModel

from app.core.logger import logger

MODEL_ID = "ARTPARK-IISc/SraVaani-1.0"


@lru_cache(maxsize=1)
def get_speech_model():
    """Load SraVaani once and reuse it."""

    logger.info("Loading SraVaani speech recognition model")

    token = settings.HF_TOKEN

    if not token:
        raise RuntimeError(
            "HF_TOKEN environment variable is not configured."
        )

    model = AutoModel.from_pretrained(
        MODEL_ID,
        trust_remote_code=True,
        token=token,
    )

    model = model.to("cpu").eval()

    logger.info("SraVaani loaded successfully")

    return model


def _transcribe_audio(file_path: str) -> dict:
    """Transcribe an audio file using SraVaani."""

    model = get_speech_model()

    with torch.inference_mode():
        hypotheses = model.transcribe(
            file_path,
            return_hypotheses=True,
        )

    texts = [
        hypothesis.text.strip()
        for hypothesis in hypotheses
        if hypothesis.text.strip()
    ]

    return {
        "text": " ".join(texts).strip(),
    }


async def transcribe_audio(file_path: str) -> dict:
    """Run transcription without blocking FastAPI's event loop."""

    return await asyncio.to_thread(
        _transcribe_audio,
        file_path,
    )