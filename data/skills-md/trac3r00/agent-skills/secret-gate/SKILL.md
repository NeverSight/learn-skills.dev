---
name: secret-gate
description: Blocks credentials from entering code, diffs, or agent output. Scans files or a unified diff for known key formats (AWS, GitHub, OpenAI/Anthropic-style, Slack, GCP, private keys, JWTs, assigned passwords) plus high-entropy assigned strings — offline, stdlib-only, no gitleaks binary. Use as a pre-commit gate on agent-written diffs, before pasting config into a session, or in CI.
when_to_use: Any workflow where an agent writes or echoes configuration, .env values, or API clients — agents paste real keys into examples more often than humans do. NOT a full gitleaks replacement; it favors precision on the formats agents actually leak.
version: 1.0.0
license: MIT
metadata:
  agentskills:
    tags: [secrets, security, ci-gate, diff, credentials]
---

# Secret Gate

An agent with your `.env` in context will eventually write it somewhere it
should not go. This gate catches the leak before it lands.

## Commands

```bash
python3 scripts/secret_gate.py src/ config.py          # scan files/dirs
git diff | python3 scripts/secret_gate.py --diff       # only added lines
git diff --cached | python3 scripts/secret_gate.py --diff   # pre-commit
python3 scripts/secret_gate.py --diff --json < changes.patch
python3 scripts/secret_gate.py --history --repo .      # git-guardian mode: scan commit history
python3 scripts/secret_gate.py --history --repo . --max-commits 500
```

Exit 1 on any finding — wire it straight into pre-commit or CI.

## Detects

- Structured keys: AWS (`AKIA...`), GitHub (`ghp_`/`github_pat_`), OpenAI/
  Anthropic-style (`sk-`, `sk-ant-`), Slack (`xox?-`), GCP (`AIza...`),
  Stripe (`sk_live_`/`rk_live_`), SendGrid (`SG....`), npm, PyPI, Discord,
  basic-auth URIs
- Private key blocks, JWTs
- Assigned passwords/secrets: `password = "..."`, `api_key: '...'`
- High-entropy strings assigned to secret-shaped names (Shannon entropy > 4.0)

## Suppression

- Inline: append `gitleaks:allow`, `secret-gate:allow`, or
  `pragma: allowlist secret` to a known-safe line.
- Placeholder values (`example`, `changeme`, `<your-key>`, `${VAR}`) are
  skipped automatically.
- `--allow REGEX` (repeatable) for project-wide allowlists.

## Pairs with

`comment-checker` (same diff-mode contract), `skill-audit` (scan skills you
install, not just code you write).
