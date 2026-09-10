import json
from pathlib import Path
from collections import defaultdict
import re

def clean_text(text):
    text = re.sub(r'https://t\.co/\w+', '', text)
    text = text.replace('\n', ' ').strip()
    return text

def main():
    data_dir = Path("data/processed")
    reports_dir = Path("reports")
    reports_dir.mkdir(exist_ok=True)
    
    # 1. Load full conversations
    print("Loading conversations...")
    convs = {}
    with open(data_dir / "atviassist_conversations.jsonl", "r", encoding="utf-8") as f:
        for line in f:
            c = json.loads(line)
            convs[c["conversation_id"]] = c
            
    # 2. Load intent_train.jsonl and extract brand responses
    print("Extracting brand responses...")
    evidence_dataset = []
    
    metrics = {
        "total_train_samples": 0,
        "with_brand_response": 0,
        "missing_brand_response": 0,
        "total_unique_blocks": 0
    }
    
    # Track exact response blocks to measure duplication
    unique_blocks = set()
    
    with open(data_dir / "intent_train.jsonl", "r", encoding="utf-8") as f:
        for line in f:
            req = json.loads(line)
            metrics["total_train_samples"] += 1
            
            conv_id = req["conversation_id"]
            if conv_id not in convs:
                metrics["missing_brand_response"] += 1
                continue
                
            conv = convs[conv_id]
            tweets = conv.get("turns", [])
            
            # Find the brand response block
            brand_block = []
            found_brand = False
            for t in tweets:
                if t["author_id"] == "ATVIAssist":
                    found_brand = True
                    brand_block.append(t["text"])
                elif found_brand:
                    # Once we hit a customer message again, the first brand block is over
                    if t["author_id"] != "ATVIAssist":
                        break
                        
            if not brand_block:
                metrics["missing_brand_response"] += 1
                continue
                
            metrics["with_brand_response"] += 1
            
            first_brand_response = brand_block[0]
            historical_response_block = " ".join(brand_block)
            historical_response_block = clean_text(historical_response_block)
            unique_blocks.add(historical_response_block)
            
            # Evidence schema
            evidence_item = {
                "evidence_id": req["request_id"],
                "conversation_id": conv_id,
                "customer_text": req["text"],
                "historical_brand_response": historical_response_block,
                "first_brand_response": first_brand_response,
                "intent": req["intent"],
                "risk_flags": req["risk_flags"]
            }
            evidence_dataset.append(evidence_item)
            
    metrics["total_unique_blocks"] = len(unique_blocks)
            
    # 3. Save Evidence Dataset
    print(f"Saving {len(evidence_dataset)} evidence items to intent_evidence.jsonl")
    with open(data_dir / "intent_evidence.jsonl", "w", encoding="utf-8") as f:
        for item in evidence_dataset:
            f.write(json.dumps(item) + "\n")
            
    # 4. Generate Report
    report = [
        "# Phase 6: Evidence Dataset Audit",
        "",
        "## Extraction Metrics",
        f"- **Total Train Samples:** {metrics['total_train_samples']}",
        f"- **Valid Pairs (with ATVIAssist response):** {metrics['with_brand_response']}",
        f"- **Missing Brand Response (dropped):** {metrics['missing_brand_response']}",
        f"- **Total Unique Brand Response Blocks:** {metrics['total_unique_blocks']}",
        "",
        "## Summary",
        "Only customer requests that received a documented reply from `ATVIAssist` are included in the retrieval index.",
        "Consecutive brand tweets were merged into a `historical_response_block` to preserve multi-tweet answers.",
        "A large discrepancy between 'Valid Pairs' and 'Total Unique Brand Response Blocks' highlights the prevalence of canned/templated responses in historical support, underscoring the need for deductive diversity filtering during Top-K retrieval."
    ]
    
    with open(reports_dir / "phase6_evidence_audit.md", "w", encoding="utf-8") as f:
        f.write("\n".join(report))
        
    print("Done. Generated reports/phase6_evidence_audit.md")

if __name__ == "__main__":
    main()
