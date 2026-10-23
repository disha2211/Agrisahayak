
import edge_tts

from app.core.logger import logger


VOICE_MAP = {
    "en": "en-IN-NeerjaNeural",
    "english": "en-IN-NeerjaNeural",
    "te": "te-IN-ShrutiNeural",
    "telugu": "te-IN-ShrutiNeural",
    "hi": "hi-IN-SwaraNeural",
    "hindi": "hi-IN-SwaraNeural",
}


async def synthesize_speech(text: str, language: str = "en") -> bytes:
    """Convert text into MP3 speech using a multilingual voice."""

    normalized_language = language.strip().lower()
    voice = VOICE_MAP.get(normalized_language)

    if not voice:
        raise ValueError(
            "Unsupported language. Use en, te, or hi."
        )

    text = text.strip()

    if not text:
        raise ValueError("Text cannot be empty.")

    logger.info(
        "Generating speech: language=%s, voice=%s",
        normalized_language,
        voice,
    )

    communicator = edge_tts.Communicate(
        text=text,
        voice=voice,
    )

    audio_data = bytearray()

    async for chunk in communicator.stream():
        if chunk["type"] == "audio":
            audio_data.extend(chunk["data"])

    if not audio_data:
        raise RuntimeError("TTS returned no audio data.")

    return bytes(audio_data)
