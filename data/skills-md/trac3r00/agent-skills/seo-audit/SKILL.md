---
name: seo-audit
description: Scores on-page SEO for HTML files — title length, meta description, single h1, image alt text, canonical link, Open Graph tags, and html lang. Reads a saved HTML file or stdin (from curl), fully offline and deterministic, no Lighthouse or browser needed. Use before publishing any page, in CI on static builds, or when auditing a site without spinning up a browser.
when_to_use: You built or are about to publish a page and want the basics that decide whether it can rank and share correctly. NOT a full SEO platform (no backlinks, no keyword research, no Core Web Vitals) — it covers the on-page HTML that the page itself controls.
version: 1.0.0
license: MIT
metadata:
  agentskills:
    tags: [seo, html, web, meta, on-page]
---

# SEO Audit

The on-page basics that decide whether a page can rank, in one deterministic
check — no browser, no API, no Lighthouse.

## Commands

```bash
python3 scripts/seo_audit.py dist/index.html
python3 scripts/seo_audit.py dist/*.html --json
curl -s https://example.com | python3 scripts/seo_audit.py - --json
python3 scripts/seo_audit.py page.html --min-score 85
```

## Checks

| Check | Pass | Warn/Fail |
|---|---|---|
| `title` | 10-70 chars, non-empty | fail otherwise |
| `meta_description` | 50-160 chars | fail otherwise |
| `h1` | exactly one | fail otherwise |
| `image_alt` | every image has alt text | fail otherwise |
| `canonical` | present | warn if missing |
| `og_tags` | og:title + og:description | warn if missing |
| `lang` | html lang attribute | warn if missing |

Score = average of check weights (pass=100, warn=60, fail=0). Default gate:
exit 1 below 70.

## Pairs with

`webapp-testing` (browser-level QA after the static checks pass),
`doc-reader` (extract the HTML first if it is buried in a document).
