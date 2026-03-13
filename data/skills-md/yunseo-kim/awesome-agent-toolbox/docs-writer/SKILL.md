---
name: docs-writer
description: Unified documentation workflow for writing, reviewing, and updating technical docs across repositories. Use when users ask to write or edit docs, review doc quality, map code changes to doc impact, scaffold new documentation, update README/API guides, or improve docs in `/docs` and `*.md`/`*.mdx` files. Supports self-contained profile-based behavior for generic docs, Next.js docs, and Angular docs.
---

# Docs Writer

This skill provides one core documentation workflow with profile-aware rules.
Use this as the default docs skill, then apply a profile when the repo has
framework-specific conventions.

## Profile Selection

Choose one profile before planning edits:

1. `generic` (default) for most repositories
2. `nextjs` for Next.js docs trees and MDX conventions
3. `angular` for Angular documentation conventions

Profile references:

- `references/PROFILE-GENERIC.md`
- `references/PROFILE-NEXTJS.md`
- `references/PROFILE-ANGULAR.md`
- `references/TEMPLATES.md`

## Phase 1: Discover

Goal: understand request scope and affected documentation surface.

Checklist:

1. Clarify whether task is new docs, update, review, or impact analysis.
2. Inspect changed code/docs and identify user-visible behavior changes.
3. Identify target audience and intent (tutorial, reference, concept, release note).
4. Select the profile and list constraints from that profile.

If request is large collaborative drafting (RFC/spec/proposal), use
the co-authoring mode in `references/CORE-CHECKLIST.md`.

## Phase 2: Plan

Goal: produce an explicit edit plan before writing.

Checklist:

1. Map code changes to documentation targets.
2. List exact files to update/create.
3. Define section-level changes for each file.
4. Note cross-links, sidebars/index pages, and related docs updates.
5. Define validation commands and quality gates.

Use `references/CORE-CHECKLIST.md` for planning prompts.
Consult `references/TEMPLATES.md` when selecting document structure and
scaffolding.

## Phase 3: Write

Goal: apply focused edits with high signal and minimal drift.

Rules:

1. Keep writing user-centered, direct, and task-oriented.
2. Preserve repository terminology and existing information architecture.
3. Use concrete examples and expected outcomes where helpful.
4. Prefer updating canonical sources over duplicating content.
5. For profile-specific formatting (frontmatter, MDX components, code block
   attributes), follow the selected profile strictly.
6. Start from `references/TEMPLATES.md` for README/API/tutorial structure before
   adding project-specific details.

When creating new docs, include:

- clear title and short description
- prerequisites (if needed)
- actionable steps/examples
- edge cases or errors (where relevant)
- next steps or related links

## Phase 4: Verify

Goal: ensure docs are accurate, consistent, and ready to merge.

Verification sequence:

1. Technical accuracy check against code and behavior.
2. Style and structure check against profile + core checklist.
3. Link/reference integrity check.
4. Formatting/lint/build checks using repository commands.
5. Final pass for redundancy, ambiguity, and stale statements.

Before completion, report:

- files changed
- why each change was needed
- validation performed and results

## Boundaries and Handoffs

- Use this skill as default for docs work.
- All profile guidance is self-contained under `references/` in this skill.
- Keep framework-specific constraints inside profile documents, not the core flow.
