---
name: duplicate-intent-audit
description: >
  Detect pages that serve the same search intent as another page, even when their wording is
  different — the pattern Google's scaled-content-abuse policy targets, and the one most
  programmatic/templated sites are exposed to without realizing it. Use when auditing any site
  with more than a handful of templated/generated pages, when a user asks "do I have duplicate
  content risk," or after a Google core/spam update.
---

# Duplicate-Intent Audit

Checking for duplicate *text* is the wrong check. Google's scaled-content-abuse policy targets
duplicate *intent* — two pages answering the same query, even when a text-diff would call them
"different." A templated site can pass every plagiarism checker and still carry real penalty risk.

---

## Step 0 — Ask before assuming

1. How is content produced — hand-written, templated from a dataset, AI-drafted, a mix?
   Templated/programmatic sites are highest-risk for this specific problem.
2. Has the same *kind* of page ever been built under two different naming schemes at different
   times (a redesign, a new batch using a different template)? This is the most common root
   cause.
3. How many pages exist, and is a full URL/title list or sitemap available? This needs to look
   across the whole set — duplicate-intent pairs are invisible one page at a time.
4. Is Search Console (or equivalent) access available? Real click/impression/position data is
   the best signal for confirming a suspected pair is actually splitting authority.
5. Has anything already been merged/redirected? Avoid re-flagging resolved pairs.

**If there's no sitemap/URL list:** discover pages by crawling from the homepage (or whatever
URLs are available) and following internal links, or ask only for the domain and enumerate via
a search-engine site-search query. **If there's no Search Console access:** proceed with Step 1
(topic/entity clustering) regardless — it doesn't need performance data — and note in the
output that Step 3's survivor-selection will be based on content quality alone rather than real
performance data. On the tool/access point specifically: if the person running this doesn't have
Search Console connected, it's free and worth setting up (verify site ownership via a DNS
record, HTML file, or meta tag) — mention it as a genuinely useful one-time step, but don't
block the audit on it.

---

## Step 1 — Detect near-duplicate pages by topic/entity, not literal text

Literal text-overlap is a secondary signal only. Primary method:

1. For every page, extract the core entity/subject and the content-type/angle (overview,
   comparison, pricing breakdown, how-to).
2. Group pages sharing both. Any group of 2+ is a candidate cluster — investigate all of them,
   even if the prose reads completely differently. Low text-overlap does not clear a pair; it
   only means they weren't copy-pasted, which isn't the actual risk being checked.

Common root causes to check for:
- **Naming-convention drift**: the same page-kind built under two different naming patterns at
  different points in the site's history. Re-scan the *whole* site's naming patterns explicitly
  rather than trusting a narrower report is complete.
- **Reversed-pair content**: for "A vs. B" comparisons, check explicitly for "B vs. A."
- **Two-hub-per-entity**: more than one hub/landing template ever used for the same entity.

---

## Step 2 — Check for orphaned pages already superseded by a redirect

Check whether the site still builds pages at URLs already redirected away by rewrite rules
elsewhere in the stack — safe, easy deletions, easy to miss because production masks them.

---

## Step 3 — Use real performance data to pick the survivor

For each confirmed cluster, pull click/impression/position data (60–90 day window). Look for the
cannibalization signature: both pages near-invisible while a genuinely distinct related page
performs normally. Choosing the survivor: weigh existing position/clicks, actual content
quality (don't default to the higher-ranking page if it's thinner — merge the better content in),
and naming-convention fit. If both are near-invisible, search equity isn't a meaningful
tiebreaker — decide on content quality and naming consistency instead.

---

## Step 4 — Recommend prevention, not just cleanup

Recommend a creation-time check in whatever process generates new pages: before publishing,
check whether this entity+content-type combination already exists under any naming convention,
and whether a comparison's reversed pair already exists.

---

## Output shape

Every detected cluster with entity/topic + content-type shared, text-overlap % as secondary
data, likely root cause, performance data per page, recommended survivor + merge plan, any
orphaned-redirect pages, and a prevention recommendation for the content-creation process.
