---
name: scrapesocial-youtube
description: Use when the user wants YouTube research or workflow guidance for lead generation, influencer discovery, brand monitoring, competitor analysis, content analytics, trend research, or audience analysis, including channel inspection, channel video or shorts collection, video detail retrieval, transcript or comment extraction, keyword or hashtag search, trending shorts research, playlist analysis, or community post retrieval.
license: MIT
prerequisites:
  - Scrape Creators API key
metadata:
  author: Skill Atlas
  version: "0.1.2"
  homepage: https://skillatlas.sh/
---

# Scrapesocial YouTube

Use this skill to choose the right `scrapesocial` YouTube command quickly for YouTube research tasks.

## Prerequisites

- A Scrape Creators API key is required for this skill. Get one at [scrapecreators.com](https://scrapecreators.com).

## Start

- Install the CLI once:

```bash
npm install -g scrapesocial@0.1.0
```

- Ensure authentication is available with `SCRAPECREATORS_API_KEY` or `--api-key`.
- Prefer the most specific identifier you already have:
  - channel URL, handle, or channel ID for channel-level work
  - video or short URL for item-level work
  - playlist ID for playlist lookups
- Reuse `continuationToken` from previous responses when you need more results.
- Use `--include-extras` on list and search commands only when you need lightweight engagement context without making a separate detail request.

## Goal-led workflows

| Goal                 | When to use this skill                                                                                              | How to start                                                                                                                                                                              |
| -------------------- | ------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Lead generation      | Use it to discover and qualify creators, channels, or brands tied to a topic.                                       | Start with `youtube search` or `youtube search hashtag`, then qualify channels with `youtube channels get` and `youtube channels videos`.                                                 |
| Influencer discovery | Use it when the user wants creators discovered through search results, shorts, or channel patterns.                 | Start with `youtube search`, `youtube search hashtag`, or `youtube shorts trending`, then validate with `youtube channels get`, `youtube channels videos`, and `youtube channels shorts`. |
| Brand monitoring     | Use it to monitor a known channel's uploads, shorts, and community activity.                                        | Start with `youtube channels get`, then collect `youtube channels videos` or `youtube channels shorts`, and use `youtube community posts get` for known posts.                            |
| Competitor analysis  | Use it to compare channel strategy, long-form versus shorts mix, and standout performers.                           | Start with `youtube channels get` for each channel, then compare `youtube channels videos --sort popular` and `youtube channels shorts --sort popular`.                                   |
| Content analytics    | Use it to explain why specific videos or shorts matter, using item detail, comments, and transcripts.               | Start with `youtube channels videos`, `youtube channels shorts`, or `youtube search`, then drill into winners with `youtube videos get`, `youtube comments`, and `youtube transcript`.    |
| Trend research       | Use it when the user wants topic discovery, hashtag discovery, or a fast view of what is winning in Shorts.         | Start with `youtube search`, `youtube search hashtag`, or `youtube shorts trending`.                                                                                                      |
| Audience analysis    | Use it for qualitative audience response from comment sections. It does not provide channel demographic breakdowns. | Start with `youtube comments` on representative videos, then use `youtube transcript` to compare message and reaction.                                                                    |

## Command Selection

### `youtube channels get`

Use to resolve and inspect a single channel.

Choose this when you need:

- channel metadata before deeper collection
- to normalize a channel URL, handle, or channel ID
- a reliable starting point for creator research

### `youtube channels videos`

Use to list a creator's regular uploads.

Choose this when you need:

- latest uploads from a channel
- a popularity-sorted sample of a creator's long-form content
- a content audit before drilling into individual videos

### `youtube channels shorts`

Use to list a creator's shorts feed separately from regular uploads.

Choose this when you need:

- short-form output from a channel
- a quick scan of what is working in a creator's shorts strategy

### `youtube videos get`

Use to fetch the structured details for one video or short.

Choose this when you need:

- full metadata for a specific item
- to enrich a result found through channel listings or search
- to inspect one standout video in depth

### `youtube transcript`

Use to pull the spoken transcript from a video or short.

Choose this when you need:

- summarization or topic extraction
- quotes, talking points, or script analysis
- downstream NLP work on the spoken content

Specify `--language` only when you need a specific language. If that language is unavailable, the transcript may be `null`.

### `youtube search`

Use to search YouTube by keyword.

Choose this when you need:

- videos about a topic rather than from one creator
- recent coverage with `--upload-date`
- popularity or relevance ranking with `--sort-by`
- shorts-only discovery with `--filter shorts`

Do not combine `--filter shorts` with `--upload-date` or `--sort-by`; the catalog notes that the filter is effectively query-only.

### `youtube search hashtag`

Use to explore content grouped around a hashtag.

Choose this when you need:

- hashtag-led discovery
- to compare all posts versus shorts-only hashtag activity

### `youtube comments`

Use to inspect audience response on a specific video.

Choose this when you need:

- top comments for sentiment and objections
- newest comments for recent audience reaction
- qualitative feedback after identifying a relevant video

### `youtube shorts trending`

Use to get a fast view of what is trending in Shorts without starting from a creator or search term.

Choose this when you need:

- trend scouting
- inspiration for short-form research
- a benchmark set for current shorts performance

### `youtube playlists get`

Use to inspect a specific playlist by playlist ID.

Choose this when you need:

- the contents or structure of a playlist
- to analyze how a creator packages related videos

### `youtube community posts get`

Use to fetch one specific community post by URL.

Choose this when you need:

- the contents of a known post
- creator communication outside of video uploads

## Common Workflows

### Creator Research

1. Run `youtube channels get` to confirm the channel.
2. Run `youtube channels videos` or `youtube channels shorts` to map the content.
3. Run `youtube videos get` on standout items.
4. Add `youtube transcript` or `youtube comments` when you need deeper analysis.

### Topic Research

1. Run `youtube search` or `youtube search hashtag`.
2. Shortlist promising results.
3. Run `youtube videos get` on the shortlisted videos.
4. Add `youtube transcript` or `youtube comments` for analysis.

### Competitive Scan

1. Run `youtube channels get` for each creator.
2. Run `youtube channels videos --sort popular` and optionally `youtube channels shorts --sort popular`.
3. Pull details for the strongest performers with `youtube videos get`.

## Starter Examples

```bash
scrapesocial youtube channels videos --handle MrBeast
scrapesocial youtube transcript --url "https://www.youtube.com/watch?v=VIDEO_ID"
scrapesocial youtube search --query "shopify seo" --upload-date this_month
scrapesocial youtube comments --url "https://www.youtube.com/watch?v=VIDEO_ID" --order top
```

## Notes

- Use channel-level commands to discover items, then switch to item-level commands for detail.
- Use `continuationToken` to paginate instead of inventing your own paging scheme.
- Use `youtube videos get` for full item detail; `--include-extras` on list or search calls is a lighter, slower middle ground.
- Run `scrapesocial --help-full` if you need exact flags or global CLI options.
