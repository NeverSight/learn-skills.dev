---
name: ad-negative-keywords
description: "Build and maintain negative keyword lists from search term reports to cut wasted ad spend in paid search - n-gram query mining to surface irrelevant search terms, the right negative match types and exclusion levels (account, shared list, campaign, ad group), and a review cadence that avoids overblocking queries that convert. Use whenever the user mentions a search term or search query report, irrelevant clicks, junk traffic, wasted ad spend, or wants to exclude or block keywords - even if they never say 'negative keywords'. Covers B2B lead gen and B2C/e-commerce; needs the account's query data. Do NOT use for account-wide underperformance with no query-level evidence - use mbfinotti/advertising-skills@ad-account-diagnostic instead."
license: MIT
metadata:
  author: Maya-Beth Finotti
  version: "1.1.8"
---

# Negative Keywords

Build and maintain a negative keyword list from search term reports, so paid-search budget stops leaking to irrelevant queries - without blocking the queries that convert.

The mechanics - match types, exclusion levels, thresholds, cadence - are identical for B2B lead gen and B2C/e-commerce. Two things differ by segment:

- Which junk categories dominate (see taxonomy).
- The decision data: B2B's sparse conversions force click/cost gates, B2C volume allows conversion-based gates.

## Evidence gate

- Never propose specific negative keywords for a live account without its search term report (also called search query report).
- Missing report → request an export, explain the overblocking review below, and name zero candidate negatives in the meantime.
- Exception: a brand-new campaign with no history may get a starter exclusion list - label it "pre-launch starter, review against real queries after 7-14 days".

A list invented from imagination has no evidence of what actually matches, and its cost, blocked converting queries, stays invisible.

## Clarifying questions

Ask once, briefly, before analyzing. Skip anything already answered. This is a tactical pass, not an interview.

1. What counts as a conversion, and what is the target CPA or ROAS?
2. What date range does the report cover, and roughly what did the account spend over it?
3. What CPC range does the account run? (Sets the click threshold.)
4. Which queries or themes must never be blocked - brand terms, converting themes, deliberate competitor bidding?
5. Which levels can you edit: account/shared list, campaign, ad group?
6. By what date must the saving show up in the account's numbers?
7. Is this a one-off cleanup, or a standing maintenance job you want to keep compounding?
8. What is the effort ceiling per pass - minutes available, who else has to approve a change, and can you reverse an account-level exclusion yourself?

Re-rank this skill's two option menus (exclusion level, cadence) against those answers:

- A hard date promotes the fast local rungs - ad group or campaign negatives applied in this pass.
- A standing-maintenance mandate promotes the compounding rungs - shared exclusion lists plus the quarterly conflict sweep.
- A tight effort ceiling or a slow approval path demotes account-level exclusions, which cost the most to audit and the most to reverse.

Every ordering below is a default, not a law: it shifts with the account and with who executes it. Re-rank against what you already know about this user - an in-house scripting ability makes the n-gram pass and the conflict sweep far cheaper than the default order assumes, and a shared list already built and attached makes that rung near-free. Where an answer rules a rung out entirely rather than moving it, delete it by name (see step 7).

## Core mechanics

Read before adding anything - most negative-keyword damage traces to these rules.

- Positive keywords expand automatically to close variants.
- Negative keywords do NOT expand to close variants. Add plurals, synonyms, and word stems as separate negatives yourself.
- Casing and misspellings are matched automatically.
- Negative match types, ranked by waste blocked per unit of overblocking risk: `phrase > exact > broad`.
  - Phrase (default) - blocks the words in that order; extra words around them still block. Best ratio: one entry kills a whole junk theme, and a wrong call costs that theme, not the account.
  - Exact - blocks only that literal query. Safest and narrowest: use it for a surgical block next to converting siblings. It needs one entry per variant, so a list built mostly of exacts becomes a standing job.
  - Broad - blocks any search containing ALL the words, in any order. Widest reach and widest blast radius: one bad broad negative silently zeroes a converting theme. Reserve for terms that are wrong in every recombination.
- Axes disagree:
  - reach: `broad > phrase > exact`
  - overblocking risk: `broad > phrase > exact`
  - upkeep effort: `exact > phrase > broad`
- Move up to broad only when the term is wrong in every recombination AND the conflict check against active keywords comes back clean. Move down to exact when the term sits one word away from a converting query.
- Check the platform's default match type when adding from a report - some default to exact, which blocks the fewest searches. Switch to phrase deliberately.
- Negatives always beat positives: a blocked active keyword still displays as active but never enters the auction.

## Workflow

