---
name: architecture-md
description: >-
  Generate an ARCHITECTURE.md file for a codebase following matklad's principles.
  Use when asked to "write an architecture doc", "create ARCHITECTURE.md", "document the
  architecture", "explain the codebase structure", "write a codemap", or when onboarding
  contributors to a project. Based on https://matklad.github.io/2021/02/06/ARCHITECTURE.md.html
  and modeled after rust-analyzer's architecture doc.
---

# ARCHITECTURE.md Generator

Generate high-quality ARCHITECTURE.md files that give newcomers a mental map of a codebase.
Based on matklad's article: the biggest contributor bottleneck is not writing code, it's
figuring out *where* to change it. ARCHITECTURE.md bridges that gap.

## Core Principles

1. **Short and stable** -- Only describe things unlikely to change frequently. Don't synchronize with code. Revisit a couple of times a year.
2. **Bird's eye first** -- Start with the problem being solved, not the solution.
3. **Codemap over prose** -- Answer "where's the thing that does X?" and "what does this thing do?" for every module.
4. **Name, don't link** -- Name important files, modules, types. Don't hyperlink (links go stale). Encourage symbol search.
5. **Invariants are gold** -- Explicitly call out what's deliberately *absent*. Important invariants are often expressed as absence, and are impossible to divine from reading code.
6. **Mark boundaries** -- API boundaries between layers constrain all possible implementations behind them. Finding a boundary by randomly reading code is hard.
7. **Cross-cutting concerns last** -- After the codemap, address things that are everywhere and nowhere (error handling, testing, config).

## Workflow

### Step 1: Explore the Codebase

Use `tree`, glob, and read tools to understand the project:

- Read README, package.json/Cargo.toml/pyproject.toml for the project's purpose
- Run `tree -L 2 -d` (or similar) to see directory structure
- Identify entry points (main files, index files, bin directories)
- Read key files at module boundaries to understand the layers

### Step 2: Identify the Architecture

Map out:

- **The problem being solved** -- What does this project do? What's the input/output?
- **Coarse-grained modules** -- What does each top-level directory/package do?
- **Data flow** -- How does data move through the system? Input -> ??? -> Output
- **API boundaries** -- Which modules are public interfaces vs internal implementation?
- **Architectural invariants** -- What rules are enforced by structure? What's deliberately absent?
- **Cross-cutting concerns** -- Error handling, testing strategy, configuration, observability

### Step 3: Write the ARCHITECTURE.md

Follow the template below. Keep the total document under ~300 lines for most projects.

## Template

```markdown
# Architecture

[One paragraph: what this project does at the highest level. What problem it solves.]

## Bird's Eye View

[How data flows through the system at the coarsest level.
Input -> Processing stages -> Output.
Keep this to 1-3 paragraphs.]

## Code Map

[Brief intro: "This section describes the high-level structure of the codebase.
Pay attention to **Boundary** and **Invariant** callouts."]

### `path/to/module-a/`

[What this module does in 1-3 sentences. Key types: `ImportantType`, `AnotherType`.]

**Boundary:** [If this is an API boundary, say so and what it means.]

**Invariant:** [What's deliberately absent or enforced. E.g., "This module never does I/O"
or "Nothing here depends on the HTTP layer."]

### `path/to/module-b/`

[Repeat for each significant module.]

### `path/to/module-c/`

[...]

## Cross-Cutting Concerns

### Error Handling

[How errors are handled across the codebase. Is it Result-based? Exceptions?
Do errors propagate or get caught at boundaries?]

### Testing

[Testing strategy. Where do tests live? What kinds of tests exist?
What are the important test boundaries?]

### [Other concerns as applicable]

[Configuration, observability/logging, code generation, build system, etc.
Only include sections that are genuinely cross-cutting.]
```

## Rules

### What to Include

- Directory/module purposes (1-3 sentences each)
- Names of important types, traits, interfaces, functions (for symbol search)
- API boundaries between layers
- Architectural invariants -- especially things that are deliberately *absent*
- Data flow at the system level
- Cross-cutting concerns that affect multiple modules

### What to Omit

- Implementation details of how individual modules work (that's inline doc)
- Links to specific files or lines (they go stale)
- Anything that changes with routine PRs
- Exhaustive API documentation (that's rustdoc/typedoc/javadoc territory)
- Setup instructions (that's README)
- Contribution guidelines (that's CONTRIBUTING.md)

### Style Rules

- Use `### \`path/to/module/\`` headers with backtick-quoted paths for the codemap
- Use **Boundary:** and **Invariant:** prefixed callouts (bold label, not blockquotes)
- Keep module descriptions to 1-3 sentences
- Name types in backticks: "Key types: `FooBar`, `BazQux`"
- Write in present tense, active voice
- Prefer concrete over abstract: "parses CLI arguments" not "handles input processing"

## Quality Checklist

Before finishing, verify:

- [ ] Can a newcomer find "the thing that does X" using only this doc?
- [ ] Are API boundaries clearly marked?
- [ ] Are architectural invariants (especially absences) called out?
- [ ] Is every section stable enough to survive 6 months without update?
- [ ] Are important types/modules named (not linked)?
- [ ] Is there a bird's eye view before the codemap?
- [ ] Are cross-cutting concerns addressed?
- [ ] Does the codemap order match the data flow or dependency direction?
- [ ] Is it under ~300 lines? (Shorter = more likely to be read and maintained)

## Reference Example

See [references/example.md](references/example.md) for a complete example ARCHITECTURE.md
for a hypothetical TypeScript project, demonstrating all the patterns above.
