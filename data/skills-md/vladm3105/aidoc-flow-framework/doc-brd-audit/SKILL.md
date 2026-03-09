---
name: doc-brd-audit
description: Manual BRD audit skill that runs shell validation scripts, adds Claude content review, and produces a combined report for doc-brd-fixer

metadata:
  tags:
    - sdd-workflow
    - quality-assurance
    - brd-audit
    - layer-1-artifact
    - shared-architecture
  custom_fields:
    layer: 1
    artifact_type: BRD
    architecture_approaches: [ai-agent-based]
    priority: primary
    development_status: active
    skill_category: quality-assurance
    upstream_artifacts: [BRD]
    downstream_artifacts: [Audit Report, Fix Cycle]
    version: "2.4"
    last_updated: "2026-03-05"
  versioning_policy: "tracks BRD-MVP-TEMPLATE schema_version"

---

# doc-brd-audit

> **MANUAL USE ONLY** - This skill is for interactive use, not pre-commit.
> Pre-commit runs shell scripts directly without Claude.

## Purpose

Run a **unified BRD audit workflow** that combines shell script validation and Claude content review into a single pass, producing one **combined report** optimized for `doc-brd-fixer` input.

**Architecture**: Shell scripts for structural validation + Claude for content quality review.

**Layer**: 1 (BRD Quality Gate Wrapper)

**Upstream**: BRD file(s)

**Downstream**:
- Combined Audit Report: `BRD-NN.A_audit_report_vNNN.md`
- Optional Fix Cycle trigger for `doc-brd-fixer`

---

## Why This Skill Exists

The 2-skill model (`doc-brd-audit` + `doc-brd-fixer`) simplifies the BRD quality workflow.

| Concern | Owner Skill |
|---------|-------------|
| All validation + scoring | `doc-brd-audit` (this skill) |
| Apply fixes from audit report | `doc-brd-fixer` |

---

## Fresh Audit Policy (MANDATORY)

**ALWAYS run the audit from scratch.** Do NOT:
- Reference previous audit reports for scoring decisions
- Skip validation steps based on drift cache history
- Assume compliance from prior fix history
- Use cached results from previous runs

**ALWAYS**:
- Run all validation scripts fresh every time
- Re-check all structure/schema compliance
- Re-compute PRD-ready score independently
- Generate a new audit report with incremented version

---

## Report Cleanup Policy (MANDATORY)

**After generating a new audit report, delete all previous reports.** Old reports serve no purpose since:
- Fresh Audit Policy means old reports are never reused for scoring
- Only the latest report is used by `doc-brd-fixer`
- Multiple old reports clutter the BRD folder

### Cleanup Rules

| File Pattern | Action | Reason |
|--------------|--------|--------|
| `BRD-NN.A_audit_report_v*.md` (older versions) | **DELETE** | Superseded by new audit |
| `BRD-NN.R_review_report_v*.md` (legacy) | **DELETE** | Deprecated format, superseded |
| `BRD-NN.F_fix_report_v*.md` | **KEEP** | Fix history may be useful for tracking |
| `.drift_cache.json` | **KEEP** | Tracks review history metadata |

### Cleanup Execution

After writing the new audit report, run:

```bash
# In the BRD folder (e.g., docs/01_BRD/BRD-50_octo_agent_orchestration/)
BRD_FOLDER="$1"
NEW_REPORT="$2"  # e.g., BRD-50.A_audit_report_v012.md

# Delete old audit reports (keep only the new one)
find "${BRD_FOLDER}" -name "BRD-*.A_audit_report_v*.md" ! -name "$(basename ${NEW_REPORT})" -delete

# Delete legacy review reports (deprecated format)
find "${BRD_FOLDER}" -name "BRD-*.R_review_report_v*.md" -delete
```

### What Gets Kept

After cleanup, the BRD folder should contain:

```
docs/01_BRD/BRD-NN_{slug}/
├── BRD-NN_{slug}.md              # Main BRD document
├── BRD-NN.A_audit_report_vNNN.md # Latest audit report (ONLY ONE)
├── BRD-NN.F_fix_report_v*.md     # Fix reports (kept for history)
└── .drift_cache.json             # Drift detection cache
```

### Cleanup Confirmation

The audit report should include a cleanup summary:

```markdown
## Cleanup Summary
- Deleted: 3 old audit reports (v009, v010, v011)
- Deleted: 4 legacy review reports
- Kept: 2 fix reports
```

---

## When to Use

Use `doc-brd-audit` when:
- You want one command for BRD quality checks
- You need a combined report for `doc-brd-fixer`
- You are running CI/manual QA before PRD generation

Do NOT use when:
- BRD does not exist (use `doc-brd` / `doc-brd-autopilot` generation first)
- You only need one specific check domain (use validator or reviewer directly)

---

## Execution Contract

### Input
- BRD path (`docs/01_BRD/BRD-NN_*/...`)
- Optional: threshold (default review threshold: 90)

