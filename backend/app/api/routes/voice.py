import subprocess
import asyncio
import os
import shutil
import tempfile
from pathlib import Path
import base64

from fastapi import APIRouter, File,  Depends, Form, HTTPException, UploadFile

from app.services.speech_service import transcribe_audio

from fastapi import Response
from app.services.tts_service import synthesize_speech

from app.api.dependencies import get_farmer_graph_agent
from app.agents.farmer_graph_agent import FarmerGraphAgent

router = APIRouter(prefix="/voice", tags=["Voice Assistant"])

ALLOWED_EXTENSIONS = {
    ".wav",
    ".mp3",
    ".mpeg",
    ".m4a",
    ".webm",
    ".ogg",
    ".mp4",
}

MAX_FILE_SIZE = 20 * 1024 * 1024  # 20 MB

LANGUAGE_CODES = {
    "auto": None,
    "en": "en",
    "english": "en",
    "te": "te",
    "telugu": "te",
    "hi": "hi",
    "hindi": "hi",
}

# Find FFmpeg through PATH, with a fallback to your Windows installation.
FFMPEG_PATH = (
    shutil.which("ffmpeg")
    or r"C:\ffmpeg\ffmpeg-9.0.2-essentials_build\bin\ffmpeg.exe"
)



def _normalize_audio_sync(input_path: str, output_path: str) -> None:
    """Convert uploaded audio to mono, 16 kHz PCM WAV."""

    if not os.path.isfile(FFMPEG_PATH):
        raise HTTPException(
            status_code=500,
            detail="FFmpeg executable was not found. Check FFMPEG_PATH.",
        )

    try:
        result = subprocess.run(
            [
                FFMPEG_PATH,
                "-hide_banner",
                "-loglevel", "error",
                "-y",
                "-i", input_path,
                "-vn",
                "-ac", "1",
                "-ar", "16000",
                "-c:a", "pcm_s16le",
                output_path,
            ],
            capture_output=True,
            text=True,
            timeout=120,
            check=False,
        )
    except subprocess.TimeoutExpired:
        raise HTTPException(
            status_code=422,
            detail="Audio conversion timed out. Try a shorter recording.",
        )

    if result.returncode != 0 or not os.path.isfile(output_path):
        from app.core.logger import logger
        logger.error("FFmpeg conversion failed: %s", result.stderr[-2000:])

        raise HTTPException(
            status_code=422,
            detail=(
                "Could not decode this audio file. "
                "Try another recording in a supported format."
            ),
        )

    if os.path.getsize(output_path) == 0:
        raise HTTPException(
            status_code=422,
            detail="The uploaded audio could not be converted.",
        )


async def normalize_audio(input_path: str, output_path: str) -> None:
    """Run audio conversion without blocking FastAPI's event loop."""
    await asyncio.to_thread(
        _normalize_audio_sync,
        input_path,
        output_path,
    )


@router.post("/transcribe")
async def transcribe(
    audio: UploadFile = File(...),
    language: str = Form("auto"),
):
    """
    Transcribe uploaded audio using SraVaani.

    Supported language options: auto, en, te, hi.
    Audio is normalized internally before transcription.
    """

    extension = Path(audio.filename or "").suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=(
                "Unsupported audio format. "
                "Use WAV, MP3, MPEG, M4A, WEBM, OGG, or MP4."
            ),
        )

    language_key = language.strip().lower()

    if language_key not in LANGUAGE_CODES:
        raise HTTPException(
            status_code=400,
            detail=(
                "Language must be auto, en, english, "
                "te, telugu, hi, or hindi."
            ),
        )

    input_path = None
    normalized_path = None

    try:
        # Save the uploaded recording temporarily.
        with tempfile.NamedTemporaryFile(
            suffix=extension,
            delete=False,
        ) as temp_file:
            input_path = temp_file.name
            total_size = 0

            while True:
                chunk = await audio.read(1024 * 1024)

                if not chunk:
                    break

                total_size += len(chunk)

                if total_size > MAX_FILE_SIZE:
                    raise HTTPException(
                        status_code=413,
                        detail="Audio file exceeds the 20 MB limit.",
                    )

                temp_file.write(chunk)

        if total_size == 0:
            raise HTTPException(
                status_code=400,
                detail="The uploaded audio file is empty.",
            )

        # Create a temporary WAV destination.
        with tempfile.NamedTemporaryFile(
            suffix=".wav",
            delete=False,
        ) as temp_wav:
            normalized_path = temp_wav.name

        # Convert all accepted formats to a consistent audio format.
        await normalize_audio(input_path, normalized_path)

        # SraVaani performs automatic language detection.
        result = await transcribe_audio(normalized_path)
        transcript = result.get("text", "").strip()

        if not transcript:
            raise HTTPException(
                status_code=422,
                detail="No speech could be recognized in the audio.",
            )

        return {
            "success": True,
            "text": transcript,
            "detected_language": None,
            "language_probability": None,
        }

    except HTTPException:
        raise

    except Exception:
        # Keep internal exception details in server logs only.
        from app.core.logger import logger
        logger.exception("Audio transcription failed")

        raise HTTPException(
            status_code=500,
            detail="Audio transcription failed. Check the backend logs.",
        )

    finally:
        await audio.close()

        for path in (input_path, normalized_path):
            if path and os.path.exists(path):
                try:
                    os.remove(path)
                except OSError:
                    pass


