---
name: shadcn
description: Build, update, debug, and style shadcn/ui components using the project's registry and conventions.
disable-model-invocation: true
allowed-tools: Bash(npx shadcn@latest *), Bash(pnpm dlx shadcn@latest *), Bash(bunx --bun shadcn@latest *)
---

# shadcn/ui

A framework for building ui, components and design systems. Components are added as source code to the user's project via the CLI.

Run CLI commands using the project's package runner: `npx shadcn@latest`, `pnpm dlx shadcn@latest`, or `bunx --bun shadcn@latest`. Determine it from `package.json` and repository conventions before acquiring project context. Examples below use `npx shadcn@latest`; substitute the project's runner.

## Current Project Context

Reuse applicable project context when actual output for the current project is already available. When that output is missing or stale, including on hosts without shell injection, run this from the target project using its package runner. A literal command in a skill is not evidence that it ran:

```bash
npx shadcn@latest info --json
```

Inspect the result for configuration, installed components, and resolved paths. Refresh it when the project, configuration, or installed component set changes, not on every styling edit. If `info` is unavailable, read `package.json`, `components.json`, the relevant installed component source, and theme files directly. State unresolved facts that matter; do not invent injected output or initialize a project merely to obtain context.

## Principles

1. **Use existing components first.** Inspect installed components and nearby usage. Search the resolved registry when a needed component is missing; consult community registries when the request or project context supports that source.
2. **Compose for the requested interface.** Reuse primitives that fit the task and surrounding product instead of imposing a fixed page recipe.
3. **Use built-in variants before custom styles.** `variant="outline"`, `size="sm"`, etc.
4. **Prefer semantic colors.** Use tokens such as `bg-primary` and `text-muted-foreground` for theme roles. Follow explicit design requirements and established project conventions when a different treatment is justified.

## API and Accessibility Requirements

The installed source, types, and selected primitive library define the component API. Preserve required composition, accessible names, keyboard behavior, focus handling, and state semantics. Do not treat a stylistic preference as an API requirement or change a working API merely to match a newer example.

- **Custom triggers:** Use the composition API supported by the project's base and installed component, such as `asChild` for Radix or `render` for Base UI. See [base-vs-radix.md](./rules/base-vs-radix.md) when those bases apply.
- **Overlay names:** Provide an accessible name for Dialog, Sheet, and Drawer through their supported title mechanism. Use `DialogTitle`, `SheetTitle`, or `DrawerTitle`, with `className="sr-only"` when the title should be visually hidden. Preserve focus and keyboard behavior when customizing them.
- **Control semantics:** Label inputs, group related controls semantically, and expose invalid and disabled state through the installed control's supported API. `data-invalid` and `data-disabled` support field styling; they do not replace `aria-invalid` or actual disabled behavior. See [forms.md](./rules/forms.md).
- **Required structure and props:** Preserve the parents and child components required by the installed implementation, such as `TabsTrigger` inside `TabsList` or an InputGroup's specialized input. Verify requirements against the selected base; do not assume every suggested grouping wrapper is mandatory. See [composition.md](./rules/composition.md).
- **Supported loading state:** Inspect the local Button API before using `isPending` or `isLoading`. When those props are absent, compose real pending behavior with the supported spinner, icon placement, and disabled state.

## Styling and Composition Defaults

Use these defaults when they fit the requested design and existing code. They yield to explicit user choices and established project conventions while preserving API and accessibility requirements. Do not report valid alternatives as defects solely because they differ from these examples.

- **Styling:** Prefer built-in variants and semantic tokens, `gap-*` for flex/grid spacing, `size-*` for equal dimensions, `truncate`, and the project's `cn()` utility. Use `className` for layout and justified local styling. Inspect existing overlay stacking before adding an override. See [styling.md](./rules/styling.md) and [customization.md](./customization.md).
- **Forms:** Prefer existing `FieldGroup`/`Field` and `InputGroup` compositions when they fit. Select ToggleGroup, RadioGroup, Checkbox, or Switch by interaction meaning, not option count alone. Preserve semantic grouping with the project's fieldset pattern. See [forms.md](./rules/forms.md).
- **Cards and groups:** Use Card sections for content they actually contain; omit empty descriptions or footers. Use grouping components where their API or the content's relationships call for them. Provide an appropriate avatar fallback when an unavailable image would otherwise lose useful identity. See [composition.md](./rules/composition.md).
- **Feedback and decoration:** Prefer existing Alert, Empty, Separator, Skeleton, and Badge components when their behavior and semantics fit. Preserve the project's established toast implementation. Do not add components or states merely to complete a pattern.
- **Icons:** Follow the configured icon library and the installed component's sizing and placement conventions, including `data-icon` where supported. Customize sizing when the requested design calls for it. Prefer component references over string lookup machinery unless the existing data contract needs identifiers. See [icons.md](./rules/icons.md).
- **Chat:** Reuse MessageScroller, Message, Bubble, Attachment, and Marker when available and suitable. Preserve their required nesting when using them, and prefer their scroll and state APIs over duplicate implementations. Existing chat UI does not need replacement merely because these primitives exist. See [chat.md](./rules/chat.md).

