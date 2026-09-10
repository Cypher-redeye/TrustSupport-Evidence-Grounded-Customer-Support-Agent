from typing import Dict, Any
import os
from src.intents.classifier import IntentClassifier
from src.retrieval.retriever import EvidenceRetriever
from src.generation.reply_router import ReplyRouter
from src.generation.template_generator import TemplateGenerator
from src.generation.mock_generator import MockGenerator
from src.generation.api_generator import APIGenerator
from src.generation.safety import SafetyValidator

class SupportAgent:
    """
    Evidence-Grounded Customer Support Agent.
    Orchestrates the classification, retrieval, routing, and generation pipelines.
    """
    def __init__(self, use_mock_generator: bool = False):
        self.classifier = IntentClassifier()
        self.retriever = EvidenceRetriever()
        self.template_generator = TemplateGenerator()
        
        if use_mock_generator:
            self.primary_generator = MockGenerator()
        else:
            self.primary_generator = APIGenerator()

    def respond(self, query: str) -> Dict[str, Any]:
        """
        Processes a user query and returns a structured response payload.
        """
        # 1. Classification & Risk Detection
        class_res = self.classifier.predict(query)
        intent = class_res["intent"]
        confidence = class_res["confidence_level"]
        risk_flags = class_res["risk_flags"] # List of dictionaries
        
        flag_names = [f["risk_flag"] for f in risk_flags] if risk_flags and isinstance(risk_flags[0], dict) else risk_flags
        
        # 2. Evidence Retrieval
        retrieval_res = self.retriever.retrieve(query)
        retrieval_status = retrieval_res["status"]
        evidence = retrieval_res.get("evidence", [])
        
        max_sim = 0.0
        if evidence:
            max_sim = max([ev.get("adjusted_score", 0.0) for ev in evidence])
            
        # 3. Routing
        reply_mode = ReplyRouter.determine_mode(
            intent=intent,
            confidence_level=confidence,
            risk_flags=flag_names,
            retrieval_status=retrieval_status,
            max_similarity=max_sim
        )
        
        should_escalate = (reply_mode == "ESCALATE")
        
        # 4. Generation
        generation_source = "API" if isinstance(self.primary_generator, APIGenerator) else "MOCK"
        generation_model = os.environ.get("GENERATION_MODEL", "gemini-2.5-flash") if generation_source == "API" else None
        fallback_used = False
        safety_passed = True
        
        reply_text = ""
        
        if reply_mode in ["ABSTAIN", "ESCALATE", "CLARIFY"]:
            # Bypass API generator for these safe modes
            reply_text = self.template_generator.generate(query, reply_mode, intent, flag_names, evidence)
            generation_source = "TEMPLATE"
            generation_model = None
        else:
            # Attempt API generation
            try:
                reply_text = self.primary_generator.generate(query, reply_mode, intent, flag_names, evidence)
                
                # 5. Safety Validation
                is_safe = SafetyValidator.validate(reply_text, evidence)
                
                if not is_safe:
                    reply_text = self.template_generator.generate(query, reply_mode, intent, flag_names, evidence)
                    generation_source = "TEMPLATE"
                    generation_model = None
                    fallback_used = True
                    safety_passed = False
                    
            except Exception as e:
                reply_text = self.template_generator.generate(query, reply_mode, intent, flag_names, evidence)
                generation_source = "TEMPLATE"
                generation_model = None
                fallback_used = True
                
        # 6. Build Provenance Payload
        evidence_ids = [ev.get("evidence_id") for ev in evidence]
        evidence_details = [
            {
                "evidence_id": ev.get("evidence_id"),
                "similarity": ev.get("adjusted_score", 0.0),
                "response": ev.get("first_brand_response", "")
            }
            for ev in evidence
        ]
        
        return {
            "reply_text": reply_text,
            "reply_mode": reply_mode,
            "intent": intent,
            "confidence": class_res["confidence_score"],
            "risk_flags": risk_flags, # Returns the rich list of dictionaries
            "should_escalate": should_escalate,
            "evidence_ids": evidence_ids,
            "evidence_details": evidence_details,
            "max_similarity": max_sim,
            "generation_source": generation_source,
            "generation_model": generation_model,
            "fallback_used": fallback_used,
            "safety_validation": {
                "passed": safety_passed,
                "flags": []
            }
        }
