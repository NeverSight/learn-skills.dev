---
name: doc-adr-fixer
description: Automated fix skill that reads audit/review reports and applies fixes to ADR documents - handles broken links, element IDs, missing files, and iterative improvement
metadata:
  tags:
    - sdd-workflow
    - quality-assurance
    - adr-fix
    - layer-5-artifact
    - shared-architecture
  custom_fields:
    layer: 5
    artifact_type: ADR
    architecture_approaches: [ai-agent-based]
    priority: primary
    development_status: active
    skill_category: quality-assurance
    upstream_artifacts: [ADR, Audit Report, Review Report, BDD, BRD]
    downstream_artifacts: [Fixed ADR, Fix Report]
    version: "2.3"
    last_updated: "2026-02-27"
  versioning_policy: "tracks ADR-MVP-TEMPLATE schema_version"
---

# doc-adr-fixer

## Purpose

Automated **fix skill** that reads the latest audit/review report and applies fixes to ADR (Architecture Decision Record) documents. This skill bridges the gap between `doc-adr-reviewer`/`doc-adr-audit` (which identify issues) and the corrected ADR, enabling iterative improvement cycles.

**Layer**: 5 (ADR Quality Improvement)

**Upstream**: ADR document, Audit/Review Report (`ADR-NN.A_audit_report_vNNN.md` preferred, `ADR-NN.R_review_report_vNNN.md` legacy), BDD (for behavior alignment), BRD (for topic alignment)

**Downstream**: Fixed ADR, Fix Report (`ADR-NN.F_fix_report_vNNN.md`)

---

## When to Use This Skill

Use `doc-adr-fixer` when:

- **After Review**: Run after `doc-adr-reviewer` identifies issues
- **Iterative Improvement**: Part of Review -> Fix -> Review cycle
- **Automated Pipeline**: CI/CD integration for quality gates
- **Batch Fixes**: Apply fixes to multiple ADRs based on review reports

**Do NOT use when**:
- No audit/review report exists (run `doc-adr-audit` or `doc-adr-reviewer` first)
- Creating new ADR (use `doc-adr` or `doc-adr-autopilot`)
- Only need validation (use `doc-adr-validator`)

---

## Skill Dependencies

| Skill | Purpose | When Used |
|-------|---------|-----------|
| `doc-adr-audit` | Preferred source of normalized findings | Input (reads audit report) |
| `doc-adr-reviewer` | Legacy/alternate source of issues to fix | Input (reads review report) |
| `doc-naming` | Element ID standards | Fix element IDs |
| `doc-adr` | ADR creation rules | Create missing sections |
| `doc-bdd` | BDD alignment reference | Verify behavior traceability |

---

## Workflow Overview

```mermaid
flowchart TD
  A[Input: ADR Path] --> B[Find Latest Audit/Review Report]
  B --> C{Report Found?}
  C -->|No| D[Run doc-adr-audit or doc-adr-reviewer First]
  C -->|Yes| E[Parse Report]

    E --> F[Categorize Issues]

    subgraph FixPhases["Fix Phases"]
        F --> F0[Phase 0: Fix Structure Violations]
        F0 --> G[Phase 1: Create Missing Files]
        G --> H[Phase 2: Fix Broken Links]
        H --> I[Phase 3: Fix Element IDs]
        I --> J[Phase 4: Fix Content Issues]
        J --> K[Phase 5: Update References]
        K --> K2[Phase 6: Handle Upstream Drift]
    end

    K2 --> L[Write Fixed ADR]
    L --> M[Generate Fix Report]
    M --> N{Re-run Review?}
    N -->|Yes| O[Invoke doc-adr-reviewer]
    O --> P{Score >= Threshold?}
    P -->|No, iterations < max| F
    P -->|Yes| Q[COMPLETE]
    N -->|No| Q
```

---

## Fix Phases

### Phase 0: Fix Structure Violations (CRITICAL)

Fixes ADR documents that are not in nested folders. This phase runs FIRST because all subsequent phases depend on correct folder structure.

**Nested Folder Rule**: ALL ADR documents MUST be in nested folders regardless of document size.

