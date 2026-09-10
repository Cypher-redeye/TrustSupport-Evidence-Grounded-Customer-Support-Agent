import json
import logging
import numpy as np
from pathlib import Path
from src.config import settings

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
CACHE_FILE = Path(settings.processed_data_dir) / "intent_embeddings.npz"

def load_data(file_path: Path):
    requests = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            requests.append(json.loads(line))
    return requests

def run_embedding():
    input_file = Path(settings.processed_data_dir) / "intent_discovery_sample.jsonl"
    
    if not input_file.exists():
        logger.error("Sample file not found.")
        return
        
    requests = load_data(input_file)
    logger.info(f"Loaded {len(requests)} request blocks for embedding.")
    
    request_ids = np.array([r['request_id'] for r in requests])
    
    # Check cache
    if CACHE_FILE.exists():
        try:
            cache = np.load(CACHE_FILE)
            cached_ids = cache['request_ids']
            cached_model = str(cache['model_name'])
            
            if cached_model == MODEL_NAME and np.array_equal(cached_ids, request_ids):
                logger.info("Valid embedding cache found. Skipping recomputation.")
                return
            else:
                logger.info("Cache is invalid or outdated (mismatched ids or model). Recomputing...")
        except Exception as e:
            logger.warning(f"Failed to load cache: {e}. Recomputing...")

    logger.info(f"Loading embedding model: {MODEL_NAME}")
    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer(MODEL_NAME)
    
    texts = [r['cleaned_text'] for r in requests]
    
    logger.info("Computing embeddings. This may take a few minutes...")
    embeddings = model.encode(texts, show_progress_bar=True, batch_size=256)
    
    logger.info(f"Saving embeddings to {CACHE_FILE}")
    np.savez_compressed(
        CACHE_FILE, 
        embeddings=embeddings, 
        request_ids=request_ids,
        model_name=MODEL_NAME,
        random_seed=settings.random_seed,
        num_messages=len(requests)
    )
    logger.info("Embeddings cached successfully.")

if __name__ == "__main__":
    run_embedding()
