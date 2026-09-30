---
name: social-calendar
description: >
  Turn content pillars, target platforms, and an honest posting cadence into a
  realistic 2-week content plan for LinkedIn, X, Instagram, Threads, Bluesky,
  and Facebook. Use when the user asks for a "content calendar", says "plan my
  week", "plan my next two weeks", or "what should I post this month". It
  balances pillars against formats (post, thread, carousel), anchors entries to
  real dates like launches and events, and deliberately leaves slack for
  reactive posting. It reads social-context.md for the user's brand voice,
  pillars, platforms, and stated cadence before planning anything. The output
  is a plan the user executes themselves — a markdown schedule of ideas with
  working hooks, not a queue of finished posts.
license: MIT
metadata:
  version: 0.1.0
  category: Plan
  topics:
    - planning
  examplePrompt: "Plan my next two weeks of LinkedIn and X content"
---

Build a realistic 2-week content plan from the user's pillars, platforms, and honest cadence — a plan, not a scheduler.

## Context

Read `social-context.md` at the project root (also check `.agents/social-context.md`) for the `## Voice`, `## Pillars`, `## Platforms`, `## Audience`, `## Cadence`, and `## Goals` sections. If the file is missing, offer to run the `social-context` skill first, but don't block — ask 2–3 quick inline questions and proceed:

- What are your 2–4 content pillars?
- Which platforms, and which one matters most?
- How many posts per week have you _actually_ sustained in the last month?

## Workflow

1. **Confirm cadence reality before anything else.** Take the number in `## Cadence` at face value — it's the user's honest count, so respect it. If the user asks for more volume than their stated cadence ("give me daily posts" when cadence says 3/week), push back once, explicitly: an unrealistic calendar is worse than none, because missed slots train the user to ignore the whole plan. Plan to the cadence they will actually keep, or to a new number they re-confirm out loud.
2. **Fix the date range.** Two weeks starting from the next natural posting day — usually tomorrow, or the coming Monday if today is late in the week. Ask about timezone only if an anchor date makes it genuinely ambiguous.
3. **Collect anchors.** Ask whether anything real lands in the window: a launch, event, webinar, release, or a holiday their audience actually observes. Anchored content is placed first; the rest of the plan flows around it. Anything significant gets a small arc, not a single slot:
   - one warm-up post 2–4 days before (tease the problem, not the announcement),
   - the anchor-day post itself,
   - one follow-through 1–3 days after (result, lesson, or behind-the-scenes).
4. **Distribute pillars.** Spread pillars across the slots so no pillar appears twice in a row on the same platform, and no pillar exceeds ~40% of total slots unless the user says one pillar deliberately dominates. Weight the mix toward the primary goal from `## Goals` — lead-gen tilts to pillars that show the product working; awareness and authority tilt to opinion and teaching. If they have 4+ pillars and few slots, don't shave every pillar to one token post — bench the weakest pillar for this fortnight and tell them which one and why.
5. **Distribute formats.** Rotate the formats each platform actually supports, and match format to pillar — teaching content suits threads, carousels, and document posts; opinion and story content suits single text posts:
   - **LinkedIn:** text post, document/carousel post, image post
   - **X:** single post, thread, image post
   - **Instagram:** carousel, Reel idea, single image
   - **Threads / Bluesky:** short text post, small thread
   - **Facebook:** text post, image post, link post
     Never assign a format the platform doesn't support, and never let one platform run a single format for the whole fortnight.
6. **Write a working title or hook for every slot.** Not a topic label — an actual first line the user could open with. "Why we killed our best feature" beats "product lessons". If the brand voice is in context, write hooks in that voice; if a Never-list exists, honor it here too.
7. **Reserve reactive slack.** Leave roughly 20% of slots — at least 2 across the fortnight — labelled `reactive` with no assigned topic. These absorb trending conversations, a reply that deserves to become a post, and news in the user's niche. Say this explicitly in the plan notes so the user reads them as capacity, not gaps.
8. **Sequence for energy, not neatness.** Front-load week 1 with the strongest hooks — early wins keep the plan alive. Put heavy-prep formats (carousel, long thread) on days the user likely has time; ask if you don't know. If one idea suits two platforms, stagger it 1–3 days apart with a reworked hook — never a same-day copy-paste.
9. **Do a final realism pass.** Before presenting, check the plan against every row of the Quality bar — volume, pillar spacing (including the ~40% cap), format mix, hooks, slack, anchors, and cross-posting stagger. Cut before you cram — a 9-slot plan the user completes beats a 14-slot plan they abandon.
10. **Offer, but don't produce unprompted, an .ics export.** If the user wants calendar entries, generate a `.ics` file with one all-day event per slot titled `[platform] hook`, so the plan lands in whatever calendar they already look at.

## Quality bar

| Check          | Constraint                                                                      |
| -------------- | ------------------------------------------------------------------------------- |
| Volume         | Matches stated cadence exactly — never exceeds it                               |
| Pillar spacing | No pillar twice in a row per platform; no pillar > ~40% of slots                |
| Format mix     | At least 2 distinct formats per platform across the fortnight                   |
| Hooks          | Every slot has a usable first line, not a topic label                           |
| Slack          | ~20% of slots marked `reactive`, minimum 2                                      |
| Anchors        | Every user-mentioned date has a slot; big ones get a warm-up and follow-through |
| Cross-posting  | Same idea on two platforms is staggered 1–3 days with a reworked hook           |

Every hook must pass the "would I stop scrolling?" test — specific, concrete, carrying a claim or tension:

| Fails                      | Passes                                                              |
| -------------------------- | ------------------------------------------------------------------- |
| "Thoughts on productivity" | "I tracked every meeting for 30 days. 11 hours were pure theater."  |
| "Our launch story"         | "We launched to 4 signups. Here's the email that turned it around." |
| "Tips for founders"        | "The advice that cost us six months: 'talk to more users.'"         |

## Deliverable

A markdown table with columns **Date | Platform | Pillar | Format | Working title / hook | Status**, every row's status set to `idea`. For example:

| Date       | Platform | Pillar          | Format    | Working title / hook                                  | Status |
| ---------- | -------- | --------------- | --------- | ----------------------------------------------------- | ------ |
| Mon Jul 20 | LinkedIn | Build-in-public | Text post | "We shipped the wrong feature first. On purpose."     | idea   |
| Tue Jul 21 | X        | Teaching        | Thread    | "7 pricing-page mistakes I keep seeing (with fixes):" | idea   |
| Wed Jul 22 | X        | —               | —         | reactive                                              | idea   |

Below the table, a short **Notes** section covering: the cadence you planned and why, which pillar (if any) was benched, and how to use the reactive slots. Offer the `.ics` export as an option. This is a plan for the user to execute themselves — hand it back and stop.