**Required Structure**:
| ADR Type | Required Location |
|----------|-------------------|
| Monolithic | `docs/05_ADR/ADR-NN_{slug}/ADR-NN_{slug}.md` |

**Fix Actions**:

| Issue Code | Issue | Fix Action |
|------------|-------|------------|
| REV-STR001 | ADR not in nested folder | Create folder, move file, update all links |
| REV-STR002 | ADR folder name doesn't match ADR ID | Rename folder to match |
| REV-STR003 | Monolithic ADR >25KB should be sectioned | Flag for manual review |

**Structure Fix Workflow**:

```python
def fix_adr_structure(adr_path: str) -> list[Fix]:
    """Fix ADR structure violations."""
    fixes = []

    filename = os.path.basename(adr_path)
    parent_folder = os.path.dirname(adr_path)

    # Extract ADR ID and slug from filename
    match = re.match(r'ADR-(\d+)_([^/]+)\.md', filename)
    if not match:
        return []  # Cannot auto-fix invalid filename

    adr_id = match.group(1)
    slug = match.group(2)
    expected_folder = f"ADR-{adr_id}_{slug}"

    # Check if already in nested folder
    if os.path.basename(parent_folder) != expected_folder:
        # Create nested folder
        new_folder = os.path.join(os.path.dirname(parent_folder), expected_folder)
        os.makedirs(new_folder, exist_ok=True)

        # Move file
        new_path = os.path.join(new_folder, filename)
        shutil.move(adr_path, new_path)
        fixes.append(f"Moved {adr_path} to {new_path}")

        # Update upstream links in moved file
        content = Path(new_path).read_text()
        updated_content = content.replace('../04_BDD/', '../../04_BDD/')
        updated_content = updated_content.replace('../03_EARS/', '../../03_EARS/')
        updated_content = updated_content.replace('../01_BRD/', '../../01_BRD/')
        Path(new_path).write_text(updated_content)
        fixes.append(f"Updated relative links for nested folder structure")

    return fixes
```

**Link Path Updates After Move**:

| Original Path | Updated Path |
|---------------|--------------|
| `../04_BDD/BDD-01_slug/BDD-01.md` | `../../04_BDD/BDD-01_slug/BDD-01.md` |
| `../01_BRD/BRD-01_slug/BRD-01.md` | `../../01_BRD/BRD-01_slug/BRD-01.md` |

---

### Phase 1: Create Missing Files

Creates files that are referenced but don't exist.

**Scope**:

| Missing File | Action | Template Used |
|--------------|--------|---------------|
| `ADR-00_INDEX.md` | Create ADR index | Index template |
| `ARCH_*.md` | Create placeholder architecture doc | ARCH template |
| Reference docs (`*_REF_*.md`) | Create placeholder | REF template |

**ADR Index Template**:

```markdown
---
title: "ADR-00: Architecture Decision Records Index"
tags:
  - adr
  - index
  - reference
custom_fields:
  document_type: index
  artifact_type: ADR-REFERENCE
  layer: 5
---

# ADR-00: Architecture Decision Records Index

Master index of all Architecture Decision Records for this project.

## Active Decisions

| ADR ID | Title | Status | Date | Impact |
|--------|-------|--------|------|--------|
| ADR-01 | [Title] | Accepted | YYYY-MM-DD | High/Medium/Low |

## Superseded Decisions

| ADR ID | Title | Superseded By | Date |
|--------|-------|---------------|------|
| [None] | | | |

## Decision Categories

| Category | ADR IDs | Description |
|----------|---------|-------------|
| Infrastructure | | Infrastructure-related decisions |
| Security | | Security architecture decisions |
| Integration | | External integration decisions |
| Data | | Data management decisions |

---

*Maintained by doc-adr-fixer. Update when adding new ADRs.*
```

**Architecture Placeholder Template**:

