# Battle Builder - Draft Rulebook

*A cooperative-competitive engine-building card game for 2-4 players*

---

## Core Concept

**Battle Builder** combines Pokémon-inspired battles with deck-building mechanics. Players cooperate to defeat monsters, earning resources to improve their decks and stats. After every three monster battles, players face each other in PvP combat. The goal is to accumulate the most Victory Points through defeating monsters (1 VP each) and players (2 VP each).

### Key Mechanics
- **Cooperative Monster Battles:** Players team up to fight monsters of varying difficulty
- **Secret Action Selection:** Simultaneous, hidden card play with stamina bidding for turn order
- **Resource Management:** Earn skill tokens during battles to upgrade your deck
- **Risk/Reward Decisions:** Choose harder monsters for better rewards, but risk defeat
- **Competitive Tension:** Within cooperation, players compete for resources and positioning

### Design Goals
- Create meaningful tension between cooperation and self-interest
- Reward tactical battle decisions, not just deck optimization
- Prevent runaway leaders through cooperative dependencies
- Keep all players engaged throughout the full game arc

---

## Game Flow

### Setup (2 Players)
Each player receives:
- Starting deck: 5 basic attack cards (2-4 damage range)
- Starting defense deck: 3 basic defense cards (2-4 block range)
- 20 HP tokens
- 20 Stamina tokens (reset each battle)

Available for purchase:
- Attack card tiers (Tier 1-3)
- Defense card tiers (Tier 1-3)
- HP upgrades
- Stamina upgrades

### Game Structure
The game consists of **4 rounds**, each containing:
1. **Team Formation** - Players pair up (in 2-player, always together; in 4-player, rotate partners)
2. **Monster Selection** - Draw 3 monster cards, choose 1 to fight
3. **Monster Battle** - Cooperative battle against chosen monster
4. **Rewards Phase** - Distribute earned skill tokens
5. **Shopping Phase** - Purchase deck/stat upgrades with tokens

After every 3 rounds: **PvP Battle Phase** - All players face off (pairings determined by VP standing or rotation)

### Total Game Arc
- **9 Monster Battles** (3 rounds × 3)
- **3 PvP Battles** (after rounds 3, 6, 9)
- **Duration:** 45-90 minutes (estimated)

### Variants to Test
**Variant A: Fixed Teams (4-player)**
- Players stay with the same partner for all 9 monster battles
- Creates deeper cooperation but reduces competitive balance

**Variant B: Auction Monster Selection**
- Instead of draw-and-choose, players bid skill tokens to select monsters first
- Winner chooses first, pays their bid to the bank
- Creates explicit trade-offs between current resources and future rewards

**Variant C: Variable Round Structure**
- Instead of fixed 3-battle rounds, players vote when to trigger PvP
- Requires majority agreement, adds negotiation layer
- Risk: Dominant players delay PvP to build bigger leads

---

## Monster Battles

### Battle Structure
A battle consists of multiple turns. Each turn follows these phases:

**1. Action Selection (Hidden)**
- Each player secretly selects one card from their attack deck
- Place it face-down in front of you

**2. Stamina Allocation (Hidden)**
- Each player secretly allocates stamina to their action using stamina tokens
- Some powerful cards may require minimum stamina expenditure
- Place stamina tokens face-down next to your action card

**3. Reveal**
- All players and the monster reveal their actions and stamina simultaneously

**4. Determine Play Order**
- Highest stamina acts first
- Ties broken randomly (coin flip/die roll)
- Monster acts at its printed speed value

**5. Resolve Actions**
- In play order: Apply attack damage to targets
- When attacked: Defender draws top card from their defense deck and blocks that much damage
- Subtract remaining damage from HP
- Track actions taken for skill token rewards

**6. Check Victory/Defeat**
- If monster reaches 0 HP: Players win, proceed to Rewards Phase
- If any player reaches 0 HP: Battle ends, proceed to Rewards Phase
- Otherwise: Return to step 1 for another turn

### Monster Cards
Each monster card specifies:
- **HP:** Total health points
- **Attack:** Damage dealt per turn
- **Speed:** Base stamina value for turn order
- **Deck Types:** Which attack/defense/special decks the monster uses
- **Special Rules:** E.g., "Attacks slower player," "AoE: deals damage to both players," "Enrage: +2 attack after turn 3"
- **Reward Value:** Base skill tokens awarded for victory

