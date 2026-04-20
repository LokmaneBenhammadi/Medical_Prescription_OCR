"""Model construction utilities for OCR and related deep learning components."""

from __future__ import annotations

from typing import Iterable

import torch
from transformers import TrOCRProcessor, VisionEncoderDecoderModel


def resolve_device(requested: str | None) -> torch.device:
	"""Resolve a device string while handling unavailable CUDA."""

	if not requested or requested == "auto":
		return torch.device("cuda" if torch.cuda.is_available() else "cpu")
	if requested == "cuda" and not torch.cuda.is_available():
		return torch.device("cpu")
	return torch.device(requested)


class TrOCREngine:
	"""Wrapper around TrOCR with sensible defaults for inference."""

	def __init__(
		self,
		model_name: str,
		device: str | None = None,
		max_length: int = 128,
		beam_size: int = 4,
	) -> None:
		self.device = resolve_device(device)
		self.processor = TrOCRProcessor.from_pretrained(model_name)
		self.model = VisionEncoderDecoderModel.from_pretrained(model_name)
		self.model.config.decoder_start_token_id = self.processor.tokenizer.cls_token_id
		self.model.config.pad_token_id = self.processor.tokenizer.pad_token_id
		self.model.config.eos_token_id = self.processor.tokenizer.sep_token_id
		self.model.generation_config.max_length = max_length
		self.model.generation_config.num_beams = beam_size
		self.model.to(self.device)
		self.model.eval()
		self.max_length = max_length
		self.beam_size = beam_size

	@torch.no_grad()
	def generate(
		self,
		images: Iterable,
		max_length: int | None = None,
		num_beams: int | None = None,
	) -> list[str]:
		images = list(images)
		if not images:
			return []
		pixel_values = self.processor(images=images, return_tensors="pt").pixel_values
		pixel_values = pixel_values.to(self.device)
		ids = self.model.generate(
			pixel_values,
			max_length=max_length or self.max_length,
			num_beams=num_beams or self.beam_size,
		)
		return self.processor.batch_decode(ids, skip_special_tokens=True)
