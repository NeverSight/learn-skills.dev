---
name: handoff
description: Compact the current conversation into a handoff document for another agent to pick up. Use when asked for a handoff, or when another skill says to write one.
argument-hint: "What will the next session be used for?"
---

Write a handoff document summarising the current conversation so a fresh agent can continue the work. Save it in the repository, in the project's handoff folder, else as `.handoff/<date>-<topic>.md`, and leave it uncommitted: the session that hands over commits it with the rest of its work.

Include a "suggested skills" section in the document, naming which skills the next agent should call the Skill tool for.

Do not duplicate content already captured in other artifacts (specs, plans, ADRs, issues, commits, diffs). Reference them by path or URL instead.

Redact any sensitive information, such as API keys, passwords, or personally identifiable information.

If the user passed arguments, treat them as a description of what the next session will focus on and tailor the doc accordingly.
