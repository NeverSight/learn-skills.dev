---
name: reviewing-code-modularity-skill
description: Use when reviewing or changing code structure so a codebase is easier to understand, change, test, or delete — including when the user uses no structural vocabulary, e.g. "this file does too much", "this is hard to test", "I keep editing the same thing in many places", or "this is a mess". Covers module boundaries, file splits, public APIs/exports, dependency direction, coupling/cohesion, shallow layers, over-abstraction, duplicated structural decisions, hard-to-test handlers/components, scattered error mapping, and refactors that move code across modules. Do not use for ordinary bug fixes, formatting, naming-only cleanup, or local edits that do not affect structure.
---

# Reviewing Code Modularity

## Goal

Reduce code complexity without architecture cosplay.

Improve module ownership, public surfaces, information hiding, dependency direction, and testable seams. Prefer deep modules with small, stable public surfaces and clear dependency direction. Use the smallest restructuring that makes code easier to understand, change, and test — never more.

## Non-negotiables

These hold in every mode. They are the point of this skill — do not dilute them.

1. Inspect the actual code and nearby conventions before recommending structure. Advice given sight-unseen is usually wrong.
2. Do not split files by line count. Split by responsibility, or not at all.
3. Do not create Clean Architecture, DDD, hexagonal layering, SOLID-heavy layering, repositories, factories, adapters, dependency injection, ports, or interfaces unless they solve present complexity in this codebase.
4. Do not introduce interfaces, factories, or DI for a single implementation unless there is real test-seam or coupling pressure.
5. Do not merge duplicated-looking code if the concepts may evolve separately. Duplication often beats a wrong abstraction.
6. Do not propose a broad rewrite when a local restructuring solves the problem.
7. Preserve behavior unless the user explicitly asks for a behavior change.
8. Do not create or edit ADRs or other docs unless the user asks.

## Core vocabulary

When terminology matters or you produce a report, use a consistent lens: module, public surface, implementation, responsibility, depth, shallow module, seam, leakage, locality, change amplification, architecture cosplay, recommendation strength. Definitions in `references/language.md`. Prefer the repo's own word for a concept when it has one.

## Before any mode

1. Inspect first: folder layout, naming, import direction, nearby similar features, test style, public exports, and existing error/validation conventions. Do not invent a new architecture until you understand the current one.
2. For each module in scope, ask: What does it own? What should it hide? What is its public surface? Who imports it? What does it import? Can it be tested without booting the whole app?
3. Read project context when a recommendation is broad or moves code across modules — see `references/decision-records.md`.

Judge complexity by whether future changes get harder: change amplification, cognitive load, unknown unknowns, obscurity. The full catalog is in `references/red-flags.md` and `references/principles.md` — load the relevant section, do not recite it.

## Mode selection

| Mode | Use when | Output |
| --- | --- | --- |
| **A — Fast review** | Review a file, diff, PR, module, route, component, or small area. | Findings ordered by risk. No candidate cards. |
| **B — Friction scan** | Scan a codebase or area for refactoring candidates, improve structure, find boundaries, or ask for a top recommendation. | Candidate cards + top recommendation. |
| **C — Candidate deepening** | A candidate is chosen, or the user asks to design a public surface/interface. | Owns/hides/surface + design comparison. |
| **D — Implementation** | The user asks the agent to actually refactor. | Smallest behavior-preserving change + validation. |

Default to the smallest mode that fits. Modes chain when the task is broad: B → C → D.

### Mode A: Fast modularity review

Inspect the code and report findings ordered by risk. For each finding:

- **Severity** — high (causes change amplification or hidden bugs now: leaked decisions, reversed dependencies, side-effectful imports), medium (will bite as the feature grows: shallow layers, mixed responsibilities, weak boundaries), or low (safe to defer: naming, small duplication, cosmetic splits).
- **File/line** if available.
- **Why it increases complexity** — name the mechanism.
- **Smallest useful fix** — behavior-preserving.
- **What not to change** — only when there is a real over-refactor risk to head off.

Do not use candidate cards and do not write an HTML report in this mode unless the user asks. Concise findings are the product.

### Mode B: Architecture friction scan

Explore the area for friction, then produce a candidate report using `references/review-report.md`:

- A single **top recommendation** first.
- **1–4 candidates**, each with: current friction (grounded in real code), why complexity increases, smallest useful fix, before/after sketch, testing impact, what not to change, and recommendation strength (Strong | Worth exploring | Speculative).

Markdown is the default. An HTML report is opt-in — only for broad scans or an explicit visual-report request. After presenting candidates, ask which one to explore, unless the user already requested implementation.

### Mode C: Candidate deepening design

Use after the user selects a candidate or asks to design a public surface. Produce:

1. What the module **owns**.
2. What it **hides**.
3. The **public surface**.
4. **Example caller code** — the smallest realistic call site.
5. The **tests that should survive** unchanged (the behavior contract).
6. What **not** to refactor.
7. **2–4 materially different designs**, only when the decision is nontrivial.
8. **One strong recommendation**, with a one-line reason.

Load `references/interface-design.md` for the design comparison. Comparing designs is not a license to add interfaces — the minimal surface often wins.

### Mode D: Behavior-preserving implementation

Use when asked to actually refactor:

- Make the **smallest behavior-preserving change** that realizes the chosen design.
- Do not silently change public APIs.
- Update imports carefully; do not move code without checking callers.
- Keep unrelated cleanup out of the change.
- Carry the candidate's "what not to change" guardrail through.
- Then validate.

Close with: what changed, why the structure is better, what checks were run, and remaining risk. For tiny changes, collapse this into a short paragraph.

## Validation

After edits:

1. Run the smallest relevant tests.
2. Run typecheck if available.
3. Run lint if available.
4. Run import or dependency-boundary checks if available.
5. Inspect the final diff; confirm no unrelated refactor crept in.
6. If validation cannot run, state that clearly.

## Reference loading

Use progressive disclosure. Reach for `rg` (or the Grep tool / `grep`); if the right section is not obvious, list headings first with `rg '^## ' references/*.md`, then read only the matching range. Do not recite references — apply them to the code at hand.

- `references/principles.md` — design tradeoffs: deep modules, information hiding, dependency direction, abstraction discipline, file splitting.
- `references/red-flags.md` — suspected problems; read only the relevant numbered red flags.
- `references/examples.md` — concrete restructurings when no nearby project pattern is enough.
- `references/language.md` — shared vocabulary when terminology matters or when producing a report.
- `references/review-report.md` — candidate report format (Mode B); not for Mode A fast reviews unless asked.
- `references/interface-design.md` — design exploration for a chosen candidate (Mode C).
- `references/decision-records.md` — project-context and ADR handling before broad recommendations.
