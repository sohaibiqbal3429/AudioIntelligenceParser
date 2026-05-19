import asyncio
import logging
from threading import Lock

import whisper
from fastapi import HTTPException

from app.config import get_settings

logger = logging.getLogger(__name__)
_model = None
_model_lock = Lock()


def _get_model():
    global _model
    if _model is None:
        with _model_lock:
            if _model is None:
                settings = get_settings()
                logger.info("Loading Whisper model: %s", settings.whisper_model)
                _model = whisper.load_model(settings.whisper_model)
    return _model


def _transcribe_sync(file_path: str) -> str:
    model = _get_model()
    result = model.transcribe(file_path)
    text = (result.get("text") or "").strip()
    return text


async def transcribe_audio(file_path: str) -> str:
    try:
        return await asyncio.to_thread(_transcribe_sync, file_path)
    except Exception as exc:
        logger.exception("Whisper transcription failed")
        raise HTTPException(status_code=500, detail="Transcription failed") from exc
