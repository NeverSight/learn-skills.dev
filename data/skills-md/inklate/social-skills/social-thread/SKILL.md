---
name: social-thread
description: >
  Build a multi-post sequence with real architecture — an X (Twitter) thread or a
  LinkedIn multi-post — instead of a chopped-up blog: a hook post that earns the read,
  one idea per post, an escalation-and-payoff structure, and a closing CTA post, every
  post budgeted to the platform's limit with the count shown. The hook is drafted three
  ways and scored before anything else is written, because post one decides whether the
  rest gets read. Use when the user says "write a thread", wants a "tweetstorm", says
  "turn this into a thread", or asks for an "X thread about" a topic. Reads
  social-context.md for voice, audience, positioning, goals, and red lines. For one
  standalone post use social-post; for the same message across platforms at once use
  social-crosspost.
license: MIT
metadata:
  version: 0.1.0
  category: Create
  topics:
    - threads
    - writing
    - hooks
  examplePrompt: "Turn this blog post into an X thread with a strong hook"
---

Write a sequence where the hook earns the read, every post carries exactly one idea, and the
last post knows what it's asking for.

## Context

Read `social-context.md` at the project root (also check `.agents/social-context.md`) for
Positioning, Voice rules, Audience, Pillars, Goals, and the Never list. If missing, offer to
run the `social-context` skill first, but don't block — ask two inline questions (which
platform — X thread or LinkedIn multi-post — and how spicy: measured/direct/provocative) and
proceed.

## Workflow

1. **Confirm the platform and load its rules.** X thread or LinkedIn multi-post? Load
   [references/platform-rules.md](references/platform-rules.md) for that platform's per-post
   limit, hook budget, sequence length, and link/hashtag norms, and budget to them, not memory.
2. Get the source material now: a blog post, notes, a story, or just a topic. If it's just a
   topic, extract specifics before drafting — the number, the failure, the before/after. A
   sequence runs on receipts, not opinions.
3. Pin the thesis in one sentence: what should a reader believe or do after the last post
   that they didn't before the first? If the material supports two theses, ask which one this
   argues. No thesis, no thread — write a single post instead and say so.
4. Outline the beats before writing any post — one per post, within the platform's post-count
   range from the reference, in an escalation shape:
   - hook
   - stakes/context (1 post max)
   - the meat, in rising order — save the second-best point for late, the best for the payoff
   - payoff
   - CTA
     Kill any beat that restates another. Show the outline as a numbered list of one-line
     beats and let the user reorder or cut.
5. Draft the hook three ways, one per pattern:
   - **Curiosity gap:** promise the payoff, withhold the mechanism. "We doubled activation with one email. It's not the one you think."
   - **Bold claim:** the thesis at full strength, no hedge. "Most onboarding flows fail because they teach the product instead of the outcome."
   - **Specific number:** the receipt up front. "47 user interviews. 3 patterns. Here's what actually makes people churn."
6. Score each hook 1–5 on three axes: stops the scroll, makes the specific promise the
   sequence actually keeps, and passes the Voice rules. Show the scores, recommend one, and
   ask the user to pick. A hook that overpromises is worse than a boring one — the sequence
   gets ratioed for the gap.
7. Write the posts from the outline. Per post: lead with the point in the first line, one
   idea only, cut every "and another thing" into its own post or the bin. Prefer line breaks
   over commas — a few short lines read better than one dense paragraph. No post should need
   its neighbor to make sense.
8. Budget characters as you go against the platform's per-post limit from the reference, and
   show the count after each like `(chars/limit)`. Keep the hook under the reference's hook
   budget to leave room. If a post lands over, cut words — never split one idea across two
   posts to make it fit.
9. Write the closer as a real CTA post: restate the payoff in one line, then one ask —
   follow, with the reason; or the link (the only post a link may appear in); or a reply
   prompt with a real question. One ask, not three.
10. Ask the numbering question: numbered (`1/`) prefix or clean posts with no numbering?
    Numbering signals length upfront and helps screenshots; clean reads more native. Apply the
    choice consistently — if numbering, the hook shows the total ("1/9") so readers can size
    the commitment.
11. Whitespace and rhythm pass: vary post lengths, check each post stands alone as a
    screenshot, verify hashtags follow the reference (none mid-sequence). Run every post
    against the Voice rules. Then check every post, and the sequence as a whole, against every
    row of the Quality bar and the platform's rules; fix any failing row before presenting.
12. Present the full sequence with per-post counts, plus the two unused hooks labeled as
    alternates in case the user wants to swap.

## Quality bar

Per-platform limits (per-post length, hook budget, sequence length, links, hashtags) live in
[references/platform-rules.md](references/platform-rules.md) — check every post against its
platform's row there, not memory. For every sequence:

| Constraint | Rule                                                                                   |
| ---------- | -------------------------------------------------------------------------------------- |
| Hook       | Within the platform's hook budget; promise matches what the sequence delivers          |
| Every post | Within the per-post limit, count shown; exactly one idea; stands alone as a screenshot |
| Length     | Within the platform's post-count range; context/setup gets at most 1 post              |
| Links      | Final post only — a mid-sequence link is where readers exit                            |
| Hashtags   | Per the reference; none mid-sequence                                                   |
| Structure  | Escalates — strongest material in the back half, payoff before CTA                     |
| CTA        | Exactly one ask in the closing post                                                    |
| Voice      | Every post passes the Voice rules in social-context.md                                 |
| Numbering  | User's chosen convention applied to every post, or to none                             |

## Deliverable

The full sequence, ready to paste: each post in its own block with its character count,
numbering per the user's choice, the chosen hook first and the two alternate hooks appended
for reference. End there.