1. Pull the search term report for the lookback window.
   - 7-14 days for a recurring weekly pass.
   - 30-90 days for a first cleanup or a low-volume account.
2. Sort by cost descending. Filter to zero conversions. This surfaces the spend producing nothing.
3. Mark a term as a candidate when it crosses either gate:
   - 15-20 clicks with zero conversions (tighten to 10-12 when CPC is high, roughly $3+).
   - Spend of 1.5-2x target CPA with zero conversions, regardless of click count.
   - Low-volume B2B: conversion data is too sparse to gate on - rely on the click/cost gates plus clear irrelevance from the taxonomy.
4. Classify each candidate with the taxonomy below. A merely uncertain term is not a candidate - leave it to collect more data.
5. Run the overblocking review on every candidate:
   - Ever converted in account history (the term or a close sibling)? Do not negate.
   - Would the chosen match type also block a plausible converting query? Narrow the match type or wording.
   - Conflicts with an active keyword anywhere in the account? The negative silently zeroes that keyword.
6. Set the match type per the ranking in Core mechanics, then expand variants manually: plural/singular, synonym, and stem forms.
7. Pick the level, ranked by waste blocked per unit of blast radius: `shared exclusion list > ad group or campaign > account`.
   - Shared exclusion list (default) - for a recurring theme across campaigns. Costs about an hour once: name it by taxonomy category, attach it, document it. After that every new campaign inherits it by attachment, so the payoff compounds. Reversible by detaching, and the blast radius stops at what you attached.
   - Ad group or campaign - for a query genuinely local to one container. Near-zero effort, near-zero blast radius, and near-zero durability: the same term resurfaces in the next campaign and gets negated again from scratch.
   - Account level - for universal disqualifiers and brand-safety terms only. Widest reach, and the worst reversibility of the three: it suppresses everywhere, including campaigns built later by someone who never saw the list, and nothing in those campaigns points back at it.
   - Axes disagree:
     - reach: `account > shared list > ad group`
     - setup effort: `shared list > account == ad group`
     - effort to audit later: `account > shared list > ad group`
     - reversibility: `ad group > shared list > account`
   - Account and ad group tie on setup effort because both are the same act - paste the term into one container's negative list, near-zero either way. Everything that separates them lands after setup, on reach, audit and reversal.
   - What the efficiency order starves: the account-level exclusion. It buys the widest reach of the three and it is the one rung nobody can audit or reverse cheaply, so a ratio always picks something smaller. Promote it anyway for a universal disqualifier or a brand-safety term - the terms whose cost of leaking once is higher than the cost of an over-wide block - and the third time the same term needs negating in a new container.
   - Move down when the term is only wrong for one product line, geography, or campaign intent.
   - Delete, don't demote: with no edit rights at account level, that rung leaves this user's menu and is reported as deleted, not ranked last. Same for the shared list on a platform that has no shared-list object at all - plan on per-container negatives and a written re-application step, rather than a rung the account cannot express.
8. Deliver in the output shape below. On a live account, present a draft for approval - never mass-apply silently.
9. Log the change (date, terms, level, match type, reason) and schedule the next pass per the cadence.

## Query mining for hidden terms

Platforms hide a large share of search terms - practitioner measurements center around 40% of spend. Token-level mining recovers signal the report no longer shows:

1. Export all visible search terms with cost, clicks, conversions.
2. Tokenize each query into unigrams, bigrams, and trigrams.
3. Aggregate cost and conversions per token across every query containing it.
4. Sort tokens by cost descending, filter zero conversions, apply the same gates as the main workflow.
5. Negate bad tokens as phrase negatives. Flag high-converting tokens as expansion leads for the account owner - positive keyword research is out of this skill's scope.

- Can run scripts: a short tokenizer over the export is the fast path.
- Can't run scripts: do the same aggregation in a spreadsheet - split words into columns, pivot, sum cost per token. Same logic, smaller scale.

These two are deliberately unranked: capability decides, not efficiency. The tokenizer is only cheaper for someone who already writes scripts, and the spreadsheet produces the identical aggregation.

## Cadence

Axes disagree:

- value (waste caught per hour): `recurring search-term pass > quarterly conflict sweep > monthly list audit`
- standing cost: `recurring pass > monthly list audit > quarterly conflict sweep`

Get the top rung running before adding either other one. The sweep is the cheapest commitment on the page and still outranks the audit on value.

- Recurring search-term pass - budget 30-45 minutes.
  - Weekly, 7-14 day lookback: higher-spend accounts (~$10k+/month), or anything new or in a learning phase.
  - Bi-weekly to monthly: stable lower-spend accounts.
  - Several near-empty passes in a row → lengthen the interval.