```markdown
---
title: "Architecture Document: [Component Name]"
tags:
  - architecture
  - reference
custom_fields:
  document_type: architecture
  status: placeholder
  created_by: doc-adr-fixer
---

# Architecture Document: [Component Name]

> **Status**: Placeholder - Requires completion

## 1. Overview

[TODO: Document architecture overview]

## 2. Components

| Component | Description | Responsibility |
|-----------|-------------|----------------|
| [Name] | [Description] | [What it does] |

## 3. Interfaces

[TODO: Document component interfaces]

## 4. Design Decisions

[TODO: Link to relevant ADRs]

---

*Created by doc-adr-fixer as placeholder. Complete this document to resolve broken link issues.*
```

---

### Phase 2: Fix Broken Links

Updates links to point to correct locations.

**Fix Actions**:

| Issue Code | Issue | Fix Action |
|------------|-------|------------|
| REV-L001 | Broken internal link | Update path or create target file |
| REV-L002 | External link unreachable | Add warning comment, keep link |
| REV-L003 | Absolute path used | Convert to relative path |
| REV-L004 | Missing BDD traceability link | Add link to corresponding BDD scenario |

**Path Resolution Logic**:

```python
def fix_link_path(adr_location: str, target_path: str) -> str:
    """Calculate correct relative path based on ADR location."""

    # Monolithic ADR: docs/05_ADR/ADR-01.md
    # Sectioned ADR: docs/05_ADR/ADR-01_slug/ADR-01.3_section.md

    if is_sectioned_adr(adr_location):
        # Need to go up one more level
        return "../" + calculate_relative_path(adr_location, target_path)
    else:
        return calculate_relative_path(adr_location, target_path)
```

**Cross-Layer Link Fix**:

| Source | Target | Link Pattern |
|--------|--------|--------------|
| ADR | BDD | `../04_BDD/BDD-NN.feature` |
| ADR | BRD | `../01_BRD/BRD-NN.md` |
| ADR | SYS | `../06_SYS/SYS-NN.md` |

---

### Phase 3: Fix Element IDs

Converts invalid element IDs to correct format.

**Conversion Rules**:

| Pattern | Issue | Conversion |
|---------|-------|------------|
| `ADR.NN.01.SS` | Code 01 invalid for ADR | `ADR.NN.13.SS` (Decision Context) |
| `DEC-XXX` | Legacy pattern | `ADR.NN.14.SS` |
| `OPT-XXX` | Legacy pattern | `ADR.NN.15.SS` |
| `CON-XXX` | Legacy pattern | `ADR.NN.16.SS` |

**Type Code Mapping** (ADR-specific valid codes: 13, 14, 15, 16):

| Code | Element Type | Description |
|------|--------------|-------------|
| 13 | Decision Context | Background and problem statement |
| 14 | Decision Statement | The actual decision made |
| 15 | Option Considered | Alternative options evaluated |
| 16 | Consequence | Implications of the decision |

**Invalid Code Conversions**:

| Invalid Code | Valid Code | Element Type |
|--------------|------------|--------------|
| 01 | 13 | Decision Context (was Functional Requirement) |
| 05 | 14 | Decision Statement (was Use Case) |
| 06 | 16 | Consequence (was Acceptance Criteria) |

**Regex Patterns**:

```python
# Find element IDs with invalid type codes for ADR
invalid_adr_type_01 = r'ADR\.(\d{2})\.01\.(\d{2})'
replacement_01 = r'ADR.\1.13.\2'

invalid_adr_type_05 = r'ADR\.(\d{2})\.05\.(\d{2})'
replacement_05 = r'ADR.\1.14.\2'

# Find legacy patterns
legacy_dec = r'###\s+DEC-(\d+):'
legacy_opt = r'###\s+OPT-(\d+):'
legacy_con = r'###\s+CON-(\d+):'
```

---

### Phase 4: Fix Content Issues

Addresses placeholders and incomplete content.

**Fix Actions**:

| Issue Code | Issue | Fix Action |
|------------|-------|------------|
| REV-P001 | `[TODO]` placeholder | Flag for manual completion (cannot auto-fix) |
| REV-P002 | `[TBD]` placeholder | Flag for manual completion (cannot auto-fix) |
| REV-P003 | Template date `YYYY-MM-DD` | Replace with current date |
| REV-P004 | Template name `[Name]` | Replace with metadata author or flag |
| REV-P005 | Empty section | Add minimum template content |
| REV-P006 | Missing decision status | Add "Proposed" as default status |

