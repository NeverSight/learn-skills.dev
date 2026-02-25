---
name: asir
description: Asir's opinionated tooling and conventions for JavaScript/TypeScript projects. Use when setting up new projects, configuring ESLint/Prettier alternatives, monorepos, library publishing, or when the user mentions Asir's preferences.
metadata:
  author: Asir
  version: "2026.2.3"
---

# Asir's Preferences

| Category | Preference |
|----------|------------|
| Package Manager | pnpm |
| Language | TypeScript (strict mode, ESM only) |
| Linting & Formatting | `@antfu/eslint-config` (no Prettier) |
| Testing | Vitest |
| Git Hooks | simple-git-hooks + lint-staged |
| Bundler (Libraries) | tsdown |
| Documentation | VitePress |

---

## Core Conventions

### TypeScript Config

```json
{
  "compilerOptions": {
    "target": "ESNext",
    "module": "ESNext",
    "moduleResolution": "bundler",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true
  }
}
```

### ESLint Setup

```js
// eslint.config.mjs
import antfu from '@antfu/eslint-config'

export default antfu()
```

Fix linting errors with `pnpm -r lint --fix`. Do NOT add a separate `lint:fix` script.

For detailed configuration options: [antfu-eslint-config](references/antfu-eslint-config.md)

### Git Hooks

```json
{
  "simple-git-hooks": {
    "pre-commit": "pnpm i --frozen-lockfile --ignore-scripts --offline && npx lint-staged"
  },
  "lint-staged": { "*": "eslint --fix" },
  "scripts": { "prepare": "npx simple-git-hooks" }
}
```

### Vitest Conventions

- Test files: `foo.ts` → `foo.test.ts` (same directory)
- Use `describe`/`it` API (not `test`)
- Use `toMatchSnapshot` for complex outputs
- Use `toMatchFileSnapshot` with explicit path for language-specific snapshots

---

## pnpm Catalogs

Use named catalogs in `pnpm-workspace.yaml` for version management:

| Catalog | Purpose |
|---------|---------|
| `prod` | Production dependencies |
| `inlined` | Bundler-inlined dependencies |
| `dev` | Dev tools (linter, bundler, testing) |
| `frontend` | Frontend libraries |

Avoid the default catalog. Catalog names can be adjusted per project needs.

---

## References

| Topic | Description | Reference |
|-------|-------------|-----------|
| ESLint Config | Framework support, formatters, rule overrides, VS Code settings | [antfu-eslint-config](references/antfu-eslint-config.md) |
| Project Setup | .gitignore, GitHub Actions, VS Code extensions | [setting-up](references/setting-up.md) |
| Library Development | tsdown bundling, pure ESM publishing | [library-development](references/library-development.md) |
| Monorepo | pnpm workspaces, centralized alias, Turborepo | [monorepo](references/monorepo.md) |
| Library Coding Patterns | [library-coding-patients](references/library-coding-patients.md) |
