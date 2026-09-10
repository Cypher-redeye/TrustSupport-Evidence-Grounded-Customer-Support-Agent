# Purchase & Billing Semantic Review

## Semantic Precedence Rules Evaluated
1. **PURCHASE_AND_BILLING**: Strict monetary/transaction failure (`double charged`, `refund`, `payment failed`, `bank`).
2. **PROGRESSION_AND_REWARDS**: Missing virtual content after a purchase (`cod points`, `supply drops`, `didn't receive`).
3. **DIGITAL_ACCESS_AND_DOWNLOAD**: Access, code redemption, installation (`download`, `code`, `season pass`).

## 50 Example Categorizations
### Example 1
- **Text:** @ATVIAssist you removed the original bo3 from the ps store so I can't download it even though I bought it, I have to pay 63$ for chronicles
- **Previous Intent:** DIGITAL_ACCESS_AND_DOWNLOAD
- **Proposed Intent:** DIGITAL_ACCESS_AND_DOWNLOAD
- **Reason:** Mentions downloading, installing, or codes
- **Assignment Rule:** is_digital_access

### Example 2
- **Text:** @ATVIAssist can I buy the ww2 soundtrack?
- **Previous Intent:** DIGITAL_ACCESS_AND_DOWNLOAD
- **Proposed Intent:** DIGITAL_ACCESS_AND_DOWNLOAD
- **Reason:** Broad match ('buy'/'bought') but no specific access, reward, or billing issue specified.
- **Assignment Rule:** fallback_to_cluster

### Example 3
- **Text:** @XboxSupport @115765 bought cod WW2 digital on xb1. I file share with my brother. He can already preload the game but I can’t @XboxSupport @115765 Just curious if that is just for people with slower internet that will take a few days to install or what. Not a huge deal. Just curious
- **Previous Intent:** DIGITAL_ACCESS_AND_DOWNLOAD
- **Proposed Intent:** DIGITAL_ACCESS_AND_DOWNLOAD
- **Reason:** Mentions downloading, installing, or codes
- **Assignment Rule:** is_digital_access

### Example 4
- **Text:** @ATVIAssist hi there. Pre-Ordered COD WW2 on the PlayStation Store but cannot find the WW2 theme? Please advise.
- **Previous Intent:** DIGITAL_ACCESS_AND_DOWNLOAD
- **Proposed Intent:** DIGITAL_ACCESS_AND_DOWNLOAD
- **Reason:** Mentions downloading, installing, or codes
- **Assignment Rule:** is_digital_access

### Example 5
- **Text:** @ATVIAssist  tell me why i spent 60 dollars on your game and it runs like fucking shit. Every fucking game lags out. How are you going to sell people a broken fucking game.
- **Previous Intent:** INFORMATION_AND_OTHER_REQUESTS
- **Proposed Intent:** INFORMATION_AND_OTHER_REQUESTS
- **Reason:** Broad match ('buy'/'bought') but no specific access, reward, or billing issue specified.
- **Assignment Rule:** fallback_to_cluster

### Example 6
- **Text:** @ATVIAssist so I bought some cod points on black ops 3 but I don’t have them. HELP????
- **Previous Intent:** MATCHMAKING_AND_LOBBIES
- **Proposed Intent:** PROGRESSION_AND_REWARDS
- **Reason:** Mentions missing virtual items (e.g. cod points/supply drops)
- **Assignment Rule:** is_progression_rewards

### Example 7
- **Text:** @ATVIAssist Last time
I ever buy season pass I'm
Litterally looking at people playing it on my friendlist this is bs!
- **Previous Intent:** DIGITAL_ACCESS_AND_DOWNLOAD
- **Proposed Intent:** DIGITAL_ACCESS_AND_DOWNLOAD
- **Reason:** Mentions downloading, installing, or codes
- **Assignment Rule:** is_digital_access

