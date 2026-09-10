import faiss
import numpy as np
import json
from pathlib import Path
from src.intents.classifier import IntentClassifier

def jaccard_similarity(text1, text2):
    t1 = set(text1.lower().split())
    t2 = set(text2.lower().split())
    if not t1 or not t2:
        return 0.0
    return len(t1.intersection(t2)) / len(t1.union(t2))

class EvidenceRetriever:
    def __init__(self, index_path="models/evidence.index", metadata_path="models/evidence_metadata.json"):
        # We reuse the classifier to avoid loading the MiniLM model twice in memory
        self.classifier = IntentClassifier()
        
        self.index = faiss.read_index(str(index_path))
        with open(metadata_path, "r", encoding="utf-8") as f:
            self.metadata = json.load(f)
            
    def retrieve(self, query_text, top_k=3, k_retrieve=20):
        # 1. Semantic Intent & Risk Extraction
        class_res = self.classifier.predict(query_text)
        
        # 2. OOD Handling
        if class_res["routing"] == "HUMAN_FALLBACK" and class_res["intent"] == "UNKNOWN":
            return {
                "status": "NO_RELIABLE_EVIDENCE",
                "reason": "OOD_QUERY",
                "predicted_intent": "UNKNOWN",
                "risk_flags": class_res["risk_flags"],
                "evidence": []
            }
            
        pred_intent = class_res["intent"]
        risk_flags = class_res["risk_flags"]
        flag_names = [f["risk_flag"] for f in risk_flags] if risk_flags and isinstance(risk_flags[0], dict) else risk_flags
        pred_risk = set(flag_names)
        
        # 3. Retrieval
        embed = self.classifier.encoder.encode([query_text])
        faiss.normalize_L2(embed)
        distances, indices = self.index.search(embed, k_retrieve)
        
        distances = distances[0]
        indices = indices[0]
        
        if len(distances) == 0 or distances[0] < 0.40:
            return {
                "status": "NO_RELIABLE_EVIDENCE",
                "reason": "LOW_SIMILARITY",
                "predicted_intent": pred_intent,
                "risk_flags": class_res["risk_flags"],
                "evidence": []
            }
            
        # 4. Intent-Aware Scoring & Metadata Filtering
        scored_items = []
        for dist, idx in zip(distances, indices):
            if idx < 0 or idx >= len(self.metadata):
                continue
                
            item = self.metadata[idx]
            final_score = float(dist)
            
            # Boost for intent agreement
            if item["intent"] == pred_intent:
                final_score += 0.05
                
            # Boost for risk overlap
            item_risk = set(item.get("risk_flags", []))
            if pred_risk and len(pred_risk.intersection(item_risk)) > 0:
                final_score += 0.05
                
            scored_items.append({
                "item": item,
                "raw_sim": float(dist),
                "adjusted_score": final_score
            })
            
        # Sort by adjusted score descending
        scored_items.sort(key=lambda x: x["adjusted_score"], reverse=True)
        
        # 5. Risk Contradiction Filter
        # If query has high severity risk (e.g., BAN_APPEAL) but top evidence doesn't, abstain.
        if "BAN_APPEAL" in pred_risk:
            found_ban = any("BAN_APPEAL" in x["item"].get("risk_flags", []) for x in scored_items[:5])
            if not found_ban:
                return {
                    "status": "NO_RELIABLE_EVIDENCE",
                    "reason": "CONTRADICTORY_RISK_BAN_APPEAL",
                    "predicted_intent": pred_intent,
                    "risk_flags": class_res["risk_flags"],
                    "evidence": []
                }
        if "LEGAL_THREAT" in pred_risk:
            found_legal = any("LEGAL_THREAT" in x["item"].get("risk_flags", []) for x in scored_items[:5])
            if not found_legal:
                return {
                    "status": "NO_RELIABLE_EVIDENCE",
                    "reason": "CONTRADICTORY_RISK_LEGAL_THREAT",
                    "predicted_intent": pred_intent,
                    "risk_flags": class_res["risk_flags"],
                    "evidence": []
                }
                
        # 6. Deduplication (Diversity Selection)
        final_evidence = []
        for scored in scored_items:
            candidate_text = scored["item"]["historical_brand_response"]
            
            is_dup = False
            for accepted in final_evidence:
                accepted_text = accepted["historical_brand_response"]
                if jaccard_similarity(candidate_text, accepted_text) > 0.8:
                    is_dup = True
                    break
                    
            if not is_dup:
                ev = scored["item"].copy()
                ev["raw_sim"] = scored["raw_sim"]
                ev["adjusted_score"] = scored["adjusted_score"]
                final_evidence.append(ev)
                
            if len(final_evidence) >= top_k:
                break
                
        if not final_evidence:
            return {
                "status": "NO_RELIABLE_EVIDENCE",
                "reason": "ALL_DUPLICATES_OR_EMPTY",
                "predicted_intent": pred_intent,
                "risk_flags": class_res["risk_flags"],
                "evidence": []
            }
            
        return {
            "status": "SUCCESS",
            "predicted_intent": pred_intent,
            "risk_flags": class_res["risk_flags"],
            "evidence": final_evidence
        }
