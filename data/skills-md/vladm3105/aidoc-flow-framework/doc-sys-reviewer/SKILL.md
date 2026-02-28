---
name: doc-sys-reviewer
description: Comprehensive content review and quality assurance for SYS documents - validates system requirement completeness, ADR alignment, quality attribute coverage, and identifies issues requiring manual attention
metadata:
  tags:
    - sdd-workflow
    - quality-assurance
    - sys-review
    - layer-6-artifact
    - shared-architecture
  custom_fields:
    layer: 6
    artifact_type: SYS
    architecture_approaches: [ai-agent-based]
    priority: primary
    development_status: active
    skill_category: quality-assurance
    upstream_artifacts: [SYS]
    downstream_artifacts: []
    version: "1.6"
    last_updated: "2026-02-27"
  versioning_policy: "tracks SYS-MVP-TEMPLATE schema_version"
---

# doc-sys-reviewer

## Purpose

Comprehensive **content review and quality assurance** for System Requirements (SYS) documents. This skill performs deep content analysis beyond structural validation, checking requirement completeness, ADR alignment, quality attribute coverage, interface definitions, and identifying issues that require manual architectural review.

**Layer**: 6 (SYS Quality Assurance)

**Upstream**: SYS (from `doc-sys-autopilot` or `doc-sys`)

**Downstream**: None (final QA gate before REQ generation)

---

## When to Use This Skill

Use `doc-sys-reviewer` when:

- **After SYS Generation**: Run immediately after `doc-sys-autopilot` completes
- **Manual SYS Edits**: After making manual changes to SYS
- **Pre-REQ Check**: Before running `doc-req-autopilot`
- **Periodic Review**: Regular quality checks on existing SYS
- **Architecture Reviews**: During system design reviews

**Do NOT use when**:
- SYS does not exist yet (use `doc-sys` or `doc-sys-autopilot` first)
- Need structural/schema validation only (use `doc-sys-validator`)
- Generating new SYS content (use `doc-sys`)

---

## Skill vs Validator: Key Differences

| Aspect | `doc-sys-validator` | `doc-sys-reviewer` |
|--------|---------------------|-------------------|
| **Focus** | Schema compliance, REQ-Ready score | Content quality, ADR alignment |
| **Checks** | Required sections, format | Quality attributes, interface completeness |
| **Auto-Fix** | Structural issues only | Content issues (links, formatting) |
| **Output** | REQ-Ready score (numeric) | Review score + issue list |
| **Phase** | Phase 4 (Validation) | Phase 5 (Final Review) |
| **Blocking** | REQ-Ready < threshold blocks | Review score < threshold flags |

---

## Review Workflow

```mermaid
flowchart TD
    A[Input: SYS Path] --> B[Load SYS Files]
    B --> C{Single or Multiple?}

    C -->|Multiple| D[Load All SYS Files]
    C -->|Single| E[Load Single File]

    D --> F[Run Review Checks]
    E --> F

    subgraph Review["Review Checks"]
        F --> G[1. Functional Requirement Completeness]
        G --> H[2. ADR Alignment]
        H --> I[3. Quality Attribute Coverage]
        I --> J[4. Interface Definition Completeness]
      J --> J2[4a. System Diagram Contract Compliance]
      J2 --> K[5. Constraint Validation]
        K --> L[6. Placeholder Detection]
        L --> M[7. Naming Compliance]
        M --> N2[8. Upstream Drift Detection]
    end

    N2 --> N{Issues Found?}
    N -->|Yes| O[Categorize Issues]
    O --> P{Auto-Fixable?}
    P -->|Yes| Q[Apply Auto-Fixes]
    Q --> R[Re-run Affected Checks]
    P -->|No| S[Flag for Manual Review]
    R --> N
    S --> T[Generate Report]
    N -->|No| T
    T --> U[Calculate Review Score]
    U --> V{Score >= Threshold?}
    V -->|Yes| W[PASS]
    V -->|No| X[FAIL with Details]
```

---

## Review Checks

