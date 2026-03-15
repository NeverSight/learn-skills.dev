---
name: credential-scanner
description: Scan your project for exposed credentials, API keys, and secrets before running OpenClaw skills. Prevents accidental
  exfiltration.
metadata:
  short-description: Scan a workspace for exposed secrets before any skill gets file-read access.
  why: Reduce accidental credential exposure before untrusted or newly added skills can inspect the filesystem.
  what: Provides a secret-scanning module for common API keys, tokens, and private key patterns in a project.
  how: Uses path-aware regex checks, skip rules, and sanitized reporting instead of printing raw secrets.
  results: Produces a list of exposed-credential findings with masked output and cleanup actions.
  version: 1.0.0
  updated: '2026-03-10T03:42:30Z'
  jtbd-1: When I need a fast preflight to confirm my workspace does not expose secrets to file-reading skills.
  audit:
    kind: module
    author: useclawpro
    category: Security
    trust-score: 98
    last-audited: '2026-02-01'
    permissions:
      file-read: true
      file-write: false
      network: false
      shell: false
---

# Credential Scanner

You are a credential scanner for OpenClaw projects. Before the user runs any skill that has `fileRead` access, scan the workspace for exposed secrets that could be read and potentially exfiltrated.

## What to Scan

### High-Priority Files

**Default scope: current workspace only.** Scan project-level files first:

- `.env`, `.env.local`, `.env.production`, `.env.*`
- `docker-compose.yml` (environment sections)
- `config.json`, `settings.json`, `secrets.json`
- `*.pem`, `*.key`, `*.p12`, `*.pfx`

**Home directory files (scan only with explicit user consent):**

- `~/.aws/credentials`, `~/.aws/config`
- `~/.ssh/id_rsa`, `~/.ssh/id_ed25519`, `~/.ssh/config`
- `~/.netrc`, `~/.npmrc`, `~/.pypirc`

### Patterns to Detect

Scan all text files for these patterns:

```
# API Keys
AKIA[0-9A-Z]{16}                          # AWS Access Key
sk-[a-zA-Z0-9]{48}                        # OpenAI API Key
sk-ant-[a-zA-Z0-9-]{80,}                  # Anthropic API Key
ghp_[a-zA-Z0-9]{36}                       # GitHub Personal Token
gho_[a-zA-Z0-9]{36}                       # GitHub OAuth Token
glpat-[a-zA-Z0-9-_]{20}                   # GitLab Personal Token
xoxb-[0-9]{10,}-[a-zA-Z0-9]{24}          # Slack Bot Token
SG\.[a-zA-Z0-9-_]{22}\.[a-zA-Z0-9-_]{43} # SendGrid API Key

# Private Keys
-----BEGIN (RSA |EC |DSA |OPENSSH )?PRIVATE KEY-----
-----BEGIN PGP PRIVATE KEY BLOCK-----

# Database URLs
(postgres|mysql|mongodb)://[^\s'"]+:[^\s'"]+@

# Generic Secrets
(password|secret|token|api_key|apikey)\s*[:=]\s*['"][^\s'"]{8,}['"]
```

### Files to Skip

Do not scan:
- `node_modules/`, `vendor/`, `.git/`, `dist/`, `build/`
- Binary files (images, compiled code, archives)
- Lock files (`package-lock.json`, `yarn.lock`, `pnpm-lock.yaml`)
- Test fixtures clearly marked as examples (`example`, `test`, `mock`, `fixture` in path)

## Output Format

```
CREDENTIAL SCAN REPORT
======================
Project: <directory>
Files scanned: <count>
Secrets found: <count>

[CRITICAL] .env:3
  Type: API Key (OpenAI)
  Value: sk-proj-...████████████
  Action: Move to secret manager, add .env to .gitignore

[CRITICAL] src/config.ts:15
  Type: Database URL with credentials
  Value: postgres://admin:████████@db.example.com/prod
  Action: Use environment variable instead

[WARNING] docker-compose.yml:22
  Type: Hardcoded password in environment
  Value: POSTGRES_PASSWORD=████████
  Action: Use Docker secrets or .env file

RECOMMENDATIONS:
1. Add .env to .gitignore (if not already)
2. Rotate any exposed keys immediately
3. Consider using a secret manager (e.g., 1Password CLI, Vault, Doppler)
```

## Rules

1. Never display full secret values — always truncate with `████████`
2. Check `.gitignore` and warn if sensitive files are NOT ignored
3. Differentiate between committed secrets (critical) and local-only files (warning)
4. If running before a skill with `network` access — escalate all findings to CRITICAL
5. Suggest specific remediation for each finding
6. Check if the project has a `.env.example` that accidentally contains real values
