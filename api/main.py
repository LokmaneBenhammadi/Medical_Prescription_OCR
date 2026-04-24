"""FastAPI application skeleton for medical prescription OCR serving."""

<<<<<<< HEAD
import os

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from api.schemas import OcrResponse
from api.utils import decode_image
from src.inference import OCRPipeline

=======
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

>>>>>>> d6de15d804c1f02f1e2b51690b648d0bf7a8c1c9
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
    description="API for medical prescription OCR inference (scaffold version).",
    openapi_tags=tags_metadata,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

<<<<<<< HEAD
CONFIG_PATH = os.environ.get("CONFIG_PATH", "configs/config.yaml")
pipeline: OCRPipeline | None = None

=======
>>>>>>> d6de15d804c1f02f1e2b51690b648d0bf7a8c1c9

@app.on_event("startup")
async def startup_event() -> None:
    """Initialize startup resources for the API service."""

<<<<<<< HEAD
    global pipeline
    pipeline = OCRPipeline.from_config(CONFIG_PATH)
=======
    print("Model will be loaded here")
>>>>>>> d6de15d804c1f02f1e2b51690b648d0bf7a8c1c9


@app.get("/", include_in_schema=False)
async def root() -> RedirectResponse:
    """Redirect root path to Swagger UI documentation."""

    return RedirectResponse(url="/docs")


@app.get("/health", tags=["System"], summary="Health check")
async def health() -> dict[str, str]:
    """Health-check endpoint used to verify service availability."""

    return {"status": "ok"}


<<<<<<< HEAD
@app.post("/predict", tags=["Inference"], summary="OCR prediction", response_model=OcrResponse)
async def predict(image: UploadFile = File(...)) -> OcrResponse:
    """Prediction endpoint for uploaded prescription images."""

    if pipeline is None:
        raise HTTPException(status_code=500, detail="Model not loaded.")
    try:
        file_bytes = await image.read()
        pil_img = decode_image(file_bytes)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    result = pipeline.predict(pil_img)
    image_id = image.filename or "uploaded"
    return OcrResponse(raw_text=result["raw_text"], lines=result["lines"], image_id=image_id)
=======
@app.post("/predict", tags=["Inference"], summary="OCR prediction placeholder")
async def predict(image: UploadFile = File(...)) -> dict[str, str]:
    """Prediction endpoint placeholder for uploaded prescription images."""

    return {"message": "not implemented yet"}
>>>>>>> d6de15d804c1f02f1e2b51690b648d0bf7a8c1c9
