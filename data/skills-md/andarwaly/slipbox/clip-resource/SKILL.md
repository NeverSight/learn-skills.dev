---
name: clip-resource
description: Fetch one or more URLs and write each as a frozen Resource, matching Obsidian Web Clipper's output shape. For users without a clipper tool. Fetchable content only; paywalled or login-gated pages are not handled by this skill.
disable-model-invocation: true
license: MIT
metadata:
  version: "1.8.0"
---

# Clip Resource

Bold terms in this file are defined in `GLOSSARY.md`.

For the case where the user has no Web Clipper, no Readwise, nothing installed: this skill fetches a URL and publishes a Resource file that looks like Web Clipper's own output. Each URL runs as independent recoverable Resource work under `/using-slipbox`; extraction and the template-resolved draft are checkpointed before the frozen target is published. It never touches `.slipbox/candidates/` or takes part in the candidate pipeline; it reads template paths via `.slipbox/bin/slipbox config get templates.<type>_path`, filename/frontmatter conventions from the configured template and established vault rules, and transcript languages via `.slipbox/bin/slipbox config get transcript_languages`, not pipeline bookkeeping. `make-literature-note` (and other note-writing skills) read the Resource file later; this skill's job ends once it's published.

## Prerequisite

- MUST: `.slipbox/AGENTS.md` exists — confirms `setup-slipbox` ran to completion.
- MUST: All dependencies (Defuddle, Firecrawl, `youtube-transcript-api`, TinyFish) are available — check at step-entry, not here.
- NEVER: proceed without either. Stop and tell the user to run `setup-slipbox` first.
- NEVER: improvise a naming/folder convention in place of running `setup-slipbox`.
- NEVER: install a missing dependency yourself — that's `setup-slipbox`'s job. Point the user there instead.

## Workflow

### 01 - Take the URL(s)

Ask for one or more URLs: articles, news stories, social/forum threads, or video links, any mix. There is no paste-the-text fallback. If the user hands you raw text instead of a link, tell them this skill only takes URLs and ask for one.

Every URL below reaches a shell command (`defuddle parse`, `firecrawl scrape`), so check each one before it gets there: it must parse as an `http`/`https` URL, and it must contain no shell metacharacters — quotes, backticks, `$`, `;`, `|`, `&`, `<`, `>`, newlines. Reject anything else and say why instead of sanitizing it into something runnable; a URL that needs escaping to be safe isn't the URL the user meant. Pass the checked URL as a single quoted argument, never interpolated into a longer shell string.

For more than one URL, spawn one subagent per URL. Each subagent runs the full fetch/extract/transform/publish pipeline (Detect the content type through Write) independently, in parallel, for its own URL only. If no subagent capability exists in this harness, process each URL sequentially instead. Either way, one URL's failure never blocks or corrupts another's — each has its own work directory, checkpoints, target, commit boundary, and outcome row.

### 02 - Detect the content type

Determine which of the four content types applies, in this priority order:

1. **User-stated type**: if the user says "clip this article" or "clip this video," take it as a starting hypothesis, not a final answer.
2. **URL pattern**: domain and path shape. See `references/url-patterns.md` for patterns organized by content type.
3. **schema.org**: `NewsArticle`, `Article`, `DiscussionForumPosting`, `VideoObject`, etc., read off the fetched page.
4. **Conflict check**: compare the user-stated type (if any) against what the URL pattern and schema.org indicate. A real conflict (user says "article," URL is a Reddit thread) gets flagged to the user before anything is written. Never silently override in either direction.
5. **Ask fallback**: if signals disagree with each other or nothing resolves confidently, ask the user which type it is rather than guessing.

The four content types: **Article**, **News**, **Social/Forum thread**, **Video**.

### 03 - Fetch and extract

Note what you actually got back: full content, a truncated snippet, or nothing. Extraction splits by content type. Use the reference file matching the type detected in Detect the content type.

| Content type | Reference | Method |
|---|---|---|
| **Article**, **News** | `references/extract-article-news.md` | A two-rung Ladder (see `GLOSSARY.md`): Defuddle first, Firecrawl fallback for blocked fetches |
| **Social/Forum thread** | `references/extract-social.md` | TinyFish or Firecrawl fetch, then the Ladder (see `GLOSSARY.md`) for facts: schema.org JSON-LD, then `<meta>` tags, then LLM-read fallback |
| **Video** | `references/extract-video.md` | `youtube-transcript-api` Python library |

Read the reference file for your type; it covers the full extraction logic, tooling, error taxonomy, and fallback paths specific to that content type.

### 04 - Transform

`clip-resource` has no opinion on what any template's body should contain. Every template is 100% user-authored via `setup-slipbox`, and there is no shipped/default treatment implied by content type. This skill resolves bare variables verbatim and executes quoted instructions exactly as written (see `references/variable-glossary.md`), for every content type equally. A template author may write bare `{{content}}` for Article, a quoted cleanup instruction for News, `{{root_post}}` plus `{{continuation}}` for Social, bare `{{transcript}}` for Video, entity sections (People/Tools/Resources/Definition) or none at all — this skill fills in whatever the actual template asks for, without assuming a "typical" shape per type.

Read the template first — its location comes from the `templates.<type>_path` scoped read described above — then resolve its variables and filters against the reference files. Mechanical fields, not content-shape opinions, still apply regardless of template: `type` in frontmatter holds the content type directly (see `GLOSSARY.md` for the Resource type-field rule). `author` resolves per type's own definition (byline for Article/News, display name falling back to handle for Social, channel name for Video) — see `references/variable-glossary.md`. `published` resolves via Defuddle's output for Article/News, or the Ladder in Fetch and extract for Social, same as any other bare fact for that type.

