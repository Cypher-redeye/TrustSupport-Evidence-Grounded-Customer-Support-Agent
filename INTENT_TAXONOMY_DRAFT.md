# INTENT TAXONOMY (DRAFT)

Based on the operational analysis of K-Means clustering (K=10) on ATVIAssist customer requests and subsequent full-dataset accounting, the following data-driven taxonomy is proposed.

## Proposed Intents

### 1. CONNECTIVITY_AND_ERRORS
**Description**: Customer is experiencing server outages, specific error codes, or getting disconnected mid-match.
**Typical Routing**: AUTO_HANDLE

### 2. PROGRESSION_AND_REWARDS
**Description**: Customer is missing earned items, supply drops, unlock tokens, or contracts are bugged/resetting.
**Typical Routing**: ESCALATE

### 3. DIGITAL_ACCESS_AND_DOWNLOAD
**Description**: Customer cannot download the game, DLC, or pre-order bonuses. (Access rights, installation, and codes).
**Typical Routing**: AUTO_HANDLE

### 4. PURCHASE_AND_BILLING
**Description**: Customer is experiencing monetary transaction issues.
**Typical Routing**: ESCALATE
**Risk Flags**: `PAYMENT`

### 5. MATCHMAKING_AND_LOBBIES
**Description**: Customer cannot find a match, headquarters is empty, or party functionality is broken.
**Typical Routing**: AUTO_HANDLE

### 6. EXPLOIT_AND_HACKER_REPORT
**Description**: Customer is reporting a player cheating, boosting, or exploiting a map glitch.
**Typical Routing**: AUTO_HANDLE
**Risk Flags**: `GAME_INTEGRITY`

### 7. GAMEPLAY_BUG_REPORT
**Description**: Customer is reporting a non-exploitative bug affecting gameplay.
**Typical Routing**: AUTO_HANDLE

### 8. FEEDBACK_AND_COMPLAINTS
**Description**: General frustration, game balance complaints, or non-actionable venting.
**Typical Routing**: AUTO_HANDLE_ACKNOWLEDGEMENT
**Risk Flags**: `HIGH_EMOTION`

### 9. INFORMATION_AND_OTHER_REQUESTS
**Description**: General inquiries, hardware compatibility questions, or multi-issue requests lacking a specific cluster definition.
**Typical Routing**: AUTO_HANDLE (via KB Retrieval)

### 10. LOW_FREQUENCY_SPECIAL_CASE
**Description**: High-risk, low-frequency cases (e.g., Ban appeals, hacked accounts, stats resets, legal threats). These are semantically distinct but too rare (< 2% combined) to support individual classification intents. They are routed purely via their specific risk flags.
**Typical Routing**: ESCALATE
**Risk Flags**: `BAN_APPEAL`, `ACCOUNT_COMPROMISED`, `PROGRESSION_DATA_LOSS`, `LEGAL_THREAT`
