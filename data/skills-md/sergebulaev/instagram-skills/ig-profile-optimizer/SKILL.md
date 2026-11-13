---
name: ig-profile-optimizer
description: "Audit and rewrite an Instagram profile end-to-end for 2026: profile photo, searchable NAME field weighted with a keyword, @handle, bio (150 chars: value plus topic plus proof), goal-matched link, category label, story highlights, the first-9 grid, and up to 3 pinned posts. Triggers on \"review my Instagram profile\", \"fix my bio\", \"optimize highlights\", \"profile audit\". The whole follow decision happens on the profile header. Not for writing captions (use ig-caption-writer)."
---

# Instagram Profile Optimizer

Audit the nine parts of an Instagram profile (photo, NAME field, @handle, bio,
link, category label, highlights, the first-9 grid, pinned posts) against what
actually converts a profile-visitor into a follower in 2026, then rewrite each
part that needs it. On Instagram the whole follow decision happens on the
profile header plus the first two or three grid rows: photo, NAME, bio, link,
then the grid at a glance. That is what this fixes.

## When to use

- User pastes their Instagram profile or @handle and asks for an audit
- "Fix my bio", "rewrite my Instagram bio", "what should my highlights be"
- User is starting to post seriously and wants the profile to match the content
- Any of: "review my Instagram profile", "optimize highlights", "profile audit"

Not for writing captions (use `ig-caption-writer`) or planning a carousel
(use `ig-carousel-planner`).

## Input

- Profile URL / @handle (or a screenshot of the profile header + first grid rows)
- Goal: **grow a following** / **sell a product** / **land clients** / **build authority**. The bio CTA, the link target, and the pinned posts change by goal
- Optional: their best-performing posts, to pick the pins and the grid order

## Output

1. **Scorecard** (9 parts, pass / needs-work / fail)
2. **Priority fixes** ranked by impact (NAME field, bio, and pins first)
3. **Before -> After** rewrites for each failing part
4. **Highlights plan** (covers, order, naming) and **grid + pin picks** with reasons

## Steps

1. **Intake.** Collect the profile state + goal. Note the account type
   (personal / creator / business), since business and creator unlock the
   category label and the professional dashboard.
2. **Score the 9 parts** against the scorecard below.
3. **Weight the NAME field with a keyword.** The NAME field (not the @handle) is
   what Instagram search indexes. Set it to `Real Name + the topic people type`
   (e.g. "Sam Rivera | Instagram Growth"), inside 30 chars. This is the single
   highest-leverage SEO fix on the profile.
4. **Rewrite the bio (150 chars).** Formula: `who you help + what you post about
   + one proof or specific`. Lead with the value, not the job title. No "I help X
   do Y" cliche opener unless the rest is specific. Line breaks and one anchor
   emoji are fine; an emoji storm is not. Fit inside 150.
5. **Set the link.** One link matched to the goal (offer / newsletter / booking).
   If they need several, a single link-hub, not a bare homepage. Business and
   creator accounts can now add multiple links, but the top one still carries the
   click.
6. **Set the category label** (business / creator accounts). One clear label that
   matches the niche, shown under the NAME. It reinforces the bio; it does not
   repeat it.
7. **Plan the highlights.** 4-6 highlights, ordered left to right by the visitor's
   next question: Start Here / Proof / Offer / FAQ / About. Custom covers in one
   consistent style, short one-word names that fit without truncating. The first
   3-4 are what a new visitor sees before scrolling.
8. **Fix the first-9 grid.** The top nine tiles are the shop window. Aim for
   readable at a glance, a consistent look (color, framing, or text style), and a
   mix that shows range without chaos. Reorder or replace weak top tiles; the
   grid is judged as a set, not tile by tile.
9. **Pick the pinned posts (up to 3).** The three best proofs of what a new
   follower will get, matched to the goal: a top performer, a clear offer, and an
   intro/who-this-is-for post. Pins override the grid order, so use them.
10. **Photo check.** Clear face, fills the frame, recent, high contrast against a
    plain background. It renders small, so detail is wasted; contrast is not.
11. **Deliver the before/after diff** + the header test: read only photo, NAME,
    bio, link, and the first grid row, and ask "would a stranger follow from this
    alone?"

## Nine-part scorecard

| # | Part | Pass criteria (2026) |
|---|------|----------------------|
| 1 | **Profile photo** | Clear face filling the frame, recent, high contrast, plain background, reads at small size |
| 2 | **NAME field** | Real name + a searchable keyword people type, inside 30 chars (this is the indexed field, not the @handle) |
| 3 | **@handle** | Short, memorable, matches the brand, no numbers/underscores if avoidable |
| 4 | **Bio** | Value + topic + proof inside 150 chars; no cliche opener; leads with what a follower gets; no emoji storm |
| 5 | **Link** | One, goal-matched; a link-hub if several are needed; top link carries the click |
| 6 | **Category label** | Set (business/creator), one clear niche label that reinforces the bio |
| 7 | **Highlights** | 4-6, ordered by the visitor's next question, consistent custom covers, short names that do not truncate |
| 8 | **First-9 grid** | Consistent look, readable at a glance, shows range; weak top tiles reordered or replaced |
| 9 | **Pinned posts** | Up to 3 present, each a best proof matched to the goal (not random recent posts) |

## Hard rules

Global voice rules: see root `SKILL.md` Voice rules. Additional skill-specific
rules:

- The header must pass the header test: a stranger reading only photo + NAME +
  bio + link + first grid row should know who this is for and want to follow.
- Lead the bio with the reader's benefit, not the user's job title.
- The NAME field always carries a searchable keyword; never leave it as bare name.
- Keep every rewrite inside the platform limits (bio 150, NAME 30). Never ship a
  truncated bio or a highlight name that cuts off.
- Highlights and grid are judged as sets; fix order and consistency, not just
  single items.
- At most one em dash in the bio (a 150-char bio rarely needs one). No "leverage", "fundamentally", "game-changer", "elevate".

## Related skills

- `ig-caption-writer` - write the captions the optimized profile and grid will host
- `ig-hook-extractor` - find a pin-worthy hook in a post that already worked
- `ig-content-planner` - plan the cadence that fills the grid and highlights
- `ig-humanizer --mode audit` - audit the bio and pinned captions before shipping
