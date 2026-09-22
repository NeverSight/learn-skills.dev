---
name: landing-page-editor
description: Use when editing, updating, or iterating on a workspace's landing page HTML (the magazine-style /w/:slug page). Supports incremental edits — fetch the current HTML, make targeted changes, then write it back. NOT for initial generation — that comes from the `brief` field which runs the server-side LANDING_PAGE_PROMPT against Gemini.
allowed-tools: Bash(astria:*), Read, Write, Edit
---

# Workspace Landing Page Editor

The workspace landing page (rendered at `/w/:slug`) is a single self-contained
HTML blob stored on `workspace.landing_page_html`. It is generated from scratch
by the server-side `LANDING_PAGE_PROMPT` whenever a `brief` is submitted — that
path overwrites the HTML wholesale.

For ANY change that should not regenerate the whole page (typography tweaks,
layout edits, adding a section, changing copy, swapping an image, fixing a
tagline), edit the HTML directly and write it back. Do NOT send a `brief`
unless the user wants a full regeneration.

All commands use the `astria` CLI (see the `astria-api` skill). Pass
`-w <workspace_id>` to target the workspace.

## Constraints carried over from `LANDING_PAGE_PROMPT`

When editing, preserve these invariants (the live `/w/:slug` page depends on them):

- The output is **inner body HTML** — no `<html>`, `<head>`, `<body>`, or `<!DOCTYPE>` tags
- Styling uses **Tailwind utility classes** (already loaded on the page). Use `<style>` only for hover/animation effects Tailwind can't express
- Pack links are exactly `/p/{slug}`; model/reference links use the `link` field from the tunes JSON verbatim (do NOT re-encode `%5B`/`%5D`)
- Every image / video is wrapped in an `<a>` tag
- Image and video URLs must be ones that already exist — do not invent URLs
- Videos use `<video autoplay muted loop playsinline poster="POSTER_URL"><source src="VIDEO_URL" type="video/mp4"></video>`
- The string `__TUNES_JSON_PAYLOAD__` inside `<script type="application/json" id="tunes-data">…</script>` is a server-side placeholder. The server substitutes it at render time with the live tunes JSON. **Never replace it with literal JSON** — that freezes the cast and newly added tunes won't appear
- Editorial styling: serif headlines, generous whitespace, hairline rules, `object-cover object-[center_top]` on portrait images, `max-h-[70vh]` on hero spreads, `aspect-[4/5]` or `aspect-[3/4]` on portrait containers

## Workflow

### 1. Fetch the current landing page HTML

```bash
astria landing get -w <workspace_id> --html > /tmp/landing_page.html
```

`astria landing get -w <workspace_id>` (without `--html`) returns the full
workspace JSON — `title`, `slug`, `brief`, `url`, `public_at`, `unlisted_at` —
when you need those. Preview the rendered page at `/w/{slug}`.

### 2. Pull workspace data (when an edit needs to reference real packs / prompts / tunes)

```bash
astria packs list -w <workspace_id> --limit 100
astria tunes list -w <workspace_id> --limit 200            # the "cast" rendered on the page
astria prompts list -w <workspace_id> --limit 100 --offset 0   # page with --offset until empty
astria prompts list -w <workspace_id> --pack-id <pack_id>      # cheaper, one section at a time
```

List endpoints paginate via `--limit`/`--offset` (default sort id desc). Loop
with `--offset` until a page comes back empty.

### 3. Make the incremental edit

Edit `/tmp/landing_page.html` locally. Keep changes surgical — the generator
produced thousands of bytes of layout and most of it should stay verbatim.
Re-read the constraints section above before saving.

### 4. Write the page back

```bash
astria landing set -w <workspace_id> --html-file /tmp/landing_page.html
```

Do NOT pass `--brief` here — that discards your edits and regenerates from
scratch via Gemini.

### 5. Verify

Open `/w/{slug}` and visually confirm the change. The `__TUNES_JSON_PAYLOAD__`
placeholder is replaced server-side at render time — if a JSON-shaped string
still shows on the rendered page, the placeholder was accidentally deleted or
renamed.

## Regenerating from scratch

Only when the user explicitly asks for a full redesign — submit a `brief` and
the server runs `LANDING_PAGE_PROMPT` against Gemini, overwriting the HTML:

```bash
astria landing set -w <workspace_id> \
  --brief "Editorial fashion lookbook, AW26, dark moody palette, emphasize the womenswear packs"
```
