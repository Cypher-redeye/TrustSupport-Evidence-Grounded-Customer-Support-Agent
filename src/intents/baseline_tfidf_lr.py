import json
import logging
import joblib
import time
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import f1_score
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
    logger.info("Loading dataset splits...")
    X_train, y_train = load_split('train')
    X_val, y_val = load_split('validation')
    X_test, y_test = load_split('test')

    param_grid = {
        'ngram_range': [(1, 1), (1, 2), (1, 3)],
        'min_df': [1, 2, 3],
        'max_features': [10000, 20000, 30000]
    }
    
    best_f1 = -1
    best_params = None
    best_pipeline = None

    logger.info("Tuning TF-IDF + Logistic Regression on Validation set...")
    start_time = time.time()
    
    for ngram in param_grid['ngram_range']:
        for min_df in param_grid['min_df']:
            for max_feat in param_grid['max_features']:
                pipeline = Pipeline([
                    ('tfidf', TfidfVectorizer(ngram_range=ngram, min_df=min_df, max_features=max_feat)),
                    ('clf', LogisticRegression(class_weight='balanced', max_iter=1000, random_state=settings.random_seed))
                ])
                
                pipeline.fit(X_train, y_train)
                preds = pipeline.predict(X_val)
                f1 = f1_score(y_val, preds, average='macro')
                
                if f1 > best_f1:
                    best_f1 = f1
                    best_params = {'ngram_range': ngram, 'min_df': min_df, 'max_features': max_feat}
                    best_pipeline = pipeline
                    
    train_time = time.time() - start_time
    logger.info(f"Best Validation Macro F1: {best_f1:.4f} with params: {best_params}")
    
    # Save Model
    models_dir = Path("models")
    models_dir.mkdir(exist_ok=True)
    joblib.dump(best_pipeline, models_dir / "tfidf_lr.joblib")
    
    # Save Metadata
    metadata = {
        "model": "TF-IDF + Logistic Regression",
        "selected_hyperparameters": best_params,
        "vocabulary_size": len(best_pipeline.named_steps['tfidf'].vocabulary_),
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
    
    with open(models_dir / "tfidf_lr_metadata.json", "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)

    logger.info("TF-IDF + LR training completed.")

if __name__ == "__main__":
    train_and_tune()