**Auto-Replacements**:

```python
replacements = {
    'YYYY-MM-DDTHH:MM:SS': datetime.now().strftime('%Y-%m-%dT%H:%M:%S'),
    'YYYY-MM-DD': datetime.now().strftime('%Y-%m-%d'),
    'MM/DD/YYYY': datetime.now().strftime('%m/%d/%Y'),
    '[Current date]': datetime.now().strftime('%Y-%m-%dT%H:%M:%S'),
    '[Status]': 'Proposed',
}
```

**ADR-Specific Content Fixes**:

| Section | Missing Content | Auto-Fill |
|---------|-----------------|-----------|
| Status | Empty | "Proposed" |
| Decision Date | Empty | Current date |
| Deciders | Empty | "[Pending assignment]" |

---

### Phase 5: Update References

Ensures traceability and cross-references are correct.

**Fix Actions**:

| Issue | Fix Action |
|-------|------------|
| Missing `@ref:` for created files | Add reference tag |
| Incorrect cross-ADR path | Update to correct relative path |
| Missing BDD traceability | Add `@trace: BDD-NN.SS` tag |
| Missing BRD alignment | Add `@trace: BRD-NN.SS` tag |

**Traceability Matrix Update**:

```markdown
## Traceability

| ADR Element | Traces To | Type |
|-------------|-----------|------|
| ADR.01.14.01 | BDD.01.09.03 | Behavior Implementation |
| ADR.01.13.01 | BRD.01.22.05 | Business Context |
```

---

### Phase 6: Handle Upstream Drift (Auto-Merge)

Addresses issues where upstream source documents (BDD) have changed since ADR creation. Implements tiered auto-merge with version management.

#### 6.0.1 Hash Validation Fixes

**FIX-H001: Invalid Hash Placeholder**

Trigger: Hash contains placeholder instead of SHA-256

Fix:
```bash
sha256sum <upstream_file_path> | cut -d' ' -f1
```
Update cache with: `sha256:<64_hex_output>`

**FIX-H002: Missing Hash Prefix**

Trigger: 64 hex chars but missing `sha256:` prefix

Fix: Prepend `sha256:` to value

**FIX-H003: Upstream File Not Found**

Trigger: Cannot compute hash (file missing)

Fix: Set `drift_detected: true`, add to manual review

| Code | Description | Auto-Fix | Severity |
|------|-------------|----------|----------|
| FIX-H001 | Replace placeholder hash with actual SHA-256 | Yes | Error |
| FIX-H002 | Add missing sha256: prefix | Yes | Warning |
| FIX-H003 | Upstream file not found | Partial | Error |

---

**Upstream/Downstream Context**:

| Direction | Layer | Artifact | Relationship |
|-----------|-------|----------|--------------|
| Upstream | 4 | BDD | Provides behavior specifications that drive decisions |
| Current | 5 | ADR | Architecture Decision Records |
| Downstream | 6 | SYS | System design implementing decisions |

**ADR ID Pattern**: `ADR-NN-SS` where:
- `NN` = Module number (01-99)
- `SS` = Sequence number within module (01-99)
- Example: `ADR-01-15` = Module 01, Decision 15

---

#### Tiered Auto-Merge System

**Change Percentage Calculation**:

```python
def calculate_drift_percentage(current_hash: str, upstream_hash: str,
                                current_content: str, upstream_content: str) -> float:
    """Calculate percentage of content change between versions."""
    if current_hash == upstream_hash:
        return 0.0

    # Line-based diff calculation
    current_lines = set(current_content.strip().split('\n'))
    upstream_lines = set(upstream_content.strip().split('\n'))

    added = upstream_lines - current_lines
    removed = current_lines - upstream_lines
    total_changes = len(added) + len(removed)
    total_lines = max(len(current_lines), len(upstream_lines), 1)

    return (total_changes / total_lines) * 100
```

**Tier Definitions**:

