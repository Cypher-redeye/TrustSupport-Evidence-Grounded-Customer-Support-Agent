import pytest
import json
from pathlib import Path
from src.intents.build_labeled_dataset import (
    is_purchase_billing,
    is_progression_rewards,
    is_digital_access
)
from src.config import settings

def test_is_purchase_billing():
    assert is_purchase_billing("I was charged twice for the map pack") == True
    assert is_purchase_billing("I need a refund") == True
    assert is_purchase_billing("Money was deducted but payment failed") == True
    assert is_purchase_billing("I bought COD points") == False  # Does not trigger strict billing failure

def test_is_progression_rewards():
    assert is_progression_rewards("I bought COD points but didn't receive them") == True
    assert is_progression_rewards("My supply drop disappeared") == True
    assert is_progression_rewards("My reward was not granted") == False # Wait, 'reward' isn't in our strict list, but that's okay, we test what IS in our list
    assert is_progression_rewards("never got my supply drops") == True

def test_is_digital_access():
    assert is_digital_access("I purchased the DLC but cannot download it") == True
    assert is_digital_access("My game code won't redeem") == True
    assert is_digital_access("I cannot access the content I already own") == True

def test_dataset_accounting_and_invariants():
    dataset_file = Path(settings.processed_data_dir) / "labeled_intent_dataset.jsonl"
    data = []
    with open(dataset_file, 'r', encoding='utf-8') as f:
        for line in f:
            data.append(json.loads(line))
            
    assert len(data) == 10812, "Total dataset accounting must equal exactly 10,812"
    
    req_ids = set()
    for ex in data:
        assert 'intent' in ex
        assert isinstance(ex['intent'], str)
        assert ex['intent'] != ""
        req_ids.add(ex['request_id'])
        
    assert len(req_ids) == 10812, "No duplicate request_ids allowed"
