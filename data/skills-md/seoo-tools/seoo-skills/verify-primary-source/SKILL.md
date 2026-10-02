---
name: verify-primary-source
description: >
  Verify any factual claim, number, threshold, rate, spec, or rule published on a content
  site against its one authoritative canonical source before publishing or editing it.
  Use before changing any figure in content, when confirming whether a flagged passage is
  actually wrong, or when auditing a site for factual accuracy. Trigger when a user asks
  "audit my site's accuracy," "is this figure still correct," "what's the source for X,"
  or when running any wider content-quality audit that touches factual claims. Prerequisite
  for content-freshness-audit and protected-field-audit (this pack).
---

# Verify Primary Source

Confirm the correct, current value of any published fact from its one authoritative source
before trusting or editing it. A checkable claim is never confirmed by assumption — always by
checking the source.

---

## Step 0 — Ask before assuming

1. What kind of claims does the content actually make (prices, specs, dates, regulatory
   thresholds, statistics, rankings, product data)?
2. Is there an existing source-of-truth mapping (a spreadsheet, a data source, an API), or does
   each page just state facts inline with no tracked source?
3. How many pages/claims are in scope? A 20-page site and a 2,000-page site need different
   sampling strategies (full check vs. representative sample + risk-tiering).
4. How often do the underlying facts actually change (daily prices vs. annual regulatory
   figures vs. essentially-static facts)?
5. Is there a specific known worry, or is this a cold-start audit?

Scope the rest of this skill to the answers — don't run every step unmodified if some don't apply.

**If the site owner can't answer some or all of these, proceed anyway rather than blocking**:
sample claim types directly from the visible content, build a best-effort source mapping from
general knowledge of the niche (flag it as provisional), and default to a representative sample
across page types rather than full coverage when scale is unclear.

---

## Step 1 — Identify the authoritative source, per claim type

For every distinct claim type, identify the one canonical source it should be checked against:

| Claim type | Authoritative source | Why not a secondary source |
|---|---|---|
| Product pricing | The vendor's own live pricing page | Third-party roundups lag and mis-tier pricing |
| Regulatory threshold | The issuing government/regulatory body's own page | Summary sites are one layer removed and propagate stale figures |
| A statistic attributed to a study | The study/publisher itself | Citing articles routinely mis-transcribe numbers |

Rule: always prefer the primary originator of the fact over anyone summarizing it. A secondary
source is acceptable only to *locate* the primary source — never as sole confirmation.

If this mapping doesn't exist yet, build it as part of the audit — it's a deliverable in its
own right, not just a means to an end.

---

## Step 2 — What to check, by claim shape

- **Numeric thresholds/rates**: confirm the exact value, not a rounded approximation; confirm
  which tier/segment it applies to.
- **Dated/versioned facts**: confirm the source's own "last updated"/"effective as of" date
  actually matches the period the site claims it for.
- **Rankings/superlatives** ("the cheapest," "#1 in X"): re-verify independently of the
  individual figures behind them — the inputs can all still be correct while the ranking itself
  has flipped.
- **Derived/calculated figures**: verify each input separately, then re-derive the output.

---

## Step 3 — Fetch and extract

1. Retrieve the source directly — don't rely on a cached summary or memory of it.
2. Check the source's own "last updated" date against the period being claimed.
3. Prefer a value in a table/structured data over one in prose.
4. If multiple periods/tiers/versions are shown, confirm which row/column applies.
5. A source in another language is still usable — the numeric value transfers directly.

---

## Step 4 — Compare to what the site currently claims

- **Correct** → record it as checked (Step 6); no edit needed.
- **Stale** → note old value, new value, source — a finding.
- **Conflicting sources** → do not silently pick one. Flag explicitly for the site owner's
  judgment (common causes: transition period, tier mismatch, fiscal-vs-calendar mismatch).

---

## Step 5 — Acceptable vs. unacceptable secondary sources

Acceptable for cross-checking only (never as sole confirmation): established industry-specific
reference sources for the niche; the primary source's own official secondary publications.

Never acceptable as a sole source: general news/blog articles, crowd-edited references,
competitor sites, AI-generated summaries with no cited source of their own.

---

## Step 6 — Record what was checked

For every claim verified: record the confirmed value, the source URL, and the date checked
(a spreadsheet row or a content-file comment is enough). See `content-freshness-audit` (this
pack) for tracking *when* a claim is next due for re-checking.

---

## Output shape

Per claim type sampled: the claim + location, confirmed value + source, and status (confirmed
correct / stale / conflicting sources — flagged / could not verify).
