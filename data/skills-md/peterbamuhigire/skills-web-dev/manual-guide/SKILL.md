---
name: manual-guide
description: "Generate end-user manuals and reference guides for ERP modules. Use when the user asks to document a feature, write a user manual, or sync a reference guide. This skill is explicitly separate from doc-architect (which manages AI guidance docs like AGENTS.md)."
---

## Required Plugins

**Superpowers plugin:** MUST be active for all work using this skill. Use throughout the entire build pipeline — design decisions, code generation, debugging, quality checks, and any task where it offers enhanced capabilities. If superpowers provides a better way to accomplish something, prefer it over the default approach.

# Manual Guide (End-User Documentation)

Create **end-user manuals** and **reference guides**. This is **not** for AI instruction documents. Do **not** edit or generate AGENTS.md or other AI guidance files when this skill is used.

## Why Manuals Matter (SaaS Baseline)

End-user manuals and system guides are **required** deliverables for any SaaS application. Features are not considered complete until:

- A user-facing manual exists for the feature
- The manual includes step-by-step instructions, screenshots/visuals, and edge cases
- The manual is aligned with the feature spec and user workflows

**Documentation Standards (MANDATORY):** ALL manual files must follow strict formatting rules:
- **500-line hard limit** per manual page - no exceptions
- **Two-tier structure**: Manual index/TOC + Individual topic pages (max 500 lines each)
- **Smart subdirectory grouping** in `/manuals/` by module
- **See `skills/doc-standards.md` for complete requirements**

## Trigger Phrases

Activate when the user asks to:

- "Document feature [X]"
- "Write manual for [Module]"
- "Sync reference guide"

## Contextual Discovery (Intelligence Phase)

Before writing a single word, analyze these four pillars:

1. **Plans**: Scan `docs/plans/**/*.md` to understand business intent and user stories.
2. **Schema**: Scan `database/schema/*.sql` to identify constraints, triggers, and auto-generated fields.
3. **Codebase**: Read implementation in `src/` or `app/` to see actual UI behavior and data flow.
4. **Documentation**: Check `docs/*` for style guides or technical debt notes.

## Output Structure (Dual-Workflow)

Every guide must include:

1. **Conceptual Overview**
   - Why the feature exists
   - How it works from a business perspective

2. **Procedural Steps**
   - Numbered steps for the happy path
   - Use bold for UI elements (**buttons**, **menus**, **fields**)

3. **Technical Reference**
   - Tables for auto-generated fields, required inputs, and background triggers

4. **Edge Cases**
   - Derived from schema constraints and validation rules

## Comprehensive Manual Standards (Required)

Use these standards to design manuals for SaaS web apps. Summarize and adapt per module.

### 1) Documentation Strategy

- Define audience personas (first-time users, regular users, admins, integrators)
- Define documentation types (getting started, feature guides, troubleshooting, API docs)
- Maintain a content audit checklist per release

### 2) Information Architecture

Organize manuals with a clear hierarchy:

- Getting Started
- Tutorials & Guides
- How-To Articles
- Reference (feature specs, error codes, shortcuts)
- Troubleshooting
- Best Practices
- What’s New

### 3) Writing & Microcopy Standards

- Use active voice and direct instructions
- Provide numbered, testable steps
- Use consistent UI terms and button labels
- Include FAQ and common errors

### 4) Visual & Media Standards

- High-resolution screenshots, annotated where needed
- Blur sensitive data
- Use consistent naming and alt text
- Optional short videos with captions

### 5) Accessibility & Localization

- Meet WCAG accessibility basics (contrast, headings, alt text, keyboard nav)
- Prepare for translation and locale formatting

### 6) Maintenance & Versioning

- Update manuals alongside feature releases
- Track changes via version control and changelogs
- Use analytics/feedback to prioritize improvements

### 7) Distribution & Promotion

