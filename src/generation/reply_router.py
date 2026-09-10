from typing import List

class ReplyRouter:
    """
    Determines the reply mode based on classification, risk, and retrieval signals.
    """
    
    SEVERE_RISKS = {"BAN_APPEAL", "ACCOUNT_COMPROMISED", "PAYMENT", "LEGAL_THREAT"}
    
    @classmethod
    def determine_mode(
        cls, 
        intent: str, 
        confidence_level: str, 
        risk_flags: List[dict], 
        retrieval_status: str, 
        max_similarity: float
    ) -> str:
        """
        Returns one of:
        - ESCALATE
        - ABSTAIN
        - CLARIFY
        - CAUTIOUS_REPLY
        - GROUNDED_REPLY
        """
        
        flag_names = [f["risk_flag"] for f in risk_flags] if risk_flags and isinstance(risk_flags[0], dict) else risk_flags
        
        # 1. Severe Risk Check
        if any(r in cls.SEVERE_RISKS for r in flag_names):
            return "ESCALATE"
            
        # 2. Retrieval Failure Check
        if retrieval_status != "SUCCESS":
            return "ABSTAIN"
            
        if max_similarity < 0.40:
            return "ABSTAIN"
            
        # 3. Confidence and Similarity Check
        if confidence_level == "LOW" and max_similarity < 0.50:
            return "CLARIFY"
            
        # 4. Game Integrity or Medium Confidence
        if "GAME_INTEGRITY" in flag_names or confidence_level == "LOW":
            return "CAUTIOUS_REPLY"
            
        # 5. Default Success
        return "GROUNDED_REPLY"
