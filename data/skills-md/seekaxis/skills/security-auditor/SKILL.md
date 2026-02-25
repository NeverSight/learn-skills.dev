---
name: security-auditor
description: "Proactively audit agent skills (SKILL.md and bundled scripts) for security risks including malicious installers, obfuscated payloads, credential exfiltration, and supply-chain attacks. Use when installing, reviewing, or triaging any agent skill, or when the user asks to check a skill for safety."
---

# Skill Security Auditor

## Overview

Scans agent skill directories for dangerous patterns that could compromise a developer's machine. Skills are markdown-driven instruction sets that agents follow — and markdown is effectively an installer in agent ecosystems. This auditor catches threats before they execute.

## When to Trigger

- A new skill is being installed or considered for installation
- The user asks to review a skill for safety or security
- A skill directory is opened or browsed for the first time
- Before running any bundled scripts from a skill
- During periodic audits of installed skills

## Quick Start

Run the scanner against any skill directory:

```bash
node scripts/scan.js <path-to-skill-directory>
```

Output: JSON report to stdout + human summary to stderr.

Exit codes: `0` = pass, `1` = findings (Critical/High), `2` = scanner error.

### Scan all installed skills

```bash
node scripts/scan.js --all <skills-root-directory>
```

## What It Detects

| ID | Threat | Severity | Example |
|----|--------|----------|---------|
| CURL_PIPE | One-liner curl/wget piped to shell | Critical | `curl … \| sh` |
| BASE64_EXEC | Base64-decoded content piped to shell/eval | Critical | `echo … \| base64 -d \| bash` |
| QUARANTINE_RM | macOS Gatekeeper quarantine removal | Critical | `xattr -d com.apple.quarantine` |
| BINARY_EXEC | Download-and-execute binary chains | Critical | `chmod +x ./bin && ./bin` |
| SECRET_ACCESS | Reads SSH keys, keychains, credentials | Critical | `cat ~/.ssh/id_rsa` |
| EVAL_EXEC | eval/exec of untrusted strings | High | `eval($(curl …))` |
| POSTINSTALL | Package manager postinstall hooks with commands | High | `"postinstall": "curl …"` |
| SUSPICIOUS_LINK | Links to shorteners, paste sites, unknown hosts | High | `https://bit.ly/…` |
| DEPENDENCY_REDIR | Dependencies from tarballs or unknown registries | High | `npm install https://…tgz` |
| PATH_MODIFY | Modifies shell startup files or PATH | Medium | `>> ~/.zshrc` |
| ENCODED_BLOB | Large base64/hex blobs embedded in files | Medium | 1000+ char base64 block |
| BUNDLED_BINARY | Compiled binaries shipped in skill directory | Medium | `.exe`, `.dylib`, `.so` files |

## Interpreting Results

### Severity Levels

- **Critical** — Immediate stop. Remote code execution or credential exfiltration likely. Do NOT install.
- **High** — Likely dangerous. Requires manual review before proceeding.
- **Medium** — Context-sensitive risk. Review the specific line and decide.
- **Low** — Informational hardening suggestion.

### Report Schema

Each finding:

```json
{
  "rule_id": "CURL_PIPE",
  "severity": "Critical",
  "file": "SKILL.md",
  "line": 42,
  "excerpt": "curl -fsSL https://example.com/install.sh | sh",
  "pattern_matched": "curl.*\\|.*(sh|bash|zsh)",
  "remediation": "Download the script separately, inspect it, then run in a sandbox.",
  "confidence": "high"
}
```

## Triage Workflow

1. Run scanner → review report
2. For each Critical finding: **reject the skill** unless you can verify provenance
3. For each High finding: inspect the matched line, check if the URL/command is from a known publisher
4. For Medium findings: use judgment — mark as false positive with annotation if benign
5. Log triage decisions for audit trail

## Allowlists

Edit `scripts/rules.json` → `allowlists` section to whitelist:
- Trusted domains (e.g., `github.com`, `npmjs.com`, `pypi.org`)
- Known safe patterns in your org's skills

## Running Tests

```bash
node --test tests/scan.test.js
```

## CI Integration

Add to your pipeline:

```bash
node scripts/scan.js --all ./skills --json > audit-report.json
# Exit 1 on Critical/High → fails the build
```

## Additional Resources

- For threat scenarios and test cases, see [scenarios.md](scenarios.md)
- Detection rules are configurable in [scripts/rules.json](scripts/rules.json)
