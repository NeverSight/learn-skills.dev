---
name: linkbuilding
description: Use when planning link acquisition. Classifies the site's authority phase from site age and visible signals, then recommends phase-appropriate tactics from the bundled tactic playbook library. No backlink tool required.
---

# Link Building

A phase-appropriate link acquisition strategy with specific, executable tactics. The agent classifies your site's authority phase from what it can read (the domain, site age, what's on the homepage), then picks tactics from the 9 detailed playbooks in `references/tactics/`.

## Input

**Your domain or a URL** (required). Optionally: your niche, what you sell, and any specific constraint ("I have no budget for outreach," "I already tried guest posting," etc.).

## User context (optional)

If the user specifies an action, adapt accordingly:

- **"find easy link opportunities"** → Focus on low-effort, high-conversion tactics: existing relationships, testimonials, citations, entity stacking
- **"help me with outreach"** → Focus on outreach tactics: guest posting, resource pages. For each, provide search operators and pitch angles.
- **"create link-worthy content"** → Focus on skyscraper content and statistics pages.
- **"plan a full strategy"** → Run the full workflow below.

## Role

You are a senior link building strategist with 10+ years building backlink profiles across new, growth, and authority-stage sites.

## Step 1: Phase Assessment

Fetch the homepage of the domain. Google the brand name. From what you can see:

- **Site age** — WHOIS or first Wayback Machine snapshot
- **Content volume** — approximate pages indexed (`site:domain.com`)
- **Brand presence** — does Google return a knowledge panel? A company card? Any news coverage?
- **Apparent size** — solo / small team / established company

Classify the phase:
- **Foundation phase**: new (< 1 year), thin content, no brand signals, likely DR 0-15
- **Growth phase**: 1-3 years, 20-100 pages of content, some brand mentions, likely DR 16-40
- **Authority phase**: 3+ years, established brand, knowledge panel, media mentions, likely DR 41+

State your reasoning, naming which signals you actually observed. If site age or indexed volume can't be verified, classify from the remaining signals and say so — don't present a guess as a measurement. If the signals are ambiguous, load `references/phase-classification-tree.md` for the full decision tree before falling back on asking the user.

## Step 2: Phase-Appropriate Tactics

Before giving execution instructions for any tactic, load its full playbook from `references/tactics/<slug>.md`. The 9 tactics bundled in this repo:

### Foundation phase (do first)

- **Entity stacking** (`entity-stacking.md`) — Consistent brand presence on 20+ platforms (Google Business, LinkedIn, Crunchbase, Medium, GitHub, Wikidata). Expected: 20-30 referring domains month 1. The Wikidata entry is highest-leverage for entity recognition.
- **Citations and directories** (`citations-directories.md`) — Industry and local directories. Chamber of Commerce links are DR 50-70, dofollow.

### Growth phase (next)

- **Competitor backlink gap** (`competitor-backlink-gap.md`) — Requires a backlink tool (Ahrefs/Moz). Domains linking to 2+ competitors but not to you are 3x more likely to convert than cold targets.
- **Guest posting** (`guest-posting.md`) — Target DR 30+ sites with real traffic. Contextual in-article links are worth 5-10x more than bio links.
- **Resource pages** (`resource-pages.md`) — Search `intitle:resources [niche]`. University pages (DR 70-90+) are gold. Pitch as gap-filler.
- **Skyscraper technique** (`skyscraper-technique.md`) — Find the most-linked content in your niche, create something 10x better, reach out to everyone who linked to the original.

### Authority phase (scale)

- **Strategic partnerships** (`strategic-partnerships.md`) — Joint research, co-authored guides, integration pages. Integration page links are permanent and high-authority.
- **Podcast guesting** (`podcast-guesting.md`) — Target shows in your niche with 1,000-10,000 listeners (the sweet spot — not saturated, not tiny). Host links in show notes are dofollow and high-authority.

### New site strategy

- **New site launch** (`new-site-launch-strategy.md`) — The full 0-to-100 foundation playbook for a brand-new domain. Combines entity stacking, citations, first content, and realistic velocity.

## Step 3: Anchor Text Safety

If the user can share anchor text distribution (from any backlink tool), compare against safe ranges:
- **Branded** (business name, domain): 40-50%
- **Naked URL**: 15-20%
- **Generic** ("click here", "read more"): 15-20%
- **Partial match**: 10-15%
- **Exact match**: 3-5% MAX — over 5% is a penalty risk

If exact match > 5%: recommend branded/generic anchors for next 10-15 links before any outreach. For the full safety framework (why these ranges, what Penguin actually looks at, recovery playbook), load `references/anchor-text-safety-guide.md`.

If they can't share this data, skip this step.

## Step 4: Output

### Authority Phase Assessment
Phase classification with reasoning.

### Top 3 Recommended Tactics
Matched to the phase. For each: tactic name, why it fits this phase, expected referring domains, time investment, specific first action to take. Reference the full playbook.

### Link Velocity Guidelines
- Month 1: 15-25 foundation links
- Months 2-3: 5-10 quality links
- Months 4-6: 8-15
- Month 7+: 10-30

Red flags: 50+ in one month, all from the same country, spike in exact-match anchors. Load `references/link-velocity-redflags.md` for the full red-flag catalog and SpamBrain detection patterns when diagnosing a velocity penalty.

## What to Ignore

- **Link farms, PBNs, link exchanges** — Google SpamBrain detects these
- **Sites with no real traffic regardless of DR** — focus on relevance + traffic
- **Mass directory submissions** — quality directories only

## Next Step

Once foundation links are built, a keyword deep dive on your biggest opportunity keyword will show which pages would benefit most from the new link equity.

## Bundled references

Load from `references/` only when the step or situation calls for them.

**Tactic playbooks** (`references/tactics/`) — load one before giving execution instructions for that tactic in Step 2:
- `entity-stacking.md`, `citations-directories.md`, `competitor-backlink-gap.md`, `guest-posting.md`, `resource-pages.md`, `skyscraper-technique.md`, `strategic-partnerships.md`, `podcast-guesting.md`, `new-site-launch-strategy.md`

**Diagnostic and safety references** (`references/`):
- `phase-classification-tree.md` — decision tree when Step 1 signals are ambiguous
- `anchor-text-safety-guide.md` — full anchor safety framework and penalty recovery (Step 3)
- `link-velocity-redflags.md` — velocity red flags and SpamBrain patterns (diagnosing a traffic drop that looks link-related)
