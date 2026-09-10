from typing import List, Dict, Any
from src.generation.base import BaseGenerator

class MockGenerator(BaseGenerator):
    """
    Mock generator for unit testing and CI environments.
    """
    
    def generate(self, query: str, reply_mode: str, intent: str, risk_flags: List[str], evidence: List[Dict[str, Any]]) -> str:
        return "Mock generated response"
