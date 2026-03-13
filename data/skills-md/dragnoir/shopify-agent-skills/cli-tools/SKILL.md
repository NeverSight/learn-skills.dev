---
name: cli-tools
description: Master Shopify CLI and developer tools. Use this skill for using Shopify CLI commands, theme development workflow, app development workflow, debugging with Theme Check, using the Liquid language server, and configuring development environments. Covers VS Code extension and development best practices.
license: MIT
compatibility: Requires Node.js 18+ and npm/pnpm
metadata:
  author: shopify-agent-skills
  version: "1.0"
  shopify-api-version: "2025-01"
---

# Shopify CLI & Developer Tools

## When to use this skill

Use this skill when:

- Installing and configuring Shopify CLI
- Running theme development commands
- Running app development commands
- Using Theme Check for linting
- Configuring VS Code for Shopify development
- Debugging Liquid code
- Setting up development workflows

## Installing Shopify CLI

### Prerequisites

- **Node.js 18+** - Required for all Shopify development
- **Git** - For version control
- **Package manager** - npm or pnpm

### Installation

```bash
# Install globally via npm
npm install -g @shopify/cli @shopify/theme

# Or via Homebrew (macOS)
brew tap shopify/shopify
brew install shopify-cli

# Verify installation
shopify version
```

### Authentication

```bash
# Log in to your Partner account
shopify auth login

# Log out
shopify auth logout

# Check current auth status
shopify auth info
```

## Theme CLI Commands

### Initialize Theme

```bash
# Clone Skeleton theme as starting point
shopify theme init my-theme

# Clone from custom repository
shopify theme init my-theme --clone-url git@github.com:org/repo.git
```

### Development Server

```bash
# Start dev server (auto-connects to store)
shopify theme dev

# Connect to specific store
shopify theme dev --store my-store.myshopify.com

# Specify theme to work on
shopify theme dev --theme THEME_ID

# Use specific port
shopify theme dev --port 9292

# Open in default browser
shopify theme dev --open

# Live reload options
shopify theme dev --live-reload hot-reload
shopify theme dev --live-reload full-page
shopify theme dev --live-reload off
```

### Push & Pull

```bash
# Push local changes to Shopify
shopify theme push

# Push as new unpublished theme
shopify theme push --unpublished

# Push to specific theme
shopify theme push --theme THEME_ID

# Push only specific files
shopify theme push --only templates/*.json

# Push ignoring specific files
shopify theme push --ignore config/settings_data.json

# Pull theme from Shopify
shopify theme pull

# Pull specific theme
shopify theme pull --theme THEME_ID

# Pull only specific files
shopify theme pull --only sections/*.liquid
```

### Theme Management

```bash
# List all themes
shopify theme list

# Publish a theme
shopify theme publish --theme THEME_ID

# Rename a theme
shopify theme rename --theme THEME_ID --name "New Name"

# Delete a theme
shopify theme delete --theme THEME_ID

# Package theme for upload
shopify theme package

# Open theme in browser
shopify theme open --theme THEME_ID
```

### Theme Check (Linting)

```bash
# Run Theme Check on current directory
shopify theme check

# Check specific path
shopify theme check --path ./sections

# Auto-fix issues
shopify theme check --auto-correct

# Output as JSON
shopify theme check --output json

# Fail on warnings (useful for CI)
shopify theme check --fail-level warning

# Show offenses inline
shopify theme check --print-offenses
```

### Theme Info & Console

```bash
# Show theme environment info
shopify theme info

# Start Liquid REPL console
shopify theme console

# Pull metafields for local development
shopify theme metafields pull
```

## App CLI Commands

### Create App

```bash
# Initialize new app
shopify app init

# Choose template interactively:
# - Remix (recommended)
# - Node
# - Ruby
# - PHP
```

### Development

```bash
# Start dev server with tunnel
shopify app dev

# Reset app configuration
shopify app dev --reset

# Skip tunnel (use your own)
shopify app dev --no-tunnel

# Specify port
shopify app dev --port 3000
```

### Generate Extensions

```bash
# Generate new extension
shopify app generate extension

# Extension types available:
# - Checkout UI
# - Admin UI
# - Theme App Extension
# - Post-purchase UI
# - Shopify Function
# - Web Pixel
# - Flow Action/Trigger
# - POS UI
```

### Deployment

```bash
# Deploy app and extensions
shopify app deploy

# List app versions
shopify app versions list

# Release specific version
shopify app release --version VERSION_ID
```

### App Info

```bash
# Show app info
shopify app info

# Show environment variables
shopify app env show

# Pull environment variables
shopify app env pull
```

### Functions

```bash
# Run function locally
shopify app function run --path extensions/my-function

# Generate types for function
shopify app function typegen --path extensions/my-function
```

## VS Code Extension

### Installation

1. Open VS Code
2. Go to Extensions (Ctrl+Shift+X)
3. Search "Shopify Liquid"
4. Install the official extension

Or install from CLI:

```bash
code --install-extension Shopify.theme-check-vscode
```

### Features

| Feature                     | Description                        |
| --------------------------- | ---------------------------------- |
| **Syntax Highlighting**     | Liquid, HTML, CSS, JS highlighting |
| **Code Completion**         | Objects, filters, tags, schema     |
| **Documentation on Hover**  | Inline docs for Liquid code        |
| **Theme Check Integration** | Real-time linting                  |
| **Schema Completion**       | JSON schema in sections            |
| **Go to Definition**        | Navigate to snippets/sections      |
| **Auto-closing Pairs**      | Liquid tags and braces             |
| **Code Formatting**         | Format Liquid code                 |