- Provide in-app help links and searchable docs
- Publish release notes and guided walkthroughs
- Maintain downloadable print/PDF versions

## Tone & Style

- Professional, instructional, literal-minded
- Use tables to compare workflows (e.g., POS vs Direct Sales)
- Avoid implementation details that are irrelevant to end users

## Manual Delivery Requirements (Required)

- Manuals must be created in `/manuals/` using subdirectories for major areas.
- Create a core page: `/public/user-manuals.php` based on the standard template (e.g., `skeleton.php`).
- The core page should dynamically include manual files, e.g. `user-manuals.php?manual=pos-system`.
- When asked to design a manual:
  1.  Check if `/public/user-manuals.php` exists.
  2.  Check if `/manuals/` exists and contains subdirectories.
  3.  If no folders exist, study the codebase and create **up to 10** top-level manual sections.
  4.  Create `/manuals/AGENTS.md` describing the directory purpose and what each subfolder should contain.
  5.  Create the manual PHP file for the requested module in its subfolder.

## Manual UI Expectations (Web)

- Make manuals **enjoyable** and **interactive**, not static help pages.
- Use a clean, high-contrast layout with subtle depth (glassmorphism-like panels).
- Provide a top progress indicator and section anchors.
- Provide a fast live search/omnibox (Cmd/Ctrl+K) with visual previews when feasible.
- Use highlighted UI callouts (dim rest of page on hover/focus of a term).
- Ensure mobile readability and fast load time.

## Manual PDF Expectations

- Produce a clean, print-ready manual for export.
- Support a dark-mode style variant where feasible.
- Use high-quality typography (sans for headings, monospace for field names).
- Include visual anchors (clean UI illustrations rather than heavy screenshots).
- Optional QR code links for video walkthroughs or live demos.

## Tool Permissions

- Allowed: `read_file`, `list_dir`, `grep_search`, `file_search`, `create_file`, `apply_patch`
- Use edits only for manuals and `/public/user-manuals.php` scaffolding

## Output Formatting

- Manuals should be created as PHP files in `/manuals/<section>/` and included dynamically by `user-manuals.php`

## Cross-References to SDLC & Documentation Skills

### Related Skills

| Skill | Relationship |
|-------|-------------|
| `sdlc-user-deploy` | SDLC-standard user documentation (User Manual, Training Materials, Ops Guide). This skill produces **in-app PHP manuals**; `sdlc-user-deploy` produces **SDLC-standard markdown docs**. Use both for complete coverage. |
| `sdlc-planning` | SRS defines features that need manuals. Use SRS feature list as manual scope checklist. |
| `sdlc-design` | API docs and SDD inform technical reference sections in manuals. |
| `sdlc-testing` | Test cases reveal edge cases that should be documented in manuals. |
| `doc-architect` | Generates AI guidance docs (AGENTS.md). **NOT** end-user manuals — use this skill instead. |
| `feature-planning` | Specs include Documentation Impact notes that define manual requirements. |
| `spec-architect` | Specs are "manual-ready" — use their workflow descriptions for manual content. |
| `project-requirements` | User workflows and business rules inform manual content. |
| `report-print-pdf` | Report export patterns — reference in manual sections about report features. |

### When to Use Which Documentation Skill

| Need | Skill |
|------|-------|
| In-app PHP manual for ERP module | `manual-guide` (this skill) |
| SDLC-standard user manual (markdown) | `sdlc-user-deploy` |
| AI guidance docs (AGENTS.md) | `doc-architect` |
| Project README and CLAUDE.md updates | `update-claude-documentation` |
| Feature spec with documentation impact | `spec-architect` or `feature-planning` |

---

**Back to:** [Skills Repository](../CLAUDE.md)
**Related:** [sdlc-user-deploy](../sdlc-user-deploy/SKILL.md) | [doc-architect](../doc-architect/SKILL.md) | [feature-planning](../feature-planning/SKILL.md)
**Last Updated:** 2026-02-20
