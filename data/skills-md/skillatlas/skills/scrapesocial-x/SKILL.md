---
name: scrapesocial-x
description: Use when the user wants X (Twitter) research or workflow guidance for lead generation, influencer discovery, brand monitoring, competitor analysis, content analytics, trend research, or audience analysis on known handles, posts, or communities, including profile inspection, recent post collection, post detail retrieval, transcript extraction, and community monitoring.
license: MIT
prerequisites:
  - Scrape Creators API key
metadata:
  author: Skill Atlas
  version: "0.1.2"
  homepage: https://skillatlas.sh/
---

# Scrapesocial X

Use this skill for read-only X research on known handles, posts, and communities. Prefer it when the user already knows the account, post, or community they want to inspect. Do not use it for posting, liking, following, DMs, account management, or cold discovery workflows that need search or follower graphs.

## Prerequisites

- A Scrape Creators API key is required for this skill. Get one at [scrapecreators.com](https://scrapecreators.com).

## Quick start

- Install the CLI once:

```bash
npm install -g scrapesocial@0.1.0
```

- Make sure auth is set up with `SCRAPECREATORS_API_KEY` or `--api-key`.
- Prefer `--format json` for one-off calls and `--format jsonl` when piping collections.
- Use `--trim` on post endpoints when you want a smaller payload.
- This skill works best when the user already has a handle, post URL, or community URL.
- If you need exact flags for a command, run `scrapesocial <command> --help`.

## Goal-led workflows

| Goal                 | When to use this skill                                                                                                                                      | How to start                                                                                                          |
| -------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------- |
| Lead generation      | Use it to qualify known handles or communities, not to build cold lead lists from scratch.                                                                  | Start with `x profiles get`, then inspect recent output with `x posts` or community context with `x communities get`. |
| Influencer discovery | Use it to vet handles discovered elsewhere or to see who is active inside a known community.                                                                | Start with `x profiles get`, `x posts`, and `x communities posts`.                                                    |
| Brand monitoring     | Use it to monitor what a known handle or community is publishing.                                                                                           | Start with `x posts` for the handle and `x communities posts` for community-level activity.                           |
| Competitor analysis  | Use it to compare how known accounts talk, what they post, and which flagship posts matter.                                                                 | Start with `x profiles get` for each account, then compare `x posts` and `x posts get` on representative posts.       |
| Content analytics    | Use it to inspect post-level messaging, media context, and spoken text in videos.                                                                           | Start with `x posts`, then drill into standout posts with `x posts get` or `x transcript`.                            |
| Trend research       | Use it only for trends inside known accounts or communities. Pair it with another skill for broad search.                                                   | Start with `x communities posts` or a shortlist of known handles and compare recent output.                           |
| Audience analysis    | Use it only for lightweight, qualitative signals from what the account or community is posting. It does not expose follower or reply analytics in this CLI. | Start with `x posts get` or `x communities posts`, then summarize repeated language and themes.                       |

## Pick the right command

### `x profiles get`

Use to resolve and inspect a known handle.

Choose this when you need:

- account metadata before deeper inspection
- a quick brand or creator snapshot
- a canonical starting point for a known handle

### `x posts`

Use to list recent posts from a known handle.

Choose this when you need:

- a recent output sample for content or competitor analysis
- a lightweight monitoring view on a known account
- post candidates for deeper inspection

### `x posts get`

Use to inspect one specific post by URL.

Choose this when you need:

- detail on one standout or campaign post
- a closer read on media, metadata, or structure
- a post-level artifact for analysis or reporting

### `x transcript`

Use to extract spoken content from a post with video.

Choose this when you need:

- spoken hooks, quotes, or talking points
- message analysis on video posts
- transcript text for downstream NLP work

### `x communities get`

Use to inspect one known X community.

Choose this when you need:

- community metadata and framing
- context before collecting community posts
- a starting point for community-led monitoring

### `x communities posts`

Use to collect posts from a known community.

Choose this when you need:

- discussion samples inside a specific community
- niche monitoring without starting from one handle
- lightweight trend checks in a known community

## Typical workflows

### Account audit

1. Resolve the handle with `x profiles get`.
2. Inspect recent output with `x posts`.
3. Open representative posts with `x posts get`.

```bash
scrapesocial x profiles get --handle nasa
scrapesocial x posts --handle nasa --trim
scrapesocial x posts get --url "https://x.com/nasa/status/..." --trim
```

### Tweet investigation

1. Start with `x posts get --url ...`.
2. Add `x transcript --url ...` when the post includes spoken video content.
3. Compare the post with surrounding account output via `x posts --handle ...`.

```bash
scrapesocial x posts get --url "https://x.com/ACCOUNT/status/POST_ID"
scrapesocial x transcript --url "https://x.com/ACCOUNT/status/POST_ID"
```

### Community monitoring

1. Resolve the community with `x communities get`.
2. Pull recent community posts with `x communities posts`.
3. Follow standout posts back to their authors with `x profiles get` when needed.

```bash
scrapesocial x communities get --url "https://x.com/i/communities/COMMUNITY_ID"
scrapesocial x communities posts --url "https://x.com/i/communities/COMMUNITY_ID"
```

## Operating guidance

- Prefer handle-based or URL-based lookups because this CLI surface is oriented around known entities.
- Use `x posts` to build a sample first, then `x posts get` or `x transcript` for depth.
- Use `x communities posts` when the user cares about a niche conversation space more than one account.
- Stay realistic about scope: this skill is best for enrichment and monitoring, not broad X search or follower-graph analysis.
