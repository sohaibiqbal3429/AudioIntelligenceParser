from fastapi import APIRouter, File, HTTPException, UploadFile

from app.config import get_settings
from app.services.extraction_service import extract_structured_data
from app.services.whisper_service import transcribe_audio
from app.utils.file_utils import persist_upload_tempfile, safe_delete, validate_audio_file

router = APIRouter()


@router.post("/upload-audio")
async def upload_audio(audio: UploadFile = File(...)) -> dict:
    settings = get_settings()
    extension = await validate_audio_file(audio)
    temp_path = await persist_upload_tempfile(
        audio,
        suffix=extension,
        max_size_bytes=settings.max_upload_size_bytes,
    )

    try:
        transcription = await transcribe_audio(temp_path)
        if not transcription:
            raise HTTPException(status_code=422, detail="No speech detected in audio")

        extracted_data = await extract_structured_data(transcription)
        return {"transcription": transcription, "extracted_data": extracted_data}
    finally:
        safe_delete(temp_path)
