---
name: startup-naming-scorer
description: Score and evaluate startup/company names using research-backed patterns from YC, a16z, Sequoia, and a 10K AI company study. Includes AI Slop Index, naming tests, syllable analysis, and category-specific guidance.
---

# Startup Naming Scorer

Research-backed naming evaluation skill. Built from analysis of 10,029 AI company names (DomainBFF Feb 2026), 300+ YC companies (W24-W26), and portfolios from a16z, Sequoia, First Round, Founders Fund, Techstars, and 500 Global.

## When to Use This Skill

- Evaluating candidate names for a new company or product
- Generating name ideas that avoid common traps
- Scoring existing names against proven patterns
- Checking if a name falls into "AI slop" territory
- Naming a B2B SaaS, infrastructure, or revenue-focused company

## The Scoring Rubric

Score every candidate name against these 6 criteria:

| Criterion | Weight | Slop (0-1) | Good (2-3) | Winner (4-5) |
|-----------|--------|-----------|-----------|--------------|
| **No AI/tech slop words** | 30% | Contains AI/ML/Deep/Neural/Smart/Data/Labs | Minor tech-adjacent word | Zero technology words |
| **Syllable count** | 20% | 4+ syllables | 3 syllables | 1-2 syllables |
| **Radio test** | 15% | Needs spelling out, ambiguous | Minor ambiguity | Heard once, found instantly |
| **No category words** | 15% | Describes the product category | Hints at category | Zero category words in name |
| **Domain availability** | 10% | Only obscure TLDs | .io/.so/.co available | .com available or strong branded alt |
| **Metaphorical resonance** | 10% | Describes the technology | Neutral/abstract | Evokes the feeling/outcome |

**Score ranges:** 0-1.5 = Slop, 1.5-3.0 = Weak, 3.0-4.0 = Competitive, 4.0-5.0 = Winner

## The AI Slop Index

### Tier 1: Nuclear Slop (instant disqualify)

| Pattern | Occurrences (of 10K) | Rule |
|---------|---------------------|------|
| **"Labs" suffix** | 477 (1 in 20) | Never use unless you're literally a research lab |
| **"AI" in name or TLD** | 30% of recent YC batches | When everyone is "AI," nobody is |
| **"Intelligence" suffix** | 105 | Tells people what you are instead of what you do |
| **"Deep" prefix** | 75 | Called "now passe" by multiple agencies |
| **"Systems" suffix** | 93 | Government contractor energy from 1987 |

### Tier 2: Heavy Slop (strong negative signal)

- **"Open" prefix**: OpenAI won. You can't.
- **Neural / Neuro**: Peaked 2018-2022. Dated.
- **Cognitive / Cogni-**: IBM Watson cosplay.
- **"Spark" prefix**: 95.5% prefix rate. Overcrowded.
- **Nova / Nexus / Apex / Pulse**: Sounds like Transformers.
- **Smart- prefix**: Implies competitors are dumb.
- **Auto- prefix**: 2014 thinking.
- **Quantum**: Used by companies with zero quantum involvement.
- **Cyber-**: 1995 sci-fi movie.

### Tier 3: Suffix Graveyard

| Suffix | Status | Note |
|--------|--------|------|
| **-ly** | Dead | Peaked ~2015. Absent from YC 2024-2026. |
| **-ify** | Dead | Shopify won. Everything else is derivative. |
| **-io** (TLD) | Declining | Acceptable for devtools only. |
| **.ai** (TLD) | Oversaturated | 28% of YC+Techstars already. |
| **-Hub** | Dead | GitHub owns this forever. |
| **-Stack** | Niche | Sounds infra even when you're not. |
| **-X** | Risky | Elon-adjacent connotation. |
| **-ware** | Legacy | 2005 energy. |

### Tier 4: Compound Slop

- **Data[Thing]**: Saturated.
- **Cloud[Thing]**: Signals 2014.
- **Smart[Thing]**: See prefix slop.
- **[Thing]Mind**: DeepMind took it.
- **[Thing]Sense**: 6sense took it.

## The 4 Naming Tests

Run every candidate through all 4:

### 1. Radio Test
Someone hears the name on a podcast. Can they spell it and Google it?
- **Pass:** Stripe, Gong, Zoom, Slack
- **Fail:** Xyleme, Qwilr, unusual spellings

### 2. Crowded Bar Test
Mentioned once in a loud room. Remembered the next morning?
- **Pass:** Short real words dominate
- **Fail:** Multi-syllable invented words

