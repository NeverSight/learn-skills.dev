---
name: coding-standard
description: Author a project's coding standard (docs/coding-standard/) and review checklist (docs/code-review-checklist/), one file per section, by inferring the conventions already in the codebase and filling gaps with defaults the user confirms. The checklist gets one security item per control the technical spec defines. Language- and stack-agnostic. Produces rules a reviewer can cite verbatim and a checklist a reviewer can walk item by item, the inputs lead-review consumes. Use when the user wants to write, generate, or formalize coding standards, a style guide, or a code review checklist.
---

# Coding Standard

Produce two documents for the current project, each a folder with one file per
section. [references/layout.md](references/layout.md) gives the file names.

- `docs/coding-standard/`: the rules, each with a short rationale and a correct/incorrect example.
- `docs/code-review-checklist/`: a binary checklist a reviewer walks per PR, each item traceable to a rule.

The standards must describe **this** codebase, not a generic ideal. Infer what the project already does and write that down; only propose new rules where there's a real gap, and confirm those with the user before committing them. A standard nobody follows is worse than none.

**Grill before writing.** This document is central: `lead-review` enforces it verbatim, so a wrong or unowned rule propagates into every future review. Read the project first (section 1), then grill the user on every open decision (section 2) one question at a time, each with your recommended default and the trade-off, walking each branch until resolved. Do not write either document until the rules are settled.

## 1. Read the project first

Before writing anything:

- **README** and `CONTRIBUTING.md`: declared conventions, build/run/test commands, project purpose.
- `CLAUDE.md` / `AGENTS.md`: often the real, enforced rules.
- **Manifests and tool config**: `package.json`/`Cargo.toml`/`go.mod`/`pyproject.toml`, plus linter/formatter/type-checker config (`.eslintrc*`, `.prettierrc*`, `rustfmt.toml`, `.golangci.yml`, `ruff.toml`, `tsconfig.json`, `.editorconfig`). These are existing, machine-enforced standards: capture them, don't reinvent them.
- **The code itself.** Sample 15 to 30 representative source files across layers. Extract the real patterns: naming, file/folder layout, error handling, layering boundaries, test structure, import conventions, comment density, file-size norms. Note where the codebase is internally inconsistent; those are decisions the user must make.
- Any existing `docs/adr/`, architecture docs, or a prior standards file to extend rather than replace.
- The security file in `docs/technical-specs/`: its threat model and its control IDs (`SEC-01`, ...). Each control becomes one checklist item.

If the repo is empty or near-empty, switch to interview mode: ask the user for stack, architecture, and preferences, and produce a starter standard from their answers.

## 2. Decide the rules

For each area below, state the rule the codebase already follows. Where the code is silent or inconsistent, mark it as an open decision and grill the user on it, one question at a time, recommending a default for each. Don't pad with rules irrelevant to the project.

- **Language & types**: version/edition, type-safety rules (e.g. no `any`/`unknown` handling, null handling, casts), enums vs unions.
- **Naming**: files, folders, functions, types, constants, DB columns, etc. Give the pattern and an example each.
- **Project structure & layering**: where code lives, allowed dependencies between layers, what must not appear where (e.g. no business logic in handlers, no direct DB access outside a repository layer).
- **File & function size**: limits and the split strategy when exceeded, only if the project cares.
- **Error handling**: domain errors vs raw throws, how errors surface to the boundary, logging.
- **Async / concurrency / transactions**: atomicity rules, race handling, where relevant.
- **Dependencies & tooling**: package manager, banned/preferred libraries, the exact verification commands (type-check, lint, format, test, build).
- **Tests**: framework, structure (AAA, one-assert-per-case), what must be tested, isolation/mocking rules, coverage expectations.
- **Security & secrets**: config access, secret handling, input validation, authz enforcement.
- **Comments, commits, docs**: comment policy, commit format (e.g. Conventional Commits), API/schema docs.
- **Formatting**: defer to the formatter config; state the command, don't restate rules the formatter enforces.

Alongside what you infer from the code, propose the baseline rules in [references/baseline-rules.md](references/baseline-rules.md) as defaults. They are stack-agnostic and apply to nearly every project; adapt the specific numbers and patterns to this codebase, and let the user confirm or adjust each.

## 3. Write the coding standard

Write `docs/coding-standard/` in the layout of [references/layout.md](references/layout.md).

- Number the headings inside each file (`## 2. Naming`, `### 2.1 Files`) so the checklist and reviewers can link to stable anchors.
- Each rule: imperative statement + one-line rationale + a `diff`-style or correct/incorrect code block in the project's language.
- Quote-able and verbatim-citable: short, declarative sentences, not prose. Prefer "Handlers contain no business logic." over a paragraph.
- `_index.md` holds the one-paragraph project and stack summary, the verification commands, and the table of contents. It holds no rules.
- Mark rules the linter/formatter/CI already enforces as **(enforced)** so reviewers don't waste time on them by hand.

## 4. Write the review checklist

Write `docs/code-review-checklist/` in the layout of [references/layout.md](references/layout.md).

- Binary `- [ ]` items, each phrased so the answer is yes/holds or it's a finding.
- Every item links back to its rule in `docs/coding-standard/`. No checklist item without a backing rule.
- The files follow how a reviewer reads a PR: scope, architecture, correctness, security, API contract, tests, commits and docs.
- `04-security.md` holds one item per security control in the technical spec, named by its ID. If the spec has no control IDs, ask the user to run `technical-spec` for the security section first, or list the controls with the user now.
- Separate or tag items the CI gate already covers, so manual review focuses on what tools can't catch.
- Keep it short enough to actually walk every PR. Cut nice-to-haves; this is the gate, not the wishlist.

## 5. Confirm and write

- Present the proposed rule set (or the open decisions) before writing files, unless the user said to just generate it.
- Write both folders under `docs/`.
- If the project already has these documents, read them and update in place rather than clobbering; preserve rules still valid and report what changed.
- If they exist as single files (`CODING_STANDARD.md` or `CODING_STANDARDS.md`, and `CODE_REVIEW_CHECKLIST.md`), ask once whether to migrate them into folders. Migrate as [references/layout.md](references/layout.md) describes. If the user says no, update the single files in place.
- After writing, point the user at `lead-review`, which consumes both documents as its source of truth.

## Rules

- Describe reality first, prescribe second. Every rule should be either already-followed or explicitly agreed by the user.
- Language- and stack-agnostic: detect the ecosystem; never assume one.
- No AI slop: no filler or hedging; every sentence informs. Use the `stop-slop` skill on prose when unsure.
- No em-dashes, no double-dashes (`--`) in prose; dashes only as Markdown syntax (list bullets, table rules) or in literal code/CLI flags (e.g. `--no-deps`).
- No emoji. Professional, declarative, citable.
- If a document carries a metadata header (`**Version:**`, `**Date:**`, `**Author:**`, `**Status:**`, `**Phase:**`), each such line ends with two trailing spaces so Markdown renders them on separate lines.
- Don't invent rules the project has no need for; a focused 20-rule standard beats a generic 100-rule one.
