---
name: eslint
description: Professional-grade ESLint development for JavaScript and TypeScript projects. Use when working with ESLint for (1) configuring ESLint in projects, (2) understanding or fixing ESLint errors and warnings, (3) creating or modifying ESLint rules, (4) integrating ESLint into build systems or editors, (5) migrating ESLint configurations, (6) setting up custom parsers or plugins, (7) troubleshooting ESLint issues, (8) implementing code quality standards, or (9) any task involving ESLint setup, configuration, or usage. Covers all ESLint versions with focus on v9+ flat config format.
---

# ESLint Development

Professional ESLint integration for JavaScript and TypeScript codebases. This skill provides comprehensive guidance for configuring, using, and extending ESLint to enforce code quality standards.

**Latest ESLint version:** 9.32.2 (December 2025)

## Quick Start

### Install ESLint

```bash
npm install --save-dev eslint
npx eslint --init
```

### Basic Configuration (Flat Config - ESLint 9+)

```javascript
// eslint.config.js
export default [
  {
    files: ["**/*.js"],
    rules: {
      "no-unused-vars": "error",
      "no-console": "warn"
    }
  }
];
```

### Run ESLint

```bash
npx eslint .                 # Lint all files
npx eslint --fix .           # Auto-fix issues
npx eslint src/**/*.js       # Lint specific files
```

## Core Workflows

### 1. Project Setup

**New projects:**
1. Install ESLint: `npm install --save-dev eslint`
2. Initialize config: `npx eslint --init` (interactive)
3. Review generated `eslint.config.js`
4. Run first lint: `npx eslint .`

**Existing projects:**
1. Review current configuration in `eslint.config.js` or `.eslintrc.*`
2. Understand applied rules and plugins
3. Migrate to flat config if using legacy format (see references/use/configure/migration-guide.md)

### 2. Configuration

ESLint uses **flat config** format (eslint.config.js) in v9+. Legacy formats (.eslintrc.*) are deprecated.

**Key configuration areas:**
- **Files**: Specify which files to lint
- **Rules**: Enable/disable specific rules and set severity
- **Language options**: Parser, source type, ECMAScript version
- **Plugins**: Extend with custom rules
- **Ignore patterns**: Exclude files from linting

See references/use/configure/configuration-files.md for complete guide.

### 3. Rule Management

**Rule severity levels:**
- `"off"` or `0` - Disable rule
- `"warn"` or `1` - Warning (doesn't affect exit code)
- `"error"` or `2` - Error (exit code 1)

**Configure rules:**

```javascript
export default [
  {
    rules: {
      "no-unused-vars": "error",
      "quotes": ["error", "double"],
      "semi": ["error", "always"],
      "no-console": "off"
    }
  }
];
```

**Find specific rule documentation:**
- All 300+ core rules documented in references/rules/
- Rule names are kebab-case (e.g., `no-unused-vars.md`, `prefer-const.md`)

### 4. Fixing Issues

**Auto-fix:**

```bash
npx eslint --fix .           # Fix all auto-fixable issues
npx eslint --fix src/        # Fix specific directory
npx eslint --fix-dry-run .   # Preview fixes without applying
```

**Manual fixes:**
1. Read error message and rule name
2. Look up rule in references/rules/[rule-name].md
3. Understand the issue and correct code examples
4. Apply fix or disable rule if not applicable

**Disable rules:**

```javascript
// Disable for one line
// eslint-disable-next-line no-console
console.log("debug");

// Disable for entire file
/* eslint-disable no-console */

// Disable specific rule in block
/* eslint-disable no-unused-vars */
const temp = getData();
/* eslint-enable no-unused-vars */
```

### 5. Integration

**Editor integration:**
- Install ESLint extension for your editor (VS Code, Sublime, etc.)
- Enables real-time linting and auto-fix on save

**Build system integration:**
- Add to npm scripts: `"lint": "eslint ."`
- CI/CD: Run `npm run lint` in build pipeline
- Pre-commit hooks: Use with husky or lint-staged

See references/use/integrations.md for editor and tool integrations.

## Advanced Usage

### Custom Rules

Create project-specific rules to enforce custom patterns:

```javascript
// eslint.config.js
import myCustomRule from './rules/my-custom-rule.js';

export default [
  {
    plugins: {
      local: { rules: { 'my-custom-rule': myCustomRule } }
    },
    rules: {
      'local/my-custom-rule': 'error'
    }
  }
];
```

See references/extend/custom-rules.md for complete guide.

### Plugins

Extend ESLint with community plugins for frameworks and libraries:

```javascript
import react from 'eslint-plugin-react';
import typescript from '@typescript-eslint/eslint-plugin';

export default [
  {
    plugins: { react, typescript },
    rules: {
      'react/jsx-uses-react': 'error',
      '@typescript-eslint/no-unused-vars': 'error'
    }
  }
];
```

See references/extend/plugins.md for plugin development and usage.

### TypeScript

For TypeScript projects, use @typescript-eslint:

```bash
npm install --save-dev @typescript-eslint/parser @typescript-eslint/eslint-plugin
```

```javascript
import tseslint from '@typescript-eslint/eslint-plugin';
import parser from '@typescript-eslint/parser';

export default [
  {
    files: ['**/*.ts', '**/*.tsx'],
    languageOptions: {
      parser: parser,
      parserOptions: {
        project: './tsconfig.json'
      }
    },
    plugins: { '@typescript-eslint': tseslint },
    rules: {
      '@typescript-eslint/no-explicit-any': 'warn',
      '@typescript-eslint/explicit-function-return-type': 'error'
    }
  }
];
```

See references/extend/custom-parsers.md for parser configuration.

## Documentation Organization

Complete ESLint documentation is organized in `references/`:

### Core Usage

- **references/use/getting-started.md** - Initial setup and installation
- **references/use/command-line-interface.md** - CLI options and flags
- **references/use/core-concepts/** - Core ESLint concepts and terminology

### Configuration

- **references/use/configure/configuration-files.md** - Flat config format (v9+)
- **references/use/configure/rules.md** - Rule configuration patterns
- **references/use/configure/language-options.md** - Parser and language settings
- **references/use/configure/plugins.md** - Plugin configuration
- **references/use/configure/ignore.md** - Ignoring files and directories
- **references/use/configure/migration-guide.md** - Migrating from legacy config

### Rules Reference

- **references/rules/** - All 300+ core ESLint rules
  - Each rule has its own file (e.g., `no-console.md`, `prefer-const.md`)
  - Includes description, examples, options, and use cases
  - Organized alphabetically by rule name

### Extension & Customization

- **references/extend/custom-rules.md** - Creating custom ESLint rules
- **references/extend/custom-parsers.md** - Building custom parsers
- **references/extend/plugins.md** - Plugin development and publishing
- **references/extend/shareable-configs.md** - Creating shareable configurations
- **references/extend/selectors.md** - AST selectors for advanced rules

### Integration

- **references/integrate/nodejs-api.md** - Programmatic ESLint API usage
- **references/use/integrations.md** - Editor and tool integrations

### Troubleshooting

- **references/use/troubleshooting/** - Common error messages and solutions
  - Covers plugin loading errors, config resolution issues, and more

### Migration Guides

- **references/use/migrate-to-9.0.0.md** - Migrating to ESLint 9.x
- **references/use/migrate-to-8.0.0.md** - Migrating to ESLint 8.x
- Additional migration guides for older versions

## Common Patterns

### Monorepo Configuration

```javascript
export default [
  {
    files: ["packages/*/src/**/*.js"],
    rules: { "no-console": "error" }
  },
  {
    files: ["packages/cli/src/**/*.js"],
    rules: { "no-console": "off" }  // Allow console in CLI package
  }
];
```

### Environment-Specific Rules

```javascript
export default [
  {
    files: ["src/**/*.js"],
    rules: { "no-console": "error" }
  },
  {
    files: ["**/*.test.js", "**/*.spec.js"],
    rules: { "no-console": "off" }  // Allow console in tests
  }
];
```

### Shared Configuration

```javascript
// config/base.js
export default {
  rules: {
    "no-unused-vars": "error",
    "semi": ["error", "always"]
  }
};

