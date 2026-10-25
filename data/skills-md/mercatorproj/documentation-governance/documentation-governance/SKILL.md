---
name: documentation-governance
description: "Govern project documentation as an engineering asset: inventory and organize docs, map documentation to authoritative code/spec sources, detect drift, validate links and metadata, and build VitePress sites for local viewing and offline delivery. Use when a user asks to organize, audit, synchronize, migrate, document, or package project documentation. Do not use as a substitute for product decisions, business-domain approval, or code refactoring."
metadata:
  version: 1.0.1
  license: MIT
  topics: [documentation, governance, vitepress, codex]
---

# Documentation Governance

## Mission

Maintain a discoverable, reviewable, verifiable documentation system that can evolve with its project. Markdown and Git are the default source format and history mechanism; VitePress is the presentation layer, not the authoritative store by itself.

## Confirmed default policy

- Governance scope: establish a coherent standard and allow directory restructuring when justified.
- Site delivery: local preview plus offline/static deliverables.
- Code synchronization: detect differences, propose updates, validate results; semantic changes require review.
- File changes: obtain confirmation before major or destructive changes.
- Automation: run manually on request. Do not add Git hooks, CI/CD, scheduled jobs, cloud publishing, or external services unless separately requested.
- Prefer repository-native tools and dependencies. Do not install packages or change package manifests without explaining the need and obtaining permission when the change is material.

## Core invariants

1. Inspect before editing. Check repository root, existing docs, project instructions, package scripts, VitePress configuration, and Git working-tree status where available.
2. Establish authority per information type. Runtime code is evidence of current behavior, not automatically the authority for intended product behavior. A conflict between requirements and implementation must be reported, not silently adjudicated.
3. Plan before major migration. Show current path → proposed path, reason, affected references, risks, and rollback approach. Ask for approval before deleting, overwriting, bulk-moving, renaming many files, or replacing existing site configuration.
4. Preserve user work. Never overwrite unrelated changes. If the working tree is dirty, distinguish pre-existing changes from changes made by this task. Do not reset, clean, or discard changes.
5. Make minimal, reviewable edits. Avoid broad rewrites when targeted corrections suffice. Preserve useful history and content.
6. Separate facts from inference. Mark uncertain claims as `needs-review` or list them in an audit report.
7. Validate after changes. Check affected links/assets, metadata, navigation, and site build when available. Report checks not run and why.
8. No silent publication. `build` is not `publish`. Offline packaging is not deployment. Never upload or publish unless explicitly authorized.
9. The skill must remain useful without VitePress. Inventory, mapping, drift analysis, and basic validation should work independently.

## Task routing

Choose the narrowest workflow that satisfies the request. Read the corresponding file in `workflows/` before executing it.

- First-time adoption or standard setup → `workflows/onboarding.md`
- Discover what exists → `workflows/inventory.md`
- Restructure or migrate files → `workflows/migration.md`
- Compare code/specs/docs or synchronize changes → `workflows/code-sync.md`
- Set up, preview, build, or package VitePress → `workflows/site-delivery.md`
- Quality review or periodic audit → `workflows/audit.md`
- User requests only a report → do not modify files unless asked.

## Execution protocol

### A. Establish context

- Identify repository root and project type.
- Read applicable project guidance (for example `AGENTS.md`, `CONTRIBUTING.md`, existing docs conventions).
- Inspect relevant files and package scripts; do not assume tools are installed.
- Note existing VitePress configuration and existing documentation source directories.
- Check Git status if Git is available. Do not infer that a clean-looking directory means no untracked files.

### B. Classify requested actions

- **Read-only:** inventory, report, link scan, drift analysis.
- **Low-risk reversible:** add a missing index, correct a clearly broken local link, create a new report file in an agreed location.
- **Major:** bulk moves/renames, deleting or replacing documents, changing authority rules, restructuring navigation, replacing site config, installing dependencies, changing package scripts, generating large derived content, packaging that excludes/rewrites assets.

Proceed with read-only work. Low-risk edits may be made when the request clearly asks for fixes. Ask before major actions and show a concise plan.

### C. Apply and verify

- Follow the selected workflow and references.
- Record important path changes in a migration map.
- Run only relevant checks; prefer deterministic scripts for mechanical checks.
- If a check cannot run, state the limitation rather than implying success.
- Summarize changed files, checks run, results, unresolved decisions, and next actions.

## Documentation model

Use the smallest set of concepts that provides clarity:

- **Canonical source:** source of truth for a specific claim or artifact.
- **Derived content:** generated from a canonical source; identify its generator and regeneration method.
- **Supporting explanation:** human-maintained explanation, rationale, examples, or tutorials.
- **Status:** `draft`, `active`, `needs-review`, `deprecated`, or `archived`.
- **Owner:** role/team/person if known; never invent an owner.
- **Review trigger:** code paths, schema, feature, version, or event that should prompt review.

Do not require frontmatter on every legacy document immediately. Introduce it for new or actively maintained documents first, then migrate legacy documents incrementally.

## Project configuration

When useful, create `.governance/docs.yml` based on `templates/docs-governance.example.yml`. Treat it as project-specific configuration, not as a mandatory global schema. Keep generated inventories/reports separate from canonical documentation and never make generated output the authority without an explicit rule.

## Tooling rules

- Scripts should be safe by default, use the standard library where practical, provide help, return non-zero on validation failures, and avoid modifying source files unless their name and documentation explicitly say they do.
- Inventory and audit outputs should go to a user-approved report location; default suggestion is `artifacts/documentation-governance/` only after confirming it will not conflict with project conventions.
- Use local links for local/offline documentation. Avoid remote assets or runtime fetches in offline deliverables unless clearly declared.
- Do not claim PDF export, single-file bundling, or complete portability unless that capability has been tested and its limitations explained.

## Definition of done

A task is complete only when its requested outcome is delivered and the response reports:

1. What changed (or that it was read-only).
2. Important files and decisions.
3. Validation performed and actual result.
4. Unresolved conflicts/risks and checks not performed.
5. How to preview/build/package locally when relevant.

See `README.md` for package map and `references/` for detailed rules.
