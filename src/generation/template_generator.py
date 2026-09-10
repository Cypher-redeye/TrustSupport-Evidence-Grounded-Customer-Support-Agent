from typing import List, Dict, Any
from src.generation.base import BaseGenerator

class TemplateGenerator(BaseGenerator):
    """
    Deterministic template fallback generator.
    Produces safe responses directly from evidence without external API dependencies.
    """
    
    def generate(self, query: str, reply_mode: str, intent: str, risk_flags: List[str], evidence: List[Dict[str, Any]]) -> str:
        if reply_mode == "ABSTAIN":
            return "I don't have enough specific information to solve this right now. Please reach out to our team at support.activision.com for further assistance."
            
        if reply_mode == "ESCALATE":
            if "BAN_APPEAL" in risk_flags or "GAME_INTEGRITY" in risk_flags:
                return "We cannot discuss enforcement actions on social media. Please refer to the Security and Enforcement Policy page."
            return "Please submit a support ticket via the official portal for further assistance with this issue."
            
        if reply_mode == "CLARIFY":
            return "Could you provide more specific details about the issue you are experiencing?"
            
        if "GAME_INTEGRITY" in risk_flags:
            return "Thank you for the report. To maintain game integrity, please use the in-game reporting tools or visit our Security and Enforcement page to submit a formal report."
            
        # For GROUNDED_REPLY and CAUTIOUS_REPLY
        ev_text = ""
        if evidence and len(evidence) > 0:
            ev_text = evidence[0].get("historical_brand_response", "")
            
        prefix = f"I understand you're experiencing an issue related to {intent.replace('_', ' ').title()}. "
        if reply_mode == "CAUTIOUS_REPLY":
            prefix = f"It sounds like you might be experiencing an issue with {intent.replace('_', ' ').title()}. "
            
        body = f"Based on similar support cases, you can try the following:\n\n{ev_text}\n\nIf the issue continues, please contact support."
        
        return prefix + body
