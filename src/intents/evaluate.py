import json
import logging
import joblib
import time
import numpy as np
import pandas as pd
from pathlib import Path
from sklearn.metrics import f1_score, accuracy_score, precision_score, recall_score, confusion_matrix
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
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

def evaluate_models():
    logger.info("Loading test set...")
    X_test, y_test = load_split('test')
    
    models_dir = Path("models")
    results_dir = Path("results")
    results_dir.mkdir(exist_ok=True)
    
    results = []
    
    # 1. TF-IDF + LR
    logger.info("Evaluating TF-IDF + LR...")
    lr_model = joblib.load(models_dir / "tfidf_lr.joblib")
    with open(models_dir / "tfidf_lr_metadata.json", "r") as f:
        lr_meta = json.load(f)
        
    start_time = time.time()
    lr_preds = lr_model.predict(X_test)
    lr_inf_time = (time.time() - start_time) / len(X_test) * 1000
    
    results.append(compute_metrics(y_test, lr_preds, "TF-IDF + LR", lr_meta, lr_inf_time))
    save_confusion_matrix(y_test, lr_preds, "tfidf_lr", results_dir)
    
    # 2. TF-IDF + SVM
    logger.info("Evaluating TF-IDF + SVM...")
    svm_model = joblib.load(models_dir / "tfidf_svm.joblib")
    with open(models_dir / "tfidf_svm_metadata.json", "r") as f:
        svm_meta = json.load(f)
        
    start_time = time.time()
    svm_preds = svm_model.predict(X_test)
    svm_inf_time = (time.time() - start_time) / len(X_test) * 1000
    
    results.append(compute_metrics(y_test, svm_preds, "TF-IDF + Linear SVM", svm_meta, svm_inf_time))
    save_confusion_matrix(y_test, svm_preds, "tfidf_svm", results_dir)
    
    # 3. Embedding models setup
    logger.info("Generating test embeddings...")
    st_model = SentenceTransformer('all-MiniLM-L6-v2')
    start_time = time.time()
    test_embeds = st_model.encode(X_test)
    embed_base_time = (time.time() - start_time) / len(X_test) * 1000
    
    # 4. Embedding Centroid
    logger.info("Evaluating Embedding Centroid...")
    embed_centroids = np.load(models_dir / "embedding_centroids.npz")
    centroids = embed_centroids['centroids']
    intents = embed_centroids['intents']
    with open(models_dir / "embedding_centroid_metadata.json", "r") as f:
        cent_meta = json.load(f)
        
    start_time = time.time()
    sims = cosine_similarity(test_embeds, centroids)
    cent_preds = [intents[np.argmax(sims[i])] for i in range(len(test_embeds))]
    cent_inf_time = (time.time() - start_time) / len(X_test) * 1000 + embed_base_time
    
    results.append(compute_metrics(y_test, cent_preds, "Embedding Centroid", cent_meta, cent_inf_time))
    save_confusion_matrix(y_test, cent_preds, "embedding_centroid", results_dir)
    
    # 5. Embedding + LR
    logger.info("Evaluating Embedding + LR...")
    elr_model = joblib.load(models_dir / "embedding_lr.joblib")
    with open(models_dir / "embedding_lr_metadata.json", "r") as f:
        elr_meta = json.load(f)
        
    start_time = time.time()
    elr_preds = elr_model.predict(test_embeds)
    elr_inf_time = (time.time() - start_time) / len(X_test) * 1000 + embed_base_time
    
    results.append(compute_metrics(y_test, elr_preds, "Embedding + LR", elr_meta, elr_inf_time))
    save_confusion_matrix(y_test, elr_preds, "embedding_lr", results_dir)
    
    # Save Model Comparison
    df = pd.DataFrame(results)
    df.to_csv(results_dir / "model_comparison.csv", index=False)
    logger.info("Evaluation completed. Results saved to model_comparison.csv.")

def compute_metrics(y_true, y_pred, model_name, meta, inf_time_ms):
    labels = sorted(list(set(y_true)))
    
    mac_f1 = f1_score(y_true, y_pred, average='macro')
    acc = accuracy_score(y_true, y_pred)
    w_f1 = f1_score(y_true, y_pred, average='weighted')
    mac_p = precision_score(y_true, y_pred, average='macro')
    mac_r = recall_score(y_true, y_pred, average='macro')
    
    # Calculate Rare Intent Recall specifically
    rare_intents = ['LOW_FREQUENCY_SPECIAL_CASE', 'PURCHASE_AND_BILLING', 'EXPLOIT_AND_HACKER_REPORT']
    rare_recall_sum = 0
    rare_count = 0
    
    class_recalls = recall_score(y_true, y_pred, labels=labels, average=None)
    for i, label in enumerate(labels):
        if label in rare_intents:
            rare_recall_sum += class_recalls[i]
            rare_count += 1
            
    rare_recall_avg = rare_recall_sum / rare_count if rare_count > 0 else 0
    
    return {
        "model": model_name,
        "validation_macro_f1": meta.get('validation_macro_f1', 0),
        "test_macro_f1": mac_f1,
        "accuracy": acc,
        "weighted_f1": w_f1,
        "macro_precision": mac_p,
        "macro_recall": mac_r,
        "rare_intent_recall": rare_recall_avg,
        "training_time_seconds": meta.get('training_time_seconds', 0),
        "inference_time_ms": inf_time_ms,
        "notes": ""
    }

def save_confusion_matrix(y_true, y_pred, name, results_dir):
    labels = sorted(list(set(y_true)))
    cm = confusion_matrix(y_true, y_pred, labels=labels)
    df = pd.DataFrame(cm, index=labels, columns=labels)
    df.to_csv(results_dir / f"confusion_matrix_{name}.csv")

if __name__ == "__main__":
    evaluate_models()
