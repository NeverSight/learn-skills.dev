---
name: handoff
description: Use when the user wants to condense the current conversation into a handoff document for another agent to pick up.
argument-hint: "What will the next session be used for?"
user-invocable: true
disable-model-invocation: true
---

# Handoff

Write a handoff markdown document summarizing the current conversation so a fresh agent can continue the work. Save it to the `/tmp` directory.

Include a "Suggested skills" section listing skills the next agent should invoke.

Do not duplicate content already captured in other artifacts (PRDs, plans, ADRs, issues, commits, diffs). Reference them by path or URL instead.

Redact any sensitive information, such as API keys, passwords, or personally identifiable information.

If the user passed arguments, treat them as a description of what the next session will focus on and tailor the document accordingly.
