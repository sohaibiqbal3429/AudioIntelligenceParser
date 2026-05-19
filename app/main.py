from fastapi import FastAPI
from app.routes.upload import router as upload_router
from app.utils.logging_config import configure_logging

configure_logging()

app = FastAPI(title="Audio Intelligence Parser", version="1.0.0")
app.include_router(upload_router)


@app.get("/health")
async def health() -> dict:
    return {"status": "ok"}
