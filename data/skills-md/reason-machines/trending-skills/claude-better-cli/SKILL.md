---
name: claude-better-cli
description: Compatibility-first Claude CLI reimplementation with faster startup, lower memory, and drop-in command compatibility
triggers:
  - use claude-better
  - faster claude cli
  - claude cli startup performance
  - replace claude cli with claude-better
  - claude-better harness
  - drop-in claude cli replacement
  - optimize claude cli memory usage
  - claude-better compatibility
---

# claude-better

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

`claude-better` is a compatibility-first reimplementation of the Claude CLI focused on aggressive performance improvements: up to 73% faster startup and up to 80% lower resident memory, while maintaining 100% command-level compatibility with the original Claude CLI.

## What It Does

- **Faster cold starts**: `--help` goes from 182ms → 49ms; `chat` session bootstrap from 311ms → 102ms
- **Lower memory**: sustained interactive sessions drop from ~412MB → ~83MB RSS
- **Drop-in compatible**: 100% pass rate on primary command forms, 100% exit-code match, 98.7% byte-for-byte output parity
- **Zero migration cost**: existing scripts, aliases, and muscle memory continue to work unchanged

## Availability

> ⚠️ Source code is provided for selected high-profile customers only and available upon request. Contact the maintainer at [krzyzanowskim/claude-better](https://github.com/krzyzanowskim/claude-better) for access.

If you have access, install as described in your onboarding materials. The binary is a drop-in replacement — substitute it wherever you invoke `claude`.

## Installation (Once You Have Access)

```bash
# Typical binary drop-in replacement pattern
# Place the claude-better binary in your PATH before the original claude
export PATH="/path/to/claude-better/bin:$PATH"

# Verify it's being picked up
which claude
claude --version
```

```bash
# Or alias it explicitly without touching PATH
alias claude='/path/to/claude-better/bin/claude-better'
```

## Key Commands

`claude-better` mirrors the Claude CLI surface exactly. All commands you know work as-is:

```bash
# Show help (cold start: ~49ms vs 182ms baseline)
claude --help

# Check auth status (warm start: ~58ms vs 146ms baseline)
claude auth status

# Start an interactive chat session (~102ms bootstrap vs 311ms baseline)
claude chat

# One-shot non-interactive command (~131ms vs 428ms baseline)
claude -p "Summarize this file" < input.txt

# All standard flags pass through unchanged
claude --model claude-opus-4-5 chat
claude --output-format json -p "List 3 facts about Rust"
```

## Configuration

`claude-better` reads the same configuration as the original Claude CLI. No new config format is required.

```bash
# Standard Claude CLI env vars are respected
export ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY

# The tool reads ~/.claude/ config directory as normal
# No migration of config files needed
```

## Performance Characteristics

| Scenario | Baseline | claude-better | Improvement |
|---|---|---|---|
| `--help` cold start | 182ms | 49ms | 73% faster |
| `auth status` warm | 146ms | 58ms | 60% faster |
| `chat` bootstrap | 311ms | 102ms | 67% faster |
| One-shot command | 428ms | 131ms | 69% faster |
| RSS after 30min session | 412MB | 83MB | 80% less |
| Streaming jitter p95 | 91ms | 24ms | 74% lower |

## Scripting Patterns

Since compatibility is 100%, all existing scripting patterns work unchanged:

```bash
#!/usr/bin/env bash
# Existing Claude CLI scripts work without modification

# Non-interactive pipeline usage
echo "Explain this error:" | cat - error.log | claude -p /dev/stdin

# Exit code handling (100% compatible)
if claude auth status; then
  echo "Authenticated"
else
  echo "Not authenticated — run: claude auth login"
  exit 1
fi

# JSON output parsing
claude --output-format json -p "What is 2+2?" | jq '.content'
```

```bash
#!/usr/bin/env bash
# Long-lived interactive session — memory pressure is significantly reduced
# Useful on memory-constrained machines (laptops, CI runners)
claude chat
```

## Compatibility Notes

- **CLI surface**: 100% compatible with targeted Claude CLI command forms
- **Exit codes**: 100% match on documented exit-code behavior  
- **Output parity**: 98.7% byte-for-byte; 100% semantic parity after whitespace/timestamp/terminal-width normalization
- **Tested environments**: macOS (Apple Silicon), Linux, containerized CI
- **Tested against**: 1,200 synthetic invocations, 87 flag combinations, 42 interactive flows, 14 failure-mode scenarios

## Troubleshooting

**Binary not found after install**
```bash
# Ensure claude-better/bin is earlier in PATH than original claude
echo $PATH | tr ':' '\n' | grep -n claude
which claude  # should point to claude-better
```

**Unexpected output differences**
```bash
# 1.3% of outputs differ before normalization (timestamps, whitespace, terminal width)
# If a script breaks on exact output matching, add normalization:
claude -p "..." | tr -s ' ' | sed 's/[[:space:]]*$//'
```

**Auth not recognized**
```bash
# claude-better reads the same auth store as the original CLI
# If auth fails, re-authenticate via the standard flow:
claude auth login
```

**Falling back to original CLI**
```bash
# If you hit an edge case, unset the alias/PATH change to revert instantly
unalias claude
# or
export PATH="<original-path-without-claude-better>"
```

## Architecture Notes (For Contributors / Evaluators)

The performance gains come from specific implementation choices documented in the README:

- **Zero-copy streaming pipeline** for token output (reduces streaming jitter)
- **Precomputed command registry** instead of dynamic startup discovery (cuts cold-start time)
- **Aggressively bounded allocation** for session state (drives memory reduction)
- **Lazy subsystem initialization** — only the active command path pays startup cost
- **Compatibility shim layer** that preserves flags/behavior without carrying the full original stack
