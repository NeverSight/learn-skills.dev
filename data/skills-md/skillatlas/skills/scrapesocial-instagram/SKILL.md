---
name: scrapesocial-instagram
description: Use when the user wants Instagram research or workflow guidance for lead generation, influencer discovery, brand monitoring, competitor analysis, content analytics, trend research, or audience analysis, including profile analysis, feed collection, post or reel inspection, transcript extraction, comment analysis, reel discovery, highlight retrieval, or embed generation.
license: MIT
prerequisites:
  - Scrape Creators API key
metadata:
  author: Skill Atlas
  version: "0.1.2"
  homepage: https://skillatlas.sh/
---

# Scrapesocial Instagram

Use this skill for read-only Instagram research and retrieval. Keep it at the job-to-command level: choose the right entry point quickly, prefer lighter responses first, and reuse IDs or cursors returned by earlier commands.

## Prerequisites

- A Scrape Creators API key is required for this skill. Get one at [scrapecreators.com](https://scrapecreators.com).

## Quick Setup

Install the CLI once:

```bash
npm install -g scrapesocial
```

Authenticate with `SCRAPECREATORS_API_KEY`, then run commands with `scrapesocial`:

```bash
SCRAPECREATORS_API_KEY=... scrapesocial instagram ...
```

Useful global flags:

- `--trim` for smaller responses when supported.
- `--format jsonl` when streaming lists into downstream tools.
- `--credit-limit <n>` when you want the CLI to hide or block expensive requests.

## Quick Start

- If the task is about an account as a whole, start with `instagram profiles get`.
- If the task is about a creator's regular feed, use `instagram posts`.
- If the task is about one specific post or reel, use `instagram posts get`.
- If the task is about spoken content in a reel or video post, use `instagram transcript`.
- If the task is about finding relevant reels by topic, use `instagram reels search`.
- If the task is about audience response on one post, use `instagram comments`.
- If the task is about a creator's reels library, use `instagram reels`.
- If the task is about story highlights, use `instagram highlights`, then `instagram highlights detail`.
- If the task is about embeddable markup for a profile, use `instagram embed`.

## Goal-led workflows

| Goal                 | When to use this skill                                                                                                                          | How to start                                                                                                                                                    |
| -------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Lead generation      | Use it to qualify known creator or brand accounts, or to turn reel discovery into a shortlist. Pair it with another source for contact details. | Start with `instagram reels search`, then switch to `instagram profiles get`, `instagram posts`, or `instagram reels` for qualification.                        |
| Influencer discovery | Use it when the user wants creators discovered or vetted through niche reels, recurring themes, and account quality.                            | Start with `instagram reels search`, then validate shortlisted handles with `instagram profiles get`, `instagram reels`, and `instagram highlights`.            |
| Brand monitoring     | Use it to monitor a known brand or creator account across feed posts, reels, and highlights.                                                    | Start with `instagram profiles get`, then branch into `instagram posts`, `instagram reels`, and `instagram highlights`.                                         |
| Competitor analysis  | Use it to compare how multiple brands or creators package their feeds, reels, highlights, and audience response.                                | Start with `instagram profiles get` for each account, then compare `instagram posts`, `instagram reels`, and `instagram comments` on representative items.      |
| Content analytics    | Use it to explain what makes certain posts or reels work, using item detail, comments, and transcripts.                                         | Start with `instagram posts` or `instagram reels`, then drill into standout items with `instagram posts get`, `instagram comments`, and `instagram transcript`. |
| Trend research       | Use it for reel-led topic scouting and validation of emerging creative patterns.                                                                | Start with `instagram reels search`, then inspect the best examples with `instagram posts get`.                                                                 |
| Audience analysis    | Use it for qualitative audience language, FAQs, and objections. It does not provide demographic audience breakdowns.                            | Start with `instagram comments` on representative posts or reels, then use `instagram profiles get` and `instagram highlights` for context.                     |

Read [references/instagram-command-map.md](references/instagram-command-map.md) when you need the full command-selection table.

## Choose the Starting Input

- Prefer a `--handle` when the user is researching an account and no richer identifier is available yet.
- Prefer a `--url` when the user gives a specific post or reel. This is the cleanest way to inspect one item or fetch its comments or transcript.
- Prefer a `--user-id` only after another command has already returned it. For reels and highlights, this can be faster than resolving by handle again.
- Prefer a returned pagination token over restarting the query. Instagram commands use command-specific cursor fields such as `next_max_id`, `max_id`, or `cursor`.
- Prefer a returned highlight ID when drilling into a specific highlight after listing highlights.

## Working Pattern

1. Start with the highest-level command that matches the job.
2. Use `--trim` on commands that support it when the goal is quick inspection, summarization, or easier downstream processing.
3. Keep IDs and cursors from the response so follow-up commands do not repeat the same discovery step.
4. Rerun without `--trim` only when you need fields that the smaller response may omit.
5. Switch from handle-based to ID-based commands after the first lookup when the command supports it and the workflow will page repeatedly.

## Common Flows

### Audit a creator account

Use `instagram profiles get` to understand the account first, then branch:

- Use `instagram posts` for the feed history.
- Use `instagram reels` for short-form video output.
- Use `instagram highlights` for archived stories.
- Use `instagram embed` if the output needs embeddable markup rather than analysis.

### Analyze one post or reel

Use `instagram posts get` when the user has a single Instagram URL and wants metadata or content details. Branch again only if needed:

- Use `instagram comments` to inspect audience reaction.
- Use `instagram transcript` to extract spoken dialogue from video content.

### Research a topic on Instagram Reels

Use `instagram reels search` for topical discovery, trend scouting, or seed collection. Once a specific reel is interesting, move to `instagram posts get` or `instagram comments` with the reel URL.

## Command Notes

- `instagram profiles basic` is a niche follow-up command when you already have a user ID and only need the lighter basic-profile view.
- `instagram highlights detail` is not a discovery command. Use it only after `instagram highlights` returns the highlight ID you want.
- `instagram comments`, `instagram posts`, and `instagram reels` are pagination-friendly. Keep the returned cursor values for iterative collection.
- `instagram transcript` is only useful for media that actually contains speech.
- This CLI is for retrieval and analysis, not posting, messaging, liking, or other write actions on Instagram.

## Reference

Read [references/instagram-command-map.md](references/instagram-command-map.md) for a command-by-command matrix with typical inputs, outcomes, and follow-up moves.
