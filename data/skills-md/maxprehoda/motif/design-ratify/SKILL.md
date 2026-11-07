---
name: design-ratify
description: "Turns settled design decisions into Tailwind theme tokens, a DESIGN.md file that states the rules for future agents, and short written notes for the decisions that are expensive to reverse. Use as phase 3 of design-system, after design-grill."
---

# Design Ratify

Write the decisions from `design-grill` into three things: design tokens, a `DESIGN.md` file, and short notes on the decisions that would be hard to change later.

## Before you start

```bash
test -f .design/decisions.json || echo "MISSING"
```

Stop if the file is missing or if any decision in it is still open.

## 1. Tokens

Tokens are named values, like `--color-primary` or `--radius-lg`, that the code uses instead of raw numbers. Check the Tailwind version recorded in `drift.json`, then write them in the matching place.

**Tailwind v4**: an `@theme` block in the main CSS file.

```css
@theme {
  --spacing: 0.25rem;
  --text-xs: 0.75rem;   --text-xs--line-height: 1.6;
  --text-base: 1rem;    --text-base--line-height: 1.6;
  --text-3xl: 1.953rem; --text-3xl--line-height: 1.2;
  --radius-lg: 0.5rem;
  --color-primary: oklch(0.55 0.22 264);
  --ease-out: cubic-bezier(0.16, 1, 0.3, 1);
  --duration-micro: 150ms;
}
```

**Tailwind v3**: `theme.extend` in `tailwind.config.js`. If `components.json` exists, keep shadcn/ui's `hsl(var(--x))` color format. Don't upgrade the project from v3 to v4 here.

Rules:

- Name tokens for what they're for, not what they look like. Use `--color-primary`, not `--color-blue-600`. A token named after its value becomes wrong the first time the value changes.
- Calculate related values from each other instead of listing each one, so changing one number updates the set. For example: `--radius-sm: calc(var(--radius-lg) - 2px)`.
- Only write tokens for decisions in `decisions.json`. Don't add tokens nobody chose.

## 2. DESIGN.md

Write this file at the root of the repo. Agents load it before future design work, so keep it easy to scan: use tables, put each rule before the reason for it, and skip any introduction.

```markdown
# Design System

Character: dense and productive. Decided <date>.

## Spacing, 4px grid
| Token | Value | Use |
|---|---|---|
| `1` | 4px | icon gaps, tight inline spacing |
| `2` | 8px | padding inside controls |
...
**Never** use one-off spacing values like `p-[13px]`. If no token fits, the scale needs changing. Change the scale.

## Type, 1.250 scale, 6 sizes
| Token | Size | Line height | Use |
...
Bigger text gets tighter line height.

## Color, named roles only
| Role | Means |
|---|---|
| `primary` | the main action on the screen |
| `muted-foreground` | secondary information |
...
**Never** use Tailwind colors directly, like `text-neutral-700`. Use the role.

## Motion
`ease-out` when entering, `ease-in` when leaving. 150ms for small interactions, 250ms standard, 400ms for large ones.

## Enforcement
`npm run design-lint`. CI fails if the number of findings goes above the baseline.
```

Give each category its own **Never** line. Agents follow rules that are written out. They don't reliably work them out from examples.

## 3. Decision notes

Write a note in `.design/records/NNNN-short-name.md` only for these decisions, or for any decision where `decisions.json` shows the user chose something other than the recommendation:

- how tokens are named
- the spacing grid
- the type scale
- the color format
- how dark mode works
- the component library

Each note covers the situation, the decision, what it means for the project, and what would make it worth revisiting. Keep it under 30 lines.

Don't write notes for individual values. Changing one color is a one-line edit.

## 4. Check the result

```bash
npx tailwindcss -i <input.css> -o /tmp/t.css 2>&1 | tail -5
```

Make sure the tokens compile. Then check that every decision in `decisions.json` shows up in the tokens, and tell the user about any that don't.
