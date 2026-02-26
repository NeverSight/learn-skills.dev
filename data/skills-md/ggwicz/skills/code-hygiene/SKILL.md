---
name: code-hygiene
description: >-
  Reviews source code for structural quality violations and code smells
  across any programming language. Produces a read-only findings report
  with concrete refactoring suggestions. Activates on code review, code
  audit, code quality check, code smells, "clean this up," "make this
  more maintainable," or "reduce complexity."
allowed-tools: Read Write Glob Grep Bash(scripts/scan-source-files.sh:*)
---

# Code Hygiene Review

Review source code against 10 language-agnostic structural quality principles and produce a findings report with concrete refactoring suggestions.

**Important: This skill produces a report. Do not modify any reviewed files.**

---

## Review Workflow

1. **Select files** — Use the user's specified files. If none specified, run `scripts/scan-source-files.sh <project-directory>` to discover source files. The `<project-directory>` argument is **required** — it must be the root of the user's project, NOT the skill's own directory.
2. **Load rules** — Read `references/principles-quick-ref.md` for the full checklist with detection signals and thresholds.
3. **Review each file** — Read each file and check against all 10 principles. Load detailed reference files on demand as violations are detected (see "When to Load Reference Files").
4. **Generate findings** — For each issue found, produce a finding using the Output Format below.
5. **Classify severity** — Use `references/severity-rubric.md` to assign high/medium/low.
6. **Verify suggestions** — For each suggested rewrite, confirm it resolves the flagged violation, does not introduce a new violation of any other principle, and preserves the original behavior. If a suggestion introduces a new violation, revise it before including it.
7. **Assemble report** — Write findings to `code-hygiene-findings-YYYYMMDD.md` in the project root (use today's date). Group findings by file, then by severity (high first). End with the summary block.

---

## Output Format

Use this exact structure for each finding:

    ## [file path]

    ### Finding [N] — [Smell name] [ID] (severity: [high|medium|low])
    - **Line [N]:** `[original code snippet]`
    - **Principle:** [One-sentence explanation of the violated principle]
    - **Refactoring:** [Named refactoring technique]
    - **Suggested:**
      [concrete rewrite as a fenced code block]

**Example:**

    ## src/services/order_service.py

    ### Finding 1 — Hidden Dependency CH-02 (severity: high)
    - **Line 8:** `self.db = PostgresConnection("prod:5432")`
    - **Principle:** Dependencies created internally are invisible, untestable, and tightly coupled to a specific implementation.
    - **Refactoring:** Inject via constructor parameter
    - **Suggested:**
      ```python
      class OrderService:
          def __init__(self, db, mailer):
              self.db = db
              self.mailer = mailer
      ```

    ### Finding 2 — Nested Pyramid CH-03 (severity: medium)
    - **Line 34:** 3 levels of nesting in `process_order()`
    - **Principle:** Each nesting level forces the reader to maintain a mental stack. Guard clauses flatten the logic.
    - **Refactoring:** Replace Nested Conditional with Guard Clauses
    - **Suggested:**
      ```python
      def process_order(order):
          if not order:
              return None
          if not order.items:
              return None
          if not order.payment:
              raise ValueError("Missing payment")
          # happy path — no nesting
      ```

If a file has no findings, omit it from the report entirely.

End the report with:

    ## Summary
    - **Files reviewed:** [N]
    - **Total findings:** [N] ([N] high, [N] medium, [N] low)
    - **Top issues:** [List the 2-3 most frequent violations]
    - **Highest-leverage fix:** [The single change that would most improve the codebase]

---

## When to Load Reference Files

Load references on demand to conserve context:

| File | When to load |
|------|-------------|
| `references/principles-quick-ref.md` | Always — load at start of every review |
| `references/severity-rubric.md` | When classifying findings |
| `references/composition-over-inheritance.md` | Inheritance depth > 1 or base class used only for code reuse |
| `references/dependency-injection.md` | `import` + instantiate inside business logic |
| `references/guard-clauses.md` | Nesting depth > 2 or pyramid-shaped conditionals |
| `references/single-responsibility.md` | Function > 25 lines or class name contains "Manager", "Handler", "Utils" |
| `references/fail-fast.md` | Bare `except:`/`catch {}`, silent `None` returns, or swallowed errors |
| `references/least-surprise.md` | `get_*` function has side effects, or boolean params at call sites |
| `references/tell-dont-ask.md` | External code reads 2+ fields from an object to make a decision |
| `references/immutability.md` | `var`, `let` (JS) where `const` works, argument mutation, shared mutable state |
| `references/naming.md` | Vague names (`data`, `info`, `result`) or abbreviations (`usr`, `mgr`) |
| `references/functional-core-imperative-shell.md` | Business logic contains I/O calls (db, http, file, print) |

---

## Scope Rules

- **Review:** application source code — functions, classes, modules, components
- **Skip:** test fixtures/factories, generated code, migration files, configuration files (JSON/YAML/TOML), vendor/third-party code, single-use scripts under 20 lines, type declaration files (.d.ts)
- **Light touch:** test files — apply naming (CH-09) and guard clauses (CH-03) but do not enforce DI (CH-02) or functional core (CH-10), since test setup is inherently side-effectful
- **Do not modify reviewed files** — produce recommendations only
