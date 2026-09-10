import json
import logging
import re
from pathlib import Path
from src.config import settings
from collections import defaultdict

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def is_purchase_billing(text):
    text = text.lower()
    return bool(re.search(r'\b(charged twice|double charged|refund|payment failed|payment declined|money deducted|billing|charged for|transaction failed|bank|credit card|transaction)\b', text))

def is_progression_rewards(text):
    text = text.lower()
    return bool(re.search(r'\b(supply drop|supply drops|cod points|cp|token|tokens|contract|contracts|didn\'t receive|missing|didn\'t get|never got)\b', text))

def is_digital_access(text):
    text = text.lower()
    return bool(re.search(r'\b(download|pre-load|preload|install|installing|code|digital copy|redeem|dlc|season pass|can\'t access|won\'t start|store)\b', text))

def analyze_semantics():
    dataset_file = Path(settings.processed_data_dir) / "labeled_intent_dataset.jsonl"
    data = []
    with open(dataset_file, 'r', encoding='utf-8') as f:
        for line in f:
            data.append(json.loads(line))
            
    broad_regex = re.compile(r'\b(buy|bought|purchased|payment|charged|refund|money back|dollars|store)\b')
    
    matches = []
    for ex in data:
        if broad_regex.search(ex['text'].lower()):
            matches.append(ex)
            
    report = """# Purchase & Billing Semantic Review

## Semantic Precedence Rules Evaluated
1. **PURCHASE_AND_BILLING**: Strict monetary/transaction failure (`double charged`, `refund`, `payment failed`, `bank`).
2. **PROGRESSION_AND_REWARDS**: Missing virtual content after a purchase (`cod points`, `supply drops`, `didn't receive`).
3. **DIGITAL_ACCESS_AND_DOWNLOAD**: Access, code redemption, installation (`download`, `code`, `season pass`).

## 50 Example Categorizations
"""
    count = 0
    for ex in matches:
        if count >= 50: break
        
        text = ex['text']
        prev_intent = ex['intent']
        
        if is_purchase_billing(text):
            proposed = "PURCHASE_AND_BILLING"
            rule = "is_purchase_billing"
            reason = "Matches strict monetary failure/charge keywords"
        elif is_progression_rewards(text):
            proposed = "PROGRESSION_AND_REWARDS"
            rule = "is_progression_rewards"
            reason = "Mentions missing virtual items (e.g. cod points/supply drops)"
        elif is_digital_access(text):
            proposed = "DIGITAL_ACCESS_AND_DOWNLOAD"
            rule = "is_digital_access"
            reason = "Mentions downloading, installing, or codes"
        else:
            # Fallback to whatever its original K-means mapped it to, except if it just says "bought", it's probably general feedback or something else
            proposed = prev_intent
            rule = "fallback_to_cluster"
            reason = "Broad match ('buy'/'bought') but no specific access, reward, or billing issue specified."
            
        report += f"### Example {count+1}\n"
        report += f"- **Text:** {text}\n"
        report += f"- **Previous Intent:** {prev_intent}\n"
        report += f"- **Proposed Intent:** {proposed}\n"
        report += f"- **Reason:** {reason}\n"
        report += f"- **Assignment Rule:** {rule}\n\n"
        
        count += 1
        
    out_file = Path("reports/purchase_billing_semantic_review.md")
    with open(out_file, 'w', encoding='utf-8') as f:
        f.write(report)
        
    logger.info("Semantic review completed.")

if __name__ == "__main__":
    analyze_semantics()
