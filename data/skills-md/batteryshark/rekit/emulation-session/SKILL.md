---
name: emulation-session
description: "Create and operate persistent Unicorn or Qiling emulation sessions across separate agent, CLI, or MCP calls. Use for iterative reverse engineering that requires stepping, register or memory changes, address/syscall/API hooks, traces, branch snapshots, or repeated inspection without restarting the emulated target. Contained execution only; never runs the target natively."
---

# Stateful Emulation Session

Use a caller-chosen session directory as durable emulator state. Each invocation locks
the directory, restores the prior state, performs one operation, and saves the result.
This keeps the skill stateful through Rekit's ordinary CLI and MCP surfaces without a
second server or a background daemon.

## Workflow

1. Create a session with a raw code blob and `--engine unicorn`, or a full binary,
   matching rootfs, and `--engine qiling`.
2. Inspect or change registers and memory before execution when needed.
3. Add bounded observation hooks, enable tracing selectively, then `step` or `run`.
4. Save a named snapshot before exploring a branch; restore it to try another path.
5. Read the trace and state, then mark the session closed when the investigation ends.

```bash
rekit run emulation-session .rekit/emu/decoder create \
  --engine unicorn --input ./decoder.bin --arch x64 --trace --format json
rekit run emulation-session .rekit/emu/decoder step --count 4 --format json
rekit run emulation-session .rekit/emu/decoder read-registers --format json
rekit run emulation-session .rekit/emu/decoder save-snapshot --label before-branch --format json
```

Read [`references/operations.md`](references/operations.md) for the action and option
matrix, engine-specific behavior, persistence format, and safety boundaries.

## Rules

- Treat session directories and Qiling snapshot files as trusted local state; do not
  restore a session supplied by an untrusted party.
- Keep instruction and trace limits finite. Emulation is containment, not proof that a
  target is harmless.
- Use `emulate-code` or `qiling-emulate` for one-shot work. Use this skill only when
  state must survive multiple operations.
- Use separate session directories for parallel investigations.
- `close` preserves evidence and marks the session closed; it never deletes files.
- Every Unicorn result records backend provenance. On Apple Silicon, native and
  Rosetta x86_64 are capability-probed separately; a host signal is returned as a
  tooling-capability error and never as guest behavior.

See [`../../docs/UNICORN-X87.md`](../../docs/UNICORN-X87.md) for the x87 capability
checks and fallback contract.
