---
name: building-components
description: Builds, restructures, and standardizes React components according to project conventions (placement, folder/file naming, exports, props patterns). Use when adding components or when reorganizing existing components during refactors, migrations, or component moves.
---

# Creating Components

## Workflow

Copy this checklist and track progress:

```
Component Progress:
- [ ] Step 1: Determine placement
- [ ] Step 2: Create folder structure
- [ ] Step 3: Create component file
- [ ] Step 4: Add sub-components (if needed)
- [ ] Step 5: Validate against checklist
- [ ] Step 6: Run lint fix and re-check
```

**Step 1: Determine placement**

Infer from context if possible, otherwise ask the user. 
See [references/placement.md](references/placement.md) for paths and conventions for each type:

- Shared (common) component
- Page-specific component
- Sub-component of existing component
- Page component

**Step 2: Create folder structure**

Create a kebab-case folder in the appropriate location. 
See [references/folder-structures.md](references/folder-structures.md) for diagrams of each scenario.

**Step 3: Create component file**

Create a PascalCase `.tsx` file inside the folder.
Follow the conventions in [references/REFERENCE.md](references/REFERENCE.md).

**Step 4: Add sub-components (if needed)**

If the component needs sub-components, create a `components/` folder inside it.
Each sub-component follows the same rules. See [references/placement.md](references/placement.md) for the sub-component pattern.

**Step 5: Validate against checklist**

Run through the validation checklist below before considering the component complete.

**Step 6: Run lint fix and re-check**

Run linter with auto-fix scoped only to the created or modified files. If errors remain after auto-fix, notify the user that manual fixes are required and stop — do NOT suppress errors with `eslint-disable`, `@ts-ignore`, `@ts-expect-error`, or any other suppression directives.

---

## Validation checklist

After creating a component, verify every item:

### Naming
- [ ] Folder name is kebab-case (e.g., `card-content`)
- [ ] File name is PascalCase and matches the exported component (e.g., `CardContent.tsx` exports `CardContent`)
- [ ] File is inside its own folder (not loose in a parent directory)

### Exports
- [ ] Uses named export: `export const ComponentName: React.FC<Props>`
- [ ] No default exports
- [ ] One component per file

### Props
- [ ] Props defined as `type Props` (not `interface`)
- [ ] Props ordered: required → optional → function callbacks
- [ ] `React.FC<Props>` used (or `React.FC` if no props)

### Structure
- [ ] Component placed in the correct directory (common vs page-specific)
- [ ] Sub-components live in a `components/` subfolder, not alongside the parent
- [ ] Implicit return used when the body is JSX-only

### Files
- [ ] Optional helper files (`types.ts`, `constants.ts`, `helpers.ts`, `index.ts`) created only if needed

### Linting
- [ ] Lint was run for changed component files
- [ ] Lint auto-fix was run
- [ ] No new lint errors remain in touched files

