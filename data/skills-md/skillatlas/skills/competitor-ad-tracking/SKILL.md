---
name: competitor-ad-tracking
description: Use when the user wants to retrieve, track, compare, or analyze competitor ads from ad libraries, including Meta/Facebook Ad Library, Google ads by domain, LinkedIn ads, and Reddit ad searches, for messaging audits, creative research, launch monitoring, offer analysis, or paid competitive intelligence.
license: MIT
prerequisites:
  - Scrape Creators API key
metadata:
  author: Skill Atlas
  version: "0.1.0"
  homepage: https://skillatlas.sh/
---

# Competitor Ad Tracking

Use this skill when the task is paid-ad-library competitor research first and platform choice second. The job is not just to pull ads. The job is to pull the right ads, preserve the raw evidence, and turn them into useful competitive signal.

## Prerequisites

- Install the CLI once:

```bash
npm install -g scrapesocial
```

- Authenticate with `SCRAPECREATORS_API_KEY` or `--api-key`.
- Start from the strongest identifier you have:
  - Domain or website: start with Google ads
  - Brand or company name: start with Meta or LinkedIn
  - Ad URL or ad ID: use the detail command directly
  - Topic, pain point, or offer: use keyword search commands first

## What makes ad extraction valuable

A raw ad dump is low value. A good extraction answers:

- What problems is this competitor paying to repeat?
- Which offers, proofs, and CTAs recur across multiple ads?
- Which creative formats keep showing up?
- What changed across dates, countries, or languages?
- Where is the whitespace for an original angle?

Always try to produce:

- An ad inventory
- A message map
- A creative-pattern summary
- A change log if this is a repeat pull
- A short "what to test differently" note

## Guardrails

- Never copy competitor headlines, scripts, visual compositions, or claims directly.
- Use extracted ads to understand category patterns, not to produce near-clones.
- Do not claim performance winners unless the payload actually includes performance data.
- Treat recurrence, freshness, and breadth as priority signals, not proof of effectiveness.
- If advertiser identity is ambiguous, stop and confirm the exact company before pulling more data.

## Platform routing

| Need                               | Best command path                                                           | Why                                             |
| ---------------------------------- | --------------------------------------------------------------------------- | ----------------------------------------------- |
| Known competitor website or domain | `google ads advertisers get --domain`                                       | Strongest domain-native lookup in this CLI.     |
| Known competitor brand on Meta     | `facebook ads companies search` -> `facebook ads companies get`             | Best advertiser-level Meta Ad Library workflow. |
| Known competitor brand on LinkedIn | `linkedin ads search --company`                                             | Direct company-level search.                    |
| Topic or pain-point scan           | `facebook ads search`, `linkedin ads search --keyword`, `reddit ads search` | Best when the advertiser is not known yet.      |
| One standout ad                    | `facebook ads get`, `google ads get`, `linkedin ads get`, `reddit ads get`  | Pull detail only after shortlist.               |

## Command notes

- `facebook ads companies search`
  - Use to find advertiser names and page IDs from a brand query.
- `facebook ads companies get`
  - Use to list ads for one advertiser.
  - `--sort-by total_impressions` is better for repeated and higher-reach signal.
  - `--sort-by relevancy_monthly_grouped` is better for current messaging.
- `facebook ads get`
  - Use to inspect one specific ad.
  - Add `--get-transcript` for short video ads when script text matters.
- `google ads advertisers get`
  - Use when the user gives a competitor site or domain.
  - Add `--get-ad-details` only after shortlisting because it costs 25 credits.
- `google ads get`
  - Use to fetch one Google ad by URL.
- `linkedin ads search`
  - Use `--company` or `--company-id` for a known brand.
  - Use `--keyword` for category scans.
  - Reuse `--pagination-token` exactly as returned.
- `linkedin ads get`
  - Use to fetch one LinkedIn ad by URL.
- `reddit ads search`
  - Use for category-level and message-level scans.
  - It is weaker than Meta or Google for exact advertiser tracking.
- `reddit ads get`
  - Use to inspect one Reddit ad after shortlisting.

## High-value workflows

### 1. Known competitor, single-date snapshot

Use this when the user wants "show me Acme's current ads."

1. Make a dated folder so future pulls are comparable.
2. Pull Google by domain if the competitor site is known.
3. Pull Meta by advertiser if the brand name is known.
4. Pull LinkedIn by company if B2B or hiring or product marketing signals matter.
5. Use detail commands only on representative or strategically important ads.

Example:

```bash
mkdir -p research/acme/2026-03-08

scrapesocial google ads advertisers get \
  --domain acme.com \
  --start-date 2026-02-01 \
  --end-date 2026-03-08 \
  > research/acme/2026-03-08/google-ads-page1.json

scrapesocial facebook ads companies search \
  --query "Acme" \
  > research/acme/2026-03-08/meta-company-search.json

scrapesocial facebook ads companies get \
  --page-id <page-id> \
  --country US \
  --status ACTIVE \
  --sort-by relevancy_monthly_grouped \
  --trim \
  > research/acme/2026-03-08/meta-ads-page1.json

scrapesocial linkedin ads search \
  --company "Acme" \
  --countries US \
  --start-date 2026-02-01 \
  --end-date 2026-03-08 \
  > research/acme/2026-03-08/linkedin-ads-page1.json
```