### Difficulty Tiers (Preliminary Values - NEEDS TESTING)
- **Easy:** 10-15 HP, 2-3 Attack, Speed 3, Rewards: 3 tokens
- **Medium:** 20-25 HP, 4-5 Attack, Speed 5, Rewards: 6 tokens  
- **Hard:** 35-40 HP, 6-8 Attack, Speed 7, Rewards: 10 tokens

### Variants to Test

**Variant A: Monster Targeting Rules**
Test different targeting behaviors:
- *Option 1:* Always attacks slower player
- *Option 2:* Attacks player who dealt most damage last turn
- *Option 3:* Attacks player with higher current HP
- *Option 4:* Attacks player with more VP

**Variant B: Dual Monster Battles**
- Each player draws 2-3 monster cards and secretly chooses one
- Both monsters are revealed simultaneously
- Players must defeat both monsters in the same battle
- Each monster acts independently; players split attention
- Rewards: Sum of both monsters' token values

**Variant C: Monster Special Abilities**
Add unique mechanics to monsters:
- **Regeneration:** Heals 2 HP at end of each turn
- **Counter:** Deals 1 damage to attacker when hit
- **Armor Piercing:** Attacks ignore defense cards
- **Speed Drain:** Reduce faster player's stamina by 2 each turn

**Variant D: Environmental Effects**
Draw an environment card that modifies the battle:
- **Narrow Passage:** Only faster player can attack
- **Sandstorm:** All players/monster -2 speed
- **Healing Springs:** Gain 1 HP per turn
- **High Ground:** +2 damage to all attacks

---

## Skill Tokens & Rewards

### Token Types (Choose One System to Test)

**System A: Unified Tokens**
- All rewards earned as generic "Skill Tokens"
- Can be spent freely on any upgrade
- *Pro:* Simple, flexible
- *Con:* Loses battle-driven incentive structure

**System B: Split Tokens (4 Types)**
- **Attack Tokens:** Earned by dealing damage, spent on attack cards
- **Defense Tokens:** Earned by blocking damage, spent on defense cards
- **Speed Tokens:** Earned by acting first, spent on stamina upgrades
- **HP Tokens:** Earned based on remaining health, spent on HP upgrades
- *Pro:* Battle decisions matter more, forces specialization
- *Con:* More components, risk of "dead" tokens

**System C: Partial Split (2 Types)**
- **Combat Tokens:** Earned during battles, spent on attack/defense cards
- **Training Tokens:** Earned based on performance (HP remaining, speed), spent on HP/stamina
- *Pro:* Balances simplicity and meaningful choices
- *Con:* Still somewhat complex

**System D: Split with Conversion**
- Use System B, but allow conversion: "Spend 3 tokens of one type to gain 2 of another"
- Conversion only available during specific phases (e.g., after PvP)
- *Pro:* Preserves battle meaning, prevents dead tokens
- *Con:* Adds complexity

### Earning Tokens in Monster Battles

**Base Rewards:**
- Defeating monster: Earn monster's printed reward value
- One player defeated: Half rewards (rounded down)
- Both players defeated: Zero rewards

**Performance Bonuses (System B - Split Tokens):**
- **Attack Tokens:** 1 per 3 damage dealt (or per "damage action" taken)
- **Defense Tokens:** 1 per 3 damage blocked (or per hit taken)
- **Speed Tokens:** 1 per turn you acted first
- **HP Tokens:** Based on remaining HP at battle end (1 token per 5 HP remaining?)

**Performance Bonuses (System A - Unified):**
- Bonus tokens based on:
  - Turns taken (fewer = more efficient = more tokens)
  - Overkill damage (excess damage to monster = bonus tokens)
  - Perfect battle (neither player took damage = bonus tokens)

### Reward Distribution in Co-op
- Each player tracks their own actions and earns tokens individually
- Base monster reward is split: Each player gets full amount (encourages cooperation)
- Or: Base reward is divided: Players split the pool (encourages efficiency)

### Variants to Test

**Variant A: Action-Based Token Earning**
Granular tracking during battle:
- Move before monster: +1 speed token
- Deal damage: +1 attack token per action (not per point of damage)
- Take damage: +1 defense token per hit
- Survive until end with HP remaining: +1 HP token per 5 HP
- *Requires:* Detailed tracking sheet per battle

**Variant B: Milestone Rewards**
Instead of per-action rewards, award tokens for achieving milestones:
- **Speedster:** Acted first 3+ times: +3 speed tokens
- **Executioner:** Dealt killing blow: +2 attack tokens
- **Tank:** Took 10+ damage: +3 defense tokens
- **Survivor:** Ended with 80%+ HP: +2 HP tokens