### Example 8
- **Text:** @ATVIAssist I want a refund I am a season pass holder for iw and I got charged 15$ so I want my money back
- **Previous Intent:** PROGRESSION_AND_REWARDS
- **Proposed Intent:** PURCHASE_AND_BILLING
- **Reason:** Matches strict monetary failure/charge keywords
- **Assignment Rule:** is_purchase_billing

### Example 9
- **Text:** @ATVIAssist I purchased and down loaded the Variety Map Pack but didn't get my 10 rare supply drops from Lion Strike. Help? https://t.co/A22ReiMUIA
- **Previous Intent:** PROGRESSION_AND_REWARDS
- **Proposed Intent:** PROGRESSION_AND_REWARDS
- **Reason:** Mentions missing virtual items (e.g. cod points/supply drops)
- **Assignment Rule:** is_progression_rewards

### Example 10
- **Text:** @ATVIAssist it seems I’ve bought some cod points Ealier this morning! For WW2 but I haven’t received them yet. Not even the co formation email
- **Previous Intent:** MATCHMAKING_AND_LOBBIES
- **Proposed Intent:** PROGRESSION_AND_REWARDS
- **Reason:** Mentions missing virtual items (e.g. cod points/supply drops)
- **Assignment Rule:** is_progression_rewards

### Example 11
- **Text:** @ATVIAssist some free bonus material sounds like it’s in store @521872 @ATVIAssist I second this!! I just want to play my new vidgi games
- **Previous Intent:** DIGITAL_ACCESS_AND_DOWNLOAD
- **Proposed Intent:** DIGITAL_ACCESS_AND_DOWNLOAD
- **Reason:** Mentions downloading, installing, or codes
- **Assignment Rule:** is_digital_access

### Example 12
- **Text:** @ATVIAssist I need help I bought cod points but theyre not on my account
- **Previous Intent:** PROGRESSION_AND_REWARDS
- **Proposed Intent:** PROGRESSION_AND_REWARDS
- **Reason:** Mentions missing virtual items (e.g. cod points/supply drops)
- **Assignment Rule:** is_progression_rewards

### Example 13
- **Text:** @ATVIAssist I bought the digital deluxe version from gameStop I entered code to download. Website went down now it says code already redeem
- **Previous Intent:** DIGITAL_ACCESS_AND_DOWNLOAD
- **Proposed Intent:** DIGITAL_ACCESS_AND_DOWNLOAD
- **Reason:** Mentions downloading, installing, or codes
- **Assignment Rule:** is_digital_access

### Example 14
- **Text:** @115890 @135958 @ATVIAssist what is going on with Infinite Warfare DLC 4 please fix this download issue this is un-exceptable @308953 @115890 @135958 @ATVIAssist I am a season pass holder and it still isn’t working for me when will the update be out @308275 @115890 @135958 @ATVIAssist Same as me i own the season pass and it is making me buy the DLC in order to play
- **Previous Intent:** DIGITAL_ACCESS_AND_DOWNLOAD
- **Proposed Intent:** DIGITAL_ACCESS_AND_DOWNLOAD
- **Reason:** Mentions downloading, installing, or codes
- **Assignment Rule:** is_digital_access

### Example 15
- **Text:** @122172 I ain’t trying to buy Ghosts for $60, help me out 🤔
- **Previous Intent:** DIGITAL_ACCESS_AND_DOWNLOAD
- **Proposed Intent:** DIGITAL_ACCESS_AND_DOWNLOAD
- **Reason:** Broad match ('buy'/'bought') but no specific access, reward, or billing issue specified.
- **Assignment Rule:** fallback_to_cluster

### Example 16
- **Text:** @ATVIAssist why can't I get my camo or anything else I bought from the $100 copy of #ww2?
- **Previous Intent:** MATCHMAKING_AND_LOBBIES
- **Proposed Intent:** MATCHMAKING_AND_LOBBIES
- **Reason:** Broad match ('buy'/'bought') but no specific access, reward, or billing issue specified.
- **Assignment Rule:** fallback_to_cluster