## CLI Conventions

- **Never decode preset codes or build preset URLs manually.** Use `npx shadcn@latest preset decode <code>`, `preset url <code>`, or `preset open <code>`. For project-aware preset detection, use `npx shadcn@latest preset resolve`.
- **Apply preset codes directly with the CLI.** Use `npx shadcn@latest apply <code>` for existing projects, or `npx shadcn@latest init --preset <code>` when initializing.

## Key Patterns

These examples illustrate the defaults above. Styling alternatives are not automatically incorrect; preserve the installed API and the requested design.

```tsx
// Default form layout with the project's Field components.
<FieldGroup>
  <Field>
    <FieldLabel htmlFor="email">Email</FieldLabel>
    <Input id="email" />
  </Field>
</FieldGroup>

// Validation: data-invalid on Field, aria-invalid on the control.
<Field data-invalid>
  <FieldLabel htmlFor="invalid-email">Email</FieldLabel>
  <Input id="invalid-email" aria-invalid aria-describedby="invalid-email-error" />
  <FieldDescription id="invalid-email-error">Invalid email.</FieldDescription>
</Field>

// Icon placement when supported by the installed Button.
<Button>
  <SearchIcon data-icon="inline-start" />
  Search
</Button>

// Prefer gap for a flex layout; preserve an intentional block layout.
<div className="flex flex-col gap-4">...</div>

// Concise equal dimensions.
<Avatar className="size-10" />

// Prefer an existing status presentation when it fits.
<Badge variant="secondary">+20.1%</Badge>
```

## Component Selection

| Need                       | Use                                                                                                 |
| -------------------------- | --------------------------------------------------------------------------------------------------- |
| Button/action              | `Button` with appropriate variant                                                                   |
| Form inputs                | `Input`, `Select`, `Combobox`, `Switch`, `Checkbox`, `RadioGroup`, `Textarea`, `InputOTP`, `Slider` |
| Related toggle options     | `ToggleGroup` + `ToggleGroupItem`, when toggle semantics fit                                         |
| Data display               | `Table`, `Card`, `Badge`, `Avatar`                                                                  |
| Navigation                 | `Sidebar`, `NavigationMenu`, `Breadcrumb`, `Tabs`, `Pagination`                                     |
| Overlays                   | `Dialog` (modal), `Sheet` (side panel), `Drawer` (bottom sheet), `AlertDialog` (confirmation)       |
| Feedback                   | `toast` (Base UI), `sonner` (Radix/Aria), `Alert`, `Progress`, `Skeleton`, `Spinner`                 |
| Command palette            | `Command` inside `Dialog`                                                                           |
| Charts                     | `Chart` (wraps Recharts)                                                                            |
| Layout                     | `Card`, `Separator`, `Resizable`, `ScrollArea`, `Accordion`, `Collapsible`                          |
| Empty states               | `Empty`                                                                                             |
| Menus                      | `DropdownMenu`, `ContextMenu`, `Menubar`                                                            |
| Tooltips/info              | `Tooltip`, `HoverCard`, `Popover`                                                                   |
| Chat / conversation UI     | `MessageScroller`, `Message`, `Bubble`, `Attachment`, `Marker`                                      |

## Key Fields

Project context from `info` may contain these fields. When reading configuration directly, establish equivalent facts from the relevant files rather than assuming all fields are present:

- **`aliases`** → use the actual alias prefix for imports (e.g. `@/`, `~/`), never hardcode.
- **`isRSC`** → when `true`, components using `useState`, `useEffect`, event handlers, or browser APIs need `"use client"` at the top of the file. Always reference this field when advising on the directive.
- **`tailwindVersion`** → `"v4"` uses `@theme inline` blocks; `"v3"` uses `tailwind.config.js`.
- **`tailwindCssFile`** → the existing theme stylesheet. Put shared variables with the project's theme owner rather than creating a competing global stylesheet.
- **`style`** → component visual treatment (e.g. `nova`, `vega`).
- **`base`** → the selected primitive library. Affects component APIs and available props; use guidance for that base.
- **`iconLibrary`** → determines icon imports. Use `lucide-react` for `lucide`, `@tabler/icons-react` for `tabler`, etc. Never assume `lucide-react`.
- **`resolvedPaths`** → exact file-system destinations for components, utils, hooks, etc.
- **`framework`** → routing and file conventions (e.g. Next.js App Router vs Vite SPA).
- **`packageManager`** → use this for any non-shadcn dependency installs (e.g. `pnpm add date-fns` vs `npm install date-fns`).
- **`preset`** → resolved preset code and values for the current project. Use `npx shadcn@latest preset resolve --json` when you only need preset information.

