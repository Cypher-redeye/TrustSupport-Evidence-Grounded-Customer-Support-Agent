import json
import logging
import random
from collections import defaultdict
from pathlib import Path
from src.config import settings

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def split_dataset():
    # 1. Load labeled dataset
    dataset_file = Path(settings.processed_data_dir) / "labeled_intent_dataset.jsonl"
    data = []
    with open(dataset_file, 'r', encoding='utf-8') as f:
        for line in f:
            data.append(json.loads(line))
            
    assert len(data) == 10812, "Input dataset must have exactly 10,812 examples."

    # 2. Group by conversation_id
    conv_groups = defaultdict(list)
    for ex in data:
        conv_groups[ex['conversation_id']].append(ex)
        
    logger.info(f"Grouped into {len(conv_groups)} unique conversations.")

    # 3. Determine 'primary intent' for each conversation for stratification purposes
    # Usually it's just the first request block's intent
    conv_intents = {}
    for cid, examples in conv_groups.items():
        intent_counts = defaultdict(int)
        for ex in examples:
            intent_counts[ex['intent']] += 1
        # Pick most frequent intent in this conversation as its primary label
        primary_intent = max(intent_counts, key=intent_counts.get)
        conv_intents[cid] = primary_intent

    # Group conversations by their primary intent
    intent_to_convs = defaultdict(list)
    for cid, intent in conv_intents.items():
        intent_to_convs[intent].append(cid)
        
    # Shuffle for determinism
    random.seed(settings.random_seed)
    for intent in intent_to_convs:
        random.shuffle(intent_to_convs[intent])

    # 4. Allocate to splits (70 / 15 / 15)
    train_convs = set()
    val_convs = set()
    test_convs = set()
    
    for intent, cids in intent_to_convs.items():
        n = len(cids)
        # Attempt proportional split
        n_val = int(0.15 * n)
        n_test = int(0.15 * n)
        
        # Ensure at least 1 in val and test if possible (especially for rare classes)
        if n >= 3:
            if n_val == 0: n_val = 1
            if n_test == 0: n_test = 1
            
        n_train = n - n_val - n_test
        
        train_convs.update(cids[:n_train])
        val_convs.update(cids[n_train : n_train + n_val])
        test_convs.update(cids[n_train + n_val : ])
        
    # Verify no conversation leakage
    assert train_convs.isdisjoint(val_convs), "Leakage between Train and Validation"
    assert train_convs.isdisjoint(test_convs), "Leakage between Train and Test"
    assert val_convs.isdisjoint(test_convs), "Leakage between Validation and Test"
    
    # 5. Build Final Splits
    train_data = []
    val_data = []
    test_data = []
    
    for ex in data:
        cid = ex['conversation_id']
        if cid in train_convs:
            train_data.append(ex)
        elif cid in val_convs:
            val_data.append(ex)
        elif cid in test_convs:
            test_data.append(ex)
        else:
            raise ValueError(f"Conversation {cid} not assigned to any split.")
            
    # Verify exact accounting
    assert len(train_data) + len(val_data) + len(test_data) == 10812, "Total split examples do not equal 10812."

    # 6. Save Splits
    def save_split(split_data, name):
        out_file = Path(settings.processed_data_dir) / f"intent_{name}.jsonl"
        with open(out_file, 'w', encoding='utf-8') as f:
            for ex in split_data:
                f.write(json.dumps(ex) + "\n")
                
    save_split(train_data, "train")
    save_split(val_data, "validation")
    save_split(test_data, "test")

    # 7. Generate Split Audit Report
    def get_stats(split_data):
        intent_counts = defaultdict(int)
        method_counts = defaultdict(int)
        risk_counts = 0
        cids = set()
        for ex in split_data:
            intent_counts[ex['intent']] += 1
            method_counts[ex['assignment_method']] += 1
            if ex['risk_flags']:
                risk_counts += 1
            cids.add(ex['conversation_id'])
        return len(split_data), len(cids), intent_counts, method_counts, risk_counts

    t_size, t_cids, t_intents, t_methods, t_risk = get_stats(train_data)
    v_size, v_cids, v_intents, v_methods, v_risk = get_stats(val_data)
    te_size, te_cids, te_intents, te_methods, te_risk = get_stats(test_data)
    
    audit = f"""# Phase 5: Split Audit

## Dataset Leakage & Verification
- **Total Examples (Train + Val + Test):** {t_size + v_size + te_size} (Must equal 10,812)
- **Train / Validation Overlap (Conversations):** {len(train_convs.intersection(val_convs))} (Must be 0)
- **Train / Test Overlap (Conversations):** {len(train_convs.intersection(test_convs))} (Must be 0)
- **Validation / Test Overlap (Conversations):** {len(val_convs.intersection(test_convs))} (Must be 0)

## Split Overview
| Split | Examples | % of Total | Unique Conversations |
|---|---|---|---|
| Train | {t_size} | {(t_size/10812*100):.1f}% | {t_cids} |
| Validation | {v_size} | {(v_size/10812*100):.1f}% | {v_cids} |
| Test | {te_size} | {(te_size/10812*100):.1f}% | {te_cids} |

## Intent Distribution per Split
"""
    # Get all unique intents across the dataset
    all_intents = sorted(list(set(t_intents.keys()) | set(v_intents.keys()) | set(te_intents.keys())))
    
    audit += "| Intent | Train | Validation | Test |\n|---|---|---|---|\n"
    for intent in all_intents:
        t_c = t_intents.get(intent, 0)
        v_c = v_intents.get(intent, 0)
        te_c = te_intents.get(intent, 0)
        audit += f"| {intent} | {t_c} | {v_c} | {te_c} |\n"
        
    audit += "\n## Risk & Assignment Methods\n"
    audit += f"- **LOW_FREQUENCY_SPECIAL_CASE (Train/Val/Test):** {t_intents.get('LOW_FREQUENCY_SPECIAL_CASE', 0)} / {v_intents.get('LOW_FREQUENCY_SPECIAL_CASE', 0)} / {te_intents.get('LOW_FREQUENCY_SPECIAL_CASE', 0)}\n"
    audit += f"- **Examples with Risk Flags (Train/Val/Test):** {t_risk} / {v_risk} / {te_risk}\n"

    with open("reports/phase5_split_audit.md", 'w', encoding='utf-8') as f:
        f.write(audit)
        
    logger.info("Dataset split successfully. Zero conversation leakage.")

if __name__ == "__main__":
    split_dataset()
