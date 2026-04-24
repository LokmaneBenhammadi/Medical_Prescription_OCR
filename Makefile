PYTHON ?= python
PIP ?= pip
UVICORN ?= uvicorn
NPM ?= npm
HOST ?= 0.0.0.0
PORT ?= 8000
CONFIG ?= configs/config.yaml
IMAGE ?= path/to/prescription.jpg
FRONTEND_DIR ?= frontend

.PHONY: help install install-frontend run-api run-frontend train infer check clean data

help:
	@echo "Available targets:"
	@echo "  make install          - Install backend dependencies from requirements.txt"
	@echo "  make install-frontend - Install frontend dependencies"
	@echo "  make run-api          - Run FastAPI server (development mode)"
	@echo "  make run-frontend     - Run React frontend (development mode)"
	@echo "  make train            - Placeholder training command"
	@echo "  make infer            - Run OCR inference on one image"
	@echo "  make check            - Syntax-check core Python modules"
	@echo "  make clean            - Remove Python cache artifacts"
	@echo "  make data             - Download automated datasets"

install:
	$(PIP) install -r requirements.txt

install-frontend:
	cd $(FRONTEND_DIR) && $(NPM) install

data:
	$(PYTHON) scripts/download_data.py

run-api:
	CONFIG_PATH=$(CONFIG) $(UVICORN) api.main:app --host $(HOST) --port $(PORT) --reload

run-frontend:
	cd $(FRONTEND_DIR) && $(NPM) run dev

train:
	$(PYTHON) -m src.train --config $(CONFIG)

infer:
	$(PYTHON) -m src.inference --config $(CONFIG) --image $(IMAGE)

check:
	$(PYTHON) -m py_compile \
		api/main.py api/schemas.py api/utils.py \
		src/__init__.py src/dataset.py src/model.py src/train.py \
		src/evaluate.py src/preprocess.py src/postprocess.py src/inference.py \
		src/detection/__init__.py src/detection/detector.py

clean:
	find . -type d -name "__pycache__" -prune -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