**Variant C: Role-Based Earning**
Before each battle, players secretly select a role card:
- **Striker:** Double attack tokens, half defense tokens
- **Tank:** Double defense tokens, half attack tokens
- **Tactician:** Double speed tokens
- **Survivor:** Double HP tokens
- If both players pick same role: -3 penalty to base reward

**Variant D: Betting System**
Before battle, each player can wager tokens:
- "I bet 2 tokens I'll deal the killing blow"
- "I bet 3 tokens neither of us will fall below 5 HP"
- If achieved: Double the wagered amount
- If failed: Lose the wagered tokens

---

## Spending Tokens & Upgrades

### Available Purchases

**Attack Cards (Tiered Decks)**
Each tier contains 3-10 unique cards with varying effects:
- **Tier 1:** 4 tokens - Basic attacks (5-7 damage, some with minor effects)
- **Tier 2:** 8 tokens - Strong attacks (8-10 damage, useful effects like "draw a card")
- **Tier 3:** 12 tokens - Elite attacks (11-15 damage, powerful effects like "ignore defense")

**Defense Cards (Tiered Decks)**
- **Tier 1:** 4 tokens - Basic blocks (4-6 block)
- **Tier 2:** 8 tokens - Strong blocks (7-9 block, some with "counter 1 damage")
- **Tier 3:** 12 tokens - Elite blocks (10-12 block, effects like "negate next attack")

**HP Upgrades**
- Cost: 3 tokens per +5 HP (or scaling: 3/5/7/9 for each successive upgrade)
- Maximum: +20 HP above starting value

**Stamina Upgrades**
- Cost: 4 tokens per +5 stamina
- Maximum: +15 stamina above starting value

### Deck Management Rules
- **No hand limit:** Keep all cards in your deck
- **Deck cycling:** When deck is exhausted, shuffle discard and continue
- **Deck thinning:** (Optional) When purchasing a card, you may remove one basic card from your deck
- Each battle, start with full deck shuffled

### Shopping Phase Timing
- After each monster battle, before next team formation
- Players shop simultaneously (no turn order)
- In 4-player: Partners may negotiate but purchase independently

### Variants to Test

**Variant A: Diminishing Returns**
Each successive upgrade costs more:
- First HP upgrade: 3 tokens
- Second: 5 tokens
- Third: 8 tokens
- Fourth: 12 tokens
- *Prevents extreme specialization, encourages balanced builds*

**Variant B: Upgrade Trees**
Some cards/upgrades require prerequisites:
- "Elite Slash" (15 damage) requires owning 2 Tier 2 attack cards
- "+10 Max HP" requires already having "+5 Max HP"
- Creates progression paths and strategic planning

**Variant C: Card Values for PvP Rewards**
Each card has printed value (Basic: 1, Tier 1: 2, Tier 2: 3, Tier 3: 4):
- When you win PvP, gain tokens equal to 1/3 of opponent's total deck value
- Creates interesting tension: Strong deck makes you powerful but increases opponent's potential reward
- May need balancing to avoid "stay weak" strategies

**Variant D: Limited Shop**
Instead of always-available cards:
- Reveal 6 random cards from each tier after each battle
- Players can only purchase from available pool
- Refreshes after each shopping phase
- Creates urgency and adaptation, reduces analysis paralysis

**Variant E: Shared Shop with Scarcity**
- Each card type has limited copies (e.g., only 2 copies of "Heavy Strike")
- First player to purchase gets it
- In 4-player, creates competition for best cards
- May need turn order system for shopping

---

## PvP Battles

### When PvP Occurs
After every 3 monster battles (rounds 3, 6, and 9):
- All players participate in PvP
- **2-player:** Single match
- **4-player:** Two simultaneous matches, pairings determined by:
  - *Option A:* VP standing (1st vs 2nd, 3rd vs 4th)
  - *Option B:* Rotation (everyone fights everyone once)
  - *Option C:* Players choose opponents (draft style)

### PvP Battle Rules
PvP battles follow the same turn structure as monster battles:
1. Secret action selection
2. Secret stamina allocation
3. Reveal simultaneously
4. Resolve in speed order (faster attacks first)
5. Both players draw defense cards when attacked
6. Continue until one player reaches 0 HP

**Key Differences from Monster Battles:**
- No cooperation - pure competition
- Both players are intelligent opponents (no preset behavior)
- No skill tokens earned during battle
- Winner receives rewards, loser may receive consolation

### PvP Rewards

**Option A: Fixed Rewards**
- Winner: 2 Victory Points + 4 skill tokens
- Loser: 0 VP + 2 skill tokens (catchup mechanic)

