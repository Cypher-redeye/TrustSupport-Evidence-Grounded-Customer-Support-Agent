import json
import logging
import joblib
import numpy as np
from pathlib import Path
from sklearn.metrics import accuracy_score
from src.config import settings
from src.intents.error_analysis import load_split

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def determine_thresholds():
    val_data = load_split('validation')
    X_val = [ex['text'] for ex in val_data]
    y_val = [ex['intent'] for ex in val_data]
    
    models_dir = Path("models")
    elr_model = joblib.load(models_dir / "embedding_lr.joblib")
    
    from sentence_transformers import SentenceTransformer
    encoder = SentenceTransformer('all-MiniLM-L6-v2')
    embeds = encoder.encode(X_val, show_progress_bar=False)
    
    probs = elr_model.predict_proba(embeds)
    preds = elr_model.predict(embeds)
    
    # We want to find thresholds for Embedding + LR 
    # High: Confidence > 0.85
    # Medium: 0.50 < Confidence <= 0.85
    # Low: 0.35 < Confidence <= 0.50
    # Unknown: Confidence <= 0.35
    
    # Let's empirically check accuracy at these tiers
    high_acc = []
    med_acc = []
    low_acc = []
    
    high_thresh = 0.85
    med_thresh = 0.50
    low_thresh = 0.35
    
    high_count, med_count, low_count, unk_count = 0, 0, 0, 0
    
    for i in range(len(preds)):
        conf = np.max(probs[i])
        correct = (preds[i] == y_val[i])
        
        if conf > high_thresh:
            high_acc.append(correct)
            high_count += 1
        elif conf > med_thresh:
            med_acc.append(correct)
            med_count += 1
        elif conf > low_thresh:
            low_acc.append(correct)
            low_count += 1
        else:
            unk_count += 1
            
    res = {
        "model": "Embedding + LR",
        "thresholds": {
            "HIGH": high_thresh,
            "MEDIUM": med_thresh,
            "LOW": low_thresh
        },
        "validation_coverage": {
            "HIGH": high_count / len(preds),
            "MEDIUM": med_count / len(preds),
            "LOW": low_count / len(preds),
            "UNKNOWN": unk_count / len(preds)
        },
        "validation_accuracy": {
            "HIGH": np.mean(high_acc) if high_acc else 0,
            "MEDIUM": np.mean(med_acc) if med_acc else 0,
            "LOW": np.mean(low_acc) if low_acc else 0
        },
        "unknown_rate": unk_count / len(preds)
    }
    
    results_dir = Path("results")
    results_dir.mkdir(exist_ok=True)
    with open(results_dir / "confidence_thresholds.json", "w", encoding="utf-8") as f:
        json.dump(res, f, indent=2)
        
    logger.info("Confidence thresholds derived from validation data.")
    
if __name__ == "__main__":
    determine_thresholds()
