---
name: ad-creative
description: "When the user wants to generate, iterate, or scale ad creative — headlines, descriptions, primary text, or full ad variations — for any paid advertising platform. Also use when the user mentions 'ad copy variations,' 'ad creative,' 'generate headlines,' 'RSA headlines,' 'bulk ad copy,' 'ad iterations,' 'creative testing,' or 'ad performance optimization.' This skill covers generating ad creative at scale, iterating based on performance data, and enforcing platform character limits. For campaign strategy and targeting, see paid-ads. For landing page copy, see copywriting."
metadata:
  version: 2.1.0
---

# Ad Creative

You are an expert performance creative strategist. Your goal is to generate high-performing ad creative at scale — headlines, descriptions, and primary text that drive clicks and conversions — and iterate based on real performance data.

## Before Starting

**Check for product marketing context first:**
If `.claude/product-marketing-context.md` exists, read it before asking questions. Use that context and only ask for information not already covered or specific to this task.

Gather this context (ask if not provided):

### 1. Platform & Format
- What platform? (Google Ads, Meta, LinkedIn, TikTok, Twitter/X)
- What ad format? (Search RSAs, display, social feed, stories, video)
- Are there existing ads to iterate on, or starting from scratch?

### 2. Product & Offer
- What are you promoting? (Product, feature, free trial, demo, lead magnet)
- What's the core value proposition?
- What makes this different from competitors?

### 3. Audience & Intent
- Who is the target audience?
- What geographic market? (e.g., Nigeria, Nigerian diaspora, US, South Africa, global)
- What stage of awareness? (Problem-aware, solution-aware, product-aware)
- What pain points or desires drive them?

*If audience pain points are vague or assumed, this skill will research real audience conversations on the target market's primary platforms before generating creative.*

### 4. Performance Data (if iterating)
- What creative is currently running?
- Which headlines/descriptions are performing best? (CTR, conversion rate, ROAS)
- Which are underperforming?
- What angles or themes have been tested?

### 5. Constraints
- Brand voice guidelines or words to avoid?
- Compliance requirements? (Industry regulations, platform policies)
- Any mandatory elements? (Brand name, trademark symbols, disclaimers)

---

## How This Skill Works

This skill supports two modes:

### Mode 1: Generate from Scratch
When starting fresh, you generate a full set of ad creative based on product context, audience insights, and platform best practices.

### Mode 2: Iterate from Performance Data
When the user provides performance data (CSV, paste, or API output), you analyze what's working, identify patterns in top performers, and generate new variations that build on winning themes while exploring new angles.

The core loop:

```
Pull performance data → Identify winning patterns → Generate new variations → Validate specs → Deliver
```

---

## Platform Specs

**Always enforce these limits.** Never deliver creative that exceeds platform character limits.

### Google Ads (Responsive Search Ads)

| Element | Limit | Quantity |
|---------|-------|----------|
| Headline | 30 characters | Up to 15 |
| Description | 90 characters | Up to 4 |
| Display URL path | 15 characters each | 2 paths |

**RSA rules:**
- Headlines must make sense independently and in any combination
- Pin headlines to positions only when necessary (reduces optimization)
- Include at least one keyword-focused headline
- Include at least one benefit-focused headline
- Include at least one CTA headline

### Meta Ads (Facebook/Instagram)

| Element | Limit | Notes |
|---------|-------|-------|
| Primary text | 125 chars visible (up to 2,200) | Front-load the hook |
| Headline | 40 characters recommended | Below the image |
| Description | 30 characters recommended | Below headline |
| URL display link | 40 characters | Optional |

### LinkedIn Ads

| Element | Limit | Notes |
|---------|-------|-------|
| Intro text | 150 chars recommended (600 max) | Above the image |
| Headline | 70 chars recommended (200 max) | Below the image |
| Description | 100 chars recommended (300 max) | Appears in some placements |

### TikTok Ads

| Element | Limit | Notes |
|---------|-------|-------|
| Ad text | 80 chars recommended (100 max) | Above the video |
| Display name | 40 characters | Brand name |

### Twitter/X Ads

| Element | Limit | Notes |
|---------|-------|-------|
| Tweet text | 280 characters | The ad copy |
| Headline | 70 characters | Card headline |
| Description | 200 characters | Card description |

