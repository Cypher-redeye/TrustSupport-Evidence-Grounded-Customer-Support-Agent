# Phase 4: Intent Discovery Report

## 1. Customer Messages Analyzed
- **Total Eligible Request Blocks:** 10,812
- **Sampling Strategy:** 100% of eligible initial customer request blocks were embedded. No downsampling was required as performance and memory were well within limits.

## 2. Methodology
- **Embedding Model:** `sentence-transformers/all-MiniLM-L6-v2` (Dimensions: 384)
- **Clustering Algorithms:** KMeans (K=6,8,10,12,15) and HDBSCAN.

## 3. Metrics Summary
| Algorithm | Config | Silhouette | Davies-Bouldin | Max Cluster % | Noise % |
|---|---|---|---|---|---|
| KMeans | K=8 | 0.0285 | 4.06 | 20.4% | 0.0% |
| KMeans | K=10 | 0.0332 | 3.90 | 15.0% | 0.0% |
| KMeans | K=12 | 0.0378 | 3.73 | 13.2% | 0.0% |
| HDBSCAN | default | 0.2486 | 1.53 | 1.5% | 87.3% |

*Note: Purely mathematical clustering metrics (Silhouette) are notoriously low for high-dimensional text embeddings. HDBSCAN classified 87% of the dataset as noise, indicating that customer queries are highly dispersed with a few incredibly dense pockets (like the "Pointe du Hoc glitch"). Therefore, operational usability (inspection) superseded geometric metrics.*

## 4. Proposed Intents & Taxonomy
We mapped the KMeans clusters into **8 Core Operational Intents**. 
Categories intentionally merged:
- "Error Code 5" and "Error Code 103295" -> `CONNECTIVITY_AND_ERRORS`
- "Missing COD Points" and "Missing Supply Drops" -> `ACCOUNT_AND_REWARDS`

Rare but critical issues (like Account Bans or Payments) are handled via **Risk Flags** (`ACCOUNT_SPECIFIC`, `PAYMENT`, `GAME_INTEGRITY`) attached to the core intents. This prevents the classifier from struggling with highly imbalanced rare classes while still enabling escalation routing.

## 5. Review Set
A 96-example golden taxonomy review set has been generated at `data/golden/intent_taxonomy_review.jsonl`. It includes centroid (highly confident), boundary (ambiguous), and random samples, tagged with `review_priority`.