### Configuration

```json
// .vscode/settings.json
{
  "shopifyLiquid.formatterDevPreview": true,
  "shopifyLiquid.themeCheckNextDevPreview": true,
  "editor.formatOnSave": true,
  "[liquid]": {
    "editor.defaultFormatter": "Shopify.theme-check-vscode"
  },
  "files.associations": {
    "*.liquid": "liquid"
  }
}
```

## Theme Check Configuration

### .theme-check.yml

```yaml
# Extends default configuration
extends: :default

# Enable/disable specific checks
SyntaxError:
  enabled: true
  severity: error

DeprecatedFilter:
  enabled: true
  severity: warning

MissingTemplate:
  enabled: true

UnusedAssign:
  enabled: true

UnusedSnippet:
  enabled: false

ImgWidthAndHeight:
  enabled: true

AssetSizeCSS:
  enabled: true
  threshold_in_bytes: 100000

AssetSizeJavaScript:
  enabled: true
  threshold_in_bytes: 50000

# Ignore specific files
ignore:
  - vendor/**/*
  - assets/vendor.js
```

### Common Theme Check Errors

| Error               | Solution                     |
| ------------------- | ---------------------------- |
| `MissingTemplate`   | Create missing template file |
| `DeprecatedFilter`  | Update to new filter syntax  |
| `UnusedAssign`      | Remove or use the variable   |
| `SyntaxError`       | Fix Liquid syntax            |
| `AssetSizeCSS`      | Reduce CSS file size         |
| `ImgWidthAndHeight` | Add width/height to images   |

## Development Workflow

### Theme Development

```bash
# 1. Clone starter theme
shopify theme init my-theme
cd my-theme

# 2. Start development
shopify theme dev --store my-store.myshopify.com

# 3. Make changes (auto-synced)
# Edit files in your editor

# 4. Run linter
shopify theme check

# 5. Push when ready
shopify theme push --theme THEME_ID

# 6. Publish live
shopify theme publish --theme THEME_ID
```

### App Development

```bash
# 1. Create app
shopify app init

# 2. Add extensions
shopify app generate extension

# 3. Start development
shopify app dev

# 4. Test locally
# App runs at http://localhost:3000

# 5. Deploy
shopify app deploy
```

## Environment Configuration

### .shopify-cli.yml (Theme)

```yaml
shop: my-store.myshopify.com
theme: THEME_ID
path: .
ignore:
  - config/settings_data.json
  - .git/*
```

### .env (App)

```env
SHOPIFY_API_KEY=your-api-key
SHOPIFY_API_SECRET=your-api-secret
SHOPIFY_APP_URL=https://your-app.com
SCOPES=read_products,write_products
HOST=https://tunnel.ngrok.io
```

## CI/CD Integration

### GitHub Actions (Theme Check)

```yaml
# .github/workflows/theme-check.yml
name: Theme Check

on: [push, pull_request]

jobs:
  theme-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Setup Node
        uses: actions/setup-node@v3
        with:
          node-version: "18"

      - name: Install Shopify CLI
        run: npm install -g @shopify/cli @shopify/theme

      - name: Run Theme Check
        run: shopify theme check --fail-level error
```

### GitHub Actions (App Deploy)

```yaml
# .github/workflows/deploy.yml
name: Deploy App

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Setup Node
        uses: actions/setup-node@v3
        with:
          node-version: "18"

      - name: Install dependencies
        run: npm ci

      - name: Deploy
        env:
          SHOPIFY_CLI_PARTNERS_TOKEN: ${{ secrets.SHOPIFY_CLI_PARTNERS_TOKEN }}
        run: npm run deploy
```

## Troubleshooting

### Common Issues

**CLI not found after install:**

```bash
# Check Node.js path
which node

# Reinstall globally
npm install -g @shopify/cli
```

**Authentication issues:**

```bash
# Clear auth and re-login
shopify auth logout
shopify auth login --reset
```

**Theme dev not syncing:**

```bash
# Check .shopify-cli.yml configuration
# Ensure correct store URL
# Check file permissions
```

**Port already in use:**

```bash
# Use different port
shopify theme dev --port 9293
shopify app dev --port 3001
```

## Quick Reference

### Theme Commands

| Command         | Description         |
| --------------- | ------------------- |
| `theme init`    | Initialize theme    |
| `theme dev`     | Start dev server    |
| `theme push`    | Upload to store     |
| `theme pull`    | Download from store |
| `theme check`   | Run linter          |
| `theme list`    | List themes         |
| `theme publish` | Publish theme       |

### App Commands

| Command                  | Description      |
| ------------------------ | ---------------- |
| `app init`               | Create app       |
| `app dev`                | Start dev server |
| `app deploy`             | Deploy app       |
| `app generate extension` | Add extension    |
| `app info`               | Show app info    |
| `app function run`       | Test function    |

## Resources

- [Shopify CLI Reference](https://shopify.dev/docs/api/shopify-cli)
- [Theme Check Docs](https://shopify.dev/docs/storefronts/themes/tools/theme-check)
- [VS Code Extension](https://shopify.dev/docs/storefronts/themes/tools/shopify-liquid-vscode)
- [Language Server](https://shopify.dev/docs/storefronts/themes/tools/cli/language-server)
- [Dawn Theme Reference](https://github.com/Shopify/dawn)
- [GitHub Actions Integration](https://shopify.dev/docs/storefronts/themes/tools/github)

For theme development, see the [theme-development](../theme-development/SKILL.md) skill.
For app development, see the [app-development](../app-development/SKILL.md) skill.