| Tier | Change % | Action | Version Increment | Human Review |
|------|----------|--------|-------------------|--------------|
| Tier 1 | < 5% | Auto-merge decision updates | Patch (x.x.+1) | No |
| Tier 2 | 5-15% | Auto-merge with changelog | Minor (x.+1.0) | No |
| Tier 3 | > 15% | Archive + regenerate | Major (+1.0.0) | Yes |

---

#### Tier 1: Minor Updates (< 5% change)

**Trigger**: Small upstream modifications (typos, clarifications, minor additions)

**Auto-Merge Actions**:

1. Update affected `@ref:` tags with new upstream version
2. Refresh decision context if wording changed
3. Increment ADR patch version (e.g., `1.0.0` -> `1.0.1`)
4. Log change in drift cache

**Example Tier 1 Fix**:

```markdown
<!-- Before -->
@ref: BDD-01.09.03 (v1.2.0)

<!-- After (auto-merged) -->
@ref: BDD-01.09.03 (v1.2.1)
<!-- Tier 1 auto-merge: Minor upstream update (2.3% change) - 2026-02-10 -->
```

---

#### Tier 2: Moderate Updates (5-15% change)

**Trigger**: Meaningful upstream changes (new scenarios, modified behaviors)

**Auto-Merge Actions**:

1. Apply all Tier 1 actions
2. Generate detailed changelog section
3. Update decision rationale if affected
4. Mark decisions as needing review with `[REVIEW-SUGGESTED]`
5. Increment ADR minor version (e.g., `1.0.1` -> `1.1.0`)
6. Add changelog block to ADR

**Changelog Block Format**:

```markdown
## Upstream Change Log

### Version 1.1.0 (2026-02-10)

**Source**: BDD-01.feature (v1.3.0)
**Change Percentage**: 8.7%
**Auto-Merge Tier**: 2

| Change Type | Description | ADR Impact |
|-------------|-------------|------------|
| Added | Scenario: Error handling for timeout | Decision ADR-01-03 context updated |
| Modified | Scenario: Authentication flow steps | Decision ADR-01-01 rationale refreshed |
| Removed | None | N/A |

**Decisions Flagged for Review**:
- ADR-01-03 [REVIEW-SUGGESTED]: New error handling scenario may affect retry strategy
```

---

#### Tier 3: Major Updates (> 15% change)

**Trigger**: Substantial upstream restructuring or new requirements

**Actions** (Requires Human Review):

1. Archive current ADR version (no deletion)
2. Create archive manifest
3. Mark all decisions as `[SUPERSEDED]` (not deleted)
4. Trigger regeneration workflow
5. Increment major version (e.g., `1.1.0` -> `2.0.0`)
6. Generate new ADR with fresh decision IDs

**No Deletion Policy**:

Decisions are NEVER deleted. Instead, they are marked as superseded:

```markdown
### ADR-01-05: Authentication Token Strategy [SUPERSEDED]

> **Superseded by**: ADR-01-15 (v2.0.0)
> **Superseded date**: 2026-02-10
> **Reason**: Upstream BDD restructured authentication flow

**Original Decision** (preserved for audit):
...
```

**Archive Manifest Format** (`ADR-NN_archive_manifest.json`):

```json
{
  "archive_version": "1.0",
  "archive_date": "2026-02-10T16:00:00",
  "archived_adr": "ADR-01",
  "archived_version": "1.1.0",
  "new_version": "2.0.0",
  "trigger": {
    "type": "tier_3_drift",
    "upstream_document": "BDD-01.feature",
    "change_percentage": 23.5,
    "upstream_version_before": "1.2.0",
    "upstream_version_after": "2.0.0"
  },
  "superseded_decisions": [
    {
      "id": "ADR-01-05",
      "title": "Authentication Token Strategy",
      "superseded_by": "ADR-01-15",
      "reason": "Upstream BDD restructured authentication flow"
    },
    {
      "id": "ADR-01-07",
      "title": "Session Management Approach",
      "superseded_by": "ADR-01-16",
      "reason": "New session requirements in BDD"
    }
  ],
  "preserved_decisions": [
    {
      "id": "ADR-01-01",
      "title": "Database Selection",
      "status": "unchanged",
      "carried_forward_as": "ADR-01-01"
    }
  ],
  "archive_location": "docs/05_ADR/archive/ADR-01_v1.1.0/"
}
```

