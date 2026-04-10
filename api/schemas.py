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
