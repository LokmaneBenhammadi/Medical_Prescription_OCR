"""Pydantic schemas for API request/response payloads."""

from __future__ import annotations

from pydantic import BaseModel


class OcrResponse(BaseModel):
    """Raw OCR response returned by the prediction endpoint."""

    raw_text: str
    lines: list[str]
    image_id: str
    line_count: int
    processing_ms: float
