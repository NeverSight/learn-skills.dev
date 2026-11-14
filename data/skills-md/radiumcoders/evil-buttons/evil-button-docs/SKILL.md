---
name: evil-button-docs
description: Generate and verify Evil Buttons component documentation and registry wiring. Use when adding a new button/component to this repo, creating or updating `content/docs/*.mdx`, adding the component to `scripts/build-registry.mjs`, exposing MDX preview components, or fixing `npm run registry:test` failures for missing docs or stale registry JSON.
---

# Evil Button Docs

Use this skill to add a new Evil Buttons component to the docs and shadcn registry without missing the project-specific glue.

## Workflow

1. Read the component in `components/evil-buttons/<file>.tsx` and identify:
   - public component name and export style
   - props, defaults, dependencies, registry dependencies, and import path
   - visual behavior worth showing in docs previews
2. Create or update `content/docs/<slug>.mdx`.
   - Use `scripts/generate-docs.mjs` to scaffold a page when starting from scratch.
   - Keep the install command as `<Cmd>@evilbuttons/<registry-name></Cmd>`.
   - Include a `<PreviewCard live>` using the real component (swapped for the dial-backed preview with prop controls when one exists in `components/landing/previews`).
3. Add the preview component to `components/mdx-custom-components.tsx` if the MDX page references it.
4. Add the item to `scripts/build-registry.mjs`.
   - Read the source file with `readFile`.
   - Create a registry item with embedded `content`.
   - Add it to `index.items`.
   - Add a `writeFile` call and console output.
5. Generate and verify:
   - `npm run registry:build`
   - `npm run registry:test`
   - `npm run lint`
   - `npm run build`

## Docs Page Shape

Use this order unless the component needs extra notes:

```mdx
---
title: ComponentName
description: One clear sentence matching the registry description.
---

ComponentName is ...

## Preview

<PreviewCard live title="ComponentName" note="Interactive">
  <ComponentName>Deploy Doom</ComponentName>
</PreviewCard>

## Install

Add the item with the shadcn CLI.

<Cmd>@evilbuttons/registry-name</Cmd>

## Usage

```tsx
import { ComponentName } from "@/components/evil-buttons/component-file";

export function ButtonDemo() {
  return <ComponentName>Launch</ComponentName>;
}
```

## Props

| Prop | Type | Default | Description |
| ---- | ---- | ------- | ----------- |

## Registry

The registry item includes `components/evil-buttons/component-file.tsx` and installs ...
```

## Registry Rules

- Use the registry `name` as the shadcn package suffix: `@evilbuttons/<name>`.
- The item file must be generated at `public/r/<name>.json`.
- `scripts/test-registry.mjs` requires every registry item to have an MDX page containing `@evilbuttons/<name>`.
- Keep npm package dependencies in `dependencies`.
- Keep shadcn registry item references in `registryDependencies`.
- Use `components/evil-buttons/<file>.tsx` as `path` and `target`.
- Re-run `npm run registry:build` after editing the registry builder; never hand-edit generated JSON as the source of truth.

## Scaffold Script

Run from the repository root:

```bash
node .agents/skills/evil-button-docs/scripts/generate-docs.mjs \
  --name my-button \
  --title MyButton \
  --description "A concise registry-ready description." \
  --component-file my-button \
  --export named \
  --deps "clsx,tailwind-merge"
```

Use `--doc-slug` when the docs filename differs from the registry name. Use `--registry-deps` for shadcn registry dependencies.

The script refuses to overwrite an existing docs page unless `--force` is passed. Use `--dry-run` to print the generated MDX without writing files.

## Final Checks

Before handing off, confirm:

- The docs page renders with the component imported in `components/mdx-custom-components.tsx`.
- `public/r/index.json` and `public/r/<name>.json` are regenerated.
- `npm run registry:test` reports the item count and passes.
- Any verification command that could not run is reported with the exact reason.
