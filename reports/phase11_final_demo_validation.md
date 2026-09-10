# Phase 11 Final Demo Validation

This report captures the final behavior of the TrustSupport system for the primary recruiter demo scenarios.

## Technical Support
**Query**: `My game keeps crashing when I launch it.`

- **Intent**: INFORMATION_AND_OTHER_REQUESTS (Confidence: 1.00)
- **Risk Status**: None
- **Reply Mode**: GROUNDED_REPLY
- **Maximum Similarity**: 0.77
- **Evidence Count**: 3
- **Generation Source**: TEMPLATE
- **Safety Result**: PASSED
- **Final Behavior**: 

> I understand you're experiencing an issue related to Information And Other Requests. Based on similar support cases, you can try the following:

@619546 Hi there, please try to verify your game cache and then restart the system. ^RK

If the issue continues, please contact support.

**Top Cleaned Evidence:**
- **Sim 0.77**: Hi there, please try to verify your game cache and then restart the system.
- **Sim 0.76**: Hi Chris, in order to properly assist you with this please send us a DM with your GT, console and if possible a video.
- **Sim 0.72**: Hi. Go ahead and try all the steps shown here: https://t.co/ebxKYFORYD

## Rewards
**Query**: `I completed the challenge but didn't receive my reward.`

- **Intent**: PROGRESSION_AND_REWARDS (Confidence: 1.00)
- **Risk Status**: None
- **Reply Mode**: GROUNDED_REPLY
- **Maximum Similarity**: 0.82
- **Evidence Count**: 3
- **Generation Source**: TEMPLATE
- **Safety Result**: PASSED
- **Final Behavior**: 

> I understand you're experiencing an issue related to Progression And Rewards. Based on similar support cases, you can try the following:

@680653 Hi there, Sorry to hear the reward is stuck. Please try clearing cache:  and rechecking. Thanks! ^TE

If the issue continues, please contact support.

**Top Cleaned Evidence:**
- **Sim 0.82**: Hi there, Sorry to hear the reward is stuck. Please try clearing cache: https://t.co/WvlDqqYZ33 and rechecking. Thanks!
- **Sim 0.79**: Hey there! Do you happen to have a screenshot of the completed challenge?
- **Sim 0.78**: Hi there, sorry for the dealy. Send me a DM so I can help you on it. ^BW https://t.co/c9WoAfwenP

## Ban Appeal
**Query**: `I was banned for no reason.`

- **Intent**: LOW_FREQUENCY_SPECIAL_CASE (Confidence: 1.00)
- **Risk Status**: BAN_APPEAL
- **Reply Mode**: ESCALATE
- **Maximum Similarity**: 0.71
- **Evidence Count**: 3
- **Generation Source**: TEMPLATE
- **Safety Result**: PASSED
- **Final Behavior**: 

> We cannot discuss enforcement actions on social media. Please refer to the Security and Enforcement Policy page.

**Top Cleaned Evidence:**
- **Sim 0.71**: Please send us a DM along with your platform and gamertag. ^JW https://t.co/c9WoAfwenP
- **Sim 0.69**: All bans are final and can not be reverted or overturned by the studio.
- **Sim 0.67**: Could you please provide me with your gamertag and cod email?

## Account Security
**Query**: `Someone hacked my account.`

- **Intent**: LOW_FREQUENCY_SPECIAL_CASE (Confidence: 0.80)
- **Risk Status**: ACCOUNT_COMPROMISED
- **Reply Mode**: ESCALATE
- **Maximum Similarity**: 0.78
- **Evidence Count**: 3
- **Generation Source**: TEMPLATE
- **Safety Result**: PASSED
- **Final Behavior**: 

> Please submit a support ticket via the official portal for further assistance with this issue.

**Top Cleaned Evidence:**
- **Sim 0.78**: Can you DM me so we can troubleshoot this further with you. Thanks! ^CB https://t.co/c9WoAfwenP
- **Sim 0.67**: Hey Aaron, feel free to send me a PM for further assistance. Thanks. ^MF https://t.co/c9WoAfwenP
- **Sim 0.63**: Hello! Sorry for the delay, please provide us more details including gamer tag, console and screenshots to help you via DM. ^ME https://t.co/c9WoAfwenP

## Game Integrity
**Query**: `This player is using an aimbot.`

- **Intent**: GAMEPLAY_BUG_REPORT (Confidence: 0.37)
- **Risk Status**: GAME_INTEGRITY
- **Reply Mode**: CAUTIOUS_REPLY
- **Maximum Similarity**: 0.69
- **Evidence Count**: 3
- **Generation Source**: TEMPLATE
- **Safety Result**: PASSED
- **Final Behavior**: 

> Thank you for the report. To maintain game integrity, please use the in-game reporting tools or visit our Security and Enforcement page to submit a formal report.

**Top Cleaned Evidence:**
- **Sim 0.69**: Please report all cheaters using the feature available. The security team looks over all reports made that way.
- **Sim 0.59**: Hi, please report all cheaters/hackers in game.
- **Sim 0.59**: Commander Officer on service, Our specialist are investigating this players,  but keep reporting them and let us know

## Out-of-Domain
**Query**: `How do I cook pasta?`

- **Intent**: UNKNOWN (Confidence: 0.07)
- **Risk Status**: None
- **Reply Mode**: ABSTAIN
- **Maximum Similarity**: 0.00
- **Evidence Count**: 0
- **Generation Source**: TEMPLATE
- **Safety Result**: PASSED
- **Final Behavior**: 

> I don't have enough specific information to solve this right now. Please reach out to our team at support.activision.com for further assistance.

