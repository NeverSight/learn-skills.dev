---
name: neobank-positioning-engine-skill
description: Analyze crypto neobank positioning against competitors, find unclaimed territory, and generate a messaging framework. Use when a neobank needs to differentiate or when auditing a prospect's positioning.
---

# Neobank Positioning Engine

Scrapes a crypto neobank's website and its competitors, extracts positioning claims, maps the competitive messaging landscape, identifies white space, and generates a complete messaging framework with actual copy.

Not a generic "brand strategy" template. Every output is grounded in what competitors actually say on their websites, what users actually complain about in reviews, and what positioning territory is genuinely unclaimed.

## Trigger

- `position [neobank name]`
- `positioning audit for [neobank name]`
- `how should [neobank name] differentiate?`
- `competitive positioning: [neobank A] vs [neobank B] vs [neobank C]`

## Workflow

### Phase 1: Scrape Positioning Data

```bash
python scripts/scrape_positioning.py "[Company Name]" "[website URL]"
```

Run for the target company and 3-5 competitors. The script:
- Loads the homepage + key pages (about, pricing, features)
- Extracts: headlines, subheadlines, value propositions, CTAs, proof points, feature claims, social proof, brand voice signals
- Saves structured output to `output/{slug}-positioning.json`

For a full competitive analysis:
```bash
python scripts/scrape_positioning.py "KAST" "https://kast.com"
python scripts/scrape_positioning.py "Revolut" "https://revolut.com"
python scripts/scrape_positioning.py "Crypto.com" "https://crypto.com"
```

If scraping fails or returns thin data, fall back to:
- Web search: `"[company]" neobank (mission OR "we help" OR "built for")`
- Cached positioning data in `references/neobank-messaging-map.md`
- App store descriptions (often contain concentrated positioning language)

### Phase 2: Extract Positioning Elements

Read scraped JSON and extract these elements for each company:

| Element | What to find | Where to look |
|---------|-------------|---------------|
| **Positioning claim** | The single sentence that says "we are X for Y" | Homepage hero, About page first paragraph |
| **Category** | How they define their market category | Meta description, PR headlines, About page |
| **Target audience** | Who they explicitly or implicitly address | Homepage copy, feature pages, pricing tiers |
| **Claimed benefits** | Top 3-5 benefits they lead with | Homepage sections below hero, feature cards |
| **Proof points** | Numbers, logos, testimonials, certifications | Trust bars, case studies, footer badges |
| **Differentiation claim** | What they say makes them different | "Why us" sections, comparison pages |
| **Brand voice** | Tone: corporate/casual/technical/rebellious | Overall copy style, CTA language, error pages |
| **CTA language** | What action they push users toward | Primary buttons, hero CTA, sticky nav CTA |
| **Omissions** | What they DON'T mention (often more revealing) | Absence of: fees, security details, regulatory info, team |

Use `references/positioning-frameworks.md` for the analytical lens.

### Phase 3: Map Positioning Territories

Plot all companies on these four positioning dimensions:

**Dimension 1: Audience Spectrum**
```
Crypto Native ←————————————→ Mainstream Consumer
(speaks DeFi)                (speaks "easy money app")
```

**Dimension 2: Trust Model**
```
Self-Custody ←————————————→ Full Custodial
("your keys")               ("we handle everything")
```

**Dimension 3: Value Proposition Core**
```
Yield/Returns ←————————————→ Utility/Spending
("earn 8% APY")              ("spend crypto anywhere")
```

**Dimension 4: Brand Personality**
```
Technical/Builder ←————————————→ Lifestyle/Consumer
("built on ZK proofs")         ("money, simplified")
```

For each company, assign a position (1-10) on each dimension. Build a 2x2 matrix using the two most relevant dimensions for this specific competitive set.

### Phase 4: White Space Analysis

Identify gaps by asking:

1. **Unclaimed territories**: Which quadrants of the positioning map have no strong player?
2. **Unspoken benefits**: What do users want (from review data) that no competitor claims?
3. **Credibility gaps**: Who claims things without proof points? (Opportunity to own with evidence.)
4. **Messaging fatigue**: Which claims are so overused they've become invisible? (Avoid these.)
5. **Audience orphans**: Which user segments are underserved by current positioning?

Consult `references/neobank-messaging-map.md` for pre-mapped positioning of major players.

Cross-reference with app store review data if available. User language in reviews often reveals positioning opportunities that competitor websites miss.

### Phase 5: Generate Messaging Framework

Produce a complete messaging framework:

**1. Positioning Statement** (Geoffrey Moore format)
```
For [target customer] who [need/pain],
[Product] is a [category]
that [key benefit].
Unlike [primary alternative],
[product] [key differentiator].
```
Provide 2-3 variants. Each takes a different strategic angle.