See [cli.md — `info` command](./cli.md) for the full field reference.

## Component Docs, Examples, and Usage

Read the installed component and nearby usage first. Run `npx shadcn@latest docs <component>` and fetch the returned documentation when adding an unfamiliar component, changing API-dependent behavior, comparing an upstream update, or resolving an uncertainty the local source does not answer.

```bash
npx shadcn@latest docs button dialog select
```

Reuse documentation already fetched when it still matches the relevant base and component version. A trivial spacing, color, or typography edit does not require fresh documentation when local source and established conventions answer it. Refresh only when relevant context changes or an API question remains. If documentation cannot be retrieved, continue from adequate local evidence and disclose any material gap.

## Resolve the Registry

Honor an explicitly named registry or item address. Otherwise inspect `components.json`, documented conventions, nearby component provenance, and earlier user decisions. Use the established source when that evidence is unambiguous, and state the choice briefly. Several configured registries do not imply a preferred one; ask only when the remaining alternatives would materially change the component or source.

Read-only searches across plausible configured sources may help establish the choice. Resolve the concrete registry before adding an item, using a qualified namespace, GitHub item address, or URL where needed to express it. Do not silently install a component from a different registry because it has the same name. See [registry.md](./registry.md) for address semantics.

## Workflow

Use only the steps relevant to the task. A local styling edit may need no registry search, installation, or preset operation.

