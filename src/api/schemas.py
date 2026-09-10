from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any

class ChatRequest(BaseModel):
    query: str = Field(..., description="The customer support query")

class EvidenceItem(BaseModel):
    evidence_id: str
    similarity: float
    response: str
    
class SafetyValidation(BaseModel):
    passed: bool
    flags: List[str] = []

class RiskFlag(BaseModel):
    risk_flag: str
    detection_method: str
    risk_score: float
    matched_anchor: Optional[str] = None

class ChatResponse(BaseModel):
    reply_text: str
    reply_mode: str
    intent: str
    confidence: float
    risk_flags: List[RiskFlag] = []
    should_escalate: bool
    evidence_ids: List[str] = []
    evidence_details: List[EvidenceItem] = []
    max_similarity: float
    generation_source: str
    generation_model: Optional[str] = None
    fallback_used: bool = False
    safety_validation: SafetyValidation
