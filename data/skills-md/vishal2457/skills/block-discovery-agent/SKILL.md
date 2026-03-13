---
name: block-discovery-agent
description: Discover reusable code blocks from a repository, resolve project/category metadata with the TS CLI, and create a Linear issue ready for block creation.
---

# Block Discovery Agent

## Purpose

Identify reusable feature blocks in a codebase and produce a complete, implementation-ready Linear issue.

Primary outcomes:
- Discover the right source files for a reusable block.
- Use TS CLI commands to resolve project details and the correct `categoryId`.
- Create a Linear issue with all metadata needed for block creation.

## Required Tools

- TS CLI via: `npx derived-cli@latest`
- Linear MCP (for issue creation)
- Repository access for source-path discovery

## Workflow

### 1) Ensure project context is initialized

1. Confirm `.derived/project.json` exists.
2. If missing, initialize:

```bash
npx derived-cli@latest init <project-slug>
```

3. Fetch project details (authoritative source for project metadata):

```bash
npx derived-cli@latest project
```

Use this command output as the source of truth for project identity. Do not hardcode project IDs.

### 2) Resolve categories and categoryId

1. Fetch categories for the initialized project:

```bash
npx derived-cli@latest list-categories
```

2. Parse the returned JSON and match the best category by semantic intent.
3. If no category fits, create one:

```bash
npx derived-cli@latest create-category "<category-name>"
```

4. Re-run `list-categories` and select the new `categoryId`.

Selection rules:
- Prefer exact domain match (e.g., Auth, Payments, Dashboard).
- Fall back to closest functional match.
- If still ambiguous, ask the user to choose from top 3 candidates.

### 3) Parse user request for target block

Extract:
- Feature/module name
- Framework/runtime context
- Scope boundaries (what to include/exclude)

If ambiguous, ask focused clarifications before selecting files.

### 4) Discover reusable source paths

Include:
- Core feature implementation files
- Feature-local types and helpers
- Feature-specific config and wiring required for reuse

Exclude:
- Global/shared utilities not specific to the feature
- Build output, lockfiles, `node_modules`, `.env*`

Normalize paths to repository-relative paths rooted at template structure.

Output format:
- Semicolon-separated paths, e.g.

```text
src/features/auth/service.ts;src/features/auth/types.ts;src/features/auth/routes.ts
```

### 5) Compose block metadata

Prepare:
- `blockName`: readable, feature-focused
- `categoryId`: from `list-categories`
- `description`: 1-2 concise sentences
- `sourcePaths`: semicolon-separated
- `setupCommands`: comma-separated post-insert commands (or empty)
- `aiInstruction`: manual integration steps only (or empty)

### 6) Create Linear issue (required)

Create a Linear issue with title:

```text
Create Block: <Block Name>
```

Use this markdown description template:

````markdown
## Block Details

**Name**: <Block Name>
**Category ID**: <categoryId>
**Project**: <project name/slug from `derived-cli project`>

## Description
<description>

## Source Paths
```
<semicolon-separated-paths>
```

## Setup Commands
```
<comma-separated-commands>
```

## AI Instructions
```
<post-insertion-instructions>
```

## Validation
```bash
npm install && npm run build
```
````

Recommended issue metadata:
- Labels: `block-creation` plus framework label
- Priority: `2` (High)
```

## Decision Rules

If project context is missing:
1. Ask user to run `npx derived-cli@latest init <project-slug>`.
2. Re-run `project` and continue.

If category is unclear:
1. Show top matches from `list-categories`.
2. Ask user to select.
3. If needed, create category and retry.

If source scope is too broad:
1. Start with smallest functional slice.
2. Include only files required for independent reuse.

## Final Output Contract

After creating the Linear issue, respond with:

```text
Created Linear issue for block discovery.
```

And include:
- Linear issue ID/link
- Selected `categoryId`
- Final semicolon-separated source paths
