---
name: control-cli
description: Exercise a requested CLI or terminal UI through the current host’s shell
  and PTY controls, recording actual behavior and preserving unrelated files and processes.
license: MIT
---

# Control CLI

Read [the runtime contract](../hap-mode/references/runtime.md). Use host shell/PTY controls in the requested working directory. Inspect command help when flags are uncertain; do not assume a private terminal-control API or a particular shell.

Use batch execution for ordinary CLIs and a persistent PTY for interactive/TUI behavior. Retain session IDs and interact through documented session APIs. Record relevant output, exit status, and observable effects; startup alone is not successful behavior.

Reproduce a failure with the smallest realistic invocation. After a fix repeat it and compare outcomes. Use isolated task-owned files for probes that write data. Preserve existing files and unrelated processes; clean up only what this task created. Never use destructive commands, production writes, or credential-printing commands as probes.

Report concrete dependency, terminal, or permission gaps. Static source reading and screenshots are not substitutes for actual CLI verification.
