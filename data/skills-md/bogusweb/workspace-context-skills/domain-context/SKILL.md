---
name: domain-context
description: Automatically loads domain README.md context when you start working in a registered library or module. Reads architecture, public API, and patterns before touching domain-specific code. Activate when the task involves a specific library, domain path, or module the user references.
---

# Domain Context Auto-Loader

You have access to a **Domain Registry** that maps library paths to their documentation. When working on domain-specific code, you MUST silently load that domain's context before proceeding.

## Step 1 — Check for a Domain Registry

At the start of any task, look for this section in `CLAUDE.md`:

```markdown
## Domain Registry
<!-- domain-registry-start -->
| Path | Import Path | Description |
|------|-------------|-------------|
| libs/widget-chat | @scope/widget-chat | Chat widget |
<!-- domain-registry-end -->
```

If `## Domain Registry` is not present, skip all steps below.

## Step 2 — Match the Task to a Domain

Determine which domain is relevant based on:

- File paths mentioned by the user or referenced in the task (e.g. `libs/widget-chat/domain/store.ts`)
- Import paths in existing code (e.g. `@scope/widget-chat`)
- Domain or library names the user explicitly mentions (e.g. "work on widget-chat")
- If multiple domains are relevant, collect all matching paths

If no domain matches, proceed normally without loading any README.

## Step 3 — Load Domain Context

For each matched domain path, read the file at `<path>/README.md`.

**Do this silently.** Do NOT announce "I'm loading the README for...". Just read it and use the knowledge to:

- Understand the domain's architecture before suggesting any implementation
- Follow existing patterns documented in the README
- Reference correct import paths and public API surface
- Respect documented constraints or conventions

## Step 4 — Apply the Context

Use what you read to answer or implement with domain-accurate precision:

- Prefer patterns shown in the README over general Angular/NgRx defaults
- When the README describes a store shape, facade pattern, or component API — use it
- If the README contradicts your assumptions, trust the README

## What a Good Domain README Contains

If you're asked to generate or update a domain README, it should include:

```markdown
# <Domain Name>

One-line description.

## Architecture
Diagram or description of layers, key files, data flow.

## Public API
Exported services, components, stores with brief description of each.

## Key Patterns
Conventions specific to this domain (store shape, facade, etc.).

## Usage Example
Minimal code snippet showing how to import and use.

## Dependencies
What this domain depends on and what depends on it.
```

## Edge Cases

| Situation | Action |
|-----------|--------|
| `README.md` is missing | Skip silently, proceed with code exploration |
| README is outdated (contradicts code) | Trust the code, flag the discrepancy to the user |
| Multiple domains match | Load all matching READMEs |
| Domain registry not in CLAUDE.md | Skip all domain context loading |