**Option B: Deck-Value-Based Rewards**
- Winner: 2 VP + tokens equal to 1/3 of loser's deck value
- Loser: 0 VP + 2 consolation tokens
- *Requires each card to have printed value*

**Option C: Wagering System**
- Before battle, each player contributes tokens to a pot (minimum 2)
- Winner takes entire pot + 2 VP
- Creates high-stakes moments and potential comebacks

**Option D: Choice Rewards**
- Create two reward piles (e.g., "5 tokens + 2 VP" vs "10 tokens")
- Winner chooses first which pile to take
- Loser gets remaining pile
- Allows strategic decisions based on current position

### Strategic Considerations
- **Deck Transparency:** Players can see which cards opponents have purchased
- **Mind Games:** Predict opponent's likely actions based on their deck composition
- **Stamina Management:** No stamina cap means battles can vary wildly in length
- **Risk Assessment:** Is it worth spending resources to win PvP, or better to conserve for monsters?

### Variants to Test

**Variant A: Attack of Opportunity**
- If you act before opponent and reduce them below 5 HP, take another turn immediately
- Creates potential for devastating combos and blow-outs
- May make speed too valuable

**Variant B: Best of Three Rounds**
- PvP battles consist of 3 rounds
- Players reset to full HP between rounds but keep stamina expenditure
- Win 2 out of 3 rounds to win the match
- Adds depth but increases game length significantly

**Variant C: Arena Effects**
- Draw an arena card that modifies PvP battle
- Examples: "Lightning Arena: +3 speed to both players," "Cursed Ground: Max HP reduced by 5"
- Adds variety and reduces predictability

**Variant D: Betting Spectators (4-player)**
- While two players battle, other two can wager tokens on the outcome
- Correct prediction: Double your wager
- Wrong prediction: Lose your wager
- Keeps all players engaged during PvP

**Variant E: Revenge Mechanic**
- If you lose PvP, gain a "Revenge Token"
- Spend it in a future PvP battle for: +5 stamina for the battle, or draw +1 defense card when hit, or deal +2 damage with all attacks
- Provides catchup without directly handing out resources

---

## Victory Conditions

### Victory Points
Track VP on a visible score track throughout the game.

**Earning Victory Points:**
- Defeat a monster in co-op: 1 VP per player (both players earn 1 VP)
- Defeat a player in PvP: 2 VP (winner only)
- Total possible VP: 9 (monsters) + 6 (PvP) = 15 VP per player maximum

**Winning the Game:**
After the 3rd PvP battle (end of round 9):
- Player with most VP wins
- Tiebreaker options:
  - *Option A:* Most remaining skill tokens
  - *Option B:* Highest total deck value
  - *Option C:* Sudden death PvP battle

### Alternative Victory Conditions to Test

**Variant A: Threshold Victory**
- First player to reach 12 VP immediately wins
- Shortens game and creates urgency
- Risk: Runaway leader problem amplified

**Variant B: Multi-Category Scoring**
Award bonus VP at game end:
- Most monsters defeated: +2 VP
- Most PvP wins: +2 VP
- Highest total deck value: +1 VP
- Most HP remaining: +1 VP
- Diversifies winning strategies

**Variant C: Secret Objectives**
Each player draws 2 secret objective cards at game start, keeps 1:
- "Defeat 4+ easy monsters: +3 VP"
- "Win final PvP battle: +3 VP"
- "Purchase 3+ Tier 3 cards: +2 VP"
- Revealed and scored at game end

**Variant D: Championship Final**
After round 9, instead of declaring winner:
- Top 2 players by VP face off in final PvP battle
- Winner of battle wins the game (regardless of VP total)
- Creates dramatic finale, but could feel arbitrary

---

## Balancing & Testing Notes

### Critical Balance Points (NEEDS EXTENSIVE TESTING)

**Monster Difficulty Curve:**
- Target win rates: Easy 85%, Medium 65%, Hard 40%
- Expected value should favor Medium slightly to encourage diverse choices
- Adjust HP/Attack/Rewards based on playtest data

**Token Economy:**
- Players should afford 1 significant upgrade after each monster battle
- By round 3 (first PvP), decks should feel noticeably improved
- By round 9, players should have diverse, specialized decks

**PvP Balance:**
- Prevent "perfect" builds that dominate PvP
- Ensure rock-paper-scissors dynamics (speed beats power, defense beats speed, power beats defense?)
- Catchup mechanics should help but not guarantee losers can win