### Example 17
- **Text:** @ATVIAssist Hi, I have purchased Destiny 2 via the Blizzard bnet app. Will I be able to upgrade/purchase an expansion pass later? 👀
- **Previous Intent:** DIGITAL_ACCESS_AND_DOWNLOAD
- **Proposed Intent:** DIGITAL_ACCESS_AND_DOWNLOAD
- **Reason:** Broad match ('buy'/'bought') but no specific access, reward, or billing issue specified.
- **Assignment Rule:** fallback_to_cluster

### Example 18
- **Text:** @ATVIAssist Do you guys have an ETA on the post match issue? I'm still experiencing this on the ps4 when I'm not hosting the party. Bought the game digital from the Playstation store if that matters.
- **Previous Intent:** INFORMATION_AND_OTHER_REQUESTS
- **Proposed Intent:** DIGITAL_ACCESS_AND_DOWNLOAD
- **Reason:** Mentions downloading, installing, or codes
- **Assignment Rule:** is_digital_access

### Example 19
- **Text:** @ATVIAssist I bought the game on my PS4 and it says preload now but it’s not preloading? And I can’t seem to find where to start it? @ATVIAssist WWII
- **Previous Intent:** DIGITAL_ACCESS_AND_DOWNLOAD
- **Proposed Intent:** DIGITAL_ACCESS_AND_DOWNLOAD
- **Reason:** Mentions downloading, installing, or codes
- **Assignment Rule:** is_digital_access

### Example 20
- **Text:** @ATVIAssist @115754 @115766 @115786 @XboxSupport This is not good for business. I dump hundreds of dollars for this game. #NoMore https://t.co/R3npgIbfi0
- **Previous Intent:** FEEDBACK_AND_COMPLAINTS
- **Proposed Intent:** FEEDBACK_AND_COMPLAINTS
- **Reason:** Broad match ('buy'/'bought') but no specific access, reward, or billing issue specified.
- **Assignment Rule:** fallback_to_cluster

### Example 21
- **Text:** @ATVIAssist I bought COD on the PS4 store. It tells me I purchased it but it won’t let me pre load it. Any suggestions ?
- **Previous Intent:** DIGITAL_ACCESS_AND_DOWNLOAD
- **Proposed Intent:** DIGITAL_ACCESS_AND_DOWNLOAD
- **Reason:** Mentions downloading, installing, or codes
- **Assignment Rule:** is_digital_access

### Example 22
- **Text:** @ATVIAssist I bought the game preorder and redeem the code but I do not understand how to use it
- **Previous Intent:** PROGRESSION_AND_REWARDS
- **Proposed Intent:** DIGITAL_ACCESS_AND_DOWNLOAD
- **Reason:** Mentions downloading, installing, or codes
- **Assignment Rule:** is_digital_access

### Example 23
- **Text:** I recently purchased a new PC running Windows 10 64 bit.  I would like to install my older games, ie. Call of Duty World at War and Call of Duty Modern Warfare but they won't install.  How can I rectify this situation.@ATVIAssist
- **Previous Intent:** MATCHMAKING_AND_LOBBIES
- **Proposed Intent:** DIGITAL_ACCESS_AND_DOWNLOAD
- **Reason:** Mentions downloading, installing, or codes
- **Assignment Rule:** is_digital_access

### Example 24
- **Text:** Only 2 more hours till #CODWWII !!!!!. @115766 I'm ready! @479781 It's so close now, Brandon. We hope you've been preparing. @115766 @479781 Are we able to buy cod points ?
- **Previous Intent:** MATCHMAKING_AND_LOBBIES
- **Proposed Intent:** PROGRESSION_AND_REWARDS
- **Reason:** Mentions missing virtual items (e.g. cod points/supply drops)
- **Assignment Rule:** is_progression_rewards

