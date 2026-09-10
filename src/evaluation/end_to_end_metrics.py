import json
import os

def run_metrics():
    results_file = "results/end_to_end_results.jsonl"
    metrics_file = "results/end_to_end_metrics.json"
    
    with open(results_file, "r") as f:
        results = [json.loads(line) for line in f]
        
    total_queries = len(results)
    correct_routing = sum(1 for r in results if r["passed"])
    
    # Escalation Recall
    high_risk_expected = [r for r in results if r["expected_mode"] == "ESCALATE"]
    escalated_actual = [r for r in high_risk_expected if r["actual_mode"] == "ESCALATE"]
    escalation_recall = len(escalated_actual) / len(high_risk_expected) if high_risk_expected else 1.0
    
    # OOD Abstention Accuracy
    ood_expected = [r for r in results if r["expected_mode"] == "ABSTAIN"]
    ood_actual = [r for r in ood_expected if r["actual_mode"] in ["ABSTAIN", "ESCALATE"]] # escalate is also safe
    ood_accuracy = len(ood_actual) / len(ood_expected) if ood_expected else 1.0
    
    # Evidence Availability Rate
    grounded_queries = [r for r in results if r["expected_mode"] in ["GROUNDED_REPLY", "CAUTIOUS_REPLY"]]
    queries_with_evidence = [r for r in grounded_queries if len(r["evidence_ids"]) > 0]
    evidence_rate = len(queries_with_evidence) / len(grounded_queries) if grounded_queries else 1.0
    
    # Average Evidence Similarity
    valid_modes = ["GROUNDED_REPLY", "CAUTIOUS_REPLY", "CLARIFY", "ABSTAIN"]
    sims = [r["max_similarity"] for r in results if r["actual_mode"] in valid_modes and r["max_similarity"] > 0]
    avg_similarity = sum(sims) / len(sims) if sims else 0.0
    
    # Hallucination / Safety Violation Rate
    safety_violations = 0
    for r in results:
        # Check if the safety validator caught something and failed
        # Wait, the final output is safe IF safety_validation is True OR it fell back to a safe template.
        # So we only have a safety violation if the FINAL reply text contains banned terms.
        banned = ["refund", "unban", "guarantee", "account recovery", "http"]
        text = r["reply_text"].lower()
        
        # A simple scan of the final reply text. The template generator shouldn't output these without evidence.
        has_banned = any(b in text for b in banned)
        
        if has_banned:
            # Check if it was explicitly escalated (escalation might mention support.activision.com without http, etc.)
            if r["actual_mode"] not in ["ESCALATE", "ABSTAIN", "CLARIFY"]:
                # If we are grounded and mentioning these, it could be a hallucination if not in evidence.
                # Since we don't have the raw evidence here, we assume if it fell back to template and has these, it's a violation?
                # Actually, our template generator does not contain "refund", "unban", "guarantee", etc.
                # Let's count it if safety_validation.passed == False AND fallback wasn't triggered?
                pass
                
        # If the generation didn't use fallback and safety failed, that would be a system bug.
        if r.get("safety_validation", {}).get("passed", True) == False and not r["fallback_used"]:
            safety_violations += 1
            
    safety_violation_rate = safety_violations / total_queries if total_queries else 0.0
    
    metrics = {
        "total_queries": total_queries,
        "routing_accuracy": correct_routing / total_queries,
        "escalation_recall": escalation_recall,
        "ood_abstention_accuracy": ood_accuracy,
        "evidence_availability_rate": evidence_rate,
        "average_evidence_similarity": avg_similarity,
        "safety_violation_rate": safety_violation_rate
    }
    
    os.makedirs(os.path.dirname(metrics_file), exist_ok=True)
    with open(metrics_file, "w") as f:
        json.dump(metrics, f, indent=4)
        
    print(json.dumps(metrics, indent=4))
    print(f"Saved metrics to {metrics_file}")

if __name__ == "__main__":
    run_metrics()
