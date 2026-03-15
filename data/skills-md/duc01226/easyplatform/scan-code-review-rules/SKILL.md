---
name: scan-code-review-rules
version: 1.0.0
description: '[Documentation] Scan project and populate/sync docs/project-reference/code-review-rules.md with code conventions, anti-patterns, architecture rules, and review checklists.'
---

> **[IMPORTANT]** Use `TaskCreate` to break ALL work into small tasks BEFORE starting — including tasks for each file read. This prevents context loss from long files. For simple tasks, AI MUST ask user whether to skip.

**Prerequisites:** **MUST READ** before executing:

- `.claude/skills/shared/scan-and-update-reference-doc-protocol.md`
- `.claude/skills/shared/understand-code-first-protocol.md`

## Quick Summary

**Goal:** Scan project codebase for established conventions, lint rules, common patterns, and anti-patterns, then populate `docs/project-reference/code-review-rules.md` with actionable review rules and checklists.

**Workflow:**

1. **Read** — Load current target doc, detect init vs sync mode
2. **Scan** — Discover conventions and patterns via parallel sub-agents
3. **Report** — Write findings to external report file
4. **Generate** — Build/update reference doc from report
5. **Verify** — Validate rules reference real code patterns

**Key Rules:**

- Generic — works with any language/framework combination
- Derive rules from ACTUAL codebase patterns, not generic best practices
- Every rule should have a "DO" example from the project and a "DON'T" counterexample
- Focus on project-specific conventions that differ from framework defaults

**Be skeptical. Apply critical thinking, sequential thinking. Every claim needs traced proof, confidence percentages (Idea should be more than 80%).**

# Scan Code Review Rules

## Phase 0: Read & Assess

1. Read `docs/project-reference/code-review-rules.md`
2. Detect mode: init (placeholder) or sync (populated)
3. If sync: extract existing sections and note what's already well-documented

## Phase 1: Plan Scan Strategy

Discover code quality infrastructure:

- Linter configs (`.eslintrc`, `.editorconfig`, `stylecop.json`, `.prettierrc`, `ruff.toml`)
- CI quality gates (build scripts, test requirements, coverage thresholds)
- Code analysis configs (SonarQube, CodeClimate, custom analyzers)
- Existing code standards docs (CONTRIBUTING.md, CODING_STANDARDS.md)
- Git hooks (pre-commit, husky configs)

Use `docs/project-config.json` if available for architecture rules and naming conventions.

## Phase 2: Execute Scan (Parallel Sub-Agents)

Launch **3 Explore agents** in parallel:

### Agent 1: Backend Rules

- Grep for naming conventions (class suffixes, method prefixes, interface naming)
- Find common base classes and when they're used vs not used
- Discover error handling patterns (try-catch, Result types, error middleware)
- Find dependency injection patterns (registration conventions, lifetime choices)
- Look for anti-patterns (direct DB access from controllers, business logic in wrong layer)
- Identify logging conventions (structured logging, log levels, correlation IDs)

### Agent 2: Frontend Rules

- Grep for component conventions (naming, file organization, template patterns)
- Find state management rules (what goes in store vs component vs service)
- Discover styling conventions (BEM, CSS modules, utility classes, naming)
- Find subscription/memory management patterns (cleanup, unsubscribe)
- Look for accessibility patterns (ARIA, semantic HTML, keyboard navigation)
- Identify performance patterns (lazy loading, change detection, memoization)

### Agent 3: Architecture Rules

- Find layer boundaries (what imports what, dependency direction)
- Discover cross-service communication patterns (direct calls vs messages)
- Find shared code conventions (what's shared vs duplicated)
- Look for testing conventions (test naming, test organization, mock patterns)
- Identify security patterns (auth checks, input validation, output encoding)
- Find configuration patterns (env vars, config files, secrets management)

Write all findings to: `plans/reports/scan-code-review-rules-{YYMMDD}-{HHMM}-report.md`

## Phase 3: Analyze & Generate

Read the report. Build these sections:

### Target Sections

| Section                | Content                                                                      |
| ---------------------- | ---------------------------------------------------------------------------- |
| **Critical Rules**     | Top 5-10 rules that cause the most bugs/issues if violated                   |
| **Backend Rules**      | Naming, patterns, error handling, DI conventions with DO/DON'T examples      |
| **Frontend Rules**     | Component, state, styling, cleanup conventions with DO/DON'T examples        |
| **Architecture Rules** | Layer boundaries, cross-service rules, shared code conventions               |
| **Anti-Patterns**      | Common mistakes found in codebase with explanations and fixes                |
| **Decision Trees**     | Flowcharts for common decisions (which base class, where to put logic, etc.) |
| **Checklists**         | PR review checklists for backend, frontend, and cross-cutting concerns       |

### Content Rules

- Every rule must have a "DO" code example from the actual project
- Every rule should have a "DON'T" counterexample (real or realistic)
- Use `file:line` references for all code examples
- Prioritize rules by impact (bugs prevented, not style preferences)
- Decision trees can use markdown flowchart format or nested bullet lists

## Phase 4: Write & Verify

1. Write updated doc with `<!-- Last scanned: YYYY-MM-DD -->` at top
2. Verify: 5 code example file paths exist (Glob check)
3. Verify: anti-pattern examples are realistic (not fabricated)
4. Report: sections updated, rules count, anti-patterns discovered

---

**IMPORTANT Task Planning Notes (MUST FOLLOW)**

- Always plan and break work into many small todo tasks using TaskCreate
- Always add a final review todo task to verify work quality and identify fixes/enhancements