1. **Get project context** — reuse applicable observed context or acquire it as described above. Do not assume shell injection ran.
2. **Check installed components first** — before running `add`, always check the `components` list from project context or list the `resolvedPaths.ui` directory. Don't import components that haven't been added, and don't re-add ones already installed.
3. **Resolve the registry and find components** — follow [Resolve the Registry](#resolve-the-registry), then search the chosen source when needed.
4. **Resolve API questions** — consult local source and applicable documentation using the criteria above. Use `npx shadcn@latest view` to browse registry items you haven't installed. To preview changes to installed components, use `npx shadcn@latest add --diff`.
5. **Install or update** — `npx shadcn@latest add`. When updating existing components, use `--dry-run` and `--diff` to preview changes first (see [Updating Components](#updating-components) below).
6. **Fix imports in third-party components** — After adding components from community registries (e.g. `@bundui`, `@magicui`), check the added non-UI files for hardcoded import paths like `@/components/ui/...`. These won't match the project's actual aliases. Use `npx shadcn@latest info` to get the correct `ui` alias (e.g. `@workspace/ui/components`) and rewrite the imports accordingly. The CLI rewrites imports for its own UI files, but third-party registry components may use default paths that don't match the project.
7. **Review added components** — Read the added files and verify imports, required composition, and [API and accessibility requirements](#api-and-accessibility-requirements). Match icon imports and styling to the requested design and project conventions. Fix concrete defects without treating every departure from a stylistic default as one.
8. **Switching presets** — Inspect the current and incoming presets before choosing the operation. Honor an already-authorized choice of **overwrite**, **partial**, **merge**, or **skip**. Ask only when the request leaves a material choice unresolved or the actual overwrite scope exceeds authorization; make the affected files and theme/configuration changes concrete first.
   - **Inspect current preset**: `npx shadcn@latest preset resolve`. Use `--json` when you need structured values.
   - **Inspect incoming preset**: `npx shadcn@latest preset decode <code>`. Use `preset url <code>` or `preset open <code>` to share or open the preset builder.
   - **Overwrite**: `npx shadcn@latest apply <code>`. Overwrites detected components, fonts, and CSS variables.
   - **Partial**: `npx shadcn@latest apply <code> --only theme,font`. Updates only the selected preset parts without reinstalling UI components. Supported values are `theme` and `font`; comma-separated combinations are allowed. `icon` is intentionally not supported, because icon changes may require full component reinstall and transforms.
   - **Merge**: `npx shadcn@latest init --preset <code> --force --no-reinstall`, then run `npx shadcn@latest info` to list installed components, then for each installed component use `--dry-run` and `--diff` to [smart merge](#updating-components) it individually.
   - **Skip**: `npx shadcn@latest init --preset <code> --force --no-reinstall`. Only updates config and CSS, leaves components as-is.
   - **Important**: Always run preset commands inside the user's project directory. `apply` only works in an existing project with a `components.json` file. The CLI automatically preserves the current base (`base` vs `radix`) from `components.json`. If you must use a scratch/temp directory (e.g. for `--dry-run` comparisons), pass `--base <current-base>` explicitly — preset codes do not encode the base.

## Updating Components

When the user asks to update a component from upstream while keeping their local changes, use `--dry-run` and `--diff` to intelligently merge. **NEVER fetch raw files from GitHub manually — always use the CLI.**

1. Run `npx shadcn@latest add <component> --dry-run` to see all files that would be affected.
2. For each file, run `npx shadcn@latest add <component> --diff <file>` to see what changed upstream vs local.
3. Compare the affected files, dependencies, theme, and configuration with the user's authorized scope. Update unchanged upstream files within that scope; merge customized files while preserving local behavior unless replacing those customizations was explicitly authorized. A general request to update everything does not by itself authorize discarding custom work.
4. Use `--overwrite` only when every file it will replace is in scope and any loss of local customizations is explicitly authorized. Authorization may come from the initial request or an earlier approval of the concrete replacement; do not ask for it again. If the preview reveals additional affected files or customization loss outside that scope, ask only for the missing decision and preserve those files until it is resolved.

## Quick Reference

```bash
# Create a new project.
npx shadcn@latest init --name my-app --preset base-nova
npx shadcn@latest init --name my-app --preset a2r6bw --template vite

# Create a monorepo project.
npx shadcn@latest init --name my-app --preset base-nova --monorepo
npx shadcn@latest init --name my-app --preset base-nova --template next --monorepo

# Initialize existing project.
npx shadcn@latest init --preset base-nova
npx shadcn@latest init --defaults  # shortcut: --template=next --preset=nova (base style implied)

# Apply a preset to an existing project.
npx shadcn@latest apply a2r6bw
npx shadcn@latest apply a2r6bw --only theme
npx shadcn@latest apply a2r6bw --only font
npx shadcn@latest apply a2r6bw --only theme,font

# Inspect preset codes and project preset state.
npx shadcn@latest preset decode a2r6bw
npx shadcn@latest preset url a2r6bw
npx shadcn@latest preset open a2r6bw
npx shadcn@latest preset resolve
npx shadcn@latest preset resolve --json

# Add components.
npx shadcn@latest add button card dialog
npx shadcn@latest add @magicui/shimmer-button
npx shadcn@latest add owner/repo/item
npx shadcn@latest add --all

# Preview changes before adding/updating.
npx shadcn@latest add button --dry-run
npx shadcn@latest add button --diff button.tsx
npx shadcn@latest add @acme/form --view button.tsx
npx shadcn@latest add owner/repo/item --dry-run

# Search registries.
npx shadcn@latest search @shadcn -q "sidebar"
npx shadcn@latest search @tailark -q "stats"
npx shadcn@latest search owner/repo -q "login"
npx shadcn@latest search                          # all configured registries
npx shadcn@latest search @shadcn -q "menu" -t ui  # filter by item type

# Get component docs and example URLs.
npx shadcn@latest docs button dialog select

# View registry item details (for items not yet installed).
npx shadcn@latest view @shadcn/button
npx shadcn@latest view owner/repo/item
```

**Named presets:** `nova`, `vega`, `maia`, `lyra`, `mira`, `luma`
**Templates:** `next`, `vite`, `start`, `react-router`, `astro` (all support `--monorepo`) and `laravel` (not supported for monorepo)
**Preset codes:** Version-prefixed base62 strings (e.g. `a2r6bw` or `b0`), from [ui.shadcn.com](https://ui.shadcn.com).

## Detailed References

- [rules/forms.md](./rules/forms.md) — FieldGroup, Field, InputGroup, ToggleGroup, FieldSet, validation states
- [rules/composition.md](./rules/composition.md) — Groups, overlays, Card, Tabs, Avatar, Alert, Empty, Toast, Separator, Skeleton, Badge, Button loading
- [rules/chat.md](./rules/chat.md) — MessageScroller, Message, Bubble, Attachment, Marker; streaming, anchoring, jump-to-latest
- [rules/icons.md](./rules/icons.md) — data-icon, icon sizing, passing icons as objects
- [rules/styling.md](./rules/styling.md) — Semantic colors, variants, className, spacing, size, truncate, dark mode, cn(), z-index
- [rules/base-vs-radix.md](./rules/base-vs-radix.md) — asChild vs render, Select, ToggleGroup, Slider, Accordion
- [cli.md](./cli.md) — Commands, flags, presets, templates
- [registry.md](./registry.md) — Authoring source registries, `include`, item definitions, dependencies, GitHub registry rules
- [customization.md](./customization.md) — Theming, CSS variables, extending components
