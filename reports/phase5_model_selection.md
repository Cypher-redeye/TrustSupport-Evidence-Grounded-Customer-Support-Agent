# Phase 5: Baseline Model Selection

## Model Comparison

| Model | Test Macro F1 | Test Accuracy | Rare Intent Recall | Inference Time (ms/example) |
|---|---|---|---|---|
| TF-IDF + LR | 0.7850 | 0.7673 | 0.8381 | 0.017 |
| TF-IDF + SVM | 0.7862 | 0.7692 | 0.7964 | 0.019 |
| Embedding Centroid | 0.7377 | 0.7964 | 0.7714 | 3.655 |
| Embedding + LR | 0.8256 | 0.8837 | 0.8131 | 3.651 |

## Recommended Production Baseline

**Model name:** TF-IDF + Logistic Regression

**Why selected:**
Although `Embedding + LR` achieved the highest Macro F1 (0.8256) and Accuracy (0.8837), `TF-IDF + LR` was selected as the recommended baseline for the following reasons:
1. **Highest Rare Intent Recall (0.8381):** It outperformed all other models (including embeddings) at retrieving critical, low-frequency risk intents (`PURCHASE_AND_BILLING`, `LOW_FREQUENCY_SPECIAL_CASE`, `EXPLOIT_AND_HACKER_REPORT`).
2. **Confidence Calibration:** Logistic Regression provides natively clean probabilities, allowing for stable thresholding (High > 85%, Unknown <= 35%).
3. **Inference Latency:** Inference is essentially instantaneous (0.017 ms/example), making it exceptionally cheap and fast compared to loading a MiniLM model.
4. **Interpretability:** Bag-of-words linear coefficients can be trivially inspected for debugging specific false positives.

**Strengths:**
- Extremely fast and lightweight.
- Best performance on rare/critical risk intents.
- Well-calibrated probabilities.

**Weaknesses:**
- Cannot handle semantic paraphrasing as well as embeddings.
- Lower overall Macro F1 and accuracy than Embedding + LR.
- Out-of-vocabulary words are ignored.

**Rare Intent Performance:**
- Achieved the highest recall (83.8%) across the 3 rarest, most operationally risky classes.

**Confidence Calibration:**
- HIGH (> 0.85): 98.8% accuracy (Coverage: 16%)
- MEDIUM (> 0.50): 89.0% accuracy (Coverage: 40%)
- LOW (> 0.35): 69.8% accuracy (Coverage: 22%)
- UNKNOWN: 20% of inputs

**Known Failure Modes:**
- Susceptible to exact keyword matching overlaps (e.g., confusing `DIGITAL_ACCESS_AND_DOWNLOAD` with `PROGRESSION_AND_REWARDS` if they share words like "game" or "account").

**Why alternatives were rejected:**
- **Embedding + LR:** Rejected despite higher F1 because rare intent recall was slightly lower, and it requires a transformer inference stack, defeating the purpose of a simple, robust classical baseline. 
- **TF-IDF + Linear SVM:** Rejected because the decision function margins are not calibrated probabilities, making UNKNOWN and confidence tiering mathematically unsound without Platt scaling.
- **Embedding Centroid:** Rejected because it performed the worst on Macro F1 (0.7377) and struggled with class imbalance.
