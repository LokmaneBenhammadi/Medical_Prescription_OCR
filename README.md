# medical_prescription_ocr

Deep learning project scaffold for extracting structured information from handwritten medical prescription images.

## 1) Architecture Overview

```text
Image
	-> Preprocessing
	-> Line Segmentation
	-> TrOCR
	-> Post-processing
	-> JSON
```

## 2) Project Structure

```text
medical_prescription_ocr/
├── Dockerfile
├── .dockerignore
├── data/
│   ├── raw/
│   ├── processed/
│   └── splits/
├── src/
│   ├── __init__.py
│   ├── dataset.py
│   ├── model.py
│   ├── train.py
│   ├── evaluate.py
│   ├── preprocess.py
│   ├── postprocess.py
│   ├── inference.py
│   └── detection/
│       ├── __init__.py
│       └── detector.py
├── api/
│   ├── __init__.py
│   ├── main.py
│   ├── schemas.py
│   └── utils.py
├── configs/
│   └── config.yaml
├── notebooks/
│   └── exploration.ipynb
├── checkpoints/
│   └── .gitkeep
├── requirements.txt
└── README.md
```

## 3) Installation

### Conda + pip

```bash
conda create -n medical_prescription_ocr python=3.10 -y
conda activate medical_prescription_ocr
pip install -r requirements.txt
```

## 4) Docker (Containerization)

Build the image:

```bash
docker build -t medical-prescription-ocr:latest .
```

Run the containerized API:

```bash
docker run --rm -p 8000:8000 medical-prescription-ocr:latest
```

Test health endpoint:

```bash
curl -X GET http://127.0.0.1:8000/health
```

## 5) Dataset Sources

1. Medical Prescription Dataset (Hugging Face)  
	 https://huggingface.co/datasets/chinmays18/medical-prescription-dataset
2. IAM Handwriting Database  
	 https://fki.tic.heia-fr.ch/databases/iam-handwriting-database
3. FUNSD (Form Understanding in Noisy Scanned Documents)  
	 https://guillaumejaume.github.io/FUNSD/

## 6) How to Train (Placeholder)

```bash
python -m src.train --config configs/config.yaml
```

## 7) How to Run Inference (Placeholder)

```bash
python -m src.inference --config configs/config.yaml --image path/to/prescription.jpg
```

## 8) How to Run the API

```bash
uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
```

## 9) API Endpoints

### GET /health

Checks service status.

```bash
curl -X GET http://127.0.0.1:8000/health
```

Example response:

```json
{
	"status": "ok"
}
```

### POST /predict

Accepts an uploaded prescription image and returns a placeholder response.

```bash
curl -X POST "http://127.0.0.1:8000/predict" \
	-H "accept: application/json" \
	-H "Content-Type: multipart/form-data" \
	-F "image=@/path/to/prescription.jpg"
```

Example response:

```json
{
	"message": "not implemented yet"
}
```

## 10) Tech Stack

| Component | Technology |
|---|---|
| Deep Learning | PyTorch |
| OCR Backbone | TrOCR (Hugging Face Transformers) |
| API Layer | FastAPI |
| Image Processing | OpenCV |
| Model/Dataset Hub | Hugging Face |

## 11) Roadmap / TODO

- [ ] Implement dataset ingestion and split generation
- [ ] Implement preprocessing and line segmentation pipeline
- [ ] Implement TrOCR model loading and fine-tuning pipeline
- [ ] Implement post-processing for structured prescription extraction
- [ ] Implement inference pipeline and confidence scoring
- [ ] Add evaluation metrics and experiment tracking
- [ ] Add API model integration and prediction serialization
- [ ] Add tests, CI checks, and deployment packaging
