---
name: product-research
description: "Validate product ideas from Reddit pain points, competitor reviews, and market signals, with a scored list. Use when researching a niche or an app idea."
license: Apache-2.0
allowed-tools: Bash(playwright-cli *) Bash(playwright-cli) Bash(sleep *)
---

# Product Research & Idea Validation

## What this skill does

Two-pass research process to find and validate product opportunities in a target niche:
- **Pass 1 (Reddit):** Raw pain points, complaints, tool requests from real community conversations
- **Pass 2 (Corroboration):** Verify freshness, check existing solutions, read competitor reviews, confirm the pain still exists today

## Inputs

The user provides:
- **Niche/audience** (e.g., "Amazon FBA sellers", "Shopify store owners", "freelance designers")
- **Optional constraints** (e.g., "solo dev", "prefer simple to build", "B2B only")

---

## Pass 1: Reddit Community Research

### Browser setup

**Always use `playwright-cli open --headed --persistent`.** Both flags required — Reddit blocks if either is missing. Headed avoids headless fingerprint detection, persistent preserves login cookies.

### Phase 1: Identify communities (1 min)

1. Open browser: `playwright-cli open --headed --persistent`
2. Navigate to Reddit, identify top 2-3 subreddits for the niche
3. Check subscriber counts to prioritize (biggest first)

### Phase 2: Landscape scan (3-5 min per subreddit)

For each subreddit, extract top posts using JS eval (NOT snapshot parsing):

```bash
# Navigate to top posts
playwright-cli goto "https://www.reddit.com/r/{subreddit}/top/?t=year"

# Extract titles + metadata in one shot
playwright-cli eval "JSON.stringify([...document.querySelectorAll('a[href*=\"/comments/\"]')].map(a => ({title: a.textContent?.trim()?.slice(0,150), href: a.href})).filter(x => x.title && x.title.length > 20 && !x.title.includes('Skip') && !x.title.includes('Navigate')).reduce((acc, x) => { if (!acc.seen.has(x.href)) { acc.seen.add(x.href); acc.result.push(x); } return acc; }, {seen: new Set(), result: []}).result.slice(0, 25))"
```

Repeat for `t=month` to get recent trends.

**Time bias: prioritize 2026 > 2025. Threads older than 2024 are background context only — never primary evidence.**

### Phase 3: Deep-dive threads (2-3 min per thread)

Read 4-5 highest-signal threads. Extract comments:

```bash
playwright-cli eval "JSON.stringify([...document.querySelectorAll('[id*=\"comment\"] p, article p')].map(p => p.textContent?.trim()).filter(t => t && t.length > 25).slice(0, 35))"
```

**What to look for in comments:**
- Complaints about existing tools ("X is clunky", "X doesn't do Y")
- Explicit asks ("I wish there was...", "does anyone know a tool that...")
- Workarounds people describe (manual processes = automation opportunity)
- Recurring frustrations (same problem in multiple threads = high confidence)
- Tool recommendations + why they're insufficient

**Track freshness for every data point:**
- Note the age of each thread/comment (Reddit shows "Xmo ago", "Xy ago")
- Flag anything older than 12 months as potentially stale
- Recent threads (< 3 months) with the same pain = strong signal
- Old threads with no recent equivalents = possibly solved or irrelevant

### Phase 4: Targeted search (only if needed, 2 min)

Only after understanding the landscape from Phase 2-3. Use informed queries based on patterns already observed, not generic "wish there was a tool" queries.

```bash
playwright-cli goto "https://www.reddit.com/r/{subreddit}/search/?q={informed_query}&sort=relevance&t=all"
```

### Phase 5: Compile Pass 1 findings

Create a raw list of pain points with thread URLs and freshness tags before moving to Pass 2.

---

## Pass 2: Corroboration & Validation

For each top 5-7 ideas from Pass 1, verify with external sources. This is what separates "someone complained on Reddit" from "this is a real, current, underserved market."

### 2A: Freshness check

For each idea, ask: **Is this pain point still active TODAY, or was it solved / became irrelevant?**

- Search for the same pain in recent (last 3 months) posts
- If the pain is old (e.g., PPC was painful in 2019) — check if the same complaints exist in 2025-2026 threads, or if new tools solved it
- Look for "I switched to X and it fixed it" comments — that means the problem may be solved

### 2B: Existing solution audit

For each idea, find what already exists:

```bash
# Search for existing tools
playwright-cli goto "https://www.google.com/search?q={niche}+{pain_point}+tool+OR+software+OR+app"

# Check review sites
playwright-cli goto "https://www.g2.com/search?query={tool_name}"
playwright-cli goto "https://www.capterra.com/search/?query={tool_name}"
```

