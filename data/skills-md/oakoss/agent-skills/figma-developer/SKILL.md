---
name: figma-developer
description: 'Extracts design data from Figma via the REST API and converts designs to React code. Use when syncing Figma tokens to CSS variables, exporting icons as SVG components, generating code from Figma designs, or automating design-to-code workflows. Use for design token extraction, icon export, component generation, and CI-based Figma sync.'
license: MIT
metadata:
  author: oakoss
  version: '1.1'
---

# Figma Developer

## Overview

Automates the Figma-to-code bridge using the Figma REST API. Extracts design tokens (colors, typography, spacing) as CSS variables and JSON, exports icons as SVG React components, generates React components from Figma node structures, and sets up CI pipelines for continuous design sync.

**When to use:** Syncing design tokens from Figma to code, exporting icon sets as React components, generating component scaffolding from Figma variants, setting up automated design sync in CI.

**When NOT to use:** Manual one-off design tweaks (just copy values), Figma plugin development (use the Plugin API instead), real-time collaborative editing (use Figma webhooks directly), or projects without a Figma design system.

## Quick Reference

| Pattern            | API / Approach                                          | Key Points                                           |
| ------------------ | ------------------------------------------------------- | ---------------------------------------------------- |
| Get file data      | `GET /v1/files/:key`                                    | Returns full document tree with styles and fills     |
| Get specific nodes | `GET /v1/files/:key/nodes?ids=...`                      | Fetch only the nodes you need to reduce payload      |
| Export images      | `GET /v1/images/:key?ids=...&format=svg`                | Renders nodes as SVG/PNG/PDF; URLs expire in 14 days |
| Get styles         | `GET /v1/files/:key/styles`                             | Lists all published color, text, and effect styles   |
| Get components     | `GET /v1/files/:key/components`                         | Lists all published components with metadata         |
| Get component sets | `GET /v1/files/:key/component_sets`                     | Returns variant groupings for components             |
| Get variables      | `GET /v1/files/:key/variables/local`                    | Extracts Figma Variables (colors, spacing, etc.)     |
| Publish variables  | `POST /v1/variables`                                    | Publishes local variables organization-wide          |
| Token extraction   | Parse styles from file response, transform to CSS/JSON  | No built-in "extract tokens" endpoint exists         |
| CI sync            | GitHub Actions cron + `peter-evans/create-pull-request` | Auto-sync PRs on Figma file changes                  |

## Figma File Organization

| Section    | Contents                                            |
| ---------- | --------------------------------------------------- |
| Colors     | All color styles with `/` hierarchy (`Primary/500`) |
| Typography | Text styles (`Heading/Large`, `Body/Regular`)       |
| Spacing    | Spacing guide values                                |
| Components | Variant groups (`Button/Primary`, `Card/Default`)   |
| Icons      | All icons in one exportable frame                   |

## Common Mistakes

| Mistake                                                   | Fix                                                              |
| --------------------------------------------------------- | ---------------------------------------------------------------- |
| Using fabricated API methods like `extractDesignTokens()` | Parse styles from `GET /v1/files/:key` response manually         |
| Hardcoding Figma values instead of using tokens           | Extract tokens to CSS variables, reference with `var()`          |
| Not normalizing Figma style names                         | Lowercase + replace special chars with hyphens                   |
| Forgetting Figma uses 0-1 RGB not 0-255                   | Multiply by 255 and round before hex conversion                  |
| No API response caching                                   | Cache with TTL to avoid rate limits                              |
| Manual icon exports                                       | Automate with `GET /v1/images/:key` + React component generation |
| No CI sync workflow                                       | GitHub Actions cron + `create-pull-request` action               |
| Using expired image URLs                                  | Image export URLs expire in 14 days; re-fetch before use         |

## Libraries

| Package                | Purpose                                  |
| ---------------------- | ---------------------------------------- |
| `figma-api`            | Community Figma REST API client (typed)  |
| `@figma/rest-api-spec` | Official TypeScript types for Figma API  |
| `style-dictionary`     | Transform design tokens across platforms |
| `svgo`                 | Optimize exported SVGs before use        |
| `@svgr/core`           | Convert SVG files to React components    |

## Delegation

- **Design systems**: see `design-system` skill
- **Asset optimization**: see `asset-manager` skill

## References

- [Setup and Authentication](references/setup.md)
- [Design Tokens](references/design-tokens.md)
- [Asset Export](references/asset-export.md)
- [Component Generation](references/component-generation.md)
- [CI Automation](references/ci-automation.md)
- [Troubleshooting](references/troubleshooting.md)