### Sequence (Mandatory)

```text
1) Run pre-commit validation scripts (see Script-Based Validation)
2) Parse script output for findings
3) Run content quality review (Claude analysis)
4) Normalize and merge all findings
5) Write BRD-NN.A_audit_report_vNNN.md
6) If auto-fixable findings exist, hand off to doc-brd-fixer
```

---

## Script-Based Validation (Pre-commit Integration)

This skill **MUST** invoke the same validation scripts used by pre-commit hooks. This ensures consistency between CI/CD and manual audit runs.

### Required Scripts

| Script | Purpose | Exit Codes |
|--------|---------|------------|
| `validate_brd_wrapper.sh` | Core + advisory validation wrapper | 0=pass, 2=core fail, 1=advisory fail |
| `validate_standardized_element_codes.py` | Element ID format validation | 0=pass, non-zero=fail |
| `detect_legacy_element_ids.py` | Legacy pattern detection | 0=pass, non-zero=warnings |

### Script Execution

```bash
# From repository root
REPO_ROOT="$(git rev-parse --show-toplevel)"
BRD_PATH="$1"  # e.g., docs/01_BRD/BRD-01_platform

# 1. Run core wrapper (includes structural + quality gate)
bash "${REPO_ROOT}/ai_dev_ssd_flow/01_BRD/scripts/validate_brd_wrapper.sh" "${BRD_PATH}" 2>&1

# 2. Run standardized element codes (strict mode)
python3 "${REPO_ROOT}/ai_dev_ssd_flow/scripts/validate_standardized_element_codes.py" "${BRD_PATH}" --strict 2>&1

# 3. Run legacy pattern detection
python3 "${REPO_ROOT}/ai_dev_ssd_flow/scripts/detect_legacy_element_ids.py" "${BRD_PATH}" --summary 2>&1
```

### Script Output Parsing

The skill MUST parse script output to extract findings:

| Output Pattern | Finding Type | Severity |
|----------------|--------------|----------|
| `[FAIL]` | Blocking issue | error |
| `[WARN]` | Non-blocking issue | warning |
| `[PASS]` | Check passed | info |
| `ERROR:` | Script error | error |
| Line with file path + issue | File-specific finding | varies |

### Validation Tiers (from validate_brd_wrapper.sh)

| Tier | Checks | Blocking |
|------|--------|----------|
| **Tier 1 (CORE)** | Standardized element codes, BRD structural validation, BRD quality gate | Yes |
| **Tier 2 (ADVISORY)** | Metadata validation, Link validation, Forward reference validation, Diagram consistency | No (default) |

### Pre-commit vs Skill Separation

**Pre-commit hooks run shell scripts directly** (no Claude):

```yaml
# .pre-commit-config.yaml - runs on every commit
- id: brd-core-wrapper           # validate_brd_wrapper.sh
- id: brd-standardized-element-codes  # validate_standardized_element_codes.py
- id: brd-legacy-patterns        # detect_legacy_element_ids.py
```

**This skill is for manual/interactive use**:

```bash
# Manual invocation for full audit + report generation
/doc-brd-audit docs/01_BRD/BRD-01_platform
```

**Flow**:
```
Automatic (pre-commit):
  git commit → shell scripts → pass/fail

Manual (skill):
  /doc-brd-audit → shell scripts → Claude review → audit report
```

### Combined Status Rules

- `PASS`: Script validation PASS AND Claude review score >= threshold AND no blocking issues
- `FAIL`: Script validation FAIL OR Claude review score < threshold OR blocking/manual-required issues present

**Diagram Contract Gate (ADVISORY for BRD)**:
- BRD diagram findings are recorded as non-blocking by default.
- Recommended tags: `@diagram: c4-l1` and `@diagram: dfd-l0`
- If sequence diagram exists, recommend one sequence tag (`@diagram: sequence-sync|sequence-async|sequence-error`)
- Recommended intent fields: `diagram_type`, `level`, `scope_boundary`, `upstream_refs`, `downstream_refs`
- Optional strict mode only when explicitly enabled (e.g., `audit_strict_diagrams: true`).

---

## Metadata Validation

The audit MUST validate BRD frontmatter metadata compliance.

### Required Metadata Fields

| Field | Type | Required | Valid Values |
|-------|------|----------|--------------|
| `document_type` | string | Yes | `brd-document` |
| `artifact_type` | string | Yes | `BRD` |
| `layer` | integer | Yes | `1` |
| `deliverable_type` | string | Yes | `code`, `document`, `ux`, `risk`, `process` |

### Metadata Validation Rules

**VALID-M001: deliverable_type Present**
- Severity: Error
- Check: `deliverable_type` exists in `custom_fields`
- Fix: Add `deliverable_type: code` (default)

**VALID-M002: deliverable_type Valid Value**
- Severity: Error
- Check: `deliverable_type` is one of: `code`, `document`, `ux`, `risk`, `process`
- Fix: Reset to `code` (default) or suggest based on BRD content

