---
name: tui-setup
description: Set up Taiga UI in an Angular project. Use when Taiga UI components are needed but the project has no @taiga-ui packages, or when tui-root / Taiga styles / providers are missing.
---

# Taiga UI setup

## 1. Check if installed

```bash
grep '@taiga-ui/' package.json
```

Packages present → skip to step 3. Nothing found → step 2.

## 2. Install

```bash
npx ng add taiga-ui --defaults --skip-confirmation
```

This is the only supported install path — do not add `@taiga-ui/*` packages to
`package.json` by hand. The schematic asks which packages to add (`core`,
`kit`, `icons`, `layout`, addons); pick what the task needs, `core` + `kit` is
the usual answer. It also wires up styles, providers and imports itself.

## 3. Verify the wiring

The schematic normally does all of this; check it and fix only what is missing.

- **Styles** — `angular.json` → `architect.build.options.styles` contains
  `@taiga-ui/core/styles/taiga-ui-theme.less` and
  `@taiga-ui/core/styles/taiga-ui-fonts.less`
- **Providers** — `provideTaiga()` is in the application providers:
  ```ts
  import {provideTaiga} from '@taiga-ui/core';
  // ...

  bootstrapApplication(App, {
    providers: [
      provideTaiga(),
      // ...
    ],
  }).catch(console.error);
  ```
  In the default CLI layout the providers array lives in `app.config.ts`.
- **Root wrapper** — the root template (`app.html`) wraps everything in
  `<tui-root>...</tui-root>`, and the root component imports `TuiRoot` from
  `@taiga-ui/core`. Without it portals, dialogs, hints and alerts do not work.

## 4. Confirm

```bash
npx ng build
```


## 5. MCP (if the client is supported)

```bash
npx @taiga-ui/mcp init --client claude    # writes .mcp.json
npx @taiga-ui/mcp init --client cursor    # writes .cursor/mcp.json
npx @taiga-ui/mcp init --client vscode    # writes .vscode/mcp.json
npx @taiga-ui/mcp init --client windsurf  # writes ~/.codeium/windsurf/mcp_config.json (global only)
npx @taiga-ui/mcp init --client opencode  # writes opencode.json
npx @taiga-ui/mcp init --client codex     # writes .codex/config.toml
```

Build passes → setup is done.
