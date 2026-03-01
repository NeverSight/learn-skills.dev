---
name: canonicalizing-urls
description: >
  Use when working with any URL that may contain tracking parameters, redirect
  wrappers, locale prefixes, or opaque share links — to produce a clean,
  canonical form. Triggers proactively when the agent uses a URL in a context
  where cleanliness matters (saving to Notion, quoting in a document, creating
  a hyperlink). Also triggers explicitly when the user says "canonicalize",
  "clean this URL", "strip tracking params", or invokes /canonicalize.
metadata:
  author: William-Yeh
---

# canonicalizing-urls

Canonicalize URLs by running `scripts/canonicalize.py` (requires `uv`).

## Proactive use

When a URL appears in a context where it will be saved, shared, or cited:
1. `uv run scripts/canonicalize.py <url>` (offline, static rules only)
2. If the URL matches an opaque short-link pattern (e.g. `/share/p/`), add `--online`
3. If the result differs from the input, substitute the canonical form
4. Note the change inline: "(canonicalized: removed fbclid)"

## Explicit use

When the user asks to canonicalize a URL:
1. `uv run scripts/canonicalize.py <url>`
2. If unchanged and URL looks non-canonical, run `--probe` to discover rules

## Adding a new rule

When the script returns unchanged output but the URL is clearly non-canonical:
1. `uv run scripts/canonicalize.py --probe <url>` — review suggested actions
2. Ask user: generalize to a pattern, or keep domain-specific?
3. Add the confirmed `Rule(...)` to `RULES` in `scripts/rules.py`
   (insert after similar-domain rules, before the closing bracket)
4. `uv run scripts/canonicalize.py <original_url>` — verify output
5. Commit: `feat: add <domain> canonicalization rule`