### Example 25
- **Text:** @115766  why is this like the only call of duty to do so crappy at launch i cant get nothing done on game no credits no contracts nothing fix this please its really annoying im about to get a refund for my 100 dollars.
- **Previous Intent:** MATCHMAKING_AND_LOBBIES
- **Proposed Intent:** PURCHASE_AND_BILLING
- **Reason:** Matches strict monetary failure/charge keywords
- **Assignment Rule:** is_purchase_billing

### Example 26
- **Text:** @115765 I just bought the game last night and cant seem to connect to the online services? Its says error code 103295
- **Previous Intent:** CONNECTIVITY_AND_ERRORS
- **Proposed Intent:** DIGITAL_ACCESS_AND_DOWNLOAD
- **Reason:** Mentions downloading, installing, or codes
- **Assignment Rule:** is_digital_access

### Example 27
- **Text:** @115765 we don’t have enough incentive to buy contracts. They aren’t worth the armory credits. How about a rare supply drop, some amount of XP, and some credits back?
- **Previous Intent:** PROGRESSION_AND_REWARDS
- **Proposed Intent:** PROGRESSION_AND_REWARDS
- **Reason:** Mentions missing virtual items (e.g. cod points/supply drops)
- **Assignment Rule:** is_progression_rewards

### Example 28
- **Text:** @ATVIAssist ps4 is fine sounds like whoever bought rights to the game. Gets more online time and the servers for them never go down #Fishy https://t.co/NsBp9ngH0x
- **Previous Intent:** CONNECTIVITY_AND_ERRORS
- **Proposed Intent:** CONNECTIVITY_AND_ERRORS
- **Reason:** Broad match ('buy'/'bought') but no specific access, reward, or billing issue specified.
- **Assignment Rule:** fallback_to_cluster

### Example 29
- **Text:** What time does WWII drop on PS store? @115765 @115766 @117014
- **Previous Intent:** DIGITAL_ACCESS_AND_DOWNLOAD
- **Proposed Intent:** DIGITAL_ACCESS_AND_DOWNLOAD
- **Reason:** Mentions downloading, installing, or codes
- **Assignment Rule:** is_digital_access

### Example 30
- **Text:** @128996 @280 @ATVIAssist @125833 how do I get a refund for the PC version of Destiny 2? Quite frankly the game is not worth it @301144 @128996 @280 @ATVIAssist @125833 Contact blizzard support if you bought it from them
- **Previous Intent:** PURCHASE_AND_BILLING
- **Proposed Intent:** PURCHASE_AND_BILLING
- **Reason:** Matches strict monetary failure/charge keywords
- **Assignment Rule:** is_purchase_billing

### Example 31
- **Text:** COD WW2 is pretty fun when it actually works, which is barely. I'm sick of waiting 20 minutes between games and not getting rank up rewards. The first COD game I buy in 6 years and it's a fucking shit show.

Fix your shit @ATVIAssist
- **Previous Intent:** MATCHMAKING_AND_LOBBIES
- **Proposed Intent:** MATCHMAKING_AND_LOBBIES
- **Reason:** Broad match ('buy'/'bought') but no specific access, reward, or billing issue specified.
- **Assignment Rule:** fallback_to_cluster

### Example 32
- **Text:** I am not on the #sony #playstation4 #ps4 network so #activision I’ll have a full #refund please. Next time #doyourjob properly @ATVIAssist https://t.co/zGp3GV2z4T
- **Previous Intent:** FEEDBACK_AND_COMPLAINTS
- **Proposed Intent:** PURCHASE_AND_BILLING
- **Reason:** Matches strict monetary failure/charge keywords
- **Assignment Rule:** is_purchase_billing

### Example 33
- **Text:** @115766 fix the multiplayer after action report 4 WW2. Really annoying to restart game after each match! If u can't, refund my $ 😡
- **Previous Intent:** MATCHMAKING_AND_LOBBIES
- **Proposed Intent:** PURCHASE_AND_BILLING
- **Reason:** Matches strict monetary failure/charge keywords
- **Assignment Rule:** is_purchase_billing

