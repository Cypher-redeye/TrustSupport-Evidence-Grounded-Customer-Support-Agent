import json
import logging
import time
import numpy as np
from pathlib import Path
from sklearn.metrics import f1_score
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
from src.config import settings

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def load_split(split_name):
    file_path = Path(settings.processed_data_dir) / f"intent_{split_name}.jsonl"
    texts = []
    labels = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            ex = json.loads(line)
            texts.append(ex['text'])
            labels.append(ex['intent'])
    return texts, labels

def train_and_tune():
    logger.info("Loading dataset splits and embedding model...")
    X_train, y_train = load_split('train')
    X_val, y_val = load_split('validation')
    X_test, y_test = load_split('test')

    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    start_time = time.time()
    
    logger.info("Generating embeddings for train set...")
    # Generate embeddings
    train_embeddings = model.encode(X_train, show_progress_bar=True)
    val_embeddings = model.encode(X_val, show_progress_bar=True)
    
    logger.info("Calculating centroids...")
    # Calculate Centroids from Train
    intents = sorted(list(set(y_train)))
    centroids = {}
    
    for intent in intents:
        # Get all embeddings for this intent
        indices = [i for i, y in enumerate(y_train) if y == intent]
        intent_embeds = train_embeddings[indices]
        # Calculate mean vector
        centroid = np.mean(intent_embeds, axis=0)
        # Normalize centroid
        centroid = centroid / np.linalg.norm(centroid)
        centroids[intent] = centroid
        
    train_time = time.time() - start_time
    
    # Predict on Validation
    centroid_matrix = np.array([centroids[i] for i in intents])
    
    # Cosine similarities
    sims = cosine_similarity(val_embeddings, centroid_matrix)
    
    preds = []
    for i in range(len(X_val)):
        best_idx = np.argmax(sims[i])
        preds.append(intents[best_idx])
        
    f1 = f1_score(y_val, preds, average='macro')
    logger.info(f"Validation Macro F1: {f1:.4f}")
    
    # Save Model
    models_dir = Path("models")
    models_dir.mkdir(exist_ok=True)
    
    np.savez(
        models_dir / "embedding_centroids.npz", 
        centroids=centroid_matrix, 
        intents=np.array(intents)
    )
    
    # Save Metadata
    metadata = {
        "model": "Embedding Centroid",
        "validation_macro_f1": f1,
        "training_time_seconds": train_time,
        "training_timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "dataset_version": "1.0",
        "intents": intents,
        "counts": {
            "train": len(y_train),
            "validation": len(y_val),
            "test": len(y_test)
        }
    }
    
    with open(models_dir / "embedding_centroid_metadata.json", "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)

    logger.info("Embedding Centroid training completed.")

if __name__ == "__main__":
    train_and_tune()
