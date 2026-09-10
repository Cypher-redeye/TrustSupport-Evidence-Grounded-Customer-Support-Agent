import json
import logging
import numpy as np
import re
import csv
from pathlib import Path
from src.config import settings
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import euclidean_distances

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def generate_taxonomy_artifacts():
    # ---------------------------------------------------------
    # 1. LOAD DATA
    # ---------------------------------------------------------
    embed_file = Path(settings.processed_data_dir) / "intent_embeddings.npz"
    if not embed_file.exists(): return
    cache = np.load(embed_file)
    embeddings = cache['embeddings']
    request_ids = cache['request_ids']
    
    sample_file = Path(settings.processed_data_dir) / "intent_discovery_sample.jsonl"
    requests = {}
    with open(sample_file, 'r', encoding='utf-8') as f:
        for line in f:
            req = json.loads(line)
            requests[req['request_id']] = req

    # K=10
    model = KMeans(n_clusters=10, random_state=settings.random_seed, n_init=10)
    labels = model.fit_predict(embeddings)
    centroids = model.cluster_centers_
    dists = euclidean_distances(embeddings, centroids)
    
    # ---------------------------------------------------------
    # 2. FULL DATASET ACCOUNTING (10,812 examples)
    # ---------------------------------------------------------
    intent_assignments = {} # req_id -> intent
    assignment_methods = {} # req_id -> method
    risk_flags = {} # req_id -> list of flags
    
    # Risk Regex Patterns
    risk_patterns = {
        'BAN_APPEAL': r'\b(ban|banned|suspended|unban)\b',
        'ACCOUNT_COMPROMISED': r'\b(hacked|stolen|compromised|unauthorized)\b',
        'PROGRESSION_DATA_LOSS': r'\b(stats reset|reset my stats|lost all my stats)\b',
        'PAYMENT': r'\b(payment|charged|refund|money back|dollars)\b',
        'GAME_INTEGRITY': r'\b(aimbot|hacker|boosting|out of map|exploit)\b',
        'LEGAL_THREAT': r'\b(sue|lawyer|legal)\b'
    }

    # Pass 1: Global Risk & Rule Overrides (Priority)
    for i, req_id in enumerate(request_ids):
        req = requests[req_id]
        text = req['text'].lower()
        c_id = labels[i]
        
        flags = []
        for flag, pattern in risk_patterns.items():
            if re.search(pattern, text):
                flags.append(flag)
        
        if flags:
            risk_flags[req_id] = flags
            
        # Isolate Low Frequency Special Cases
        if 'BAN_APPEAL' in flags or 'ACCOUNT_COMPROMISED' in flags or 'PROGRESSION_DATA_LOSS' in flags or 'LEGAL_THREAT' in flags:
            intent_assignments[req_id] = 'LOW_FREQUENCY_SPECIAL_CASE'
            assignment_methods[req_id] = 'RISK_RULE'
            continue
            
        # Cluster 2 Rule Assisted Split
        if c_id == 2:
            if 'PAYMENT' in flags:
                intent_assignments[req_id] = 'PURCHASE_AND_BILLING'
                assignment_methods[req_id] = 'RULE_ASSISTED_SPLIT'
            elif re.search(r'\b(download|pre-load|preload|install|installing|code|digital copy|redeem)\b', text):
                intent_assignments[req_id] = 'DIGITAL_ACCESS_AND_DOWNLOAD'
                assignment_methods[req_id] = 'RULE_ASSISTED_SPLIT'
            else:
                # If neither matched exactly, default to DIGITAL_ACCESS based on cluster majority
                intent_assignments[req_id] = 'DIGITAL_ACCESS_AND_DOWNLOAD'
                assignment_methods[req_id] = 'RULE_ASSISTED_SPLIT'
            continue
            
    # Pass 2: Direct Cluster Mapping for the rest
    for i, req_id in enumerate(request_ids):
        if req_id in intent_assignments:
            continue
            
        c_id = labels[i]
        if c_id in [1, 4]:
            intent_assignments[req_id] = 'CONNECTIVITY_AND_ERRORS'
            assignment_methods[req_id] = 'DIRECT_CLUSTER_MAPPING'
        elif c_id in [7, 8]:
            intent_assignments[req_id] = 'PROGRESSION_AND_REWARDS'
            assignment_methods[req_id] = 'DIRECT_CLUSTER_MAPPING'
        elif c_id == 3:
            intent_assignments[req_id] = 'MATCHMAKING_AND_LOBBIES'
            assignment_methods[req_id] = 'DIRECT_CLUSTER_MAPPING'
        elif c_id == 5:
            intent_assignments[req_id] = 'EXPLOIT_AND_HACKER_REPORT'
            assignment_methods[req_id] = 'DIRECT_CLUSTER_MAPPING'
        elif c_id == 6:
            intent_assignments[req_id] = 'GAMEPLAY_BUG_REPORT'
            assignment_methods[req_id] = 'DIRECT_CLUSTER_MAPPING'
        elif c_id == 0:
            intent_assignments[req_id] = 'FEEDBACK_AND_COMPLAINTS'
            assignment_methods[req_id] = 'DIRECT_CLUSTER_MAPPING'
        elif c_id == 9:
            intent_assignments[req_id] = 'INFORMATION_AND_OTHER_REQUESTS'
            assignment_methods[req_id] = 'DIRECT_CLUSTER_MAPPING'
        else:
            # Fallback for completely unknown data
            intent_assignments[req_id] = 'EXCLUDED_NOISE'
            assignment_methods[req_id] = 'EXCLUSION_RULE'

    # Compute Final Distributions
    intent_counts = {}
    intent_pcts = {}
    total_assigned = len(request_ids)
    for intent in intent_assignments.values():
        intent_counts[intent] = intent_counts.get(intent, 0) + 1
        
    # Write Final Distribution CSV
    dist_csv = Path("results/final_intent_distribution.csv")
    dist_csv.parent.mkdir(exist_ok=True)
    with open(dist_csv, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["intent", "count", "percentage", "assignment_method"])
        for intent, count in sorted(intent_counts.items(), key=lambda x: x[1], reverse=True):
            pct = (count / total_assigned) * 100
            
            # Extract common assignment method for this intent
            methods = [m for rid, m in assignment_methods.items() if intent_assignments[rid] == intent]
            main_method = max(set(methods), key=methods.count)
            
            writer.writerow([intent, count, f"{pct:.2f}%", main_method])

    # ---------------------------------------------------------
    # 3. UNMAPPED REQUEST ANALYSIS (Cluster 9 & Noise)
    # ---------------------------------------------------------
    unmapped_md = f"""# Unmapped Request Analysis

## Overview
During initial taxonomy drafting, Cluster 9 and edge-case exceptions were unaccounted for in the estimated distributions. This document rigorously analyzes all previously unmapped requests.

## Accounting Equation
- **Total Eligible Request Blocks:** {total_assigned}
- **Assigned Intents:** {sum(1 for v in intent_assignments.values() if v != 'EXCLUDED_NOISE')}
- **Documented Exclusions:** {sum(1 for v in intent_assignments.values() if v == 'EXCLUDED_NOISE')}
- **Total Accounted For:** {len(intent_assignments)}
- **Missing / Unaccounted:** {total_assigned - len(intent_assignments)} (Must be 0)

## Analysis of Cluster 9 (Now: INFORMATION_AND_OTHER_REQUESTS)
- **Count:** {intent_counts.get('INFORMATION_AND_OTHER_REQUESTS', 0)}
- **Percentage:** {(intent_counts.get('INFORMATION_AND_OTHER_REQUESTS', 0) / total_assigned * 100):.2f}%
- **Common Patterns:** Hardware inquiries (Guitar Hero controllers), cross-title issues, highly generic "how to" questions, and multi-issue queries that don't strongly cluster around a single technical vector.
- **Decision:** Added `INFORMATION_AND_OTHER_REQUESTS` to cleanly map the remainder of the dataset without forcing generic queries into strict bug/error intents.
"""
    with open("reports/unmapped_request_analysis.md", 'w', encoding='utf-8') as f:
        f.write(unmapped_md)
        
    # ---------------------------------------------------------
    # 4. GENERATE REVIEW SET (Schema & Margins)
    # ---------------------------------------------------------
    review_set = []
    used_indices = set()
    
    def make_review_item(idx, sample_type, priority, notes):
        req_id = request_ids[idx]
        req = requests[req_id]
        c_id = labels[idx]
        
        point_dists = dists[idx]
        sorted_dists = np.sort(point_dists)
        nearest = sorted_dists[0]
        second_nearest = sorted_dists[1] if len(sorted_dists) > 1 else nearest
        margin = second_nearest - nearest
        
        return {
            "request_id": req['request_id'],
            "tweet_ids": req['tweet_ids'],
            "conversation_id": req['conversation_id'],
            "text": req['text'],
            "raw_cluster_id": str(c_id),
            "system_proposed_intent": intent_assignments[req_id],
            "human_reviewed_intent": None,
            "assignment_method": assignment_methods[req_id],
            "nearest_cluster_distance": float(nearest),
            "second_nearest_cluster_distance": float(second_nearest),
            "assignment_margin": float(margin),
            "review_priority": priority,
            "sample_type": sample_type,
            "risk_candidate": bool(risk_flags.get(req_id, [])),
            "risk_candidate_reason": risk_flags.get(req_id, []),
            "notes": notes
        }

    for c_id in range(10):
        c_indices = np.where(labels == c_id)[0]
        c_dists = dists[c_indices]
        
        c_margins = []
        for i in range(len(c_indices)):
            sorted_dists = np.sort(c_dists[i])
            c_margins.append(sorted_dists[1] - sorted_dists[0])
        c_margins = np.array(c_margins)
        
        # Centroids
        own_dists = c_dists[:, c_id]
        centroid_idx = np.argsort(own_dists)[:3]
        for idx in centroid_idx:
            global_idx = c_indices[idx]
            review_set.append(make_review_item(global_idx, "CENTROID", "HIGH", "Cluster core"))
            used_indices.add(global_idx)
            
        # Boundary
        boundary_idx = np.argsort(c_margins)[:3]
        for idx in boundary_idx:
            global_idx = c_indices[idx]
            if global_idx not in used_indices:
                review_set.append(make_review_item(global_idx, "BOUNDARY", "HIGH", "Smallest assignment margin"))
                used_indices.add(global_idx)
                
        # Random
        np.random.seed(settings.random_seed + c_id)
        rand_idx = np.random.choice(len(c_indices), min(4, len(c_indices)), replace=False)
        for idx in rand_idx:
            global_idx = c_indices[idx]
            if global_idx not in used_indices:
                review_set.append(make_review_item(global_idx, "RANDOM", "LOW", "Random sample"))
                used_indices.add(global_idx)

    # Inject LOW_FREQUENCY_SPECIAL_CASE (Risk)
    risk_added = 0
    for i, req_id in enumerate(request_ids):
        if risk_added >= 15: break
        if i in used_indices: continue
        if assignment_methods[req_id] == 'RISK_RULE':
            review_set.append(make_review_item(i, "RISK", "HIGH", "Low Frequency Special Case"))
            used_indices.add(i)
            risk_added += 1

    out_review = Path("data/golden/intent_taxonomy_review.jsonl")
    with open(out_review, 'w', encoding='utf-8') as f:
        for r in review_set:
            f.write(json.dumps(r) + "\n")

    # ---------------------------------------------------------
    # 5. DRAFT TAXONOMY MARKDOWN
    # ---------------------------------------------------------
    taxonomy_md = f"""# INTENT TAXONOMY (DRAFT)

Based on the operational analysis of K-Means clustering (K=10) on ATVIAssist customer requests and subsequent full-dataset accounting, the following data-driven taxonomy is proposed.

## Proposed Intents

### 1. CONNECTIVITY_AND_ERRORS
**Description**: Customer is experiencing server outages, specific error codes, or getting disconnected mid-match.
**Typical Routing**: AUTO_HANDLE

### 2. PROGRESSION_AND_REWARDS
**Description**: Customer is missing earned items, supply drops, unlock tokens, or contracts are bugged/resetting.
**Typical Routing**: ESCALATE

### 3. DIGITAL_ACCESS_AND_DOWNLOAD
**Description**: Customer cannot download the game, DLC, or pre-order bonuses. (Access rights, installation, and codes).
**Typical Routing**: AUTO_HANDLE

### 4. PURCHASE_AND_BILLING
**Description**: Customer is experiencing monetary transaction issues.
**Typical Routing**: ESCALATE
**Risk Flags**: `PAYMENT`

### 5. MATCHMAKING_AND_LOBBIES
**Description**: Customer cannot find a match, headquarters is empty, or party functionality is broken.
**Typical Routing**: AUTO_HANDLE

### 6. EXPLOIT_AND_HACKER_REPORT
**Description**: Customer is reporting a player cheating, boosting, or exploiting a map glitch.
**Typical Routing**: AUTO_HANDLE
**Risk Flags**: `GAME_INTEGRITY`

### 7. GAMEPLAY_BUG_REPORT
**Description**: Customer is reporting a non-exploitative bug affecting gameplay.
**Typical Routing**: AUTO_HANDLE

### 8. FEEDBACK_AND_COMPLAINTS
**Description**: General frustration, game balance complaints, or non-actionable venting.
**Typical Routing**: AUTO_HANDLE_ACKNOWLEDGEMENT
**Risk Flags**: `HIGH_EMOTION`

### 9. INFORMATION_AND_OTHER_REQUESTS
**Description**: General inquiries, hardware compatibility questions, or multi-issue requests lacking a specific cluster definition.
**Typical Routing**: AUTO_HANDLE (via KB Retrieval)

### 10. LOW_FREQUENCY_SPECIAL_CASE
**Description**: High-risk, low-frequency cases (e.g., Ban appeals, hacked accounts, stats resets, legal threats). These are semantically distinct but too rare (< 2% combined) to support individual classification intents. They are routed purely via their specific risk flags.
**Typical Routing**: ESCALATE
**Risk Flags**: `BAN_APPEAL`, `ACCOUNT_COMPROMISED`, `PROGRESSION_DATA_LOSS`, `LEGAL_THREAT`
"""
    with open("INTENT_TAXONOMY_DRAFT.md", 'w', encoding='utf-8') as f:
        f.write(taxonomy_md)

    # ---------------------------------------------------------
    # 6. TAXONOMY MAPPING TRACEABILITY
    # ---------------------------------------------------------
    def get_pct(intent):
        return f"{(intent_counts.get(intent, 0) / total_assigned * 100):.2f}%"
        
    mapping_md = f"""# Taxonomy Mapping (K=10 Traceability)

## 1. CONNECTIVITY_AND_ERRORS
- **Count / Percentage**: {intent_counts.get('CONNECTIVITY_AND_ERRORS', 0)} ({get_pct('CONNECTIVITY_AND_ERRORS')})
- **Source Clusters**: Cluster 1 (Error Codes), Cluster 4 (Server Outages)
- **Assignment Method**: DIRECT_CLUSTER_MAPPING
- **Routing**: AUTO_HANDLE
- **Risk Flags**: None

## 2. PROGRESSION_AND_REWARDS
- **Count / Percentage**: {intent_counts.get('PROGRESSION_AND_REWARDS', 0)} ({get_pct('PROGRESSION_AND_REWARDS')})
- **Source Clusters**: Cluster 7 (Supply Drops), Cluster 8 (Tokens & Contracts)
- **Assignment Method**: DIRECT_CLUSTER_MAPPING
- **Routing**: ESCALATE
- **Risk Flags**: None

## 3. DIGITAL_ACCESS_AND_DOWNLOAD
- **Count / Percentage**: {intent_counts.get('DIGITAL_ACCESS_AND_DOWNLOAD', 0)} ({get_pct('DIGITAL_ACCESS_AND_DOWNLOAD')})
- **Source Clusters**: Cluster 2 (Partial)
- **Assignment Method**: RULE_ASSISTED_SPLIT
- **Routing**: AUTO_HANDLE
- **Risk Flags**: None

## 4. PURCHASE_AND_BILLING
- **Count / Percentage**: {intent_counts.get('PURCHASE_AND_BILLING', 0)} ({get_pct('PURCHASE_AND_BILLING')})
- **Source Clusters**: Cluster 2 (Partial)
- **Assignment Method**: RULE_ASSISTED_SPLIT
- **Routing**: ESCALATE
- **Risk Flags**: PAYMENT

## 5. MATCHMAKING_AND_LOBBIES
- **Count / Percentage**: {intent_counts.get('MATCHMAKING_AND_LOBBIES', 0)} ({get_pct('MATCHMAKING_AND_LOBBIES')})
- **Source Clusters**: Cluster 3
- **Assignment Method**: DIRECT_CLUSTER_MAPPING
- **Routing**: AUTO_HANDLE
- **Risk Flags**: None

## 6. EXPLOIT_AND_HACKER_REPORT
- **Count / Percentage**: {intent_counts.get('EXPLOIT_AND_HACKER_REPORT', 0)} ({get_pct('EXPLOIT_AND_HACKER_REPORT')})
- **Source Clusters**: Cluster 5
- **Assignment Method**: DIRECT_CLUSTER_MAPPING
- **Routing**: AUTO_HANDLE
- **Risk Flags**: GAME_INTEGRITY

## 7. GAMEPLAY_BUG_REPORT
- **Count / Percentage**: {intent_counts.get('GAMEPLAY_BUG_REPORT', 0)} ({get_pct('GAMEPLAY_BUG_REPORT')})
- **Source Clusters**: Cluster 6
- **Assignment Method**: DIRECT_CLUSTER_MAPPING
- **Routing**: AUTO_HANDLE
- **Risk Flags**: None

## 8. FEEDBACK_AND_COMPLAINTS
- **Count / Percentage**: {intent_counts.get('FEEDBACK_AND_COMPLAINTS', 0)} ({get_pct('FEEDBACK_AND_COMPLAINTS')})
- **Source Clusters**: Cluster 0
- **Assignment Method**: DIRECT_CLUSTER_MAPPING
- **Routing**: AUTO_HANDLE_ACKNOWLEDGEMENT
- **Risk Flags**: HIGH_EMOTION

## 9. INFORMATION_AND_OTHER_REQUESTS
- **Count / Percentage**: {intent_counts.get('INFORMATION_AND_OTHER_REQUESTS', 0)} ({get_pct('INFORMATION_AND_OTHER_REQUESTS')})
- **Source Clusters**: Cluster 9
- **Assignment Method**: DIRECT_CLUSTER_MAPPING
- **Routing**: AUTO_HANDLE
- **Risk Flags**: None

## 10. LOW_FREQUENCY_SPECIAL_CASE
- **Count / Percentage**: {intent_counts.get('LOW_FREQUENCY_SPECIAL_CASE', 0)} ({get_pct('LOW_FREQUENCY_SPECIAL_CASE')})
- **Source Clusters**: Extracted globally
- **Assignment Method**: RISK_RULE
- **Routing**: ESCALATE
- **Risk Flags**: BAN_APPEAL, ACCOUNT_COMPROMISED, PROGRESSION_DATA_LOSS, LEGAL_THREAT
"""
    with open("reports/taxonomy_mapping.md", 'w', encoding='utf-8') as f:
        f.write(mapping_md)
        
    logger.info("Final taxonomy artifacts generated successfully.")

if __name__ == "__main__":
    generate_taxonomy_artifacts()
