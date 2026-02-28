---
name: bootstrap-project-documentation
description: Bootstrap or adapt project docs using project-documentation-template. Initialize (empty) or Adjust (non-empty, template as target); repeatable; no empty dirs unless requested; strict kebab-case naming. Use for lifecycle docs, ADR, version sync.
tags: [documentation, eng-standards, writing]
related_skills: [generate-standard-readme, write-agents-entry]
version: 1.1.1
license: MIT
recommended_scope: both
metadata:
  author: ai-cortex
compatibility: Requires access to https://raw.githubusercontent.com or a local clone of nesnilnehc/project-documentation-template.
---

# Skill: Bootstrap Project Documentation

## Purpose

Bootstrap or adapt project documentation using the [project-documentation-template](https://github.com/nesnilnehc/project-documentation-template) structure. Two modes: **Initialize** (empty project—copy templates and fill placeholders) and **Adjust** (non-empty—use template as target, propose renames/moves/merges, apply in-place after confirmation). Supports repeatable runs; avoids empty dirs and template files unless requested; enforces strict kebab-case naming. Both modes follow conventions from the template’s `llms.txt` and `AGENTS.md`.

---

## Use Cases

- **Empty project**: Initialize a full docs skeleton by copying template subsets and filling placeholders for small/medium/large projects.
- **Non-empty project**: Use the template as target reference; analyze existing docs, propose renames/moves/merges to align structure and naming; apply in-place changes after user confirmation. Do not create empty dirs or template files unless requested. Can be run repeatedly.
- **Shared workflows**: Generate Architecture Decision Records (ADR), update version information across docs, validate placeholders and links.
- **Iterative runs**: Run the skill repeatedly to progressively organize and refine docs; each run builds on the current state without requiring a full reinit.

**When to use**: When a project needs structured lifecycle documentation aligned with the enterprise template, or when existing docs should be aligned with that structure.

---

## Behavior

### Mode Selection

First determine the execution mode. User override takes precedence; otherwise:

| Mode | Trigger | Behavior |
| :--- | :------ | :------- |
| **Initialize** | No `docs/` or `docs/` empty | Copy subset, fill placeholders, create `VERSION`, output docs skeleton |
| **Adjust** | `docs/` has ≥1 valid document | Scan, compare, output recommendation list; apply after user confirmation |

**Detection rules**:

- No `docs/` or `docs/` is empty → **Initialize**
- `docs/` exists and has ≥1 valid `.md` file → **Adjust**
- User explicitly specifies `--mode=initialize` or `--mode=adjust` → use that mode

### Initialize Mode Steps

1. Determine project scale: small, medium, or large (from user or context).
2. Select the document subset from the template by scale:
   - **Small**: Project Overview, Development Guide, User Guide
   - **Medium**: + Architecture, Design, Requirements & Planning
   - **Large**: + Process Management, Operations Guide, Compliance, Community & Contributing
3. Fetch templates from `TEMPLATE_BASE_URL` (see Appendix) or use a local clone.
4. Copy **only** selected docs to the project `docs/`. Do not create empty directories or placeholder files unless the user explicitly requests them.
5. Fill placeholders with project metadata (name, dates, tech stack) and prompt for missing critical data.
6. Create a `VERSION` file (e.g. `1.0.0`) unless the user explicitly requests no new files.
7. Validate: no unreplaced placeholders, links valid, tables aligned.

### Adjust Mode Steps

1. Use [project-documentation-template](https://github.com/nesnilnehc/project-documentation-template) as the **target reference** for structure, conventions, and file/directory names.
2. Scan existing docs under `docs/` (structure, placeholders, links, versions).
3. Compare to the template and identify gaps:
   - Structure and path mismatches (nonstandard dir/file names)
   - Documents alignable to template (rename, move, or merge)
   - Unfilled placeholders, broken links, version inconsistencies
4. Produce a **recommendation list** and present it to the user; ask for confirmation before applying.
5. After confirmation, apply changes **in-place** to existing files. Do not create empty directories or add template files unless the user explicitly requests them.
6. The skill is **idempotent**: it can be run repeatedly to iteratively organize and refine docs.

### Conventions (from llms.txt)

- **Placeholders**: `[description]`, `[option1/option2]`, `YYYY-MM-DD`, `[number]`
- **Tables**: Preserve column alignment; `*` marks required fields
- **Version**: Use SemVer; update version history at document bottom on changes
- **References**: Internal `[Name](relative/path)`; external ` number `
- **Dates**: `YYYY-MM-DD`

### File and directory naming (strict)

- **Directories**: `kebab-case` only (e.g. `project-overview`, `development-guide`, `process-management`)
- **Files**: `kebab-case` with `.md` extension (e.g. `goals-and-vision.md`, `versioning-standards.md`)
- **ADR files**: `YYYYMMDD-slug-title.md` (e.g. `20250225-process-management-strategy.md`)
- No spaces, underscores, or PascalCase; lowercase letters, digits, hyphens only.

---

## Input & Output

### Input

- **Project metadata**: Name, description, tech stack
- **Scale**: small | medium | large (optional; infer from context if absent)
- **Mode override** (optional): `initialize` | `adjust`

### Output

- **Initialize**: Filled docs under `docs/`, `VERSION`, and a short summary of created files
- **Adjust**: A recommendation list (markdown or structured), then—after confirmation—the applied changes and summary

---

## Restrictions

- Replace all placeholders before finalizing documents; do not leave `[description]` etc. in final output unless explicitly deferred.
- Do not add or keep broken internal links; verify relative paths.
- Use consistent dates (`YYYY-MM-DD`) and SemVer for versions.
- In Adjust mode, do not apply changes without user confirmation.
- Do not remove structural elements (sections, tables) from templates without user approval.
- Do not create empty directories or add template files unless the user explicitly requests them.
- Use strict file and directory naming (kebab-case, ADR format `YYYYMMDD-title.md`) when creating or renaming paths.

---

## Self-Check

- [ ] **Mode**: Was the correct mode (Initialize vs Adjust) chosen and applied?
- [ ] **Placeholders**: Are all `[...]` placeholders replaced or explicitly marked for later fill?
- [ ] **Links**: Do internal links resolve and do external links point to valid resources?
- [ ] **Version**: Is the version consistent across `VERSION` and affected documents?
- [ ] **Tables**: Is Markdown table alignment preserved?
- [ ] **Confirm**: In Adjust mode, were changes applied only after user confirmation?
- [ ] **No extra dirs/files**: Were empty dirs and template files avoided unless user requested them?
- [ ] **Naming**: Are all new/renamed paths in kebab-case with correct ADR format where applicable?

---

## Examples

### Example 1: Initialize (Empty Project, Small Scale)

**Context**: New repo `my-service`, no `docs/` directory.

**Steps**: Agent selects Initialize; scale = small. Copies Project Overview, Development Guide, User Guide from template. Fills project name, dates, placeholder descriptions. Creates `VERSION` as `1.0.0`. Outputs a summary of created files.

**Output snippet**: `docs/project-overview/goals-and-vision.md`, `docs/development-guide/...`, `docs/user-guide/...`, `VERSION`. All placeholders filled with project-specific content.

### Example 2: Adjust (Non-Empty Project)

**Context**: Repo has `docs/` with `project_overview/goals.md` (nonstandard paths). Some placeholders unfilled.

**Steps**: Agent selects Adjust. Uses [project-documentation-template](https://github.com/nesnilnehc/project-documentation-template) as target. Produces recommendation list:

- Rename `project_overview/` → `project-overview/`, `goals.md` → `goals-and-vision.md` (kebab-case, match template)
- Unfilled placeholders in `goals-and-vision.md`: `[project description]`, `[target date]`
- Broken link: `../architecture/tech-stack.md` (path does not exist)

Agent presents the list and asks: "Apply these changes? (Y/n)". User confirms. Agent renames dirs/files, fixes placeholders and links in-place. No new empty dirs or template files created.

### Example 3: Common Workflow—Generate ADR

**Context**: Any project; user needs an Architecture Decision Record.

**Steps**: Agent fetches `docs/process-management/decisions/ADR-TEMPLATE.md` from template. Determines next ADR number (e.g. ADR-001). Fills context, options, rationale, consequences with user input. Saves as `docs/process-management/decisions/YYYYMMDD-decision-title.md` (kebab-case slug) and updates the decision index if present.

---

## Appendix: Output Contract

### Initialize Mode

| Deliverable | Required |
| :--- | :--- |
| `docs/` with selected template files only (no empty dirs) | Yes |
| `VERSION` file | Yes (unless user explicitly requests no new files) |
| All placeholders replaced (or marked for later) | Yes |
| Version history table at document bottom | Per template |

### Adjust Mode Recommendation List Format

| Section | Content |
| :--- | :--- |
| Target reference | [project-documentation-template](https://github.com/nesnilnehc/project-documentation-template) |
| Path/naming issues | Current path → recommended path (kebab-case, template alignment) |
| Alignable documents | Existing docs that can be renamed/moved/merged to match template |
| Unfilled placeholders | File path + placeholder text |
| Broken/outdated links | File path + link |
| Version issues | Conflicts or missing version refs |

### Template Source

- **TEMPLATE_BASE_URL** (canonical): `https://raw.githubusercontent.com/nesnilnehc/project-documentation-template/main/`
- Key files: `llms.txt`, `AGENTS.md`, `README.md`, `docs/`
- If fetch fails (network unavailable): prompt the user to provide a local clone path or retry later; do not proceed with stale or missing templates.
