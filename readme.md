# Audio Intelligence Parser

FastAPI backend with a local Whisper transcription pipeline and OpenAI-based structured extraction.

## Features
- `POST /upload-audio` using `multipart/form-data`.
- Allowed file types: `.mp3`, `.wav`, `.m4a`.
- Streams upload into a temporary file with size limits, transcribes locally with `openai-whisper`, then deletes temp file.
- Sends transcription to OpenAI Chat Completions for strict JSON extraction of:
  - `name`, `email`, `age`, `gender`, `phone`
- Returns both `transcription` and `extracted_data`.

## Run
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

## Example response
```json
{
  "transcription": "My name is Jane Doe...",
  "extracted_data": {
    "name": "Jane Doe",
    "email": null,
    "age": 28,
    "gender": "female",
    "phone": null
  }
}
```
