---
name: status
description: Use when an agent needs to read or publish its one-line Tariboy progress status.
---

# Status

**REQUIRED:** Use `cli-text` before passing text to this CLI. Keep the storage
rules below; quote transport separately. Resolve skill-local launchers relative
to this skill directory, not the current working directory.

Execute the launcher when command execution is available. If it is unavailable,
return the exact command instead; never claim a status was read or updated unless
the command succeeded.

Use `scripts/status.sh` to read status, or `scripts/status.sh set "what I am doing"` to update it. Do not set or propose a multi-line status; reduce it to a one-line progress summary. A status update leaves the current iteration unchanged, so continuing work needs no loop action. Only when the user explicitly asks the status change to finish the iteration, return two parts: the one-line `set` command, then a separate explanation that completion requires the `loop` skill. Never put lifecycle instructions inside the status message.