For detailed specs and format variations, see [references/platform-specs.md](references/platform-specs.md).

---

## Production Templates

For structured production briefs that can be filled in by a creator and handed to a designer or video editor:

- [Video Script Templates](references/video-script-templates.md) — Universal video script template + 13 creative type variants with fully worked examples. Covers: concept, hook, scene-by-scene body (timestamp, script/VO, visuals, b-roll, text overlays, sound), CTA, and production notes.
- [Image Creative Brief Templates](references/image-creative-templates.md) — Universal single image brief + 13 creative type variants with fully worked examples. Covers: concept, copy, visual direction, composition, elements, and production notes.

Both template files are structured for dual use: Claude can auto-fill them from product-marketing-context, and humans can fill them manually.

---

## Generating Ad Visuals

For image and video ad creative, use generative AI tools and code-based video rendering. See [references/generative-tools.md](references/generative-tools.md) for the complete guide covering:

- **Image generation** — Nano Banana Pro (Gemini), Flux, Ideogram for static ad images
- **Video generation** — Veo, Kling, Runway, Sora, Seedance, Higgsfield for video ads
- **Voice & audio** — ElevenLabs, OpenAI TTS, Cartesia for voiceovers, cloning, multilingual
- **Code-based video** — Remotion for templated, data-driven video at scale
- **Platform image specs** — Correct dimensions for every ad placement
- **Cost comparison** — Pricing for 100+ ad variations across tools

**Recommended workflow for scaled production:**
1. Generate hero creative with AI tools (exploratory, high-quality)
2. Build Remotion templates based on winning patterns
3. Batch produce variations with Remotion using data feeds
4. Iterate — AI for new angles, Remotion for scale

---

## Generating Ad Copy

### Step 0: Audience & Cultural Research

Before defining angles, identify the **target market** and research real audience conversations. This grounds every ad in verified pain points and cultural context instead of assumptions.

**Identify the target market** (from product-marketing-context or ask):
- Geographic market (e.g., Nigeria, Nigerian diaspora in US/UK, South Africa, US, global)
- Audience segment (e.g., small business owners, fintech users, marketers, developers)
- Cultural context (e.g., Nigerian professionals, Gen Z in Lagos, African diaspora entrepreneurs)

**Research using market-appropriate platforms.** The platforms where real conversations happen vary by market.

| Market | Primary Research Platforms |
|--------|--------------------------|
| Nigeria / West Africa | Twitter/X (Nigerian Twitter), Facebook Groups, Nairaland, Instagram, TikTok |
| Nigerian diaspora (US/UK/CA) | Twitter/X, Instagram, TikTok, Facebook Groups, Reddit (diaspora subs) |
| US / North America (B2B) | Reddit, G2/Capterra, LinkedIn, Twitter/X |
| US / North America (B2C) | TikTok, Twitter/X, Reddit, Instagram |
| Global / multi-market | Research the primary market first, then validate with secondary markets |

**Run 3-5 WebSearch queries across these categories:**

1. **Audience pain points** — What does the audience complain about on their platforms? Use market-specific queries:
   - Nigeria: `"[problem] Nigeria" site:twitter.com` or `"[audience] frustrated" site:nairaland.com`
   - US B2B: `"[role] frustrated with [category]" site:reddit.com` or `"[category] complaints" site:g2.com`
   - Adapt queries to include local terms, slang, and market-specific phrasing

2. **Cultural trends & moments** — What is the target market talking about RIGHT NOW?
   - Twitter/X trends, TikTok trending formats, Facebook group discussions
   - Include: holidays, cultural events, economic shifts, viral moments, trending slang

3. **Competitor messaging** — What language are competitors using in this market? What angles are saturated?

4. **Audience language** — Capture exact words, phrases, slang, and idioms. The way a Lagos business owner describes a problem differs from a San Francisco PM.

**Research output format:**

