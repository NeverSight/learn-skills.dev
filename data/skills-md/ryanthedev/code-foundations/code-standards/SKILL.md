---
name: code-standards
description: "Generates or updates docs/code-standards.md by scanning the codebase for actual conventions. Produces an example-rich standards file optimized for LLM consumers, grounded in the project's real patterns. Not for auditing one file's naming, comments, or clarity (use code-clarity-and-docs)."
user-invocable: false
---

# Skill: code-standards

Generate or update `docs/code-standards.md` — a project-specific conventions file optimized for LLM consumers.

LLMs default to training-data averages. Without project-specific guidance, they produce generic code that passes tests but fails review. This skill extracts the patterns that matter: concrete examples, forbidden patterns, and exemplar file pointers.

---

## Workflow

### 1. Detect

Check for existing standards file:

```
1. Look for docs/code-standards.md (or legacy docs/code-patterns.md)
2. If legacy exists: migrate path (rename to docs/code-standards.md)
```

### 2. Decide: Skip, Update, or Generate

**If file exists**, read the `<!-- base-commit: ... -->` header and check staleness:

```bash
git rev-list <base-commit>..HEAD --count
```

| Commits since | Action |
|---------------|--------|
| 0 | **Skip** — file is current, return it as-is |
| 1–20 | **Update** — spot-check recent diffs (`git diff <base-commit>..HEAD`), update changed sections only |
| 21+ | **Generate** — full re-scan, regenerate entire file |

**If file exists but has no `<!-- base-commit: ... -->` header**, the sha is unknown, or the repo is not a git repo: treat as **Generate**.

**If file missing**, proceed to full **Generate**.

### 3. Scan

Search the codebase for conventions. Adapt searches to what the project actually contains — not every section applies to every codebase.

**Search strategy per section:**

| Section | What to grep/glob for |
|---------|----------------------|
| Forbidden Patterns | Linter configs, eslint-disable comments, TODO/HACK comments |
| Code Examples | Covered by other searches — select best do/don't pairs found |
| Error Handling | try/catch, Result types, error classes, `.catch()` |
| Imports & Dependencies | Import statements, barrel files, dependency direction |
| Testing Patterns | Test files, helpers, fixtures, mocks |
| Naming | Variable/function/file naming across 5+ files |
| File Organization | Directory structure, co-location patterns |
| Technology Decisions | Package files, config files, framework imports |
| Exemplar Files | Well-structured files that demonstrate multiple conventions |

**Scan breadth over depth** — sample across the codebase rather than exhaustively cataloging one directory.

**For Update mode:** Only search sections where recent diffs show changes to relevant patterns.

### 4. Write

Read the section templates before writing: `Read(${CLAUDE_PLUGIN_ROOT}/skills/code-standards/references/section-templates.md)`

**File format:**

```markdown
<!-- base-commit: [HEAD sha] -->
<!-- generated: [YYYY-MM-DD] -->

# Code Standards

[sections per templates]
```

**Core rules:**
- Every section MUST contain at least one code snippet or file pointer. Descriptions without examples waste tokens and don't anchor behavior.
- Separate the rule from the example. State the constraint, then show the code. Never weave constraints into narrative prose — constraints dissolve in paragraphs (NLD-P, 2602.22790).
- Examples should explain WHY the pattern works, not just show the code. Interpretable examples outperform raw code blocks (CL4SE, 2602.23047).
- Only document what deviates from mainstream conventions. "Use meaningful variable names" is noise.
- Show the project's way, not the textbook way. Extract from actual code, don't invent idealized examples.
- Shorter is better. A 200-line file that's all signal beats a 500-line file with filler.

Write to `docs/code-standards.md`. Do NOT commit the file.

### 5. Verify

After writing, self-check:

- [ ] Every section has a code snippet or file pointer
- [ ] No section is pure prose without an example
- [ ] base-commit header matches current HEAD
- [ ] File is under 300 lines (warn if over, trim filler)
- [ ] No generic advice the LLM already knows

---

## Sections

Nine sections. Contrastive sections (DO/DON'T) come first — they resist confirmation bias and anchor behavior more reliably than descriptive sections (2603.18740). Not all sections apply to every project — skip where you find no meaningful conventions.

1. **Forbidden Patterns** — Anti-patterns with rationale and correct alternative
2. **Code Examples** — 2-3 do/don't pairs showing the most important conventions
3. **Error Handling** — The project's specific strategy
4. **Imports & Dependency Direction** — Ordering, what can import what
5. **Testing Patterns** — Framework, helpers, fixtures
6. **Naming Conventions** — Variables, functions, files, modules
7. **File Organization** — Where new things go, co-location rules
8. **Technology Decisions** — Non-obvious choices and constraints only
9. **Exemplar Files** — Pointers to "gold standard" files for common tasks

See the templates file for detailed format per section.

---

## Chain

| From | To |
|------|-----|
| plan (codebase scan step) | Returns `docs/code-standards.md` path |
| build-agent (discovery phase) | Reads the file directly |
