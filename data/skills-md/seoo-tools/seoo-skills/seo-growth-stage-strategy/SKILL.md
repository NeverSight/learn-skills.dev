---
name: seo-growth-stage-strategy
description: >
  Determine how much SEO tinkering is actually appropriate for a site right now, before
  recommending any optimization action — a small/growing site and a mature one need opposite
  advice. Use at the start of any SEO engagement, before running any other audit skill in this
  pack, or when a user asks "should I be optimizing more" or "why isn't more tinkering helping."
  This is a gating skill: its answer changes what the other audit skills should even recommend.
---

# SEO Growth-Stage Strategy

Answers a question every other skill in this pack depends on: is this site at a stage where
adding coverage matters more than polishing what exists, or the reverse? Don't run a full
optimization audit on instinct — establish the stage first.

---

## Step 0 — Ask before assuming (this IS the skill, more than usual)

1. **How much content/coverage exists relative to the site's addressable topic space?** Still
   filling obvious gaps, or reasonably comprehensive already?
2. **How mature is the traffic?** Growing steadily, plateaued, or declining? Roughly how much
   traffic/revenue is at stake if something goes wrong?
3. **How much has actually been tinkered with already** — titles, structure, technical
   fixes — versus how much is genuinely new content?
4. **Is there a current, active concern** (a real drop, a suspected issue) or is this a
   proactive check-in with nothing specific wrong?
5. **What would "success" mean right now** — more coverage, better conversion on existing
   traffic, or just stability?

Do not skip this and jump straight to recommending fixes. The right answer to "should you
optimize this page" is genuinely different depending on the answers above.

**If none of this can be answered:** infer from whatever's directly observable — rough page
count, how recently content looks like it was added or updated, any traffic/revenue figures
volunteered elsewhere in the conversation — and, absent any of that either, default to treating
the site as early/growth-stage. That's the lower-risk assumption: biasing toward "build more
coverage" when the site is actually mature costs some efficiency, but biasing toward "hold back
and just optimize" when the site is actually still small risks under-investing in the thing that
matters most at that stage. Note explicitly that the assessment is an inference, not confirmed.

---

## Step 1 — Early/growth-stage guidance (small, still filling coverage gaps)

Bias toward **volume and coverage over polish**. At this stage, the highest-ROI activity is
usually filling gaps (see `content-opportunity-discovery`, this pack) rather than incrementally
optimizing pages that already exist — there's more value in a topic not yet covered at all than
in shaving a few percent off an existing page's CTR. Keep the other audit skills' findings on
file, but weight recommendations toward "build the missing thing" over "fine-tune the existing
thing," unless something is actively broken (see Step 3).

---

## Step 2 — Mature/plateaued-stage guidance (comprehensive, growth has slowed)

Bias shifts toward **protecting and optimizing what already exists**. New-content ROI
diminishes once coverage is reasonably comprehensive, while the value of defending existing
rankings, fixing real quality/compliance issues (`page-quality-audit`, `protected-field-audit`,
this pack), and careful, measured optimization (`measurement-discipline`, this pack) rises. This
is also the stage where the full discipline of that measurement skill matters most — more is at
stake per change, so isolating cause and effect properly is worth the overhead it costs.

---

## Step 3 — Always: separate a real emergency from normal fluctuation, regardless of stage

Some things warrant immediate action at *any* stage, bypassing the growth-vs-mature framing
above entirely: a sudden major traffic drop, the site appearing broken, search-engine-reported
indexing errors. These are different in kind from ordinary ranking movement, and shouldn't wait
for a scheduled review cycle.

**Before reacting, determine whether the movement is broad or narrow** — this changes what the
correct response is:
- **Broad** (many unrelated pages moved together, same direction, same time) → likely an
  external cause (an algorithm update, a technical/infrastructure break) rather than anything
  about the specific pages. Investigate the external cause first; don't start editing individual
  pages in response to a site-wide event — that risk making unrelated changes indistinguishable
  from the real cause later.
- **Narrow** (a specific page or small cluster moved, nothing else did) → likely genuinely
  about that content/those pages. This is where a targeted audit (the other skills in this
  pack) is the right response.

Reacting to a broad decline with narrow, page-level tinkering — or reacting to a narrow issue by
assuming it's a site-wide event and doing nothing — are both real, common mistakes worth
explicitly checking against before recommending any action.

---

## Output shape

A stated stage assessment (early/growth vs. mature/plateaued, with the reasoning), a
recommendation on where effort should go right now (coverage vs. optimization, weighted
accordingly), and — if there's an active concern — an explicit broad-vs-narrow classification
with the reasoning, before any specific fix is recommended.