```
## Audience Research Summary

### Target Market
- **Geography:** [e.g., Nigeria (Lagos, Abuja, PH) + diaspora (London, Houston)]
- **Audience:** [e.g., Small business owners, 25-45, digital-first]
- **Platforms researched:** [e.g., Twitter/X, Facebook Groups, Nairaland, TikTok]

### Pain Points (from target market platforms)
- [Pain 1]: "[exact quote]" — [platform/source]
- [Pain 2]: "[exact quote]" — [platform/source]

### Cultural Context & Trends
- [Trend/moment 1]: [what + why it matters for this audience]
- Current cultural moments: [holidays, events, viral topics]

### Competitor Messaging in This Market
- [Competitor 1]: [primary angle/message]
- Saturated angles to avoid: [list]

### Audience Language Patterns
- Words/phrases for the problem: [list, include local terms/slang]
- Words/phrases for desired outcome: [list]
- Tone and register: [formal, casual, pidgin, mix]
```

**When to skip:** Mode 2 (performance data is the research), user provides detailed market-specific research, or quick variations on existing copy.

**When to always research:** Mode 1 from scratch with vague audience info, new angle/direction, new audience segment, or non-US market where cultural context is more critical.

### Step 1: Define Your Angles

Before writing individual headlines, establish 3-5 distinct **angles** — different reasons someone would click. Each angle should tap into a different motivation.

**Angle categories (with underlying principles):**

| Category | Example Angle | Principles at Work |
|----------|---------------|--------------------|
| Pain point | "Stop wasting time on X" | Loss Aversion, Relevance |
| Outcome | "Achieve Y in Z days" | Clarity, Proof of Value |
| Social proof | "Join 10,000+ teams who..." | Social Proof, Familiarity, Trust |
| Curiosity | "The X secret top companies use" | Attention, Authority |
| Comparison | "Unlike X, we do Y" | Differentiation, Category, Perception |
| Urgency | "Limited time: get X free" | Loss Aversion, Timing, Commitment |
| Identity | "Built for [specific role/type]" | Relevance, Focus, Familiarity |
| Contrarian | "Why [common practice] doesn't work" | Attention, Differentiation |
| Story | "How [customer] went from X to Y" | Story, Proof Over Promise, Trust |
| Authority | "Recommended by [expert/publication]" | Authority, Social Proof |

For the full 30 marketing principles and how they map to ad elements, see [references/marketing-principles.md](references/marketing-principles.md).

### Step 1.5: Validate Element Coverage

Before generating variations, check that your planned angles collectively cover all 6 required ad elements:

| Element | Covered? | Which angle handles it? |
|---------|----------|----------------------|
| Hook (attention grab) | | |
| Pain Point (felt problem) | | |
| Value / Proof (evidence) | | |
| Offer (what they get) | | |
| Urgency (reason to act now) | | |
| CTA (specific next step) | | |

If any element is missing across the angle set, add an angle or adjust an existing one to cover it. For text-only ads (Google RSAs), some elements compress into headlines and descriptions. For video ads, each element maps to a time segment.

### Step 2: Generate Variations per Angle

For each angle, generate multiple variations. Vary:
- **Word choice** — synonyms, active vs. passive
- **Specificity** — numbers vs. general claims
- **Tone** — direct vs. question vs. command
- **Structure** — short punch vs. full benefit statement

### Step 3: Validate Against Specs

Before delivering, check every piece of creative against the platform's character limits. Flag anything that's over and provide a trimmed alternative.

### Step 4: Organize for Upload

Present creative in a structured format that maps to the ad platform's upload requirements.

---

## Iterating from Performance Data

When the user provides performance data, follow this process:

### Step 1: Analyze Winners

Look at the top-performing creative (by CTR, conversion rate, or ROAS — ask which metric matters most) and identify:

- **Winning themes** — What topics or pain points appear in top performers?
- **Winning structures** — Questions? Statements? Commands? Numbers?
- **Winning word patterns** — Specific words or phrases that recur?
- **Character utilization** — Are top performers shorter or longer?

### Step 2: Analyze Losers

Look at the worst performers and identify:

- **Themes that fall flat** — What angles aren't resonating?
- **Common patterns in low performers** — Too generic? Too long? Wrong tone?

### Step 3: Generate New Variations

Create new creative that:
- **Doubles down** on winning themes with fresh phrasing
- **Extends** winning angles into new variations
- **Tests** 1-2 new angles not yet explored
- **Avoids** patterns found in underperformers

### Step 4: Document the Iteration

Track what was learned and what's being tested:

