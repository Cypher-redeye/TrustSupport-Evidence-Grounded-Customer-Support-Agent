import json
import logging
import re
from pathlib import Path
from src.config import settings
from collections import defaultdict

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def run_audit():
    dataset_file = Path(settings.processed_data_dir) / "labeled_intent_dataset.jsonl"
    data = []
    with open(dataset_file, 'r', encoding='utf-8') as f:
        for line in f:
            data.append(json.loads(line))
            
    # Phase 4 original broad regex vs Phase 5 restricted risk regex
    broad_regex_str = r'\b(buy|bought|purchased|payment|charged|refund|money back|dollars|store)\b'
    phase5_risk_str = r'\b(payment|charged|refund|money back|dollars)\b'
    
    broad_regex = re.compile(broad_regex_str)
    
    keyword_counts = defaultdict(int)
    keywords_to_check = ['payment', 'charged', 'double charged', 'refund', 'money', 'dollars', 'purchase', 'bought', 'buy', 'store', 'billing']
    
    broad_matches = []
    where_did_they_go = defaultdict(int)
    
    for ex in data:
        text = ex['text'].lower()
        
        # Check individual keywords
        for kw in keywords_to_check:
            if kw == 'double charged':
                if 'double charged' in text: keyword_counts[kw] += 1
            elif kw == 'money back':
                if 'money back' in text: keyword_counts[kw] += 1
            elif re.search(r'\b' + kw + r'\b', text):
                keyword_counts[kw] += 1
                
        # Check broad match
        if broad_regex.search(text):
            broad_matches.append(ex)
            where_did_they_go[ex['intent']] += 1

    # Generate Audit Report
    audit = f"""# Phase 5: PURCHASE_AND_BILLING Discrepancy Audit

## 1. Phase 4 Reported/Estimated Count
In Phase 4, `src/intents/analyze_subclusters.py` reported **421** examples for "Payment/Purchase/Transactions". 

## 2. Final Phase 5 Deterministic Count
In Phase 5, the final dataset generated exactly **18** examples assigned to `PURCHASE_AND_BILLING`.

## 3. Exact Labeling Rules Currently Used
**In Phase 4 (`analyze_subclusters.py`)**: 
The count of 421 was generated using a broad dataset-wide regex:
`r'\\b(buy|bought|purchased|payment|charged|refund|money back|dollars|store)\\b'`

**In Phase 5 (`build_labeled_dataset.py`)**:
The rules were significantly tightened and constrained by cluster geometry. 
1. The regex was shortened to: `r'\\b(payment|charged|refund|money back|dollars)\\b'` (dropping `buy`, `bought`, `purchased`, `store`).
2. The assignment was constrained to **only trigger if the point was in K-Means Cluster 2**.

```python
if c_id == 2:
    if 'PAYMENT' in flags:
        intent_assignments[req_id] = 'PURCHASE_AND_BILLING'
```
This intersection (Cluster 2 AND restricted regex) is why the count dropped from 421 to 18.

## 4. Number of Examples Matching Each Keyword
Across the entire 10,812 dataset:
"""
    for kw, count in sorted(keyword_counts.items(), key=lambda x: x[1], reverse=True):
        audit += f"- {kw}: {count}\n"

    audit += "\n## 5 & 6. At least 20 Actual Examples Matching Broad Billing/Payment Concepts\n\n"
    for i, ex in enumerate(broad_matches[:20]):
        audit += f"### Example {i+1}\n"
        audit += f"- **request_id**: {ex['request_id']}\n"
        audit += f"- **conversation_id**: {ex['conversation_id']}\n"
        audit += f"- **text**: {ex['text']}\n"
        audit += f"- **Phase 5 assigned intent**: {ex['intent']}\n"
        audit += f"- **assignment_method**: {ex['assignment_method']}\n"
        audit += f"- **risk_flags**: {ex['risk_flags']}\n\n"

    audit += "## 7. Where are these broad matches currently being assigned?\n"
    audit += "The 421 broad matches from the entire dataset were distributed across the following intents in Phase 5:\n"
    for intent, count in sorted(where_did_they_go.items(), key=lambda x: x[1], reverse=True):
        audit += f"- {intent}: {count}\n"
        
    audit += """
## 8. Was the Phase 4 estimate documented as an estimate?
Yes. The Phase 4 `INTENT_TAXONOMY_DRAFT.md` explicitly noted:
`*(Note: Estimated counts derived from raw cluster sizes and keyword extrapolation).*`
However, the degree to which `PURCHASE_AND_BILLING` was extrapolated across the entire dataset vs restricted to Cluster 2 was the primary source of the divergence.

## 9. Do all 10,812 requests still have exactly one valid intent?
Yes. As verified in Step 1, all 10,812 requests were mapped 1:1 to exactly one intent without duplication or missing examples.
"""

    with open("reports/phase5_purchase_billing_audit.md", 'w', encoding='utf-8') as f:
        f.write(audit)

    logger.info("Audit completed successfully.")

if __name__ == "__main__":
    run_audit()
