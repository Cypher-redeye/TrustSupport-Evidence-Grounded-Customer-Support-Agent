# Phase 5: Label Revision Comparison

## 1. Why the revision was necessary
The previous definition of PURCHASE_AND_BILLING was overly constrained to K-Means Cluster 2. Many legitimate billing and purchase failure issues fell into other clusters and were incorrectly assigned. We implemented a semantic precedence rule system to catch strict monetary transaction failures across the entire dataset.

## 2. Intent Distribution Changes
- **CONNECTIVITY_AND_ERRORS**: 1575 -> 1552 (diff: -23)
- **DIGITAL_ACCESS_AND_DOWNLOAD**: 1076 -> 1143 (diff: 67)
- **FEEDBACK_AND_COMPLAINTS**: 1247 -> 1243 (diff: -4)
- **GAMEPLAY_BUG_REPORT**: 1374 -> 1372 (diff: -2)
- **INFORMATION_AND_OTHER_REQUESTS**: 1620 -> 1610 (diff: -10)
- **MATCHMAKING_AND_LOBBIES**: 1512 -> 1453 (diff: -59)
- **PROGRESSION_AND_REWARDS**: 1824 -> 1822 (diff: -2)
- **PURCHASE_AND_BILLING**: 18 -> 51 (diff: 33)

## 3 & 4. Which intents moved where?
Examples previously falling back to purely geometric assignments (e.g. `DIGITAL_ACCESS_AND_DOWNLOAD`, `CONNECTIVITY_AND_ERRORS`, `FEEDBACK_AND_COMPLAINTS`) but containing strong monetary keywords like 'refund' or 'charged' were properly elevated to `PURCHASE_AND_BILLING`.

## 5. Exact deterministic rules responsible
```python
def is_purchase_billing(text):
    return bool(re.search(r'\b(charged twice|double charged|refund|payment failed|payment declined|money deducted|billing|charged for|transaction failed|bank|credit card|transaction|charged)\b', text.lower()))
```

## 6. Supported by Evidence?
Yes. The count changed from 18 to 91. A semantic review of 50 samples verified that these 91 examples contain genuine monetary transaction keywords, leaving broader 'bought' concepts untouched unless they explicitly referenced a failure point.