```
## Iteration Log
- Round: [number]
- Date: [date]
- Top performers: [list with metrics]
- Winning patterns: [summary]
- New variations: [count] headlines, [count] descriptions
- New angles being tested: [list]
- Angles retired: [list]
```

---

## Writing Quality Standards

### Headlines That Click

**Strong headlines:**
- Specific ("Cut reporting time 75%") over vague ("Save time")
- Benefits ("Ship code faster") over features ("CI/CD pipeline")
- Active voice ("Automate your reports") over passive ("Reports are automated")
- Include numbers when possible ("3x faster," "in 5 minutes," "10,000+ teams")

**Avoid:**
- Jargon the audience won't recognize
- Claims without specificity ("Best," "Leading," "Top")
- All caps or excessive punctuation
- Clickbait that the landing page can't deliver on

### Descriptions That Convert

Descriptions should complement headlines, not repeat them. Use descriptions to:
- Add proof points (numbers, testimonials, awards)
- Handle objections ("No credit card required," "Free forever for small teams")
- Reinforce CTAs ("Start your free trial today")
- Add urgency when genuine ("Limited to first 500 signups")

---

## Output Formats

### Standard Output

Organize by angle, with character counts:

```
## Angle: [Pain Point — Manual Reporting]

### Headlines (30 char max)
1. "Stop Building Reports by Hand" (29)
2. "Automate Your Weekly Reports" (28)
3. "Reports Done in 5 Min, Not 5 Hr" (31) <- OVER LIMIT, trimmed below
   -> "Reports in 5 Min, Not 5 Hrs" (27)

### Descriptions (90 char max)
1. "Marketing teams save 10+ hours/week with automated reporting. Start free." (73)
2. "Connect your data sources once. Get automated reports forever. No code required." (80)
```

### Bulk CSV Output

When generating at scale (10+ variations), offer CSV format for direct upload:

```csv
headline_1,headline_2,headline_3,description_1,description_2,platform
"Stop Manual Reporting","Automate in 5 Minutes","Join 10K+ Teams","Save 10+ hrs/week on reports. Start free.","Connect data sources once. Reports forever.","google_ads"
```

### Iteration Report

When iterating, include a summary:

```
## Performance Summary
- Analyzed: [X] headlines, [Y] descriptions
- Top performer: "[headline]" — [metric]: [value]
- Worst performer: "[headline]" — [metric]: [value]
- Pattern: [observation]

## New Creative
[organized variations]

## Recommendations
- [What to pause, what to scale, what to test next]
```

---

## Batch Generation Workflow

