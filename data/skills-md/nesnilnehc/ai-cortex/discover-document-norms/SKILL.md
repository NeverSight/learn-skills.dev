---
name: discover-document-norms
description: Help users establish project-specific artifact norms (paths, naming, lifecycle) through dialogue and scanning. Core goal - produce docs/ARTIFACT_NORMS.md and optional .ai-cortex/artifact-norms.yaml.
tags: [documentation, eng-standards, workflow]
version: 1.0.0
license: MIT
related_skills: [bootstrap-docs, assess-doc-readiness]
recommended_scope: project
metadata:
  author: ai-cortex
triggers: [discover norms, document norms]
input_schema:
  type: free-form
  description: Project path, optional starting point (AI Cortex default, project-documentation-template, blank)
output_schema:
  type: document-artifact
  description: docs/ARTIFACT_NORMS.md and optionally .ai-cortex/artifact-norms.yaml
---

# Skill: Discover Document Norms

## Purpose

Help users define their project-specific artifact norms (paths, naming, lifecycle) for document governance. Projects may have their own documentation structure; this skill discovers and formalizes it so other skills (capture-work-items, brainstorm-design, assess-doc-readiness) can follow project norms.

---

## Core Objective

**Primary Goal**: Produce `docs/ARTIFACT_NORMS.md` (and optionally `.ai-cortex/artifact-norms.yaml`) that declares the project's artifact paths, naming, and lifecycle for backlog, design, ADR, and calibration artifacts.

**Success Criteria** (ALL must be met):

1. ✅ **Project structure scanned**: Existing `docs/` structure and conventions inspected
2. ✅ **User preferences confirmed**: Paths for backlog, design, adr, doc-readiness confirmed via dialogue (or accepted from starting template)
3. ✅ **ARTIFACT_NORMS.md written**: Human-readable norms file at `docs/ARTIFACT_NORMS.md`
4. ✅ **Optional YAML created**: If user requests, `.ai-cortex/artifact-norms.yaml` written with machine-readable schema
5. ✅ **User confirmed**: User explicitly approved the norms before final write

**Acceptance Test**: Can another skill (e.g. capture-work-items) read the output and correctly resolve paths for this project?

---

## Scope Boundaries

**This skill handles**:

- Scanning project `docs/` structure
- Dialogue to confirm artifact paths and naming
- Generating `docs/ARTIFACT_NORMS.md` and optional `.ai-cortex/artifact-norms.yaml` per [spec/artifact-norms-schema.md](../../spec/artifact-norms-schema.md)
- Starting from AI Cortex default, project-documentation-template, or blank

**This skill does NOT handle**:

- Bootstrapping full project docs (use `bootstrap-docs`)
- Assessing doc readiness (use `assess-doc-readiness`)
- Validating existing docs against norms (use `validate-doc-artifacts`)

**Handoff point**: When norms are written and confirmed, hand off to other document-producing skills or `validate-doc-artifacts` for compliance checks.

---

## Use Cases

- **New project**: No artifact norms yet; user wants to establish them before using capture-work-items or brainstorm-design.
- **Existing project**: Project has custom `docs/` structure; formalize it so skills align.
- **Migration**: Adopting AI Cortex defaults or project-documentation-template; create norms file for consistency.

---

## Behavior

### Interaction Policy

- **Defaults**: Project path = workspace root; start from AI Cortex defaults if no norms
- **Choice options**: Starting point `[ai-cortex][template][blank]`; path mapping per artifact type
- **Confirm**: Before writing ARTIFACT_NORMS.md; all path mappings

### Phase 1: Scan

1. Inspect project root and `docs/` (if exists)
2. Identify existing paths: backlog, design, adr, calibration, etc.
3. Note any conventions (naming, front-matter) from sample files

### Phase 2: Choose Starting Point

Ask user or infer from context:

- **AI Cortex default**: Use [spec/artifact-contract.md](../../spec/artifact-contract.md) as baseline
- **project-documentation-template**: Map template structure to artifact types
- **Blank**: Start with minimal table, user fills in paths

### Phase 3: Confirm Paths

For each artifact type (backlog-item, design, adr, doc-readiness):

- Propose path_pattern and naming from starting point or existing structure
- Ask user to confirm or customize
- Document Path Detection rules for backlog-item if applicable

### Phase 4: Write and Confirm

1. Generate `docs/ARTIFACT_NORMS.md` per [spec/artifact-norms-schema.md](../../spec/artifact-norms-schema.md)
2. Optionally generate `.ai-cortex/artifact-norms.yaml`
3. Present summary; request user confirmation before writing
4. Write files after confirmation

---

## Input & Output

### Input

- Project path (default: current workspace root)
- Optional: starting point (ai-cortex | template | blank)

### Output

- `docs/ARTIFACT_NORMS.md`: Human-readable artifact norms table
- `.ai-cortex/artifact-norms.yaml` (optional): Machine-readable schema

---

## Restrictions

### Hard Boundaries

- **No overwrite without confirmation**: Do not write or overwrite norms files without explicit user approval.
- **Schema compliance**: Output MUST follow [spec/artifact-norms-schema.md](../../spec/artifact-norms-schema.md).

### Skill Boundaries (Avoid Overlap)

**Do NOT do these (other skills handle them)**:

- Full docs bootstrap → `bootstrap-docs`
- Readiness assessment → `assess-doc-readiness`
- Compliance validation → `validate-doc-artifacts`

---

## Self-Check

### Core Success Criteria (ALL must be met)

- [ ] **Project structure scanned**: Existing docs/ inspected
- [ ] **User preferences confirmed**: Paths confirmed via dialogue
- [ ] **ARTIFACT_NORMS.md written**: File exists at docs/ARTIFACT_NORMS.md
- [ ] **User confirmed**: User approved before write

### Acceptance Test

**Can another skill read the output and correctly resolve paths for this project?**

If NO: Norms incomplete or inconsistent. Return to Phase 3.
If YES: Handoff complete.

---

## Examples

### Example 1: New Project, AI Cortex Default

**Context**: Empty project, no docs/.

**Steps**: Start from AI Cortex default. Propose paths: `docs/backlog/`, `docs/design-decisions/`, `docs/process-management/decisions/`, `docs/calibration/`. User confirms. Write `docs/ARTIFACT_NORMS.md` and create `docs/` subdirs as needed.

### Example 2: Existing Custom Structure

**Context**: Project has `docs/work-items/`, `docs/decisions/`, no formal norms.

**Steps**: Scan structure. Propose mapping: backlog-item → `docs/work-items/`, adr → `docs/decisions/`. User confirms. Write norms file with custom paths.

---

## Appendix: Output contract

This skill produces **document-artifact** outputs for project norms. Output MUST conform to:

| Element | Requirement |
| :--- | :--- |
| **Primary output** | `docs/ARTIFACT_NORMS.md` — human-readable artifact norms table (artifact_type, path_pattern, naming, lifecycle) |
| **Optional output** | `.ai-cortex/artifact-norms.yaml` — machine-readable schema per [spec/artifact-norms-schema.md](../../spec/artifact-norms-schema.md) |
| **Path mapping** | Each artifact_type mapped to a path_pattern; user must confirm before write |
