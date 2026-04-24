"""Image preprocessing pipeline for prescription normalization."""

from __future__ import annotations

from typing import Iterable

import cv2
import numpy as np
from PIL import Image

from .detection.detector import detect_line_bboxes


def deskew(pil_img: Image.Image, max_angle: float = 5.0) -> Image.Image:
    """Estimate skew and rotate the image if needed."""

    gray = np.array(pil_img.convert("L"))
    edges = cv2.Canny(gray, 50, 200, apertureSize=3)
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 100, minLineLength=50, maxLineGap=10)
    if lines is None:
        return pil_img

    angles = []
    for x1, y1, x2, y2 in lines[:, 0]:
        angle = np.degrees(np.arctan2(y2 - y1, x2 - x1))
        if -45 <= angle <= 45:
            angles.append(angle)
    if not angles:
        return pil_img

    median = float(np.median(angles))
    if abs(median) < 0.5 or abs(median) > max_angle:
        return pil_img

    height, width = gray.shape
    matrix = cv2.getRotationMatrix2D((width // 2, height // 2), median, 1.0)
    rotated = cv2.warpAffine(
        np.array(pil_img.convert("RGB")),
        matrix,
        (width, height),
        borderMode=cv2.BORDER_REPLICATE,
    )
    return Image.fromarray(rotated)


def preprocess_image(pil_img: Image.Image, apply_binarize: bool = True) -> Image.Image:
    """Apply a light preprocessing pipeline suitable for OCR."""

    rgb = pil_img.convert("RGB")
    deskewed = deskew(rgb)

    if not apply_binarize:
        return deskewed

    gray = cv2.cvtColor(np.array(deskewed), cv2.COLOR_RGB2GRAY)
    denoised = cv2.fastNlMeansDenoising(gray, None, 14, 7, 21)
    thresh = cv2.adaptiveThreshold(
        denoised,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        31,
        10,
    )
    kernel = np.ones((2, 2), np.uint8)
    opened = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
    rgb_opened = cv2.merge([opened, opened, opened])
    return Image.fromarray(cv2.cvtColor(rgb_opened, cv2.COLOR_BGR2RGB))


def segment_lines(pil_img: Image.Image, min_height: int = 15) -> list[Image.Image]:
    """Return line crops based on horizontal projection line detection."""

    bboxes = detect_line_bboxes(pil_img, min_height=min_height)
    if not bboxes:
        return [pil_img]
    return [pil_img.crop((0, top, pil_img.width, bottom)) for top, bottom in bboxes]


def batch_preprocess(images: Iterable[Image.Image]) -> list[Image.Image]:
    """Convenience wrapper for preprocessing multiple images."""

    return [preprocess_image(img) for img in images]