---

#### Enhanced Drift Cache

**Updated `.drift_cache.json` Structure**:

```json
{
  "cache_version": "2.0",
  "adr_id": "ADR-01",
  "adr_version": "1.1.0",
  "adr_updated": "2026-02-10T16:00:00",
  "drift_reviewed": "2026-02-10T16:00:00",
  "upstream_tracking": {
    "BDD": {
      "document": "../../04_BDD/BDD-01.feature",
      "tracked_version": "1.3.0",
      "content_hash": "a1b2c3d4e5f6...",
      "last_sync": "2026-02-10T16:00:00"
    }
  },
  "downstream_tracking": {
    "SYS": {
      "document": "../../06_SYS/SYS-01.md",
      "notified_version": "1.1.0",
      "notification_date": "2026-02-10T16:00:00"
    }
  },
  "merge_history": [
    {
      "date": "2026-02-10T16:00:00",
      "tier": 2,
      "change_percentage": 8.7,
      "upstream_document": "BDD-01.feature",
      "version_before": "1.0.1",
      "version_after": "1.1.0",
      "decisions_updated": ["ADR-01-01", "ADR-01-03"],
      "decisions_flagged": ["ADR-01-03"],
      "auto_merged": true
    },
    {
      "date": "2026-02-08T10:00:00",
      "tier": 1,
      "change_percentage": 2.3,
      "upstream_document": "BDD-01.feature",
      "version_before": "1.0.0",
      "version_after": "1.0.1",
      "decisions_updated": ["ADR-01-02"],
      "decisions_flagged": [],
      "auto_merged": true
    }
  ],
  "acknowledged_drift": [
    {
      "document": "BDD-01.feature",
      "acknowledged_date": "2026-02-07",
      "acknowledged_version": "1.1.5",
      "reason": "Reviewed - documentation-only changes, no ADR impact"
    }
  ]
}
```

---

#### Auto-Merge Decision Flow

```mermaid
flowchart TD
    A[Detect Upstream Drift] --> B[Calculate Change %]
    B --> C{Change < 5%?}

    C -->|Yes| D[Tier 1: Auto-Merge]
    D --> D1[Update @ref tags]
    D1 --> D2[Increment patch version]
    D2 --> D3[Log to drift cache]
    D3 --> Z[Complete]

    C -->|No| E{Change 5-15%?}

    E -->|Yes| F[Tier 2: Auto-Merge + Changelog]
    F --> F1[Apply Tier 1 actions]
    F1 --> F2[Generate changelog block]
    F2 --> F3[Mark REVIEW-SUGGESTED]
    F3 --> F4[Increment minor version]
    F4 --> F5[Log to merge history]
    F5 --> Z

    E -->|No| G[Tier 3: Archive + Regenerate]
    G --> G1[Create archive manifest]
    G1 --> G2[Archive current version]
    G2 --> G3[Mark decisions SUPERSEDED]
    G3 --> G4[Increment major version]
    G4 --> G5[Trigger regeneration]
    G5 --> G6[Notify downstream SYS]
    G6 --> H[Human Review Required]
```

---

#### Downstream Notification

When ADR changes (any tier), notify downstream SYS documents:

```markdown
<!-- Downstream notification added to SYS-01.md -->
<!-- ADR-DRIFT-NOTIFICATION: ADR-01 updated to v1.1.0 (2026-02-10) -->
<!-- Tier 2 merge: 8.7% upstream change from BDD-01.feature -->
<!-- Decisions potentially affecting this SYS: ADR-01-01, ADR-01-03 -->
<!-- Review recommended for: Section 4 (Authentication Design) -->
```

---

#### Command Options for Phase 6

| Option | Default | Description |
|--------|---------|-------------|
| `--auto-merge` | true | Enable tiered auto-merge system |
| `--merge-tier-override` | none | Force specific tier (1, 2, or 3) |
| `--skip-archive` | false | Skip archiving for Tier 3 (not recommended) |
| `--notify-downstream` | true | Send notifications to SYS documents |
| `--generate-changelog` | true | Generate changelog for Tier 2+ |
| `--preserve-superseded` | true | Keep superseded decisions (required) |

