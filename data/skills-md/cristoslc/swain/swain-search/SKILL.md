---
name: swain-search
description: "Evidence pool collection and normalization for swain-design artifacts. Collects sources from the web, local files, and media (video/audio), normalizes them to markdown, and caches them in reusable evidence pools. Use when researching a topic for a spike, ADR, vision, or any artifact that needs structured evidence. Also use to refresh stale pools or extend existing ones with new sources. Triggers on: 'research X', 'gather evidence for', 'build an evidence pool', 'search for sources about', 'refresh the evidence pool', 'what do we know about X', or when swain-design needs research inputs for a spike or ADR."
user-invocable: true
license: MIT
allowed-tools: Bash, Read, Write, Edit, Glob, Grep, Skill, WebSearch, WebFetch
metadata:
  short-description: Evidence pool collection and normalization
  version: 1.0.0
  author: cristos
  source: swain
---

# swain-search

Collect, normalize, and cache source materials into reusable evidence pools that swain-design artifacts can reference.

## Mode detection

| Signal | Mode |
|--------|------|
| No pool exists for the topic, or user says "research X" / "gather evidence" | **Create** — new pool |
| Pool exists and user provides new sources or says "add to" / "extend" | **Extend** — add sources to existing pool |
| Pool exists and user says "refresh" or sources are past TTL | **Refresh** — re-fetch stale sources |
| User asks "what pools do we have" or "find evidence about X" | **Discover** — search existing pools by tag |

## Create mode

Build a new evidence pool from scratch.

### Step 1 — Gather inputs

Ask the user (or infer from context) for:

1. **Pool ID** — a slug for the topic (e.g., `websocket-vs-sse`). Suggest one if the context is clear.
2. **Tags** — keywords for discovery (e.g., `real-time`, `websocket`, `sse`)
3. **Sources** — any combination of:
   - Web search queries ("search for WebSocket vs SSE comparisons")
   - URLs (web pages, forum threads, docs)
   - Video/audio URLs
   - Local file paths
4. **Freshness TTL overrides** — optional, defaults are fine for most pools

If invoked from swain-design (e.g., spike entering Active), the artifact context provides the topic, tags, and sometimes initial sources.

### Step 2 — Collect and normalize

For each source, use the appropriate capability. Read `references/normalization-formats.md` for the exact markdown structure per source type.

**Web search queries:**
1. Use a web search capability to find relevant results
2. Select the top 3-5 most relevant results
3. For each: fetch the page, normalize to markdown per the web page format
4. If no web search capability is available, tell the user and skip

**Web page URLs:**
1. Fetch the page using a browser or page-fetching capability
2. Strip boilerplate (nav, ads, sidebars, cookie banners)
3. Normalize to markdown per the web page format
4. If fetch fails, record the URL in manifest with a `failed: true` flag and move on

**Video/audio URLs:**
1. Use a media transcription capability to get the transcript
2. Normalize to markdown per the media format (timestamps, speaker labels, key points)
3. If no transcription capability is available, tell the user and skip — or accept a pre-made transcript

**Local files:**
1. Use a document conversion capability (PDF, DOCX, etc.) or read directly if already markdown
2. Normalize per the document format
3. For markdown files: add frontmatter only, preserve content

**Forum threads / discussions:**
1. Fetch and normalize per the forum format (chronological, author-attributed)
2. Flatten nested threads to chronological order with reply-to context

Each normalized source file goes to `sources/NNN-<slug>.md` with sequential numbering.

### Step 3 — Generate manifest

Create `manifest.yaml` following the schema in `references/manifest-schema.md`. Include:
- Pool metadata (id, created date, tags)
- Default freshness TTL per source type
- One entry per source with provenance (URL/path, fetch date, content hash, type)

Compute content hashes as SHA-256 of the normalized markdown content:

```bash
shasum -a 256 sources/001-example.md | cut -d' ' -f1
```

### Step 4 — Generate synthesis

Create `synthesis.md` — a structured distillation of key findings across all sources.

