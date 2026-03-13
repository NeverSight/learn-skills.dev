---
name: documentation
description: >
  How to create, update, and manage documentation for any software project.
  Use this skill whenever asked to add documentation, update docs, create a runbook, write an ADR,
  document a feature, add a product spec, write onboarding guides, or any documentation-related task.
  Also trigger when making behavior-changing code changes (features, fixes, refactors, integrations, infra changes)
  that require accompanying documentation updates — even if the user doesn't explicitly mention "docs".
---

# Documentation Skill

Universal guide for creating and maintaining project documentation. Works with any project type, docs tooling, and team structure.

## Reference Files

Read these as needed — don't load everything upfront:

| File | When to read |
| ---- | ------------ |
| `references/templates.md` | Index of all templates — points to individual files in `references/templates/` |
| `references/templates/<type>.md` | When creating a new doc (Feature, ADR, Workflow, Runbook, Postmortem, Product/PRD, Onboarding) |
| `references/folder-structure.md` | When unsure where a doc goes or when creating a new section |
| `references/decision-guide.md` | When deciding which section and template to use (includes flowchart) |
| `references/project-types/*.md` | When adapting the standard structure for a specific project type |
| `references/tooling/*.md` | When the project uses a docs site tool (VitePress, Docusaurus, etc.) |

---

## Documentation Philosophy

Follow these principles when writing or updating documentation:

1. **Document what isn't obvious from reading code** — business rules, decisions, trade-offs, and operational procedures. Don't document what the code already says clearly.
2. **Document decisions and rationale** — "why" matters more than "what". Use ADRs for architecture decisions.
3. **One source of truth per topic** — prefer updating an existing doc over creating a new one. Never have two active docs describing the same current behavior.
4. **Docs are part of "done"** — every behavior-changing PR (feature, fix, refactor, integration, infra change) should update relevant docs in the same change.
5. **Short, linked docs > long monolithic docs** — five clear 1-page docs beat one 30-page document. Link between related docs.
6. **Metadata on every doc** — status, owner, and last-reviewed date make docs maintainable. Stale docs are worse than no docs.

---

## Mandatory Workflow

Follow these steps in order for every documentation change.

### Step 1: Check what already exists

Before creating anything new, search the `docs/` directory (and the registry/index if the project has one). Check if a doc already covers the topic. Prefer updating existing docs over creating new ones.

### Step 2: Determine where the doc goes

Use the decision guide (`references/decision-guide.md`) to find the right section. The two-step filter:

1. **Is this about a single module?** → `modules/<module>/` subtree
2. **Otherwise, match by purpose** → see the table below

| Purpose | Location | Template |
|---------|----------|----------|
| New developer guide | `onboarding/` | Onboarding Guide |
| Product spec / glossary | `product/` | Product/PRD |
| Coding convention | `conventions/backend/` or `conventions/frontend/` | None (reference doc) |
| Architecture decision | `adr/` | ADR |
| System design | `architecture/` | None |
| Engineering process | `workflows/` | Workflow |
| Operations / incidents | `operations/` | Runbook or Postmortem |
| Security posture | `security/` | None or Runbook |
| Module feature | `modules/<m>/features/` | Feature |
| Module domain logic | `modules/<m>/domain/` | Feature |
| Module runbook | `modules/<m>/runbooks/` | Runbook |

For the full flowchart with boundary cases, read `references/decision-guide.md`.

### Step 3: Write or update the document

Every doc file must include this frontmatter:

```md
---
title: '<doc title>'
summary: '<one-line purpose>'
status: active
owner: '<team-or-role>'
last_reviewed: YYYY-MM-DD
source_paths:
  - '<repo/path/used/as/source>'
replaces: '<old doc path, if replacing>'
replaced_by: '<new doc path, if being replaced>'
---
```

- `status`: `draft` | `active` | `superseded` | `archived`
- `last_reviewed`: always set to today's date
- `replaces` / `replaced_by`: only when superseding another doc

For the document body, read `references/templates.md` to get the right template for your doc type.

### Step 4: Update the index

If the project uses a registry file or docs index (`registry.md`, `docs/README.md`):

1. **New docs**: Add an entry with path, type, status, and owner
2. **Updated docs**: Update `last_reviewed` date
3. **Superseded docs**: Change status, add note linking to replacement

### Step 5: Update docs site (if applicable)

If the project uses a docs site tool (VitePress, Docusaurus, etc.), new pages must be added to the site configuration. Read the matching adapter in `references/tooling/` for details.

### Step 6: Handle superseded docs (only when replacing)

1. Move old doc to `legacy/superseded/` (or archive/delete if no historical value)
2. Set `status: superseded` and add `replaced_by` in old doc's frontmatter
3. Add `replaces` in new doc's frontmatter
4. Update both entries in the index/registry

---

## Project Type Adaptation

The standard folder structure works for any project, but different project types emphasize different sections. Read the matching reference file for specific guidance:

| Project Type | Reference | Key Emphasis |
|-------------|-----------|--------------|
| Monorepo | `references/project-types/monorepo.md` | `modules/` directory, registry, cross-module architecture |
| Monolith | `references/project-types/monolith.md` | Simpler structure, operations, architecture overview |
| Frontend-only | `references/project-types/frontend-only.md` | `conventions/frontend/`, product specs, UI architecture |
| Backend-only | `references/project-types/backend-only.md` | `conventions/backend/`, operations, security, API design |

---

## When to Document

Not everything needs a doc. Document when:

- Something costs time to understand from the code alone
- A decision has trade-offs worth recording
- A feature has business rules or edge cases
- An operational process would be hard to reproduce without a guide
- Someone new would have to ask the same question more than once

These are the signals that a topic deserves documentation.

---

## Quick Checklist

Before submitting any documentation change:

- [ ] Searched for existing docs on this topic first
- [ ] Frontmatter is complete with today's date in `last_reviewed`
- [ ] Doc is in the correct section per the decision guide
- [ ] Index/registry updated (if project uses one)
- [ ] Docs site config updated (if project uses one, new pages only)
- [ ] Superseded docs handled properly (if replacing)
- [ ] Links between related docs are added
