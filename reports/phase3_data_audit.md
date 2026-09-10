# Phase 3 Data Audit: ATVIAssist

## Metric Discrepancy Documentation
**Phase 2 Multi-turn Ratio: ~0.67 vs Phase 3 Exact Multi-turn Ratio: ~0.43**

- **Phase 2 Methodology:** Used a high-level, single-pass heuristic. A conversation was assumed to be 'multi-turn' if a brand tweet was in response to *any* other tweet, and the total conversation volume was estimated by grouping `@mentions` via simple regexes.
- **Phase 3 Methodology:** Uses exact, multi-pass graph reconstruction. Every edge (`in_response_to_tweet_id` and `response_tweet_id`) is strictly followed and cross-validated. A multi-turn conversation requires a verified `Customer -> Brand -> Customer` path.
- **Why Phase 3 is More Trustworthy:** It eliminates false positives caused by isolated tweets, misattributions, or simple heuristic counting errors. The Phase 2 values were intended merely for sorting/ranking candidate brands at scale and must not be used as final analytical metrics.

## Customer Message Counts
- **Total relevant tweets in ATVIAssist graph:** 48351
- **Total customer-authored tweets:** 30701
- **Total inbound customer tweets:** 30521
- **Customer tweets included in reconstructed conversations:** 30701
- **Customer tweets excluded from reconstructed conversations (orphans):** 0

## Conversation Completeness
- **Total Conversations:** 11113
- **Complete conversations (multi-turn):** 4726
- **Partial conversations (single-turn/broken):** 6387
- **Orphaned tweets:** 0
- **Conversations with missing parent:** 71
- **Conversations with missing child:** 672
- **Instances excluded due to cycle detection:** 0

## Depth & Multi-turn
- **Average conversation depth:** 3.20
- **Median conversation depth:** 2
- **Maximum conversation depth:** 32
- **Exact multi-turn ratio:** 0.43

## 20 Randomly Sampled Conversations
> *Note: These are actual, non-synthetic conversational threads extracted directly from the reconstructed graph data using deterministic IDs.*

### conv_2249586
| Turn (Depth) | Tweet ID | Author | Inbound | Parent Tweet | Child Tweet(s) | Text |
|---|---|---|---|---|---|---|
| 0 | 2249586 | 655475 | True |  | 2249584,2249587 | @ATVIAssist when can I have my xp back guys? Been waiting 2 weeks for a reply from one of your team |
| 1 | 2249584 | ATVIAssist | False | 2249586 | 2249585 | @655475 ...sure you keep us posted. Thank you. ^RN |
| 1 | 2249587 | ATVIAssist | False | 2249586 |  | @655475 Hello there, I apologize for the delay. How can I assist you today? Can you clarify your current issue? Please be....^RN |
| 2 | 2249585 | 655475 | True | 2249584 |  | @ATVIAssist Do you want me to Dm you the issue? I was deranked on launch but still haven’t been able to contact you.. |

### conv_2710450
| Turn (Depth) | Tweet ID | Author | Inbound | Parent Tweet | Child Tweet(s) | Text |
|---|---|---|---|---|---|---|
| 0 | 2710450 | 761060 | True |  | 2710449 | @115766 fix your shitty servers I’m tired of lagging out |
| 1 | 2710449 | ATVIAssist | False | 2710450 |  | @761060 Are you on a wired or wireless connection? Can you hard reset your router and modem and try logging back in? ^EC |

### conv_1629021
| Turn (Depth) | Tweet ID | Author | Inbound | Parent Tweet | Child Tweet(s) | Text |
|---|---|---|---|---|---|---|
| 0 | 1629021 | 498662 | True |  | 1629020 | Get ur fucking servers fixed @ATVIAssist |
| 1 | 1629020 | ATVIAssist | False | 1629021 |  | @498662 Hi! Some players are experiencing connectivity issues. We're actively looking into getting this resolved. Stay tuned. ^FB |

