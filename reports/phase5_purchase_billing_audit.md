# Phase 5: PURCHASE_AND_BILLING Discrepancy Audit

## 1. Phase 4 Reported/Estimated Count
In Phase 4, `src/intents/analyze_subclusters.py` reported **421** examples for "Payment/Purchase/Transactions". 

## 2. Final Phase 5 Deterministic Count
In Phase 5, the final dataset generated exactly **18** examples assigned to `PURCHASE_AND_BILLING`.

## 3. Exact Labeling Rules Currently Used
**In Phase 4 (`analyze_subclusters.py`)**: 
The count of 421 was generated using a broad dataset-wide regex:
`r'\b(buy|bought|purchased|payment|charged|refund|money back|dollars|store)\b'`

**In Phase 5 (`build_labeled_dataset.py`)**:
The rules were significantly tightened and constrained by cluster geometry. 
1. The regex was shortened to: `r'\b(payment|charged|refund|money back|dollars)\b'` (dropping `buy`, `bought`, `purchased`, `store`).
2. The assignment was constrained to **only trigger if the point was in K-Means Cluster 2**.

```python
if c_id == 2:
    if 'PAYMENT' in flags:
        intent_assignments[req_id] = 'PURCHASE_AND_BILLING'
```
This intersection (Cluster 2 AND restricted regex) is why the count dropped from 421 to 18.

## 4. Number of Examples Matching Each Keyword
Across the entire 10,812 dataset:
- bought: 173
- money: 108
- buy: 84
- store: 71
- refund: 47
- purchase: 30
- dollars: 16
- charged: 5
- payment: 3

## 5 & 6. At least 20 Actual Examples Matching Broad Billing/Payment Concepts

### Example 1
- **request_id**: req_conv_1092121
- **conversation_id**: conv_1092121
- **text**: @ATVIAssist you removed the original bo3 from the ps store so I can't download it even though I bought it, I have to pay 63$ for chronicles
- **Phase 5 assigned intent**: DIGITAL_ACCESS_AND_DOWNLOAD
- **assignment_method**: RULE_ASSISTED_SPLIT
- **risk_flags**: []

### Example 2
- **request_id**: req_conv_2206245
- **conversation_id**: conv_2206245
- **text**: @ATVIAssist can I buy the ww2 soundtrack?
- **Phase 5 assigned intent**: DIGITAL_ACCESS_AND_DOWNLOAD
- **assignment_method**: RULE_ASSISTED_SPLIT
- **risk_flags**: []

### Example 3
- **request_id**: req_conv_1286088
- **conversation_id**: conv_1286088
- **text**: @XboxSupport @115765 bought cod WW2 digital on xb1. I file share with my brother. He can already preload the game but I can’t @XboxSupport @115765 Just curious if that is just for people with slower internet that will take a few days to install or what. Not a huge deal. Just curious
- **Phase 5 assigned intent**: DIGITAL_ACCESS_AND_DOWNLOAD
- **assignment_method**: RULE_ASSISTED_SPLIT
- **risk_flags**: []

### Example 4
- **request_id**: req_conv_1283324
- **conversation_id**: conv_1283324
- **text**: @ATVIAssist hi there. Pre-Ordered COD WW2 on the PlayStation Store but cannot find the WW2 theme? Please advise.
- **Phase 5 assigned intent**: DIGITAL_ACCESS_AND_DOWNLOAD
- **assignment_method**: RULE_ASSISTED_SPLIT
- **risk_flags**: []

### Example 5
- **request_id**: req_conv_2668427
- **conversation_id**: conv_2668427
- **text**: @ATVIAssist  tell me why i spent 60 dollars on your game and it runs like fucking shit. Every fucking game lags out. How are you going to sell people a broken fucking game.
- **Phase 5 assigned intent**: INFORMATION_AND_OTHER_REQUESTS
- **assignment_method**: DIRECT_CLUSTER_MAPPING
- **risk_flags**: ['PAYMENT']

