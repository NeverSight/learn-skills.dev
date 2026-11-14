---
name: pr-implementor-babysitter
description: Follow code reviews of authored changes, respond to review comments, and fix accepted feedback. Use when acting as the change author, not the reviewer.
---

# Implementor babysitter

Start after creating the review request on the host. Set up a monitor for review comments and requested changes until it closes, merges, or the user ends the assignment. The skill defines what to do when invoked; it does not keep an agent running. Use the available host and scheduler capabilities: prefer an event trigger for review activity, then a scheduled check if event triggers are unavailable. If neither is available, tell the user that follow-up requires a new invocation. On each wake-up, fetch the current request state and act only on new, relevant feedback.

Keep a durable per-request checkpoint with processed comment and review IDs and the last handled head commit. If a reliable checkpoint is unavailable, reconstruct what has already been handled from the request history. Ignore the agent's own comments so a reply does not trigger another reply.

Read each new comment or thread in context and check its claim against the code, intended behavior, and relevant repository boundaries. Separate the problem the reviewer observed from any fix they proposed. A real problem may need a different fix when the proposed one would introduce a wrong dependency, violate an API contract, or move responsibility into the wrong layer. Make the smallest sound fix, run relevant checks, push the change, and explain any different approach in the thread with the evidence behind it. Answer questions directly. If the concern itself is mistaken, explain the evidence politely; do not change correct code merely to close a thread. Avoid multiple pushes and replies for comments that can be handled together.

You may resolve a review thread yourself only when you applied the reviewer's suggested diff in full, line for line, and it covers the entire concern. For any other fix, partial application, alternative approach, or explanation without a code change, reply in the thread and leave the resolution decision to the reviewer.

Use the thread for routine clarifications, requests for more detail, and minor disagreements. Bring a consequential or stalled disagreement to the user with the reviewer's point, the relevant code or behavior, the tradeoff, and a recommendation. Examples include conflicting requirements, a scope change, or a disputed design decision. Continue with independent feedback while waiting. Do not silently dismiss or resolve the disputed thread.

Track feedback and completion signals from every reviewer, including humans and agents. Treat the current head as reviewed only after all requested or participating reviewers have finished reviewing that head and their actionable threads are resolved. After you push any new commit, wait for them to review the new head again, even if they had approved or said they had no further comments on the previous one. Do not treat an earlier completion signal as covering later changes.

Label every comment the agent posts. Use `Agent-authored` when the agent decided on or substantially wrote the point. Use `Agent-assisted at the user's direction` when the user directed the point and asked the agent to phrase or post it. This distinction depends on who directed the substance, even when the same account posts both. Include the agent name or identity when available; never imply a human wrote an agent comment.

Do not merge or close the request unless separately asked. When it closes or merges, stop its monitor and report the final status of addressed and open feedback.
