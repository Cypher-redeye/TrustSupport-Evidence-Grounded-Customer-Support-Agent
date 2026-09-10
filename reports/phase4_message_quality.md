# Phase 4: Message Quality & Sampling Report

## Extraction Strategy
The unit of analysis is defined as the **INITIAL CUSTOMER REQUEST BLOCK**. This consists of all contiguous customer tweets belonging to the initial support request *before* the first brand response. Mentions were stripped during quality analysis to ensure the message contained actual content.

## Processing Statistics
- **Total Conversations:** 11113
- **Total Eligible Request Blocks Extracted:** 10812
- **Total Excluded:** 301

### Exclusion Reasons
- **NO_INITIAL_CUSTOMER_MESSAGE**: 132
- **TOO_SHORT**: 81
- **EMPTY_AFTER_CLEANING**: 52
- **TOO_LONG**: 36

## Sampling Decision
Since the number of eligible request blocks (10812) is <= 15,000, we are embedding **ALL eligible request blocks** to preserve maximum data fidelity. No downsampling was required.

> The complete sample has been saved to `data/processed/intent_discovery_sample.jsonl`.