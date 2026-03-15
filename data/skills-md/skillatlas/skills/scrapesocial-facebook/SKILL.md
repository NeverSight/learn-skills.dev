---
name: scrapesocial-facebook
description: Use when the user wants Facebook research or workflow guidance for lead generation, influencer discovery, brand monitoring, competitor analysis, content analytics, trend research, or audience analysis, including page or profile audits, post, reel, photo, or comment extraction, group monitoring, transcript retrieval, and Facebook ad or advertiser analysis.
license: MIT
prerequisites:
  - Scrape Creators API key
metadata:
  author: Skill Atlas
  version: "0.1.2"
  homepage: https://skillatlas.sh/
---

# Scrapesocial Facebook

Use this skill for Facebook research and analysis tasks. It maps the user's goal to the right `scrapesocial` Facebook command.

## Prerequisites

- A Scrape Creators API key is required for this skill. Get one at [scrapecreators.com](https://scrapecreators.com).

## Quick start

- Install the CLI once:

```bash
npm install -g scrapesocial
```

- Ensure authentication is available through `SCRAPECREATORS_API_KEY` or `--api-key`.
- Start from the most stable identifier you have:
  - A page/profile URL for organic Facebook data
  - A post URL for a single post, transcript, or comment thread
  - A group URL for community research
  - A brand name, keyword, page ID, or ad ID for Ad Library work
- Prefer a narrow command first, then paginate or deepen only when needed.

## Goal-led workflows

| Goal                 | When to use this skill                                                                                                              | How to start                                                                                                                                                                        |
| -------------------- | ----------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Lead generation      | Use it to qualify known brands, pages, advertisers, or community-led prospects. It is better for qualification than cold discovery. | Start with `facebook ads companies search` for known brands or `facebook profiles get` for known pages, then expand with `facebook profiles posts` or `facebook ads companies get`. |
| Influencer discovery | Use it to vet known creators or pages surfaced elsewhere and see whether they publish consistently in the niche.                    | Start with `facebook profiles get`, then compare `facebook profiles reels` and `facebook profiles posts`.                                                                           |
| Brand monitoring     | Use it to watch owned pages, groups, and ad activity over time.                                                                     | Start with `facebook profiles posts`, `facebook profiles reels`, `facebook groups posts`, or `facebook ads companies get`, depending on the surface.                                |
| Competitor analysis  | Use it to compare page activity, creative formats, and paid messaging across competitors.                                           | Start with `facebook profiles get` for each page, then use `facebook profiles posts` and `facebook ads companies get` for side-by-side review.                                      |
| Content analytics    | Use it to explain which posts, reels, photos, or ads deserve deeper analysis.                                                       | Start with `facebook profiles posts` or `facebook profiles reels`, then inspect winners with `facebook posts get`, `facebook comments`, or `facebook transcript`.                   |
| Trend research       | Use it for group conversations and ad-library pattern spotting.                                                                     | Start with `facebook groups posts` for discussion trends or `facebook ads search` for creative and message trends.                                                                  |
| Audience analysis    | Use it for qualitative audience language, objections, and reactions. It does not provide demographic audience breakdowns.           | Start with `facebook comments` on representative posts or `facebook groups posts` for community discussion.                                                                         |

## Choose the right command

- `scrapesocial facebook profiles get`
  - Use for page/profile metadata.
  - Good first step for business pages; add `--get-business-hours` when hours matter.

- `scrapesocial facebook profiles posts`
  - Use to collect recent timeline posts from a page or profile.
  - Good for content audits, engagement review, and finding post URLs to inspect further.

- `scrapesocial facebook profiles reels`
  - Use to collect a page's reels feed.
  - Good for short-form creative research and video content tracking.

- `scrapesocial facebook profiles photos`
  - Use to collect a page's photo feed.
  - Good for image creative analysis and gallery extraction.

- `scrapesocial facebook posts get`
  - Use for one post or reel when you need the full object.
  - Add `--get-comments` or `--get-transcript` when you want an initial deep dive in one request.

- `scrapesocial facebook comments`
  - Use to paginate through a post or reel's comments.
  - Prefer `--feedback-id` when available; get it from `facebook posts get`.

- `scrapesocial facebook transcript`
  - Use when you only need the transcript for a post and do not need the rest of the post payload.

- `scrapesocial facebook groups posts`
  - Use to pull posts from a Facebook group.
  - Good for community monitoring, topic discovery, and trend spotting.

- `scrapesocial facebook ads search`
  - Use to search the Meta Ad Library by keyword or theme.
  - Best for market scans, messaging research, and finding ads before you know the advertiser.

- `scrapesocial facebook ads companies search`
  - Use to find advertiser identities and page IDs from a company or brand name.
  - Best first step when the user says "show me this brand's Facebook ads."

- `scrapesocial facebook ads companies get`
  - Use to list ads for a known advertiser.
  - Best when you already have the page ID or have just looked it up.

- `scrapesocial facebook ads get`
  - Use to inspect one specific ad in detail.
  - Add `--get-transcript` for short video ads when transcript text matters.

## Common workflows

### Page or profile audit

1. Run `facebook profiles get` to confirm the page and collect top-level metadata.
2. Run `facebook profiles posts` for the timeline.
3. Add `facebook profiles reels` and `facebook profiles photos` if the user wants a fuller creative inventory.
4. Open individual posts with `facebook posts get` when deeper analysis is needed.

### Post investigation

1. Start with `facebook posts get --url ...`.
2. If you need the first comments or transcript immediately, add `--get-comments` and/or `--get-transcript`.
3. If the thread is long, continue with `facebook comments`, reusing `--feedback-id` from the post payload when available.

### Group research

1. Use `facebook groups posts --url ...`.
2. Adjust `--sort-by` based on the task:
   - `TOP_POSTS` for what performs best
   - `RECENT_ACTIVITY` or `CHRONOLOGICAL` for monitoring current discussions
3. Keep paginating with `--cursor` until you have enough coverage.

### Ad research

1. If you know the message or market but not the advertiser, start with `facebook ads search`.
2. If you know the brand, start with `facebook ads companies search`, then move to `facebook ads companies get`.
3. Use `facebook ads get` on standout ads for creative details or transcripts.
4. Apply filters like country, status, media type, and date range before paginating widely.

## Working notes

- Many Facebook listing commands return pagination data. Reuse `--cursor`, `--page-id`, or `--group-id` exactly as returned.
- `facebook comments` is much faster with `--feedback-id` than with only a post URL.
- `facebook ads search` is best for theme-based discovery. `facebook ads companies get` is best for advertiser-level collection.
- Use `--trim` on ad commands when you want leaner payloads for downstream processing.

## Minimal examples

```bash
scrapesocial facebook profiles get --url https://www.facebook.com/nasa
scrapesocial facebook profiles posts --url https://www.facebook.com/nasa
scrapesocial facebook posts get --url https://www.facebook.com/... --get-comments --get-transcript
scrapesocial facebook groups posts --url https://www.facebook.com/groups/...
scrapesocial facebook ads companies search --query "Nike"
scrapesocial facebook ads companies get --page-id 123456789
scrapesocial facebook ads search --query "running shoes" --country US --status ACTIVE
scrapesocial facebook ads get --id 1234567890 --get-transcript
```