**Stamina Economy:**
- Starting stamina (20) should last 4-6 turns of moderate spending
- Encourage varied stamina allocation, not just "spend max every turn"
- High-stamina builds shouldn't dominate both PvE and PvP

### Runaway Leader Mitigation Strategies
Test combinations of:
1. Co-op dependency (strong player needs weak partner)
2. Consolation rewards for PvP losers
3. Monster targeting rules (attacks leader preferentially)
4. Diminishing returns on upgrades
5. Auction/bidding systems that cost resources

### Data to Track During Playtesting
- Monster selection distribution (are all difficulties chosen?)
- Win/loss rates per monster difficulty
- Average tokens earned per battle
- Time per battle (target: 5-10 minutes)
- Time per full game (target: 60-90 minutes)
- Final VP spread (goal: within 3-4 VP for close games)
- Player engagement (are trailing players invested?)

---

## Quick Reference: Turn Structure

### Monster Battle Turn
1. **Select Action** (hidden) - Choose 1 attack card
2. **Allocate Stamina** (hidden) - Spend stamina tokens
3. **Reveal** - Show cards and stamina simultaneously
4. **Determine Order** - Highest stamina goes first
5. **Resolve Attacks** - In order: deal damage, draw defense, subtract HP
6. **Check End** - Monster or player at 0 HP? If no, repeat from step 1

### Game Round Structure
1. **Team Up** - Form pairs (2-player: automatic, 4-player: rotate)
2. **Draw Monsters** - Reveal 3 monster cards
3. **Choose Monster** - Team selects which to fight
4. **Battle** - Follow Monster Battle Turn structure
5. **Distribute Rewards** - Award skill tokens based on performance
6. **Shop** - Purchase upgrades with tokens
7. **PvP Check** - After every 3 rounds, trigger PvP battles

---

## Design Philosophy & Future Development

### Core Pillars
1. **Meaningful Cooperation:** Co-op isn't just about winning together; internal competition for resources creates tension
2. **Tactical Depth:** Battle decisions matter as much as deck construction
3. **Risk/Reward Mastery:** Skill expression through difficulty selection and resource management
4. **Social Dynamics:** Deception, negotiation, and reading opponents are valid strategies

### Known Issues to Address
- **Complexity:** Many moving parts may cause analysis paralysis - simplify where possible
- **Game Length:** 9 battles + 3 PvP could exceed 90 minutes - consider shortening to 6 monsters + 2 PvP
- **Alpha Gamer Problem:** Experienced player may dominate co-op decisions - encourage secret selections
- **Luck vs. Skill:** Random defense draws add variance - consider hand management instead

### Expansion Ideas (Post-Core Testing)
- **Character Classes:** Asymmetric starting decks and abilities (Warrior, Mage, Rogue)
- **Monster Families:** Themed monster sets with synergies (Dragons, Undead, Elementals)
- **Equipment Cards:** Persistent bonuses purchased between battles
- **Campaign Mode:** Linked scenarios with story progression
- **Team Abilities:** Combos that trigger when partners coordinate specific actions

### Next Steps
1. **Prototype Battle Mechanics** - Test single battle with basic cards and monsters
2. **Balance Token Economy** - Iterate on earn/spend rates until progression feels good
3. **Test Full Arc** - Play complete 9-round game, track engagement and balance
4. **Simplify Complexity** - Cut or streamline mechanics that don't justify their overhead
5. **Blind Playtesting** - Have others play without designer present to find rules gaps

---

## Prototype Materials Needed

### For First Playtest (2-Player, 1 Battle)
- 10 attack cards per player (index cards, write damage values 2-5)
- 6 defense cards per player (index cards, write block values 2-5)
- 3 monster cards (Easy: 12 HP / 3 ATK, Medium: 18 HP / 4 ATK, Hard: 25 HP / 6 ATK)
- Tokens for HP tracking (poker chips, beads, or printed tokens)
- Stamina tokens (20 per player - suggest different color chips)
- Skill tokens (use coins or different color chips)
- Paper/pencil for tracking turn-by-turn actions

### For Full Playtest (2-Player, Full Game)
- Full decks with card variety (6-8 unique cards per tier)
- 9 monster cards across difficulties (3 easy, 3 medium, 3 hard)
- Victory Point tracker (paper scoreboard)
- Tier 1-3 purchasable cards (prepare 4-5 options per tier)
- Upgrade tokens/markers for HP and Stamina increases
- Timer to track game length
- Playtest feedback form

---

*This is a living document. Update after each playtest with findings and revised values.*