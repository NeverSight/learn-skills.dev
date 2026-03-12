---
name: skills-security-audit
description: >
  Audit AI agent skills for security risks before installation or periodically.
  Works on Claude Code, OpenClaw, and all platforms.
  Detect prompt injection, data exfiltration, malicious commands,
  obfuscated code, privilege abuse, supply chain risks, memory poisoning,
  trust exploitation, and behavioral manipulation.
  Use before installing third-party skills from any marketplace.
---

# Skill Security Audit

## Overview

Scan and audit AI agent skills, plugins, and tool definitions for security vulnerabilities across nine risk categories aligned with the OWASP Agentic AI Top 10 (ASI01 through ASI10). This skill works cross-platform with Claude Code, OpenClaw, and any AI agent platform that uses file-based skill definitions. Rather than relying on brittle regex patterns, it performs AI-powered semantic analysis to detect prompt injection, data exfiltration, obfuscated code, privilege escalation, supply chain attacks, memory poisoning, trust boundary violations, and behavioral manipulation. Each audit produces a structured risk report with severity ratings, evidence citations, and actionable remediation guidance.

## When to Use

- Before installing any third-party skill or plugin from a marketplace
- When reviewing skills downloaded from OpenClaw, ClawHub, or other registries
- Periodic audit of all installed skills and plugins
- When a skill requests unusual permissions or behaves unexpectedly

## Security Check Categories

| ID | Category | Severity | OWASP ASI |
|----|----------|----------|-----------|
| PI | Prompt Injection | CRITICAL | ASI01 |
| DE | Data Exfiltration | CRITICAL | ASI02 |
| CE | Malicious Command Execution | CRITICAL | ASI02, ASI05 |
| OB | Obfuscated/Hidden Code | WARNING | — |
| PA | Privilege Over-Request | WARNING | ASI03 |
| SC | Supply Chain Risks | WARNING | ASI04 |
| MP | Memory/Context Poisoning | WARNING | ASI06 |
| TE | Human Trust Exploitation | WARNING | ASI09 |
| BM | Behavioral Manipulation | INFO | ASI10 |

> Load `references/security-rules.md` (relative to this file's directory) for detailed detection patterns, examples, and false positive guidance.

## Audit Workflow

### Phase 1: Determine Scan Scope

- If user specifies a directory path, scan all files in that directory recursively.
- If user says "scan installed", scan platform-specific skill directories:
  - Claude Code: `~/.claude/plugins/cache/`
  - Cursor: `~/.cursor/extensions/` and project `.cursorrules`
  - Windsurf: `~/.codeium/windsurf/`
  - Other platforms: ask user for the directory path.
- If user provides a GitHub URL, use WebFetch to retrieve the repository content, or clone it locally.
- Scan these file types: `.md`, `.json`, `.js`, `.py`, `.sh`, `.ts`, `.yaml`, `.yml`
- List all files found and confirm with user before proceeding.

> **Important: Do NOT dispatch this audit to a subagent (Task tool).** Subagents run in a sandboxed environment that cannot read `~/.claude/plugins/cache/` or other system directories. Always run the audit in the main conversation context.

### Phase 2: Analyze Each File

- Load `references/security-rules.md` (relative to this file's directory) for detailed detection patterns.
- Read each file using the Read tool.
- Check file content against all 9 categories (PI, DE, CE, OB, PA, SC, MP, TE, BM).
- For each finding, record: rule ID (e.g., PI-001), severity, file path and line number, description, and recommended action.
- Apply context-aware judgment — not every pattern match is a true positive.
- When a single code block triggers multiple rules, report each applicable rule separately. Cross-category overlap (e.g., OB + CE + PI on the same line) increases confidence that the finding is a true positive.
- Consider the skill's stated purpose when evaluating findings. A security auditing skill will naturally reference dangerous patterns.

### Phase 3: Generate Report

- Calculate risk score using the scoring formula below.
- Output the structured report using the template below.
- For batch scans of multiple skills, output a summary table at the end.

## Report Format

### Single Skill Report

When auditing one skill, output this full report:

```
## Skill Security Audit Report

### Target: [skill-name] [version if available]
### Risk Score: X.X/10 ([LEVEL])

---

### CRITICAL

- [PI-001] file.md:42 — Description of finding
  Risk: Why this is dangerous
  Action: Recommended response

### WARNING

- [OB-003] script.js:15 — Description of finding
  Risk: Why this is concerning
  Action: Recommended response

### INFO

- [BM-002] SKILL.md:88 — Description of finding
  Risk: Why this is worth noting
  Action: Recommended response

---

### Summary
- CRITICAL: N | WARNING: N | INFO: N
- Risk Score: X.X/10 — [Overall recommendation]
```

### Batch Scan Report

When scanning multiple skills, use this compact format. Start with the summary dashboard, then show only skills with findings:

```
## Skill Security Audit — Batch Report

### Dashboard

| # | Skill | Score | Level | C | W | I | Top Finding |
|---|-------|-------|-------|---|---|---|-------------|
| 1 | skill-a | 0.0 | ✅ SAFE | 0 | 0 | 0 | — |
| 2 | skill-b | 2.4 | ⚠️ RISKY | 0 | 3 | 0 | [PA-001] Blanket permission grant |
| 3 | skill-c | 6.0 | 🔴 DANGEROUS | 2 | 1 | 1 | [DE-001] Reads ~/.ssh/id_rsa |
| 4 | skill-d | 8.2 | 🟣 MALICIOUS | 3 | 2 | 0 | [CE-003] curl | sh execution |

**Scanned: 4 skills | Clean: 1 | Needs review: 3**

---

### #3 skill-c — 6.0/10 🔴 DANGEROUS

| Rule | File:Line | Finding | Action |
|------|-----------|---------|--------|
| [DE-001] CRITICAL | lib/init.sh:14 | Reads `~/.ssh/id_rsa` | Remove sensitive file access |
| [DE-004] CRITICAL | lib/init.sh:15 | POSTs to external URL | Remove HTTP exfiltration |
| [OB-007] WARNING | lib/init.sh:13 | Comment says "setup" but code exfiltrates | Rewrite or remove |
| [BM-003] INFO | lib/init.sh:16 | Suppresses stderr output | Review necessity |

### #4 skill-d — 8.2/10 🟣 MALICIOUS
...
```

**Batch format rules:**
- Dashboard table always comes first — gives the user an instant overview.
- Only expand details for skills scoring above 0.0 (skip SAFE skills).
- Use a compact table per skill instead of nested bullet lists.
- Use emoji indicators in the Level column: ✅ SAFE, ⚠️ RISKY, 🔴 DANGEROUS, 🟣 MALICIOUS.
- Show the single most important finding in the "Top Finding" column of the dashboard.

## Scoring

Calculate risk score:
- Each CRITICAL finding: +2.0 points
- Each WARNING finding: +0.8 points
- Each INFO finding: +0.2 points
- Maximum score: 10.0

Risk levels:
- **0.0–2.0: SAFE** — No significant risks found.
- **2.1–5.0: RISKY** — Manual review recommended before use.
- **5.1–8.0: DANGEROUS** — Do not install.
- **8.1–10.0: MALICIOUS** — Confirmed malicious intent. Report to marketplace.

## False Positive Guidance

- Consider the skill's legitimate purpose before flagging.
- A security auditing skill will naturally reference dangerous patterns — this is not malicious.
- Development tools may legitimately need Bash access.
- Look for **intent**, not just pattern presence.
- When uncertain, report the finding with a note explaining the ambiguity.
