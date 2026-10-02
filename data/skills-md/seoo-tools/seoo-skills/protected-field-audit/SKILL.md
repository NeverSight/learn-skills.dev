---
name: protected-field-audit
description: >
  Check whether a page's title, meta description, headings, or other SEO-load-bearing fields
  are still factually true — not just whether they're optimized. Use when auditing any site
  where content gets edited over time, especially one with many templated pages where a
  sitewide data correction can miss the titles/headings that quote a now-outdated figure.
  Builds on verify-primary-source (this pack) to confirm what the correct value actually is.
---

# Protected-Field Audit

Checks for a specific failure mode: a page's body gets corrected when a fact changes, but its
title, meta description, or a heading — fields treated as "don't touch" for SEO reasons — still
quotes the old figure. The page ends up contradicting itself.

---

## Step 0 — Ask before assuming

1. Is there a policy of not touching titles/meta/headings once set? If so, this is exactly
   where this failure mode hides.
2. How does content get corrected when a fact changes — manual edit, scripted find-and-replace,
   automated pipeline? Automated corrections are *more* likely to miss protected fields, often
   deliberately scoped to "body only" to avoid SEO risk.
3. Which fields does the site consider "protected" (never touched without explicit sign-off)?
4. Has a recent bulk accuracy fix touched body content but explicitly excluded titles/headings?
   If so, that's the first place to check.

**If there's no defined "protected fields" list:** default to treating title, meta description,
and H1 as protected — that's a safe universal baseline regardless of the site — and check those
at minimum even without an answer to Step 0.3.

---

## Step 1 — Find quantitative/factual claims in protected fields

For every page, extract any number, superlative, date, or specific claim in a title, meta
description, heading, FAQ question, or similar protected field.

---

## Step 2 — Compare each claim against current body content

- **Consistent** → no issue.
- **Contradicts the body** → the failure mode. Flag, showing both values side by side.
- **Body itself looks wrong too** → hand off to `verify-primary-source` (this pack) first.

---

## Step 3 — Distinguish "wrong number" from "wrong wording"

- **Number-only drift** (structure fine, just the digit is stale) → low-risk to fix directly.
- **Directional/structural drift** (the field's whole claim is now backwards or nonsensical) →
  a bigger edit with real keyword/positioning risk. Always flag for the site owner's explicit
  sign-off rather than rewriting autonomously.

Never leave a field asserting something the body now disproves — at minimum, flag it clearly
even when the full fix needs sign-off.

---

## Step 4 — Check the same pattern in derived/aggregate fields

Rankings, "best of" claims, and computed banners (e.g. a savings comparison) can go stale even
when every individual input is correct, because the *combination* changed. Re-check derived
claims whenever any input changes, not just the inputs themselves.

---

## Output shape

Per page: the protected field, its claim, and any body contradiction; classification
(number-only vs. directional/structural); and, if the pattern recurs across many pages, a note
to check whether a recent bulk-edit process explicitly excluded these fields.
