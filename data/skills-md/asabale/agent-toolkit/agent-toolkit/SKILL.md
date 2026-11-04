---
name: agent-toolkit
description: Use when you need to find, run, chain, or save reusable CLI tools with tk instead of MCP servers.
---

# Agent Toolkit (`tk`)

Minimum turns and tokens. Use an existing tool first. When a raw command is repeatable, save it.

## 0. Bootstrap (if `tk` is missing)

Idempotent. Clone or update `~/.agent-toolkit`, then install or call that `tk`:

```bash
git clone --depth 1 https://github.com/ASabale/agent-toolkit.git ~/.agent-toolkit || git -C ~/.agent-toolkit pull --ff-only
~/.agent-toolkit/install.sh
export PATH="$HOME/.local/bin:$PATH"
```

Or run `~/.agent-toolkit/tk` directly. Re-running is safe.

## 1. Use (`Find → Run`)

1. **Find**: `tk find "<intent>"` (match plus a runnable command).
2. **Run** that line with real `--flag` values: `tk run <tool> --flag "<value>"`.
   `tk info <tool>` for flags. On failure, run `fix` from `stderr`. If output has `next`, run it. Pipe JSON or `tk run <chain>` for multi-step.

## 2. Evolve (`Save → Check`)

When `tk find` misses and raw CLI solved a repeatable task:

1. **Save** (`$TK_ARG_<FLAG>` inputs, compact JSON on `stdout`): `tk save <namespace>.<name> --summary "<1-line summary>" --safety <read-only|mutating|destructive> --file <script>`
   Or: `tk chain save <namespace>.<name> --summary "<1-line summary>" --steps '<json-or-names>'`
2. **Verify**: `tk check <namespace>.<name> && tk run <namespace>.<name> --dry-run`
3. **Prune**: `tk evolve` reports unused, failures, overlap; `tk prune` archives drops.

## Rules
- Distill `stdout`. Named `--flags` only; no positional args; no hardcoded IDs, hosts, or paths.
- Do not wrap one UNIX command; save tools that collapse steps, filter noise, or enforce safety.
