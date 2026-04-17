"""Detection interfaces for locating text lines or regions before OCR transcription."""

from __future__ import annotations

import cv2
import numpy as np
from PIL import Image


def _binarize_for_lines(gray: np.ndarray) -> np.ndarray:
	blur = cv2.GaussianBlur(gray, (3, 3), 0)
	_, binary = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
	return binary


def detect_line_bboxes(
	pil_img: Image.Image,
	min_height: int = 15,
	min_gap: int = 2,
) -> list[tuple[int, int]]:
	"""Detect text line bounding boxes using horizontal projection."""

	gray = np.array(pil_img.convert("L"))
	binary = _binarize_for_lines(gray)
	h_proj = np.sum(binary, axis=1)

	bboxes: list[tuple[int, int]] = []
	in_line = False
	start = 0
	for y, val in enumerate(h_proj):
		if val > 0 and not in_line:
			in_line = True
			start = y
		elif val == 0 and in_line:
			end = y
			if end - start >= min_height:
				bboxes.append((start, end))
			in_line = False

	if in_line and gray.shape[0] - start >= min_height:
		bboxes.append((start, gray.shape[0]))

	if not bboxes:
		return []

	merged: list[list[int]] = []
	for top, bottom in bboxes:
		if not merged:
			merged.append([top, bottom])
			continue
		if top - merged[-1][1] <= min_gap:
			merged[-1][1] = bottom
		else:
			merged.append([top, bottom])

	return [(int(t), int(b)) for t, b in merged]
