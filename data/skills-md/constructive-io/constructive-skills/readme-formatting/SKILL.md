---
name: readme-formatting
description: Format README files with Constructive branding including header logos and badges. Use when creating new packages, publishing modules, or when asked to "add header image", "add badges", "format README", or "standardize README".
compatibility: npm, pnpm, pgpm, any package type
metadata:
  author: constructive-io
  version: "1.0.0"
---

# README Formatting (Constructive Standard)

Format README files with consistent Constructive branding including centered header logos and appropriate badges for different package types.

## When to Apply

Use this skill when:
- Creating a new npm, pnpm, or pgpm package
- Publishing a module to npm or pgpm registry
- Asked to add header images or badges to a README
- Standardizing README formatting across packages
- A README is missing the Constructive logo header

## Header Logo

All Constructive packages should include a centered logo at the top of the README, immediately after the package title.

### Standard Header (Most Packages)

```markdown
# package-name

<p align="center" width="100%">
  <img height="250" src="https://raw.githubusercontent.com/constructive-io/constructive/refs/heads/main/assets/outline-logo.svg" />
</p>
```

### Root Repository Header

For root-level README files (monorepo roots), use the filled logo with smaller height:

```markdown
# Repository Name

<p align="center" width="100%">
  <img height="150" src="https://raw.githubusercontent.com/constructive-io/constructive/refs/heads/main/assets/logo.svg" />
</p>
```

## Badges

Badges appear in a centered paragraph below the logo. Include badges based on package type and visibility.

### Badge Types

| Badge | When to Use | Example |
|-------|-------------|---------|
| CI Status | Public repos with GitHub Actions | Shows build status |
| License | All public packages | MIT, Apache-2.0, etc. |
| npm Version | npm/pnpm packages published to registry | Shows current version |
| Downloads | Optional, for popular packages | Shows download count |

### Badge Templates

**CI Status Badge:**
```html
<a href="https://github.com/{org}/{repo}/actions/workflows/ci.yml">
  <img height="20" src="https://github.com/{org}/{repo}/actions/workflows/ci.yml/badge.svg" />
</a>
```

**MIT License Badge:**
```html
<a href="https://github.com/{org}/{repo}/blob/main/LICENSE">
  <img height="20" src="https://img.shields.io/badge/license-MIT-blue.svg"/>
</a>
```

**npm Version Badge (from package.json in repo):**
```html
<a href="https://www.npmjs.com/package/{package-name}">
  <img height="20" src="https://img.shields.io/github/package-json/v/{org}/{repo}?filename=packages%2F{package-folder}%2Fpackage.json"/>
</a>
```

**npm Version Badge (from npm registry):**
```html
<a href="https://www.npmjs.com/package/{package-name}">
  <img height="20" src="https://img.shields.io/npm/v/{package-name}.svg"/>
</a>
```

**Downloads Badge (optional):**
```html
<a href="https://www.npmjs.com/package/{package-name}">
  <img height="20" src="https://img.shields.io/npm/dm/{package-name}.svg"/>
</a>
```

### Complete Badge Section

```markdown
<p align="center" width="100%">
  <a href="https://github.com/{org}/{repo}/actions/workflows/ci.yml">
    <img height="20" src="https://github.com/{org}/{repo}/actions/workflows/ci.yml/badge.svg" />
  </a>
  <a href="https://github.com/{org}/{repo}/blob/main/LICENSE">
    <img height="20" src="https://img.shields.io/badge/license-MIT-blue.svg"/>
  </a>
  <a href="https://www.npmjs.com/package/{package-name}">
    <img height="20" src="https://img.shields.io/npm/v/{package-name}.svg"/>
  </a>
</p>
```

## Package Type Guidelines

### npm/pnpm Packages (Published to npm)

Include: Logo + CI badge + License badge + Version badge

```markdown
# @scope/package-name

<p align="center" width="100%">
  <img height="250" src="https://raw.githubusercontent.com/constructive-io/constructive/refs/heads/main/assets/outline-logo.svg" />
</p>

<p align="center" width="100%">
  <a href="https://github.com/constructive-io/repo/actions/workflows/ci.yml">
    <img height="20" src="https://github.com/constructive-io/repo/actions/workflows/ci.yml/badge.svg" />
  </a>
  <a href="https://github.com/constructive-io/repo/blob/main/LICENSE">
    <img height="20" src="https://img.shields.io/badge/license-MIT-blue.svg"/>
  </a>
  <a href="https://www.npmjs.com/package/@scope/package-name">
    <img height="20" src="https://img.shields.io/npm/v/@scope/package-name.svg"/>
  </a>
</p>

Package description here.
```

