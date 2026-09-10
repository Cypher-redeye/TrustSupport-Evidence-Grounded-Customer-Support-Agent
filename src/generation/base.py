from abc import ABC, abstractmethod
from typing import List, Dict, Any

class BaseGenerator(ABC):
    """
    Abstract base class for all reply generators.
    """
    @abstractmethod
    def generate(self, query: str, reply_mode: str, intent: str, risk_flags: List[str], evidence: List[Dict[str, Any]]) -> str:
        pass
