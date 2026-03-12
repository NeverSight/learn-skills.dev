---
name: clawscan
description: "Security scanner and hardening tool for OpenClaw deployments. Use when: user asks for security scan, audit, hardening, vulnerability check, or posture assessment of their OpenClaw setup. Runs 25+ checks across config security, file exposure, skill security, network security, and OpenClaw-specific hardening. Outputs A-F grade with actionable recommendations. Pure bash, zero dependencies."
---

# ClawScan Security

## Quick Start

Run a full scan:
```bash
bash "$(dirname "$0")/scripts/scan.sh"
```

## Usage

```bash
# Basic scan (shows failures only)
scripts/scan.sh

# Verbose (show all checks)
scripts/scan.sh --verbose

# JSON output
scripts/scan.sh --json

# Custom OpenClaw path
scripts/scan.sh --path /custom/openclaw/dir

# Formatted report
scripts/scan.sh --json | scripts/report.sh
```

## What It Checks

### Config Security (40 pts)
- Config file exists and is valid JSON
- No hardcoded API keys/tokens
- Gateway auth configured
- Gateway bind address secure
- HTTPS/TLS for remote access
- Model allowlist configured
- Exec security policy

### File Exposure (25 pts)
- No passwords in MEMORY.md
- No .env files with secrets
- No private keys in workspace
- Workspace permissions secure

### Skill Security (20 pts)
- Skills from known sources
- No exec override to 'full'
- No unjustified elevated permissions
- Skills directory permissions

### Network Security (15 pts)
- Gateway not publicly exposed without auth
- Webhooks use HTTPS
- Browser cookies secured

### OpenClaw-Specific (35 pts) — NEW
- Gateway auth token strength
- Config file not world-readable
- Model allowlist not wildcard
- Cron job security (elevated flags, dangerous commands)
- Memory files not world-readable
- OpenClaw version current
- Session/workspace isolation

## Tiers

- **Free:** All checks above. A-F grading. Text + JSON output.
- **Pro ($19/mo):** Advanced OS checks, trend tracking, severity scoring. Coming soon.
- **Managed ($49/mo):** Continuous monitoring, auto-remediation, alerting. Coming soon.

## Check Documentation

- OS checks: `references/checks-os.md`
- OpenClaw checks: `references/checks-openclaw.md`
