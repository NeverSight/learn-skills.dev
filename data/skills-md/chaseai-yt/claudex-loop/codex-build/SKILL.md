---
name: codex-build
description: "Have Codex implement a concrete work order and have Claude independently inspect the final changes. Preserves the explicit Codex builder choice; use claudex-loop for host-based planning and automatic reviewer selection."
---

# Codex Build

Compatibility entry point: the builder is explicitly Codex. The shared workflow and executable live in the sibling `claudex-loop` skill; install that skill alongside this one.

Load the shared [build reference](../claudex-loop/references/build.md) and [runtime reference](../claudex-loop/references/runtime.md). Preserve `SPEC_FILE` (mapped to the runner's `--plan`), `LOG_FILE`, `PROOF_CMD`, `MAX_FIX_ROUNDS`, and explicit model/effort arguments. The spec may have any filename; never substitute PLAN.md silently.

- In Claude Code, Claude coordinates and delegates implementation to Codex through the runner's `build --host claude --builder codex` path. Claude then inspects all changes and independently runs proof checks. Log evidence and limitations. A fresh Claude CLI inspector is also available through the shared runner if useful.
- In Codex, implement in the current host session with its normal tools, then use a fresh Claude inspector through `inspect --host codex --builder codex`. Do not ask Codex to certify its own changes as independent review.

Use the current valid plan approval when this follows claudex-loop. An explicitly requested standalone work order can use `--unreviewed-spec`, with that status recorded. If the spec still needs consequential decisions, settle those before delegating; do not build by inventing missing requirements.

Preserve unrelated changes, record the baseline, independently run the proof, inspect staged and new files as well as the unstaged diff, and keep fix rounds bounded. After a Claude takeover, require fresh Codex inspection of Claude's edits; if both contributed, log authorship and have each inspect the other's changes. Never present an earlier review as covering later fixes. Present the completed diff for any remaining sign-off required by the user's authorization.
