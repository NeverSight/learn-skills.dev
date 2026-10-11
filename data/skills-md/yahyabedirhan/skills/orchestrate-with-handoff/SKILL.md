---
name: orchestrate-with-handoff
description: Pick up an effort from a handoff document and orchestrate it to a pull request.
argument-hint: "Path to the handoff document"
disable-model-invocation: true
---

# Orchestrate With Handoff

Start work without asking the maintainer for a go-ahead: they gave it when they handed the effort over to you.

1. Read the handoff. Confirm you are in the worktree and on the branch it names.
   - **If not:** say so and stop, because the effort's commits belong on that branch in that worktree.
2. Run `/orchestrate-effort` on the spec and tickets the handoff names, and on the handoff itself.

When the spec, tickets and handoff leave a question open, and the handoff says the session that wrote it can still be reached, look for the answer in that session before you decide the question yourself: it may know what the handoff left out.
