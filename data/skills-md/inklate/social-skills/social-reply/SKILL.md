---
name: social-reply
description: >
  Triage a pasted batch of comments, mentions, and DMs from LinkedIn, X,
  Instagram, Facebook, or Threads, and draft on-voice replies where they're
  warranted. Use when the user says "help me reply", asks you to "draft
  responses to these comments", says "triage my mentions", or asks you to
  "answer these DMs". Each item gets bucketed as question, praise, objection,
  lead signal, or troll/spam, assigned a recommended action — reply,
  react-only, DM, or ignore — and, where a reply is warranted, a draft written
  in the user's voice. It reads social-context.md for brand voice, product
  facts, and escalation boundaries so replies sound like the user and never
  invent answers. Lead signals get flagged prominently with a suggested next
  step; legally or PR-sensitive items get escalated with a reason, not
  drafted.
license: MIT
metadata:
  version: 0.1.0
  category: Create
  topics:
    - engagement
    - writing
  examplePrompt: "Triage these 14 comments from my launch post and draft replies"
---

Turn a raw batch of comments, mentions, and DMs into a triaged worklist with on-voice reply drafts — leads flagged first, trolls dismissed with reasons.

## Context

Read `social-context.md` at the project root (also check `.agents/social-context.md`) for the `## Voice` rules and the `## Never` list — replies must sound like the user and stay inside the red lines. Product facts (pricing, roadmap, what you may confirm) and who handles escalations are not in that file, so ask for them directly the first time they matter. If `social-context.md` is missing, offer to run the `social-context` skill first, but don't block — ask 2–3 quick inline questions and proceed:

- How formal is your reply voice — emoji or none, first names or handles?
- Anything you must never promise or confirm (roadmap dates, discounts, integrations)?
- Who handles escalations (legal, refunds, press), and what's your next step for a warm lead — call link, DM, trial invite?

## Workflow

1. **Parse the batch.** Number every item. Preserve the author handle, platform, and channel (public comment vs DM) where given — the same words deserve a different reply in public than in private. If items are ambiguous or truncated, note it on the item rather than guessing intent.
2. **Bucket each item** into exactly one of:
   - **question** — wants information;
   - **praise** — positive, no ask;
   - **objection** — pushback, skepticism, competitor comparison, complaint;
   - **lead signal** — buying intent: "is there a trial?", "does it work for teams?", pricing questions, "how do I get started", asking to be contacted;
   - **troll/spam** — bad faith, off-topic promotion, bait.
     Intent outranks form: a pricing question is a lead signal, not a question; a complaint from a paying customer is an objection, not a troll, no matter the tone.
3. **Order the worklist by priority:** leads first, then questions, then objections, then praise; trolls/spam last. Within leads, order by strength of intent — "where do I sign up" beats "interesting, might look at this".
4. **Assign an action per item:**
   - `reply` — a public answer adds value for onlookers too; default for questions, objections, and leads.
   - `react-only` — a like/heart is enough; default for short praise, where a written "Thank you so much!!" adds nothing.
   - `DM` — move to private: anything needing account details, pricing negotiation, or a lead worth a direct conversation. Still reply publicly first with one line ("Answered you in DMs — short version: yes") so onlookers see responsiveness.
   - `ignore` — trolls/spam, always with a one-line why addressed to the user, e.g. "engagement bait; replying boosts the thread's ranking, not yours".
5. **Draft replies where warranted.** In the user's voice: short, human, specific to what the person actually said. The first line responds to _their_ words, not a template. Banned: corporate padding ("Thanks for reaching out!", "Great question!"), exclamation-mark inflation, restating their question back at them, and signing off like an email. Public replies ≤ 2–3 sentences; DMs may run slightly longer and must end with one clear next step.
6. **Handle objections with substance.** Concede what's true, correct what's false with a fact from context, never argue tone. If the objection is valid and context has no counter-fact, the honest reply is "fair — here's what we're doing about it", or a flag to the user that they must supply the answer. Never invent capabilities, dates, or policies to win a thread.
7. **Flag every lead prominently.** Mark it `LEAD` at the top of the worklist with three parts:
   - the intent evidence — quote their exact words;
   - the suggested next step from context — send the call link, offer the trial, move to DM;
   - a reply draft that executes the step without being pushy: answer their actual question first, invite second.
8. **Escalate, don't draft, the dangerous ones.** Legal threats, refund/chargeback disputes, safety or harassment reports, press/journalist inquiries, anything touching an individual's private data, and public accusations that could become a PR moment. Mark `ESCALATE`, give the one-line why, name who should handle it (from what the user told you; ask if you don't know), and draft at most a holding line ("Taking this seriously — following up with you directly") for cases where public silence would look worse than acknowledgment.
9. **Sanity-pass the drafts as a set.** Read all the replies together. If ten of them open with the same word or lean on the same phrase, vary them — people read whole comment sections, and copy-paste warmth reads as neither warm nor human. Check the set against every voice rule and the Never list, and against every row of the Quality bar — the default action, reply length, and opener for each bucket, plus the hard rules.

## Quality bar

| Bucket      | Default action                   | Reply length         | Draft opens with                        |
| ----------- | -------------------------------- | -------------------- | --------------------------------------- |
| Lead signal | Reply, then DM next step         | ≤ 3 sentences public | Their actual question, answered         |
| Question    | Reply                            | ≤ 3 sentences        | The answer itself, not a preamble       |
| Objection   | Reply                            | ≤ 3 sentences        | The concession or the correcting fact   |
| Praise      | React-only; reply if substantive | 1 sentence           | Something specific from their comment   |
| Troll/spam  | Ignore                           | —                    | — (one-line why, addressed to the user) |

Hard rules:

- Never invent product facts, prices, or capabilities — if context doesn't have the answer, say so and ask the user.
- Never promise timelines or roadmap items that aren't in context.
- Never draft full replies for `ESCALATE` items — a holding line at most, and only when silence would look worse.
- Every `ignore` and every `ESCALATE` carries its one-line reason; unexplained skips erode the user's trust in the triage.
- No two adjacent drafts open with the same word; the set must read as a person, not a macro.
- Tone-match the item: a joke gets a light reply, a frustrated customer gets a straight one — the voice rules set the range, the item picks the point.

## Deliverable

A prioritized worklist: each item numbered with author/platform, bucket, action, and — where warranted — the reply draft ready to paste, with `LEAD` and `ESCALATE` items visually prominent at the top of their sections. Each entry reads like:

> **LEAD — #7, @mariab (X, public comment)** — "does this work for agencies managing 10 clients?"
> Action: reply, then DM. Next step: send the team-plan trial link.
> Draft: "It does — multi-client is the main reason agencies pick us. DMing you a trial link so you can test it on a real client."

Close with a two-line batch summary: counts per bucket, and the number of leads worth same-day follow-up. The user reviews, edits, and posts the replies themselves — hand the worklist back and stop.
