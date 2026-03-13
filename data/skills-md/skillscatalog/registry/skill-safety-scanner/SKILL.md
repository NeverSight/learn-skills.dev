---
name: skill-safety-scanner
description: Run local safety scans on Agent Skills before publishing. Detects secrets, dangerous code patterns, and analyzes required permissions.
version: 1.0.0
license: MIT
author: "@anthropic-agent-skills"
tags:
  - safety
  - security
  - scanning
  - validation
---

## Instructions

Use this skill to run safety scans on any Agent Skill directory before publishing. The scanner detects:

- **Secrets** - Hardcoded API keys, tokens, passwords, private keys
- **Dangerous Code** - eval(), exec(), command injection, XSS patterns
- **Permissions** - Required capabilities (filesystem, network, subprocess, etc.)

### When to Use

- Before submitting a skill for publication
- To preview what the catalog safety scan will find
- To identify and fix security issues early
- As part of CI/CD pipelines

### How to Use

Scan a skill directory:

```
Scan the skill at /path/to/my-skill for safety issues
```

Get detailed output:

```
python3 safety_scan.py /path/to/my-skill --verbose
```

Get JSON output for CI integration:

```
python3 safety_scan.py /path/to/my-skill --json
```

### Output

```
Safety Scan Report
  Skill: my-skill
  Grade: B (85/100)

  Scores:
    Secrets: 100/100
    Dangerous Code: 70/100

  Permissions Detected:
    - filesystem
    - network

  Findings (1):
    [medium] Potential command injection
      File: scripts/main.py:42
      Code: subprocess.run(cmd, shell=True)

  Recommendation: Review the finding above before publishing.
```

## Examples

**Basic scan:**
```
User: Scan my skill at ./document-tools for safety issues
Agent: Running safety scan on ./document-tools...

       Grade: A (95/100)
       No critical issues found.
```

**Finding secrets:**
```
User: Check ./my-api-client for security issues
Agent: Running safety scan...

       Grade: F (0/100)

       Findings:
         [critical] Hardcoded API key detected
           File: config.py:5
           Code: API_KEY = "sk-ant-..."

       You must remove this secret before publishing.
```

## Limitations

- Does not scan dependencies (use npm audit / pip-audit separately)
- Pattern-based detection may have false positives
- Cannot detect all security issues (not a replacement for security review)
- Scans local files only (not GitHub URLs)

## Dependencies

- Python 3.9+
- No external dependencies (uses Python stdlib)