### Example 34
- **Text:** .@ATVIAssist put Tony Hawk's Pro Skater HD back on the PS Store!
- **Previous Intent:** DIGITAL_ACCESS_AND_DOWNLOAD
- **Proposed Intent:** DIGITAL_ACCESS_AND_DOWNLOAD
- **Reason:** Mentions downloading, installing, or codes
- **Assignment Rule:** is_digital_access

### Example 35
- **Text:** @ATVIAssist how will I be getting the multiplayer upgrade if I bought the game digitally?
- **Previous Intent:** DIGITAL_ACCESS_AND_DOWNLOAD
- **Proposed Intent:** DIGITAL_ACCESS_AND_DOWNLOAD
- **Reason:** Broad match ('buy'/'bought') but no specific access, reward, or billing issue specified.
- **Assignment Rule:** fallback_to_cluster

### Example 36
- **Text:** @115765 @ATVIAssist I got the pro edition and never got the zombies camo and call of duty code endowment pack yet in my mail in the hq help https://t.co/lBDv0FiyEB @115765 @ATVIAssist Also I have redeemed in the Microsoft store and downloaded and is yet to show up in the mail in the hq
- **Previous Intent:** DIGITAL_ACCESS_AND_DOWNLOAD
- **Proposed Intent:** PROGRESSION_AND_REWARDS
- **Reason:** Mentions missing virtual items (e.g. cod points/supply drops)
- **Assignment Rule:** is_progression_rewards

### Example 37
- **Text:** @ATVIAssist  hey im having trouble getting the iw dlc 4 on xb1 i bought season pass but its still making me pay for dlc 4
- **Previous Intent:** DIGITAL_ACCESS_AND_DOWNLOAD
- **Proposed Intent:** DIGITAL_ACCESS_AND_DOWNLOAD
- **Reason:** Mentions downloading, installing, or codes
- **Assignment Rule:** is_digital_access

### Example 38
- **Text:** @ATVIAssist I bought Call Of Duty Modern Warfare Remastered from the Infinite Warfare game and I then sold the game and now it won’t let me play MWR without the IW disc but I want to play it. What can I do?
- **Previous Intent:** MATCHMAKING_AND_LOBBIES
- **Proposed Intent:** MATCHMAKING_AND_LOBBIES
- **Reason:** Broad match ('buy'/'bought') but no specific access, reward, or billing issue specified.
- **Assignment Rule:** fallback_to_cluster

### Example 39
- **Text:** @115766  game I purchased and downloaded through the Xbox marketplace (COD ww2), that I have been playing for a couple of weeks now has error code 0x803f8001, I am signed into the profile it was purchased on and like previously mentioned have been playing it with no issues
- **Previous Intent:** CONNECTIVITY_AND_ERRORS
- **Proposed Intent:** DIGITAL_ACCESS_AND_DOWNLOAD
- **Reason:** Mentions downloading, installing, or codes
- **Assignment Rule:** is_digital_access

### Example 40
- **Text:** @115766 for black ops 3. If you wanna buy a perk from the wunderfizz you dont see in kino the bottle can you fix that?
- **Previous Intent:** GAMEPLAY_BUG_REPORT
- **Proposed Intent:** GAMEPLAY_BUG_REPORT
- **Reason:** Broad match ('buy'/'bought') but no specific access, reward, or billing issue specified.
- **Assignment Rule:** fallback_to_cluster

### Example 41
- **Text:** @ATVIAssist I did not receive my deluxe codes for the Xbox One digital version.  I want to know how I can go about getting a refund.
- **Previous Intent:** PURCHASE_AND_BILLING
- **Proposed Intent:** PURCHASE_AND_BILLING
- **Reason:** Matches strict monetary failure/charge keywords
- **Assignment Rule:** is_purchase_billing

