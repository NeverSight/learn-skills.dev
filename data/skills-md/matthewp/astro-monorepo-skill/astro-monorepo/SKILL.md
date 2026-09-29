---
name: astro-monorepo
description: Guidelines for working on the Astro framework monorepo - covers build system, testing, coding conventions, and contribution workflow. Use when contributing to withastro/astro.
license: BSD-3-Clause
metadata:
  author: matthewp
  version: "1.0"
---

# Astro Monorepo Development Guide

Use this skill when working on the Astro framework monorepo.

## Project Structure

```
astro/
├── packages/           # Core packages and integrations
│   ├── astro/          # Core Astro framework
│   ├── create-astro/   # CLI scaffolding tool
│   ├── integrations/   # Framework integrations (react, vue, svelte, etc.)
│   ├── language-tools/ # VS Code extension, language server
│   ├── markdown/       # Markdown processing
│   ├── db/             # Astro DB
│   └── ...
├── examples/           # Example Astro projects
├── benchmark/          # Performance benchmarks
├── scripts/            # Build and utility scripts (astro-scripts)
└── .changeset/         # Changeset configuration
```

## Testing

### Test Framework

- **Primary:** `node:test` (native Node.js test runner)
- **E2E:** Playwright (Chromium + Firefox)
- **Assertions:** `node:assert/strict`

### Running Individual Tests

For most tests, run them directly with Node:

```shell
node packages/astro/test/astro-component.test.js
```

This is the fastest way to run a single test file during development.

### Running E2E Tests

E2E tests use Playwright. To run a specific E2E test by name:

```shell
# From root - runs test matching the pattern
pnpm run test:e2e:match "test name pattern"

# Or from packages/astro
cd packages/astro
pnpm run test:e2e:match "test name pattern"
```

This runs `playwright test -g "pattern"` which matches against test names.

### Test Patterns

```typescript
import assert from "node:assert/strict";
import { describe, it, before, after } from "node:test";
import { loadFixture } from "./test-utils.js";

describe("Feature", () => {
  let fixture;

  before(async () => {
    fixture = await loadFixture({ root: "./fixtures/my-test/" });
    await fixture.build();
  });

  it("should work", async () => {
    const html = await fixture.readFile("/index.html");
    assert.ok(html.includes("expected content"));
  });
});
```

**Important:** Use a custom `outDir` per test to avoid cache conflicts between tests.

## Runtime Code Restrictions

The codebase has three distinct runtime contexts:

1. **Node.js** (`src/core/`) - Build/dev commands, can use any Node.js APIs
2. **Inside Vite** (`src/runtime/server/`) - SSR execution, some Node.js restrictions
3. **Browser** (`src/runtime/client/`) - Client hydration, no Node.js APIs

**CRITICAL:** Code in `runtime/` folders or `runtime.ts` files must be runtime-agnostic:

- NO direct `node:` imports (breaks Cloudflare, Deno, etc.)
- Node.js APIs allowed in Vite plugins but NOT in virtual modules
- Test runtime code works in non-Node environments

## Contribution Workflow

### Git

Do not stage or commit changes unless explicitly asked to.

### Changesets

Required for any package changes (not needed for `examples/*`):

```shell
pnpm exec changeset
```

Select affected packages, bump type (patch/minor/major), and write a description.

### Pull Requests

When creating a pull request, use the template at `.github/PULL_REQUEST_TEMPLATE.md`. The PR body must include:

1. **Changes** - Short, concise bullet points describing what changed. Include before/after screenshots if relevant.
2. **Testing** - Explain how the change was tested. If no tests were added, explain why.
3. **Docs** - Note if docs are needed. Tag `@withastro/maintainers-docs` for feedback if unsure.

Don't forget to run `pnpm exec changeset` before submitting!

## Working with GitHub Issues

### Identifying URL Types

**Regular issue URL:**

```
https://github.com/withastro/astro/issues/14481
                                       ^^^^^^
                                       Issue number
```

**Project board item URL:**

```
https://github.com/orgs/withastro/projects/21/views/1?pane=issue&itemId=154871753
                   ^^^^           ^^^^^^^^                       ^^^^^^^^^^^^^^^^
                   "orgs"         Project #                      Project item ID (NOT an issue number)
```

Key differences:

- Regular issues: `/repos/` or `/{owner}/{repo}/issues/{number}`
- Project items: `/orgs/{org}/projects/{number}` with `itemId` query param
- Project items can be **draft issues** (no linked repo issue), **linked issues**, or **pull requests**

### Fetching Regular Issues

Use `gh issue view` for regular repository issues:

```shell
# Fetch a specific issue by number
gh issue view 14481 --repo withastro/astro

# Fetch with full body content in JSON format
gh issue view 14481 --repo withastro/astro --json title,body,url,labels,state

# List recent issues
gh issue list --repo withastro/astro --limit 20
```

### Fetching Project Board Items

Project board URLs require GraphQL. The `itemId` in the URL is a project-specific database ID, not an issue number.

```shell
# Fetch a specific project item by its itemId (e.g., 154871753)
gh api graphql -f query='
query {
  organization(login: "withastro") {
    projectV2(number: 21) {
      items(first: 100) {
        nodes {
          databaseId
          type
          fieldValues(first: 20) {
            nodes {
              ... on ProjectV2ItemFieldTextValue {
                text
                field { ... on ProjectV2FieldCommon { name } }
              }
              ... on ProjectV2ItemFieldSingleSelectValue {
                name
                field { ... on ProjectV2FieldCommon { name } }
              }
            }
          }
          content {
            ... on Issue {
              title
              body
              url
              number
            }
            ... on DraftIssue {
              title
              body
            }
          }
        }
      }
    }
  }
}' | jq '.data.organization.projectV2.items.nodes[] | select(.databaseId == 154871753)'
```

**Important:** Project items with `"type": "DRAFT_ISSUE"` have no linked repository issue - their content is only in the `DraftIssue` fragment. Items with `"type": "ISSUE"` are linked to real repo issues.

### Common Issue Queries

```shell
# Search for issues by label
gh issue list --repo withastro/astro --label "bug" --limit 20

# Search issues by text
gh issue list --repo withastro/astro --search "cloudflare adapter"

# Get issue comments
gh api repos/withastro/astro/issues/14481/comments
```

## Downloading StackBlitz Reproductions

Bug reports often include StackBlitz reproductions. Use `stackblitz-clone` to download them:

```shell
# Clone a StackBlitz project to a directory
npx stackblitz-clone https://stackblitz.com/edit/project-id

# Clone to a specific directory
npx stackblitz-clone https://stackblitz.com/edit/project-id ./my-repro
```

You can also change the URL domain from `stackblitz.com` to `stackblitz.zip` to download directly:

```
Original:  https://stackblitz.com/edit/nuxt-starter-k7spa3r4
Download:  https://stackblitz.zip/edit/nuxt-starter-k7spa3r4
```