Structure the synthesis by **theme**, not by source. Group related findings together, cite sources by ID, and surface:
- **Key findings** — what the sources collectively say about the topic
- **Points of agreement** — where sources converge
- **Points of disagreement** — where sources conflict or present alternatives
- **Gaps** — what the sources don't cover that might matter

Keep it concise. The synthesis is a starting point, not a comprehensive report — the user or artifact author will refine it.

### Step 5 — Report

Tell the user what was created:

> **Evidence pool `<pool-id>` created** with N sources.
>
> - `docs/evidence-pools/<pool-id>/manifest.yaml` — provenance and metadata
> - `docs/evidence-pools/<pool-id>/sources/` — N normalized source files
> - `docs/evidence-pools/<pool-id>/synthesis.md` — thematic distillation
>
> Reference from artifacts with: `evidence-pool: <pool-id>@<commit-hash>`

## Extend mode

Add new sources to an existing pool.

1. Read the existing `manifest.yaml`
2. Collect and normalize new sources (same as Create step 2)
3. Number new sources sequentially after the highest existing ID
4. Append new entries to `manifest.yaml`
5. Update `refreshed` date
6. Regenerate `synthesis.md` incorporating all sources (old + new)
7. Report what was added

## Refresh mode

Re-fetch stale sources and update changed content.

1. Read `manifest.yaml`
2. For each source, check if `fetched` date + `freshness-ttl` has elapsed
3. For stale sources:
   - Re-fetch the raw content
   - Re-normalize to markdown
   - Compute new content hash
   - If hash changed: replace the source file, update manifest entry
   - If hash unchanged: update only `fetched` date
4. Update `refreshed` date in manifest
5. If any content changed, regenerate `synthesis.md`
6. Report: "Refreshed N sources. M had changed content, K were unchanged."

For sources with `freshness-ttl: never`, skip them during refresh.

## Discover mode

Help the user find existing pools relevant to their topic.

1. Scan `docs/evidence-pools/*/manifest.yaml` for all pools
2. Match against the user's query by:
   - **Tag match** — pool tags contain query keywords
   - **Title match** — pool ID slug contains query keywords
3. For each match, show: pool ID, tags, source count, last refreshed date, referenced-by list
4. If no matches, suggest creating a new pool

## Graceful degradation

The skill references capabilities generically. When a capability isn't available:

| Capability | Fallback |
|-----------|----------|
| Web search | Skip search-based sources. Tell user: "No web search capability available — provide URLs directly or add a search MCP." |
| Browser / page fetcher | Try basic URL fetch. If that fails: "Can't fetch this URL — paste the content or provide a local file." |
| Media transcription | "No transcription capability available — provide a pre-made transcript file, or add a media conversion tool." |
| Document conversion | "Can't convert this file type — provide a markdown version, or add a document conversion tool." |

Never fail the entire run because one capability is missing. Collect what you can, skip what you can't, and report clearly.

## Capability detection

Before collecting sources, check what's available. Look for tools matching these patterns — the exact tool names vary by installation:

- **Web search**: tools with "search" in the name (e.g., `brave_web_search`, `bing-search-to-markdown`)
- **Page fetching**: tools with "fetch", "webpage", "browser" in the name (e.g., `fetch_content`, `webpage-to-markdown`, `browser_navigate`)
- **Media transcription**: tools with "audio", "video", "youtube" in the name (e.g., `audio-to-markdown`, `youtube-to-markdown`)
- **Document conversion**: tools with "pdf", "docx", "pptx", "xlsx" in the name (e.g., `pdf-to-markdown`, `docx-to-markdown`)

Report available capabilities at the start of collection so the user knows what will and won't work.

## Linking from artifacts

Artifacts reference evidence pools in frontmatter:

```yaml
evidence-pool: websocket-vs-sse@abc1234
```

The format is `<pool-id>@<commit-hash>`. The commit hash pins the pool to a specific version — pools evolve over time as sources are added or refreshed, and the hash ensures reproducibility.

When creating or extending a pool, remind the user to commit and then update the referencing artifact's frontmatter with the new commit hash.
