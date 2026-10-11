---
name: effective-comms
description: >-
  Router for the "effective comms" trigger. Decides whether a communication needs `/comms-prep`,
  `/comms-review`, or no gate yet, then performs that action.
---

# Effective Comms: pick the next action

Answer four questions, then take the first row that matches.

1. Is the substance ready to communicate, or is underlying work still producing it?
2. Is this a routine, low-stakes reply, one where a misunderstanding would be cheap to correct in
   the next exchange? Shortness alone does not make it one.
3. Is there a brief for this communication that still fits its objective and conversation?
4. Does a draft exist?

| State | Do |
|---|---|
| Underlying work is still producing the substance | Stay with that work. No gate is due yet. |
| Ready to write a one-line acknowledgement or direct yes/no answer | Write it. No gate is due. |
| A routine, low-stakes reply, whether or not a draft exists | Use the quick path in `/comms-prep`: answer its four questions, draft or check the draft, self-review, and deliver. |
| Ready to draft, and a fitting brief exists | Draft from the brief. If the brief calls for review, run `/comms-review` when the draft is complete. |
| Ready to draft, and no fitting brief exists | Run `/comms-prep`, draft from the brief, and follow its review decision. |
| A draft exists and no fitting brief exists | Run `/comms-prep` from the draft's intended purpose, then follow its review decision. |
| A draft and a fitting brief exist, and the brief calls for review | Run `/comms-review`. |
| A draft and a fitting brief exist, and the brief does not call for review | Deliver the draft. |

The two gate skills carry every rule. This router adds none and holds no state: once you invoke a
gate, it runs to completion on its own terms.
