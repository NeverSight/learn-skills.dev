---
name: launch
description: Launch one agent for a task as a top-level session on its own worktree, or as a fusion orchestrator with --fusion.
argument-hint: "[--fusion] [--model <model>] [--on <host>:<path>] <task>"
disable-model-invocation: true
---

Invoke `routing` first.

1. Infer the task's likely edit scope, then run `scripts/launch.sh --sessions [--on '<host>:<path>']`.
   File `status` is relative to this worktree; an active session with no files may not have edited
   yet. With `--on`, sessions list titles only, so judge overlap from titles.
   Mention small, localized overlaps without blocking. Resolve every likely large conflict with me
   before launching: reuse the worktree/session, wait for integration, or proceed regardless.

2. Launch. The worktree starts at this checkout's HEAD; if the task depends on uncommitted changes,
   raise it with me first.

   ```
   scripts/launch.sh --model <model> --title <title> [--fusion] [--on '<host>:<path>'] <prompt>
   ```

   - **`--model`:** if the invocation includes `--model <model>`, pass it as-is; otherwise use the
     model `routing` picks (fusion orchestrator with `--fusion`, else the handoff's model).
   - **With `--fusion`:** pass it on. The prompt is the task, expanded to stand alone; the launched
     agent has none of this conversation.
   - **Without:** write the prompt as a spec or a brief, as `routing` defines them; ask the agent
     to commit its work.
   - `<title>`: names the session, the worktree, and its new branch. Write a headline naming the
     change, e.g. `Fix login redirect loop`, distinct from its siblings at a glance.

3. Report the session ID and the worktree path.
