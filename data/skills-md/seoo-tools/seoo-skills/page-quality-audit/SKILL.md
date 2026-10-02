---
name: page-quality-audit
description: >
  Audit programmatic/templated content against a concrete E-E-A-T and content-quality bar.
  Use when auditing any templated content page (a calculator, a comparison, a data-driven
  guide) for whether it would survive real scrutiny — from a reader, from Google's
  helpful-content/E-E-A-T standards, or from a spam-policy review. Works alongside
  duplicate-intent-audit (this pack) — that skill checks whether a page duplicates another
  page's intent; this skill checks whether a single page is actually good on its own.
---

# Page Quality Audit

A concrete, scorable checklist for content quality — not vague "make it more helpful" advice.

---

## Step 0 — Ask before assuming

1. Is the content YMYL-adjacent (money, health, legal, safety)? Stakes are higher there, but
   the checks below apply to any site.
2. How is content produced — human, AI-assisted, fully automated? The check is whether
   disclosure is honest, not whether AI-assistance is disqualifying.
3. Is there a stated verification/update process, even informal? If not, that's a finding.
4. How many pages share a template, and do they all get the same non-commodity treatment
   (Step 2)?

**If there's no answer on YMYL status:** apply the stricter standard by default — it's safer to
over-apply E-E-A-T rigor to content that turns out not to need it than the reverse — and note
the assumption in the output. **If production method is unknown:** still check disclosure
honesty (Step 1) directly from what the page itself states; that check doesn't require knowing
the answer in advance.

---

## Step 1 — Check honesty of attribution and process disclosure

- Never fabricate a named expert who didn't review the content — flag as a serious finding.
- If AI is used, disclose it honestly at the site level (what it does/doesn't do in the
  process). Per-page disclosure isn't necessary if the site-level one is clear.
- The real trust signal is a demonstrated process — a visible verification explanation, a
  visible last-updated date, a real contact/corrections channel — not an invented byline.
- Confirm sourcing goes to primary authorities (`verify-primary-source`, this pack) and
  "last updated" claims are actually current (`content-freshness-audit`, this pack).

---

## Step 2 — Check for the restated-data-table trap

A page that only reformats a public data table adds no value over the source, and is exactly
what scaled-content-abuse enforcement targets. Check every templated page for at least one
non-commodity element: a worked example, a cross-entity insight, a verified edge case, original
analysis of what the numbers mean. Pure "table, restated in prose" is a real finding.

---

## Step 3 — Check for shared boilerplate beyond navigation

Sample pages sharing a template and check what percentage of body text is byte-identical beyond
genuine nav/link elements. Large shared blocks are both a duplicate-intent risk
(`duplicate-intent-audit`, this pack) and independently a quality problem.

---

## Step 4 — Check claim hedging matches actual certainty

Flag absolute/guaranteed-outcome language on anything that's actually a projection ("you WILL
save $X") versus properly hedged, assumption-stated language ("you COULD save approximately
$X, based on [assumptions]"). Check that assumptions behind any projected figure are stated
plainly, not omitted.

---

## Step 5 — Check for genuine comprehensiveness, not just length

Check whether a page answers the actual question a real reader in this situation would have —
not just whether it hits a word-count target. A short page that answers the real question beats
a padded long one.

---

## Output shape

Per page/template family: attribution/disclosure honesty; presence of a non-commodity element;
shared-boilerplate percentage; overclaimed/unhedged language found; a comprehensiveness
assessment against the reader's actual likely question.
