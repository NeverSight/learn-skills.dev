---
name: exec-observe
description: "DYNAMIC: run a target in a fresh working directory with a timeout and capture its behavior — exit code, stdout/stderr, wall-clock time, and files it creates. EXECUTES the target; use the tracer skills for syscall, API, or network visibility. Run only where you accept the target's risk."
---

# Execute & Observe (dynamic)

**⚡ Dynamic tier — this RUNS the target.** Run it only where you don't mind the risk:
a disposable VM or a dedicated analysis box, or behind an isolation provider.

## When to use

Use this when you need the target's exit status, output, file effects, and timing. For
deeper visibility, use `syscall-trace`, `net-capture`, or `frida-trace`.

## What it does

Runs the target in a fresh temp working directory with a timeout, and captures:
- **exit code** (and whether it timed out),
- **stdout / stderr** (head),
- **wall-clock duration**,
- **files created** in the working dir.

It bounds the run (working dir + timeout) but does **not** sandbox the target — the
target can do anything the host allows.

## Consent

Because it executes untrusted code, it's gated:
- via rekit: `rekit run --allow-dynamic exec-observe <target>` (the dispatcher sets the
  consent env for the runner);
- direct call: pass `--yes-i-consent` or set `REKIT_ALLOW_DYNAMIC=1`.

Without consent it refuses with `exit 4`.

## Usage

```bash
rekit run --allow-dynamic exec-observe ./sample --timeout 15
rekit run --allow-dynamic exec-observe ./sample --format json
```

## Prerequisites

- **python3 ≥ 3.8** — pure stdlib. (Whatever the *target* needs to run is on you.)
