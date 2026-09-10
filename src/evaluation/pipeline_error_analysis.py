import json
import os
from collections import defaultdict

def run_error_analysis():
    results_file = "results/end_to_end_results.jsonl"
    report_file = "reports/phase8_pipeline_error_analysis.md"
    
    with open(results_file, "r") as f:
        results = [json.loads(line) for line in f]
        
    failed = [r for r in results if not r["passed"]]
    
    errors = defaultdict(list)
    
    for r in failed:
        q = r["query"]
        expected = r["expected_mode"]
        actual = r["actual_mode"]
        
        # Determine error source
        if r["expected_intent"] != "UNKNOWN" and r["intent"] != r["expected_intent"]:
            errors["Intent Classification"].append(r)
            
        elif expected == "GROUNDED_REPLY" and actual == "ABSTAIN":
            errors["Evidence Retrieval (Miss)"].append(r)
            
        elif expected == "ABSTAIN" and actual != "ABSTAIN":
            errors["OOD Handling (False Positive)"].append(r)
            
        elif expected == "ESCALATE" and actual != "ESCALATE":
            errors["Risk Detection (False Negative)"].append(r)
            
        elif expected == "CAUTIOUS_REPLY" and actual == "GROUNDED_REPLY":
             errors["Routing (Insufficient Caution)"].append(r)
             
        else:
            errors["Other Routing/Pipeline"].append(r)
            
    report_lines = [
        "# Phase 8 Pipeline Error Analysis\n",
        f"**Total Queries Evaluated:** {len(results)}\n",
        f"**Total Failed Queries:** {len(failed)}\n\n"
    ]
    
    for cat, items in errors.items():
        if not items:
            continue
        report_lines.append(f"## {cat} ({len(items)})\n")
        for item in items:
            report_lines.append(f"- **Query:** {item['query']}")
            report_lines.append(f"  - Expected Mode: {item['expected_mode']}")
            report_lines.append(f"  - Actual Mode: {item['actual_mode']}")
            report_lines.append(f"  - Intent: {item['intent']} (Expected: {item['expected_intent']})")
            report_lines.append(f"  - Max Sim: {item['max_similarity']:.2f}\n")
            
    os.makedirs(os.path.dirname(report_file), exist_ok=True)
    with open(report_file, "w") as f:
        f.write("\n".join(report_lines))
        
    print(f"Error analysis report generated at {report_file}")

if __name__ == "__main__":
    run_error_analysis()
