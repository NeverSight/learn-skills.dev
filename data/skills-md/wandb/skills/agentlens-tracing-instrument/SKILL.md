---
name: agentlens-tracing-instrument
description: Add Forge AgentLens tracing to Python or TypeScript agents. Use when asked to trace agent turns, model calls, tools, or subagents with Forge or AgentLens.
---

# Forge AgentLens instrumentation

Complete the [login check](#check-login-first) before editing or initializing.
If no valid login exists, send only that section's reply and stop.

Forge exports explicit agent spans through a private OTel provider. It does
not auto-instrument frameworks, replace the global provider, or export that
provider's spans.

After a valid login, read the [Python](references/python.md) or
[TypeScript](references/typescript.md) reference and
[trace fidelity](references/trace_fidelity.md) before editing.
Verify the APIs against the installed SDK version.

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

## Instrument

- Confirm `entity/project`; a bare project cannot resolve its entity. Initialize
  once per process with runtime `WANDB_API_KEY`. Never print or commit credentials.
- Map Conversation → Turn → LLM/Tool/SubAgent to real boundaries: one turn per
  user exchange, one LLM span through stream consumption, one tool per execution.
  Preserve provider tool-call IDs and use explicit parents for delegated work.
- Preserve outputs, exceptions, retries, and cancellation. Close spans on failure;
  avoid duplicate capture from existing instrumentation.
- Keep project routing stable while work is active. Flush/shutdown at process
  exit, not per request. Python supports content suppression; this TypeScript
  revision requires omitting sensitive fields explicitly. Neither redacts PII.

## Implement incrementally

Add one traced path at a time: a model call, its tool loop, then delegation or
concurrency where applicable. After each change, run the path and follow
[read-back verification](references/read_back.md). Compare emitted and stored
spans with the actual execution before extending the instrumentation.

Fix mismatches and rerun the same check before continuing. Empty results,
failed queries, and unavailable checks are unverified, not passes. Stop at
that boundary and report what the user must do to unblock verification.

## Verify

Run the [conformance check](references/trace_fidelity.md#conformance-check)
for the paths you instrumented, including success, failure, and overlapping requests.
If the full suite requires CI, browsers, or unavailable services, run feasible
local checks and report the skipped coverage.
Assert parentage, tool-call IDs, and `gen_ai.operation.name` values
`invoke_agent`, `chat`, and `execute_tool` using Forge's provider or a local
OTLP receiver. Confirm backend arrival when authorized credentials are available;
otherwise report it unverified. Init/flush success alone is not delivery proof.
