import json
import random
from pathlib import Path
from src.retrieval.retriever import EvidenceRetriever

def main():
    data_dir = Path("data/processed")
    reports_dir = Path("reports")
    reports_dir.mkdir(exist_ok=True)
    
    print("Initializing Retriever...")
    retriever = EvidenceRetriever()
    
    test_data = []
    with open(data_dir / "intent_test.jsonl", "r", encoding="utf-8") as f:
        for line in f:
            test_data.append(json.loads(line))
            
    print(f"Loaded {len(test_data)} test items.")
    
    metrics = {
        "total": len(test_data),
        "abstentions": 0,
        "abstention_ood": 0,
        "abstention_low_sim": 0,
        "abstention_risk": 0,
        "recall_at_1": 0,
        "recall_at_3": 0,
        "recall_at_5": 0,
        "risk_total": 0,
        "risk_recall_1": 0,
        "risk_recall_3": 0,
        "risk_recall_5": 0,
        "duplicate_count": 0,
        "sum_similarity": 0.0,
        "retrieved_count": 0,
        "classification_errors": 0,
        "retrieval_errors": 0
    }
    
    errors = []
    golden_samples = []
    
    # We want 50 random samples for golden review
    random.seed(42)
    golden_indices = set(random.sample(range(len(test_data)), 50))
    
    for i, item in enumerate(test_data):
        if i % 200 == 0:
            print(f"Evaluating {i}/{len(test_data)}...")
            
        true_intent = item["intent"]
        res = retriever.retrieve(item["text"], top_k=5, k_retrieve=20)
        
        # Golden review collection
        if i in golden_indices:
            golden_samples.append((item, res))
            
        if res["status"] != "SUCCESS":
            metrics["abstentions"] += 1
            if res["reason"] == "OOD_QUERY":
                metrics["abstention_ood"] += 1
                errors.append({"item": item, "reason": "OOD_ABSTENTION"})
            elif res["reason"] == "LOW_SIMILARITY":
                metrics["abstention_low_sim"] += 1
                errors.append({"item": item, "reason": "LOW_SIMILARITY_ABSTENTION"})
            else:
                metrics["abstention_risk"] += 1
                errors.append({"item": item, "reason": "RISK_CONTRADICTION_ABSTENTION"})
            continue
            
        # Retrieval successful
        metrics["retrieved_count"] += 1
        evidence = res["evidence"]
        
        # Zero Leakage Verification
        for ev in evidence:
            assert ev["conversation_id"] != item["conversation_id"], f"LEAKAGE DETECTED: Conv {item['conversation_id']}"
            
        # Metric: Mean Similarity
        avg_sim = sum(ev["raw_sim"] for ev in evidence) / len(evidence)
        metrics["sum_similarity"] += avg_sim
        
        # Metric: Recall
        intents_in_top_5 = [ev["intent"] for ev in evidence]
        
        r1 = true_intent == intents_in_top_5[0] if len(intents_in_top_5) >= 1 else False
        r3 = true_intent in intents_in_top_5[:3]
        r5 = true_intent in intents_in_top_5
        
        if r1: metrics["recall_at_1"] += 1
        if r3: metrics["recall_at_3"] += 1
        if r5: metrics["recall_at_5"] += 1
        
        # Risk Recall (does top K contain ANY of the true risk flags, if true risk flags exist?)
        true_risk = set(item.get("risk_flags", []))
        if true_risk:
            metrics["risk_total"] += 1
            risk_in_top_5 = [set(ev.get("risk_flags", [])) for ev in evidence]
            
            rr1 = len(true_risk.intersection(risk_in_top_5[0])) > 0 if len(risk_in_top_5) >= 1 else False
            rr3 = any(len(true_risk.intersection(r)) > 0 for r in risk_in_top_5[:3])
            rr5 = any(len(true_risk.intersection(r)) > 0 for r in risk_in_top_5)
            
            if rr1: metrics["risk_recall_1"] += 1
            if rr3: metrics["risk_recall_3"] += 1
            if rr5: metrics["risk_recall_5"] += 1
            
        # Duplicate Tracking
        brand_responses = [ev["historical_brand_response"] for ev in evidence]
        if len(brand_responses) > len(set(brand_responses)):
            metrics["duplicate_count"] += 1
        
        # Error tracking (Failed to find true intent in Top-3)
        if not r3:
            if res["predicted_intent"] != true_intent:
                metrics["classification_errors"] += 1
                errors.append({"item": item, "reason": "CLASSIFICATION_ERROR", "predicted": res["predicted_intent"]})
            else:
                metrics["retrieval_errors"] += 1
                errors.append({"item": item, "reason": "RETRIEVAL_ERROR", "predicted": res["predicted_intent"]})
                
    # Calculate percentages
    evaluated = metrics["retrieved_count"]
    r1_pct = metrics["recall_at_1"] / evaluated if evaluated > 0 else 0
    r3_pct = metrics["recall_at_3"] / evaluated if evaluated > 0 else 0
    r5_pct = metrics["recall_at_5"] / evaluated if evaluated > 0 else 0
    
    rr_total = metrics["risk_total"]
    rr1_pct = metrics["risk_recall_1"] / rr_total if rr_total > 0 else 0
    rr3_pct = metrics["risk_recall_3"] / rr_total if rr_total > 0 else 0
    rr5_pct = metrics["risk_recall_5"] / rr_total if rr_total > 0 else 0
    
    dup_rate = metrics["duplicate_count"] / evaluated if evaluated > 0 else 0
    mean_sim = metrics["sum_similarity"] / evaluated if evaluated > 0 else 0
    abs_rate = metrics["abstentions"] / metrics["total"]
    
    # 1. Generate Error Analysis Report
    err_report = [
        "# Phase 6: Retrieval Error Analysis",
        f"\n**Total Queries:** {metrics['total']}",
        f"**Abstentions:** {metrics['abstentions']} ({abs_rate:.1%})",
        f"  - OOD: {metrics['abstention_ood']}",
        f"  - Low Similarity: {metrics['abstention_low_sim']}",
        f"  - Risk Contradiction: {metrics['abstention_risk']}",
        f"**Duplicate Rate:** {dup_rate:.1%}",
        f"**Mean Similarity:** {mean_sim:.3f}",
        "\n## Intent Recall",
        f"- **Recall@1:** {r1_pct:.1%}",
        f"- **Recall@3:** {r3_pct:.1%}",
        f"- **Recall@5:** {r5_pct:.1%}",
        "\n## Risk Recall (Out of {} queries with risk flags)".format(rr_total),
        f"- **Risk Recall@1:** {rr1_pct:.1%}",
        f"- **Risk Recall@3:** {rr3_pct:.1%}",
        f"- **Risk Recall@5:** {rr5_pct:.1%}",
        "\n## Failure Modes (Top-3 Misses)",
        f"- **Classification Errors:** {metrics['classification_errors']} (Retriever misled by wrong semantic prediction)",
        f"- **Retrieval Errors:** {metrics['retrieval_errors']} (Classifier was correct, but true intent wasn't in Top-3)"
    ]
    with open(reports_dir / "phase6_retrieval_error_analysis.md", "w", encoding="utf-8") as f:
        f.write("\n".join(err_report))
        
    # 2. Generate Golden Review
    golden_doc = ["# Phase 6: Golden Retrieval Review\n\n50 Random test queries manually reviewed for evidence grounding.\n"]
    for i, (item, res) in enumerate(golden_samples):
        golden_doc.append(f"### Query {i+1}")
        golden_doc.append(f"**Customer:** {item['text']}")
        golden_doc.append(f"**True Intent:** `{item['intent']}`")
        golden_doc.append(f"**Status:** `{res['status']}`")
        if res['status'] == "SUCCESS":
            golden_doc.append(f"**Predicted Intent:** `{res['predicted_intent']}`\n")
            golden_doc.append("**Top Evidence:**")
            for j, ev in enumerate(res['evidence'][:3]):
                golden_doc.append(f"- **[Sim: {ev['raw_sim']:.2f} | Intent: {ev['intent']}]** {ev['historical_brand_response']}")
        else:
            golden_doc.append(f"**Reason:** `{res['reason']}`")
        golden_doc.append("\n---\n")
        
    with open(reports_dir / "phase6_golden_retrieval_review.md", "w", encoding="utf-8") as f:
        f.write("\n".join(golden_doc))
        
    print(f"Done! Recall@3 = {r3_pct:.1%}")

if __name__ == "__main__":
    main()