// eslint.config.js
import baseConfig from './config/base.js';

export default [
  baseConfig,
  {
    files: ["src/**/*.js"],
    rules: {
      "no-console": "warn"
    }
  }
];
```

## Best Practices

1. **Start with recommended config** - Use `eslint:recommended` as baseline
2. **Enable auto-fix** - Configure editor to fix on save for productivity
3. **Use strict mode gradually** - Start with warnings, upgrade to errors iteratively
4. **Document exceptions** - Add comments when disabling rules
5. **Keep config organized** - Split large configs into multiple files
6. **Test rule changes** - Run linter on entire codebase before committing config changes
7. **Update regularly** - Keep ESLint and plugins up to date for latest rules and fixes
8. **Use flat config** - Migrate to eslint.config.js format (v9+ standard)

## Workflow for Fixing Errors

When ESLint reports errors:

1. **Identify the rule** - Look for rule name in error message (e.g., `no-unused-vars`)
2. **Read rule docs** - Check references/rules/[rule-name].md
3. **Review examples** - Examine correct/incorrect examples in the docs
4. **Apply fix** - Either fix code or configure rule if not applicable
5. **Verify** - Re-run ESLint to confirm error is resolved

## Updating Documentation

To update this skill's documentation when new ESLint versions are released:

See scripts/docs-updater/USAGE.md for complete instructions on extracting updated documentation from the ESLint repository.

## Key Differences Between Versions

### ESLint 9.x (Flat Config)

- New flat config format (eslint.config.js)
- Simplified configuration structure
- Better TypeScript support
- Improved performance

### ESLint 8.x (Legacy)

- Uses .eslintrc.* files (deprecated in v9+)
- Different plugin loading mechanism
- Legacy config format

**Migration:** See references/use/configure/migration-guide.md for migrating from v8 to v9.

## Working with This Skill

This skill provides:

1. **Comprehensive rule reference** - All 300+ ESLint rules with examples
2. **Configuration patterns** - Flat config examples and best practices
3. **Integration guides** - Editor, build system, and CI/CD integration
4. **Troubleshooting** - Common errors and solutions
5. **Migration guides** - Version upgrade assistance
6. **Extension patterns** - Custom rules, plugins, and parsers

For specific rule details, configuration options, or integration patterns, consult the organized reference documentation in `references/`.