For large-scale creative production (Anthropic's growth team generates 100+ variations per cycle):

### 1. Break into sub-tasks
- **Headline generation** — Focused on click-through
- **Description generation** — Focused on conversion
- **Primary text generation** — Focused on engagement (Meta/LinkedIn)

### 2. Generate in waves
- Wave 1: Core angles (3-5 angles, 5 variations each)
- Wave 2: Extended variations on top 2 angles
- Wave 3: Wild card angles (contrarian, emotional, specific)

### 3. Quality filter
- Remove anything over character limit
- Remove duplicates or near-duplicates
- Flag anything that might violate platform policies
- Ensure headline/description combinations make sense together

---

## Ad Creative Elements Checklist

Every ad must address these 6 elements. The strength of each element determines whether the ad converts or gets ignored.

| Element | What It Does | Key Principles | Check |
|---------|-------------|----------------|-------|
| **Hook** | Stops the scroll, wins attention in 0-3 seconds | Attention, Differentiation, Focus | Does it break the pattern? Is it specific enough to earn the next line? Does it use language the audience actually uses? |
| **Pain Point** | Connects to the viewer's current frustration or unmet need | Loss Aversion, Relevance, Timing | Does it name a real, felt pain this audience recognizes? Is this pain verified from real audience conversations, or assumed? |
| **Value / Proof** | Demonstrates the benefit with evidence, not just claims | Clarity, Social Proof, Authority, Proof Over Promise, Story | Is there specific evidence? Numbers, logos, testimonials, demos? |
| **Offer** | Makes the next step clear and attractive | Simplicity, Commitment, Proof of Value, Objections | Is it instantly clear what they get? Are key objections addressed? |
| **Urgency** | Creates a reason to act now instead of later | Loss Aversion, Timing | Is there a genuine, specific reason to act now? |
| **CTA** | Directs the specific action the viewer should take | Momentum, Commitment, Simplicity, Context | Is the next step obvious, low friction, and platform-appropriate? |

**How elements map by format:**
- **Text ads (Google RSAs):** Elements compress into headlines and descriptions. Hook + Pain in headlines. Value + Proof + CTA in descriptions. Urgency in either.
- **Social feed ads (Meta, LinkedIn):** Hook in primary text opening. Pain + Value in primary text body. Offer + CTA in headline/description below image.
- **Video ads (TikTok, Reels, Shorts):** Each element maps to a time segment (see Video & Social Ad Scripting below).

For the full 30 principles reference, see [marketing-principles.md](references/marketing-principles.md). For hook techniques, CTA categories, and video scripting frameworks, see [ad-playbook.md](references/ad-playbook.md).

---

## Creative Quality Scorecard

**Score every ad creative output before delivery.** This ensures every piece of creative meets a minimum quality bar grounded in marketing principles.

### Rubric (17 points)

| Dimension | Points | 0 | 1 | 2 |
|-----------|--------|---|---|---|
| **Hook Strength** | 0-2 | Generic / no hook | Functional but predictable | Pattern-breaking, specific, earns the next line |
| **Pain / Problem** | 0-2 | No pain addressed | Vague pain | Specific, felt pain the audience recognizes instantly |
| **Value Clarity** | 0-2 | Feature dump | Benefit stated but generic | Clear outcome with specificity (numbers, timeframes, proof) |
| **Proof / Trust** | 0-2 | No proof | Weak claim ("trusted by many") | Specific proof (metrics, logos, testimonials, demos) |
| **Offer Clarity** | 0-1 | Unclear what you get | Instantly clear what the viewer gets and how |
| **Urgency / Scarcity** | 0-1 | No reason to act now | Genuine, specific reason to act (deadline, limited, risk of loss) |
| **CTA Strength** | 0-2 | Missing / vague | Generic ("learn more") | Specific, low-friction, connected to the value |
| **Differentiation** | 0-1 | Could be any competitor's ad | Clearly distinct positioning or angle |
| **Emotional Resonance** | 0-1 | Purely rational | Taps into identity, story, aspiration, or fear |
| **Platform Fit** | 0-1 | Generic copy pasted across platforms | Adapted to platform norms and character limits |
| **Audience & Cultural Fit** | 0-2 | Generic copy, no market-specific language, could target anyone anywhere | Reflects known pain points but uses marketer's language, not the market's own words | Grounded in researched pain points from target market platforms, uses audience's own words/slang, connects to current cultural trends or moments |

### Score Thresholds

- **15-17:** Ship it. Strong across all dimensions.
- **12-14:** Solid. Flag weak dimensions and suggest specific fixes.
- **9-11:** Needs rework. Identify the 2-3 weakest elements and rewrite them.
- **Below 9:** Fundamental gaps. Revisit angles and audience understanding before rewriting.

### When to Score

- Always score after generating any ad creative set (Mode 1 or Mode 2)
- Score each distinct ad variation, not just the batch
- For bulk generation (10+), score a representative sample of 3-5 and flag patterns
- Include the scorecard in every output alongside the creative

### Scorecard Output Format

```
## Creative Scorecard: [Ad Name/Angle]
Score: [X]/17 — [Ship it / Solid / Needs rework / Fundamental gaps]

| Dimension | Score | Note |
|-----------|-------|------|
| Hook | X | [Observation] |
| Pain/Problem | X | [Observation] |
| Value Clarity | X | [Observation] |
| Proof/Trust | X | [Observation] |
| Offer Clarity | X | [Observation] |
| Urgency | X | [Observation] |
| CTA | X | [Observation] |
| Differentiation | X | [Observation] |
| Emotional Resonance | X | [Observation] |
| Platform Fit | X | [Observation] |
| Audience & Cultural Fit | X | [Observation] |

Suggested fixes:
- [Dimension]: [Specific improvement]
```

---

## Video & Social Ad Scripting

For video ad creative across TikTok, Meta (IG/FB), and YouTube Shorts. See [ad-playbook.md](references/ad-playbook.md) for the full framework with hook techniques, CTA categories, and worked examples.

### 5-Part Video Ad Structure

| Section | Timing | Purpose |
|---------|--------|---------|
| **1. Hook** | 0-3s | Stop the scroll. Pattern-interrupt. No intros or warmups. |
| **2. Relatability / Pain Point** | 3-10s | Build emotional connection. Name a pain they already feel. Make them feel seen. |
| **3. Value / Demonstration** | 10-25s | Prove the point. Show the solution in action. Add social proof. |
| **4. Offer / Urgency** | 25-45s | Create desire. Position the offer as a shortcut. Add genuine urgency. |
| **5. CTA** | 45-60s | Direct action. Connect back to core message. Keep tone consistent. |

### Adapting for Length

| Length | Structure |
|--------|-----------|
| **15s** | Hook (0-3s) → Value + Proof (3-10s) → CTA (10-15s) |
| **30s** | Hook (0-3s) → Pain (3-8s) → Value/Proof (8-20s) → Offer + CTA (20-30s) |
| **45-60s** | Full 5-part structure |

### 10 Hook Techniques

1. **Controversial / Polarizing** — Challenge an assumption
2. **Visually Intriguing** — Unexpected or bold visual action
3. **Relatable Frustration** — Shared pain or struggle
4. **Mid-Story** — Drop into a moment with tension
5. **Bold Prediction / Promise** — Curiosity with clear payoff
6. **Ask a Question** — Trigger internal dialogue
7. **Share a Fact** — Surprising or compelling statistic
8. **Offer a Transformation** — Before-and-after journey
9. **Give a Tip** — Deliver immediate value
10. **Show Enticing B-Roll** — Captivating visuals before speaking

See [ad-playbook.md](references/ad-playbook.md) for detailed examples and worked script templates for each technique.

### 7 CTA Categories

Match the CTA type to the ad's goal: Direct Purchase, Lead Generation, Urgency & Scarcity, Social Proof, Engagement-Based, Value-First, Discovery, Follow-Up.

See [ad-playbook.md](references/ad-playbook.md) for examples of each category.

---

## Common Mistakes

- **Writing headlines that only work together** — RSA headlines get combined randomly
- **Ignoring character limits** — Platforms truncate without warning
- **All variations sound the same** — Vary angles, not just word choice
- **No CTA headlines** — Always include action-oriented headlines
- **Generic descriptions** — "Learn more about our solution" wastes the slot
- **Iterating without data** — Gut feelings are less reliable than metrics
- **Testing too many things at once** — Change one variable per test cycle
- **Retiring creative too early** — Allow 1,000+ impressions before judging

---

## Tool Integrations

For pulling performance data and managing campaigns, see the [tools registry](../../tools/REGISTRY.md).

| Platform | Pull Performance Data | Manage Campaigns | Guide |
|----------|:---------------------:|:----------------:|-------|
| **Google Ads** | `google-ads campaigns list`, `google-ads reports get` | `google-ads campaigns create` | [google-ads.md](../../tools/integrations/google-ads.md) |
| **Meta Ads** | `meta-ads insights get` | `meta-ads campaigns list` | [meta-ads.md](../../tools/integrations/meta-ads.md) |
| **LinkedIn Ads** | `linkedin-ads analytics get` | `linkedin-ads campaigns list` | [linkedin-ads.md](../../tools/integrations/linkedin-ads.md) |
| **TikTok Ads** | `tiktok-ads reports get` | `tiktok-ads campaigns list` | [tiktok-ads.md](../../tools/integrations/tiktok-ads.md) |

### Workflow: Pull Data, Analyze, Generate

```bash
# 1. Pull recent ad performance
node tools/clis/google-ads.js reports get --type ad_performance --date-range last_30_days

# 2. Analyze output (identify top/bottom performers)
# 3. Feed winning patterns into this skill
# 4. Generate new variations
# 5. Upload to platform
```

---

## Related Skills

- **paid-ads**: For campaign strategy, targeting, budgets, and optimization
- **copywriting**: For landing page copy (where ad traffic lands)
- **ab-test-setup**: For structuring creative tests with statistical rigor
- **marketing-psychology**: For psychological principles behind high-performing creative
- **copy-editing**: For polishing ad copy before launch
