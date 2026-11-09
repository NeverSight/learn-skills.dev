---
name: ig-content-planner
description: "Generate a weekly Instagram content plan from a theme, audience, and content pillars. Produces a per-day mix of Reels, carousels, single images, and stories, each with a hook formula, angle, posting time, and primary goal, plus a weekly saves-and-shares goal (the 2026 lever), a story cadence, and a balance check across saves, shares, comments, and follows. Use to plan a week instead of ad-hoc posting. Not for drafting one caption (use ig-caption-writer) or one carousel (use ig-carousel-planner)."
---

# Instagram Content Planner

Produce a weekly Instagram plan built around a pillar discipline and the
format mix Instagram rewards: Reels for reach, carousels for saves, stories for
the relationship. The plan sets a weekly saves-and-shares goal, because sends per
reach and saves are the 2026 levers.

## When to use

- User asks "plan my week on Instagram" or "what should I post this week"
- User wants to escape ad-hoc posting and establish a rhythm
- Before a launch week (the plan aligns a product pillar)

## Input

- **Theme** (optional): e.g. "launching our design course"
- **Audience description:** e.g. "junior designers, career switchers"
- **Pillar mix** (optional): defaults to 40% Educational / 30% Story /
  20% Engagement / 10% Promotion
- **Posting cadence** (optional): defaults to 4-5 feed posts/week + daily stories
- **Voice samples** (optional): past captions for voice calibration

## Output

A markdown plan with:

### 7-day calendar

| Day | Format | Pillar | Formula | 1-line angle | Goal | Time |
|---|---|---|---|---|---|---|
| Mon | Reel | Educational | IG9 Pattern-Interrupt | "you post Reels at the worst time" | shares | 12:00 PM |
| Tue | Carousel | Educational | IG5 Listicle | "7 portfolio mistakes" | saves | 11:30 AM |
| Wed | Story set | Engagement | poll + question | "which layout wins?" | comments | 7:00 PM |
| Thu | Carousel | Story | IG6 Before/After | "my first $0 to first $4k" | follows | 11:00 AM |
| Fri | Single image | Engagement | IG3 Relatable | "opening Canva for one graphic" | comments | 1:00 PM |
| Sat | Reel | Educational | IG10 How-I Teardown | "how I edit a Reel in 20 min" | saves | 10:00 AM |
| Sun | Story set | Promotion | reshare + link | "course doors open" | follows | 6:00 PM |

(The skill fills real angles from the theme. Stories run daily underneath the
feed posts.)

### Weekly saves goal

- Set a concrete **saves + shares target** for the week (the primary lever).
  Default heuristic: at least 3 of the week's feed posts are save-bait formats
  (IG1, IG5, IG6, IG8, IG10) and at least 2 are send-bait (IG2, IG7, IG9).
- Track saves and shares as the headline metric, not likes.

### Daily story cadence

- 2-4 story frames/day: behind-the-scenes, a poll or question sticker, and at
  least one reshare of a recent feed post (a send-equivalent signal that pushes
  the post to followers who missed it).
- Stories deepen the follower relationship; they do not chase non-follower reach.

### Weekly balance check

- [ ] Format mix: at least 2 Reels (reach), at least 2 carousels (saves), stories daily
- [ ] At least 3 save-bait posts and 2 send-bait posts
- [ ] At least 1 real first-person story post (build trust, earn follows)
- [ ] No pillar over 50% of the week's feed posts
- [ ] No formula repeated more than twice in the week
- [ ] Promotion pillar 1-2 posts max
- [ ] Goal mix spread across saves, shares, comments, follows

## Goal mix (balance the week)

Every formula earns a primary signal. A week that is all save-bait or all
relatable reads as engineered. Spread the goals:

| Goal | Formulas | Weekly target |
|---|---|---|
| Saves | IG1, IG5, IG6, IG8, IG10 | at least 3 (the headline lever) |
| Shares | IG2, IG7, IG9 | at least 2 |
| Comments | IG3, IG4 | at least 1 |
| Follows | IG4, IG6, IG8 | at least 1 |

## Rules

- **Consistency beats frequency.** 4-5 quality feed posts/week with daily stories
  beats a daily dump of filler. Do not pad to hit a count.
- **Reels for reach, carousels for saves, stories for the relationship.** Use the
  right surface for the job.
- **Reels can run more often** than carousels without fatigue, because each
  reaches a fresh non-follower audience.
- **Best windows:** weekdays 11 AM-1 PM and 7-9 PM local, plus Sunday evening.
  Check the user's own insights when available.
- **Promotion pillar max 1-2 posts/week.** Overuse buries reach.
- **One formula per slot, varied across the week.** Do not stack three IG5 carousels.

## Formula -> pillar mapping

| Pillar | Preferred formulas |
|---|---|
| Educational | IG5 Listicle, IG8 Framework, IG10 How-I Reel, IG1 Number-First |
| Story | IG4 Confession, IG6 Before/After |
| Engagement | IG3 Relatable, IG9 Pattern-Interrupt Reel, story stickers |
| Promotion | IG6 (results that imply the product), IG1 (your own data) |

## Steps

1. Gather inputs. Ask for theme, audience, pillar preferences if not provided.
2. Validate the pillar mix sums to 100%; warn if any pillar is over 50%.
3. For each day, pick: format (Reel/carousel/image/story), pillar, formula (do
   not over-repeat), angle, posting time (audience timezone), goal.
4. Set the weekly saves + shares goal and the daily story cadence.
5. Run the weekly balance check and the goal-mix check; flag anything missing.
6. Return as markdown, plus optional JSON for import.

## Example

See `references/example-week.md` for a filled-in 7-day plan.

## Files

- `SKILL.md` - this file
- `references/example-week.md` - worked 7-day plan
- `references/pillars-framework.md` - the Instagram pillar discipline explained

## Related skills

- `ig-caption-writer` - draft each single-image caption from the plan
- `ig-carousel-planner` - draft each carousel from the plan
- `ig-hashtag-strategist` - rotate sized hashtag sets across the week
- `ig-hook-extractor` - study competitors' posts while planning
