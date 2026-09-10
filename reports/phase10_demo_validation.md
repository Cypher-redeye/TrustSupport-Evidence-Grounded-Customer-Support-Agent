# Phase 10 Demo Validation

## Normal Support
- **Query**: `My game keeps crashing when I launch it.`
- **Predicted Intent**: `INFORMATION_AND_OTHER_REQUESTS`
- **Confidence**: `1.00`
- **Risk Flags**: `[]`
- **Reply Mode**: `GROUNDED_REPLY`
- **Evidence Availability**: `Yes`
- **Maximum Similarity**: `0.77`
- **Generation Source**: `TEMPLATE`
- **Safety Result**: `Passed`
- **Final Behavior**: `GROUNDED_REPLY executed gracefully.`

## Rewards
- **Query**: `I completed the challenge but didn't receive my reward.`
- **Predicted Intent**: `PROGRESSION_AND_REWARDS`
- **Confidence**: `1.00`
- **Risk Flags**: `[]`
- **Reply Mode**: `GROUNDED_REPLY`
- **Evidence Availability**: `Yes`
- **Maximum Similarity**: `0.82`
- **Generation Source**: `TEMPLATE`
- **Safety Result**: `Passed`
- **Final Behavior**: `GROUNDED_REPLY executed gracefully.`

## Ban Appeal
- **Query**: `I was banned for no reason.`
- **Predicted Intent**: `LOW_FREQUENCY_SPECIAL_CASE`
- **Confidence**: `1.00`
- **Risk Flags**: `['BAN_APPEAL']`
- **Reply Mode**: `ESCALATE`
- **Evidence Availability**: `Yes`
- **Maximum Similarity**: `0.71`
- **Generation Source**: `TEMPLATE`
- **Safety Result**: `Passed`
- **Final Behavior**: `ESCALATE executed gracefully.`

## Account Security
- **Query**: `Someone hacked my account.`
- **Predicted Intent**: `LOW_FREQUENCY_SPECIAL_CASE`
- **Confidence**: `0.80`
- **Risk Flags**: `['ACCOUNT_COMPROMISED']`
- **Reply Mode**: `ESCALATE`
- **Evidence Availability**: `Yes`
- **Maximum Similarity**: `0.78`
- **Generation Source**: `TEMPLATE`
- **Safety Result**: `Passed`
- **Final Behavior**: `ESCALATE executed gracefully.`

## Game Integrity
- **Query**: `This player is using an aimbot.`
- **Predicted Intent**: `GAMEPLAY_BUG_REPORT`
- **Confidence**: `0.37`
- **Risk Flags**: `['GAME_INTEGRITY']`
- **Reply Mode**: `CAUTIOUS_REPLY`
- **Evidence Availability**: `Yes`
- **Maximum Similarity**: `0.69`
- **Generation Source**: `TEMPLATE`
- **Safety Result**: `Passed`
- **Final Behavior**: `CAUTIOUS_REPLY executed gracefully.`

## Out-of-Domain
- **Query**: `How do I cook pasta?`
- **Predicted Intent**: `UNKNOWN`
- **Confidence**: `0.07`
- **Risk Flags**: `[]`
- **Reply Mode**: `ABSTAIN`
- **Evidence Availability**: `No`
- **Maximum Similarity**: `0.00`
- **Generation Source**: `TEMPLATE`
- **Safety Result**: `Passed`
- **Final Behavior**: `ABSTAIN executed gracefully.`

