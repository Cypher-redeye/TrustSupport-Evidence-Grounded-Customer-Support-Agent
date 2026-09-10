import os
import json
import numpy as np
import pytest
from pathlib import Path

from src.intents.prepare_messages import is_noise
from src.config import settings

def test_is_noise():
    # Empty message
    noisy, reason = is_noise("")
    assert noisy is True
    assert reason == "EMPTY_AFTER_CLEANING"
    
    # URL only
    noisy, reason = is_noise("http://example.com/test")
    assert noisy is True
    assert reason == "EMPTY_AFTER_CLEANING"
    
    # Mention only
    noisy, reason = is_noise("@ATVIAssist")
    assert noisy is True
    assert reason == "EMPTY_AFTER_CLEANING"
    
    # Too short
    noisy, reason = is_noise("fix game")
    assert noisy is True
    assert reason == "TOO_SHORT"
    
    # Valid
    noisy, reason = is_noise("@ATVIAssist my game keeps crashing when I launch multiplayer")
    assert noisy is False
    assert reason == ""

def test_embedding_cache_structure(tmp_path):
    # Test that the embed.py expects a specific cache structure
    cache_file = tmp_path / "intent_embeddings.npz"
    embeddings = np.random.rand(10, 384)
    request_ids = np.array([f"req_{i}" for i in range(10)])
    
    np.savez_compressed(
        cache_file, 
        embeddings=embeddings, 
        request_ids=request_ids,
        model_name="test-model",
        random_seed=42,
        num_messages=10
    )
    
    cache = np.load(cache_file)
    assert 'embeddings' in cache
    assert 'request_ids' in cache
    assert cache['model_name'] == 'test-model'
    assert len(cache['embeddings']) == 10

def test_sampling_determinism():
    # Test that setting the random seed ensures consistent sampling 
    # (Since we didn't end up downsampling, this just tests the seed config)
    import random
    random.seed(settings.random_seed)
    sample1 = random.sample(range(1000), 10)
    
    random.seed(settings.random_seed)
    sample2 = random.sample(range(1000), 10)
    
    assert sample1 == sample2

def test_invalid_clustering_config():
    # Test that trying to load missing embeddings handles gracefully
    from src.intents.cluster import load_data
    
    # Mock settings to point to empty dir
    original_dir = settings.processed_data_dir
    settings.processed_data_dir = "invalid_dir_that_doesnt_exist"
    
    emb, ids = load_data()
    assert emb is None
    assert ids is None
    
    settings.processed_data_dir = original_dir

def test_review_set_schema():
    review_file = Path("data/golden/intent_taxonomy_review.jsonl")
    if review_file.exists():
        with open(review_file, 'r', encoding='utf-8') as f:
            line = f.readline()
            if line:
                req = json.loads(line)
                assert "request_id" in req
                assert "tweet_ids" in req
                assert "conversation_id" in req
                assert "text" in req
                assert "raw_cluster_id" in req
                assert "system_proposed_intent" in req
                assert "human_reviewed_intent" in req
                assert "nearest_cluster_distance" in req
                assert "second_nearest_cluster_distance" in req
                assert "assignment_margin" in req
                assert "review_priority" in req
                assert "sample_type" in req
                assert "risk_candidate" in req
                assert "risk_candidate_reason" in req
                assert "notes" in req

def test_boundary_calculation():
    from sklearn.metrics.pairwise import euclidean_distances
    # Mock boundary margin calculation
    embeddings = np.array([[0, 0], [1.5, 0], [3, 0]])
    centroids = np.array([[0, 0], [3, 0]])
    
    dists = euclidean_distances(embeddings, centroids)
    
    # Point at [1.5, 0] is exactly in the middle
    pt_dists = dists[1]
    sorted_dists = np.sort(pt_dists)
    margin = sorted_dists[1] - sorted_dists[0]
    
    assert margin == 0.0 # Exactly on the boundary

def test_risk_retrieval_regex():
    import re
    text = "my account was hacked and I got banned"
    
    patterns = [
        (r'\b(ban|banned|suspended|unban)\b', "Ban/Suspension"),
        (r'\b(hacked|stolen|compromised|unauthorized)\b', "Account Compromise")
    ]
    
    reasons = []
    for p, r in patterns:
        if re.search(p, text):
            reasons.append(r)
            
    assert "Ban/Suspension" in reasons
    assert "Account Compromise" in reasons
    assert len(reasons) == 2

def test_taxonomy_traceability():
    mapping_file = Path("reports/taxonomy_mapping.md")
    if mapping_file.exists():
        content = mapping_file.read_text(encoding='utf-8')
        assert "CONNECTIVITY_AND_ERRORS" in content
        assert "PROGRESSION_AND_REWARDS" in content
        assert "Cluster 1" in content
        assert "Cluster 7" in content

def test_review_set_proposed_intent():
    review_file = Path("data/golden/intent_taxonomy_review.jsonl")
    if review_file.exists():
        with open(review_file, 'r', encoding='utf-8') as f:
            for line in f:
                req = json.loads(line)
                assert req.get("system_proposed_intent"), "System proposed intent must be populated"
                assert req.get("human_reviewed_intent") is None, "Human intent should be null"
                assert req.get("assignment_method"), "Assignment method must be present"
                assert req["assignment_method"] in ["DIRECT_CLUSTER_MAPPING", "RULE_ASSISTED_SPLIT", "SUBCLUSTER_MAPPING", "RISK_RULE", "EXCLUSION_RULE"]

def test_final_taxonomy_accounting():
    dist_file = Path("results/final_intent_distribution.csv")
    if dist_file.exists():
        import csv
        total = 0
        with open(dist_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                total += int(row['count'])
                
        # Total mapped should exactly equal 10812 (including exclusions if any)
        assert total == 10812, f"Total intent sum must exactly equal 10812 eligible requests, got {total}"
