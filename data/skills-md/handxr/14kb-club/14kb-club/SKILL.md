---
name: 14kb-club
description: Analyze web projects for the 14KB Club — audit that the critical rendering path (HTML + CSS + JS + fonts) fits within 14KB gzipped for instant first paint via TCP slow start. Hybrid mode detects anti-patterns in source code and measures real gzipped sizes from build output. Works with any framework (Next.js, Vite, Astro, Nuxt, Angular, SvelteKit, Remix, Gatsby, CRA, plain HTML, PHP). Use when reviewing web performance, auditing page weight, optimizing first paint, checking critical path size, or when a user asks to make their site faster, lighter, or check if it fits in 14KB. Triggers on web projects with HTML/CSS/JS files.
---

# 14KB Club

Audit web projects against the 14KB TCP slow start budget. Conservative approach: report and suggest, never auto-apply.

## Workflow

1. Identify target directory or file
2. Run the auditor script:
   ```bash
   python3 <skill-path>/scripts/14kb_club.py <file_or_dir> --json
   ```
3. Parse JSON output
4. Present budget bar (if build detected) + issues grouped by severity
5. Propose fixes starting with errors, then warnings
6. Wait for user approval before applying changes
7. Re-run after fixes to verify improvement

## Running the Auditor

```bash
# Single file
python3 <skill-path>/scripts/14kb_club.py index.html

# Entire project (auto-detects framework + build folder)
python3 <skill-path>/scripts/14kb_club.py src/

# Scan build output for real gzipped sizes
python3 <skill-path>/scripts/14kb_club.py dist/

# Custom budget (default: 14KB)
python3 <skill-path>/scripts/14kb_club.py . --budget 10

# Force a specific build directory
python3 <skill-path>/scripts/14kb_club.py . --build-dir .next/

# Include low-severity hints
python3 <skill-path>/scripts/14kb_club.py . --strict

# Machine-readable JSON
python3 <skill-path>/scripts/14kb_club.py . --json
```

## What It Detects

### CSS Critical Path (severity: error)
- External CSS in `<head>` without `media` attribute — render-blocking
- No inline `<style>` for critical CSS — all CSS is external
- `@import` chains in CSS files — sequential blocking requests
- CSS files > 14KB gzipped

### JS Blocking (severity: error)
- `<script src>` without `defer`/`async` in `<head>` — blocks parsing
- Known third-party blocking scripts (GA, GTM, Facebook, Intercom, etc.)
- Legacy DOM write methods — blocks parsing
- JS files > 14KB gzipped

### Fonts (severity: warning)
- `@font-face` without `font-display: swap` — invisible text (FOIT)
- Font files not preloaded — late discovery
- Google Fonts loading 4+ weights — each adds 20-50KB
- More than 2 font families

### HTML Bloat (severity: warning)
- Inline SVGs > 2KB
- data: URIs > 1KB
- HTML > 14KB uncompressed
- Excess meta/preload tags (10+)
- Inline style blocks > 5KB

## Build Mode

When a build folder is detected (or specified with `--build-dir`), the script measures real gzipped sizes and renders a budget bar:

```
Budget: [===========>   ] 11.2 / 14.0 KB gzipped (80%)

  HTML:   3.2 KB  [====      ] 23%
  CSS:    4.1 KB  [=====     ] 29%
  JS:     3.9 KB  [=====     ] 28%
  Fonts:  0.0 KB  [          ]  0%

Status: PASS — 2.8KB under budget
```

Auto-detected frameworks: Next.js, Vite, Astro, Nuxt, Angular, SvelteKit, Remix, Gatsby, CRA, Plain HTML, PHP.

## Interpreting Results

- `!!` **Error**: Render-blocking issue — fix immediately
- `!~` **Warning**: Significant weight contributor — fix in performance-critical pages
- `~~` **Info**: Minor optimization opportunity (only with `--strict`)

## Fix Priority

1. **Render-blocking CSS** — inline critical CSS, defer the rest
2. **Render-blocking JS** — add `defer` or `async`, move before `</body>`
3. **Third-party scripts** — defer/async or load via tag manager
4. **Font loading** — add `font-display: swap` + preload
5. **HTML bloat** — extract SVGs, remove data URIs, trim meta tags

## Detailed Rules

For complete detection rules, edge cases, and fix patterns, read [references/14kb-rules.md](references/14kb-rules.md).
