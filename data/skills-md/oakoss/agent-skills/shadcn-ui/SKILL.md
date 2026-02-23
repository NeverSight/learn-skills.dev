---
name: shadcn-ui
description: 'Builds accessible, customizable component libraries using shadcn/ui with Radix UI or Base UI, Tailwind CSS 4, and React 19. Covers component ownership, oklch CSS theming, type-safe forms with Field and Zod, CLI workflows, and registry patterns. Use when adding shadcn/ui components, configuring themes, building forms with Zod, creating custom registries, or composing accessible component variants. Use for shadcn CLI, dark mode, component variants, form validation.'
license: MIT
metadata:
  author: oakoss
  version: '1.0'
  source: 'https://ui.shadcn.com/docs'
---

# shadcn/ui

## Overview

Guides building accessible, customizable UI with shadcn/ui as a code generation platform (not an npm dependency). Components are copied into your project via the CLI and fully owned. Supports Radix UI or Base UI primitives, Tailwind CSS 4 with oklch color tokens, React 19 direct ref patterns, and type-safe form validation with the Field component and Zod.

**When to use:** Adding shadcn/ui components, theming with CSS variables and oklch colors, building forms with React Hook Form or TanStack Form, creating custom registries, composing accessible component variants, setting up dark mode.

**When NOT to use:** Non-React frameworks (use shadcn-vue or shadcn-svelte instead), projects using a different component library (MUI, Chakra), projects not using Tailwind CSS.

## Quick Reference

| Pattern              | API / Approach                             | Key Points                                            |
| -------------------- | ------------------------------------------ | ----------------------------------------------------- |
| Init project         | `npx shadcn@latest init`                   | Auto-detects framework, configures CSS variables      |
| Add component        | `npx shadcn@latest add [name]`             | Copies source code into your project                  |
| Custom project       | `npx shadcn@latest create`                 | Pick library (Radix/Base UI), style, theme, fonts     |
| Check updates        | `npx shadcn@latest diff [component]`       | Shows upstream changes for your components            |
| Search registry      | `npx shadcn@latest search @registry`       | Browse and install from namespaced registries         |
| Build registry       | `npx shadcn@latest build`                  | Generate registry JSON from `registry.json`           |
| Theme tokens         | `:root` vars + `@theme inline` mapping     | oklch color values, dark mode via `.dark` class       |
| Dark mode            | `@custom-variant dark (&:is(.dark *))`     | Swaps CSS variables under `.dark` selector            |
| Component variant    | `cva()` from `class-variance-authority`    | Type-safe variant definitions                         |
| Polymorphic slot     | `asChild` prop with `<Slot>` from Radix    | Merge props onto child element                        |
| Direct ref           | `ref` as a regular prop                    | `forwardRef` is deprecated in React 19                |
| Form (current)       | `<Field />` + React Hook Form + Zod        | Replaces legacy `<Form />` component                  |
| Form (legacy)        | `<Form />` + `<FormField />` + Zod         | Still works but no longer actively developed          |
| Class merging        | `cn()` utility wrapping `clsx` + `twMerge` | Safely merge Tailwind classes without conflicts       |
| Toast / notification | Sonner (`npx shadcn@latest add sonner`)    | Default notification approach; auto-dismiss, stacking |
| Init with blocks     | `npx shadcn@latest init sidebar-01`        | Bootstrap project with pre-built page blocks          |
| RTL support          | `dir="rtl"` on root element                | Built-in RTL layout support for all components        |
| New components       | `Spinner`, `Kbd`, `ButtonGroup`            | Recently added utility and layout components          |

## Common Mistakes

| Mistake                                                   | Correct Pattern                                                         |
| --------------------------------------------------------- | ----------------------------------------------------------------------- |
| Installing shadcn/ui as an npm dependency                 | Use the CLI (`npx shadcn@latest add`) to copy source into your project  |
| Using `forwardRef` with React 19 components               | Pass `ref` directly as a prop -- `forwardRef` is deprecated in React 19 |
| Using HSL values for color tokens                         | Use oklch format: `--primary: oklch(0.205 0 0)`                         |
| Wrapping variables with `hsl()` or `oklch()` in utilities | Reference CSS variables directly: `var(--primary)`                      |
| Putting tokens directly in `@theme {}`                    | Use `:root` for values + `@theme inline` to map them to Tailwind        |
| Using legacy `<Form />` for new forms                     | Use `<Field />` component with React Hook Form or TanStack Form         |
| Skipping Zod validation in form components                | Always pair forms with Zod schemas for type-safe validation             |
| Using `div` elements for interactive controls             | Use Radix or Base UI primitives for semantic HTML and accessibility     |
| Modifying components in `node_modules`                    | Components live in your source tree -- own and customize directly       |
| Using old CLI command `shadcn-ui@canary`                  | Use `npx shadcn@latest` for all CLI operations                          |

## Delegation

- **Component discovery and primitive lookup**: Use `Explore` agent
- **Theme migration or multi-file refactoring**: Use `Task` agent
- **Design system architecture planning**: Use `Plan` agent
- **Registry setup and distribution**: Use `Task` agent

> If the `tanstack-form` skill is available, delegate advanced form state management (array fields, linked fields, async validation) to it.
> If the `tailwind` skill is available, delegate utility class patterns and design token architecture to it.

## References

- [Theming and dark mode](references/theming-and-dark-mode.md)
- [Component patterns and variants](references/component-patterns.md)
- [Form patterns with Field, React Hook Form, and Zod](references/form-patterns.md)
- [CLI and registry](references/cli-and-registry.md)
