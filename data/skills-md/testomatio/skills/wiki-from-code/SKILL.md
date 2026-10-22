---
name: wiki-from-code
description: >-
  Builds and refreshes a product wiki from the application source code (implicit requirements).
  Optionally attaches issue-tracker task/issue/story links.
  Use when the user asks to build or refresh the wiki/requirements/specification/docs from code, or to catalog existing functionality.
metadata:
  author: Testomat.io
  version: 1.0.0
---

# Wiki from code

Wiki of **how the product works now**. Bootstrap from code. Refresh when the code changes.

We call this "wiki" as the closest term to what we are building. But user may ask for "requirements" or "specification" or "docs" or something similar.

**Implicit** requirements means inferred from code. **Explicit** requirements means from issues/tasks/docs etc.

Decide audience once:

| Audience | Human wiki |
| --- | --- |
| End users (default, preferred) | Behavior and acceptance only. No file paths, types, stack, or protocol internals. |
| Callers who are not end users (API, job, contract etc.) | Technical entry could be treated as requirements. |

## Modes

Pick one. If unclear, **bootstrap** when `wiki/` is missing, else **refresh**.

| Mode | When |
| --- | --- |
| `bootstrap` | First wiki from this repo |
| `refresh` | Code moved; update implicit pages + catalog |

Default root: `wiki/` (or the user’s path).

Move from **overview** to **details**. Do not write feature pages before the tree exists.

## Steps

```
- [ ] 1. Catalog (shallow)
- [ ] 2. Tracker links? (ask; optional)
- [ ] 3. Overview tree (indexes)
- [ ] 4. Dive each area (one subagent each)
- [ ] 5. Validate
- [ ] 6. Report
```

Read [references/layout.md](references/layout.md) before writing files.

## Rules

- Current-state code wins any other source (e.g. docs, tests, config, infra, comments, issues etc). Intended, but not implemented (or implemented differently) behavior goes in `mismatches/` only — never a SHOULD heading on a feature page.
- Name areas and features from the **product** and user perspective, not the stack or code.
- Capabilities describe *what the product does*. Catalog records *where that lives in the repo*.
- Pair capabilities and catalog items (use relative path) (`capabilities/{area}/{feature}.md` ↔ `catalog/{area}/{feature}.yaml`). Feature page: after breadcrumb, relative link to the YAML.
- Tracker links (tasks, issues, stories, etc.) are optional. **Ask** before adding any. Put them in catalog YAML (`issues`), not on feature pages. Do not invent keys or URLs.

## 1. Catalog (shallow)

The **catalog** is what exists in the product: first a shallow area → feature list, then YAML facts in `catalog/`. Code, test, doc, and issue tracker links live here (`sources`, `tests`, `wiki_path`, `issues`).

From **code** map the product into **areas**, each with a **feature list**. That list *is* the catalog of what exists in the product at this step. Do not draft Requirement/Acceptance or YAML yet.

If an area is large, group features into sub-folders at this step. Catalog YAML uses the same relative path as the feature page.

## 2. Tracker links (optional)

**Ask the user** whether to attach issue-tracker links (tasks, issues, stories, etc.) to catalog YAML.

If none of MCP / user-supplied links work: skip with reason. Do not write placeholder tickets.

Write only into catalog YAML (`issues`). Omit the `issues` key when a feature has no match.

## 3. Overview tree

Write only the indexes first ([references/layout.md](references/layout.md)). Give the tree hierarchy when the product is complex enough. If names are ambiguous, **stop and show the list** before diving.

Shared rules live on one page; others link.

## 4. Dive each area

For each feature: catalog YAML first (`catalog/{area}/{feature}.yaml`), then the feature page (Requirement / Acceptance). Stubs, unused wiring, and doc-vs-code gaps go in `mismatches/` with all required source links (layout).

Use `subagent` per area/feature to keep the main agent focused on the helicopter view, subagents focused on the details of one area/feature.

Each subagent gets: area/feature name, allowed paths, audience, [references/layout.md](references/layout.md), "code wins", and whether tracker `issues` are in scope (matched links to write, or omit). Feature pages are Requirement / Acceptance only. Do not rewrite sibling areas except to add the one index line the parent asked for.

Subagent returns: files written, mismatches, open questions. Parent merges links and sitemap; then validates.

Exception: a one-line fix on an existing page already in context — no subagent spawn.

## 5. Validate

```markdown
Structure
- [ ] wiki/README.md is a sitemap; every listed link exists
- [ ] catalog YAML exists for every feature; every wiki_path exists
- [ ] catalog/README.md indexes every area; each area catalog README lists its YAML
- [ ] Area (and group) folders named from the product, not from stack/code
- [ ] Feature pages use the layout heading order (Requirement, Acceptance); breadcrumbs match folder depth; links are relative
- [ ] Feature pages link to the paired catalog YAML (relative path)
- [ ] Feature pages are not mega-dumps (one cluster per page)
- [ ] Feature pages not overloaded with meta info (it is located in catalog YAML)
- [ ] Tracker links are in catalog YAML (`issues`); omitted when declined or none matched; no invented keys/URLs

Content
- [ ] Features described from the user perspective, not the stack/code
- [ ] Catalog is YAML facts, not a second spec
- [ ] Current-state Requirement matches code
- [ ] mismatches/ covers disagreements (between code and other sources)
```

## 6. Report

Where to start from. Results. Mismatches. Huge projects: those three only.

## Next actions

- Explain a capability in QA language → `qa-explain-behavior`
- Risk scenarios for a capability → `qa-thinking`
- Test cases for capability/feature → `qa-write-test-cases`
