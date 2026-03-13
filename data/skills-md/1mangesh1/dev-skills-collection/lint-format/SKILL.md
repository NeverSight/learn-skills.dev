---
name: lint-format
description: Linting and formatting setup with ESLint, Prettier, Ruff, Black, and EditorConfig. Use when user asks to "set up linting", "configure ESLint", "add Prettier", "format code", "set up Ruff", "fix lint errors", "add editorconfig", or any code quality tooling tasks.
---

# Lint & Format

Set up linting and formatting for consistent code quality.

## ESLint (JavaScript/TypeScript)

### Setup (Flat Config - ESLint 9+)

```bash
npm init @eslint/config@latest
# or
npm install -D eslint @eslint/js typescript-eslint
```

```javascript
// eslint.config.js
import js from "@eslint/js";
import tseslint from "typescript-eslint";

export default [
  js.configs.recommended,
  ...tseslint.configs.recommended,
  {
    rules: {
      "no-unused-vars": "off",
      "@typescript-eslint/no-unused-vars": ["error", { argsIgnorePattern: "^_" }],
      "@typescript-eslint/no-explicit-any": "warn",
      "no-console": ["warn", { allow: ["warn", "error"] }],
    },
  },
  {
    ignores: ["dist/", "node_modules/", "*.config.js"],
  },
];
```

### With React

```bash
npm install -D eslint-plugin-react eslint-plugin-react-hooks
```

```javascript
// eslint.config.js
import react from "eslint-plugin-react";
import reactHooks from "eslint-plugin-react-hooks";

export default [
  // ...base config
  {
    plugins: { react, "react-hooks": reactHooks },
    rules: {
      ...reactHooks.configs.recommended.rules,
      "react/react-in-jsx-scope": "off",
      "react/prop-types": "off",
    },
    settings: {
      react: { version: "detect" },
    },
  },
];
```

### Run

```bash
npx eslint .
npx eslint --fix .
npx eslint src/
npx eslint "src/**/*.{ts,tsx}"
```

## Prettier

### Setup

```bash
npm install -D prettier eslint-config-prettier
```

```json
// .prettierrc
{
  "semi": true,
  "singleQuote": false,
  "tabWidth": 2,
  "trailingComma": "all",
  "printWidth": 100,
  "arrowParens": "always",
  "endOfLine": "lf"
}
```

```
// .prettierignore
dist
node_modules
coverage
*.min.js
pnpm-lock.yaml
```

### ESLint + Prettier

```javascript
// eslint.config.js
import prettier from "eslint-config-prettier";

export default [
  // ...other configs
  prettier,  // Must be last to override conflicting rules
];
```

### Run

```bash
npx prettier --write .
npx prettier --check .
npx prettier --write "src/**/*.{ts,tsx,css,json}"
```

## Ruff (Python - Linter + Formatter)

### Setup

```bash
pip install ruff
```

```toml
# pyproject.toml
[tool.ruff]
target-version = "py312"
line-length = 100

[tool.ruff.lint]
select = [
    "E",    # pycodestyle errors
    "W",    # pycodestyle warnings
    "F",    # pyflakes
    "I",    # isort
    "N",    # pep8-naming
    "UP",   # pyupgrade
    "B",    # flake8-bugbear
    "SIM",  # flake8-simplify
    "TCH",  # flake8-type-checking
]
ignore = [
    "E501",  # line too long (handled by formatter)
]

[tool.ruff.lint.isort]
known-first-party = ["myproject"]

[tool.ruff.format]
quote-style = "double"
indent-style = "space"
```

### Run

```bash
# Lint
ruff check .
ruff check --fix .

# Format
ruff format .
ruff format --check .
```

## Black (Python Formatter)

```bash
pip install black

# Format
black .
black --check .
black --diff .
```

```toml
# pyproject.toml
[tool.black]
line-length = 100
target-version = ["py312"]
```

## mypy (Python Type Checker)

```bash
pip install mypy

mypy src/
mypy --strict src/
```

```toml
# pyproject.toml
[tool.mypy]
python_version = "3.12"
strict = true
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
```

## EditorConfig

```ini
# .editorconfig
root = true

[*]
end_of_line = lf
insert_final_newline = true
trim_trailing_whitespace = true
charset = utf-8

[*.{js,ts,tsx,json,css,yml,yaml}]
indent_style = space
indent_size = 2

[*.py]
indent_style = space
indent_size = 4

[*.md]
trim_trailing_whitespace = false

[Makefile]
indent_style = tab
```

## Pre-commit Integration

```bash
# Install
npm install -D husky lint-staged

# Setup husky
npx husky init

# .husky/pre-commit
npx lint-staged
```

```json
// package.json
{
  "lint-staged": {
    "*.{ts,tsx}": ["eslint --fix", "prettier --write"],
    "*.{json,md,yml}": ["prettier --write"],
    "*.py": ["ruff check --fix", "ruff format"]
  }
}
```

### Python pre-commit

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.3.0
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.8.0
    hooks:
      - id: mypy
```

```bash
pip install pre-commit
pre-commit install
pre-commit run --all-files
```

## package.json Scripts

```json
{
  "scripts": {
    "lint": "eslint .",
    "lint:fix": "eslint --fix .",
    "format": "prettier --write .",
    "format:check": "prettier --check .",
    "typecheck": "tsc --noEmit",
    "check": "npm run lint && npm run format:check && npm run typecheck"
  }
}
```

## Reference

For CI integration and configuration recipes: `references/configs.md`