@router.post("/synthesize")
async def synthesize(
    text: str = Form(...),
    language: str = Form("en"),
):
    """Convert text into speech and return an MP3 audio response."""

    try:
        audio_bytes = await synthesize_speech(text, language)

        return Response(
            content=audio_bytes,
            media_type="audio/mpeg",
            headers={
                "Content-Disposition": 'attachment; filename="speech.mp3"'
            },
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    except Exception as exc:
        from app.core.logger import logger
        logger.exception("Speech synthesis failed")

        raise HTTPException(
            status_code=502,
            detail="Speech generation failed. Check the backend logs.",
        ) from exc



@router.post("/chat")
async def voice_chat(
    audio: UploadFile = File(...),
    language: str = Form("en"),
    agent: FarmerGraphAgent = Depends(get_farmer_graph_agent),
):
    """
    Audio -> STT -> existing Farmer Agent -> TTS.
    Returns transcript, agent answer, and base64-encoded MP3.
    """

    language_key = language.strip().lower()

    if language_key not in {"en", "english", "te", "telugu", "hi", "hindi"}:
        raise HTTPException(
            status_code=400,
            detail="Language must be en, te, or hi.",
        )

    language_key = {
        "english": "en",
        "telugu": "te",
        "hindi": "hi",
    }.get(language_key, language_key)

    extension = Path(audio.filename or "").suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Unsupported audio format.",
        )

    input_path = None
    normalized_path = None

    try:
        # 1. Save the uploaded recording.
        with tempfile.NamedTemporaryFile(
            suffix=extension,
            delete=False,
        ) as temp_file:
            input_path = temp_file.name
            total_size = 0

            while True:
                chunk = await audio.read(1024 * 1024)

                if not chunk:
                    break

                total_size += len(chunk)

                if total_size > MAX_FILE_SIZE:
                    raise HTTPException(
                        status_code=413,
                        detail="Audio file exceeds the 20 MB limit.",
                    )

                temp_file.write(chunk)

        if total_size == 0:
            raise HTTPException(
                status_code=400,
                detail="The uploaded audio file is empty.",
            )

        # 2. Normalize audio for SraVaani.
        with tempfile.NamedTemporaryFile(
            suffix=".wav",
            delete=False,
        ) as temp_wav:
            normalized_path = temp_wav.name

        await normalize_audio(input_path, normalized_path)

        # 3. Speech-to-text.
        stt_result = await transcribe_audio(normalized_path)
        transcript = stt_result.get("text", "").strip()

        if not transcript:
            raise HTTPException(
                status_code=422,
                detail="No speech could be recognized.",
            )

        # 4. Call the existing Farmer Agent.
        answer = await agent.run(transcript)

        if not isinstance(answer, str):
            answer = str(answer)

        answer = answer.strip()

        if not answer:
            raise HTTPException(
                status_code=502,
                detail="The Farmer Agent returned an empty answer.",
            )

        # 5. Convert the answer to spoken audio.
        audio_bytes = await synthesize_speech(
            answer,
            language_key,
        )

        # 6. Return all results together.
        return {
            "success": True,
            "transcript": transcript,
            "answer": answer,
            "audio_format": "mp3",
            "audio_base64": base64.b64encode(
                audio_bytes
            ).decode("ascii"),
        }

    except HTTPException:
        raise

    except Exception:
        from app.core.logger import logger
        logger.exception("Voice chat failed")

        raise HTTPException(
            status_code=500,
            detail="Voice chat failed. Check the backend logs.",
        )

    finally:
        await audio.close()

        for path in (input_path, normalized_path):
            if path and os.path.exists(path):
                try:
                    os.remove(path)
                except OSError:
                    pass

