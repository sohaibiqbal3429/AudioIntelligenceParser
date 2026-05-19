import json
import logging
from typing import Any

from fastapi import HTTPException
from openai import AsyncOpenAI

from app.config import get_settings

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = (
    "Extract personal details from transcribed speech. "
    "Return only valid JSON with EXACT keys: name, email, age, gender, phone. "
    "If a value is missing, return null. Do not guess or infer missing values."
)


JSON_RESPONSE_SHAPE = {"name": None, "email": None, "age": None, "gender": None, "phone": None}


def _normalize_output(parsed: dict[str, Any]) -> dict[str, Any]:
    normalized = dict(JSON_RESPONSE_SHAPE)
    for key in normalized:
        normalized[key] = parsed.get(key)
    return normalized


async def extract_structured_data(transcription: str) -> dict[str, Any]:
    settings = get_settings()
    if not settings.openai_api_key:
        raise HTTPException(status_code=500, detail="OPENAI_API_KEY is not configured")

    client = AsyncOpenAI(api_key=settings.openai_api_key)

    try:
        response = await client.chat.completions.create(
            model=settings.openai_model,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {
                    "role": "user",
                    "content": (
                        "Transcription text:\n"
                        f"{transcription}\n\n"
                        "Return JSON only with keys: name, email, age, gender, phone."
                    ),
                },
            ],
            temperature=0,
        )
        content = response.choices[0].message.content or "{}"
        parsed = json.loads(content)
        if not isinstance(parsed, dict):
            raise ValueError("Model response is not a JSON object")
        return _normalize_output(parsed)
    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("Structured extraction failed")
        raise HTTPException(status_code=502, detail="OpenAI extraction failed") from exc
