---
name: tui-migration
description: >
  Use this skill when migrating a Taiga UI project to a new major version. Before starting,
  confirm with the user which major versions are involved (e.g. v4 → v5). Substitute the source
  version as CURRENT_MAJOR and the target version as NEXT_MAJOR throughout this workflow.
  Also invoke when running migration schematics, handling migration TODOs left after `ng update` or `nx migrate`,
  asked to fix TODOs, clean up migration notes, resolve deprecation warnings, or work with @taiga-ui/legacy package.
  Follow the complete migration workflow: gather context, prepare environment, run schematics, review changes,
  handle TODOs, and troubleshoot common issues. Resolve every actionable TODO only when the surrounding code
  proves the fix is safe; otherwise inspect more context or ask the user before changing behavior, templates,
  styles, or scripts.
---

## Goal

Successfully migrate a Taiga UI project to the next major version while:

- Preserving runtime behavior, template output, styles, and build tooling
- Handling post-schematics TODOs safely and systematically
- Identifying and resolving common migration issues
- Minimizing breaking changes through careful verification

## Step 0: Gather Context Before Acting

**CRITICAL:** Before executing any command or editing any file, collect and confirm the following:

| Question                              | Where to find it                                              |
| ------------------------------------- | ------------------------------------------------------------- |
| Source and target major versions      | Ask the user if not stated                                    |
| Package manager (npm / yarn / pnpm)   | `package.json` → `packageManager` field or lock-file presence |
| Build system (Angular CLI / Nx)       | Presence of `nx.json` or `angular.json`                       |
| Monorepo: how many apps/libs affected | `nx.json` → `projects`, or `angular.json` → `projects`        |
| Custom webpack / ESBuild config       | `angular.json` → `builder` field                              |

**If the Taiga UI MCP server is available**, use `get_migration_guide` now to load the
{CURRENT_MAJOR} → {NEXT_MAJOR} migration notes before proceeding. This gives you
authoritative breaking-change information for the entire session.

**Do not proceed to Phase 1 until every item in the table is resolved.**

## Before You Start - Prerequisites Checklist

- [ ] **Node.js**: Use Node.js LTS version
- [ ] **NPM**: Version 10 or higher (or equivalent for yarn/pnpm)
- [ ] **Current Taiga UI**: Update to the latest version of v{CURRENT_MAJOR} first
- [ ] **Angular**: Update to a version compatible with v{NEXT_MAJOR} (check migration guide)
- [ ] **Prettier**: Set `endOfLine` option to `auto` to prevent line ending issues after migration

> **⛔ NEVER use `--legacy-peer-deps`, `--force`, or any flag that bypasses dependency resolution.**
> These flags hide real version conflicts that will break at runtime. Resolve conflicts explicitly instead.

## Migration Workflow

### Phase 1: Run Migration Schematics

**For Angular CLI projects:**

```bash
ng update @taiga-ui/cdk
```

**For Nx projects:**

```bash
nx migrate @taiga-ui/cdk
nx migrate --run-migrations=migrations.json
```

### Phase 2: Review Changed Code

After schematics complete:

1. **Review all changed code lines** - Some changes contain new code comments (like `// TODO: (Taiga UI migration)`). These comments typically contain instructions for manually migrating deleted entities with new alternatives.

2. **Check for @taiga-ui/legacy imports** - You may find new imports from `@taiga-ui/legacy`. This is a transitional package for outdated entities before their full removal:
   - Everything in this package in v{NEXT_MAJOR} will be removed in v{NEXT_MAJOR+1}
   - You can continue using them temporarily
   - Most deprecated entities have modern alternatives marked with `@deprecated` tag (IDEs display these as stricken-through)
   - **Strongly recommended**: Replace with modern alternatives as soon as possible

### Phase 3: Handle Migration TODOs

Handle post-schematics TODOs without breaking runtime behavior, template output, styles, or build tooling.

#### Core Rules for TODOs

- TODOs are not permission to guess. They are a prompt to verify what is actually safe to change.
- Fix all actionable TODOs in scope, but only after proving each fix from nearby code and usage.
- Prefer the smallest possible change that preserves current behavior.
- Never remove a deprecated package, import, or utility just because a TODO suggests it unless the codebase proves it is unused.
- If a fix could change logic, generated markup, CSS application, or script behavior, validate the surrounding usage first.
- If the safe fix is unclear, ask the user instead of inventing code.

#### TODO Processing Order

Process TODOs starting from shared modules and barrel files (`index.ts`, `public-api.ts`) to unblock consumers, then move to services, components, and finally style entry points. Complete all TODOs in a file before moving to the next one. If a file cannot be completed, add a Quick Entry to MIGRATION_ISSUES.md and continue.