---

## Command Usage

### Basic Usage

```bash
# Fix ADR based on latest review
/doc-adr-fixer ADR-01

# Fix with explicit review report (legacy)
/doc-adr-fixer ADR-01 --review-report ADR-01.R_review_report_v001.md

# Fix with explicit audit report (preferred)
/doc-adr-fixer ADR-01 --review-report ADR-01.A_audit_report_v001.md

# Fix and re-run review
/doc-adr-fixer ADR-01 --revalidate

# Fix with iteration limit
/doc-adr-fixer ADR-01 --revalidate --max-iterations 3
```

### Options

| Option | Default | Description |
|--------|---------|-------------|
| `--review-report` | latest | Specific audit/review report to use (`.A_audit_report` preferred) |
| `--revalidate` | false | Run reviewer after fixes |
| `--max-iterations` | 3 | Max fix-review cycles |
| `--fix-types` | all | Specific fix types (comma-separated) |
| `--create-missing` | true | Create missing reference files |
| `--backup` | true | Backup ADR before fixing |
| `--dry-run` | false | Preview fixes without applying |
| `--acknowledge-drift` | false | Interactive drift acknowledgment mode |
| `--update-drift-cache` | true | Update .drift_cache.json after fixes |

**Report Selection Precedence**:
1. Select latest report by timestamp.
2. If timestamps are equal, prefer `ADR-NN.A_audit_report_vNNN.md` over `ADR-NN.R_review_report_vNNN.md`.

### Fix Types

| Type | Description |
|------|-------------|
| `missing_files` | Create missing index, architecture docs |
| `broken_links` | Fix link paths |
| `element_ids` | Convert invalid/legacy element IDs |
| `content` | Fix placeholders, dates, status |
| `references` | Update traceability and cross-references |
| `drift` | Handle upstream drift detection issues |
| `all` | All fix types (default) |

---

## Output Artifacts

### Fix Report

**Nested Folder Rule**: ALL ADRs use nested folders (`ADR-NN_{slug}/`) regardless of size. Fix reports are stored alongside the ADR document in the nested folder.

**File Naming**: `ADR-NN.F_fix_report_vNNN.md`

**Location**: Inside the ADR nested folder: `docs/05_ADR/ADR-NN_{slug}/`

**Structure**:

```markdown
---
title: "ADR-NN.F: Fix Report v001"
tags:
  - adr
  - fix-report
  - quality-assurance
custom_fields:
  document_type: fix-report
  artifact_type: ADR-FIX
  layer: 5
  parent_doc: ADR-NN
  source_review: ADR-NN.A_audit_report_v001.md
  fix_date: "YYYY-MM-DDTHH:MM:SS"
  fix_tool: doc-adr-fixer
  fix_version: "1.0"
---

# ADR-NN Fix Report v001

## Summary

| Metric | Value |
|--------|-------|
| Source Review | ADR-NN.A_audit_report_v001.md (or legacy `ADR-NN.R_review_report_v001.md`) |
| Issues in Review | 12 |
| Issues Fixed | 10 |
| Issues Remaining | 2 (manual review required) |
| Files Created | 2 |
| Files Modified | 3 |

## Files Created

| File | Type | Location |
|------|------|----------|
| ADR-00_INDEX.md | ADR Index | docs/05_ADR/ |
| ARCH_Authentication.md | Arch Placeholder | docs/00_REF/architecture/ |

## Fixes Applied

| # | Issue Code | Issue | Fix Applied | File |
|---|------------|-------|-------------|------|
| 1 | REV-L001 | Broken index link | Created ADR-00_INDEX.md | ADR-01.md |
| 2 | REV-L001 | Broken arch link | Created placeholder ARCH file | ADR-01.md |
| 3 | REV-N004 | Element type 01 invalid | Converted to type 13 | ADR-01.md |
| 4 | REV-L003 | Absolute path used | Converted to relative | ADR-02.md |

## Issues Requiring Manual Review

| # | Issue Code | Issue | Location | Reason |
|---|------------|-------|----------|--------|
| 1 | REV-P001 | [TODO] placeholder | ADR-01:L45 | Architecture expertise needed |
| 2 | REV-D001 | BDD drift detected | ADR-01:L120 | Review behavior changes |

## Validation After Fix

| Metric | Before | After | Delta |
|--------|--------|-------|-------|
| Review Score | 88 | 95 | +7 |
| Errors | 3 | 0 | -3 |
| Warnings | 5 | 2 | -3 |

## Next Steps

1. Complete ARCH_Authentication.md placeholder
2. Address remaining [TODO] placeholders
3. Review BDD drift and update decision if needed
4. Run `/doc-adr-reviewer ADR-01` to verify fixes
```

