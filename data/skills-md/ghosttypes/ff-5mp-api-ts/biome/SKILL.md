---
name: biome
description: Comprehensive Biome (biomejs.dev) integration for professional TypeScript/JavaScript development. Use for linting, formatting, code quality, and flawless Biome integration into codebases. Covers installation, configuration, migration from ESLint/Prettier, all linter rules, formatter options, CLI usage, editor integration, monorepo setup, and CI/CD integration. Use when working with Biome tooling, configuring biome.json, setting up linting/formatting, migrating projects, debugging Biome issues, or implementing production-ready Biome workflows.
---

# Biome - Professional TypeScript/JavaScript Tooling

Biome is a fast, modern toolchain for JavaScript, TypeScript, JSX, JSON, CSS, GraphQL, and HTML. It provides formatting, linting, and code analysis with a single tool and zero configuration required.

## When to Use This Skill

Use this skill when:
- Setting up Biome in a new or existing project
- Configuring biome.json for specific requirements
- Migrating from ESLint and/or Prettier to Biome
- Implementing linter rules or formatter options
- Integrating Biome with editors (VS Code, Zed, IntelliJ)
- Setting up CI/CD pipelines with Biome
- Configuring monorepos or large projects
- Debugging Biome configuration or performance issues
- Understanding specific lint rules or code actions
- Upgrading from Biome v1 to v2

## Quick Start

### Installation

```bash
# npm
npm i -D -E @biomejs/biome

# pnpm
pnpm add -D -E @biomejs/biome

# yarn
yarn add -D -E @biomejs/biome
```

### Initialize Configuration

```bash
npx @biomejs/biome init
```

This creates a `biome.json` with recommended defaults.

### Basic Commands

```bash
# Format and lint
npx @biomejs/biome check --write ./src

# Format only
npx @biomejs/biome format --write ./src

# Lint only
npx @biomejs/biome lint ./src

# CI mode (no writes, exit on errors)
npx @biomejs/biome ci ./src
```

## Core Workflows

### 1. Project Setup

For new projects:
1. Install Biome as dev dependency
2. Run `npx @biomejs/biome init`
3. Configure `biome.json` for project needs
4. Add scripts to package.json
5. Set up editor integration
6. Configure CI/CD

See [references/docs/guides/getting-started.md](references/docs/guides/getting-started.md) for details.

### 2. Configuration

Biome configuration lives in `biome.json` or `biome.jsonc`. Key sections:
- `$schema` - JSON schema for IDE autocomplete
- `files` - File inclusion/exclusion patterns
- `formatter` - Formatting options (indentation, line width, etc.)
- `linter` - Linting rules and their configuration
- `javascript`, `json`, `css` - Language-specific options
- `overrides` - Per-file or per-directory overrides

For complete configuration reference, see [references/docs/reference/configuration.md](references/docs/reference/configuration.md).

### 3. Migration from ESLint/Prettier

Biome can replace both ESLint and Prettier in most projects:

1. Audit existing ESLint/Prettier config
2. Map rules to Biome equivalents
3. Configure Biome to match existing style
4. Run side-by-side comparison
5. Remove ESLint/Prettier dependencies
6. Update scripts and CI/CD

See [references/docs/guides/migrate-eslint-prettier.md](references/docs/guides/migrate-eslint-prettier.md) for detailed migration guide.

### 4. Monorepo/Large Projects

For monorepos or projects with multiple packages:

1. Create root `biome.json` with shared config
2. Use `extends` in package-specific configs
3. Configure file patterns for each package
4. Set up workspace-aware linting
5. Optimize for performance

See [references/docs/guides/big-projects.md](references/docs/guides/big-projects.md) for monorepo patterns.

### 5. Editor Integration

Biome has official extensions for:
- **VS Code** - Full LSP support, format on save, quick fixes
- **Zed** - Native integration, inline diagnostics
- **IntelliJ** - Plugin available

Install the extension for your editor and configure workspace settings. See [references/docs/guides/editors_first-party-extensions.md](references/docs/guides/editors_first-party-extensions.md).

## Reference Documentation

This skill includes complete Biome v2.x documentation:

### Essential References
- [INDEX.md](references/INDEX.md) - Complete documentation index
- [CLI Reference](references/docs/reference/cli.md) - All commands and options (70 KB)
- [Configuration Reference](references/docs/reference/configuration.md) - All config options (42 KB)
- [JavaScript Rules](references/docs/linter/javascript_rules.md) - Complete rule list (68 KB)

### Documentation Categories

