---
name: react-icons
description: Use this skill when adding, fixing, replacing, refactoring, or standardizing icons with react-icons in React, Next.js, Vite, CRA, JavaScript, or TypeScript projects. Covers correct imports, icon family choice, accessibility, styling, bundle-conscious usage, and inline SVG migration.
license: MIT
compatibility: React, Next.js, Vite, CRA, JavaScript, TypeScript, npm, pnpm, yarn, bun
metadata:
  author: MD Abu Abdullah
  package: react-icons
  official: false
---

# React Icons Skill

Use this skill to make practical, maintainable `react-icons` changes in existing React codebases. Treat the project you are editing as the source of truth: inspect its package manager, styling system, icon conventions, accessibility patterns, and framework before adding or changing icons.

This skill is unofficial and is not maintained by the official React Icons project.

## When to use this skill

Use this skill when:

- The user asks to add icons to a React, Next.js, Vite, CRA, JavaScript, or TypeScript project.
- The user asks to replace hardcoded SVG markup with `react-icons`.
- The user has broken `react-icons` imports, missing icons, or incorrect icon names.
- The user wants brand icons for GitHub, React, X/Twitter, LinkedIn, npm, Vercel, or similar services.
- The user wants consistent icon styling across a page, sidebar, toolbar, form, dashboard, or design system.
- The user wants accessible icon buttons, decorative icons, status icons, or loading indicators.
- The user wants to convert hardcoded SVG or one-off icon components into reusable icon components.

## Core rules

- Import icons from subpackages, never from the root `react-icons` package.
- Prefer exact named imports for the icons being used.
- Keep the icon family consistent inside a UI area unless there is a specific reason to mix families.
- Prefer Simple Icons from `react-icons/si` for brand and product logo icons.
- Use `aria-hidden="true"` for decorative icons.
- Use `aria-label` or visible text for icon-only buttons.
- Prefer `currentColor` and `className` for styling so icons inherit text color and design-system states.
- Detect the package manager from lockfiles before installing: `package-lock.json` -> npm, `pnpm-lock.yaml` -> pnpm, `yarn.lock` -> yarn, `bun.lockb` or `bun.lock` -> bun.
- Do not install `@react-icons/all-files` unless the user explicitly asks for that package.

## Install commands

Only install `react-icons` in the target application, not in this skill repository.

Use the command matching the project's package manager:

```sh
npm install react-icons
```

```sh
pnpm add react-icons
```

```sh
yarn add react-icons
```

```sh
bun add react-icons
```

## Correct import examples

Use subpackage imports:

```tsx
import { FaGithub } from "react-icons/fa";

export function GithubLink() {
  return (
    <a href="https://github.com" className="inline-flex items-center gap-2">
      <FaGithub aria-hidden="true" />
      <span>GitHub</span>
    </a>
  );
}
```

```tsx
import { Fa6XTwitter } from "react-icons/fa6";

export function XLink() {
  return <Fa6XTwitter aria-label="X" />;
}
```

```tsx
import { FiSearch } from "react-icons/fi";

export function SearchFieldIcon() {
  return <FiSearch aria-hidden="true" className="search-field__icon" />;
}
```

```tsx
import { LuSettings } from "react-icons/lu";

export function SettingsIcon() {
  return <LuSettings aria-hidden="true" size={20} />;
}
```

```tsx
import { MdHome } from "react-icons/md";

export function HomeNavIcon() {
  return <MdHome aria-hidden="true" className="nav__icon" />;
}
```

```tsx
import { SiReact } from "react-icons/si";

export function ReactBadge() {
  return (
    <span className="tech-badge">
      <SiReact aria-hidden="true" />
      <span>React</span>
    </span>
  );
}
```

## Incorrect imports

Do not import from the root package:

```tsx
import { FaGithub } from "react-icons";
```

Replace that with the correct family subpackage import.

## Choosing icon families

Choose icons in this order:

- Use the icon family already present in the same project or UI area first.
- For SaaS dashboards, admin panels, and dense product UI, prefer Lucide (`react-icons/lu`), Tabler (`react-icons/tb`), or Feather (`react-icons/fi`).
- For Material UI style apps, prefer Material Design icons (`react-icons/md`).
- For brand and product logos, prefer Simple Icons (`react-icons/si`).
- For Bootstrap-style UI, prefer Bootstrap Icons (`react-icons/bs`).
- For GitHub-like UI, prefer Octicons (`react-icons/go`).

Use `references/icon-prefixes.md` for common families, import paths, prefix examples, and best-fit guidance.

## Accessibility rules

Use `references/accessibility.md` when deciding whether an icon is decorative, named by visible text, an icon-only control, a loading indicator, or a status signal.

Default patterns:

- Decorative icon next to visible text: set `aria-hidden="true"` on the icon.
- Icon-only button: put the accessible name on the button with `aria-label`.
- Status icon: include visible text such as "Success", "Error", or "Warning"; do not rely on icon shape or color alone.

## Styling rules

- Use `className` when the project uses SCSS, BEM, CSS Modules, Tailwind, or a design system.
- Use the `size` prop for simple one-off cases.
- Avoid hardcoded icon colors unless the user or design system requires a fixed brand/status color.
- Prefer `currentColor` by setting color on the parent element or CSS class.
- Keep common sizes predictable: `16`, `18`, `20`, and `24` are good defaults.
- Icon-only buttons need accessible names even if the icon visually communicates the action.
- Keep hover, active, disabled, focus, and dark-mode states on the button or parent class when possible.

