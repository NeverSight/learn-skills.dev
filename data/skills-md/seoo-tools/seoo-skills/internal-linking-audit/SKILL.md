---
name: internal-linking-audit
description: >
  Audit a site's internal linking structure to find where existing authority isn't being
  redistributed to pages that could use it. Use when auditing any multi-page site's link
  structure, after a batch of new content is published, or when a user asks "are my internal
  links okay" or "why isn't this page ranking despite good content." Fixing internal links
  redistributes authority the site already has — often faster ROI than publishing new pages.
---

# Internal Linking Audit

Checks whether link equity actually flows to the pages that need it, not just whether links
exist somewhere.

---

## Step 0 — Ask before assuming

1. What content types/tiers exist, and what's each one's intended role? (e.g. deep
   terminal pages that should *receive* links, hub/connector pages that should link *out* to
   several terminal pages, topic-aggregator pages that collect a cluster.) Different tiers need
   different link behavior — auditing them all the same way misses real structural gaps.
2. How are internal links actually implemented — a structured field/array per page, inline
   links in body content, both?
3. Is Search Console (or equivalent) access available? Cross-referencing link structure against
   real performance data is what turns "here are some missing links" into "here are the highest-
   ROI missing links."
4. Roughly how many pages exist per content type/tier, and how fast is new content being added?
   A structural gap between two tiers can persist and even worsen as the site grows if nothing
   ever explicitly checks for it — growth alone doesn't self-correct a linking gap.

**If tiers/roles aren't defined:** infer likely tiers directly from URL structure and observable
page-type patterns rather than asking for a formal definition. **If there's no Search Console
access:** Step 2's structural tier-to-tier gap check doesn't need it — run that regardless — and
note that Step 3's prioritization will be based on structural signals alone rather than real
performance data. If the person running this doesn't have Search Console connected, it's free
and worth setting up (verify site ownership via a DNS record, HTML file, or meta tag) — mention
it as a genuinely useful step, but don't block on it.

---

## Step 1 — Map content tiers and expected linking relationships

Before counting anything, define what "correct" linking looks like for this specific site:
which tier should link to which. A common shape: terminal/deep pages ← comparison/connector
pages ← topic hub pages, with hub pages also receiving back-links from their own sub-pages.
Write this down explicitly — it's the yardstick everything else gets measured against.

---

## Step 2 — Build the actual link graph and check it against the expected shape

For each page, record its outbound links (target + tier) and compile inbound counts per page.
Then check specifically for **tier-to-tier gaps** — an entire category of expected links that's
near-zero across the whole site, not just individual missing links on individual pages. This
kind of gap is easy to miss page-by-page and is usually the highest-value finding, because
fixing it touches every page in the category at once. Also check the inverse: pages with
unusually low inbound counts relative to their tier's norm.

---

## Step 3 — Cross-reference against real performance data

For pages with thin inbound linking, check their actual search performance. Pages that are
already close to ranking well (moderate impressions, position just outside the top results) and
under-linked are the highest-priority fix — internal links redistributing existing authority is
often faster than any other lever available. Pages that are both thin on links *and* have no
real search demand are lower priority.

---

## Step 4 — Check the linking mechanism itself, not just the current link counts

- Minimum outbound links per page from genuine body/contextual content, not just a footer list.
- Descriptive anchor text (not "click here").
- **A backfill step for new pages**: when a new page is published, does anything systematically
  find every *existing* page that should now link to it, or does the new page just sit there
  with only its own outbound links until someone remembers to add inbound ones? A one-time
  forward-looking check ("does this new page link out correctly") isn't enough — the more common
  gap is the reverse direction.

---

## Output shape

Any structural tier-to-tier gap found (with rough page counts affected — this is usually the
headline finding); a ranked list of specific pages that are both near-ranking and under-linked;
mechanism findings (thin outbound links, poor anchor text, no inbound-backfill process); and a
concrete action plan ordered by estimated impact, not just by ease of implementation.
