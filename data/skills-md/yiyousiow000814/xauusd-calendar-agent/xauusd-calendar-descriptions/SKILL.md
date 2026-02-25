---
name: xauusd-calendar-descriptions
description: Human-written economic calendar event descriptions for a global calendar with XAUUSD relevance and impact rules. Use when writing or reviewing event descriptions or notes for economic calendar entries, ensuring concise non-robotic language and conditional XAUUSD impact guidance.
---

# SKILL.md - XAUUSD Economic Calendar Descriptions (Global, Human-Readable, Research-First)

## Goal

Generate concise, human-readable descriptions for economic calendar events in a global calendar, with optional impact notes only when relevant to XAUUSD.

## Scope

* Calendar includes all countries/regions.
* Asset focus is XAUUSD.
* Output: 1-2 sentences per event.

## Output Rules

1. At most two sentences.
2. Sentence 1 (always): Define what the event measures/decides using precise measurement terms:
   * rate, policy decision, index, diffusion index, weekly number, % change, balance, statement, minutes, auction
3. Sentence 2 (optional): Add only if the event can plausibly influence XAUUSD via major pricing channels.

## Research-First Requirement (Stops Copy-Paste Notes)

Do not reuse a generic explanation across multiple events (for example, "CPI measures inflation") unless you verified it for that exact event.

Minimum bar per event:

1. Find at least one credible source describing the indicator/decision for that exact country/issuer.
2. Extract one short supporting excerpt (one line is enough).
3. Only then write the 1-2 sentence note in natural English.

Source preference order:

1. Official publisher (central bank / statistics office / ministry / exchange / treasury / agency).
2. Official press release / PDF / page for that indicator.
3. Reputable financial calendar / major news outlet as fallback when official sources are hard to access.

## Efficiency Without Template Notes (Cache + Official "Hub" Pages)

Goal: keep the "one-by-one" evidence standard while reducing repeated web searches and minimizing token usage.

Principles:

1. Each event still needs its own supporting excerpt (one line) and its own final note.
2. Efficiency comes from reusing official sources (not reusing wording).

## Quota-Friendly Mode (No Agents)

If you cannot use multiple agents (quota constraints), do not switch to generic template notes.
Keep the same per-event evidence bar and make research faster by:

1. Using the helper script to search and cache candidate pages (`tmp/sources/`).
2. Restricting searches to official domains with `site:` (for example, `site:bls.gov`, `site:bea.gov`, `site:census.gov`).
3. Reusing cached official "hub" pages for related variants (level, MoM, YoY) while still writing each event note individually.

## This Repo's Exact Workflow (What "Good" Looks Like Here)

When following this skill in this repository, the expected workflow is:

1. Pick exactly one event id to work on (for example, `USD::pce deflator::m/m`).
2. Find at least one credible source line for that exact event (prefer official publisher pages).
3. Cache sources under `tmp/` (gitignored), extract a one-line excerpt, and record it in `tmp/event_notes_research_log.md` (do not commit).
4. Write/replace the note in `event_notes.json` in natural English (1-2 sentences).
5. Run the repo quality gate (`python scripts/calendar/build_event_notes.py`) and rewrite if it flags anything.

### Fast, reproducible web research (recommended)

Use `r.jina.ai` for both search and fetching readable page text, then cache locally:

```powershell
$ProgressPreference = 'SilentlyContinue'
New-Item -ItemType Directory -Force tmp/sources | Out-Null

# 1) Search (DuckDuckGo HTML via r.jina.ai)
$q = [uri]::EscapeDataString('BLS CPI definition prices paid by urban consumers market basket')
(Invoke-WebRequest -UseBasicParsing "https://r.jina.ai/http://duckduckgo.com/html/?q=$q").Content |
  Set-Content -Encoding utf8 tmp/sources/ddg_cpi.md

# 2) Fetch the best official hit (again via r.jina.ai) and cache it
$url = 'https://www.bls.gov/cpi/'
(Invoke-WebRequest -UseBasicParsing "https://r.jina.ai/$url").Content |
  Set-Content -Encoding utf8 tmp/sources/bls_cpi.md

# 3) Extract one supporting excerpt line for evidence
Select-String -Path tmp/sources/bls_cpi.md -Pattern 'average change over time' | Select-Object -First 1
```

You can also use the helper script for one event id:

```powershell
python scripts/calendar/research_event_note_sources.py --event-id "USD::pce deflator::m/m"
```

It does not edit JSON; it only helps you find/copy evidence lines faster.

### When official sites block CLI fetching (WAF, SPA, 403)

Some official sites are hard to fetch from a CLI (CloudFront 403, "Request Rejected", single-page apps).
Do not fall back to generic template notes.

Use this order:

