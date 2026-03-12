---
name: react-linter-setup
description: "Sets up ESLint for React and TypeScript projects aligned with company standards. Use when installing or configuring the project linter, adding devDependencies, custom ESLint rules, package.json scripts, or when the user asks to set up or migrate to the company React/TypeScript ESLint stack."
metadata:
  keywords: "eslint, setup, install, react, typescript, lint config, package.json, devDependencies, custom rules"
---

# React & TypeScript linter setup

This skill handles **project setup** for the company ESLint stack: installing dependencies, adding config files, custom rules, and `package.json` scripts. For applying and enforcing rules on existing code, use a coding-standards or review skill when available.

## When to use this skill

- User wants to **install** or **configure** ESLint in a React/TypeScript project.
- User asks to **add** lint scripts, devDependencies, or ESLint flat config.
- User wants **custom rules** (e.g. TODO ticket reference) or to **migrate** to the company config.
- User mentions "setup linter", "eslint config", "lint setup", "add eslint to project".

## Prerequisites

- Project has a `package.json` (npm or yarn).
- Project has a `tsconfig.json` (or `tsconfig.app.json`) at the root — required for `projectService: true` in the config.
- Node.js 18+ (for ESLint 10 and flat config).

## Setup checklist

Follow this order. Reference files are in `assets/` and `references/`.

### 1. Dependencies

Install the listed devDependencies (see [assets/package.json.snippet.json](assets/package.json.snippet.json) for **example** versions and structure). Prefer **current compatible versions** in real projects — the snippet is for illustration only. Merge into the project `package.json` or run:

```bash
yarn add -D eslint @eslint/js typescript-eslint eslint-plugin-react eslint-plugin-react-hooks eslint-plugin-testing-library globals
```

(or equivalent `npm install -D ...`). See [references/dependencies-and-scripts.md](references/dependencies-and-scripts.md) for package list, example versions, and rationale.

### 2. ESLint config and TODO ticket rule (flat config — ESLint 9+)

- Copy [assets/eslint.config.js](assets/eslint.config.js) to the **project root** (it includes the TODO ticket reference rule).
- Copy [assets/eslint-rules/todo-ticket-ref.js](assets/eslint-rules/todo-ticket-ref.js) to the repo (e.g. `eslint-rules/todo-ticket-ref.js`).
- Ensure `globalIgnores` match the project (e.g. `dist`, generated code). Adjust the rule `pattern` for your ticketing tool (e.g. JIRA) if needed.

### 3. Scripts

Add to `package.json` `scripts` (same as in [assets/package.json.snippet.json](assets/package.json.snippet.json); versions in that file are examples only):

```json
"lint": "eslint .",
"lint:fix": "eslint . --fix"
```

Use `yarn` or `npm` consistently with the rest of the project.

### 4. Verify

- Run `yarn lint` or `npm run lint`.
- Fix any environment issues (missing tsconfig, wrong ignores, parser options).

See [assets/README.md](assets/README.md) for file list and quick reference.

## Rules applied (summary)

The default config applies common React/TypeScript rules:

- **Coding**: `no-explicit-any`, `prefer-const`, `eqeqeq`, `no-nested-ternary`, `no-empty` (catch), `no-useless-catch`, `prefer-nullish-coalescing`, `consistent-indexed-object-style`, `max-depth`
- **React**: `no-array-index-key`, `jsx-fragments`, `react-hooks/*`
- **Tests**: `testing-library/prefer-screen-queries`

## Reference files

| Purpose              | File                                                                 |
| -------------------- | -------------------------------------------------------------------- |
| Dependencies & scripts | [references/dependencies-and-scripts.md](references/dependencies-and-scripts.md) |
| Assets overview      | [assets/README.md](assets/README.md)                                |

## Rules of thumb

- **One config at root**: Use a single `eslint.config.js` at the project root (flat config).
- **Match package manager**: Use `yarn` or `npm` consistently for install and scripts.
- **Ignore generated code**: Add generated or third-party paths to `globalIgnores` to avoid noisy violations.
- **TypeScript required**: The config uses `projectService: true`; do not use this skill for non-TypeScript projects without adapting the config.