Good follow-up questions:

- Are they pushing the same offer on every platform?
- Are the landing pages product pages, comparison pages, webinars, free trials, or demos?
- Are they talking to one segment or several?

### 2. Topic-first market scan

Use this when the user knows the category or pain point, but not the advertiser mix yet.

1. Search Meta, LinkedIn, and Reddit by keyword.
2. Note the advertisers that appear repeatedly.
3. Pivot into advertiser-level pulls for the most relevant competitors.

Example:

```bash
scrapesocial facebook ads search \
  --query "project management" \
  --country US \
  --status ACTIVE \
  --media-type VIDEO \
  --trim

scrapesocial linkedin ads search \
  --keyword "project management" \
  --countries US

scrapesocial reddit ads search \
  --query "project management" \
  --industries TECH_B2B \
  --formats VIDEO
```

This is valuable for:

- Identifying category hooks
- Seeing how competitors name the problem
- Spotting recurring offers and CTA structures

### 3. Standout-ad deep dive

Use this after the list pull, not before.

1. Shortlist ads that repeat, look new, or represent a clear strategic angle.
2. Pull detailed objects for only those ads.
3. For short video ads on Meta, add transcripts.

Example:

```bash
scrapesocial facebook ads get --id <ad-id> --get-transcript
scrapesocial google ads get --url <ad-url>
scrapesocial linkedin ads get --url <ad-url>
scrapesocial reddit ads get --id <ad-id>
```

Look for:

- Exact hook and promise
- Proof element: testimonial, number, customer logo, stat, or demo
- Offer type: free trial, demo, guide, discount, comparison, or webinar
- CTA language
- Landing-page path or page type if exposed

### 4. Repeat tracking over time

Use this when the user wants monitoring rather than a one-off pull.

1. Save raw outputs in `research/<competitor>/<YYYY-MM-DD>/`.
2. Reuse the same filters every run so comparisons stay valid.
3. Compare:
   - New ads
   - Removed ads
   - New offers
   - New landing pages
   - New countries or languages
   - Creative-format shifts
4. Only deep-dive net-new or strategically important ads.

A repeat pull is more valuable than a single pull because it shows:

- What the competitor keeps funding
- What they are testing now
- What campaigns appear seasonal or launch-driven
- Whether positioning is changing

## What to extract from each ad

Do not just save the raw JSON and stop. Pull out:

- Platform
- Advertiser
- Ad ID or URL
- Date range or recency fields if present
- Country and language filters used
- Headline or primary copy
- CTA
- Media type
- Transcript or voiceover text if available
- Landing page URL or domain if present
- Offer
- Proof
- Hook or problem statement

## How to turn extracted ads into useful analysis

### Message map

For each competitor, group ads by:

- Problem
- Desired outcome
- Proof
- Offer
- Audience segment
- Funnel stage

### Creative map

Track whether the ads lean on:

- Product UI or demo
- Founder or spokesperson
- Testimonial or social proof
- Before and after comparison
- Listicle or "mistakes" framing
- Event, webinar, or downloadable lead magnet
- Direct-response offer

### Change log

Compare snapshots over time for:

- Net-new messages
- Retired messages
- New product launches
- Pricing or discount changes
- Localization or expansion
- Enterprise versus SMB split

### Whitespace

The highest-value output is not "here is what they do." It is:

- What every competitor says
- What no one is saying
- Which objections are overworked
- Which proof points are weak or repetitive
- Where an original position is available

## Evidence hierarchy

Rank confidence like this:

1. Same hook repeated across many ads
2. Same hook repeated across platforms
3. Same hook persists across multiple dates
4. Same hook is paired with multiple creative variants
5. Same hook is tied to multiple landing pages or offers

One isolated ad is weak signal. Repetition is stronger signal.

## Important limits

- Ad libraries show existence, messaging, and some metadata. They do not automatically tell you revenue, ROAS, conversion rate, or true winner status.
- More ads can mean localization, testing, or coverage, not necessarily better performance.
- No single platform gives a complete view of the competitor's paid program.
- Reddit is better for theme discovery than exact advertiser monitoring.

## Minimal examples

```bash
scrapesocial facebook ads companies search --query "Notion"
scrapesocial facebook ads companies get --page-id <page-id> --status ACTIVE --country US --trim
scrapesocial facebook ads get --id <ad-id> --get-transcript

scrapesocial google ads advertisers get --domain notion.so
scrapesocial google ads get --url <ad-url>

scrapesocial linkedin ads search --company "Notion" --countries US
scrapesocial linkedin ads search --keyword "knowledge management" --countries US
scrapesocial linkedin ads get --url <ad-url>

scrapesocial reddit ads search --query "knowledge management" --industries TECH_B2B
scrapesocial reddit ads get --id <ad-id>
```

## Pairing notes

- Pair with `skillatlas/scrapesocial-facebook` when the user wants paid and organic Meta activity side by side.
- Pair with `skillatlas/scrapesocial-reddit` when the user also needs demand language and objections from organic discussions.
- Pair with `skillatlas/scrapesocial-youtube` or `skillatlas/scrapesocial-tiktok` if the user wants to compare paid creative with organic creative systems.
