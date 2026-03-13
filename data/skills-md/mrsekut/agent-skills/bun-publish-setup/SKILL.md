---
name: bun-publish-setup
description: First-time npm publish for bun libraries and GitHub Actions setup for automated publishing. Validates/fixes package.json, performs initial publish, and configures CI/CD workflow.
---

# bun-publish-setup

First-time npm publish for bun libraries and GitHub Actions setup for automated publishing.

## Prerequisites

- bun is installed
- Logged in to npm (`npm whoami` to verify)
- GitHub repository exists

## Workflow

1. **Pre-publish checks & fixes** — Validate and fix package.json, tsconfig, build, README, etc.
2. **First publish** — Confirm with dry-run, then run bun publish
3. **GitHub Actions setup** — Create workflow for auto-publish on version tag push

## Phase 1: Pre-publish Checks & Fixes

### 1-1: Validate & Fix package.json

Read package.json and validate the following fields. Suggest fixes for any missing or incorrect fields.

**Required fields:**

- `name` — Package name. Check if scoped (`@scope/name`)
- `version` — `0.1.0` or `1.0.0` is appropriate for first publish
- `description` — Brief description of the package
- `license` — e.g. MIT. Verify consistency with LICENSE file

**Recommended fields:**

- `repository` — GitHub repository URL. Can be inferred from `git remote get-url origin`
- `keywords` — Keywords for npm search
- `author` — Author info

**Entry points (for TypeScript libraries):**

- `main` — CJS entry point (e.g. `./dist/index.js`)
- `module` — ESM entry point (e.g. `./dist/index.mjs`)
- `types` — Type definitions (e.g. `./dist/index.d.ts`)
- `exports` — Conditional exports. Recommended format:

```json
{
	"exports": {
		".": {
			"types": "./dist/index.d.ts",
			"import": "./dist/index.mjs",
			"require": "./dist/index.js"
		}
	}
}
```

**Published files:**

- `files` — Files/directories to include in the npm package (e.g. `["dist", "README.md", "LICENSE"]`). Ensure unnecessary files are excluded.

### 1-2: Check Package Name Availability

```bash
npm view <package-name>
```

- 404 means the name is available
- If already taken, suggest alternative names to the user

### 1-3: Validate tsconfig.json

For TypeScript projects, verify:

- `declaration: true` — Type definition generation is enabled
- `outDir` — Build output directory matches package.json entry points
- `declarationDir` — Type definition output directory (if configured)

### 1-4: Run Build (only if build script exists)

Only run if a `build` script is defined in package.json. Not needed for projects that publish TS source directly.

```bash
bun run build
```

- Verify build succeeds
- Verify expected files are generated in the output directory

### 1-5: Check README.md

- Verify README.md exists
- If missing, suggest creating one

### 1-6: Check LICENSE File

- Verify LICENSE file exists
- Verify consistency with `license` field in package.json
- If missing, suggest creating one based on the `license` field

## Phase 2: First Publish

### 2-1: Dry-run Preview

```bash
bun publish --dry-run
```

Check the output for:

- Unnecessary files (source code, tests, config files, etc.) in the publish list
- Reasonable package size

If issues found, go back to Phase 1 to fix.

### 2-2: Publish

Present dry-run results to the user and get confirmation before publishing.

```bash
bun publish
```

For scoped packages on first publish, `--access public` is required:

```bash
bun publish --access public
```

**Note:** On first publish, bun will prompt for browser-based npm authentication. Tell the user to press ENTER to open the authentication URL in their browser and complete the login. Wait for the user to confirm authentication is done before proceeding.

### 2-3: Verify Publication

```bash
npm view <package-name>
```

Verify the package was published successfully.

## Phase 3: GitHub Actions Setup

### 3-1: Create Workflow File

Create `.github/workflows/publish.yml`:

```yaml
# yaml-language-server:$schema=https://raw.githubusercontent.com/SchemaStore/schemastore/master/src/schemas/json/github-workflow.json
name: npm publish

on:
  push:
    tags:
      - "*"

jobs:
  publish:
    runs-on: ubuntu-latest
    timeout-minutes: 10
    permissions:
      contents: read
      id-token: write
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - uses: actions/setup-node@v4
        with:
          registry-url: "https://registry.npmjs.org"
          node-version: 24

      - uses: oven-sh/setup-bun@v2
      - run: bun install --frozen-lockfile
      - run: bun run build

      - name: Update npm
        run: npm install -g npm@latest

      # Include this step only if a build script exists
      - run: bun run build

      - run: npm publish --provenance --access public
```

For scoped packages, change to `npm publish --access public`. Remove the build step if no build script exists.

### 3-2: Configure npm Publishing Access

Guide the user through setting up GitHub Actions publishing from the npm package settings:

1. Go to the package's access page: `https://www.npmjs.com/package/<package-name>/access`
2. Under publishing access, select **GitHub Actions**
3. Fill in the form:
   - **Organization or user**: GitHub username or org (e.g. `mrsekut`)
   - **Repository**: Repository name (e.g. `bun-publish-setup`)
   - **Workflow filename**: `publish.yml`
   - **Environment name**: leave blank

### 3-3: Release Flow

Explain the release process to the user:

```bash
# 1. Bump version (automatically creates commit & tag)
npm version patch  # or minor, major

# 2. Push with tags → GitHub Actions auto-publishes to npm
git push --follow-tags
```
