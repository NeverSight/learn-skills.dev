---
name: rst_go_base_guide
description: Guides Go development to follow project architecture and code style rules. Use when implementing or reviewing Go code, adding features, refactoring, or when the user asks to follow project rules or standards. Ensures compliance with ai_go/v1/rules (project_architecture.md, code_style.md) and .cursor/rules.
---

# rst_go_base_guide

Guides development so that all Go code and structure follow the project rules (architecture and code style).

## When to apply

Apply this skill when:

- Writing or reviewing Go code
- Designing modules, APIs, or directory layout
- Initializing a new project or adding a new service/package
- The user explicitly asks to follow project rules, standards, or architecture

## Rule lookup order (required)

This skill may run in a **global** context (e.g. from `~/.cursor/skills`), where paths like `.cursor/rules/*.mdc` are relative and may not point to the current project. Resolve rule files in this order:

1. **Current project root** (workspace or repo where the user is working):
   - `ai_go/v1/rules/core_principles.md` (MUST follow in every interaction)
   - `.ai-context/rules/core_principles.md`, `.ai-context/rules/core_principles_zh.md`
   - `ai_go/v1/rules/project_architecture.md`, `ai_go/v1/rules/code_style.md`
   - `.ai-context/rules/project_architecture.md`, `.ai-context/rules/code_style.md` (三方项目)
   - `ai_go/v1/rules/project_architecture_zh.md`, `ai_go/v1/rules/code_style_zh.md` (中文版)
   - `.ai-context/rules/project_architecture_zh.md`, `.ai-context/rules/code_style_zh.md` (中文版，三方项目)
   - `.cursor/rules/go-project-architecture.mdc`, `.cursor/rules/go-code-style.mdc`
2. If not found under the project root: **user directory**
   - `~/.cursor/skills/` or `~/.claude/rules/` (or equivalent rule locations under the user’s home).
3. **If a required rule file is still not found**: do **not** guess or invent rules. **MUST** return a clear **user-facing message** that the rule reference failed, e.g.  
   *"Rule file not found: [path]. Please add the rules under the project root (e.g. ai_go/v1/rules/) or under ~/.cursor/skills / ~/.claude/rules so this skill can apply them."*

Always try the project root first; only fall back to the user directory when the project does not contain the rule files.

## Rule sources (must read when guiding)

When guiding implementation or review, **read the relevant full rule file(s)** (or the Cursor rule summary) using the **lookup order** above, and apply them; do not guess.

| Source | Path (relative to project root or user dir) |
|--------|---------------------------------------------|
| Full architecture | `ai_go/v1/rules/project_architecture.md`, `.ai-context/rules/project_architecture.md` |
| Full architecture (中文) | `ai_go/v1/rules/project_architecture_zh.md`, `.ai-context/rules/project_architecture_zh.md` |
| Full code style | `ai_go/v1/rules/code_style.md`, `.ai-context/rules/code_style.md` |
| Full code style (中文) | `ai_go/v1/rules/code_style_zh.md`, `.ai-context/rules/code_style_zh.md` |
| Cursor architecture summary | `.cursor/rules/go-project-architecture.mdc` |
| Cursor code style summary | `.cursor/rules/go-code-style.mdc` |

For more detail on what each file covers, see [reference.md](reference.md).

## Code style MUST when coding

When writing or generating code, **MUST** follow the **Formatting** and **Naming** sections in code_style.md (resolve path via the **Rule lookup order** above). These are mandatory (gofmt/goimports, import grouping, line length, package/file/identifier naming, abbreviations, receiver names, etc.). Do not skip or relax them. If code_style.md cannot be found, report the failure to the user as in the lookup order section.

## Guiding behavior

1. **Before suggesting structure or code**  
   Check against the rules:
   - **Layout**: `internal/` layering (domain, dao or storage, server/handler, infra, router, service, service/dto); docs under `docs/changelog` (SDD, etc.) and `docs/design` (PRD, etc.).
   - **Dependencies**: Outer depends on inner; exception—inner may use an outer package only if that outer package does not depend on any other internal package (e.g. infra as a leaf used by service). Handlers must not call dao/storage/domain/infra directly.
   - **Code style**: Naming, errors (wrap with `%w`, no panic in service/handler), context first param, DTO tags (json; Gin binding or framework equivalent), interfaces in consuming layer.

2. **When the user asks “how should I do X?”**  
   Answer in line with the rules and point to the specific rule or section when it matters (e.g. “per project_architecture.md, handlers must not call dao/infra directly”).

## Rule compliance checklist

Use this checklist when implementing or reviewing; details remain in the rule files.

- [ ] Dependencies go inward; no inner→outer unless the outer is a leaf (e.g. infra with no internal deps).
- [ ] Handlers/router call only service; dao/storage/domain/infra only used by service.
- [ ] No cyclic dependencies between packages.
- [ ] Interfaces defined in consuming layer; dependencies injected explicitly.
- [ ] Domain models independent of transport/persistence.
- [ ] External input validated at boundary; mapped to domain types.
- [ ] No panic in service or handler; return errors.
- [ ] Request/response DTOs have explicit `json` tags; validation per framework (e.g. Gin binding).
- [ ] **Formatting and Naming** from code_style.md are followed (gofmt, imports, package/file/identifier naming).
- [ ] SDD and similar docs under `docs/changelog`; PRD and design docs under `docs/design`.
- [ ] Business logic changes: update or add design docs under `docs/design`.
