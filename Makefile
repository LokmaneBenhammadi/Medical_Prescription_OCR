PYTHON ?= python
PIP ?= pip
UVICORN ?= uvicorn
HOST ?= 0.0.0.0
PORT ?= 8000
CONFIG ?= configs/config.yaml
IMAGE ?= path/to/prescription.jpg

<<<<<<< HEAD
.PHONY: help install run-api train infer check clean data
=======
.PHONY: help install run-api train infer check clean
>>>>>>> d6de15d804c1f02f1e2b51690b648d0bf7a8c1c9

help:
	@echo "Available targets:"
	@echo "  make install     - Install dependencies from requirements.txt"
	@echo "  make run-api     - Run FastAPI server (development mode)"
	@echo "  make train       - Placeholder training command"
	@echo "  make infer       - Placeholder inference command"
	@echo "  make check       - Syntax-check core Python modules"
	@echo "  make clean       - Remove Python cache artifacts"
<<<<<<< HEAD
	@echo "  make data        - Download automated datasets"
=======
>>>>>>> d6de15d804c1f02f1e2b51690b648d0bf7a8c1c9

install:
	$(PIP) install -r requirements.txt

<<<<<<< HEAD
data:
	$(PYTHON) scripts/download_data.py

=======
>>>>>>> d6de15d804c1f02f1e2b51690b648d0bf7a8c1c9
run-api:
	$(UVICORN) api.main:app --host $(HOST) --port $(PORT) --reload

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