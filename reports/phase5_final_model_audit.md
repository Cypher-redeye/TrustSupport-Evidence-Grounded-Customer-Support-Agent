# Phase 5: Final Model Selection Audit

## Direct Model Comparison

| Model | Test Macro F1 | Accuracy | Weighted F1 | PURCHASE_AND_BILLING Recall | LOW_FREQUENCY_SPECIAL_CASE Recall | EXPLOIT_AND_HACKER_REPORT Recall | Combined Rare Recall | Risk False Negatives | Inference Latency |
|---|---|---|---|---|---|---|---|---|---|
| TF-IDF + Logistic Regression | 0.7850 | 0.7673 | 0.7687 | 0.7143 | 0.8333 | 0.9667 | 0.8381 | 8 | 0.017 ms |
| TF-IDF + Linear SVM | 0.7862 | 0.7692 | 0.7695 | 0.7143 | 0.7917 | 0.8833 | 0.7964 | 14 | 0.019 ms |
| Embedding Centroid | 0.7377 | 0.7964 | 0.8007 | 0.7143 | 0.6667 | 0.9333 | 0.7714 | 14 | 3.655 ms |
| Embedding + Logistic Regression | 0.8256 | 0.8837 | 0.8853 | 0.7143 | 0.7917 | 0.9333 | 0.8131 | 11 | 3.651 ms |

## Question 1: How much higher is Embedding + LR Macro F1 than TF-IDF + LR?
Embedding + LR achieves a **4.06% higher Macro F1** (0.8256 vs 0.7850) and a massive **11.64% higher absolute Accuracy** (0.8837 vs 0.7673) compared to TF-IDF + LR.

## Question 2: How much higher is TF-IDF + LR rare-intent recall than Embedding + LR?
TF-IDF + LR has a **2.50% higher combined rare-intent recall** (0.8381 vs 0.8131) than Embedding + LR.

## Question 3: Is the rare-intent advantage statistically/practically significant enough to justify sacrificing overall Macro F1?
**No.** The rare-intent recall advantage amounts to only a difference of **3 false negatives** in the entire Test set of 1,618 examples. Sacrificing nearly 12% in global dataset accuracy (hundreds of correctly routed semantic conversations) to save 3 instances of a rare intent is mathematically and operationally disproportionate.

## Question 4: Which model has fewer risk-sensitive false negatives?
**TF-IDF + Logistic Regression** has the fewest (8 false negatives across all 3 risk categories), closely followed by Embedding + LR (11 false negatives). Both models are highly capable of isolating operational risk.

## Question 5: Would a hybrid architecture be better?
**Yes.** The system is evidence-grounded and risk-aware, which intrinsically calls for separating probabilistic semantic intent classification from strict operational risk detection. 
By employing a hybrid architecture, the Embedding + LR model can optimize for general semantic meaning (maximizing accuracy across the 90%+ of normal queries), while independent deterministic rules (`_extract_risk_flags`) can guarantee that risk policies (e.g., Ban Appeals, Legal Threats) are flagged and routed appropriately regardless of what semantic bucket the classifier assigns the query to.

## FINAL DECISION

**C. Use Hybrid Architecture**

**Technical Justification:**
The core operational requirement is that high-risk queries are caught and escalated. TF-IDF + LR was originally favored solely because it had slightly fewer risk false negatives (8 vs 11). However, because we have already implemented a dedicated deterministic risk detection layer (`_extract_risk_flags` via keyword heuristics), the semantic classifier does not need to bear the entire burden of risk detection.
Therefore, we should not sacrifice 11.6% overall semantic accuracy to gain 3 fewer false negatives. 
By utilizing **Embedding + LR for semantic intent classification** and **Deterministic semantic/risk rules for risk detection**, we achieve the best of both paradigms: state-of-the-art conversational semantic routing (88.3% accuracy) combined with hard-coded fail-safes for customer escalation.

*Note: The unified `IntentClassifier` has been updated to load `embedding_lr.joblib` instead of `tfidf_lr.joblib` to reflect this final decision.*