### Example 42
- **Text:** @ATVIAssist i didn't receive my 1k cod points when i buy the cod ww2 yesterday... what should i do ?🤨🤔
- **Previous Intent:** MATCHMAKING_AND_LOBBIES
- **Proposed Intent:** PROGRESSION_AND_REWARDS
- **Reason:** Mentions missing virtual items (e.g. cod points/supply drops)
- **Assignment Rule:** is_progression_rewards

### Example 43
- **Text:** @ATVIAssist I just bought some cod points but they won’t show up on my game and I can’t use em. Console is ps4
- **Previous Intent:** MATCHMAKING_AND_LOBBIES
- **Proposed Intent:** PROGRESSION_AND_REWARDS
- **Reason:** Mentions missing virtual items (e.g. cod points/supply drops)
- **Assignment Rule:** is_progression_rewards

### Example 44
- **Text:** @ATVIAssist why cant i play carentan map? I have the season pass and i have downloaded it from the playstation store.
- **Previous Intent:** DIGITAL_ACCESS_AND_DOWNLOAD
- **Proposed Intent:** DIGITAL_ACCESS_AND_DOWNLOAD
- **Reason:** Mentions downloading, installing, or codes
- **Assignment Rule:** is_digital_access

### Example 45
- **Text:** @115766 I purchased cod points but i never received them this is very annoying. I literally spent $10 and got nothing in return
- **Previous Intent:** PROGRESSION_AND_REWARDS
- **Proposed Intent:** PROGRESSION_AND_REWARDS
- **Reason:** Mentions missing virtual items (e.g. cod points/supply drops)
- **Assignment Rule:** is_progression_rewards

### Example 46
- **Text:** @115766 u fucking cunts fix ur connection To ur servers I bought this Game for 70$ so pls do what u have to do
- **Previous Intent:** CONNECTIVITY_AND_ERRORS
- **Proposed Intent:** CONNECTIVITY_AND_ERRORS
- **Reason:** Broad match ('buy'/'bought') but no specific access, reward, or billing issue specified.
- **Assignment Rule:** fallback_to_cluster

### Example 47
- **Text:** @ATVIAssist I love the fact that I got charged $16.00 for a DLC that I shouldn't have got charged for because I own the season pass.
- **Previous Intent:** PURCHASE_AND_BILLING
- **Proposed Intent:** PURCHASE_AND_BILLING
- **Reason:** Matches strict monetary failure/charge keywords
- **Assignment Rule:** is_purchase_billing

### Example 48
- **Text:** @115766 very disappointed, just bought Cod ww2. When I open either sp or mp, I receive “Cod ww2 has stopped working” Are you guys aware of this issue, as many other people have the same issue. I have tried everything on your troubleshooting guide, but no success. 1060 i5-7500
- **Previous Intent:** MATCHMAKING_AND_LOBBIES
- **Proposed Intent:** MATCHMAKING_AND_LOBBIES
- **Reason:** Broad match ('buy'/'bought') but no specific access, reward, or billing issue specified.
- **Assignment Rule:** fallback_to_cluster

### Example 49
- **Text:** @atviassist I own the IW season pass on the Xbox but it's still making me buy DLC4
- **Previous Intent:** DIGITAL_ACCESS_AND_DOWNLOAD
- **Proposed Intent:** DIGITAL_ACCESS_AND_DOWNLOAD
- **Reason:** Mentions downloading, installing, or codes
- **Assignment Rule:** is_digital_access

### Example 50
- **Text:** @ATVIAssist I didn’t preorder WW2  to get an error code the whole day... Fix error code 4128 or I want a refund
- **Previous Intent:** CONNECTIVITY_AND_ERRORS
- **Proposed Intent:** PURCHASE_AND_BILLING
- **Reason:** Matches strict monetary failure/charge keywords
- **Assignment Rule:** is_purchase_billing

