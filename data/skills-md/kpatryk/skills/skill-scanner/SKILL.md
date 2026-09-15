---
name: skill-scanner
license: MIT
description: >
  Comprehensive guide for Skill Scanner (Cisco AI Defense) to detect prompt injection,
  data exfiltration, command abuse, and malicious patterns in AI agent skills. Use this
  skill whenever a user asks to scan `SKILL.md` packages, secure a `skills/` repository,
  integrate agent-skill security checks in CI/CD (especially GitHub Actions SARIF uploads),
  tune scanner policies, reduce false positives, add pre-commit scanning, or troubleshoot
  `skill-scanner` flags and analyzer behavior. Always use this skill for requests involving
  "skill scanner", "agent skill security", "scan-all", policy presets (strict/balanced/permissive),
  overlap checks, or threat findings triage.
---

# skill-scanner

`skill-scanner` is a best-effort security scanner for Agent Skills. It combines static signatures, YARA, pipeline taint analysis, optional behavioral dataflow analysis, LLM semantic analysis, and optional cloud analyzers to detect probable threats in skill packages.

## Documentation URLs used to create this skill

- https://github.com/cisco-ai-defense/skill-scanner
- https://raw.githubusercontent.com/cisco-ai-defense/skill-scanner/main/README.md
- https://raw.githubusercontent.com/cisco-ai-defense/skill-scanner/main/docs/getting-started/quick-start.md
- https://raw.githubusercontent.com/cisco-ai-defense/skill-scanner/main/docs/github-actions.md
- https://raw.githubusercontent.com/cisco-ai-defense/skill-scanner/main/docs/user-guide/custom-policy-configuration.md
- https://raw.githubusercontent.com/cisco-ai-defense/skill-scanner/main/docs/reference/policy-quick-reference.md
- https://raw.githubusercontent.com/cisco-ai-defense/skill-scanner/main/docs/architecture/threat-taxonomy.md

## Safety and expectation setting

- Treat results as **best-effort detection**, not proof of safety.
- "No findings" means no known patterns were detected; it does **not** guarantee zero risk.
- Human review remains required for high-risk skills and production policies.

## Install and upgrade

```bash
# One-off package install
uv tool install cisco-ai-skill-scanner

# Keep current installation up to date
uv tool upgrade cisco-ai-skill-scanner

# Verify
skill-scanner --help
```

## Environment variables (optional, feature-dependent)

```bash
# LLM analyzer / meta analyzer
export SKILL_SCANNER_LLM_API_KEY="..."
export SKILL_SCANNER_LLM_MODEL="anthropic/claude-sonnet-4-20250514"

# Optional cloud analyzers
export VIRUSTOTAL_API_KEY="..."
export AI_DEFENSE_API_KEY="..."
```

## Core commands

```bash
# Interactive wizard
skill-scanner

# Single skill directory
skill-scanner scan skills/my-skill

# Whole repo skill tree
skill-scanner scan-all skills --recursive --check-overlap

# CI-friendly SARIF output
skill-scanner scan-all skills \
  --recursive \
  --check-overlap \
  --format sarif \
  --output skill-scanner-results.sarif
```

## Analyzer selection strategy

| Analyzer | Enable with | Use when | Notes |
|---|---|---|---|
| Static | default | Always | YAML + YARA signature coverage |
| Bytecode | default | Python skill packages | Checks `.pyc` integrity |
| Pipeline | default | Any shell tooling | Taint analysis for command chains |
| Behavioral | `--use-behavioral` | Python-heavy logic | AST dataflow analysis |
| LLM | `--use-llm` | Deeper semantic review | Requires API key |
| Meta | `--enable-meta` | Reducing noisy LLM findings | Pair with `--use-llm` |
| VirusTotal | `--use-virustotal` | Binary artifacts present | API key + possible upload policy |
| AI Defense | `--use-aidefense` | Centralized cloud checks | API key required |
| Trigger specificity | `--use-trigger` | Vague over-broad descriptions | Useful for skill quality checks |

## Policy and risk tuning

Use policy presets first, then custom YAML if needed:

```bash
# Presets
skill-scanner scan-all skills --policy balanced
skill-scanner scan-all skills --policy strict
skill-scanner scan-all skills --policy permissive

# Generate policy file then customize
skill-scanner generate-policy --preset balanced -o skill-scanner-policy.yaml
skill-scanner scan-all skills --policy skill-scanner-policy.yaml

# Interactive policy editor
skill-scanner configure-policy -o skill-scanner-policy.yaml
```

### Important merge behavior for custom policies

- Custom policy files merge on top of defaults.
- Scalar fields override directly.
- Lists replace default lists (they do not append automatically).

When reducing false positives, prefer:

