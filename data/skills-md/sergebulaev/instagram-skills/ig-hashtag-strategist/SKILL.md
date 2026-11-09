---
name: ig-hashtag-strategist
description: "Build a sized Instagram hashtag set for a post using the 2026 reality that 3 to 5 well-chosen tags beat 30 random ones. Sizes each tag as niche (under 50k posts), mid (50k to 500k), or broad (500k+), then assembles a 2-3 niche, 1-2 mid, 0-1 broad mix that a small or mid account can actually rank in, matched to the post content and rotated to avoid spam patterns. Use to choose hashtags for a caption, carousel, or Reel. Not for writing the caption itself (use ig-caption-writer)."
---

# Instagram Hashtag Strategist

Pick 3-5 hashtags that actually help, sized so the post can rank. The 30-tag wall
is dead: in 2026 hashtags work as topic labels, and a small account ranks in
niche tags, not in million-post broad ones. This skill builds the sized set.

## When to use

- User has a caption, carousel, or Reel and needs hashtags
- User is still posting 20-30 generic tags and wants the 2026 approach
- User wants tags sized to where their account can actually rank

## The model: size, not volume

A tag's **size** is its total post count. The strategy is a mix so the post
ranks in the small tags while touching the bigger ones.

| Tier | Post count | Role | Use |
|---|---|---|---|
| Niche | under 50k | where a small/mid account can actually rank for hours | 2-3 |
| Mid | 50k - 500k | enough audience, beatable competition | 1-2 |
| Broad | 500k+ | a brief category-label touch, ranks for minutes | 0-1 |

**Default: 3-5 total.** Full reasoning in `../../references/hashtag-strategy.md`.

## Steps

1. **Get the post.** The caption, carousel topic, or Reel subject, plus the
   target audience and the account's rough size (so the niche/mid split fits).
2. **Extract topics.** Pull the 3-5 real topics the post is about (the subject,
   the niche community, the format, the outcome).
3. **Generate candidates per tier.** For each topic, propose niche, mid, and
   broad candidates. Niche tags are specific and long-tail
   (`#notionforfreelancers`); broad tags are single common words (`#marketing`).
4. **Size each candidate.** Estimate the tier from specificity (the API does not
   expose counts, so use judgment and tell the user to verify counts in the app's
   search). Flag any obviously generic or flag-prone tags
   (`#follow4follow`, `#like4like`) to drop.
5. **Assemble the set.** 2-3 niche + 1-2 mid + 0-1 broad, total 3-5. Drop the
   broad slot if nothing genuinely fits. Every tag must match the content.
6. **Check the match.** Reject any tag that is popular but off-topic; a mismatch
   mistrains the recommendation engine and lowers reach.
7. **Rotate.** Tell the user to vary the set per topic, not reuse one block on
   every post (identical sets across many posts read as automation).
8. **Output.** The 3-5 set, each tagged with its tier and a one-line why, plus
   placement guidance (end of caption or first comment).

## Output format

```
Sized set (4 tags):
  #notionforfreelancers   niche   the exact community this post serves
  #freelanceworkflow      niche   long-tail, low churn, rankable
  #productivitytips       mid     warm relevant audience, beatable
  #notion                 broad   category label, one touch

Placement: end of the caption or the first comment. Rotate the niche tags per topic.
```

## Hard rules

Global voice rules: see root `SKILL.md` Voice rules. Additional skill-specific
rules:

- 3-5 tags total. Never output a 30-tag block.
- Every tag must describe the actual content. No popular-but-off-topic tags.
- At most one broad tag; drop it if nothing fits.
- Flag and remove engagement-farm tags (`#follow4follow`, `#like4like`) and any
  known flagged tags.
- Hashtags go at the end of the caption or in the first comment, never
  mid-sentence.
- Rotate sets per topic; do not hand the user one block to paste forever.

## Anti-patterns (skill will refuse)

- Outputting 20-30 hashtags.
- A "viral hashtag pack" of generic broad tags.
- Tags that do not match the post to chase a bigger audience.
- Hiding 30 tags behind dots to "look clean".
- All-broad sets a small account cannot rank in.

## Resources

- `../../references/hashtag-strategy.md` - the full 2026 sizing model and recipe
- `../../references/algorithm-heuristics.md` - why sends and saves, not hashtag feeds, drive reach

## Related skills

- `ig-caption-writer` - writes the caption the hashtags attach to
- `ig-carousel-planner` - the carousel whose caption carries the set
- `ig-content-planner` - rotate tag themes across a week
