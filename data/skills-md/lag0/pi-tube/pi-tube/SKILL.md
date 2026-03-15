---
name: pi-tube
description: |
  Official pi-tube CLI skill for deterministic media transcription workflows.

  USE FOR:
  - YouTube/Instagram/direct URL/local file transcription via CLI
  - Deterministic Markdown/JSON artifact generation
  - Provider readiness and configuration flows

  Must be pre-installed. See rules/install.md for installation and setup, and rules/security.md for output handling.
allowed-tools:
  - Bash(pi-tube *)
---

# Pi-Tube CLI

Deterministic transcription CLI focused on agent-friendly output contracts.

Run `pi-tube --help` for current command details.

## Prerequisites

- `pi-tube` available in PATH.
- Provider credentials configured with `pi-tube config` or env variables.

If not installed, follow [rules/install.md](rules/install.md).
For output safety and untrusted content handling, follow [rules/security.md](rules/security.md).

## Quick Checks

```bash
pi-tube --version
pi-tube help
pi-tube help config
pi-tube help setup
pi-tube provider-status
```

## Typical Workflow

1. Configure defaults and credential references:

```bash
pi-tube config provider set deepgram
pi-tube config provider env deepgram DEEPGRAM_API_KEY
pi-tube config provider env groq GROQ_API_KEY
pi-tube config language set pt-BR
pi-tube config list
```

2. Run transcription:

```bash
pi-tube "https://youtube.com/watch?v=dQw4w9WgXcQ"
pi-tube --provider groq --language pt --json "./recording.mp3"
```

3. Inspect output:

- Default: deterministic markdown artifact
- `--json`: deterministic schema-versioned JSON contract

## Key Commands

```bash
pi-tube <input>
pi-tube help [command]
pi-tube --json <input>
pi-tube config provider set <deepgram|groq>
pi-tube config provider env <deepgram|groq> <ENV_VAR>
pi-tube config language set <code>
pi-tube config set <key> <value>    # legacy compatibility
pi-tube config get <key>            # legacy compatibility
pi-tube config list
pi-tube setup skills --global --yes
pi-tube provider-status
```

## Notes

- Precedence: CLI flags > config defaults > env defaults.
- If no provider credential is configured, CLI exits early with deterministic error guidance.
- If selected provider fails with auth/unavailable/failed and alternate provider is configured, CLI can fallback automatically.
- `config provider env` expects an env var name (ex: `GROQ_API_KEY`), not a raw secret value.
- Instagram private/auth-gated URLs fail with `INSTAGRAM_AUTH_REQUIRED`.
- For release quality gates, run `bun test` and `bun run verify:fixtures`.
