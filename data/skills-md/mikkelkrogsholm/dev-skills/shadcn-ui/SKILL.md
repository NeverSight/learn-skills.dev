---
name: shadcn-ui
description: "shadcn/ui — copy-owned React component library built on Radix UI and Tailwind CSS. Use when building with shadcn/ui or asking about its components, CLI, theming, configuration, or integration with Next.js, Vite, Remix, or other frameworks. Fetch live documentation for up-to-date details."
---

# shadcn/ui

shadcn/ui is a collection of accessible, composable React components built on Radix UI primitives and styled with Tailwind CSS — components are copied into your project via CLI, giving you full ownership of the source code.

## Documentation

- **Docs**: https://ui.shadcn.com/llms.txt

## Best Practices

- **Form components include React Hook Form and Zod — do not add separate form libraries.** The `Form` component wraps `react-hook-form` with built-in Zod validation. Adding `formik`, `react-final-form`, or additional validation packages is redundant.
- **`components.json` controls path aliases, Tailwind config, and component style** — always check this file exists and is correctly configured before adding components. An incorrect `tailwind.config` path or missing CSS variable setup in `globals.css` causes components to render without styles.
- **There is no "update all" command** — `shadcn add` and `shadcn diff` operate per-component. When suggesting upgrades, list each component individually; bulk update scripts must be written manually.
