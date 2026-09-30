---
name: social-post
description: >
  Draft a single social post for one platform — LinkedIn, X (Twitter), Instagram,
  Facebook, Threads, Bluesky, or Mastodon — built for how that platform's feed
  actually reads: a hook that survives the fold, one idea, white-space rhythm, a
  specific call to action, and platform-correct links and hashtags. Use when the
  user says "write a post", "draft a LinkedIn post", "write an X post", "post this
  on Instagram", or asks for "a post about" something. Produces two hook variants
  and self-checks the draft against the user's voice rules. For the same message
  adapted across several platforms at once use social-crosspost; for a multi-post
  sequence use social-thread. Reads social-context.md for voice, audience, pillars,
  positioning, goals, and red lines so the post sounds like the user.
license: MIT
metadata:
  version: 0.1.0
  category: Create
  topics:
    - posts
    - writing
  examplePrompt: "Write a LinkedIn post about the lesson from our failed launch"
---

Write one platform-native post that sounds like the user and survives the feed: hook above
the fold, one idea, room to breathe, a CTA that asks for something specific.

## Context

Read `social-context.md` at the project root (also check `.agents/social-context.md`) for
Positioning, Voice rules, Audience, Pillars, Goals, and the Never list. If it's missing,
offer to run the `social-context` skill first, but don't block — ask three quick inline
questions (which platform, who's the audience, any hard nos) and proceed.

## Workflow

1. **Confirm the platform and load its rules.** One post targets one platform — ask which if
   the user didn't say. Load [references/platform-rules.md](references/platform-rules.md) for
   that platform's fold, length, link, hashtag, and formatting norms, and draft to them, not
   from memory. (For the same message across several platforms at once, use `social-crosspost`.)
2. Get the raw material immediately. Ask what the post is about if not stated; if the user
   gave a topic, dig for the _specific_: the number, the mistake, the exact moment, the line
   someone actually said. A post about "lessons from our launch" is dead; a post about "the
   day-3 metric that told us it was over" is alive. Don't draft until you have at least one
   concrete detail.
3. Pick the angle. Map the material to one of the user's Pillars and check it against the
   Never list. If the material could serve two audiences (peers vs. buyers), ask which one
   this post is for — the same story is told differently to each.
4. Ruthlessly cut to one idea. If the material contains two lessons, tell the user and ask
   which ships today (the other becomes a future post). A post that argues two things argues
   nothing.
5. Draft the hook first, in two different patterns. The hook is everything above the fold —
   the platform's visible-truncation point from the reference. Pick two contrasting patterns:
   - **Outcome-first:** the result, no context. "We deleted our pricing page. Trials went up 40%."
   - **Confession:** the mistake stated flat. "I spent $30k on a launch nobody noticed."
   - **Contrarian claim:** the belief they're wrong about. "Your case studies aren't building trust. They're screening you out."
   - **Specific scene:** drop into the moment. "Tuesday, 6:14am, our biggest customer's name in my inbox with the subject 'we need to talk'."
     Never open with throat-clearing ("I've been thinking a lot lately about…") and respect any Voice rule about openers.
6. Write the body for each hook, sized to the platform: one thought per paragraph, a line
   break every 1–2 sentences where the platform allows it. Structure = tension → turn →
   takeaway. The takeaway must be something the reader can _use_, not a moral ("be resilient"
   fails; "kill the launch if week-1 activation is under 20%" passes).
7. End with one specific CTA matched to the post's job and the user's primary goal (`## Goals`):
   - a pointed question that has a real answer ("What's your kill threshold?"), or
   - an offer ("I wrote up the full postmortem — comment 'launch' and I'll send it"), or
   - a plain follow reason.
     Never "Thoughts?" or "Agree?".
8. Place the link the platform's way (from the reference). Say why once when the platform
   penalizes body links; if the link belongs off-body, write the first-comment or bio
   version — one line of context plus the link.
9. Apply the platform's hashtag norm from the reference: always specific (`#devtools` not
   `#business`), never a hashtag soup.
10. Self-check both variants against every Voice rule in `social-context.md`, line by line.
    Fix violations; if a rule conflicts with a strong hook, keep the voice and note the
    tradeoff to the user.
11. Final pass — read each variant as it will render on the platform, then check both variants
    against every row of the Quality bar and the platform's rules in the reference. Fix any
    that fails. Count characters and show the hook and total counts.
12. Present both variants labeled by hook pattern, with hook char count and total char count
    for each, plus the first-comment/bio link text if any. Ask which variant to refine, and
    iterate on the winner.

## Quality bar

Per-platform limits (length, fold, links, hashtags, formatting) live in
[references/platform-rules.md](references/platform-rules.md) — check every draft against its
platform's row there, not against memory. For every post:

| Constraint     | Rule                                                                    |
| -------------- | ----------------------------------------------------------------------- |
| Hook           | Works standing alone, above the platform's fold                         |
| Ideas per post | Exactly one                                                             |
| Length         | Within the platform's limit; sweet spot well under it                   |
| Links          | Placed the platform's way; off-body text provided when needed           |
| Hashtags       | The platform's norm; specific, never a soup                             |
| CTA            | One, specific, answerable; no "Thoughts?"/"Agree?" engagement bait      |
| Formatting     | Renders clean on the platform (e.g. no markdown where it shows literal) |
| Voice          | Passes every rule in the Voice section of social-context.md             |

## Deliverable

Two ready-to-paste variants (labeled by hook pattern, with hook and total character counts),
the first-comment or bio link text if a link was involved, and a one-line note on which
variant you'd pick and why. End there.
