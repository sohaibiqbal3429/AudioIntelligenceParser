# Audio Intelligence Parser

FastAPI backend with a local Whisper transcription pipeline and OpenAI-based structured extraction, plus a Next.js frontend.

## Architecture
- **Backend (FastAPI)**: receives audio upload, transcribes locally using Whisper, extracts structured fields using OpenAI.
- **Frontend (Next.js)**: provides upload UI and calls backend API (`/upload-audio`).

## Backend Features
- `POST /upload-audio` using `multipart/form-data`.
- Allowed file types: `.mp3`, `.wav`, `.m4a`.
- Streams upload into a temporary file with size limits, transcribes locally with `openai-whisper`, then deletes temp file.
- Sends transcription to OpenAI Chat Completions for strict JSON extraction of:
  - `name`, `email`, `age`, `gender`, `phone`
- Returns both `transcription` and `extracted_data`.

## Run Backend
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

## Run Frontend
```bash
cd frontend
cp .env.local.example .env.local
npm install
npm run dev
```

Frontend runs at `http://localhost:3000` and calls backend at `NEXT_PUBLIC_API_BASE_URL` (default `http://localhost:8000`).

## Example API response
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
