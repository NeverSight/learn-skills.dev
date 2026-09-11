---
name: arbitr
description: >-
  Operates the Arbitr translation API through the official arbitr CLI. Use when
  a user wants to set up Arbitr, translate local files, create or monitor a
  translation project, download deliverables, or check API-key access.
license: MIT
compatibility: Requires Python 3.11+, terminal access, and network access to https://api-arbitr.straker.ai
metadata:
  author: strakergroup
  version: "1.0"
---

# Arbitr CLI

Use the official `arbitr` CLI for local files. Treat `arbitr --help` and
`arbitr COMMAND --help` as the command reference.

## Setup

If the CLI is missing or no API key is configured, fetch and follow:

```text
https://arbitr.apidocumentation.com/getting-started/agent-setup/index.md
```

Do not submit a translation project as part of setup.

## Credentials

Keys are created only at:

```text
https://arbitr.straker.ai/settings/api-keys
```

Never ask the user to paste a key into chat. Ask them to store it locally as
`ARBITR_API_KEY` in the environment or an ignored `.env` file, then confirm
when it is ready. Never pass a key as a command-line flag, echo it, log it, or
overwrite unrelated `.env` values.

Run `arbitr me` before the first API operation. It returns the key's `org_id`,
`mode`, and `scopes`. Submit and download require both `verify:submit` and
`verify:read`.

- Prefer a test key (`abr_test_…`) while wiring. It validates requests without
  running the pipeline or spending credits.
- A live key (`abr_live_…`) spends credits on submit. Confirm with the user
  before their first live submission.

## Projects

Use lowercase BCP-47 locale tags such as `ko-kr` and `fr-fr`. Bare codes such
as `ko` are rejected unless the user explicitly asks for `--resolve-locales`.

Before composing a command, run `arbitr COMMAND --help` for the relevant
operation. For a standard unattended translation, submit with `--wait` and an
`--out` directory so the CLI waits for a terminal state and downloads the
deliverables.

If a wait exits `3`, the project needs human action. Do not resubmit it. Report
the gate and follow the CLI's resume guidance.

Use a caller-supplied `--idempotency-key` when retrying a failed submit so a
retry cannot create a second project.

## MCP

Use the CLI for files on disk. Hosted MCP accepts a public HTTPS file URL, not
a local path. Configure MCP only when the user asks or the client has no shell:

```text
https://arbitr.apidocumentation.com/getting-started/mcp/index.md
```
