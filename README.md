# medical_prescription_ocr

Deep learning project for extracting text from handwritten medical prescription images with a fine-tuned TrOCR model, a FastAPI backend, and a simple React frontend for local testing.

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
├── frontend/
│   ├── src/
│   ├── package.json
│   └── vite.config.js
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

## 5) Local Web App

Run the backend and frontend in two terminals.

### Backend

```bash
pip install -r requirements.txt
uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
```

The backend loads the fine-tuned Hugging Face model from `khedim/Medical-Prescription-OCR`.

### Fully Offline CPU Setup

Use this flow if you want to run everything locally on CPU after downloading the model once.

1. Download the checkpoint from Hugging Face into the repo:

```bash
hf download khedim/Medical-Prescription-OCR \
	--local-dir checkpoints/medical-prescription-ocr
```

2. Point the app at the local checkpoint by updating `configs/config.yaml`:

```yaml
model:
	name: "checkpoints/medical-prescription-ocr"
```

3. Start the backend in offline mode so it does not contact Hugging Face again:

```bash
export TRANSFORMERS_OFFLINE=1
export HF_HUB_OFFLINE=1
uvicorn api.main:app --host 127.0.0.1 --port 8000 --reload
```

4. Start the frontend in a second terminal:

```bash
cd frontend
npm install
npm run dev
```

5. Open the app in your browser:

```text
http://127.0.0.1:5173
```

### Frontend

If you are not using the offline CPU flow above, run the frontend in a second terminal with `cd frontend`, `npm install`, and `npm run dev`, then open `http://127.0.0.1:5173`.

If you want to point the frontend to a different API URL, create `frontend/.env` with:

```bash
VITE_API_URL=http://127.0.0.1:8000
```

## 6) Dataset Sources

1. Medical Prescription Dataset (Hugging Face)  
	 https://huggingface.co/datasets/chinmays18/medical-prescription-dataset
2. IAM Handwriting Database  
	 https://fki.tic.heia-fr.ch/databases/iam-handwriting-database
3. FUNSD (Form Understanding in Noisy Scanned Documents)  
	 https://guillaumejaume.github.io/FUNSD/

## 7) How to Train

```bash
python -m src.train --config configs/config.yaml
```

## 8) How to Run Inference

```bash
python -m src.inference --config configs/config.yaml --image path/to/prescription.jpg
```

## 9) How to Run the API

```bash
uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
```

## 10) API Endpoints

### GET /health

Checks service status.

```bash
curl -X GET http://127.0.0.1:8000/health
```

Example response:

```json
{
	"status": "ok",
	"model_loaded": "true"
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
	"raw_text": "clinic_name: Meadowview Health\nclinic_address: 45 Oak Ave.",
	"lines": [
		"clinic_name: Meadowview Health",
		"clinic_address: 45 Oak Ave."
	],
	"image_id": "prescription.png",
	"line_count": 2,
	"processing_ms": 1842.37
}
```

## 11) Tech Stack

| Component | Technology |
|---|---|
| Deep Learning | PyTorch |
| OCR Backbone | TrOCR (Hugging Face Transformers) |
| API Layer | FastAPI |
| Frontend | React + Vite |
| Image Processing | OpenCV |
| Model/Dataset Hub | Hugging Face |

## 12) Notes

- Default local config uses `device: auto`, so the model runs on CPU when CUDA is unavailable.
- For faster local CPU inference, the default API config uses beam size `2`.
- The frontend is intentionally minimal: upload an image, run OCR, and inspect raw text plus line-by-line output.
