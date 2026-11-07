---
name: follow-up-email-writer
description: "Use this skill when you need to follow up after no reply, after a meeting, after a proposal or after a prospect went quiet: \"write a follow-up email\", \"they ghosted me\", \"follow up after the demo\". Diagnoses the situation, picks the right follow-up type (add value, new angle, recap, nudge on a decision, re-engage), and writes a short follow-up that gives the reader a reason to respond without guilt-tripping or saying \"just checking in\"."
license: MIT
metadata:
  title: Follow-up email writer
  category: cold-email
  tags: "SDR, Sales, Founders"
  author: prosyo
  version: "1.0.0"
  keywords: "follow up email after no response, sales follow up email, follow up after demo, claude follow up skill, ghosted prospect email"
  inputs: "Previous emails or meeting notes, Stage of the conversation, Time since last contact"
  outputs: "Diagnosis, Follow-up email, Next step if no reply"
---

Use this whenever the next email is a follow-up. It produces a follow-up that adds something new, because "just checking in" gives the reader nothing to respond to.

## Inputs

- The thread so far, or the meeting notes.
- Stage: cold (no reply yet), post-meeting, post-proposal, gone quiet mid-deal.
- How long it has been and any known deadlines.

## The play

### 1. Diagnose
| Situation | Likely reason for silence | Follow-up type |
| --- | --- | --- |
| Cold, no reply | Not relevant enough, or bad timing | New angle or value add |
| After a first meeting | Busy; next step was vague | Recap with a clear next step |
| After a demo or proposal | Internal discussion, competing priorities, objection not voiced | Decision nudge with an easy answer |
| Quiet for 3+ weeks mid-deal | Priority dropped or a blocker appeared | Honest re-engage, permission to close |
| After an event or call | Momentum fading | Deliver what was promised |

### 2. Add something
Every follow-up carries one new thing: an insight, a short customer story, an answer to a question they had, a resource, a relevant change. If there is nothing new, the follow-up should be a short, honest question instead.

### 3. Make replying easy
End with a question that can be answered in one line or one word. Multiple-choice questions work well mid-deal: "Is this (a) still a priority, (b) on hold until Q3, or (c) solved another way?"

### 4. Keep it short
Cold follow-ups: 25-70 words. Post-meeting recaps: as long as the next steps need, in bullets.

## Examples

**Post-meeting recap**

> Hi Tom, thanks for the time today. What I heard: close takes 9 days, approvals are the bottleneck, and you want options before the budget review on the 14th.
>
> Next steps: I send the Contoso checklist today; you loop in Priya; we meet Thursday at 10 to review it together. Does that still work?

**Gone quiet mid-deal**

> Hi Tom, it has been a few weeks since the proposal, so I suspect priorities have shifted. Is it (a) still on for this quarter, (b) paused until later, or (c) solved another way? Any answer helps me stop guessing.

## What good looks like

- The reader learns something or gets something in every follow-up.
- Post-meeting emails go out the same day.
- The common mistake is "just bumping this", "circling back" or "did you get a chance to look", which signal you have nothing to add.

## Rules

- MUST add one new piece of value or one clear, easy question.
- MUST reference the actual previous conversation accurately.
- NEVER guilt-trip ("I've tried to reach you several times").
- NEVER fake urgency or deadlines that do not exist.

## Example prompts

- "They went quiet after the proposal two weeks ago. Write the follow-up."
- "Write a recap email after today's discovery call. Notes below."
- "Follow up on my cold email from last week with a new angle."
