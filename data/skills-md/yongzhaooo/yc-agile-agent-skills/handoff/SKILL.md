---
name: handoff
description: Compact the current conversation into a handoff document for another agent to pick up.
---

Write a handoff document so a fresh agent, which cannot see this conversation, can continue the work.

**Where to save.** For project work, use the project's existing handoff, report, or stage-receipt location and format when one is defined; do not create a second project registry. Otherwise save it to the OS temp directory, not the workspace: resolve it from `$TMPDIR`, falling back to `/tmp` (`%TEMP%` on Windows), never a session-scoped scratchpad. Tell the user the absolute path of the file you wrote. A temporary file is a navigation aid, not durable evidence. Write the document in the project's documentation language, else the user's language.

**What the next agent needs**, each item only when it applies:

- the objective and the assigned scope, including what is out of scope, with links to the authoritative plan, spec, or status entry and any upstream receipts;
- the current state as of writing: date, repository, branch, HEAD commit, and uncommitted or untracked work that matters, plus the source, runtime, or data identities in use; in a shared checkout, which files or hunks belong to this work and which belong to others and must not be touched. Tell the next agent to re-check `git status` and HEAD before acting;
- what was verified, with the command or a link to evidence at a location that outlives this session, kept apart from what is assumed, proposed, or unverified; flag anything that exists only in a session scratchpad. Keep completed work apart from measured results and promotion decisions;
- approaches already tried and rejected, and checks that are still valid, so the next agent does not redo them;
- open decisions and who owns them, pending gates, and authorization limits; a handoff does not expand authorization or override a request to stop;
- the exact next step and a safe resume point;
- a "suggested skills" section naming the skills the next agent should invoke.

Read the working state rather than relying on memory. Do not claim a gate passed from a previous agent's prose alone, and do not rerun valid checks merely to produce a handoff. If work is incomplete, say so and list what is pending.

Do not duplicate content already captured in other artifacts (specs, plans, ADRs, issues, commits, diffs). Reference them by path or URL instead.

Redact any sensitive information, such as API keys, passwords, or personally identifiable information.

If the user passed arguments, treat them as a description of what the next session will focus on and tailor the doc accordingly.