`clip-resource` fills in only what the template's own variables and filters ask for — see `references/variable-glossary.md` and `references/filter-glossary.md`. The active Video path is YouTube-specific; a Video template may therefore use `{{video_id}}` to construct YouTube's deterministic thumbnail URL. No corresponding generic cover variable exists for Article, News, or Social, so do not invent or guess one. Nothing beyond that: no line naming an idea worth pursuing, no conclusion about what the content means. Reading the material and forming an opinion on it is `make-literature-note`'s surface pass (per its own SKILL.md), run later and separately. A Resource file that already contains a take would skip that analytical step instead of feeding it.

### 05 - Write

Read the destination with `.slipbox/bin/slipbox config get paths.resources` and decode
its JSON string value. Join that vault-relative folder with the resolved Resource
filename, preserving configured casing and nested directories. Pass this exact path
as the work target and artifact mutation path `/using-slipbox`; report the same saved
path after publication. The CLI accepts the complete vault-relative path and validates
it; the caller resolves the configured folder. A missing, empty, or invalid setting
blocks publication and requires configuration repair; preserve any extraction/draft
already obtained. Do not substitute a default folder or append a content-type folder.
On resume, compare the stored target with this configured destination; if they differ,
report the mismatch and resolve it with the user before publication.

Classify whether the resolved template used bare variables or a quoted instruction (see `references/variable-glossary.md`); this controls whether the staged draft needs the Resource-mode `/write-checks` gate below.

Start or resume work for this Resource with kind `resource`, activity `clip`, and the
source URL `/using-slipbox`; the target is create-only and frozen. Record the detected
type, extraction method, metadata, status, and any failure details in the work state. Do
not create a permanent extraction cache.

Checkpoint work with `manifest.json` plus `extraction.json` after fetch/extraction, including
the source URL and the extracted payload or a structured failure. Resolve the template into
`draft.md` and checkpoint work `/using-slipbox` before publication. A bare-variable draft
is still transactional; never write the final Resource directly from the fetched response.

If a quoted instruction (see `references/variable-glossary.md`) was resolved for this clip, run `/write-checks` with `artifact-kind: resource` on the synthesized draft before publication. Resource mode runs Style and Humanize only and returns the pass/revise signal — it does not resolve fields, place zones, or invoke `note validate`. If this clip used only bare variables, skip the checks — nothing was synthesized to check.

Publish an artifact `/using-slipbox` from the staged `draft.md`, with the target's expected
starting fingerprint and create-only semantics. A target collision — including a pre-existing
file or a target changed during work — fails without replacement. On successful publication,
treat the Resource as frozen: this skill does not reopen it to edit, append, or correct it.
If the fetch or transform needs a fix, resume or discard the preserved work and start a fresh
clip; never patch the frozen target.

If fetch or transform fails, persist the failed extraction and draft state in the Resource work directory and report the failure; do not publish a partial Resource. Work may be resumed or explicitly discarded later. A failed URL never aborts another URL's work.

### 06 - Report the outcome

For a single URL, two valid endings, both explicit:

- **Success**: the Resource file exists at its path, shaped per Transform, with the correct `type` in frontmatter.

  ```
  Clip Saved

  **Type:** article
  **URL:** https://example.com/some-post
  **Saved to:** <resolved Resource path>
  ```

- **Fetch failure**: the fetch returned an error, or returned content but it's a paywall teaser, a login wall, a blocked/rate-limited transcript request, or otherwise not the real article/thread/video. Do not write a partial Resource file, and do not attempt to work around the paywall, login gate, or block. A clear failure report is a complete, correct run of this skill; a half-written Resource file is not.

  ```
  Clip Failed

  **URL:** https://example.com/some-post
  **Type:** article (detected)
  **Reason:** Defuddle and Firecrawl fallback both failed — page returned a login wall.
  ```

For multiple URLs, one batch table covering every URL together, successes and failures alike, matching `find-connections`' batch-present convention:

```
Clip Results — 3 URLs

| URL | Type | Result |
|---|---|---|
| example.com/a | article | Saved to `<resolved Resource path for a>` |
| example.com/b | video | Failed — transcript disabled |
| example.com/c | social | Saved to `<resolved Resource path for c>` |
```

No closing prompt or question after either shape. State the outcome and end.

## Variable syntax (summary)

Templates (paths resolved via `.slipbox/bin/slipbox config get templates.<type>_path`, per the scoped read above) use two variable forms, matching Obsidian Web Clipper's own convention. No new syntax invented. Full detail in `references/variable-glossary.md` (bare variables, quoted instructions, and filters); see `references/filter-glossary.md` for the filter vocabulary (`|wikilink`, `|date:"..."`, etc.).

## References

| File | Purpose | Triggering condition |
|---|---|---|
| `references/extract-article-news.md` | Extraction ladder, fallback paths for Article and News types | Content type is Article or News |
| `references/extract-social.md` | Extraction method for social/forum threads (schema.org, meta tags, LLM fallback) | Content type is Social/Forum thread |
| `references/extract-video.md` | Transcript extraction for video | Content type is Video |
| `references/filter-glossary.md` | Filter vocabulary and application rules | Template uses any filter (`\|wikilink`, `\|date`, etc.) |
| `references/url-patterns.md` | Domain and path patterns for content-type detection | Detecting content type from URL shape |
| `references/variable-glossary.md` | Variable definitions, bare vs. quoted forms, and when to use each | Resolving any template variable |