### Example 6
- **request_id**: req_conv_1398673
- **conversation_id**: conv_1398673
- **text**: @ATVIAssist so I bought some cod points on black ops 3 but I don’t have them. HELP????
- **Phase 5 assigned intent**: MATCHMAKING_AND_LOBBIES
- **assignment_method**: DIRECT_CLUSTER_MAPPING
- **risk_flags**: []

### Example 7
- **request_id**: req_conv_804381
- **conversation_id**: conv_804381
- **text**: @ATVIAssist Last time
I ever buy season pass I'm
Litterally looking at people playing it on my friendlist this is bs!
- **Phase 5 assigned intent**: DIGITAL_ACCESS_AND_DOWNLOAD
- **assignment_method**: RULE_ASSISTED_SPLIT
- **risk_flags**: []

### Example 8
- **request_id**: req_conv_868709
- **conversation_id**: conv_868709
- **text**: @ATVIAssist I want a refund I am a season pass holder for iw and I got charged 15$ so I want my money back
- **Phase 5 assigned intent**: PROGRESSION_AND_REWARDS
- **assignment_method**: DIRECT_CLUSTER_MAPPING
- **risk_flags**: ['PAYMENT']

### Example 9
- **request_id**: req_conv_4496
- **conversation_id**: conv_4496
- **text**: @ATVIAssist I purchased and down loaded the Variety Map Pack but didn't get my 10 rare supply drops from Lion Strike. Help? https://t.co/A22ReiMUIA
- **Phase 5 assigned intent**: PROGRESSION_AND_REWARDS
- **assignment_method**: DIRECT_CLUSTER_MAPPING
- **risk_flags**: []

### Example 10
- **request_id**: req_conv_87704
- **conversation_id**: conv_87704
- **text**: @ATVIAssist it seems I’ve bought some cod points Ealier this morning! For WW2 but I haven’t received them yet. Not even the co formation email
- **Phase 5 assigned intent**: MATCHMAKING_AND_LOBBIES
- **assignment_method**: DIRECT_CLUSTER_MAPPING
- **risk_flags**: []

### Example 11
- **request_id**: req_conv_1725532
- **conversation_id**: conv_1725532
- **text**: @ATVIAssist some free bonus material sounds like it’s in store @521872 @ATVIAssist I second this!! I just want to play my new vidgi games
- **Phase 5 assigned intent**: DIGITAL_ACCESS_AND_DOWNLOAD
- **assignment_method**: RULE_ASSISTED_SPLIT
- **risk_flags**: []

### Example 12
- **request_id**: req_conv_336925
- **conversation_id**: conv_336925
- **text**: @ATVIAssist I need help I bought cod points but theyre not on my account
- **Phase 5 assigned intent**: PROGRESSION_AND_REWARDS
- **assignment_method**: DIRECT_CLUSTER_MAPPING
- **risk_flags**: []

### Example 13
- **request_id**: req_conv_2481406
- **conversation_id**: conv_2481406
- **text**: @ATVIAssist I bought the digital deluxe version from gameStop I entered code to download. Website went down now it says code already redeem
- **Phase 5 assigned intent**: DIGITAL_ACCESS_AND_DOWNLOAD
- **assignment_method**: RULE_ASSISTED_SPLIT
- **risk_flags**: []

### Example 14
- **request_id**: req_conv_792411
- **conversation_id**: conv_792411
- **text**: @115890 @135958 @ATVIAssist what is going on with Infinite Warfare DLC 4 please fix this download issue this is un-exceptable @308953 @115890 @135958 @ATVIAssist I am a season pass holder and it still isn’t working for me when will the update be out @308275 @115890 @135958 @ATVIAssist Same as me i own the season pass and it is making me buy the DLC in order to play
- **Phase 5 assigned intent**: DIGITAL_ACCESS_AND_DOWNLOAD
- **assignment_method**: RULE_ASSISTED_SPLIT
- **risk_flags**: []

