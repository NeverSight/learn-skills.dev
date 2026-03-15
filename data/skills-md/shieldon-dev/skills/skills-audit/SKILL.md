---
name: skills-audit
description: >
  Security scanner for AI agent skills. Audits skill files for credential theft,
  data exfiltration, dangerous commands, and obfuscation before installation.
  Use before installing any new skill to get a structured risk report with
  score (0-100), severity level, and actionable findings. Runs locally with
  zero external dependencies — nothing is sent over the network.
license: MIT
compatibility: Requires Python 3.10+. No additional packages needed — uses standard library only.
metadata:
  author: shieldon
  version: "1.0"
  homepage: https://shieldon.dev
allowed-tools: Bash(python:*)
---

# Skills Audit

Security scanner that audits AI agent skill files before installation. Detects credential theft, data exfiltration, dangerous commands, and obfuscation using pattern matching. Everything runs locally — no data leaves your machine.

## When to Use

Before installing any new skill or MCP server, scan it first. This catches embedded secrets, reverse shells, data exfiltration endpoints, obfuscated payloads, and other threats that hide in skill files.

## How to Run

Three input modes:

### Scan a local file

```bash
python scripts/scan.py --file /path/to/SKILL.md
```

### Fetch and scan a remote skill by URL

```bash
python scripts/scan.py --url https://example.com/SKILL.md
```

### Scan raw content directly

```bash
python scripts/scan.py --content "<paste skill text here>"
```

## Output Format

JSON with risk score, severity level, findings, and recommendation:

```json
{
  "scan_id": "a1b2c3d4-...",
  "risk_score": 75,
  "risk_level": "HIGH",
  "recommendation": "BLOCK",
  "findings": [
    {
      "type": "regex",
      "description": "AWS access key pattern detected",
      "severity": "HIGH",
      "evidence": "Matched Credential_AWS_Access_Key: AKIAIOSFODNN7EXAMPLE"
    }
  ]
}
```

## Decision Logic

| Score | Risk Level | Recommendation | Action |
|-------|-----------|----------------|--------|
| 0-29 | LOW | SAFE | Proceed with installation |
| 30-60 | MEDIUM | REVIEW | Ask human to review findings before proceeding |
| 61-70 | HIGH | REVIEW | Ask human to review — multiple concerning patterns |
| 71-100 | HIGH/CRITICAL | BLOCK | Do not install — refuse and explain findings |

Any finding with CRITICAL severity overrides to BLOCK regardless of total score.

## What It Detects

37 detection patterns across 4 threat categories:

- **Credential theft** — AWS, GitHub, Stripe, OpenAI, Anthropic, Supabase, database connection strings, crypto private keys, and 30+ more secret formats
- **Data exfiltration** — Discord/Slack/Telegram webhooks, paste services, file drop services, HTTP client POST calls, DNS tunneling
- **Dangerous commands** — Reverse shells, system destruction, privilege escalation, container escape, SSH key injection, PowerShell execution, deserialization attacks
- **Obfuscation** — Base64 decode chains, hex encoding, eval+encoding combos, string concatenation evasion, unicode escape sequences

For the full pattern list, see `references/DETECTION-COVERAGE.md`.

## Privacy

Everything runs locally. The `--file` and `--content` modes make zero network requests. The `--url` mode fetches only the specified URL (5s timeout, 100KB limit) and processes it locally. No data is sent to any external service.
