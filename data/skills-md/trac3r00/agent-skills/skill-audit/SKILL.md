---
name: skill-audit
description: Security-scans third-party agent skills before you trust them. A SKILL.md is executable authority — agents follow it with your credentials and filesystem. Detects prompt-injection patterns (instruction overrides, concealment directives), data-exfiltration signatures (sensitive paths + network sends), and dangerous script patterns (pipe-to-shell, eval-on-download) in any skills directory. Offline, deterministic, stdlib-only.
when_to_use: Before installing skills from a marketplace, after skill-sync aggregates skills from multiple providers, or as a periodic audit of everything your agents load. Findings are review candidates, not verdicts — read the flagged lines. NOT a sandbox or a guarantee; a clean report is not proof of safety.
version: 1.0.0
license: MIT
metadata:
  agentskills:
    tags: [security, prompt-injection, exfiltration, skills, supply-chain]
---

# Skill Audit

You audit npm packages before installing them. Skills deserve the same: a
malicious SKILL.md does not need code execution — the agent IS the executor.

## Commands

```bash
python3 scripts/skill_audit.py ~/.claude/skills ~/.codex/skills   # audit stores
python3 scripts/skill_audit.py --skill ./some-new-skill           # one skill
python3 scripts/skill_audit.py ~/.agents/skills --json --fail-over 0  # CI gate
```

Pair with `skill-sync`: after syncing skills into a universal directory, audit
that directory before any agent reads it.

## Detects

| Kind | Pattern |
|---|---|
| `instruction-override` | "ignore previous instructions", "disregard system prompt" |
| `concealment` | "do not tell the user", "without informing the owner" |
| `sensitive-path-exfil` | `~/.ssh`, `.env`, credentials paths near curl/POST/fetch (same line or 3-line window) |
| `pipe-to-shell` | `curl ... \| sh` install patterns |
| `eval-on-download` | `eval(urlopen(...))` and friends |
| `credential-harvest` | environment dumps flowing into network sends |
| `large-encoded-blob` | 120+ char base64 payloads hiding instructions |

## Reading results

Every finding carries skill, file:line, and the evidence line. Legitimate
skills trip patterns too (a browsing skill legitimately mentions curl and
cookies) — that is why the default gate is `--fail-over 0` findings for NEW
skills you have not read, and a higher budget for stores you already reviewed.