### Example 15
- **request_id**: req_conv_1087839
- **conversation_id**: conv_1087839
- **text**: @122172 I ain’t trying to buy Ghosts for $60, help me out 🤔
- **Phase 5 assigned intent**: DIGITAL_ACCESS_AND_DOWNLOAD
- **assignment_method**: RULE_ASSISTED_SPLIT
- **risk_flags**: []

### Example 16
- **request_id**: req_conv_1518955
- **conversation_id**: conv_1518955
- **text**: @ATVIAssist why can't I get my camo or anything else I bought from the $100 copy of #ww2?
- **Phase 5 assigned intent**: MATCHMAKING_AND_LOBBIES
- **assignment_method**: DIRECT_CLUSTER_MAPPING
- **risk_flags**: []

### Example 17
- **request_id**: req_conv_2270344
- **conversation_id**: conv_2270344
- **text**: @ATVIAssist Hi, I have purchased Destiny 2 via the Blizzard bnet app. Will I be able to upgrade/purchase an expansion pass later? 👀
- **Phase 5 assigned intent**: DIGITAL_ACCESS_AND_DOWNLOAD
- **assignment_method**: RULE_ASSISTED_SPLIT
- **risk_flags**: []

### Example 18
- **request_id**: req_conv_2724883
- **conversation_id**: conv_2724883
- **text**: @ATVIAssist Do you guys have an ETA on the post match issue? I'm still experiencing this on the ps4 when I'm not hosting the party. Bought the game digital from the Playstation store if that matters.
- **Phase 5 assigned intent**: INFORMATION_AND_OTHER_REQUESTS
- **assignment_method**: DIRECT_CLUSTER_MAPPING
- **risk_flags**: []

### Example 19
- **request_id**: req_conv_1556550
- **conversation_id**: conv_1556550
- **text**: @ATVIAssist I bought the game on my PS4 and it says preload now but it’s not preloading? And I can’t seem to find where to start it? @ATVIAssist WWII
- **Phase 5 assigned intent**: DIGITAL_ACCESS_AND_DOWNLOAD
- **assignment_method**: RULE_ASSISTED_SPLIT
- **risk_flags**: []

### Example 20
- **request_id**: req_conv_811195
- **conversation_id**: conv_811195
- **text**: @ATVIAssist @115754 @115766 @115786 @XboxSupport This is not good for business. I dump hundreds of dollars for this game. #NoMore https://t.co/R3npgIbfi0
- **Phase 5 assigned intent**: FEEDBACK_AND_COMPLAINTS
- **assignment_method**: DIRECT_CLUSTER_MAPPING
- **risk_flags**: ['PAYMENT']

## 7. Where are these broad matches currently being assigned?
The 421 broad matches from the entire dataset were distributed across the following intents in Phase 5:
- DIGITAL_ACCESS_AND_DOWNLOAD: 132
- PROGRESSION_AND_REWARDS: 97
- MATCHMAKING_AND_LOBBIES: 84
- CONNECTIVITY_AND_ERRORS: 41
- INFORMATION_AND_OTHER_REQUESTS: 25
- PURCHASE_AND_BILLING: 18
- GAMEPLAY_BUG_REPORT: 13
- FEEDBACK_AND_COMPLAINTS: 8
- LOW_FREQUENCY_SPECIAL_CASE: 3

## 8. Was the Phase 4 estimate documented as an estimate?
Yes. The Phase 4 `INTENT_TAXONOMY_DRAFT.md` explicitly noted:
`*(Note: Estimated counts derived from raw cluster sizes and keyword extrapolation).*`
However, the degree to which `PURCHASE_AND_BILLING` was extrapolated across the entire dataset vs restricted to Cluster 2 was the primary source of the divergence.

## 9. Do all 10,812 requests still have exactly one valid intent?
Yes. As verified in Step 1, all 10,812 requests were mapped 1:1 to exactly one intent without duplication or missing examples.
