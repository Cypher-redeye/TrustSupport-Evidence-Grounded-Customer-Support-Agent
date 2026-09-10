import os
import logging
from pathlib import Path
from src.config import settings

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

DATASET_NAME = "thoughtvector/customer-support-on-twitter"

def find_dataset(raw_dir: Path) -> Path | None:
    """Detects the exact location of the dataset under data/raw/."""
    expected_exact = raw_dir / "twcs" / "twcs.csv"
    if expected_exact.exists():
        return expected_exact
        
    for path in raw_dir.rglob("*.csv"):
        if path.name.lower() == "twcs.csv":
            return path
    return None

def is_kaggle_configured() -> bool:
    """Check if Kaggle API is configured."""
    kaggle_dir = Path.home() / ".kaggle"
    kaggle_json = kaggle_dir / "kaggle.json"
    
    has_env_vars = bool(os.environ.get("KAGGLE_USERNAME") and os.environ.get("KAGGLE_KEY"))
    has_config_file = kaggle_json.exists()
    
    return has_env_vars or has_config_file

def download_dataset():
    """Download the dataset from Kaggle if not already present."""
    raw_dir = Path(settings.raw_data_dir)
    
    existing_csv = find_dataset(raw_dir)
    if existing_csv:
        logger.info(f"Dataset already found at {existing_csv}. Skipping download.")
        return True

    if not is_kaggle_configured():
        logger.error(
            "Kaggle API credentials not found. \n"
            "Please configure the Kaggle API by placing your kaggle.json in ~/.kaggle/ "
            "or setting KAGGLE_USERNAME and KAGGLE_KEY environment variables.\n"
            "Alternatively, manually download the dataset from:\n"
            f"https://www.kaggle.com/datasets/{DATASET_NAME}\n"
            f"Extract it and place `twcs.csv` at `{raw_dir.absolute()}/twcs/twcs.csv`."
        )
        return False
    
    try:
        import kaggle
        logger.info(f"Downloading dataset {DATASET_NAME} to {raw_dir}...")
        kaggle.api.authenticate()
        kaggle.api.dataset_download_files(DATASET_NAME, path=str(raw_dir), unzip=True)
        
        target_csv = raw_dir / "twcs" / "twcs.csv"
        direct_csv = raw_dir / "twcs.csv"
        if direct_csv.exists() and not target_csv.exists():
            target_csv.parent.mkdir(exist_ok=True, parents=True)
            direct_csv.rename(target_csv)
            logger.info("Moved twcs.csv to twcs/twcs.csv")

        if target_csv.exists():
            logger.info(f"Successfully downloaded and extracted dataset to {target_csv}")
            return True
        else:
            logger.warning(f"Downloaded but could not find twcs.csv in {raw_dir}. Please check extraction manually.")
            return False

    except Exception as e:
        logger.error(f"Failed to download dataset: {e}")
        return False

if __name__ == "__main__":
    download_dataset()