**2. One-Liner Options** (5-7 words max)
Generate 5 options. Rules:
- No buzzwords ("revolutionary," "next-gen," "seamless")
- Must pass the "could a competitor say this?" test. If yes, it's not differentiated.
- Must connect to a real proof point or capability
- Should feel inevitable in hindsight, not clever

**3. Value Propositions** (3 pillars)
For each pillar:
- Headline (under 8 words)
- Supporting sentence (one sentence, specific)
- Proof point (number, case study, or verifiable claim)

**4. Messaging by Audience**
For each identified target segment:
- Their language (how they describe the problem)
- Hook (what gets their attention)
- Proof (what convinces them)
- CTA (what action to push)

**5. What NOT to Say**
List 5-10 specific phrases, claims, or angles to avoid. For each:
- The phrase
- Why it fails (overused / unsubstantiated / wrong audience / competitor-owned)

**6. Competitive Response Matrix**
For each major competitor:
- Their strongest claim
- Their weakest point
- How to position against them without naming them

### Phase 6: Render and Deliver

Save the structured brief as JSON to `output/{slug}-brief.json`, then render as PDF:
```bash
python scripts/render_positioning.py "output/{slug}-brief.json"
```

## Rules

1. **Evidence over opinion.** Every positioning recommendation must trace back to: competitor website copy, user review language, market data, or structural advantage. "I think you should position as X" is worthless. "No competitor in your segment claims X, users ask for it in 23% of reviews, and you have the technical capability" is useful.

2. **Specificity over abstraction.** "Differentiate on trust" is a waste of time. "Publish your reserve audit monthly, link it from the homepage hero, and use the line 'See exactly where your money is. Updated [date]'" is actionable.

3. **The competitor test.** For every positioning claim: could a competitor say the exact same thing? If yes, it's not positioning. It's wallpaper. Push harder.

4. **Real language only.** Pull actual phrases from websites and reviews. Don't invent marketing speak. The best positioning borrows the customer's own words.

5. **Omissions matter.** What a company doesn't say is often more revealing than what they do. If nobody talks about fees, that's a territory. If nobody shows their team, that's a trust gap to exploit.

6. **No AI slop.** No "in today's competitive landscape." No "it's worth noting." Direct. Compressed. CMO-ready.

7. **Positioning is a bet.** Don't try to be everything. The framework should force a choice. "You can own X or Y. Here's the tradeoff. Here's our recommendation and why."

## Examples

**Input:** "Position KAST against Revolut and Crypto.com"

**Process:**
1. Scrape KAST, Revolut, Crypto.com websites
2. Extract positioning elements for all three
3. Map on dimensions: KAST is crypto-native + spending-focused, Revolut is mainstream + utility, Crypto.com is crypto-native + yield
4. White space: no player owns "transparent crypto spending" (Revolut hides crypto fees, Crypto.com leads with earn/yield, KAST could own spending transparency)
5. Generate framework: "The crypto card that shows you everything." Three pillars: transparent fees, multi-chain spending, no lock-ups.
6. Render PDF, deliver

**Input:** "How should a new crypto neobank targeting LatAm differentiate?"

**Process:**
1. Scrape top 5 LatAm-serving neobanks (Nubank, Mercado Pago, Ualá, dLocal, Lemon Cash)
2. Extract positioning. All cluster around "financial inclusion" and "easy access"
3. White space: nobody owns "USD stability" messaging specifically (they all talk features, not the core anxiety: peso depreciation)
4. Framework: Position around the emotional need (protecting purchasing power) not the feature (crypto/USD access)
5. Generate copy that speaks LatAm financial anxiety, not crypto jargon

## Edge Cases

- **Pre-launch company (no website yet)**: Use pitch deck, app store description, social media bios. Positioning analysis becomes purely competitive: "here's the landscape, here's the gap, here's where to plant your flag."
- **Very crowded segment (10+ competitors)**: Don't map all of them. Pick the 3-4 that compete for the same user. Map the rest as "background noise" with one-line positioning summaries.
- **Company with no clear positioning**: Flag it: "Your current messaging is [list of generic claims]. None pass the competitor test. You have no positioning. Here are three options."
- **B2B crypto infrastructure (not consumer neobank)**: Adjust dimensions. Replace Audience Spectrum with "Developer-focused vs Business-focused." Replace Trust Model with "Self-hosted vs Managed."

## Files

| Path | Purpose |
|------|---------|
| `scripts/scrape_positioning.py` | Website scraper for positioning elements |
| `scripts/analyze_positioning.py` | LLM-powered analysis: phases 2-5 automated via API |
| `scripts/render_positioning.py` | JSON brief to styled PDF |
| `scripts/run_pipeline.py` | Chains scrape → analyze → render in one command |
| `references/positioning-frameworks.md` | Moore, Dunford, territory mapping, competitive patterns |
| `references/neobank-messaging-map.md` | Pre-mapped positioning of 10+ neobanks and exchanges |
| `output/` | Generated positioning data and briefs |