**Guides** (11 files)
- Getting started, configuration, migration, editor setup, monorepos

**Formatter** (3 files)
- Formatting engine, Prettier differences, design philosophy

**Linter** (13 files)
- Linting rules for JavaScript/TypeScript, CSS, JSON, GraphQL, HTML
- Rule sources and framework-specific domains (React, Next.js, etc.)

**Assist** (9 files)
- Code actions and refactoring capabilities for all languages

**Reference** (8 files)
- CLI, configuration, diagnostics, environment variables, reporters, editor extensions

**Recipes** (4 files)
- CI/CD integration, git hooks, Renovate setup, badges

**Internals** (7 files)
- Architecture, philosophy, language support, versioning, changelogs

Use [references/INDEX.md](references/INDEX.md) for quick navigation to specific topics.

## Common Patterns

### Typical biome.json

```json
{
  "$schema": "https://biomejs.dev/schemas/2.0.5/schema.json",
  "vcs": {
    "enabled": true,
    "clientKind": "git",
    "useIgnoreFile": true
  },
  "files": {
    "ignoreUnknown": false,
    "includes": ["src/**/*"]
  },
  "formatter": {
    "enabled": true,
    "indentStyle": "space",
    "indentWidth": 2,
    "lineWidth": 100
  },
  "linter": {
    "enabled": true,
    "rules": {
      "recommended": true
    }
  },
  "javascript": {
    "formatter": {
      "quoteStyle": "single",
      "trailingCommas": "es5",
      "semicolons": "always"
    }
  }
}
```

### Package.json Scripts

```json
{
  "scripts": {
    "format": "biome format --write .",
    "lint": "biome lint .",
    "check": "biome check --write .",
    "ci": "biome ci ."
  }
}
```

### CI/CD Integration

```yaml
# GitHub Actions
- name: Run Biome
  run: npx @biomejs/biome ci .
```

See [references/docs/recipes/continuous-integration.md](references/docs/recipes/continuous-integration.md) for complete CI/CD examples.

## Updating Documentation

To update this skill's documentation with the latest from biomejs.dev:

```bash
python scripts/scrape_biome_docs.py --update-all --output references/docs
```

This scrapes all current documentation and updates the reference files.

## Key Concepts

### Formatting Philosophy
- Opinionated defaults with minimal configuration
- Focuses on consistency over personal preference
- Significantly faster than Prettier (10-20x)
- Format-preserving when possible

### Linting Approach
- Rules organized by category (correctness, performance, style, etc.)
- Framework-aware domains (React, Next.js, etc.)
- Recommended rules enabled by default
- Fast incremental linting

### Tool Integration
- Single tool replaces ESLint + Prettier + more
- Zero-config defaults work for most projects
- Native TypeScript support, no type-checking required
- Incremental adoption possible

## Best Practices

1. **Start with recommended rules** - Enable `"recommended": true` then customize
2. **Use VCS integration** - Let Biome respect .gitignore
3. **Pin Biome version** - Use exact versions in package.json
4. **Configure per-language** - Override general settings for specific languages
5. **Use overrides sparingly** - Prefer consistent configuration across the project
6. **Test before committing** - Run `biome ci` in CI/CD
7. **Enable editor integration** - Format on save for best experience
8. **Read diagnostics carefully** - Biome provides detailed error explanations

## Troubleshooting

Common issues and solutions:

**Biome not finding files**
- Check `files.includes` in biome.json
- Verify VCS integration settings
- Review .gitignore patterns

**Performance issues**
- See [references/docs/guides/investigate-slowness.md](references/docs/guides/investigate-slowness.md)
- Check file inclusion patterns
- Consider using `files.ignoreUnknown`

**Rule conflicts with existing code**
- Use suppressions for one-off cases
- Configure rule severity (error/warn/off)
- See [references/docs/analyzer/suppressions.md](references/docs/analyzer/suppressions.md)

**Migration issues**
- Compare Biome output with ESLint/Prettier
- Use configuration overrides for edge cases
- See migration guide for common patterns

For detailed troubleshooting, consult the relevant reference documentation.

## Resources

### scripts/
Contains the Biome documentation scraper for keeping this skill up to date:
- `scrape_biome_docs.py` - Scrapes and cleans Biome documentation from biomejs.dev

### references/
Complete Biome v2.x documentation (56 files, 896 KB):
- `INDEX.md` - Navigation index for all documentation
- `docs/` - All scraped and cleaned documentation files organized by category

The documentation is comprehensive and production-ready, covering all aspects of Biome from installation to advanced usage patterns.