### 0. Structure Compliance (BLOCKING)

Validates SYS follows the mandatory nested folder rule.

**Nested Folder Rule**: ALL SYS documents MUST be in nested folders.

**Required Structure**:

| SYS Type | Required Location |
|----------|-------------------|
| Monolithic | `docs/06_SYS/SYS-NN_{slug}/SYS-NN_{slug}.md` |

**Error Codes**:

| Code | Severity | Description |
|------|----------|-------------|
| REV-STR001 | Error | SYS not in nested folder (BLOCKING) |
| REV-STR002 | Error | Folder name doesn't match SYS ID |
| REV-STR003 | Warning | File name doesn't match folder name |

**This check is BLOCKING** - SYS must pass structure validation before other checks proceed.

---

### 1. Functional Requirement Completeness

Validates all functional requirements are complete.

**Scope**:
- Each requirement has description
- Acceptance criteria defined
- Priority assigned
- Dependencies documented
- Rationale provided

**Error Codes**:

| Code | Severity | Description |
|------|----------|-------------|
| REV-FR001 | Error | Requirement missing description |
| REV-FR002 | Error | No acceptance criteria |
| REV-FR003 | Warning | Priority not assigned |
| REV-FR004 | Info | Dependencies not documented |
| REV-FR005 | Info | Rationale missing |

---

### 2. ADR Alignment

Validates SYS requirements trace to ADR decisions.

**Scope**:
- Requirements implement ADR decisions
- No conflicting requirements
- Technology choices consistent
- Architectural constraints honored

**Error Codes**:

| Code | Severity | Description |
|------|----------|-------------|
| REV-AA001 | Error | Requirement conflicts with ADR decision |
| REV-AA002 | Warning | Technology choice not in ADR |
| REV-AA003 | Warning | Requirement without ADR traceability |
| REV-AA004 | Info | Architectural constraint may be violated |

---

### 3. Quality Attribute Coverage

Validates non-functional requirements coverage.

**Scope**:
- Performance requirements defined
- Security requirements present
- Reliability/availability specified
- Scalability addressed
- Maintainability considered

**Error Codes**:

| Code | Severity | Description |
|------|----------|-------------|
| REV-QA001 | Error | No performance requirements |
| REV-QA002 | Error | Security requirements missing |
| REV-QA003 | Warning | Availability not specified |
| REV-QA004 | Warning | Scalability not addressed |
| REV-QA005 | Info | Maintainability not considered |

---

### 4. Interface Definition Completeness

Validates system interfaces are well-defined.

**Scope**:
- External interfaces documented
- Internal interfaces defined
- Data formats specified
- Protocols identified
- Error handling defined

**Error Codes**:

| Code | Severity | Description |
|------|----------|-------------|
| REV-IF001 | Error | External interface not documented |
| REV-IF002 | Warning | Data format not specified |
| REV-IF003 | Warning | Protocol not identified |
| REV-IF004 | Info | Error handling not defined |

### 4a. System Diagram Contract Compliance

Validates SYS bridge requirements defined by `ai_dev_ssd_flow/DIAGRAM_STANDARDS.md` and SYS quality-gate contracts.

**Scope**:
- Required `System Diagram Contract` subsection exists
- Required fields present: `downstream_c4_l4_owner`, `required_sequence_paths`, `trust_boundaries`
- Required tags present for bridge ownership: `@diagram: c4-l4-ownership`, `@diagram: sequence-l4`
- SYS contract references remain consistent with downstream SPEC ownership location

**Error Codes**:

| Code | Severity | Description |
|------|----------|-------------|
| REV-DC001 | Error | Missing `System Diagram Contract` section |
| REV-DC002 | Error | Missing required bridge fields (`downstream_c4_l4_owner`, `required_sequence_paths`, or `trust_boundaries`) |
| REV-DC003 | Error | Missing required SYS bridge tags (`@diagram: c4-l4-ownership`, `@diagram: sequence-l4`) |
| REV-DC004 | Warning | Downstream SPEC ownership reference appears incomplete or inconsistent |

