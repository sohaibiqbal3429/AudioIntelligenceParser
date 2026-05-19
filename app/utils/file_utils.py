import os
import tempfile
from pathlib import Path

from fastapi import HTTPException, UploadFile

ALLOWED_EXTENSIONS = {".mp3", ".wav", ".m4a"}


async def validate_audio_file(upload_file: UploadFile) -> str:
    extension = Path(upload_file.filename or "").suffix.lower()
    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type. Allowed: {', '.join(sorted(ALLOWED_EXTENSIONS))}",
        )
    return extension


async def persist_upload_tempfile(upload_file: UploadFile, suffix: str, max_size_bytes: int) -> str:
    size = 0
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp:
        temp_path = temp.name
        while True:
            chunk = await upload_file.read(1024 * 1024)
            if not chunk:
                break
            size += len(chunk)
            if size > max_size_bytes:
                temp.close()
                safe_delete(temp_path)
                raise HTTPException(status_code=413, detail="Uploaded file is too large")
            temp.write(chunk)

    if size == 0:
        safe_delete(temp_path)
        raise HTTPException(status_code=400, detail="Uploaded file is empty")

    await upload_file.seek(0)
    return temp_path


def safe_delete(path: str) -> None:
    try:
        os.remove(path)
    except FileNotFoundError:
        return
