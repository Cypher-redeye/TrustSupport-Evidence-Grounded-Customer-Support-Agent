# Phase 5: Split Audit

## Dataset Leakage & Verification
- **Total Examples (Train + Val + Test):** 10812 (Must equal 10,812)
- **Train / Validation Overlap (Conversations):** 0 (Must be 0)
- **Train / Test Overlap (Conversations):** 0 (Must be 0)
- **Validation / Test Overlap (Conversations):** 0 (Must be 0)

## Split Overview
| Split | Examples | % of Total | Unique Conversations |
|---|---|---|---|
| Train | 7580 | 70.1% | 7580 |
| Validation | 1616 | 14.9% | 1616 |
| Test | 1616 | 14.9% | 1616 |

## Intent Distribution per Split
| Intent | Train | Validation | Test |
|---|---|---|---|
| CONNECTIVITY_AND_ERRORS | 1088 | 232 | 232 |
| DIGITAL_ACCESS_AND_DOWNLOAD | 801 | 171 | 171 |
| EXPLOIT_AND_HACKER_REPORT | 282 | 60 | 60 |
| FEEDBACK_AND_COMPLAINTS | 871 | 186 | 186 |
| GAMEPLAY_BUG_REPORT | 962 | 205 | 205 |
| INFORMATION_AND_OTHER_REQUESTS | 1128 | 241 | 241 |
| LOW_FREQUENCY_SPECIAL_CASE | 116 | 24 | 24 |
| MATCHMAKING_AND_LOBBIES | 1019 | 217 | 217 |
| PROGRESSION_AND_REWARDS | 1276 | 273 | 273 |
| PURCHASE_AND_BILLING | 37 | 7 | 7 |

## Risk & Assignment Methods
- **LOW_FREQUENCY_SPECIAL_CASE (Train/Val/Test):** 116 / 24 / 24
- **Examples with Risk Flags (Train/Val/Test):** 457 / 94 / 92
