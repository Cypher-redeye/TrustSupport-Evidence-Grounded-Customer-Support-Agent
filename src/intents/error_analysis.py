import json
import logging
import joblib
import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from src.config import settings

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def load_split(split_name):
    file_path = Path(settings.processed_data_dir) / f"intent_{split_name}.jsonl"
    data = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            data.append(json.loads(line))
    return data

def run_error_analysis():
    logger.info("Loading validation data for error analysis...")
    val_data = load_split('validation')
    X_val = [ex['text'] for ex in val_data]
    y_val = [ex['intent'] for ex in val_data]
    
    # Analyze best model. Assuming TF-IDF + LR for simplicity as it usually provides clean probabilities.
    # We will load it to extract errors
    models_dir = Path("models")
    lr_model = joblib.load(models_dir / "tfidf_lr.joblib")
    
    preds = lr_model.predict(X_val)
    probs = lr_model.predict_proba(X_val)
    
    classes = lr_model.classes_
    
    errors = []
    corrects = []
    
    for i in range(len(val_data)):
        pred_idx = np.where(classes == preds[i])[0][0]
        conf = probs[i][pred_idx]
        
        ex = val_data[i]
        
        item = {
            "request_id": ex['request_id'],
            "conversation_id": ex['conversation_id'],
            "text": ex['text'],
            "true_intent": ex['intent'],
            "predicted_intent": preds[i],
            "confidence": conf,
            "risk_flags": ex['risk_flags']
        }
        
        if preds[i] != ex['intent']:
            errors.append(item)
        else:
            corrects.append(item)
            
    # 1. Top 20 High-Confidence Errors
    errors.sort(key=lambda x: x['confidence'], reverse=True)
    top_20_errors = errors[:20]
    
    # 2. Low-Confidence Correct Predictions
    corrects.sort(key=lambda x: x['confidence'])
    low_conf_correct = corrects[:10]
    
    # 3. Most Confused Intent Pairs
    confusion_pairs = {}
    for err in errors:
        pair = tuple(sorted([err['true_intent'], err['predicted_intent']]))
        confusion_pairs[pair] = confusion_pairs.get(pair, 0) + 1
        
    top_pairs = sorted(confusion_pairs.items(), key=lambda x: x[1], reverse=True)[:5]
    
    # Generate Report
    report = "# Phase 5: Error Analysis (TF-IDF + LR Validation)\n\n"
    
    report += "## 1. Top 20 High-Confidence Errors\n\n"
    for i, err in enumerate(top_20_errors):
        report += f"### {i+1}. Confidence: {err['confidence']:.4f}\n"
        report += f"- **True Intent:** {err['true_intent']}\n"
        report += f"- **Predicted Intent:** {err['predicted_intent']}\n"
        report += f"- **Risk Flags:** {err['risk_flags']}\n"
        report += f"- **Text:** {err['text']}\n\n"
        
    report += "## 2. Low-Confidence Correct Predictions\n\n"
    for i, corr in enumerate(low_conf_correct):
        report += f"- Confidence: {corr['confidence']:.4f} | Intent: {corr['true_intent']} | Text: {corr['text']}\n"
        
    report += "\n## 3. Most Confused Intent Pairs\n\n"
    for pair, count in top_pairs:
        report += f"- **{pair[0]}** vs **{pair[1]}**: {count} errors\n"
        
    report += "\n## 4. Risk Intent Performance\n\n"
    report += "See full evaluation metrics in `results/model_comparison.csv` for precise recall.\n"
    
    reports_dir = Path("reports")
    reports_dir.mkdir(exist_ok=True)
    with open(reports_dir / "phase5_error_analysis.md", "w", encoding="utf-8") as f:
        f.write(report)
        
    logger.info("Error analysis complete.")

if __name__ == "__main__":
    run_error_analysis()
