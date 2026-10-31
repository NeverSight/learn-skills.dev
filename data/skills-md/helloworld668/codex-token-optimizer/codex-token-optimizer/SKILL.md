---
name: codex-token-optimizer
description: Reduce Codex token usage during coding sessions by choosing when to wrap shell commands with RTK, when to use Headroom MCP compression/retrieval/stats, and how to quantify savings. Use when the user mentions token budget, context bloat, long logs, large command output, RTK, Rust Token Killer, Headroom, MCP compression, Codex token optimization, or measuring token savings.
---

# Codex Token Optimizer

## Purpose

Keep useful evidence available while reducing avoidable context growth.

Use RTK for shell command output before it enters the model context. Use Headroom MCP for large text blobs, logs, retrieved documents, or tool outputs that should stay retrievable without sending every raw token to the model.

## Prerequisites

- Confirm `rtk` is available before relying on it: `rtk --version`.
- Configure RTK for Codex when needed: `rtk init -g --codex`, then restart Codex or open a new thread.
- Confirm Headroom MCP tools are visible before relying on them: `headroom_compress`, `headroom_retrieve`, and `headroom_stats`.
- If Headroom MCP was just installed, restart Codex or open a new thread before assuming the tools are active.
- Do not claim whole-session savings from RTK or Headroom alone. RTK measures command-output compression; Headroom measures its own compression layer. Codex app usage can also include conversation history, prompts, model overhead, and non-shell tool payloads.

## Environment Preflight

Run a quick environment check only when token optimization matters for the current task, the user asks about savings, or the task is likely to produce large outputs.

For RTK:

```bash
rtk --version
```

For Headroom, check whether the MCP tools are visible in the current Codex session. Do not assume a newly configured MCP server is available until Codex has been restarted or a new thread has been opened.

If a tool is missing, continue with bounded normal workflow instead of failing the task:

- For shell commands, use targeted commands such as `rg`, `sed -n`, `head`, `tail`, narrow test selections, and focused file reads.
- For large text, summarize only the task-relevant parts and preserve exact file paths, line numbers, command names, error codes, and identifiers needed for later verification.
- Do not report savings for a missing tool.
- Do not install software automatically. Ask for explicit user approval before installing RTK, Headroom, MCP servers, Python packages, Homebrew packages, or any other machine-level dependency.

When the user asks to install or approves installation, use the platform's normal install flow and then verify:

```bash
brew install rtk
rtk init -g --codex
rtk --version
rtk gain
```

For Headroom MCP, follow the current Headroom installation path for the user's environment, register the MCP server with Codex, verify that `headroom_compress`, `headroom_retrieve`, and `headroom_stats` are exposed, and tell the user that Codex may need a restart or new thread.

## Decision Rules

Use RTK by default for shell commands that may produce noisy or repetitive output:

```bash
rtk git status
rtk git diff
rtk git log -n 20
rtk rg "pattern" .
rtk find "*.ts" .
rtk pytest -q
rtk npm test
rtk cargo test
rtk docker logs service-name
rtk kubectl logs pod-name
```

Prefer RTK specialized modes for noisy tasks:

```bash
rtk err npm run build
rtk test pytest -q
rtk summary some-long-command
```

Use raw commands, or `rtk proxy <command>` when exact raw formatting matters and tracking is still useful. Examples include user-requested verbatim output, protocol payloads, binary output, generated files, checksums, or cases where compression could hide a significant line.

Use Headroom MCP when the content is too large to keep inline but may need exact retrieval later:

- Long logs or stack traces after RTK still leaves too much output.
- Large pasted text, RAG chunks, documentation excerpts, issue threads, or previous-agent handoff notes.
- Tool outputs where a compact summary is enough for now but exact lines may be needed later.

After compressing with Headroom, keep the returned handle or retrieval key visible in notes. Retrieve the original with `headroom_retrieve` before quoting exact text, making final claims from sparse evidence, or editing code based on details that may have been compressed away.

## Workflow

1. Classify the token risk before running a command or loading a large artifact.
2. Run the environment preflight when optimization depends on RTK or Headroom.
3. For shell work, run the command through RTK unless exact raw output is required and RTK is available.
4. For non-shell or still-large content, use Headroom MCP to compress and preserve a retrieval path when Headroom tools are available.
5. Retrieve original Headroom content when correctness depends on exact lines, names, versions, stack frames, or config values.
6. Report savings with separate metrics:
   - RTK: `rtk gain`, `rtk gain --history`, or `rtk gain --graph`.
   - Headroom: `headroom_stats`.
7. Explain the measurement scope. Do not add RTK and Headroom numbers together unless they clearly measure the same token boundary.

## Safety And Quality

- Never use compression to avoid reading required evidence.
- Do not compress secrets, credentials, private keys, payment data, or direct personal contact data into model-visible summaries.
- Be conservative for security, legal, medical, financial, deployment, and data-loss-sensitive tasks: retrieve raw evidence before final conclusions.
- If a compressed summary conflicts with raw output, trust the raw output.
- If RTK or Headroom is unavailable, say so and continue with normal commands while keeping output bounded with targeted commands such as `rg`, `sed -n`, `head`, `tail`, or narrow test selections.
