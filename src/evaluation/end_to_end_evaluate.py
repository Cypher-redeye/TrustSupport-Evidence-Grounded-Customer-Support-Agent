import json
import os
from tqdm import tqdm
from src.agent.support_agent import SupportAgent

def run_evaluation():
    input_file = "data/golden/end_to_end_evaluation.jsonl"
    output_file = "results/end_to_end_results.jsonl"
    
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    with open(input_file, "r") as f:
        queries = [json.loads(line) for line in f]
        
    print(f"Loaded {len(queries)} evaluation queries.")
    print("Initializing SupportAgent...")
    
    agent = SupportAgent(use_mock_generator=False)
    results = []
    
    for i, item in enumerate(tqdm(queries, desc="Evaluating")):
        q = item["query"]
        expected_mode = item["expected_mode"]
        expected_intent = item["expected_intent"]
        
        try:
            res = agent.respond(q)
            
            # Determine if passed
            # We are flexible if expecting GROUNDED and got CAUTIOUS (or vice versa for Ambiguous/Retrieval stress tests)
            actual_mode = res["reply_mode"]
            
            passed = False
            if actual_mode == expected_mode:
                passed = True
            elif expected_mode == "GROUNDED_REPLY" and actual_mode in ["CAUTIOUS_REPLY", "CLARIFY"]:
                # Normal queries could hit clarify if confidence is low
                passed = True
            elif expected_mode == "CAUTIOUS_REPLY" and actual_mode in ["GROUNDED_REPLY", "CLARIFY", "ABSTAIN"]:
                passed = True
            elif expected_mode == "CLARIFY" and actual_mode in ["CAUTIOUS_REPLY", "ABSTAIN"]:
                passed = True
            elif expected_mode == "ESCALATE" and actual_mode == "ESCALATE":
                passed = True
            elif expected_mode == "ABSTAIN" and actual_mode in ["ABSTAIN", "ESCALATE"]:
                passed = True
            
            record = {
                "query": q,
                "expected_intent": expected_intent,
                "expected_mode": expected_mode,
                "actual_mode": actual_mode,
                "intent": res["intent"],
                "confidence": res["confidence"],
                "risk_flags": res["risk_flags"],
                "should_escalate": res["should_escalate"],
                "max_similarity": res["max_similarity"],
                "evidence_ids": res["evidence_ids"],
                "reply_text": res["reply_text"],
                "generation_source": res["generation_source"],
                "passed": passed
            }
            results.append(record)
            
        except Exception as e:
            record = {
                "query": q,
                "expected_intent": expected_intent,
                "expected_mode": expected_mode,
                "actual_mode": "ERROR",
                "intent": "ERROR",
                "confidence": 0.0,
                "risk_flags": [],
                "should_escalate": False,
                "max_similarity": 0.0,
                "evidence_ids": [],
                "reply_text": str(e),
                "generation_source": "ERROR",
                "passed": False
            }
            results.append(record)
            
    with open(output_file, "w") as f:
        for r in results:
            f.write(json.dumps(r) + "\n")
            
    print(f"Saved {len(results)} results to {output_file}")

if __name__ == "__main__":
    run_evaluation()
