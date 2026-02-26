---
name: react-coding-standards
description: "Enforces internal React and TypeScript coding standards using avoid/prefer rules. Use when reviewing or refactoring React/TS code, applying company standards, or when the user asks to align code with coding standards."
metadata:
  keywords: "avoid, prefer, React, TypeScript, naming, patterns, tests, lint"
---

# React & TypeScript coding standards

This skill applies company coding standards expressed as **Avoid** (anti-patterns) and **Prefer** (recommended patterns) across many reference categories. When invoked on code, follow the two-phase workflow below.

## Reference categories

Standards are defined in the `references/` folder. Load these files when you need the exact Avoid/Prefer rules and examples:

| Category            | File                                                                         | Scope                                                                |
| ------------------- | ---------------------------------------------------------------------------- | -------------------------------------------------------------------- |
| **Coding patterns** | [references/common-coding-patterns.md](references/common-coding-patterns.md) | TypeScript (types, control flow, errors, enums, destructuring, etc.) |
| **Naming patterns** | [references/common-naming-patterns.md](references/common-naming-patterns.md) | File/folder names (kebab-case, suffixes/prefixes), boolean prefixes   |
| **React patterns**  | [references/common-react-patterns.md](references/common-react-patterns.md)   | Hooks, components, JSX, state, styling, fragments                    |
| **Unit testing**    | [references/common-unit-testing.md](references/common-unit-testing.md)       | Jest, React Testing Library, AAA, mocks, selectors                   |

## Two-phase workflow

When the skill is invoked on code (selected files, git staged files, branch):

### Phase 1 — Collect violations

1. **Analyze** the provided code against all available reference files.
2. **Audit file and folder names** in scope against [references/common-naming-patterns.md](references/common-naming-patterns.md) (kebab-case, suffixes/prefixes by intent, folder structure). List every file or folder that does **not** match as a violation with category **"File and folder naming"**, current path, and the preferred name/path.
3. **Identify** every other place where the code matches an **Avoid** pattern described in those references.
4. **List** each violation in a single report with:
   - **Category** (file and folder naming / coding / naming / React / unit testing)
   - **Rule name** (e.g. “Avoid Using `any` for Type Definitions” or “File/folder not kebab-case”)
   - **Location** (file and line or snippet)
   - **Short reason** (what is wrong)

5. If no Avoid pattern is found, state that the code complies and stop. Otherwise proceed to Phase 2.

### Phase 2 — Apply corrections

1. **Always start with file and folder renames.** Do not skip this step. For every violation in the report with category **"File and folder naming"**: rename the file or folder to the preferred name/path from the reference, then update all import paths that reference it. If the report had no file/folder naming violations, explicitly confirm that file and folder names were checked and comply. Only then proceed to in-file corrections.
2. For **each** remaining violation from the report (excluding file/folder naming):
   - Open the corresponding reference file and find the **Prefer** section paired with that Avoid rule.
   - Apply the recommended correction (refactor) so the code follows the Prefer pattern.
3. **Preserve** business logic and behavior; only change structure, naming, or patterns.
4. **Prefer minimal edits**: one logical change per violation, no unnecessary rewrites.
5. When several standards apply to the same area, prioritize in this order:
   - TypeScript safety (types, `any`, optional params)
   - Naming clarity (boolean prefixes, descriptive names)
   - React architecture (hooks, components, state, keys)
   - Testing structure (AAA, screen queries, mocks)

## Rules of thumb

- **Strict avoid/prefer**: Only treat as violations what is explicitly described as Avoid in the reference files; only apply fixes that are explicitly described as Prefer there.
- **File/folder renames are mandatory**: When the Phase 1 report includes "File and folder naming" violations, Phase 2 must start by applying those renames and updating imports—never skip to in-file edits.
- **One violation, one fix**: One Avoid → one corresponding Prefer; do not mix multiple rules in a single edit unless they target the same line.
- **Readability and maintainability**: After corrections, the code should be easier to read and maintain, without changing behavior.

## Quick reference

- **Collect first**: Always complete the full list of Avoid violations before making edits (including the file/folder naming audit).
- **Files and folders first**: Phase 2 must begin with file and folder renames when the report lists "File and folder naming" violations; never apply in-file corrections before renames and import updates.
- **Then redress**: Apply each Prefer in turn, using the reference file as the source of truth for the exact pattern and examples.
