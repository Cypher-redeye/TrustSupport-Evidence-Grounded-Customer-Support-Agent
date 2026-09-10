# Phase 6: Retrieval Error Analysis

**Total Queries:** 1616
**Abstentions:** 47 (2.9%)
  - OOD: 46
  - Low Similarity: 0
  - Risk Contradiction: 1
**Duplicate Rate:** 0.0%
**Mean Similarity:** 0.704

## Intent Recall
- **Recall@1:** 85.3%
- **Recall@3:** 93.6%
- **Recall@5:** 95.6%

## Risk Recall (Out of 90 queries with risk flags)
- **Risk Recall@1:** 66.7%
- **Risk Recall@3:** 81.1%
- **Risk Recall@5:** 84.4%

## Failure Modes (Top-3 Misses)
- **Classification Errors:** 87 (Retriever misled by wrong semantic prediction)
- **Retrieval Errors:** 14 (Classifier was correct, but true intent wasn't in Top-3)