---
name: eslint
description: Lints JavaScript and TypeScript code, configures rules, and fixes issues automatically. Use when linting code, fixing style issues, configuring eslint.config.js, or enforcing code quality standards.
---

# ESLint

Pluggable linting for JavaScript and TypeScript.

## Installation

```bash
bun add -D eslint @eslint/js typescript-eslint globals
```

## Running ESLint

```bash
eslint .                   # Lint all files
eslint --fix .             # Auto-fix issues
eslint src/file.ts         # Specific file
eslint --format json .     # JSON output
eslint --format stylish .  # Styled output
```

## Configuration (Flat Config - ESLint 9+)

### eslint.config.js (Recommended)

```javascript
import js from "@eslint/js";
import tseslint from "typescript-eslint";
import globals from "globals";

export default tseslint.config(
  js.configs.recommended,
  ...tseslint.configs.recommended,
  {
    languageOptions: {
      globals: {
        ...globals.node,
        ...globals.es2022,
      },
    },
  },
  {
    ignores: ["dist/", "node_modules/", "*.config.js"],
  },
);
```

### eslint.config.js (Strict TypeScript)

```javascript
import js from "@eslint/js";
import tseslint from "typescript-eslint";
import globals from "globals";

export default tseslint.config(
  js.configs.recommended,
  ...tseslint.configs.strictTypeChecked,
  ...tseslint.configs.stylisticTypeChecked,
  {
    languageOptions: {
      globals: {
        ...globals.node,
        ...globals.es2022,
      },
      parserOptions: {
        projectService: true,
        tsconfigRootDir: import.meta.dirname,
      },
    },
  },
  {
    ignores: ["dist/", "node_modules/"],
  },
);
```

## Common Rules

### TypeScript Rules

```javascript
{
  rules: {
    "@typescript-eslint/no-unused-vars": ["error", { argsIgnorePattern: "^_" }],
    "@typescript-eslint/no-explicit-any": "warn",
    "@typescript-eslint/explicit-function-return-type": "off",
    "@typescript-eslint/no-floating-promises": "error",
    "@typescript-eslint/consistent-type-imports": ["warn", {
      prefer: "type-imports",
      fixStyle: "separate-type-imports"
    }],
  }
}
```

### JavaScript Rules

```javascript
{
  rules: {
    "no-console": ["warn", { allow: ["warn", "error"] }],
    "no-var": "warn",
    "no-unused-vars": ["error", { argsIgnorePattern: "^_" }],
  }
}
```

## File-Specific Configuration

```javascript
export default tseslint.config(
  js.configs.recommended,
  ...tseslint.configs.recommended,
  {
    files: ["src/**/*.ts"],
    rules: {
      "@typescript-eslint/no-explicit-any": "error",
    },
  },
  {
    files: ["tests/**/*.ts"],
    rules: {
      "@typescript-eslint/no-explicit-any": "off",
    },
  },
  {
    ignores: ["dist/", "node_modules/"],
  },
);
```

## Ignore Patterns

```javascript
{
  ignores: ["dist/", "node_modules/", "*.config.js", "coverage/", "build/"];
}
```

## React Plugin

```bash
bun add -D eslint-plugin-react eslint-plugin-react-hooks eslint-plugin-react-refresh
```

```javascript
import reactPlugin from "eslint-plugin-react";
import reactHooks from "eslint-plugin-react-hooks";
import reactRefresh from "eslint-plugin-react-refresh";

export default tseslint.config(
  // ...base config
  {
    plugins: {
      react: reactPlugin,
      "react-hooks": reactHooks,
      "react-refresh": reactRefresh,
    },
    rules: {
      ...reactPlugin.configs.recommended.rules,
      ...reactHooks.configs.rules,
      "react-refresh/only-export-components": "warn",
    },
  },
);
```

## CI Integration

### GitHub Actions

```yaml
name: Lint
on: [push, pull_request]
jobs:
  eslint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: oven-sh/setup-bun@v2
      - run: bun install
      - run: bun run lint
```
