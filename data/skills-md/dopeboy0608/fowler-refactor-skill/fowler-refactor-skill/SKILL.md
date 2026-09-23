---
name: fowler-refactor-skill
description: Analyze code using Martin Fowler's refactoring catalog (Extract Function, Decompose Conditional, Replace Conditional with Lookup Table, Split Phase, etc.) and propose safe, backward-compatible improvements via a structured interview. Use when asked to refactor, improve code structure, remove code smells, introduce indirection layers, or when invoking /fowler-refactor-skill explicitly.
---

# Martin Fowler Refactoring Advisor

Analyzes code for smells using Martin Fowler's *Refactoring* catalog, conducts a `grill-me`-style interview to understand the requirement, proposes a structured plan with Before/After design, and applies changes only after explicit user approval — ensuring zero breaking changes to existing callers.

> Pattern catalog and code smell reference: [references/fowler-patterns.md](./references/fowler-patterns.md)

---

## ⚠️ Operating Principles

1. **Explicit invocation only**: Does not auto-trigger on casual language like "clean this up". Activates when the user explicitly calls `/fowler-refactor-skill` or mentions refactoring with clear intent.
2. **Zero Side-Effect / Backward Compatibility**: Public interfaces (function signatures, props, return types) are preserved 100%. No breaking changes to existing callers. Non-breaking structure is non-negotiable.
3. **Propose before touching**: A refactoring proposal (report) is presented first. Code is modified only after the user approves — or after feedback is incorporated.
4. **One question at a time (`grill-me`)**: If the scope or intent is unclear, ask one focused question with a recommended answer until the three core axes are resolved.

---

## Workflow

```
[1. Requirements Analysis  (grill-me interview)]
                 ↓
[2. Fowler Pattern Mapping  & Proposal Report]
                 ↓
[3. User Feedback Loop  & Approval]
                 ↓
[4. Code Application  & Verification]
```

---

## Step 1 — Requirements Analysis (`grill-me`)

If the target file or refactoring intent is ambiguous, run the interview below.

### Interview Rules
- **One question at a time.**
- Provide a **💡 Recommended answer** with each question.
- If the answer can be found by reading the codebase directly, read it — do not ask.

### Three Core Axes (resolve all three, then stop asking)
1. **Target / Scope** — specific function, component, module, or file
2. **Problem / Code Smell** — what hurts: long function, duplicated logic, deep nesting, tight coupling, etc.
3. **Constraints** — interfaces to preserve, presence of tests, external API contracts

---

## Step 2 — Fowler Pattern Mapping & Proposal Report

Read [references/fowler-patterns.md](./references/fowler-patterns.md) and map the identified smells to the most appropriate patterns. Output the following report:

```markdown
## 🔍 Refactoring Proposal

### 1. Target & Identified Code Smells
- **Target**: `path/to/File.ts`
- **Smells**:
  - 🦨 **[Smell name]** — [why it hurts]

### 2. Recommended Fowler Patterns
- 🎯 **[Pattern name]** — [why this pattern addresses the smell]
- 🎯 **[Pattern name]** — [why this pattern addresses the smell]

### 3. Before vs After Design

#### Before
```ts
// current structure (summarised)
```

#### After
```ts
// refactored structure (interfaces / key extractions)
```

### 4. Compatibility & Side-Effect Guarantee
- **Public interface preserved**: [yes/no + details]
- **Callers impacted**: [none / list]
- **Safety notes**: [defaults, fallbacks, migration notes if any]

### 5. Expected Benefits
- [readability, cohesion, testability, OCP compliance, etc.]
```

---

## Step 3 — Feedback Loop & Approval

- After presenting the proposal, ask the user if they have additional requests or concerns.
- Update the proposal to reflect feedback.
- **Do not touch code** until the user gives explicit approval ("apply", "go ahead", "confirmed", etc.).

---

## Step 4 — Code Application & Verification

Once approved, apply changes in this order:

1. **Non-breaking code changes**
   - Apply the minimum change required.
   - Preserve all public interfaces and call sites.
   - Follow the project's existing style conventions (arrow functions, destructuring, naming, etc.).

2. **Static verification**
   - Run type-check / lint (`lsp_diagnostics` or project's own `tsc --noEmit` / `eslint`) to confirm zero type and reference errors.
   - Confirm existing call sites compile without modification.

3. **Format & organize**
   - Apply the project's formatter (Prettier / Biome / gofmt / rustfmt — whatever is configured) on modified files.

4. **Report**
   - List modified files and summarize what changed and what was intentionally left unchanged.
