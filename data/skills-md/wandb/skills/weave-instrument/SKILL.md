---
name: weave-instrument
description: Add Weave tracing to Python or TypeScript agents and LLM applications. Use when asked to instrument model calls, tools, or agent turns with Weave.
---

# Weave instrumentation

Complete the [login check](#check-login-first) before editing or initializing.
If no valid login exists, send only that section's reply and stop.

After a valid login, inspect the application's dependencies, agent boundaries,
and existing OTel provider. Confirm `entity/project` and runtime credentials
before sending data; never read, print, or commit API keys. Read
[trace fidelity](references/trace_fidelity.md) before changing any instrumentation
path. Initialize once at startup with
`weave.init("entity/project")` in Python or `await weave.init(...)` in Node.

## Check login first

Before editing code or initializing tracing, verify the existing W&B login for
the target deployment with a noninteractive, read-only identity request through
the configured SDK or connector. Use credentials in place; never print, copy,
or inspect secret values. Do not call `login` or tracing `init` as a login probe.

If no valid login exists, stop. Do not edit, initialize, or continue this skill.
Do not run `wandb login` in this session. This session's shell is not a normal
terminal, so `wandb login --verify` exits with `No API key configured` instead
of prompting. Do not ask for a key in this chat or create credentials.

Send only this, and nothing else. No decisions, notes, plans, or
documentation links:

There's no W&B login yet, so this stops here. Open a new terminal tab and run
`wandb login --verify`. Create an API key at
https://wandb.ai/authorize?ref=models. If the browser opens a different page,
open that link again. Paste the key in that terminal, not here, and type
continue.

On a self-hosted or dedicated deployment, use `wandb login --verify --host <base-url>`
and the authorize page that command prints. Still send only that.

- If the check is unavailable or fails because of connectivity or permissions,
  report login/access as unverified and stop; do not assume credentials are invalid.
- After the user continues, confirm the application runtime can use its own
  configured credentials and access `entity/project`. A browser login does not
  establish SDK authentication. Node/Forge runtimes without a `.netrc` fallback
  need credentials configured by the user through their runtime secret mechanism.

## Choose the mechanism

- **Explicit agent spans:** use the Session SDK for turns, model calls, tools,
  and delegation when auto-instrumentation cannot produce the required tree.
  Read the [Python](references/session_sdk_python.md) or
  [TypeScript](references/session_sdk_typescript.md) reference.
- **Auto-instrumentation:** use only when the installed SDK captures the
  library and desired span shape. Check Python's `INTEGRATION_MODULE_MAPPING`
  or Node's `integrations/hooks.ts`, then verify emitted spans. Read
  [auto-instrumentation caveats](references/otel_auto.md); registry membership
  alone does not prove capture is active. Avoid duplicate manual wrapping.
- **Existing OTel pipeline:** add Weave export to that provider using
  [endpoint configuration](references/otel_endpoint.md).

A turn spans one user exchange, including its tool loop. An LLM span covers
one model call through stream completion; a Tool covers execution; a SubAgent
covers delegation. Record actual output/usage and preserve provider tool-call
IDs. Keep return values, exceptions, retries, and cancellation unchanged.
Close spans on failure and isolate concurrent conversations.

## Implement incrementally

Add one traced path at a time: a model call, its tool loop, then delegation or
concurrency where applicable. After each change, run the path and follow
[read-back verification](references/read_back.md). Compare emitted and stored
spans with the actual execution before extending the instrumentation.

Fix mismatches and rerun the same check before continuing. Empty results,
failed queries, and unavailable checks are unverified, not passes. Stop at
that boundary and report what the user must do to unblock verification.

## Verify

Run relevant application tests and the
[conformance check](references/trace_fidelity.md#conformance-check) for the paths
you instrumented. If the full suite requires CI, browsers, or unavailable
services, run focused local checks covering success and failure, and report the
skipped coverage. Check parentage and
`gen_ai.operation.name`: `invoke_agent` for turns/subagents, `chat` for LLMs,
`execute_tool` for tools. Agent-shaped traces belong in Agents; flat calls in
Calls. Confirm backend arrival when credentials are available; an init banner
or successful flush is not delivery proof. Otherwise report the unverified
surface and give the application's exact smoke command.

Adapted from [Weave](https://github.com/wandb/weave/tree/c003a2f4e425cde178ebcc4a2a3dbf8534fba1d3/skills/weave-instrument).
Use the installed SDK's exports when they differ from these references.
