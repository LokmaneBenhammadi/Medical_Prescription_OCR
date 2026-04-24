"""FastAPI application for serving medical prescription OCR locally."""

from __future__ import annotations

import os
import time

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from api.schemas import OcrResponse
from api.utils import decode_image
from src.inference import OCRPipeline

tags_metadata = [
    {
        "name": "System",
        "description": "Service status and operational endpoints.",
    },
    {
        "name": "Inference",
        "description": "Prescription OCR prediction endpoints.",
    },
]

app = FastAPI(
    title="Medical Prescription OCR API",
    version="0.1.0",
    description="Local API for running line-level OCR on prescription images.",
    openapi_tags=tags_metadata,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

CONFIG_PATH = os.environ.get("CONFIG_PATH", "configs/config.yaml")
pipeline: OCRPipeline | None = None


@app.on_event("startup")
async def startup_event() -> None:
    """Load the OCR pipeline once when the API starts."""

    global pipeline
    pipeline = OCRPipeline.from_config(CONFIG_PATH)


@app.get("/", include_in_schema=False)
async def root() -> RedirectResponse:
    """Redirect root path to Swagger UI documentation."""

    return RedirectResponse(url="/docs")


@app.get("/health", tags=["System"], summary="Health check")
async def health() -> dict[str, str]:
    """Health-check endpoint used to verify service availability."""

    return {"status": "ok", "model_loaded": str(pipeline is not None).lower()}


@app.post("/predict", tags=["Inference"], summary="OCR prediction", response_model=OcrResponse)
async def predict(image: UploadFile = File(...)) -> OcrResponse:
    """Run OCR on an uploaded prescription image."""

    if pipeline is None:
        raise HTTPException(status_code=500, detail="Model not loaded.")

    if not image.content_type or not image.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Please upload a valid image file.")

    try:
        file_bytes = await image.read()
        pil_img = decode_image(file_bytes)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    started_at = time.perf_counter()
    result = pipeline.predict(pil_img)
    processing_ms = round((time.perf_counter() - started_at) * 1000, 2)
    image_id = image.filename or "uploaded"

    return OcrResponse(
        raw_text=result["raw_text"],
        lines=result["lines"],
        image_id=image_id,
        line_count=len(result["lines"]),
        processing_ms=processing_ms,
    )
