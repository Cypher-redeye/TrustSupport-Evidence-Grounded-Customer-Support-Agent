import pytest
import os
import json
from pathlib import Path
from src.retrieval.retriever import EvidenceRetriever

@pytest.fixture(scope="module")
def retriever():
    return EvidenceRetriever()

def test_ood_query(retriever):
    res = retriever.retrieve("What is the weather today?")
    assert res["status"] == "NO_RELIABLE_EVIDENCE"
    assert res["reason"] == "OOD_QUERY"
    assert len(res["evidence"]) == 0

def test_deterministic_retrieval(retriever):
    q = "I bought cod points but they are missing from my account."
    res1 = retriever.retrieve(q, top_k=3)
    res2 = retriever.retrieve(q, top_k=3)
    
    assert res1["status"] == "SUCCESS"
    assert res1["evidence"][0]["evidence_id"] == res2["evidence"][0]["evidence_id"]
    assert res1["evidence"][1]["evidence_id"] == res2["evidence"][1]["evidence_id"]
    
def test_duplicate_handling(retriever):
    # A generic query that might hit canned responses
    res = retriever.retrieve("how do I clear my cache on xbox?", top_k=3)
    if res["status"] == "SUCCESS" and len(res["evidence"]) == 3:
        # Check jaccard
        t1 = set(res["evidence"][0]["historical_brand_response"].lower().split())
        t2 = set(res["evidence"][1]["historical_brand_response"].lower().split())
        t3 = set(res["evidence"][2]["historical_brand_response"].lower().split())
        
        sim12 = len(t1 & t2) / len(t1 | t2)
        sim13 = len(t1 & t3) / len(t1 | t3)
        sim23 = len(t2 & t3) / len(t2 | t3)
        
        # Should be diverse, Jaccard <= 0.8
        assert sim12 <= 0.8, "Top 1 and 2 are duplicates"
        assert sim13 <= 0.8, "Top 1 and 3 are duplicates"
        assert sim23 <= 0.8, "Top 2 and 3 are duplicates"

def test_risk_contradiction(retriever):
    # This query should trigger BAN_APPEAL risk
    res = retriever.retrieve("My account was banned for no reason unban me now I will sue you")
    # Even if it retrieves something, if no retrieved item has BAN_APPEAL, it must abstain or return only valid stuff
    if res["status"] == "NO_RELIABLE_EVIDENCE":
        assert res["reason"] in ["CONTRADICTORY_RISK_BAN_APPEAL", "CONTRADICTORY_RISK_LEGAL_THREAT", "LOW_SIMILARITY", "ALL_DUPLICATES_OR_EMPTY"]

def test_missing_index():
    with pytest.raises(Exception):
        EvidenceRetriever(index_path="models/fake_index.index")
        
def test_no_leakage_in_test_set(retriever):
    # Grab one test set item
    test_file = Path("data/processed/intent_test.jsonl")
    if not test_file.exists():
        pytest.skip("Test set not found")
        
    with open(test_file, "r", encoding="utf-8") as f:
        item = json.loads(f.readline())
        
    res = retriever.retrieve(item["text"], top_k=3)
    if res["status"] == "SUCCESS":
        for ev in res["evidence"]:
            assert ev["conversation_id"] != item["conversation_id"]
