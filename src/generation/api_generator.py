import os
import json
from typing import List, Dict, Any
from google import genai
from google.genai import types
from src.generation.base import BaseGenerator

class APIGenerator(BaseGenerator):
    """
    API generator using google-genai SDK for Gemini models.
    Falls back gracefully via exceptions caught by SupportAgent.
    """
    
    def __init__(self):
        # We will dynamically grab the key or let it fail if not provided
        self.api_key = os.environ.get("GEMINI_API_KEY")
        self.model_name = os.environ.get("GENERATION_MODEL", "gemini-2.5-flash")
        
        if self.api_key:
            self.client = genai.Client(api_key=self.api_key)
        else:
            self.client = None

    def generate(self, query: str, reply_mode: str, intent: str, risk_flags: List[str], evidence: List[Dict[str, Any]]) -> str:
        if not self.client:
            raise ValueError("GEMINI_API_KEY not configured. Falling back to template.")
            
        evidence_text = "\n\n".join([ev.get("historical_brand_response", "") for ev in evidence])
        
        prompt = f"""You are an evidence-grounded customer support assistant. Your task is to answer the customer using ONLY the provided historical support evidence.

RULES:
1. Do not invent troubleshooting steps.
2. Do not invent URLs.
3. Do not promise refunds.
4. Do not promise account recovery.
5. Do not promise unbans.
6. Do not claim an action has been completed.
7. Do not mention information absent from the evidence.
8. If the evidence is insufficient, say that you cannot confirm the solution.
9. Write clearly, concisely and empathetically.
10. Do not copy historical responses verbatim unless necessary.

CUSTOMER QUERY: {query}
PREDICTED INTENT: {intent}
RETRIEVED EVIDENCE: 
{evidence_text}

Generate a helpful support response."""

        # Use low temperature to strictly enforce grounding
        response = self.client.models.generate_content(
            model=self.model_name,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.2,
                top_p=0.95,
            ),
        )
        
        if not response.text:
            raise ValueError("Empty response from API.")
            
        return response.text.strip()
