---
name: design-enforce
description: "Installs a lint script that works in any framework and flags one-off bracket values, hex codes, off-scale spacing and font sizes, and Tailwind colors used instead of named roles. Builds its config from the project's own tokens, records a baseline so CI only fails when things get worse, and can check shadcn/ui components. Use as phase 5 of design-system, after design-apply."
---

# Design Enforce

Install a lint script that flags any value outside the design system, using the project's own tokens as its rules.

## Why a script and not an ESLint rule

ESLint rules read JavaScript and JSX. They can't see Svelte markup, Vue templates, Astro files or plain HTML. `assets/design-lint.mjs` reads files as plain text, so it works the same in every framework and needs no plugins.

## Install

```bash
mkdir -p .design scripts
cp <skill>/assets/design-lint.mjs scripts/design-lint.mjs
```

Add it to `package.json`:

```json
{ "scripts": { "design-lint": "node scripts/design-lint.mjs" } }
```

## Config

Write `.design/lint.config.json` using the values in `DESIGN.md`, not the defaults built into the script.

```json
{
  "include": ["src"],
  "extensions": [".svelte", ".tsx", ".jsx", ".vue", ".astro", ".html"],
  "spacingScale": ["0", "1", "2", "3", "4", "6", "8", "12", "16"],
  "textScale": ["xs", "sm", "base", "lg", "xl", "2xl", "3xl"],
  "radiusScale": ["none", "sm", "md", "lg", "full"],
  "semanticColors": ["background", "foreground", "primary", "muted", "accent", "card", "destructive", "border"],
  "allowRawPalette": false,
  "exceptions": []
}
```

`spacingScale` and `textScale` must match `DESIGN.md` exactly. If they don't, the linter enforces a different system from the one the docs describe.

## Rules

| Rule | Level | What it flags |
|---|---|---|
| `arbitrary-value` | error | one-off bracket values like `p-[13px]` or `w-[327px]` |
| `raw-hex` | error | hex codes like `#3b82f6` in markup |
| `off-scale-spacing` | error | spacing like `p-7` when 7 isn't one of the spacing sizes |
| `off-scale-text` | error | font sizes like `text-7xl` that aren't in the type scale |
| `raw-palette` | warning | Tailwind colors like `text-neutral-700` used instead of a named role |
| `off-scale-radius` | warning | one-off corner radius like `rounded-[3px]` |

Errors make the script exit with a failure. Warnings don't.

Keep `raw-palette` as a warning while the code is being migrated, and change it to an error after batch 3 of `design-apply` is done. Tell the user this is the plan when you install it.

## Baseline

On an existing codebase, the first run usually finds hundreds or thousands of problems.

Save that number as the baseline in `.design/lint.config.json`, and set CI to fail only when the count goes above it. Don't make CI fail on every finding. A check that can never pass gets switched off, and a switched-off check looks like it's working while catching nothing.

Lower the baseline as each `design-apply` batch lands.

## Exceptions

Put `// design-lint-disable` on a line to skip it, and always include a reason in the comment. Without a reason, nobody can tell later whether the exception is still needed.

## shadcn/ui components

Do this only if `components.json` exists.

shadcn/ui copies component source files into the repo instead of installing them as a package. Over time they drift away from the originals and from each other. And a problem inside a shared component spreads: a Tailwind color hard-coded in `ui/button` ends up on every button in the product.

Follow the four steps in `references/shadcn-alignment.md`: fix `components.json`, check the files in `ui/` for hard-coded values and local edits, replace hand-built components that duplicate shadcn ones, and treat findings inside `ui/` as errors.

## Optional extras

Offer these, but don't install them without asking.

A pre-commit hook:

```bash
echo 'npm run design-lint --quiet' >> .husky/pre-commit
```

A CI step that runs `npm run design-lint`.

## Report

Give the number of findings per rule, the three files with the most findings, and the baseline. Say which rules currently fail the build and which only warn.
