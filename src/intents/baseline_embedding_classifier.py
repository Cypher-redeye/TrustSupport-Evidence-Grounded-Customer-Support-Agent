import json
import logging
import joblib
import time
import numpy as np
from pathlib import Path
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score
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
    
    logger.info("Generating embeddings for train and val sets...")
    train_embeddings = model.encode(X_train, show_progress_bar=True)
    val_embeddings = model.encode(X_val, show_progress_bar=True)
    
    param_grid = {
        'C': [0.1, 0.5, 1.0, 2.0],
        'class_weight': [None, 'balanced']
    }
    
    best_f1 = -1
    best_params = None
    best_clf = None

    logger.info("Tuning Embedding + LR on Validation set...")
    
    for c_val in param_grid['C']:
        for cw in param_grid['class_weight']:
            clf = LogisticRegression(C=c_val, class_weight=cw, max_iter=2000, random_state=settings.random_seed)
            clf.fit(train_embeddings, y_train)
            
            preds = clf.predict(val_embeddings)
            f1 = f1_score(y_val, preds, average='macro')
            
            if f1 > best_f1:
                best_f1 = f1
                best_params = {'C': c_val, 'class_weight': cw}
                best_clf = clf
                    
    train_time = time.time() - start_time
    logger.info(f"Best Validation Macro F1: {best_f1:.4f} with params: {best_params}")
    
    # Save Model
    models_dir = Path("models")
    models_dir.mkdir(exist_ok=True)
    joblib.dump(best_clf, models_dir / "embedding_lr.joblib")
    
    # Save Metadata
    metadata = {
        "model": "Embedding + Logistic Regression",
        "selected_hyperparameters": best_params,
        "validation_macro_f1": best_f1,
        "training_time_seconds": train_time,
        "training_timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "dataset_version": "1.0",
        "counts": {
            "train": len(y_train),
            "validation": len(y_val),
            "test": len(y_test)
        }
    }
    
    with open(models_dir / "embedding_lr_metadata.json", "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)

    logger.info("Embedding + LR training completed.")

if __name__ == "__main__":
    train_and_tune()
