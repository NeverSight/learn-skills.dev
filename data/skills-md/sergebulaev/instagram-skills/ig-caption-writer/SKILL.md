---
name: ig-caption-writer
description: "Draft an Instagram caption with the hook in the first 125 characters, a skimmable body, and one clear CTA, using a 2026 hook formula chosen by goal (saves, shares, comments, follows). Runs the humanizer pass and, on approval, publishes with the image or video you supply via the Publora media flow. Use to caption a single image or a Reel. Not for slide-by-slide carousels (use ig-carousel-planner) or auditing a draft (use ig-humanizer --mode audit)."
---

# Instagram Caption Writer

Write a caption that earns the tap and the save. Instagram hides everything after
~125 characters behind "more", so the hook does the entire job in the first
line. This skill front-loads that hook, keeps the body skimmable, and lands one
clear call to action.

## When to use

- User says "write me an Instagram caption about X"
- User has a single image or a Reel and needs the caption around it
- User wants a sharper hook for a draft they already have
- User wants a caption that auto-publishes with their media on approval

## Formulas this skill uses (caption-first shapes)

| Code | Formula | Primary goal | Best for |
|---|---|---|---|
| IG1 | Number-First Result | saves | one odd-precision result + a "steal this" promise |
| IG2 | Contrarian Truth | shares | a sharp, defensible against-the-grain claim |
| IG3 | Relatable Cold-Open | comments | a specific shared moment, no setup |
| IG4 | Mini-Story Confession | comments, follows | a real first-person story with a cost |

Full skeletons in `../../references/hook-formulas.md`. For carousels (IG5-IG8) use
`ig-carousel-planner`; for Reels (IG9-IG10) the hook lives in the video, and this
skill writes the supporting caption.

### Pick by goal first

| Goal | Reach for |
|---|---|
| Saves | IG1 |
| Shares | IG2 |
| Comments | IG3, IG4 |
| Follows | IG4 |

## Steps

**Voice profile first (all drafts).** If `../../references/voice-profile.md` has `filled: yes`, load it and match the user's voice fingerprint, hard rules, and CTA/link style throughout. If it is not filled, mention once that `ig-humanizer --mode profile` can learn their voice from a few posts, then proceed with the generic voice rules.

**Never invent the specifics.** The rules below ask for a concrete number, a date and a named entity, because that is what separates a real post from a generated one. Take them from what the user actually said in this conversation. **Do not invent a figure, a date, a client name or a result, and do not soften a vague claim into a plausible-looking number.** If the user has nothing concrete for a beat, ask them once, and if they still have nothing, drop the claim rather than decorate it. A published invented number is a retraction; a missing one is only a weaker post.

1. **Gather inputs.** Topic, angle, the media (single image or Reel), target
   audience, and the goal (saves / shares / comments / follows).
2. **Pick the formula.** Use the goal table to shortlist, then suggest 2-3 that
   also fit the topic and let the user choose.
3. **Write the hook (first 125 chars).** It must land the payoff, tension, or
   number before the "more" fold and make sense on its own.
4. **Write the body.** Short lines, white space between beats, one idea. Teach or
   tell the story that the hook promised. Keep it under 2,200 chars.
5. **Write one CTA.** A specific save or send prompt ("save this for your next
   launch", "send to the friend who keeps doing #2"), a real question, or a
   single next step. Never "what do you think?".
6. **Add hashtags.** Hand off the topic to `ig-hashtag-strategist` or apply the
   3-5 sized set yourself (see `../../references/hashtag-strategy.md`). Put them at
   the end or note they go in the first comment.
7. **Humanizer pass.** Scrub 2026 AI vocab by paragraph density, cap em
   dashes (about one per 100 words; a caption's single dash is not a tell,
   never swap one for a period), break stacked triads, generic openers and
   reveal bridges. Fix only a paragraph that reads machine-flat; never
   manufacture variance or one-word lines for drama. Add an odd-precision
   number with a named referent or a named entity where the claim allows.
   Canonical rules: `ig-humanizer` V3.
8. **Optional audit.** Invoke `ig-humanizer --mode audit` for a pass-fail check.
9. **Approval card.** Show: formula used, the hook (flag if over 125 chars),
   full caption, char count, hashtag set, primary goal, and the media the user
   must supply.
10. **On approval, publish with media.** Call `lib.publish(kind="post",
    draft_text=<approved caption>, target_url="https://www.instagram.com/",
    media=[<local file paths>], platforms=[<INSTAGRAM_PLATFORM_ID>],
    scheduled_time=<iso_or_None>)`. For a Reel pass `kind="reel"`. The wrapper
    runs the Publora draft then upload then schedule flow. With no media or no
    Publora key it returns a copy-paste block and a reminder to attach the media.

## Hard rules

Global voice rules: see root `SKILL.md` Voice rules. Additional skill-specific
rules:

- The first 125 characters must stop the scroll on their own. Rewrite any hook
  that needs the second line to make sense.
- One idea per caption. Two ideas means two posts.
- One specific number where the claim allows it.
- 3-5 sized hashtags, never 30. 0-3 emoji, placed with intent.
- Media is required. Never present a caption as publishable without reminding
  the user to attach the image or video.
- Do not hard-sell. One natural mention of the next step, max.

## Anti-patterns (skill will refuse)

- A hook that only makes sense after the fold.
- Em dashes above the cap (more than about one per 100 words), or an em dash swapped for a period.
- "Let's talk about.." or "Here's the thing.." openers; "The result?" as a reveal.
- Announced candor ("real talk", "not gonna lie", "POV:" on something that is not a POV) with no dated fact behind it.
- Staccato stacks ("No X. No Y. Just Z.") and one-word lines added for drama.
- 20-30 hashtags stuffed at the top.
- Engagement bait ("double tap if you agree", "comment YES").
- Rule-of-three lists without specifics.
- "leverage", "fundamentally", "game-changer", "level up", "dive in".
- Padding a one-line idea to look substantial.

## Resources

- `../../references/hook-formulas.md` - all 10 Instagram formulas (IG1-IG4 are caption-first)
- `../../references/algorithm-heuristics.md` - 2026 Instagram ranking rules
- `../../references/hashtag-strategy.md` - the 3-5 sized hashtag recipe
- `../../references/media-workflow.md` - the draft, upload, schedule flow
- `references/caption-checklist.md` - the per-caption scrub and fit list

## Related skills

- `ig-carousel-planner` - when the idea is a slide-by-slide carousel
- `ig-hashtag-strategist` - build the sized hashtag set
- `ig-humanizer` - AI-tell scrubber, plus `--mode audit` for review
- `ig-hook-extractor` - reverse-engineer a hook from a post you admire