**What to capture:**
- Tool name, pricing, rating
- Top complaints in reviews (1-2 star reviews are gold — they show unmet needs)
- Feature gaps mentioned by reviewers
- "I switched FROM X because..." comments

### 2C: Competitor weakness analysis

For the top 3 ideas, read 1-star and 2-star reviews of existing solutions:

```bash
# Extract review text
playwright-cli eval "JSON.stringify([...document.querySelectorAll('[class*=\"review\"] p, [class*=\"Review\"] p, [data-testid*=\"review\"] p')].map(p => p.textContent?.trim()).filter(t => t && t.length > 30).slice(0, 20))"
```

**Key patterns in bad reviews:**
- "Too expensive for what it does" → price disruption opportunity
- "Clunky UI / hard to use" → UX opportunity
- "Missing X feature" → feature gap opportunity
- "Support is terrible" → service opportunity
- "Hasn't been updated in years" → abandoned product opportunity

### 2D: Market size signals

Quick checks for each top idea:
- Google the main existing tool — check their pricing page for plan tiers (indicates market maturity)
- Check Chrome Web Store for related extensions (install counts = market size proxy)
- Check ProductHunt for similar launches (comments show reception)

---

## Scoring Framework

| Factor | 1 | 2 | 3 |
|--------|---|---|---|
| **Pain (P)** | Nice-to-have | Saves hours/week | Critical to revenue/survival |
| **Confidence (C)** | 1-2 mentions | 3-5 threads + upvotes | Recurring theme, multiple sources |
| **Ease (E)** | Complex orchestration, many integrations | Standard web app, some API work | Simple SaaS, weeks to MVP |
| **Promotability (M)** | Hard to reach, enterprise sale | Niche communities, word of mouth | Reddit/YouTube/SEO natural fit, viral potential |
| **TAM (T)** | Small subset of niche | Most active members | Everyone in the niche |
| **Freshness (F)** | Modifier: 0.5x if only old threads, 1x if mixed, 1.5x if hot right now |

**Score = P x C x E x M x T x F** (higher = better)

Adjustments per user constraints:
- If user says "solo dev" or "easy to build" → weight Ease higher (multiply E by 1.5)
- If user says "complex is fine" → don't penalize Ease
- If user specifies revenue model → factor willingness-to-pay signals from threads

## Output Format

```markdown
# {Niche} App Ideas — Research Report

**Date:** YYYY-MM-DD
**Pass 1 Sources:** {subreddits with member counts}
**Pass 2 Sources:** {review sites, competitor tools checked}

## Scoring Framework
{table}

## Ranked Ideas

### 1. [Idea Name] — Score: X (P:X C:X E:X M:X T:X F:X)

**Problem:** What the audience is struggling with

**Freshness:** {ACTIVE / STALE / EMERGING} — {one-line justification, e.g., "3 threads in last 2 months, complaints intensifying due to 2026 fee changes"}

**Evidence (Reddit):**
- [Thread title](https://reddit.com/r/.../comments/...) — "key quote" (X upvotes, Y comments, Z ago)
- [Thread title](https://reddit.com/r/.../comments/...) — "key quote" (X upvotes, Z ago)

**Existing solutions & gaps:**
- {Tool} (${price}/mo, {rating} on G2) — Gap: "{what users complain about}"
- {Tool} (${price}/mo) — Gap: "{missing feature}"

**Opportunity angle:** What specifically to build differently
**MVP scope:** What v1 looks like + rough timeline

### 2. ...

## Top 3 Recommendation
{Brief rationale for the top picks given user's constraints}
```

## Behavioral Rules

1. **Add small random jitter** between actions: `sleep $((RANDOM % 2 + 1))` between navigations
2. **Use JS eval for data extraction**, not snapshot parsing — 10x faster and more reliable
3. **Browse organically first** — read top posts to understand the landscape before searching
4. **Don't use overly literal search queries** — people don't write "I wish someone built X." They complain, ask for alternatives, describe workarounds
5. **Read comments, not just titles** — titles are clickbait, comments contain the real pain
6. **Always track thread age** — a pain point from 3 years ago with no recent mentions may be solved
7. **Corroborate before scoring** — Reddit gives signal, Pass 2 gives conviction. Don't rank high on Reddit alone
8. **Close browser when done** — `playwright-cli close`
9. **Target 10-15 ideas from Pass 1, detail top 5 with Pass 2** — diminishing returns after ~30 min total per niche
10. **Always use `--headed --persistent`** — user wants to watch, session persists
11. **Always include thread URLs** — every evidence point must link to the source so user can verify firsthand
