# Phase 6: Evidence Dataset Audit

## Extraction Metrics
- **Total Train Samples:** 7580
- **Valid Pairs (with ATVIAssist response):** 7580
- **Missing Brand Response (dropped):** 0
- **Total Unique Brand Response Blocks:** 7577

## Summary
Only customer requests that received a documented reply from `ATVIAssist` are included in the retrieval index.
Consecutive brand tweets were merged into a `historical_response_block` to preserve multi-tweet answers.
A large discrepancy between 'Valid Pairs' and 'Total Unique Brand Response Blocks' highlights the prevalence of canned/templated responses in historical support, underscoring the need for deductive diversity filtering during Top-K retrieval.