### pgpm Packages (PostgreSQL Modules)

Include: Logo + CI badge + License badge (no npm version badge)

```markdown
# @pgpm/module-name

<p align="center" width="100%">
  <img height="250" src="https://raw.githubusercontent.com/constructive-io/constructive/refs/heads/main/assets/outline-logo.svg" />
</p>

<p align="center" width="100%">
  <a href="https://github.com/constructive-io/repo/actions/workflows/ci.yml">
    <img height="20" src="https://github.com/constructive-io/repo/actions/workflows/ci.yml/badge.svg" />
  </a>
  <a href="https://github.com/constructive-io/repo/blob/main/LICENSE">
    <img height="20" src="https://img.shields.io/badge/license-MIT-blue.svg"/>
  </a>
</p>

Module description here.
```

### Internal/Private Packages

Include: Logo only (no badges needed)

```markdown
# package-name

<p align="center" width="100%">
  <img height="250" src="https://raw.githubusercontent.com/constructive-io/constructive/refs/heads/main/assets/outline-logo.svg" />
</p>

Package description here.
```

### Packages with Custom License

For packages with "All Rights Reserved" or custom licenses, omit the license badge:

```markdown
<p align="center" width="100%">
  <a href="https://github.com/constructive-io/repo/actions/workflows/ci.yml">
    <img height="20" src="https://github.com/constructive-io/repo/actions/workflows/ci.yml/badge.svg" />
  </a>
</p>
```

## Complete README Template

```markdown
# @scope/package-name

<p align="center" width="100%">
  <img height="250" src="https://raw.githubusercontent.com/constructive-io/constructive/refs/heads/main/assets/outline-logo.svg" />
</p>

<p align="center" width="100%">
  <a href="https://github.com/{org}/{repo}/actions/workflows/ci.yml">
    <img height="20" src="https://github.com/{org}/{repo}/actions/workflows/ci.yml/badge.svg" />
  </a>
  <a href="https://github.com/{org}/{repo}/blob/main/LICENSE">
    <img height="20" src="https://img.shields.io/badge/license-MIT-blue.svg"/>
  </a>
  <a href="https://www.npmjs.com/package/@scope/package-name">
    <img height="20" src="https://img.shields.io/npm/v/@scope/package-name.svg"/>
  </a>
</p>

Brief description of what the package does.

## Installation

\`\`\`bash
pnpm add @scope/package-name
\`\`\`

## Usage

\`\`\`typescript
import { something } from '@scope/package-name';
\`\`\`

## API

Document the main exports and functions.

## License

MIT (or appropriate license)
```

## Checklist

When formatting a README, verify:

- [ ] Package title is at the top (h1)
- [ ] Logo is centered below the title
- [ ] Logo uses correct URL (outline-logo.svg for packages, logo.svg for roots)
- [ ] Logo height is appropriate (250px for packages, 150px for roots)
- [ ] Badges are in a separate centered paragraph below logo
- [ ] Badge links point to correct URLs
- [ ] Version badge uses correct package name (with scope if applicable)
- [ ] License badge matches actual license in package
- [ ] CI badge points to correct workflow file

## Common Mistakes

1. **Missing logo**: Always add the header logo
2. **Wrong logo URL**: Use the raw.githubusercontent.com URL, not a relative path
3. **Badges in wrong order**: CI, then License, then Version
4. **Missing badge links**: Each badge image should be wrapped in an anchor tag
5. **Incorrect package name in version badge**: Must match exactly what's published to npm
6. **Using license badge for "All Rights Reserved"**: Only use for open source licenses

## References

- Logo assets: https://github.com/constructive-io/constructive/tree/main/assets
- Shields.io badges: https://shields.io/
- Related skill: `pnpm-publishing` for publishing workflow
- Related skill: `pgpm-publishing` for pgpm module publishing