---

### 5. Constraint Validation

Validates system constraints are reasonable.

**Scope**:
- Resource constraints realistic
- Time constraints achievable
- Budget constraints considered
- Technology constraints compatible

**Error Codes**:

| Code | Severity | Description |
|------|----------|-------------|
| REV-CV001 | Warning | Resource constraint may be unrealistic |
| REV-CV002 | Warning | Time constraint may be unachievable |
| REV-CV003 | Info | Budget constraint not documented |
| REV-CV004 | Warning | Technology constraint may be incompatible |

---

### 6. Placeholder Detection

Identifies incomplete content requiring replacement.

**Error Codes**:

| Code | Severity | Description |
|------|----------|-------------|
| REV-P001 | Error | [TODO] placeholder found |
| REV-P002 | Error | [TBD] placeholder found |
| REV-P003 | Warning | Template value not replaced |

---

### 7. Naming Compliance

Validates element IDs follow `doc-naming` standards.

**Scope**:
- Element IDs use `SYS.NN.TT.SS` format
- Element type codes valid for SYS (01, 05, 17, 18, 19, 20, 21)
- No legacy patterns (SR-NNN, SYS-NNN)

**Error Codes**:

| Code | Severity | Description |
|------|----------|-------------|
| REV-N001 | Error | Invalid element ID format |
| REV-N002 | Error | Element type code not valid for SYS |
| REV-N003 | Error | Legacy pattern detected |

---

### 8. Upstream Drift Detection (Mandatory Cache)

Detects when upstream ADR documents have been modified after the SYS was created or last updated.

**The drift cache is mandatory.** All drift detection operations require cache initialization and maintenance.

**Purpose**: Identifies stale SYS content that may not reflect current architecture decisions. When ADR documents change, the SYS may need updates to maintain alignment with architectural decisions.

**Upstream Documents**:
- **ADR documents**: Architecture Decision Records that SYS requirements must implement

**Scope**:
- `@adr:` tag targets (ADR document references)
- Traceability section upstream artifact links
- Any markdown links to `../05_ADR/`
- Technology choice references that trace to ADR decisions

---

#### Drift Cache File (MANDATORY)

Location: `docs/06_SYS/.drift_cache.json`

**Schema**:

```json
{
  "cache_version": "1.0",
  "created": "2026-02-10T17:00:00",
  "last_checked": "2026-02-10T17:00:00",
  "sys_documents": {
    "SYS-01_f1_iam.md": {
      "sys_hash": "sha256:abc123...",
      "last_updated": "2026-02-10T17:00:00",
      "upstream_refs": {
        "ADR-01_authentication_strategy.md": {
          "path": "../../05_ADR/ADR-01_authentication_strategy.md",
          "hash": "sha256:def456...",
          "checked": "2026-02-10T17:00:00",
          "status": "current"
        },
        "ADR-05_data_storage.md": {
          "path": "../../05_ADR/ADR-05_data_storage.md",
          "hash": "sha256:ghi789...",
          "checked": "2026-02-10T17:00:00",
          "status": "current"
        }
      }
    }
  }
}
```

**Cache Status Values**:
- `current`: Hash matches, no drift detected
- `drifted`: Hash mismatch, upstream modified
- `missing`: Upstream file not found
- `new`: New reference, not yet cached

---

#### Three-Phase Detection Algorithm

**Phase 1: Cache Initialization**

```
1. Check if .drift_cache.json exists
   - If missing → Create new cache file
   - If exists → Load and validate schema

2. For each SYS document:
   a. Extract all upstream references:
      - @adr: tags → [ADR document ID]
      - Links to ../05_ADR/ → [path]
      - Traceability table upstream artifacts → [path]
      - Technology choices → [related ADR]
   b. Resolve paths to absolute file paths
   c. Initialize upstream_refs entries if missing
```

**Phase 2: Hash Comparison**