### 3. Building Test
On the side of a building, does it look like a real company?
- **Pass:** Anthropic, Stripe, Linear
- **Fail:** Names that are too cute or too clever for enterprise

### 4. Tell-a-Friend Test
Can a customer recommend you without spelling it out?
- **Pass:** "Check out Gong." That is the whole recommendation.
- **Fail:** "Check out Proximitty, that is P-R-O-X..."

## What Winners Actually Do

### The Data
- **82%** of unicorn SaaS companies use single-word names
- **47%** action/verb-based (Stripe, Slack, Zoom)
- **31%** abstract/invented (Figma, Notion, Vercel)
- **55-60%** of all YC names are real English words or compounds
- **~90%** of top YC performers by valuation use real words
- **2 syllables** is the statistical sweet spot

### The 7 Naming Patterns (ranked by success rate)

1. **Recontextualized Real Words**: Single dictionary word, new meaning. THE winner pattern. (Stripe, Ramp, Notion, Slack, Zoom, Maven, Clay, Cursor)
2. **Transparent Compounds**: Two real words combined. (Dropbox, Coinbase, DoorDash, Instacart)
3. **Invented CVCV Words**: Made-up but phonetically natural. (Twilio, Figma, Vercel)
4. **Metaphorical / Evocative**: Suggests attributes through metaphor. (Gong, Clari, 6sense, Chorus)
5. **Human First Names**: Rising trend. (Harvey, Jasper, Oscar, Ada)
6. **Literary/Mythological** (Palantir, Anduril, Asimov)
7. **Name + Descriptor**: Declining. (Scale AI, Norm AI)

### Revenue Intelligence Winners Specifically
- **Gong**: sound of a closed deal
- **Clari**: clarity into your pipeline
- **6sense**: sixth sense for buyer intent
- **Chorus**: sales team in harmony

**Pattern: Every winner uses a metaphor or sensory word, not a description.**

## Category-Specific Guidance

### B2B SaaS / Revenue / Infrastructure
- Short, sharp, competent: Ramp, Vanta, Clay, Stedi
- Avoid whimsy: credibility and recall efficiency matter
- Real words that sound sturdy and institutional

### B2C / Consumer
- Whimsical, emotional, memorable: Spotify, TikTok, Robinhood
- Human first names gaining ground
- Two-word story names: Warby Parker, Blue Apron

### Developer Tools
- Descriptive compounds: Databricks, LangChain, Retool
- .io acceptable here
- Action verbs: Factory, Crunched

## How to Use This Skill

### Evaluate a Single Name
```
Score the name "Ballast" for a B2B revenue intelligence platform
```

### Generate Candidates
```
Generate 20 two-syllable real-word candidates for a 
compliance-focused revenue engine
```

### Compare Finalists
```
Compare and score: Timber vs Mandate vs Vertic 
for a governed revenue intelligence platform
```

## Workflow

1. **Gather context**: What does the company do? Who buys it? What vertical?
2. **Generate candidates**: Use Pattern 1 (real words) and Pattern 4 (metaphorical) primarily
3. **Score each name**: Apply the 6-criterion rubric
4. **Run the 4 tests**: Radio, Crowded Bar, Building, Tell-a-Friend
5. **Check the Slop Index**: Flag any Tier 1-4 violations
6. **Domain/trademark screen**: Check .com, .so, .io availability + USPTO classes 35, 36, 38, 42
7. **Present top 3-5**: With scores, test results, and domain status

## Constraints to Respect

When the user has established naming constraints, honor them. Common constraints:
- Syllable count limits (e.g., 2-3 max)
- No "AI" in the name
- No specific letters (e.g., no X)
- No specific suffixes (-ly, -ify, -io, -ai, -hub)
- No compound words
- No fake Latin/Greek assembly
- Must pass coffee shop test
- Must look good "on the side of a building"
- Trademark-clean in relevant classes

## Sources

- DomainBFF: 10,000 AI Company Names Analysis (Feb 2026)
- NameStormers: "Name Slop" analysis
- River + Wolf: AI naming trends
- Crunchbase: Multi-year startup naming trends
- SmartBranding: YC batch domain analyses (W24, F25, W26)
- namemy.app: SaaS Naming Guide (unicorn analysis)
- YC company directory and unicorn list
- a16z, Sequoia, First Round, Founders Fund portfolio analysis
