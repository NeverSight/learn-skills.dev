---
name: scan-feature-docs
version: 1.0.0
description: '[Documentation] Scan project and populate/sync docs/project-reference/feature-docs-reference.md with app-to-service mapping, doc structure, templates, and documentation conventions.'
---

> **[IMPORTANT]** Use `TaskCreate` to break ALL work into small tasks BEFORE starting — including tasks for each file read. This prevents context loss from long files. For simple tasks, AI MUST ask user whether to skip.

**Prerequisites:** **MUST READ** before executing:

- `.claude/skills/shared/scan-and-update-reference-doc-protocol.md`
- `.claude/skills/shared/understand-code-first-protocol.md`

## Quick Summary

**Goal:** Scan existing business feature documentation and populate `docs/project-reference/feature-docs-reference.md` with app-to-service mapping, documentation structure conventions, template usage, and section standards.

**Workflow:**

1. **Read** — Load current target doc, detect init vs sync mode
2. **Scan** — Discover documentation patterns via parallel sub-agents
3. **Report** — Write findings to external report file
4. **Generate** — Build/update reference doc from report
5. **Verify** — Validate discovered paths and templates exist

**Key Rules:**

- Generic — works with any documentation structure (docs/, wiki/, etc.)
- Discover documentation organization dynamically from file system
- Map relationships between apps/services and their documentation
- Every reference must point to real files found in this project

**Be skeptical. Apply critical thinking, sequential thinking. Every claim needs traced proof, confidence percentages (Idea should be more than 80%).**

# Scan Feature Docs

## Phase 0: Read & Assess

1. Read `docs/project-reference/feature-docs-reference.md`
2. Detect mode: init (placeholder) or sync (populated)
3. If sync: extract existing sections and note what's already well-documented

## Phase 1: Plan Scan Strategy

Discover documentation locations:

- `docs/` directory structure (business features, architecture, guides)
- `docs/business-features/` or similar feature doc directories
- `docs/templates/` or similar template directories
- README.md files across service directories
- Wiki or external doc references in config files

Use `docs/project-config.json` if available for module lists and app mappings.

## Phase 2: Execute Scan (Parallel Sub-Agents)

Launch **2 Explore agents** in parallel:

### Agent 1: Documentation Structure

- Glob for `docs/**/*.md` to map full documentation tree
- Find documentation templates (template files, skeleton docs)
- Discover documentation section patterns (recurring H2/H3 headings across docs)
- Identify INDEX.md / README.md hub files and their link structures
- Count docs per app/module to assess coverage distribution
- Find AI companion docs (\*.ai.md or similar patterns)

### Agent 2: App-to-Service Mapping

- Map frontend apps to backend services (from config, imports, or API calls)
- Find API reference docs and their relationship to services
- Discover troubleshooting docs and their coverage
- Find cross-references between docs (links, mentions)
- Identify documentation conventions (naming, numbering, tagging patterns)
- Look for doc generation tools or scripts

Write all findings to: `plans/reports/scan-feature-docs-{YYMMDD}-{HHMM}-report.md`

## Phase 3: Analyze & Generate

Read the report. Build these sections:

### Target Sections

| Section                       | Content                                                      |
| ----------------------------- | ------------------------------------------------------------ |
| **App-to-Service Mapping**    | Table: App name, Backend services, Doc directory, Doc count  |
| **Directory Structure**       | Tree showing docs/ organization with purpose annotations     |
| **Template Paths**            | Table: Template name, Path, Purpose, Used by N docs          |
| **Section Structure**         | Standard sections found across feature docs (with frequency) |
| **Documentation Conventions** | Naming conventions, numbering schemes, required fields       |
| **Evidence Rules**            | How docs reference code (file:line patterns, test case IDs)  |
| **Coverage Gaps**             | Apps/services without documentation, incomplete docs         |

### Content Rules

- Use tables for all structured data (mappings, templates, conventions)
- Include actual directory tree output (top 3 levels)
- Show section heading patterns with frequency counts
- Highlight well-documented vs under-documented areas

## Phase 4: Write & Verify

1. Write updated doc with `<!-- Last scanned: YYYY-MM-DD -->` at top
2. Verify: 3 template paths exist on filesystem
3. Verify: app-to-service mappings match actual directory structure
4. Report: sections updated, coverage statistics, gaps identified

---

**IMPORTANT Task Planning Notes (MUST FOLLOW)**

- Always plan and break work into many small todo tasks using TaskCreate
- Always add a final review todo task to verify work quality and identify fixes/enhancements