```
1. For each upstream reference in cache:
   a. Read upstream file content
   b. Compute SHA-256 hash
   c. Compare to cached hash:
      - Match → status = "current"
      - Mismatch → status = "drifted", flag REV-D002
      - File missing → status = "missing", flag REV-D006

2. Detect new references not in cache:
   a. Add to upstream_refs with status = "new"
   b. Compute initial hash
```

**Phase 3: Cache Update**

```
1. Update last_checked timestamp
2. For each drifted reference:
   a. Store new hash
   b. Update checked timestamp
   c. Preserve previous hash for delta analysis
3. Write updated cache to disk
4. Generate drift report
```

---

#### Hash Calculation (MANDATORY BASH EXECUTION)

**CRITICAL**: You MUST execute actual bash commands to compute hashes. DO NOT write placeholder values.

**Compute File Hash**:

```bash
sha256sum <file_path> | cut -d' ' -f1
```

Store result as: `"hash": "sha256:<64_hex_characters>"`

**REJECTED VALUES** (re-compute immediately):
- `sha256:verified_no_drift`
- `sha256:pending_verification`
- Any value where hex portion != 64 characters

**Section Hash** (for anchor-specific tracking):

```bash
sed -n '/^## Section Name/,/^## /p' <file_path> | head -n -1 | sha256sum | cut -d' ' -f1
```

**Verification**:

```bash
grep -oP '"hash":\s*"sha256:[0-9a-f]{64}"' .drift_cache.json
```

---

#### Error Codes

| Code | Severity | Description |
|------|----------|-------------|
| REV-D001 | Warning | Upstream ADR modified after SYS creation |
| REV-D002 | Warning | Referenced ADR decision section has changed (hash mismatch) |
| REV-D003 | Info | Upstream ADR version incremented |
| REV-D004 | Info | New content added to upstream ADR |
| REV-D005 | Error | Critical ADR substantially modified (>20% change) |
| REV-D006 | Error | Drift cache missing or corrupted - requires initialization |
| REV-D009 | Error | Invalid hash placeholder detected (`verified_no_drift`, `pending_verification`) |

---

#### Report Output

```markdown
## Upstream Drift Analysis

**Cache Status**: Loaded from docs/06_SYS/.drift_cache.json (last checked: 2026-02-10T17:00:00)

| Upstream Document | SYS Reference | Cached Hash | Current Hash | Status | Severity |
|-------------------|---------------|-------------|--------------|--------|----------|
| ADR-01_authentication_strategy.md | @adr Decision | sha256:abc123... | sha256:xyz789... | DRIFTED | Warning |
| ADR-05_data_storage.md | Traceability | sha256:def456... | sha256:def456... | Current | - |

**Drift Summary**:
- Total upstream references: 2
- Current: 1
- Drifted: 1
- Missing: 0

**Recommendation**: Review upstream ADR changes and update SYS if architecture decisions have changed.
```

---

#### Auto-Actions

- Initialize `.drift_cache.json` if missing (mandatory)
- Update cache with current hashes after review
- Add `[DRIFT]` marker to affected @adr tags (optional)
- Generate drift summary in review report
- Preserve hash history for trend analysis

---

#### Configuration

| Setting | Default | Description |
|---------|---------|-------------|
| `cache_enabled` | true | **Mandatory** - Cache must be enabled |
| `drift_threshold_days` | 7 | Days before drift becomes Warning |
| `critical_threshold_days` | 30 | Days before drift becomes Error |
| `hash_algorithm` | SHA-256 | Hash algorithm for content comparison |
| `tracked_patterns` | `@adr:` | Patterns to track for drift |

---

## Review Score Calculation

**Scoring Formula**:

| Category | Weight | Calculation |
|----------|--------|-------------|
| Functional Requirement Completeness | 24% | (complete / total_reqs) × 24 |
| ADR Alignment | 19% | (aligned / total_reqs) × 19 |
| Quality Attribute Coverage | 19% | (covered / required_attrs) × 19 |
| Interface Definition Completeness | 14% | (complete_interfaces / total) × 14 |
| Constraint Validation | 5% | (valid_constraints / total) × 5 |
| Placeholder Detection | 5% | (no_placeholders ? 5 : 5 - count) |
| Naming Compliance | 9% | (valid_ids / total_ids) × 9 |
| Upstream Drift | 5% | (fresh_refs / total_refs) × 5 |

