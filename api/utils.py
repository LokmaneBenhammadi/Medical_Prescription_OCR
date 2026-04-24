"""Utility helpers for API-side image decoding and preprocessing integration."""

<<<<<<< HEAD
from io import BytesIO

=======
>>>>>>> d6de15d804c1f02f1e2b51690b648d0bf7a8c1c9
from PIL import Image


def decode_image(file_bytes: bytes) -> Image.Image:
    """Decode raw uploaded bytes into a PIL image object."""

<<<<<<< HEAD
    try:
        with Image.open(BytesIO(file_bytes)) as img:
            return img.convert("RGB")
    except Exception as exc:  # pragma: no cover - handled by API layer
        raise ValueError("Invalid image file.") from exc
=======
    raise NotImplementedError("Image decoding is not implemented yet.")
>>>>>>> d6de15d804c1f02f1e2b51690b648d0bf7a8c1c9