1. Official PDF press release / methodology note (often easier to fetch than the main site).
2. Official API or machine-readable endpoint (JSON/CSV) if the institution provides it.
3. An official secondary domain or a machine-readable mirror that contains the same text verbatim.
4. Only if all official routes are blocked: a reputable secondary source (major financial calendar or major news outlet), and keep the note strictly definitional.

### Evidence logging (must do per event)

Append one short block per event to `tmp/event_notes_research_log.md`:

```text
EVENT: USD::cpi::m/m
SOURCE: https://www.bls.gov/cpi/
EXCERPT: "The Consumer Price Index (CPI) is a measure of the average change over time in the prices paid by urban consumers for a market basket..."
NOTE: (paste your final 1-2 sentence note)
```

## Repo Quality Gates (Important)

This repo enforces a couple of non-obvious checks via `python scripts/calendar/build_event_notes.py`:

1. Banned phrases: never use `tracks` or `growth indicator` anywhere in notes.
2. Sentence limit: a simple punctuation heuristic counts `. ! ?` as sentence endings.
   * Avoid abbreviations with periods like `U.S.` because they can be miscounted as extra sentences.
   * Prefer `US` instead of `U.S.` and keep punctuation minimal.
3. ASCII-safe text: avoid curly quotes (use `'` instead of `’`) so JSON stays clean and consistent.

Recommended workflow:

1. Identify the official publisher domain for the event (central bank, statistics office, exchange, etc.).
2. Find 1-3 "hub" pages that cover many indicators for that publisher (glossary, methodology, release landing page, catalog page).
3. Cache hub pages locally under `tmp/` (gitignored) so you can extract excerpts offline for many events.
4. For each event, extract a one-line excerpt from cached content (or fetch a specific page if needed), then write the note.
5. Record evidence per event (URL + excerpt) in `tmp/event_notes_research_log.md` (do not commit).

Optional helper script:

* Use `scripts/calendar/research_event_note_sources.py` to quickly collect candidate sources and
  definition-like excerpt lines for one event id.
* The script does not change any JSON; it only caches pages under `tmp/sources/` and prints
  copy-paste evidence candidates.

Examples:

```powershell
python scripts/calendar/research_event_note_sources.py --event-id "USD::m2 money supply::m/m"
python scripts/calendar/research_event_note_sources.py --event-id "USD::opec monthly report::none" --max-results 8
python scripts/calendar/research_event_note_sources.py --event-id "EUR::cpi::y/y" --query "site:ec.europa.eu HICP year-on-year change definition"
```

PowerShell caching pattern:

```powershell
$ProgressPreference = 'SilentlyContinue'
New-Item -ItemType Directory -Force tmp/sources | Out-Null

# Cache an official hub page once
$url = 'https://www.abs.gov.au/statistics/economy/price-indexes-and-inflation/consumer-price-index-australia/latest-release'
$cache = 'tmp/sources/abs_cpi_latest_release.md'
(Invoke-WebRequest -UseBasicParsing ("https://r.jina.ai/$url")).Content | Set-Content -Encoding utf8 $cache

# For each event, extract a supporting excerpt from the cached file
Get-Content $cache | Select-String -Pattern 'measures household inflation' -Context 0,0 | Select-Object -First 1
```

Search strategy (high signal, low noise):

* Prefer `site:<official-domain> <indicator name> definition` queries.
* Use `https://r.jina.ai/http://duckduckgo.com/html/?q=...` for search when direct access is blocked.
* Only fall back to non-official sources when official pages are inaccessible.

Keep diffusion-index thresholds:

* For PMI-style diffusion indexes, keep the threshold explanation when it is relevant and known (for example, `50 = expansion`).
  Do not delete this detail just to shorten the note; it materially improves usability for non-specialists.

## Relevance Decision (When to add Sentence 2)

Add an impact sentence only if at least one condition is true:

### High relevance (usually add impact)

* Major central bank policy decisions/guidance from systemically important economies (rate decision, statement, minutes, press conference, key testimony/speech)
* Major inflation prints that can shift global rate expectations (headline/core CPI or equivalents, PCE equivalents, PPI equivalents - especially for large economies)
* Major labor prints that move rate expectations or risk sentiment (jobs/payrolls, unemployment rate, wages; weekly claims where applicable)
* Major activity/risk indicators from large economies (PMI/ISM equivalents, GDP, retail sales, industrial production)

### Medium relevance (add impact only if widely watched / high-impact on the calendar)

* Secondary inflation/labor/activity data from mid-sized economies
* Trade balance/current account when it is a market focus driver
* Long-dated government bond auctions (can affect yields/rates narrative)

### Low relevance (do NOT add impact)

