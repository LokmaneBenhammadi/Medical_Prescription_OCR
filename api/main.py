"""FastAPI application skeleton for medical prescription OCR serving."""

from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

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


@app.on_event("startup")
async def startup_event() -> None:
    """Initialize startup resources for the API service."""

    print("Model will be loaded here")


@app.get("/", include_in_schema=False)
async def root() -> RedirectResponse:
    """Redirect root path to Swagger UI documentation."""

    return RedirectResponse(url="/docs")


@app.get("/health", tags=["System"], summary="Health check")
async def health() -> dict[str, str]:
    """Health-check endpoint used to verify service availability."""

    return {"status": "ok"}


@app.post("/predict", tags=["Inference"], summary="OCR prediction placeholder")
async def predict(image: UploadFile = File(...)) -> dict[str, str]:
    """Prediction endpoint placeholder for uploaded prescription images."""

    return {"message": "not implemented yet"}
