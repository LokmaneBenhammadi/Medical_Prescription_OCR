"""Utility helpers for API-side image decoding and preprocessing integration."""

from io import BytesIO

from PIL import Image


def decode_image(file_bytes: bytes) -> Image.Image:
    """Decode raw uploaded bytes into a PIL image object."""

    try:
        with Image.open(BytesIO(file_bytes)) as img:
            return img.convert("RGB")
    except Exception as exc:  # pragma: no cover - handled by API layer
        raise ValueError("Invalid image file.") from exc
