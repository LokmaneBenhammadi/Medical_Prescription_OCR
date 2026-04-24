"""Inference entry points for running OCR on new prescription images."""

<<<<<<< HEAD
from __future__ import annotations

import argparse
from dataclasses import dataclass
from typing import Any

import yaml
from PIL import Image

from .detection.detector import detect_line_bboxes
from .model import TrOCREngine
from .preprocess import preprocess_image


@dataclass
class PipelineConfig:
	model_name: str
	max_length: int
	beam_size: int
	device: str
	min_line_height: int
	preprocess_for_lines: bool


def _load_config(path: str) -> PipelineConfig:
	with open(path, "r", encoding="utf-8") as handle:
		data = yaml.safe_load(handle) or {}

	model_cfg = data.get("model", {})
	infer_cfg = data.get("inference", {})
	detect_cfg = data.get("detection", {})

	return PipelineConfig(
		model_name=model_cfg.get("name", "microsoft/trocr-base-handwritten"),
		max_length=int(model_cfg.get("max_length", 128)),
		beam_size=int(infer_cfg.get("beam_size", 4)),
		device=str(infer_cfg.get("device", "auto")),
		min_line_height=int(detect_cfg.get("min_line_height", 15)),
		preprocess_for_lines=bool(detect_cfg.get("preprocess_for_lines", True)),
	)


class OCRPipeline:
	"""Line-level OCR pipeline for prescription images."""

	def __init__(self, config: PipelineConfig) -> None:
		self.config = config
		self.engine = TrOCREngine(
			model_name=config.model_name,
			device=config.device,
			max_length=config.max_length,
			beam_size=config.beam_size,
		)

	@classmethod
	def from_config(cls, config_path: str) -> "OCRPipeline":
		return cls(_load_config(config_path))

	def predict(self, image: Image.Image) -> dict[str, Any]:
		original = image.convert("RGB")
		working = (
			preprocess_image(original, apply_binarize=False)
			if self.config.preprocess_for_lines
			else original
		)

		bboxes = detect_line_bboxes(working, min_height=self.config.min_line_height)
		if not bboxes:
			line_images = [original]
		else:
			line_images = [
				original.crop((0, top, original.width, bottom))
				for top, bottom in bboxes
			]

		preds = [p.strip() for p in self.engine.generate(line_images)]
		raw_text = "\n".join([p for p in preds if p])
		return {"raw_text": raw_text, "lines": preds, "bboxes": bboxes}


def main() -> None:
	parser = argparse.ArgumentParser(description="Run line-level OCR on a prescription image")
	parser.add_argument("--config", default="configs/config.yaml")
	parser.add_argument("--image", required=True)
	args = parser.parse_args()

	pipeline = OCRPipeline.from_config(args.config)
	image = Image.open(args.image).convert("RGB")
	result = pipeline.predict(image)
	print(result["raw_text"])


if __name__ == "__main__":
	main()
=======
# import torch
# from PIL import Image
>>>>>>> d6de15d804c1f02f1e2b51690b648d0bf7a8c1c9