Example:

```tsx
import { FiSearch } from "react-icons/fi";

export function SearchButton() {
  return (
    <button className="icon-button" aria-label="Search">
      <FiSearch aria-hidden="true" className="icon-button__icon" />
    </button>
  );
}
```

```scss
.icon-button {
  color: var(--color-text-muted);
}

.icon-button:hover {
  color: var(--color-text);
}

.icon-button__icon {
  width: 20px;
  height: 20px;
}
```

## Next.js rules

Use `references/nextjs.md` for App Router guidance.

React Icons are React components and can be used in App Router projects. A component only needs `"use client"` if the surrounding component uses client-only behavior such as state, effects, browser APIs, event handlers, or client-only library behavior. Do not add `"use client"` only because an icon is imported.

Keep imports specific:

```tsx
import { FiSearch } from "react-icons/fi";
```

Avoid dynamic imports unless there is a real bundle or performance reason.

## Refactoring inline SVGs

When migrating inline SVGs to `react-icons`:

1. Identify what the SVG means: search, close, menu, settings, GitHub brand, warning status, and so on.
2. Choose a matching icon from the existing project family first.
3. Preserve size, stroke or fill behavior, `className`, layout, hover states, focus states, and disabled states.
4. Preserve accessibility behavior: decorative icons stay hidden; meaningful icons keep an accessible name or visible text.
5. Remove unused SVG code, local icon components, imports, CSS selectors, and test snapshots that only existed for the old SVG.

Use `references/migration-examples.md` for before/after examples.

## TypeScript examples

Normal icon:

```tsx
import { FiSearch } from "react-icons/fi";

export function SearchIcon() {
  return <FiSearch aria-hidden="true" size={20} />;
}
```

Icon-only button:

```tsx
import { FiSearch } from "react-icons/fi";

type SearchButtonProps = {
  onClick: () => void;
};

export function SearchButton({ onClick }: SearchButtonProps) {
  return (
    <button type="button" aria-label="Search" onClick={onClick}>
      <FiSearch aria-hidden="true" size={20} />
    </button>
  );
}
```

Reusable `IconButton` accepting an icon as `React.ComponentType`:

```tsx
import type { ComponentType } from "react";
import { FiSearch } from "react-icons/fi";

type IconComponent = ComponentType<{
  "aria-hidden"?: boolean;
  className?: string;
  size?: number | string;
}>;

type IconButtonProps = {
  label: string;
  icon: IconComponent;
  onClick: () => void;
};

export function IconButton({ label, icon: Icon, onClick }: IconButtonProps) {
  return (
    <button type="button" aria-label={label} onClick={onClick}>
      <Icon aria-hidden="true" size={20} />
    </button>
  );
}

export function SearchAction() {
  return <IconButton label="Search" icon={FiSearch} onClick={() => {}} />;
}
```

If the project does not use the automatic JSX runtime or does not already import React types globally, add the needed type import:

```tsx
import type { ComponentType } from "react";

type IconComponent = ComponentType<{
  "aria-hidden"?: boolean;
  className?: string;
  size?: number | string;
}>;
```

## Common fixes

Module not found:

- Check whether `react-icons` is installed in the target app.
- Install it with the detected package manager.
- Make sure the import path is a valid subpackage such as `react-icons/fi`, `react-icons/fa`, `react-icons/fa6`, `react-icons/lu`, or `react-icons/si`.

Wrong icon name:

- Verify the icon exists in the selected family.
- Pay attention to prefixes: Feather icons use `Fi`, Lucide uses `Lu`, Simple Icons uses `Si`, Font Awesome 6 uses `Fa6`.
- If the exact icon does not exist, choose the closest match from the same family before mixing families.

Wrong subpackage:

- Match the component prefix to the import path.
- `FiSearch` comes from `react-icons/fi`, not `react-icons/fa`.
- `Fa6XTwitter` comes from `react-icons/fa6`, not `react-icons/fa`.

Too many mixed icon families:

- Inventory the imports in the file or UI area.
- Pick the dominant family unless brand icons require Simple Icons or Font Awesome.
- Replace outliers with equivalent icons from the dominant family.

Hydration concerns caused by unrelated client-only behavior:

- Do not blame `react-icons` by default. Icons are deterministic React components.
- Look for client-only state, browser APIs, dates, random values, local storage, theme initialization, or conditional rendering around the icon.
- Add `"use client"` only to components that actually need client behavior.

Icon color is not changing:

- Check whether CSS targets `color` on the icon or parent, not only `fill` or `stroke`.
- Most `react-icons` components use `currentColor`, so setting `color` through a class is usually enough.
- Avoid inline fixed colors when the icon should respond to hover, theme, or disabled states.

## Agent checklist

Before finishing:

- Confirm `react-icons` is installed if the target app needs it.
- Confirm imports are from subpackages.
- Confirm there are no root `react-icons` icon imports.
- Confirm the icon family is consistent within each UI area.
- Confirm decorative icons are hidden from screen readers.
- Confirm icon-only buttons have accessible labels.
- Confirm unused SVG code and imports are removed.
- Confirm TypeScript passes if the project uses TypeScript.
- Confirm lint passes if the project has a lint command.