**VALID-M003: document_type Correct for Instance**
- Severity: Error
- Check: `document_type` is `brd-document` (not `template`)
- Fix: Change to `brd-document`

### Metadata Validation Detection

```python
def validate_deliverable_type(frontmatter: dict) -> list[Finding]:
    """Validate deliverable_type metadata field."""
    findings = []
    custom_fields = frontmatter.get('custom_fields', {})

    # Check M001: deliverable_type present
    if 'deliverable_type' not in custom_fields:
        findings.append({
            'code': 'VALID-M001',
            'severity': 'error',
            'message': 'Missing deliverable_type in custom_fields',
            'fix_action': 'Add deliverable_type: code',
            'confidence': 'auto-safe'
        })
        return findings

    # Check M002: valid value
    deliverable_type = custom_fields['deliverable_type']
    valid_values = ['code', 'document', 'ux', 'risk', 'process']

    if deliverable_type not in valid_values:
        findings.append({
            'code': 'VALID-M002',
            'severity': 'error',
            'message': f'Invalid deliverable_type: {deliverable_type}',
            'valid_values': valid_values,
            'fix_action': f'Change to one of: {", ".join(valid_values)}',
            'confidence': 'auto-assisted'  # May need content analysis
        })

    return findings
```

---

## Combined Report Format (for doc-brd-fixer)

Output file: `BRD-NN.A_audit_report_vNNN.md`

Required sections:

1. `## Summary`
   - BRD ID, timestamp (EST), overall status
   - Script validation status, Claude review score
2. `## Score Calculation (Deduction-Based)`
   - Formula: `100 - total_deductions`
   - Deductions grouped by: contamination (max 50), FR completeness (max 30), structure/quality (max 20)
   - Threshold comparison (`>=90` pass gate)
3. `## Metadata Validation Findings`
   - deliverable_type presence and validity
   - document_type correctness
   - Other required metadata fields
4. `## Script Findings`
   - Findings from shell validation scripts
   - List by severity/code
5. `## Claude Review Findings`
   - Findings from Claude content quality review
   - List by severity/code
6. `## Diagram Contract Findings`
   - Required BRD tags status (`c4-l1`, `dfd-l0`)
   - Sequence contract status when sequence is present
   - Intent header completeness status
7. `## Fix Queue for doc-brd-fixer`
   - `auto_fixable`
   - `manual_required`
   - `blocked`
8. `## Recommended Next Step`
   - `run doc-brd-fixer`
   - or `manual update required`

### Fix Queue Normalization

Each finding MUST include:
- `source`: `script` | `claude` (script = shell validation, claude = content review)
- `code`: issue code
- `severity`: `error|warning|info`
- `file`: relative path
- `section`: heading/anchor if known
- `action_hint`: short imperative guidance
- `confidence`: `high|medium|manual-required`

---

## Hand-off Contract to doc-brd-fixer

`doc-brd-fixer` MUST accept combined audit report as equivalent upstream input:
- `BRD-NN.A_audit_report_vNNN.md`
- `BRD-NN.R_review_report_vNNN.md` (legacy compatibility)

If both exist, fixer should prefer latest timestamp.

---

## Example Invocation

```bash
/doc-brd-audit docs/01_BRD/BRD-01_platform/BRD-01_platform.md
```

Expected outcome:
1. Shell validation scripts run (same as pre-commit)
2. Claude content quality review runs
3. Combined audit report generated: `BRD-01.A_audit_report_vNNN.md`
4. Fixer can execute directly from combined report

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 2.4 | 2026-03-05 | **Metadata Validation**: Added validation for `deliverable_type` metadata field (VALID-M001, VALID-M002, VALID-M003); Validates presence, valid values (`code`, `document`, `ux`, `risk`, `process`), and `document_type` correctness; Added "Metadata Validation Findings" section to combined report |
| 2.3 | 2026-03-05 | **Report Cleanup Policy**: Added mandatory cleanup of old audit reports after generating new one; Deletes previous `BRD-NN.A_audit_report_v*.md` and legacy `BRD-NN.R_review_report_v*.md` files; Keeps fix reports and drift cache; Added cleanup summary section to audit report |
| 2.2 | 2026-03-05 | **Shell-first approach**: Pre-commit runs shell scripts directly (not Claude); Skill is for manual use only; Skill invokes same scripts then adds Claude review; Removed obsolete `doc-brd-validator`/`doc-brd-reviewer` references |
| 2.1 | 2026-03-01 | Added Fresh Audit Policy (MANDATORY); All validation and scoring unified in this skill |
| 1.3 | 2026-02-26 | Added advisory BRD C4/DFD/sequence diagram contract checks and required `Diagram Contract Findings` section in combined audit reports |
| 1.2 | 2026-02-26 | Initial audit wrapper; combined report contract for fixer |