#### TODO Classification → Required Question Template

| Category                        | Stop condition                                 | Question to ask                                                                                            |
| ------------------------------- | ---------------------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| **Template/DI** (high priority) | Direct replacement exists                      | Usually safe to fix without asking                                                                         |
| **Style package removal**       | Any class from that package found in templates | "I found `<className>` used in `<file>`. Should I keep the old style package until these are migrated?"    |
| **No direct replacement**       | TODO explicitly says so                        | "The migration notes say `<API>` was removed with no direct replacement. What behavior should replace it?" |
| **Dynamic binding**             | `[input]="expr"` where expr is runtime value   | "The binding `[appearance]="mode"` uses a runtime value. Should the new API accept the same values?"       |
| **Multiple valid paths**        | More than one replacement exists in docs       | "Two replacements exist: `<A>` and `<B>`. Which one matches your intended behavior?"                       |
| **Warning-only**                | TODO indicates manual decision needed          | "This TODO requires your decision: `<TODO text>`. What is your preferred approach?"                        |

**Classification examples:**

- `TODO: replace TuiButtonModule with TuiButton` → **Template/DI** (high priority, usually safe)
- `TODO: remove @taiga-ui/styles import` → **Style package** (STOP, check usage first)
- `TODO: migrate to standalone component API` → **TypeScript** (medium priority, check consumers)
- `TODO: this API was removed, no direct replacement` → **Warning-only** (ask user)

#### TODO Workflow

1. **Identify and classify the TODO** using the table above
2. **Look up the replacement using MCP (if available):**
   - For component replacements: call `get_component_example` with the new component name
   - For architectural changes: call `get_overview` or `migration_guide`
   - Skip this step only if the replacement is unambiguous from local code context alone
3. **Trace real usage before editing anything:**
   - Search the current component, template, styles, and nearby files for direct references
   - For style-related TODOs, follow the Style Package Removal algorithm below
   - Confirm whether the TODO targets one site or a broader pattern
4. **Decide whether the TODO is safely actionable:**
   - If there is a one-to-one replacement and it preserves behavior, apply it
   - If a deprecated package is mentioned, check whether any runtime, template, or style usage still depends on it before deleting it
   - If multiple replacements are plausible, or the fix depends on dynamic bindings or generated output, stop and ask the user using the question template
5. **Apply the smallest safe fix:**
   - Keep changes localized
   - Avoid broad refactors unless they are required to preserve behavior
   - Do not remove imports, packages, or scripts unless the surrounding evidence supports that removal
6. **Verify the result:**
   - Re-read the touched area to make sure logic, classes, and selectors still line up
   - Run the narrowest available check for the affected slice when possible
   - If the change still feels ambiguous after verification, do not expand the patch; ask the user

### Phase 4: Troubleshooting

#### Problem: TypeScript errors TS6133 - variable is declared but its value is never read

**Solution:** Migration schematics don't include code formatting on purpose (it would slow down execution). Use your IDE or linter:

- **WebStorm**: Right-click on root folder → "Optimize imports" (removes all unused imports recursively)
- **Visual Studio Code**: Use "Organize Imports" folder source action across all files recursively
- **ESLint/Prettier**: Run well-optimized rules to clean up unused imports

#### Problem: Yarn users or legacy-peer-deps workaround needed

**Solution:** Taiga UI depends on many Taiga Family packages. Yarn and pnpm do not automatically install transitive peer dependencies. Manually check each Taiga UI package's `package.json` and install missing peer dependencies.

#### Problem: Cannot resolve dependency for ng-web-apis, maskito, ng-polymorpheus, or ng-event-plugins

**Solution:** Same as above - manually install transitive peer dependencies by checking each Taiga UI package's `package.json`

#### Problem: `Cannot find module 'ts-morph'` error after `nx migrate --run-migrations`

**Solution:** This is an Nx issue with the ng migrate command. Either:

- Bump Nx version, or
- Run `npm install` followed by re-running the migration

#### Problem: FATAL ERROR: Reached heap limit Allocation failed - JavaScript heap out of memory

**Solution:** Migration schematics recursively traverse every file and directory, which can be memory-intensive. Increase the memory limit for the Node.js process:

```bash
NODE_OPTIONS="--max-old-space-size=4096" ng update @taiga-ui/cdk
```

#### Problem: Basic `ng update` / `nx migrate` command fails, need to execute schematics manually

**Solution:**

1. Manually update all Taiga UI packages to v{NEXT_MAJOR} in `package.json` (change versions without console commands, then run `npm install`)
2. Verify `node_modules/@taiga-ui/cdk/package.json` contains the v{NEXT_MAJOR} version
3. Execute:

