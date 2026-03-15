---
name: kenshinx-ui
description: Comprehensive UI component library based on Tailwind CSS and shadcn/ui. Use this skill when the user asks to build or style UI using the @kenshinx/ui library, or when you need access to its React components (e.g., Button, Form, Dialog).
---

# @kenshinx/ui

This skill provides access to `@kenshinx/ui`, a complete, accessible, and customizable React UI component library. 

## Quick Start

If `@kenshinx/ui` is not installed in the target project, install it and its peer dependencies first:
```bash
npm install @kenshinx/ui lucide-react class-variance-authority clsx tailwind-merge tailwindcss-animate \
  @radix-ui/react-avatar @radix-ui/react-checkbox @radix-ui/react-collapsible @radix-ui/react-dialog \
  @radix-ui/react-dropdown-menu @radix-ui/react-label @radix-ui/react-popover @radix-ui/react-select \
  @radix-ui/react-slot @radix-ui/react-switch @radix-ui/react-tabs @radix-ui/react-tooltip @radix-ui/react-progress \
  react-hook-form @hookform/resolvers zod recharts react-day-picker date-fns sonner cmdk
```
*(Alternatively, check `scripts/setup.sh` if provided)*

## Components & Usage

For a list of all available `@kenshinx/ui` components and how to import them, read [references/components.md](references/components.md).

## Styling & Theming

To understand how to apply the design system, setup the Tailwind CSS preset, and use the color tokens, read [references/styling.md](references/styling.md).