- Quarterly conflict sweep - a full conflict check against active keywords, plus the match-type review (are broad negatives over-blocking?). Four short runs a year that catch the most expensive failure in this skill: a negative silently zeroing a keyword that was serving.
- Monthly list audit - prune stale entries from shared exclusion lists, merge duplicates. Hygiene only: defer it while the recurring pass is still surfacing real waste.

## Irrelevant-query taxonomy

Same categories for B2B and B2C; the weighting differs.

| Category              | Signals                                                   | Hits hardest                                           |
| --------------------- | --------------------------------------------------------- | ------------------------------------------------------ |
| Competitor            | competitor brand names                                    | both - strategy call, confirm before negating          |
| Job seeker            | jobs, careers, salary, hiring, intern, resume             | B2B                                                    |
| DIY / free intent     | free, diy, template, cheap, open source                   | B2B                                                    |
| Informational         | what is, how to, meaning, tutorial, course, pdf           | B2B                                                    |
| Wrong geography       | cities/countries not served                               | both                                                   |
| Wrong product tier    | used, refurbished, wholesale, mini, for kids, replacement | B2C                                                    |
| Comparison / research | reviews, best, vs, comparison                             | both - often early-funnel, not junk; judge per account |
| Unsafe / brand-unsafe | adult, illegal, tragedy-adjacent                          | both                                                   |

- Treat competitor and comparison terms as strategy calls, never automatic junk - some accounts bid them deliberately. Ask first.
- B2C/e-commerce adds attribute mismatches (size, color, gender, model) the catalog can't serve.

## Output shape

Deliver every pass as:

1. Summary: spend analyzed, wasted spend found (cost on zero-conversion candidates), % of total, and any exclusion level deleted from this account's menu with the constraint that deleted it.
2. Additions table: term | match type | level | evidence (clicks, cost, conversions) | category | variants added.
3. Do-not-negate list: candidates that failed the overblocking review, with the reason.
4. Watchlist: uncertain terms left to collect data, each with the gate that would trip it.
5. Next review date.

See [references/worked-example.md](references/worked-example.md) for a filled-in B2B pass and an e-commerce pass, plus a negative example of what not to do.

## Failure modes

- Overblocking: every negative narrows reach, and a healthy account's true waste is often only 4-8% of spend. Negate the clearly wrong, never the merely uncertain.
- Negating a converting term: the single most expensive mistake - the overblocking review exists for it. Check conversion history first, always.
- Forgetting the close-variant asymmetry: a negative blocks "running shoes" but not "running shoe". Lists without manual plural/synonym variants quietly leak.
- Default match-type trap: adding from the report at a default of exact blocks almost nothing - the list looks maintained while the waste continues.
- Conflicts with active keywords: a negative above an active keyword silently zeroes it. Run the quarterly sweep. Re-check whenever adding broad negatives.
- Volume worship: more negatives is not better. A large published study of account-level exclusions found near-zero CPA/ROAS difference versus accounts without them - where and how negatives are applied matters more than how many.
- Query-length blind spot: very long searches can slip past negatives positioned late in the phrase - never rely on negatives alone for brand safety.

## Objective and measurement

- Primary KPI: wasted spend share = cost on zero-conversion irrelevant terms / total analyzed spend, recomputed each pass on the same lookback window length.
- Pass threshold: after 90 days on cadence, wasted spend share under 10% of non-brand spend AND zero converting terms blocked (verify against the change log and conversion history).
- Secondary KPIs:
  - CPA/ROAS delta across adjacent equal-length windows.
  - Reclaimed non-brand spend - practitioners report 10-20% reclaimed within 90 days on previously unmanaged accounts.
- Already at 4-8% wasted share? The account is near its practical floor: shift effort to the conflict sweep and watchlist, and lengthen the cadence rather than forcing new exclusions.

## References

- [references/worked-example.md](references/worked-example.md) - worked B2B and e-commerce passes in the output shape, plus a negative example.
- [references/platform-notes.md](references/platform-notes.md) - optional vendor-specific notes (defaults, limits, keywordless surfaces). Load only when the user names their platform.
- mbfinotti/advertising-skills@ad-bidding-strategy - bid strategy decisions.
- mbfinotti/advertising-skills@ad-spend-allocation - budget allocation across campaigns.
- mbfinotti/advertising-skills@ad-budget-pacing - campaign pacing and spend distribution.
- mbfinotti/advertising-skills@ad-account-diagnostic - account-wide underperformance diagnosis.
- mbfinotti/advertising-skills@paid-landing-page-audit - landing page optimization.
- mbfinotti/advertising-skills@ad-copy-variants - ad copy and creative testing.
