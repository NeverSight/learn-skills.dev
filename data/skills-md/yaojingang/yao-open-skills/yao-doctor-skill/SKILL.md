---
name: yao-doctor-skill
description: Audit local and OpenClaw skill libraries for privacy theft, credential theft, stealthy exfiltration, unsafe execution chains, deceptive instructions, and persistence behavior, then generate a visual HTML security report. Use when Codex needs to security-review one skill or a full skill library before install, enablement, or execution. Do not use for generic cleanup, usage estimation, or app-level security review outside skill packages.
---

# Yao Doctor Skill

## Boundary

Own this recurring job: security-review skill packages as untrusted code and untrusted instructions, separate broad capability risk from actual unsafe behavior, and produce evidence-backed recommendations before the skills are installed or executed.

Do not route here for:

- generic code security reviews outside skill folders
- skill cleanup, archival, deduplication, or stale-usage analysis
- privacy policy writing without scanning files
- creating a brand-new skill with no security audit need

## Default Workflow

1. Run `scripts/run_yao_doctor_skill.py [root] [more-roots]`.
   If no roots are provided, auto-discover the current workspace, OpenClaw skill roots, Codex and Claude local skill roots, Codex plugin-cache skills, supported local workbench configuration surfaces, and project-level workbench surfaces such as repo `AGENTS.md`, `CLAUDE.md`, or selected `.claude/.codex` files.
2. Scan every discovered skill directory containing `SKILL.md`, plus recognized workbench surfaces such as local Codex and Claude configuration bundles and project-local agent configuration areas.
3. For each skill, score two separate layers:
   - capability risk: what the skill can access or execute
   - unsafe behavior: what the skill appears to do with sensitive data or hidden actions
4. Reuse the incremental cache when possible, and surface per-target diffs plus evidence type and confidence in the final report.
5. Generate `_yao_doctor_skill_reports/<timestamp>/report.html`, `report.json`, and `report.md`.
   Also update the stable entry:
   - full scans -> `_yao_doctor_skill_reports/full-library-latest/report.html`
   - changed-only scans -> `_yao_doctor_skill_reports/changed-only-latest/report.html`
6. Summarize the highest-severity findings first, with exact paths, lines, evidence type, confidence, and the reason a finding is merely risky, suspicious, unsafe, or critical.

## Security Principles

- Do not equate broad permissions with automatic compromise.
- Treat a skill as unsafe only when there is evidence of privacy theft, credential theft, stealthy exfiltration, deceptive behavior, remote execution, or persistence abuse.
- Distinguish capability from intent. A skill may be powerful without being malicious.
- Escalate hard when a sensitive source and an external sink appear in the same execution path or file.
- Favor precise path-level evidence over generic suspicion.
- Stay read-only unless the user explicitly authorizes destructive or quarantine actions.

## Outputs

Primary artifact:

- visual HTML security report with the fixed section order:
  - overview
  - data analysis
  - definitions
  - module guide
  - skill modules
  - footer credit

Current interactive contract:

- sticky top navigation
- Chinese default with English toggle
- linked type filters between data analysis and module list
- module cards with audit opinion, findings, and capability evidence
- stable latest report entry for in-app browsing and reuse

Per skill, include:

- absolute path
- declared skill name and one-line summary
- capability risk score and level
- unsafe behavior score and level
- final disposition: `safe`, `risky`, `suspicious`, `unsafe`, or `critical`
- top capabilities discovered
- concrete findings with file path, line, category, severity, rationale, and recommended action

## Resources

- [Security Principles](references/security-principles.md)
- [Detection Taxonomy](references/detection-taxonomy.md)
- [Report Blueprint](references/report-blueprint.md)
- [Report UI Contract](references/report-ui-contract.md)
- [Solution Architecture](reports/solution-architecture.md)
- `scripts/scan_security_skills.py`
- `scripts/render_security_report.py`
- `scripts/run_yao_doctor_skill.py`
- `scripts/validate_report_ui_contract.py`
- `evals/trigger_cases.json`