**Angular CLI:**

```bash
ng update @taiga-ui/cdk --from=@taiga-ui/cdk@<old-version> --to=@taiga-ui/cdk@<new-version>
```

**Nx:**

```bash
nx migrate @taiga-ui/cdk --from=@taiga-ui/cdk@<old-version>
nx migrate --run-migrations=migrations.json
```

## Documenting Uncertain or Broken Migration Points

When encountering migration issues that cannot be resolved immediately, create and maintain a dedicated file
(e.g., `MIGRATION_ISSUES.md` or `TODO_MIGRATION.md`) to track all uncertain or potentially broken areas.

### Two-tier Documentation Format

**Quick entry** (for straightforward blockers):

```markdown
- [ ] `src/app/button.component.html:34` — `TuiButtonModule` TODO,
      blocked: dynamic `[appearance]` binding, need user input
```

Use quick entries for:

- Single-file issues with clear blocking reason
- Cases where the question to ask is obvious from the TODO
- Minor style package usage that needs user decision

**Full entry** (only when multiple files affected or behavior change is possible):

Use the 7-field format below for:

- Issues spanning multiple files
- Potential behavior changes
- Complex style package dependencies
- Cases requiring detailed explanation

### Required Format for Full Entry

Each documented issue must include:

1. **File path** - Full relative path to the affected file (or list of files)
2. **Line number** - Exact line where the issue occurs
3. **Original code** - The code snippet before your attempted fix
4. **Issue description** - Clear explanation of what is uncertain or broken
5. **Attempted solutions** - What migration approaches you considered and why they may not work
6. **Potential impact** - What could break if the wrong fix is applied (runtime, template, styles, build)
7. **Migration version** - Which Taiga UI version migration this relates to (if known)

### Example Full Entry Format

````markdown
## Issue #<number>: <Brief description>

**Files:**

- `path/to/component.ts`
- `path/to/component.html`

**Lines:** 42, 15

**Migration:** v4 -> v5

**Original code:**

```typescript
// TODO: migrate to new button API
@Input() mode: 'accent' | 'primary' = 'primary';
```

```html
<button [mode]="mode">Click me</button>
```

**Issue:**
The old `mode` input was replaced with a new directive-based API, but this component
uses dynamic binding that may not be compatible with the new approach.

**Attempted solutions:**

- Direct replacement with `tuiAppearance` - unclear if dynamic values work
- Keeping old API temporarily - requires deprecated module import

**Potential impact:**

- Runtime error if binding fails
- Visual regression if styling is not applied correctly
````

### Workflow Integration

1. **During initial scan:** Create the migration issues file at the start of the migration session
2. **When blocked:** Add a Quick Entry before moving to the next TODO
3. **Before asking user:** Reference the documented entry in your question
4. **After resolution:** Mark the entry as resolved with a brief note about the applied fix

## Definition of Done

**The migration session is complete when ALL of the following are true:**

- [ ] No `// TODO: (Taiga UI migration)` comments remain in source files, OR each remaining TODO has a corresponding entry in MIGRATION_ISSUES.md
- [ ] No imports from `@taiga-ui/legacy` exist, OR each remaining import is explicitly accepted by the user
- [ ] `ng build` / `nx build` completes without errors
- [ ] No new TypeScript errors were introduced (TS6133 unused-import errors are acceptable — resolve via IDE as described in Phase 4)
- [ ] All entries in MIGRATION_ISSUES.md have been shown to the user

**Do not refactor, rename, or improve code beyond what migration requires.**

## When to Ask the User

Use the question templates from the TODO Classification table for all TODO-related decisions.

Additionally, ask when:

- Migration schematics failed or produced unexpected errors
- The project has custom configurations that may affect migration
- Step 0 context cannot be determined automatically
- A peer-dependency conflict cannot be resolved by aligning Taiga UI package versions

## What Not to Do

- **Do not use `--legacy-peer-deps`, `--force`, or any flag that bypasses dependency resolution, and do not add `legacy-peer-deps=true` to `.npmrc` if it was not already there** — these hide real version conflicts that will break the migration at runtime; resolve conflicts explicitly instead
- Do not hardcode a fix based only on the TODO text
- Do not delete deprecated dependencies first and discover breakage later
- Do not rewrite unrelated code while chasing a migration TODO
- Do not suppress TODOs with a new warning if the actual fix is already known and safe
- Do not continue if you cannot explain why the change is safe from the local code context
- Do not skip the prerequisites checklist - ensure environment is properly prepared
- Do not skip Step 0 (Gather Context) - know your environment before acting
