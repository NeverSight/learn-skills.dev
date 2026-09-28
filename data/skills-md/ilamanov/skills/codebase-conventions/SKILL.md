---
name: codebase-conventions
description: Generally-applicable conventions for how code is written and arranged — tooling/package manager, import style, file & component naming, comments, and where files live (colocation vs. global folders). Use whenever creating, naming, moving, or importing a file, running project commands, or deciding where a new module belongs. Consult BEFORE writing the code so the conventions are baked in, not retrofitted. If a convention below matches the work, apply it — don't ask, just follow it (call out the choice in one line so the user can override).
---

# Codebase Conventions

Generally-applicable conventions for how code is written and arranged. **Read every convention below. If any matches what you're about to do, apply it.** These are defaults for the user's projects; where a project clearly already follows a different convention, match the project and say so.

## When to consult this skill

Any time you are:

- Creating a new file, or deciding where a new module (component, hook, util, server action, type, etc.) should live
- Naming a file, component, or export
- Writing an import
- Running a project command (install, build, test, scripts)
- Adding a comment

## Conventions

### File placement & colocation

Treat each feature/route folder as a **self-contained unit** — almost as if it were its own small repo. The closer a feature's code lives to where it's consumed, the easier it is to experiment with, reason about, and eventually move or delete. **Default to colocating; promote to a global folder only when usage is genuinely broad.**

Decide placement by how many features use the code:

- **Used by a single feature/route** → keep it inside that feature's own folder (e.g. a local `components/`, `hooks/`, `actions/`, or `lib/` sub-folder within the feature), right next to its consumer. Don't promote it to a global folder.
- **Shared by a few sibling features** → hoist it to the **nearest common ancestor folder** the consumers share — not all the way to a top-level global folder. Find the lowest folder containing all usages and put it there.
- **Truly global — used across many features** → a root-level shared folder (e.g. `components/`, `lib/`, `hooks/`, `actions/`, or the project's equivalent) is correct.

Additional guidance:

- **Design-system / UI primitives** (the shared component library, e.g. a `components/ui/` folder) stay global regardless of how many features use them.
- **Third-party service init/config clients** (database client, email, vector store, queue, analytics, etc.) belong in the global shared folder — they're cross-cutting infrastructure, not feature code.
- A feature's component staying co-located is correct **even if something outside the feature imports it**. An external import doesn't by itself justify promoting it to a global folder — only broad, multi-feature usage does. Promote only when it has genuinely become shared.

### Tooling & imports

- Use **`pnpm`** for all project commands (install, run scripts, add/remove deps). Don't reach for `npm`/`yarn` unless the project is clearly set up for one of them.
- Use the project's **path alias** (commonly `@/`) for non-relative imports rather than long `../../../` chains. Match whatever alias the project already configures.

### Naming

- **Files** in `kebab-case`.
- **React components** in `PascalCase`.
- **Named exports only** — avoid default exports (except where a framework requires one, e.g. a route/page entry file).

### Comments

- Leave short inline comments next to code that involves **non-obvious assumptions, product-specific logic, repo-specific mechanisms, or anything that isn't industry-standard**. One sentence is enough.
- Do **not** add comments that merely restate what the code already makes clear. If a competent reader would understand it from the code alone, no comment.

## Future conventions

This skill will grow over time. New conventions should be added under the **Conventions** section above, phrased as rules the agent can apply mechanically.