### conv_1605167
| Turn (Depth) | Tweet ID | Author | Inbound | Parent Tweet | Child Tweet(s) | Text |
|---|---|---|---|---|---|---|
| 0 | 1605167 | 184826 | True |  | 1605166 | @ATVIAssist guys any chance you could help me, im having an issue with my progression on #CODWWII |
| 1 | 1605166 | ATVIAssist | False | 1605167 |  | @184826 Hi there, please send us a DM for further assistance. ^RK https://t.co/c9WoAfwenP |

### conv_2419443
| Turn (Depth) | Tweet ID | Author | Inbound | Parent Tweet | Child Tweet(s) | Text |
|---|---|---|---|---|---|---|
| 0 | 2419443 | 695082 | True |  | 2419441,2419446 | @ATVIAssist I preordered COD WW2 &amp; am unable access https://t.co/t2Np4Nd6dj to follow steps on back of the pre-order card #504GatewayTimeout |
| 1 | 2419441 | ATVIAssist | False | 2419443 | 2419442 | @695082 ... 2 should help. ^RN |
| 1 | 2419446 | ATVIAssist | False | 2419443 |  | @695082 Hello there, I apologize for the delay. Please make sure you refer here for more info: https://t.co/cm1idGIcwG.  Number...^RN |
| 2 | 2419442 | 695082 | True | 2419441 | 2419444 | @ATVIAssist It says my code was already redeemed.  I didn't get any notifications of it being redeemed last night.  I also didn't get an email.. #Help |
| 3 | 2419444 | ATVIAssist | False | 2419442 | 2419445 | @695082 Have you been able to redeem the code before? Can you clarify where you received your code? Please let us know. ^RN |
| 4 | 2419445 | 695082 | True | 2419444 |  | @ATVIAssist Last night I got 504 timeout error and it never said successful. This morning it said it was redeemed I got it from Target yesterday |

### conv_504091
| Turn (Depth) | Tweet ID | Author | Inbound | Parent Tweet | Child Tweet(s) | Text |
|---|---|---|---|---|---|---|
| 0 | 504091 | 235501 | True |  | 504090 | @ATVIAssist I am problem clean out my mail in headguaters |
| 1 | 504090 | ATVIAssist | False | 504091 |  | @235501  Hello there, I apologize for the delay. Are you currently in need of assistance? Please be make sure you keep us updated. Thank you. ^RN |

### conv_2523113
| Turn (Depth) | Tweet ID | Author | Inbound | Parent Tweet | Child Tweet(s) | Text |
|---|---|---|---|---|---|---|
| 0 | 2523113 | 718553 | True |  | 2523112 | @ATVIAssist Appreciate the hard work addressing issues. It’s tough job. I think everyone needs to be patient. Great game though! #CODWWII |
| 1 | 2523112 | ATVIAssist | False | 2523113 |  | @718553 Thank you! We appreciate your support, if you ever have any questions feel free to reach back out to us. ^EC |

### conv_572804
| Turn (Depth) | Tweet ID | Author | Inbound | Parent Tweet | Child Tweet(s) | Text |
|---|---|---|---|---|---|---|
| 0 | 572804 | 254605 | True |  | 572803 | @ATVIAssist Sooooooo we just leaving headquarters empty or what? |
| 1 | 572803 | ATVIAssist | False | 572804 | 572802 | @254605 Apologies for the delay, things should be cleared up with the latest patch- are you still seeing this? ^NM |
| 2 | 572802 | 254605 | True | 572803 | 572801 | @ATVIAssist Nah we good days later |
| 3 | 572801 | ATVIAssist | False | 572802 |  | @254605 Glad to hear that! Let us know if you run into any other issues ^NM |

### conv_2353242
| Turn (Depth) | Tweet ID | Author | Inbound | Parent Tweet | Child Tweet(s) | Text |
|---|---|---|---|---|---|---|
| 0 | 2353242 | 680005 | True |  | 2353241 | @ATVIAssist Keep getting kicked out of local splitscreen zombies and getting "request command not received" error. This happened multiple times and it's really frustrating playing for 2 hours and getting kicked out like that. Also can't find any mp match on xbox one. |
| 1 | 2353241 | ATVIAssist | False | 2353242 |  | @680005 Hey there, can you please send me a message via DM? More than happy to help. ^EX https://t.co/c9WoAfwenP |

