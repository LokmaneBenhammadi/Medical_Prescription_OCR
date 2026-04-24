"""Pydantic schemas for API request/response payloads."""

from pydantic import BaseModel


class PrescriptionEntry(BaseModel):
    """Structured representation of a single prescription line item."""

    drug_name: str
    dosage: str
    frequency: str
    raw_line: str


class PrescriptionResponse(BaseModel):
    """Top-level structured OCR response returned by the prediction endpoint."""

    raw_text: str
    entries: list[PrescriptionEntry]
    image_id: str
<<<<<<< HEAD


class OcrResponse(BaseModel):
    """Raw OCR response for baseline inference."""

    raw_text: str
    lines: list[str]
    image_id: str
=======
>>>>>>> d6de15d804c1f02f1e2b51690b648d0bf7a8c1c9