---

## Integration with Autopilot

This skill is invoked by `doc-adr-autopilot` in the Review -> Fix cycle:

```mermaid
flowchart LR
    subgraph Phase5["Phase 5: Review & Fix Cycle"]
        A[doc-adr-reviewer] --> B{Score >= 90?}
        B -->|No| C[doc-adr-fixer]
        C --> D{Iteration < Max?}
        D -->|Yes| A
        D -->|No| E[Flag for Manual Review]
        B -->|Yes| F[PASS]
    end
```

**Autopilot Integration Points**:

| Phase | Action | Skill |
|-------|--------|-------|
| Phase 5a | Run initial review | `doc-adr-reviewer` |
| Phase 5b | Apply fixes if issues found | `doc-adr-fixer` |
| Phase 5c | Re-run review | `doc-adr-reviewer` |
| Phase 5d | Repeat until pass or max iterations | Loop |

---

## Error Handling

### Recovery Actions

| Error | Action |
|-------|--------|
| Audit/review report not found | Prompt to run `doc-adr-audit` or `doc-adr-reviewer` first |
| Cannot create file (permissions) | Log error, continue with other fixes |
| Cannot parse audit/review report | Abort with clear error message |
| Max iterations exceeded | Generate report, flag for manual review |

### Backup Strategy

Before applying any fixes:

1. Create backup in `tmp/backup/ADR-NN_YYYYMMDD_HHMMSS/`
2. Copy all ADR files to backup location
3. Apply fixes to original files
4. If error during fix, restore from backup

---

## Related Skills

| Skill | Relationship |
|-------|--------------|
| `doc-adr-audit` | Preferred combined audit source (input) |
| `doc-adr-reviewer` | Provides review report (input) |
| `doc-adr-autopilot` | Orchestrates Review -> Fix cycle |
| `doc-adr-validator` | Structural validation |
| `doc-naming` | Element ID standards |
| `doc-adr` | ADR creation rules |
| `doc-bdd` | Upstream behavior reference |
| `doc-brd` | Upstream business context |

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 2.3 | 2026-02-27 | Migrated frontmatter to `metadata`; added compatibility for `ADR-NN.A_audit_report_vNNN.md` (preferred) with legacy `ADR-NN.R_review_report_vNNN.md`; defined deterministic precedence (latest timestamp, then `.A_` over `.R_` on ties); corrected nested-folder report path examples to `docs/05_ADR` |
| 2.2 | 2026-02-26 | Aligned with ADR-MVP-TEMPLATE.md v1.1 (11-section MVP structure) |
| 2.1 | 2026-02-11 | **Structure Compliance**: Added Phase 0 for nested folder rule enforcement (REV-STR001-STR003); Runs FIRST before other fix phases |
| 2.0 | 2026-02-10 | Enhanced Phase 6 with tiered auto-merge system; Three-tier thresholds (Tier 1 <5%, Tier 2 5-15%, Tier 3 >15%); No deletion policy - superseded decisions preserved; Archive manifest for Tier 3; Enhanced drift cache with merge history; Auto-generated ADR IDs (ADR-NN-SS pattern); Downstream SYS notification; Change percentage calculation |
| 1.0 | 2026-02-10 | Initial skill creation; 6-phase fix workflow; ADR Index and Architecture file creation; Element ID conversion (types 13, 14, 15, 16); Broken link fixes; BDD/BRD upstream drift handling; Integration with autopilot Review->Fix cycle |
