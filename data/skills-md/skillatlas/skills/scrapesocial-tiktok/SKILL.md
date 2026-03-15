---
name: scrapesocial-tiktok
description: Use when the user wants TikTok research or workflow guidance for lead generation, influencer discovery, brand monitoring, competitor analysis, content analytics, trend research, or audience analysis, including account analysis, creator discovery, video inspection, comment scraping, transcript extraction, hashtag or song research, and TikTok Shop or product research.
license: MIT
prerequisites:
  - Scrape Creators API key
metadata:
  author: Skill Atlas
  version: "0.1.2"
  homepage: https://skillatlas.sh/
---

# Scrapesocial TikTok

Use this skill when the task is about structured TikTok research, analysis, or discovery.

## Prerequisites

- A Scrape Creators API key is required for this skill. Get one at [scrapecreators.com](https://scrapecreators.com).

Start by identifying the job to be done, then choose the smallest command that answers it. Prefer a narrow lookup before broad searches when you already have a handle or URL.

## Quick start

Install the CLI once:

```bash
npm install -g scrapesocial@0.1.0
```

Authenticate first:

```bash
export SCRAPECREATORS_API_KEY=...
```

Basic invocation:

```bash
scrapesocial tiktok ...
```

## Goal-led workflows

| Goal                 | When to use this skill                                                                                                                              | How to start                                                                                                                                                                                       |
| -------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Lead generation      | Use it for creator, seller, and shop discovery in consumer, creator, or commerce niches.                                                            | Start with `tiktok users search`, `tiktok users popular`, or `tiktok shops search`, then qualify candidates with `tiktok users profile`, `tiktok users audience`, or `tiktok shops products list`. |
| Influencer discovery | Use it when the user wants to find creators in a niche and verify whether their audience and content style fit.                                     | Start with `tiktok users search`, `tiktok videos search`, or `tiktok videos trending`, then validate with `tiktok users profile`, `tiktok users audience`, and `tiktok users videos`.              |
| Brand monitoring     | Use it to track known creators, brand accounts, or TikTok Shop sellers.                                                                             | Start with `tiktok users profile`, `tiktok users videos`, or `tiktok shops products list`, then inspect specific videos with `tiktok videos get` or `tiktok videos comments`.                      |
| Competitor analysis  | Use it to compare creators, content strategies, sellers, products, and audience fit.                                                                | Start with `tiktok users profile`, `tiktok users videos`, `tiktok users following`, `tiktok shops search`, and `tiktok shops products reviews`.                                                    |
| Content analytics    | Use it to explain why specific videos, hooks, scripts, or comment sections matter.                                                                  | Start with `tiktok users videos --sort-by popular` or `tiktok videos search`, then drill into winners with `tiktok videos get`, `tiktok videos transcript`, and `tiktok videos comments`.          |
| Trend research       | Use it when the user wants the strongest discovery surface for fast-moving creators, sounds, hashtags, and formats.                                 | Start with `tiktok videos trending`, `tiktok hashtags popular`, `tiktok songs popular`, or `tiktok videos search`.                                                                                 |
| Audience analysis    | Use it when the user needs the strongest audience workflow in this repo. It supports both explicit audience data and qualitative audience reaction. | Start with `tiktok users audience`, then layer in `tiktok videos comments` or `tiktok users followers` when sampling community fit.                                                                |

## Choose the right command

### Account and creator research

Use these when the user wants to understand a specific creator or discover similar creators.

- `tiktok users profile`
  Best for: basic profile data, bio, stats, profile metadata.
  Use first when you only need a creator snapshot.
- `tiktok users audience`
  Best for: audience demographics and market breakdowns.
  Use when the user asks who follows a creator, audience composition, or geo/demographic fit.
- `tiktok users videos`
  Best for: a creator's published videos.
  Use when reviewing recent output, top-performing posts, or building a content sample.
- `tiktok users live`
  Best for: checking whether an account is live and inspecting live metadata.
- `tiktok users following`
  Best for: who a creator follows.
  Use for competitive mapping, creator clustering, or inspiration research.
- `tiktok users followers`
  Best for: follower lists.
  Use when the user wants overlap analysis, community sampling, or lead discovery.
- `tiktok users search`
  Best for: finding creators by keyword.
  Use when you do not yet know the exact handle.
- `tiktok users popular`
  Best for: broad discovery of large or fast-rising accounts.

### Video analysis

Use these when the user cares about a specific video or wants to find videos on a topic.

- `tiktok videos get`
  Best for: one video's full details.
  Use when you already have a TikTok URL and need metadata, engagement, or transcript-enabled detail.
- `tiktok videos transcript`
  Best for: spoken content extraction.
  Use for summarization, quote extraction, hooks analysis, or repurposing scripts.
- `tiktok videos comments`
  Best for: audience reaction and qualitative research.
  Use when the user wants sentiment, objections, FAQs, or language straight from viewers.
- `tiktok videos search --query`
  Best for: topic-based content discovery.
  Use for researching how TikTok is talking about a niche, product, event, or keyword.
- `tiktok videos search --hashtag`
  Best for: hashtag-centric research.
  Use when the user already knows the hashtag they want to inspect.
- `tiktok videos search --top --query`
  Best for: top-result discovery rather than general recall.
  Use when quality matters more than completeness.
- `tiktok videos popular`
  Best for: generally popular videos.
- `tiktok videos trending`
  Best for: what's trending now in a region.
  Use this for trend spotting, creative monitoring, and fast-moving market checks.

### Trend and culture signals

Use these when the user wants to understand what is taking off on TikTok.

- `tiktok songs popular`
  Best for: current music signals.
  Use for trend monitoring, creative inspiration, and audio selection research.
- `tiktok songs get`
  Best for: metadata on a known clip ID.
- `tiktok songs videos`
  Best for: videos using a specific sound.
  Use when the user wants concrete examples of how a sound is being used.
- `tiktok hashtags popular`
  Best for: rising or established hashtag trends by market or industry.
  Use for campaign research, niche mapping, or content ideation.

### TikTok Shop research

Use these when the user is researching products, sellers, or commerce behavior.

- `tiktok shops search`
  Best for: finding shops by keyword.
- `tiktok shops products list`
  Best for: listing products from a shop page.
  Use when the user wants assortment, catalog breadth, or seller merchandising analysis.
- `tiktok shops products get`
  Best for: one product page in detail.
  Use when the user wants price, offer, product metadata, or related-video context.
- `tiktok shops products reviews`
  Best for: buyer feedback.
  Use when the user wants objections, complaints, praise themes, or review mining.

## Common workflows

### Understand a creator

1. Run `tiktok users profile`.
2. If audience fit matters, run `tiktok users audience`.
3. If content strategy matters, run `tiktok users videos --sort-by popular` and inspect a sample.

### Research a topic or trend

1. Start with `tiktok videos search --query` or `tiktok videos search --hashtag`.
2. Add `tiktok videos trending` or `tiktok hashtags popular` for broader context.
3. Pull `tiktok videos transcript` or `tiktok videos comments` on standout posts for qualitative analysis.

### Investigate a specific video

1. Run `tiktok videos get --video-url ...`.
2. Add `tiktok videos transcript` if spoken content matters.
3. Add `tiktok videos comments` if audience reaction matters.

### Research a commerce niche

1. Start with `tiktok shops search`.
2. Inspect a seller via `tiktok shops products list`.
3. Deep-dive one SKU with `tiktok shops products get` and `tiktok shops products reviews`.

## Important operating notes

- Use `--trim` for list-heavy commands when the user wants a smaller payload.
- Use pagination flags like `--cursor`, `--max-cursor`, `--min-time`, or `--page` when the first response is not enough.
- Use `--region` or `--country-code` when the user cares about a specific market. Trend outputs can differ materially by geography.
- If you already have a TikTok user ID or product ID and the command supports it, pass it to make follow-up requests more direct.
- Prefer URL-based commands for exact lookups and search commands for discovery.
- When the task is analysis rather than raw retrieval, fetch only the minimum data needed and then summarize patterns for the user.

## Example requests that should trigger this skill

- "Analyze this TikTok creator's audience and recent videos."
- "Find trending TikTok videos about cold plunge."
- "Pull comments from this TikTok and tell me the main objections."
- "Show me popular TikTok songs in the US this month."
- "Research TikTok Shop competitors for collagen peptides."
