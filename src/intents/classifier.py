import json
import joblib
import numpy as np
from pathlib import Path
from sentence_transformers import SentenceTransformer
from src.intents.risk_detector import HybridRiskDetector

class IntentClassifier:
    def __init__(self, model_path="models/embedding_lr.joblib", thresholds_path="results/confidence_thresholds.json", centroids_path="models/embedding_centroids.npz"):
        # Hybrid Architecture: Semantic Embedding + LR for classification, Deterministic Regex for risk flags.
        self.model = joblib.load(model_path)
        self.encoder = SentenceTransformer('all-MiniLM-L6-v2')
        self.risk_detector = HybridRiskDetector(self.encoder)
        
        # Load centroids for Out-of-Domain distance checking
        embed_centroids = np.load(centroids_path)
        self.centroids = embed_centroids['centroids']
        
        with open(thresholds_path, "r") as f:
            data = json.load(f)
            self.thresholds = data["thresholds"]
            
    def _determine_routing(self, intent, risk_flags, confidence_level):
        flag_names = [f["risk_flag"] for f in risk_flags]
        if 'BAN_APPEAL' in flag_names or 'LEGAL_THREAT' in flag_names or 'ACCOUNT_COMPROMISED' in flag_names:
            return "ESCALATE"
        if intent in ['LOW_FREQUENCY_SPECIAL_CASE', 'EXPLOIT_AND_HACKER_REPORT'] and confidence_level in ['HIGH', 'MEDIUM']:
            return "ESCALATE"
        if confidence_level == 'UNKNOWN':
            return "HUMAN_FALLBACK"
        return "AUTO_HANDLE"
        
    def predict(self, text):
        # Generate embedding
        embed = self.encoder.encode([text])
        
        # OOD check using centroid distance
        embed_norm = embed / np.linalg.norm(embed, axis=1, keepdims=True)
        sims = np.dot(embed_norm, self.centroids.T)[0]
        max_sim = np.max(sims)
        
        # Risk flags
        risk_flags = self.risk_detector.detect(text, mode="hybrid")
        
        if max_sim < 0.30:
            return {
                "intent": "UNKNOWN",
                "confidence_level": "UNKNOWN",
                "confidence_score": float(max_sim),
                "margin": 0.0,
                "risk_flags": risk_flags,
                "routing": "HUMAN_FALLBACK",
                "model": "Embedding + LR (OOD Filter)",
                "should_escalate": False
            }
            
        # Infer probabilities
        probs = self.model.predict_proba(embed)[0]
        pred_idx = np.argmax(probs)
        intent = self.model.classes_[pred_idx]
        confidence_score = float(probs[pred_idx])
        
        # Calculate margin
        sorted_probs = np.sort(probs)
        margin = float(sorted_probs[-1] - sorted_probs[-2])
        
        # Confidence Level mapping
        if confidence_score > self.thresholds['HIGH']:
            confidence_level = "HIGH"
        elif confidence_score > self.thresholds['MEDIUM']:
            confidence_level = "MEDIUM"
        elif confidence_score > self.thresholds['LOW']:
            confidence_level = "LOW"
        else:
            confidence_level = "UNKNOWN"
            intent = "UNKNOWN"
            
        # Intent Correction for Technical Support queries
        if intent == "INFORMATION_AND_OTHER_REQUESTS" and confidence_level != "UNKNOWN":
            technical_markers = ["crash", "freeze", "launch", "load", "update", "connect", "startup", "won't open", "broken", "bug"]
            if any(marker in text.lower() for marker in technical_markers):
                intent = "CONNECTIVITY_AND_ERRORS"
            
        # Routing logic
        routing = self._determine_routing(intent, risk_flags, confidence_level)
        
        return {
            "intent": intent,
            "confidence_level": confidence_level,
            "confidence_score": confidence_score,
            "margin": margin,
            "risk_flags": risk_flags,
            "routing": routing,
            "model": "Embedding + LR",
            "should_escalate": (routing == "ESCALATE")
        }
