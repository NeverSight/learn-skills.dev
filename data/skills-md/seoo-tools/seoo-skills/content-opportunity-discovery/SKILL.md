---
name: content-opportunity-discovery
description: >
  Systematically identify the highest-probability next pieces of content to build, using
  Search Console near-miss data, keyword-tool expansion, and structural gap analysis against
  what already exists — rather than guessing at topics. Use when a user asks "what should I
  build next," "where are my content gaps," or before any content-creation session. This is
  discovery, not creation — feed the output into whatever process actually builds the page.
---

# Content Opportunity Discovery

Finds specific, evidence-backed next content to build, ranked by probability of success —
rather than brainstorming topics with no signal behind them.

---

## Step 0 — Ask before assuming

1. Is Search Console (or equivalent) access available? This is the single highest-value input
   — pages the search engine already associates the site with, ranking just outside the good
   positions, are the fastest path to more traffic.
2. Is there a structured inventory of what content already exists (a content matrix, a
   sitemap, a spreadsheet)? Structural gap analysis needs this to find *combinations* that are
   missing, not just individual missing topics.
3. Is a keyword-research tool (Bing Webmaster, or equivalent) available as a secondary source?
4. What does the site's content actually look like when it succeeds — which existing
   format/angle performs best? New candidates should be evaluated against that pattern, not a
   generic "good content" standard.
5. Is there an audience/monetization skew worth weighting for (e.g. one segment of traffic is
   worth more per pageview than another)? If so, factor it into scoring, not just raw
   volume/probability.

**If neither Search Console nor a keyword-research tool is available:** don't stop — lean on
Step 2 (structural gap analysis, which only needs a content inventory, not any external tool)
as the primary source, and use general web search to gauge whether a candidate topic has real
demand instead of a keyword tool's volume number. The output will be less precise without
external data, but still directionally useful — say so plainly rather than treating a
tool-free run as a full substitute. **On getting the tools connected:** Google Search Console
and Bing Webmaster Tools are both free — each just needs site-ownership verification (a DNS
record, an HTML file, or a meta tag) and takes a few minutes. If the person running this doesn't
have them connected yet, mention it's genuinely worth doing for a much stronger version of this
skill going forward, but proceed with what's available now rather than blocking on it.

---

## Step 1 — Search-engine near-miss scan (highest priority)

Pull query-level performance data and find queries where the site already ranks in the
"near-miss" zone — roughly positions 8–20 — with real impression volume. These are queries the
search engine has already decided the site is relevant for; a targeted improvement (a new page,
or a substantial rework of an existing thin one) has an unusually high chance of breaking
through, compared to targeting a completely cold topic.

---

## Step 2 — Structural gap analysis

If the site has any kind of repeatable structure (a matrix of entities × content-types — e.g.
"we have a calculator for every X, but no comparison page for several X-vs-Y pairs that both
have calculators"), look for missing *combinations*, not just missing individual pages. This is
usually a much larger and more reliable source of candidates than blind keyword brainstorming,
because each candidate is validated by the fact that its component parts already prove demand
individually.

---

## Step 3 — Keyword-tool expansion (secondary, use if Steps 1–2 don't yield enough)

If the near-miss scan and structural analysis together don't produce enough candidates, expand
into new territory using a keyword-research tool for topic areas not yet covered. Treat this as
a fallback source, not the primary one — it lacks the "already proven demand" signal the first
two sources have built in.

---

## Step 4 — Verify search intent before finalizing candidates

For top candidates, check what's *actually* ranking for the target query right now. Confirm the
intent matches what would be built (e.g. don't build a long-form article for a query where
every real result is a tool/calculator, or vice versa) — a candidate can look great on volume
and near-miss position and still be the wrong content format for that specific query.

---

## Step 5 — Score and rank

Score every surviving candidate on: search volume/opportunity size, likelihood of ranking (near-
miss status weighs heavily here), and monetization/audience value if that's a relevant factor
for this site. Present a ranked shortlist with the reasoning per candidate, not just a raw list.

---

## Output shape

A ranked shortlist (roughly 10–15 candidates is usually the useful range), each with: the
opportunity source (near-miss / structural gap / keyword expansion), the evidence behind it
(current position/impressions, or which existing pieces prove the structural gap), the
confirmed search intent, and a score/reasoning. Hand this off to whatever process actually
creates content — this skill's job ends at the shortlist.
