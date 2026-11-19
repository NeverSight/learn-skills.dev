---
name: ux-ai-interaction
description: Design how people give an AI feature context, follow a generation, and keep or revise its output. Use for inline suggestions, conversation, model choice, streaming, cancellation, and retries.
license: MIT
---

# Design the exchange around the user's work

Name the thing the person wants to leave with. A suggested subject line can live beside the field where it will be used. Reconciling several documents may need a conversation that preserves earlier decisions. If the outcome follows a fixed rule, consider whether a direct control already does the job.

Take an example through three separate objects: the editable draft, one submitted attempt, and the result the person chooses to use. Give each a clear owner. In a writing tool, for instance, a delayed suggestion belongs to the selected passage as it existed when the request was sent. If the writer has since edited that passage, offer a preview before applying anything.

In a conversation, identify who produced each message and keep failures, tool activity, and generated text distinguishable. Preserve the turn order when reopening a conversation. Make editing an earlier turn explicit about which later answers will remain part of the active history.

**Make the request inspectable.** Show which text, files, and earlier turns will be included. Let users remove an attachment without clearing their draft. Expose a model choice when its consequences matter to this job, and explain a meaningful difference such as supported inputs or response time. If a switch makes an attachment unusable, keep it visible and let the user decide whether to remove it or choose a compatible model. At a context limit, say what counts toward the budget, label estimates, and disclose any omitted or summarized history. Offer an edit that will let the request fit.

Show current token usage against the selected model's usable limit, including included history and attachments, and allow room for the requested answer. Recalculate when context or model changes and warn early enough for the user to adjust. Label any estimated cost separately from actual usage, with the assumptions that affect it.

Keep the active model visible and explain unavailable choices. If a fallback changes which model produced the answer, identify that change. Let the person inspect any consequential context reduction before the next request.

**Keep editing and sending separate.** Accepting an inline completion should be deliberate and reversible. Provide a visible send action for a composer that accepts several lines. Check paste, line breaks, and the Enter key during input-method composition. A rejected submission should reopen with the draft and eligible attachments available for correction.

Offer suggestions on demand when unsolicited completions would interrupt the task. Make keyboard acceptance and dismissal discoverable, preserve ordinary editing keys, and let someone dismiss a suggestion and keep typing.

**Bind updates to the attempt.** From the first acknowledgment to the final event, each update must identify the request it belongs to. While waiting, communicate only progress the system can actually observe. As text arrives, let the reader scroll away, select text, and return to the newest portion. Keep announcements useful at reading speed; a token-by-token live region can make the screen unusable.

Try this sequence with a controllable stream:

1. Send request A. Delay its first output, deliver half a sentence, then press Stop. Mark the visible fragment as interrupted and keep it readable.
2. Start request B. Deliver a delayed fragment and a completion event for A. Neither event should extend A, modify B, or turn off B's busy indicator.
3. Finish B. Confirm that copying, applying, or rating B acts on that exact version. If the user regenerates, keep enough identity to distinguish the alternatives.

**Give each failure a way forward.** For an oversized request, identify removable context. For a rate limit with a known reset time, show when another attempt is available. For a disconnect, retain the prompt and any clearly labeled partial answer. If generation could have triggered an external action, find out whether it took effect before retrying. Feedback on a bad response should remain associated with that response after edits or regeneration.

Distinguish an unavailable provider from an input problem or service refusal. Offer a compatible model, a permitted reformulation, or a manual path when available. For response feedback, offer a quick rating and optional detail, show when it has been recorded, and preserve the selection and detail if saving fails. Keep giving feedback and generating a replacement as separate actions.

For a design request, describe what the user sees and controls at the transition most likely to cost them work. For a review or fix, reproduce it with a delayed, stopped, or failed attempt and report the draft and result that survive. Check that Send, Stop, and recovery remain keyboard reachable while output grows, with readable focus and restrained motion at narrow widths and zoom. Say whether the behavior was observed on a real service or exercised with simulated events.
