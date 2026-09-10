import re
import numpy as np

class HybridRiskDetector:
    def __init__(self, encoder):
        self.encoder = encoder
        
        # 1. Regex Patterns (High Precision)
        self.regex_patterns = {
            'BAN_APPEAL': r'\b(ban|banned|suspended|unban)\b',
            'ACCOUNT_COMPROMISED': r'\b(hacked|stolen|compromised|unauthorized)\b',
            'PROGRESSION_DATA_LOSS': r'\b(stats reset|reset my stats|lost all my stats)\b',
            'LEGAL_THREAT': r'\b(sue|lawyer|legal|lawsuit|class action)\b',
            'PAYMENT': r'\b(payment|charged|refund|money back|dollars|buy|bought|purchase)\b',
            'GAME_INTEGRITY': r'\b(aimbot|hacker|boosting|out of map|exploit|cheating)\b'
        }
        
        # 2. Semantic Anchors (High Recall)
        self.semantic_anchors = {
            'BAN_APPEAL': [
                "I was banned for no reason",
                "unban my account please",
                "my account got suspended unfairly"
            ],
            'ACCOUNT_COMPROMISED': [
                "someone hacked into my account",
                "my account was stolen",
                "unauthorized access to my profile",
                "h4cked account"
            ],
            'LEGAL_THREAT': [
                "I will sue your company",
                "I am contacting my lawyer",
                "I am filing a class action lawsuit",
                "taking legal action against you"
            ],
            'PAYMENT': [
                "I want a refund right now",
                "I was charged twice for this",
                "give me my money back",
                "unauthorized charge on my credit card"
            ],
            'GAME_INTEGRITY': [
                "this guy is using an aimbot",
                "report a hacker in my lobby",
                "he is exploiting the map glitch",
                "selling boosting services"
            ]
        }
        
        # Encode anchors once during initialization
        self.encoded_anchors = {}
        for risk_type, phrases in self.semantic_anchors.items():
            emb = self.encoder.encode(phrases)
            # Normalize for cosine similarity
            emb_norm = emb / np.linalg.norm(emb, axis=1, keepdims=True)
            self.encoded_anchors[risk_type] = {
                "phrases": phrases,
                "embeddings": emb_norm
            }
            
        # 3. Thresholds
        self.thresholds = {
            "BAN_APPEAL": 0.72,
            "ACCOUNT_COMPROMISED": 0.70,
            "PAYMENT": 0.75,
            "LEGAL_THREAT": 0.72,
            "GAME_INTEGRITY": 0.70,
            "PROGRESSION_DATA_LOSS": 0.75
        }
        
    def detect(self, text, mode="hybrid"):
        """
        mode: "regex", "semantic", or "hybrid"
        """
        text_lower = text.lower()
        results = []
        
        # Check Regex
        if mode in ["regex", "hybrid"]:
            for flag, pattern in self.regex_patterns.items():
                if re.search(pattern, text_lower):
                    results.append({
                        "risk_flag": flag,
                        "detection_method": "REGEX",
                        "risk_score": 1.0,
                        "matched_anchor": None
                    })
                    
        # Check Semantic
        if mode in ["semantic", "hybrid"]:
            # Need to encode query
            query_emb = self.encoder.encode([text])[0]
            query_norm = query_emb / np.linalg.norm(query_emb)
            
            for risk_type, anchor_data in self.encoded_anchors.items():
                # Skip if already detected via regex in hybrid mode
                if mode == "hybrid" and any(r["risk_flag"] == risk_type for r in results):
                    continue
                    
                sims = np.dot(anchor_data["embeddings"], query_norm)
                max_sim_idx = np.argmax(sims)
                max_sim = float(sims[max_sim_idx])
                
                threshold = self.thresholds.get(risk_type, 0.75)
                
                if max_sim >= threshold:
                    results.append({
                        "risk_flag": risk_type,
                        "detection_method": "SEMANTIC",
                        "risk_score": max_sim,
                        "matched_anchor": anchor_data["phrases"][max_sim_idx]
                    })
                    
        return results