**Total**: Sum of all categories (max 100)

**Thresholds**:
- **PASS**: ≥ 90
- **WARNING**: 80-89
- **FAIL**: < 80

---

## Command Usage

```bash
# Review specific SYS
/doc-sys-reviewer SYS-01

# Review SYS by path
/doc-sys-reviewer docs/06_SYS/SYS-01_f1_iam.md

# Review all SYS
/doc-sys-reviewer all
```

---

## Output Report

Review reports are stored alongside the reviewed document per project standards.

**Nested Folder Rule**: ALL SYS use nested folders (`SYS-NN_{slug}/`) regardless of size. This ensures review reports, fix reports, and drift cache files are organized with their parent document.

**File Naming**: `SYS-NN.R_review_report_vNNN.md`

**Location**: Inside the SYS nested folder: `docs/06_SYS/SYS-NN_{slug}/`

### Versioning Rules

1. **First Review**: Creates `SYS-NN.R_review_report_v001.md`
2. **Subsequent Reviews**: Auto-increments version (v002, v003, etc.)
3. **Same-Day Reviews**: Each review gets unique version number

**Version Detection**: Scans folder for existing `SYS-NN.R_review_report_v*.md` files and increments.

**Example**:

```
docs/06_SYS/SYS-01_f1_iam/
├── SYS-01_f1_iam.md
├── SYS-01.R_review_report_v001.md    # First review
├── SYS-01.R_review_report_v002.md    # After fixes
└── .drift_cache.json
```

### Delta Reporting

When previous reviews exist, include score comparison in the report.

See `REVIEW_DOCUMENT_STANDARDS.md` for complete versioning requirements.

---

## Integration with doc-sys-autopilot

This skill is invoked during Phase 5 of `doc-sys-autopilot`:

```mermaid
flowchart LR
    A[Phase 4: Validation] --> B[Phase 5: Final Review]
    B --> C{doc-sys-reviewer}
    C --> D[Phase 6: Continue]
```

---

## Related Skills

| Skill | Relationship |
|-------|--------------|
| `doc-naming` | Naming standards for Check #7 |
| `doc-sys-audit` | Wraps validator + reviewer into combined audit report |
| `doc-sys-autopilot` | Invokes this skill in Phase 5 |
| `doc-sys-validator` | Structural validation (Phase 4) |
| `doc-sys-fixer` | Applies fixes based on review findings |
| `doc-sys` | SYS creation rules |
| `doc-adr-reviewer` | Upstream QA |
| `doc-req-autopilot` | Downstream consumer |

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.6 | 2026-02-27 | Migrated frontmatter to `metadata`; normalized SYS report location paths to `docs/06_SYS`; documented relationship with `doc-sys-audit` wrapper |
| 1.4 | 2026-02-11 | Added Check #0: Structure Compliance (BLOCKING) - validates SYS in nested folders; REV-STR001-STR003 error codes; Must pass before other checks proceed |
| 1.3 | 2026-02-10 | **Mandatory Drift Cache**: Cache now required for all drift detection; Three-phase detection algorithm; SHA-256 hash calculation with Python implementation; REV-D006 error code for missing/corrupted cache; Enhanced report output with cache status; cache_enabled=true is mandatory |
| 1.2 | 2026-02-10 | Added Check #8: Upstream Drift Detection - detects when ADR documents modified after SYS creation; REV-D001-D005 error codes; drift cache support; configurable thresholds; Added doc-sys-fixer to Related Skills |
| 1.1 | 2026-02-10 | Added review versioning support (_vNNN pattern); Delta reporting for score comparison |
| 1.0 | 2026-02-10 | Initial skill creation with 7 review checks; ADR alignment; Quality attribute coverage; Interface completeness |
