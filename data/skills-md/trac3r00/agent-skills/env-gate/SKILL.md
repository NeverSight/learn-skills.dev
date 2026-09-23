---
name: env-gate
description: Prevents production crashes from environment variable drift. Compares a deployed .env against .env.example to find missing required keys, present-but-empty required keys, undeclared extra keys, and placeholder values left in the deployed file. Use before every deploy, in CI, or when onboarding a new environment — the #1 backend incident shape is "new key in the example never made it to prod".
when_to_use: Any project with .env.example + per-environment .env files, especially when multiple people or agents add keys. NOT a secrets manager or a secret scanner (use secret-gate for that); it checks completeness and drift, not credential safety.
version: 1.0.0
license: MIT
metadata:
  agentskills:
    tags: [env, deployment, backend, configuration, ci-gate]
---

# Env Gate

The most common backend incident is boring: a new key lands in `.env.example`,
the deploy goes out without it, and the crash surfaces in production logs.
This gate runs in CI or pre-deploy and fails the build first.

## Commands

```bash
python3 scripts/env_gate.py .env --example .env.example
python3 scripts/env_gate.py .env.production --example .env.example --json
python3 scripts/env_gate.py .env --example .env.example \
    --required-prefix DATABASE --required-prefix REDIS
python3 scripts/env_gate.py .env.local --example .env.example --ignore-extra
```

## Semantics

| Condition | Meaning | Exit |
|---|---|---|
| `missing` | key declared in example, absent in deployed | 1 |
| `empty_required` | key present in deployed but with no value | 1 |
| `placeholder` | deployed value still `<change-me>`-style | 1 |
| `extra` | deployed key the example no longer declares | 1 (suppress with `--ignore-extra`) |
| clean | all checks pass | 0 |

- `--required-prefix` (repeatable): scope missing/empty checks to keys starting
  with the prefix (e.g. only `DATABASE_*` must be complete; optional debug
  keys may drift).
- Placeholder values (`<your-key>`, `${VAR}`, `changeme`, `xxx`) in the
  deployed file are flagged — a deployed placeholder is worse than a missing
  key because it fails silently at runtime.

## Pairs with

`secret-gate` — env-gate asks "is the config complete?", secret-gate asks
"did a credential leak into the wrong place?". Run both pre-deploy.