### conv_1504998
| Turn (Depth) | Tweet ID | Author | Inbound | Parent Tweet | Child Tweet(s) | Text |
|---|---|---|---|---|---|---|
| 0 | 1504998 | 469288 | True |  | 1504996 | @ATVIAssist Hi ! I am Having an issue With WW2 on ps4 . The Game says i have new items in the emblems but i cannot find it ! https://t.co/5UInA9j8e4 |
| 1 | 1504996 | ATVIAssist | False | 1504998 | 1504997 | @469288 Hello Zekyn, are you still unable to find the new emblems?   ^DA |
| 2 | 1504997 | 469288 | True | 1504996 | 1504999 | @ATVIAssist Yes , still cannot find it ! Any solutions ? |
| 3 | 1504999 | 469288 | True | 1504997 |  | @ATVIAssist I Also have this multiplayer upgrade that i cannot take ! I press X but nothing happens https://t.co/Oc8eTPgWDQ |

### conv_1291623
| Turn (Depth) | Tweet ID | Author | Inbound | Parent Tweet | Child Tweet(s) | Text |
|---|---|---|---|---|---|---|
| 0 | 1291623 | 314543 | True |  | 1291622 | https://t.co/A3dCkM2cGr |
| 1 | 1291622 | 314543 | True | 1291623 | 1291621 | @ATVIAssist |
| 2 | 1291621 | ATVIAssist | False | 1291622 |  | @314543 Can you send us the prove on a DM https://t.co/c9WoAfwenP. if it is a video have to be on youtube. ^BW |

### conv_1730944
| Turn (Depth) | Tweet ID | Author | Inbound | Parent Tweet | Child Tweet(s) | Text |
|---|---|---|---|---|---|---|
| 0 | 1730944 | 523013 | True |  | 1730942 | @ATVIAssist any update on double xp not working for cod ww2. tried reaching out two other times |
| 1 | 1730942 | ATVIAssist | False | 1730944 | 1730943 | @523013 Hello Soldier, can you please clear cache and head to the HQ and verify the tiems on your mail and let us know ^JR |
| 2 | 1730943 | 523014 | True | 1730942 | 1730945 | @ATVIAssist @523013 How do you clear cache? |
| 3 | 1730945 | 523015 | True | 1730943 | 1730946 | @523014 @ATVIAssist @523013 what console you on ? |
| 4 | 1730946 | 523014 | True | 1730945 | 1730947 | @523015 @ATVIAssist @523013 Ps4 |
| 5 | 1730947 | 523015 | True | 1730946 | 1730948 | @523014 https://t.co/fIQSjBmLTL AC |
| 6 | 1730948 | 523014 | True | 1730947 |  | @523015 Thanks |

