---
name: doc-ears-audit
description: Unified EARS audit wrapper that runs validator then reviewer and produces a combined report for fixer consumption

metadata:
  tags:
    - sdd-workflow
    - quality-assurance
    - ears-audit
    - layer-3-artifact
    - shared-architecture
  custom_fields:
    layer: 3
    artifact_type: EARS
    architecture_approaches: [ai-agent-based]
    priority: primary
    development_status: active
    skill_category: quality-assurance
    upstream_artifacts: [EARS]
    downstream_artifacts: [Audit Report, Fix Cycle]
    version: "1.0"
    last_updated: "2026-02-26"
  versioning_policy: "tracks EARS-MVP-TEMPLATE schema_version"

---

# doc-ears-audit

## Purpose

Run a **single EARS audit workflow** that executes:

1. `doc-ears-validator` (structural/schema gate)
2. `doc-ears-reviewer` (semantic/content quality gate)

Then emit one **combined report** optimized for `doc-ears-fixer` input.

**Layer**: 3 (EARS Quality Gate Wrapper)

**Upstream**: EARS file(s)

**Downstream**:
- Combined Audit Report: `EARS-NN.A_audit_report_vNNN.md`
- Optional Fix Cycle trigger for `doc-ears-fixer`

---

## Why This Skill Exists

Use this wrapper to avoid user confusion between validator and reviewer while preserving separation of concerns.

| Concern | Owner Skill |
|---------|-------------|
| Schema/template compliance | `doc-ears-validator` |
| Content quality and testability | `doc-ears-reviewer` |
| Single user-facing audit command | `doc-ears-audit` |

---

## When to Use

Use `doc-ears-audit` when:
- You want one command for EARS quality checks
- You need a combined report for `doc-ears-fixer`
- You are running QA before BDD generation

Do NOT use when:
- EARS does not exist (use `doc-ears` / `doc-ears-autopilot` generation first)
- You only need one specific check domain (use validator or reviewer directly)

---

## Execution Contract

### Input
- EARS path (`docs/03_EARS/EARS-NN_*/...`)
- Optional: threshold (default review threshold: 90)

### Sequence (Mandatory)

```text
1) Run doc-ears-validator
2) Run doc-ears-reviewer
3) Normalize and merge findings
4) Write EARS-NN.A_audit_report_vNNN.md
5) If auto-fixable findings exist, hand off to doc-ears-fixer
```

### Combined Status Rules

- `PASS`: Validator PASS AND Reviewer score >= threshold AND no blocking issues
- `FAIL`: Validator FAIL OR Reviewer score < threshold OR blocking/manual-required issues present

---

## Combined Report Format (for doc-ears-fixer)

Output file: `EARS-NN.A_audit_report_vNNN.md`

Required sections:

1. `## Summary`
   - EARS ID, timestamp (EST), overall status
   - Validator status, reviewer score
2. `## Score Calculation (Deduction-Based)`
   - Formula: `100 - total_deductions`
   - Threshold comparison (`>=90` pass gate)
3. `## Validator Findings`
   - List by severity/code
4. `## Reviewer Findings`
   - List by severity/code
5. `## Coverage Findings`
   - EARS syntax compliance summary
   - Threshold quantification coverage summary
   - Traceability/tag coverage summary
6. `## Fix Queue for doc-ears-fixer`
   - `auto_fixable`
   - `manual_required`
   - `blocked`
7. `## Recommended Next Step`
   - `run doc-ears-fixer`
   - or `manual update required`

### Fix Queue Normalization

Each finding MUST include:
- `source`: `validator` | `reviewer`
- `code`: issue code
- `severity`: `error|warning|info`
- `file`: relative path
- `section`: heading/anchor if known
- `action_hint`: short imperative guidance
- `confidence`: `high|medium|manual-required`

---

## Hand-off Contract to doc-ears-fixer

`doc-ears-fixer` MUST accept combined audit report as equivalent upstream input:
- `EARS-NN.A_audit_report_vNNN.md` (preferred)
- `EARS-NN.R_review_report_vNNN.md` (legacy compatibility)

Precedence rule:
1. Select newest timestamp.
2. If timestamps are equal, prefer `.A_audit_report` over `.R_review_report`.

---

## Example Invocation

```bash
/doc-ears-audit docs/03_EARS/EARS-01_f1_iam/EARS-01_f1_iam.md
```

Expected outcome:
1. validator runs
2. reviewer runs
3. combined audit report generated
4. fixer can execute directly from combined report

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-02-26 | Initial EARS audit wrapper; validator→reviewer orchestration; combined report contract for fixer with `.A_` preferred and `.R_` legacy compatibility |

## Implementation Plan Consistency (IPLAN-004)

- Treat plan-derived outputs as valid source mode and verify intent preservation from implementation plan scope/objectives.
- Validate upstream autopilot precedence assumption: `--iplan > --ref > --prompt`.
- Flag objective/scope conflicts between plan context and artifact output as blocking issues requiring clarification.
- Do not introduce legacy fallback paths such as `docs-v2.0/00_REF`.

