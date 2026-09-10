# Phase 5: Confusion Matrix Analysis

## Methodology

Four baseline models were evaluated on the independent test set (N=1,618) to analyze inter-class confusion:

- TF-IDF + Logistic Regression
- TF-IDF + Linear SVM
- Embedding Centroid
- Embedding + Logistic Regression

Confusion matrices for each model are saved in the `results/` directory as CSV files:
- `results/confusion_matrix_tfidf_lr.csv`
- `results/confusion_matrix_tfidf_svm.csv`
- `results/confusion_matrix_embedding_centroid.csv`
- `results/confusion_matrix_embedding_lr.csv`

## Major Confusion Patterns

### 1. DIGITAL_ACCESS_AND_DOWNLOAD vs PROGRESSION_AND_REWARDS
This was the most frequent confusion pair across all models.
- **Cause:** Both classes deal with the lack of access to digital items. `DIGITAL_ACCESS_AND_DOWNLOAD` involves codes, redemption, and game ownership. `PROGRESSION_AND_REWARDS` involves missing virtual items (e.g., COD points, camos) *after* successful purchase or gameplay.
- **Model behavior:** TF-IDF models struggle when customers say "I didn't get my game" vs "I didn't get my points", as the keywords heavily overlap (e.g., "missing", "didn't get").

### 2. CONNECTIVITY_AND_ERRORS vs MATCHMAKING_AND_LOBBIES
- **Cause:** Network issues often manifest as matchmaking failures (e.g., "getting kicked from lobby", "can't connect to match").
- **Model behavior:** Both models exhibited boundary bleed. Semantic rules from Phase 4 defined server crashes as `CONNECTIVITY` and slow queue times as `MATCHMAKING`, but customer language is ambiguous ("I can't get into a game").

### 3. GAMEPLAY_BUG_REPORT vs FEEDBACK_AND_COMPLAINTS
- **Cause:** Customers often report bugs using highly emotional or complaining language ("this game is broken", "fix your trash game").
- **Model behavior:** The Embedding + LR model correctly identified the semantic frustration, but often misclassified specific bug descriptions into the generic `FEEDBACK_AND_COMPLAINTS` bucket.

## Risk-Sensitive Performance

### PURCHASE_AND_BILLING
- **Performance:** Exceptionally well-isolated by TF-IDF models due to the strict vocabulary of financial failure ("charged", "money", "bought").
- **False Negatives:** Almost zero. When it failed, it confused with `PROGRESSION_AND_REWARDS`.

### LOW_FREQUENCY_SPECIAL_CASE
- **Performance:** Excellent recall across models, proving that group-stratified splitting successfully preserved the signal of this highly specific class.
- **False Negatives:** When missed, it was usually classified as `ACCOUNT_COMPROMISED` (due to similar account-centric language) or `FEEDBACK_AND_COMPLAINTS`.

## Conclusion
The confusion patterns follow the semantic boundaries established during Phase 4 Intent Discovery. The models performed exactly as expected, struggling primarily where the actual operational boundary is ambiguous or where customer language lacks specificity.
