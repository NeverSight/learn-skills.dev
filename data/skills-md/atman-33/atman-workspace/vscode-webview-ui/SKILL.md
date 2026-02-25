---
name: vscode-webview-ui
description: Develop React applications for VS Code Webview surfaces. Use when working on the `webview-ui` package, creating features, components, or hooks for VS Code extensions. Includes project structure, coding guidelines, and testing instructions.
---

# VS Code Webview UI

## Overview

This skill assists in developing the React application that powers VS Code webview surfaces. It covers the `webview-ui` workspace, which is bundled with Vite and communicates with the extension host via the `bridge/vscode` helper.

## Project Structure

The `webview-ui` package follows this structure:

```
webview-ui/
├── src/
│   ├── components/        # Shared visual components reused across features
│   │   └── ui/            # shadcn/ui component library
│   ├── hooks/             # Shared React hooks
│   ├── features/
│   │   └── {feature}/
│   │       ├── index.tsx  # Feature entry component rendered from routing
│   │       ├── components/# Feature-specific components
│   │       └── hooks/     # Feature-specific hooks
│   ├── bridge/            # Messaging helpers for VS Code <-> webview
│   └── index.tsx          # Runtime router that mounts the selected feature
├── public/                # Static assets copied verbatim by Vite
├── vite.config.ts         # Vite build configuration
└── README.md
```

## Coding Guidelines

- **Shared Modules**: Prefer shared modules under `src/components` and `src/hooks` before introducing feature-local code.
- **Feature Boundaries**: Add feature-only utilities inside the nested `components/` or `hooks/` directories to keep boundaries clear.
- **Styling**: Keep styling in Tailwind-style utility classes (see `src/app.css` for base tokens) and avoid inline styles when reusable classes exist.
- **Messaging**: Exchange messages with the extension via `vscode.postMessage` and subscribe through `window.addEventListener('message', …)` inside React effects.
- **Configuration**: When adding new steering or config references, obtain paths through the shared `ConfigManager` utilities from the extension layer.

## Testing & Quality

- **Integration Tests**: Use Playwright or Cypress style integration tests if adding complex interactions (tests live under the repo-level `tests/`).
- **Pre-commit Checks**: Run `npm run lint` and `npm run build` before committing to ensure TypeScript and bundler checks pass.