1. Rule scoping and allowlists in policy.
2. Severity overrides.
3. `disabled_rules` only as a last resort.

## Output formats and CI behavior

```bash
# Summary for local quick checks
skill-scanner scan-all skills --format summary

# JSON for downstream tooling
skill-scanner scan-all skills --format json --output results.json

# SARIF for GitHub code scanning
skill-scanner scan-all skills --format sarif --output results.sarif

# Markdown report
skill-scanner scan-all skills --format markdown --detailed --output report.md

# Build gate
skill-scanner scan-all skills --fail-on-severity high
```

## Common usage workflows

### 1) Local repository triage

```bash
skill-scanner scan-all skills \
  --recursive \
  --check-overlap \
  --use-behavioral \
  --policy balanced \
  --format table
```

### 2) Deep analysis run (high coverage)

```bash
skill-scanner scan-all skills \
  --recursive \
  --check-overlap \
  --use-behavioral \
  --use-llm \
  --enable-meta \
  --llm-consensus-runs 3 \
  --policy strict \
  --format markdown \
  --detailed \
  --output skill-security-report.md
```

### 3) Lenient parsing for malformed skill packages

```bash
skill-scanner scan-all skills --recursive --lenient
```

## pre-commit integration

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/cisco-ai-defense/skill-scanner
    rev: v1.0.0  # use latest release tag
    hooks:
      - id: skill-scanner
```

Alternative installer:

```bash
skill-scanner-pre-commit install
```

## GitHub Actions integration pattern

Use a reusable script in `scripts/scan-skills.sh` and upload SARIF:

```yaml
name: Scan Skills

on:
  pull_request:
    paths:
      - "skills/**"
      - "scripts/scan-skills.sh"
      - ".github/workflows/scan-skills.yml"

jobs:
  scan:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      security-events: write
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - uses: astral-sh/setup-uv@v6
        with:
          enable-cache: true
      - run: ./scripts/scan-skills.sh
      - if: always()
        uses: github/codeql-action/upload-sarif@v3
        with:
          sarif_file: skill-scanner-results.sarif
```

## Error handling and troubleshooting

- **Missing command**: install/upgrade via `uv tool install|upgrade cisco-ai-skill-scanner`.
- **LLM errors**: verify API keys and `SKILL_SCANNER_LLM_MODEL`.
- **Unexpected false positives**: tune policy (`rule_scoping`, allowlists, severity overrides) before disabling rules.
- **Large trees**: use file limits in policy, then rerun with custom YAML.
- **Malformed skills**: use `--lenient` for migration scenarios.

## Usage examples (input -> expected output)

### Example 1: Basic repository scan

- Input: "Scan `skills/` and show whether high-risk findings exist."
- Command:
  ```bash
  skill-scanner scan-all skills --recursive --fail-on-severity high
  ```
- Expected output:
  - Summary per skill.
  - Exit non-zero if findings at/above `high` exist.

### Example 2: GitHub code scanning integration

- Input: "Produce SARIF for PR annotations."
- Command:
  ```bash
  skill-scanner scan-all skills --recursive --format sarif --output results.sarif
  ```
- Expected output:
  - `results.sarif` file suitable for `github/codeql-action/upload-sarif`.

### Example 3: High-noise repo tuning

- Input: "Find real issues but reduce documentation false positives."
- Command:
  ```bash
  skill-scanner scan-all skills \
    --recursive \
    --policy balanced \
    --use-llm \
    --enable-meta
  ```
- Expected output:
  - Lower-noise findings due to policy defaults + meta filtering.

### Example 4: Skill-package quality check

- Input: "Detect copied/overlapping skill descriptions in the same repo."
- Command:
  ```bash
  skill-scanner scan-all skills --recursive --check-overlap
  ```
- Expected output:
  - Overlap-related findings where descriptions are suspiciously similar.

## Python SDK quick start

```python
from skill_scanner import SkillScanner
from skill_scanner.core.analyzers import BehavioralAnalyzer

scanner = SkillScanner(analyzers=[BehavioralAnalyzer()])
result = scanner.scan_skill("skills/my-skill")
print(result.max_severity, len(result.findings))
```

## Practical execution checklist

When asked to run `skill-scanner` in a repository:

1. Identify target (`scan` for one skill, `scan-all` for folder trees).
2. Use `--recursive` for multi-directory repositories.
3. Emit SARIF for CI integrations.
4. Apply policy preset (`balanced` default, `strict` for audits).
5. Add `--use-behavioral` for Python-heavy skills.
6. Add `--use-llm --enable-meta` only when API keys are available and deeper semantic checks are needed.
7. Explain that findings are risk indicators, not definitive proof of compromise.
