---
name: self-awareness
description: Inspect the active Feynman workbench session, artifacts, execution log, settings, and provenance. Use when the task asks what happened in this session, which files were written, what tools ran, or what remains unverified.
---

# Self Awareness

Use this skill to answer questions about the active Feynman session.

Workflow:

1. Inspect the workbench state, session logs, execution records, artifact versions, plan files, and settings that own the fact.
2. Report counts and statuses from current files or API output, not from memory.
3. Distinguish artifacts produced by chat, notebook, compute, upload, seed fixtures, and manual files.
4. Identify verification state: checked, inferred, unverified, blocked, or failed.
5. Keep secrets, private paths, and irrelevant transcript content out of summaries.

This skill is for Feynman introspection, not for querying the local reference app.