* Small-country second-tier releases unlikely to move global USD/yields/risk
* Niche sector indicators with limited market attention
* Local events with little spillover

Default behavior: If uncertain, omit Sentence 2 (definition-only is always acceptable).

## Impact Sentence Rules (If Sentence 2 is used)

Impact must be conditional and relative to expectations:

* Use: "higher-than-expected / lower-than-expected (vs forecast)"
* For central banks: "hawkish/dovish surprise"

Impact must explain through one primary channel (pick the most relevant, do not stack multiple):

1. USD and (real) yields / rate expectations
2. Risk sentiment / safe-haven demand
3. Inflation expectations feeding into yields

Keep it realistic: use can / may / often, not absolute "will".

## Banned / Anti-Robotic Rules

* Never use: "tracks"
* Never call everything a: "growth indicator"
* Never repeat the event name as its own definition
* Never prefix events with currency codes as if currency = country
* Avoid filler like "important indicator" or "for the economy"; say what it measures instead
* Avoid long, encyclopedic sentences and heavy parentheses

## No-Code / No-Batch-Generation Rule (Must Follow)

* Do not generate descriptions "by code." Do not output any code, pseudocode, scripts, loops, batch logic, JSON batch structures, placeholders, or variable-style tokens (for example, anything like `{Country}` / `{Period}` / bracketed template fields).
* Each event description must read like it was individually written in natural language, even if there are thousands of events. Avoid uniform "copy-paste sentence skeletons" that clearly look programmatically stitched.
* Do not mention the generation method (no meta text like "auto-generated", "using a template", "based on rules"). Only output the final description text.

## Low-Relevance Handling (Optional)

If you must mention impact but relevance is low, use one restrained line only:

* "Usually limited direct impact on XAUUSD unless it shifts broader USD, yields, or risk sentiment."

## Quality Gate (Self-check every event; rewrite if any fail)

Fail if:

* Banned phrases appear ("tracks", "growth indicator")
* More than 2 sentences
* Sentence 1 does not clearly define what it measures/decides
* Sentence 2 exists but lacks higher/lower-than-expected or hawkish/dovish framing
* Impact does not connect to USD/yields/risk/safe-haven in a plausible way
* Text contains any placeholders/variables or looks like a batch template output
* You did not do per-event source verification (Research-First Requirement)

## Style Targets (Make it sound human)

* Use simple verbs: measures, sets, reflects, shows, provides
* Prefer concrete nouns: reading, index, policy rate, price pressures, weekly claims
* Keep the tone trader-readable: short, direct, no fluff

## Examples (Global calendar, XAUUSD-focused)

* "Eurozone CPI (YoY) measures consumer inflation. Higher-than-expected inflation can raise yield expectations and pressure XAUUSD; softer inflation can support it."
* "Bank of Japan Rate Decision sets the policy rate. A more hawkish-than-expected outcome can lift yields and weigh on XAUUSD; a dovish surprise can support it."
* "China PMI is a diffusion index of business activity (50 = expansion). A weaker-than-expected reading can hurt risk sentiment and support XAUUSD as a safe haven."
* "Norway Retail Sales (MoM) measures the monthly % change in consumer spending." (definition-only)

## Core Execution Instruction (Use verbatim)

For each economic calendar event, write a short human-readable description for XAUUSD.
Use at most two sentences. The first sentence must define what the event measures or decides using precise measurement terms (rate/index/diffusion index/weekly number/% change/balance/statement/minutes/auction).
Before writing, do per-event web research: find at least one credible source for that exact event (prefer official publishers), extract a short supporting excerpt, and only then write the note. Do not reuse identical wording across countries unless the source supports that similarity.
Use caching for efficiency: prefer official hub pages, save them under `tmp/`, and extract per-event excerpts from cached sources. This reduces search overhead without lowering the evidence standard.
Only add a second sentence if the event is meaningfully relevant to XAUUSD (major central bank policy/guidance, major inflation, major labor, or major activity/risk indicators from widely watched economies, or anything that can shift global USD and yield expectations or risk sentiment).
If you add impact, it must be conditional and relative to expectations: use "higher-than-expected / lower-than-expected (vs forecast)" or "hawkish/dovish surprise", and explain via USD, yields/real yields, rate expectations, or risk sentiment/safe-haven demand.
Never use "tracks", never call everything a "growth indicator", never repeat the event name as its own definition, and never prefix events with currency codes as if currency = country.
For PMI-style diffusion indexes, keep the threshold explanation when relevant (for example, 50 = expansion).
If relevance is low, write only the definition (or optionally one very restrained line saying direct impact is usually limited). After writing, self-check and rewrite if any rule is violated.
Do not output any code, placeholders, or batch-template text. Each description must read like it was individually written.
