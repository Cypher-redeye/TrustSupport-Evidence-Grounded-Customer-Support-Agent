import re
from typing import List, Dict, Any

class SafetyValidator:
    """
    Validates generated LLM responses for hallucinations and policy violations.
    """
    
    BANNED_TERMS = ["refund", "unban", "guarantee"]
    URL_PATTERN = re.compile(r'(https?://[^\s]+|support\.activision\.com[^\s]*)', re.IGNORECASE)
    
    @classmethod
    def validate(cls, generated_text: str, evidence: List[Dict[str, Any]]) -> bool:
        """
        Returns True if safe, False if unsafe (hallucination/banned term detected).
        """
        
        # 1. Banned Term Check
        lower_text = generated_text.lower()
        for term in cls.BANNED_TERMS:
            if term in lower_text:
                return False
                
        # 2. Evidence-Conditional URL Filter
        generated_urls = cls.URL_PATTERN.findall(generated_text)
        if not generated_urls:
            return True
            
        evidence_text = " ".join([ev.get("historical_brand_response", "") for ev in evidence])
        
        for url in generated_urls:
            # Clean punctuation from end of URL (e.g. if it matched a period or parenthesis)
            clean_url = url.strip(".,)'\"")
            if clean_url not in evidence_text:
                return False
                
        return True