### conv_790486
| Turn (Depth) | Tweet ID | Author | Inbound | Parent Tweet | Child Tweet(s) | Text |
|---|---|---|---|---|---|---|
| 0 | 790486 | 308502 | True |  | 790487,790485 | Hi @ATVIAssist on the xbox one I have the season pass for infinite warfare and cannot download dlc4 as it says I have to pay. |
| 1 | 790485 | 308503 | True | 790486 | 790482 | @308502 @ATVIAssist Same |
| 2 | 790482 | 308502 | True | 790485 | 790483,790481,790484 | @308503 @ATVIAssist I ended up buying it :( |
| 3 | 790481 | ATVIAssist | False | 790482 |  | @308502 ...this may have caused. Please stay tuned for updates. ^FB |
| 3 | 790484 | ATVIAssist | False | 790482 | 790491 | @308502 Hi, we're aware of this issue and it is currently being looked into. Sorry for any frustrations and inconvenience... ^FB |
| 4 | 790491 | 308275 | True | 790484 |  | @ATVIAssist @308502 There is a lot of Inconvenience |

### conv_443987
| Turn (Depth) | Tweet ID | Author | Inbound | Parent Tweet | Child Tweet(s) | Text |
|---|---|---|---|---|---|---|
| 0 | 443987 | 220179 | True |  | 443984 | Yo @115765  fix the glitch on pointe du hoc where ppl can get In the wall |
| 1 | 443984 | ATVIAssist | False | 443987 | 443985,443986 | @220179 SHG is working on this now, be sure to report any glitchers you see in-game, the ban hammer will clear 'em out! ^NM |
| 2 | 443985 | 220180 | True | 443984 |  | @ATVIAssist I Still Receive Error Code 5 And 1 When I Try To Login To Multiplayer |
| 2 | 443986 | 220181 | True | 443984 |  | @ATVIAssist solve the error code 1, 3 and 5, i cant play WWII MP! HELP |

### conv_483514
| Turn (Depth) | Tweet ID | Author | Inbound | Parent Tweet | Child Tweet(s) | Text |
|---|---|---|---|---|---|---|
| 0 | 483514 | 230027 | True |  | 483513 | @ATVIAssist unban |
| 1 | 483513 | ATVIAssist | False | 483514 |  | @230027  Hey there. Please send us a DM along with your platform and gamertag. I'll be happy to help you out with this. ^JW https://t.co/c9WoAfwenP |

### conv_482239
| Turn (Depth) | Tweet ID | Author | Inbound | Parent Tweet | Child Tweet(s) | Text |
|---|---|---|---|---|---|---|
| 0 | 482239 | 229677 | True |  | 482237 | So I was using the panzerschreck in a game and I got kicked and got this message. No idea what this means. @115766 @115765 @ATVIAssist #CODWWII https://t.co/ZqhXhh1ifq |
| 1 | 482237 | ATVIAssist | False | 482239 | 482238 | @229677 Hey. What's your region, gamertag and does this only appear when playing hardcore matches? ^SM |
| 2 | 482238 | 229677 | True | 482237 |  | @ATVIAssist I'm in North America on XB1. My gamertag is Z BOSS 01. This has only happened to me when playing hardcore |

### conv_944030
| Turn (Depth) | Tweet ID | Author | Inbound | Parent Tweet | Child Tweet(s) | Text |
|---|---|---|---|---|---|---|
| 0 | 944030 | 343840 | True |  | 944029 | @122172 is there any support for the Call of Duty Modern Warfare 3 yet? |
| 1 | 944029 | ATVIAssist | False | 944030 |  | @343840 Hi there, pardon my delay. What can I help you with in this title? Could you tell me more via DM? ^AM https://t.co/c9WoAfwenP |

### conv_1797172
| Turn (Depth) | Tweet ID | Author | Inbound | Parent Tweet | Child Tweet(s) | Text |
|---|---|---|---|---|---|---|
| 0 | 1797172 | 540002 | True |  | 1797171 | @115758 how about fixing your shitty game and give me my money back, lost 6 dollars trying to get cod points |
| 1 | 1797171 | ATVIAssist | False | 1797172 |  | @540002 Hi there, Sounds like you had troubles with a CoD Point purchase? Shoot over a DM let's troubleshoot. ^TE https://t.co/c9WoAfwenP |

### conv_2702899
| Turn (Depth) | Tweet ID | Author | Inbound | Parent Tweet | Child Tweet(s) | Text |
|---|---|---|---|---|---|---|
| 0 | 2702899 | 759196 | True |  | 2702898 | @ATVIAssist @115754 @115766 Just found a dude on PSN glitching out of the map Pointe Du Hoc on WWII. Kinda ruined the game. His PSN is sum1002 https://t.co/QxobkKcFFF |
| 1 | 2702898 | ATVIAssist | False | 2702899 |  | @759196 Hey there! We are currently aware of this issue and looking into it. Please report him with the reporting tool. ^MB |

### conv_1729828
| Turn (Depth) | Tweet ID | Author | Inbound | Parent Tweet | Child Tweet(s) | Text |
|---|---|---|---|---|---|---|
| 0 | 1729828 | 522794 | True |  | 1729826 | broke ass game @115766 @ATVIAssist @115765 |
| 1 | 1729826 | ATVIAssist | False | 1729828 | 1729827 | @522794 Please send me a message via DM. ^EX https://t.co/c9WoAfwenP |
| 2 | 1729827 | 522795 | True | 1729826 |  | @ATVIAssist @522794 You going to reply to my messages then? Pull your finger out and do some work |
