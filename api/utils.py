"""Utility helpers for API-side image decoding and preprocessing integration."""

from PIL import Image


def decode_image(file_bytes: bytes) -> Image.Image:
    """Decode raw uploaded bytes into a PIL image object."""

    raise NotImplementedError("Image decoding is not implemented yet.")
