import json
import os
import re

def run_groundedness():
    results_file = "results/end_to_end_results.jsonl"
    metadata_file = "models/evidence_metadata.json"
    report_file = "reports/phase8_groundedness_report.md"
    
    with open(results_file, "r") as f:
        results = [json.loads(line) for line in f]
        
    with open(metadata_file, "r") as f:
        metadata = json.load(f)
        
    # Map for easy lookup
    metadata_map = {item["evidence_id"]: item for item in metadata}
    
    grounded_queries = [r for r in results if r["actual_mode"] == "GROUNDED_REPLY"]
    
    report_lines = [
        "# Phase 8 Groundedness Report\n",
        f"Total Grounded Replies Evaluated: {len(grounded_queries)}\n"
    ]
    
    fails = {
        "check1": 0,
        "check2": 0,
        "check3": 0,
        "check4": 0,
        "check5": 0
    }
    
    url_pattern = re.compile(r'(https?://[^\s]+|support\.activision\.com[^\s]*)', re.IGNORECASE)
    unsupported_guarantees = ["i guarantee", "you will receive", "we will refund", "we will unban", "your account will be restored"]
    
    for r in grounded_queries:
        ev_ids = r["evidence_ids"]
        reply = r["reply_text"].lower()
        
        # Check 1: Evidence exists
        if len(ev_ids) == 0:
            fails["check1"] += 1
            
        # Check 2: Similarity threshold
        if r["max_similarity"] < 0.50:
            fails["check2"] += 1
            
        # Check 5: Provenance Integrity (Checking it before check 3)
        valid_ev_ids = True
        for eid in ev_ids:
            if eid not in metadata_map:
                valid_ev_ids = False
                fails["check5"] += 1
                break
                
        # Check 3: Unsupported URLs
        generated_urls = url_pattern.findall(r["reply_text"])
        if generated_urls and valid_ev_ids:
            evidence_texts = [metadata_map[eid].get("historical_brand_response", "").lower() for eid in ev_ids]
            combined_ev = " ".join(evidence_texts)
            
            for url in generated_urls:
                clean_url = url.strip(".,)'\"").lower()
                if clean_url not in combined_ev:
                    fails["check3"] += 1
                    break
                    
        # Check 4: Unsupported Guarantees
        if any(g in reply for g in unsupported_guarantees):
            # This is strict flag
            fails["check4"] += 1
            
    report_lines.append("## Verification Results\n")
    report_lines.append(f"- **Check 1 (Evidence Exists):** {len(grounded_queries) - fails['check1']} passed, {fails['check1']} failed.")
    report_lines.append(f"- **Check 2 (Similarity >= 0.50):** {len(grounded_queries) - fails['check2']} passed, {fails['check2']} failed.")
    report_lines.append(f"- **Check 3 (Unsupported URLs):** {len(grounded_queries) - fails['check3']} passed, {fails['check3']} failed.")
    report_lines.append(f"- **Check 4 (Unsupported Guarantees):** {len(grounded_queries) - fails['check4']} passed, {fails['check4']} failed.")
    report_lines.append(f"- **Check 5 (Provenance Integrity):** {len(grounded_queries) - fails['check5']} passed, {fails['check5']} failed.")
    
    os.makedirs(os.path.dirname(report_file), exist_ok=True)
    with open(report_file, "w") as f:
        f.write("\n".join(report_lines))
        
    print(f"Groundedness report generated at {report_file}")

if __name__ == "__main__":
    run_groundedness()
