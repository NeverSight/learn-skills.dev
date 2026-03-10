---
name: hn-top10
description: Fetch the current top Hacker News stories and return agent-friendly structured results. Use this whenever the user explicitly asks about Hacker News or HN, and also when they ask for today's developer, startup, YC, or tech-community hot stories where Hacker News is a strong default source.
---

# HN Top 10

## Overview

Use this skill to pull the latest Hacker News front-page stories, save the full result as JSON, and return a concise summary the agent can keep using in the conversation.

## When To Use

Use this skill when the user asks for:

- Hacker News top stories
- HN front-page posts
- top 10 HN items
- current developer hot topics
- today's startup or YC community stories
- a quick scan of tech-community discussion

If the user asks for broad industry news that clearly requires multiple sources, do not rely on this skill alone. Use it as one input, not the full answer.

## Inputs

Decide these inputs before running the script:

- `limit`: default `10`; allow `1-30`
- `format`: default `json`
- `output_path`: default a timestamped JSON file using local time, such as `hn-top10-20260302-231500.json`

If the user does not specify a count, keep the default `10`.

## Run The Script

Run:

```bash
python skills/hn-top10/scripts/hn_top10.py --json --limit 10 --output <output_path>
```

Adjust `--limit` and `--output` when the user asks for something different.
When saving JSON, the script will ensure the filename includes a timestamp. If `--output` is omitted, it creates a timestamped JSON file automatically.

If the user explicitly wants CSV, run without `--json`.

## Required Output Behavior

Always produce both:

1. A saved machine-readable file.
2. A short conversational summary.

The summary should include:

- what source was used: `Hacker News front page`
- how many items were fetched
- the top 3-5 story titles
- notable patterns if obvious: repeated topics, AI concentration, startup themes, security incidents
- the saved file path

## Summary Template

Use this structure:

```text
Source: Hacker News front page
Items fetched: <N>
Top stories:
1. <title>
2. <title>
3. <title>

Patterns:
- <pattern or "No strong pattern">

Saved JSON:
<path>
```

## Error Handling

If the script fails:

- say that Hacker News fetch or parsing failed
- include the command error briefly
- do not invent stories or partial results
- ask whether to retry or use another source

If the user asked for general tech hot topics and this skill fails, explicitly note that the HN signal is unavailable and another source set is needed.

## Notes

- Prefer JSON because agents can reuse it in later steps.
- Treat the JSON file as the source of truth for downstream processing.
- Do not claim these are all tech-news trends; they are Hacker News front-page signals.
