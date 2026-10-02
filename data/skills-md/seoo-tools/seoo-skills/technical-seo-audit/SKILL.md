---
name: technical-seo-audit
description: >
  Audit a page's technical SEO fundamentals — meta tags, canonical URLs, structured data,
  heading hierarchy, mobile basics. Use when auditing any page's on-page technical setup, when
  a user asks "is my technical SEO okay," or as part of a full site audit alongside
  page-quality-audit and internal-linking-audit (this pack). This dimension changes over time
  (Google periodically deprecates rich-result types) — verify current status rather than
  trusting a fixed list.
---

# Technical SEO Audit

Checks the mechanical/structural SEO layer: does Google's crawler and renderer get what they
need from this page, cleanly and without contradictions.

---

## Step 0 — Ask before assuming

1. What platform/CMS renders the pages? (Determines whether fixes are template-level, one-time
   fixes that scale, or truly per-page.)
2. Is there an existing sitemap/robots.txt, and when was it last checked for correctness?
3. Does structured data (schema/JSON-LD) already exist anywhere on the site?
4. Roughly how many distinct page templates exist? A technical issue found on one template
   instance is usually present on every page using that template — fix at the template level,
   don't patch instances one at a time.

**If any of the above is unknown:** check by examining a handful of live rendered pages directly
(view source, or fetch the page) rather than needing the platform/CMS named — most of what this
skill checks (meta tags, schema, heading structure) is directly observable from the rendered
page itself, and doesn't require background knowledge about the site's tech stack.

---

## Step 1 — Meta tags

- **Title**: Google truncates by *pixel width*, not character count — roughly 600px desktop /
  540px mobile, which works out to roughly 50–60 characters as a rough proxy (wide characters
  like "W" cost more width than narrow ones like "i"). Unique per page, primary term near the
  front. Verify current pixel/character guidance before treating any specific number as fixed —
  this shifts as Google's SERP rendering changes.
- **Meta description**: similarly pixel-width truncated (roughly 920px desktop / 680px mobile,
  ≈120–158 characters as a rough proxy). Unique per page, states the actual value proposition,
  not keyword-stuffed.
- **Canonical URL**: present, absolute, points to *this* page (not a different one — check for
  the common bug of every page on a template canonicalizing to the same wrong URL), consistent
  trailing-slash convention with the rest of the site.
- **Viewport tag**: present (`width=device-width, initial-scale=1.0`) — required for mobile-first
  indexing.

---

## Step 2 — Structured data (schema.org / JSON-LD)

Google periodically deprecates which schema types produce a *visual* rich result — deprecation
usually means the rich-result display stops, not that the underlying markup becomes invalid or
harmful. **Before recommending or auditing any schema type, check Google's current structured
data documentation for its live status** rather than assuming a type still produces a rich
result (FAQPage and HowTo, for example, no longer do — verify what else has changed since).
Check: valid JSON-LD syntax, required fields present for whatever type is used, and that the
markup actually matches what's visible on the page (mismatched schema is itself a violation).

---

## Step 3 — Heading hierarchy and on-page structure

- Exactly one H1 per page, containing the actual topic, not a generic template string.
- Logical nesting (H1 → H2 → H3, no skipped levels).
- **H2/H3 text should use semantic variants and related entities, not the primary keyword
  repeated verbatim** — this signals topical depth to Google rather than keyword stuffing, and
  is also just better for a human reader scanning the page.
- Target topic/term appears naturally in the opening content, not buried.

---

## Step 4 — Mobile and rendering basics

- No horizontal scroll at mobile viewport widths.
- Tap targets and text sized for mobile use without zooming.
- Confirm the page actually renders the same content to Google's crawler as to a browser
  (check for any client-side-only content that wouldn't be in the initial render).

---

## Output shape

Per template family (not per page, unless template-level fixes don't explain a specific
instance): meta tag issues (length/truncation, duplication, wrong canonical), structured data
status (valid/invalid, using a currently-supported type or not), heading hierarchy issues,
mobile-rendering issues. Flag anything found on one template instance as likely present
site-wide on that template.
