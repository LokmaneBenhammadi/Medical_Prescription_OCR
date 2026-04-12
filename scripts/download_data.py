import os
import zipfile
import urllib.request
from pathlib import Path

# Try importing huggingface_hub, provide a graceful fallback if not installed
try:
    from huggingface_hub import snapshot_download
    HF_AVAILABLE = True
except ImportError:
    HF_AVAILABLE = False

DATA_DIR = Path("data/raw")

def download_funsd():
    funsd_dir = DATA_DIR / "funsd"
    funsd_dir.mkdir(parents=True, exist_ok=True)
    
    url = "https://guillaumejaume.github.io/FUNSD/dataset.zip"
    zip_path = funsd_dir / "dataset.zip"
    
    if (funsd_dir / "dataset").exists():
        print("✅ FUNSD dataset already exists.")
        return

    print(f"⬇️ Downloading FUNSD dataset from {url}...")
    urllib.request.urlretrieve(url, zip_path)
    
    print("📦 Extracting FUNSD dataset...")
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(funsd_dir)
    
    # Remove the zip file after extraction
    os.remove(zip_path)
    print("✅ FUNSD dataset downloaded and extracted successfully.\n")

def download_medical_prescription():
    med_dir = DATA_DIR / "medical-prescription-dataset"
    med_dir.mkdir(parents=True, exist_ok=True)
    
    if not HF_AVAILABLE:
        print("⚠️  'huggingface_hub' is not installed. Skipping Medical Prescription Dataset.")
        print("   -> To install: pip install huggingface_hub")
        print("   -> Or run: pip install -r requirements.txt\n")
        return

    print("⬇️ Downloading Medical Prescription Dataset from Hugging Face...")
    try:
        snapshot_download(
            repo_id="chinmays18/medical-prescription-dataset",
            repo_type="dataset",
            local_dir=med_dir,
            local_dir_use_symlinks=False
        )
        print("✅ Medical Prescription Dataset downloaded successfully.\n")
    except Exception as e:
        print(f"❌ Failed to download Medical Prescription Dataset: {e}\n")

def notify_iam_dataset():
    print("ℹ️  IAM Handwriting Database Requires Manual Download")
    print("   1. Register at: https://fki.tic.heia-fr.ch/databases/iam-handwriting-database")
    print("   2. Download the data files.")
    print("   3. Extract them into the 'data/raw/iam' directory.\n")

def main():
    print("🚀 Starting Dataset Download Process...\n")
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    
    download_medical_prescription()
    download_funsd()
    notify_iam_dataset()
    
    print("🎉 All automated downloads completed!")
    print(f"📁 Check your datasets in: {DATA_DIR.absolute()}")

if __name__ == "__main__":
    main()
