---
name: wp-playground-development
description: WordPress Playground review and development guidance. Use when reviewing Blueprints, Playground JSON setup flows, `@wp-playground/cli` usage, embedded Playground demos, reproducible bug repros, docs examples, or when user mentions "WordPress Playground", "Blueprint", "playground.json", "run-blueprint", "build-snapshot", "embed Playground", or "zero-setup repro". Helps review Blueprint design, local Playground workflows, demo reliability, and reproducible WordPress environments.
---

# WordPress Playground Development Skill

## Overview

Systematic review guidance for WordPress Playground-based demos and reproducible environments. **Core principle:** Playground setups should be deterministic, portable, and easy to understand from the Blueprint or CLI entrypoint alone. Review covers Blueprint structure, local CLI usage, embedded demos, repro environments, and demo-specific WordPress configuration.

## When to Use

**Use when:**
- Reviewing a Blueprint JSON file
- Auditing docs that embed or link to Playground
- Building a zero-setup bug repro or demo
- Reviewing Playground CLI usage in local workflows or tests
- Designing a repeatable environment for blocks, plugins, or themes

**Don't use for:**
- General block or plugin review without Playground
- WP-CLI operations outside a Playground context
- Static analysis or CI setup alone

## Code Review Workflow

1. **Identify the Playground entrypoint**
   - Blueprint JSON
   - Playground CLI command
   - Embedded iframe or blueprint URL
   - Local docs or scripts used to reproduce an issue

2. **Check reproducibility first**
   - Explicit WordPress and PHP versions where needed
   - Steps are ordered and self-contained
   - No hidden manual steps outside the Blueprint/docs

3. **Review setup steps**
   - Theme/plugin install and activation
   - Login, site options, content seeding
   - File writes, copies, or mounts
   - Any `wp-cli` steps used inside the Blueprint

4. **Review developer ergonomics**
   - Can someone rerun this without guesswork?
   - Is the landing page meaningful?
   - Are local and browser-based flows clearly separated?

5. **Classify findings**
   - **CRITICAL:** non-reproducible setup, hidden dependencies, broken step order, external assumptions not documented
   - **WARNING:** versions implicit, overly brittle mounts, confusing landing page, heavyweight repro for a tiny issue
   - **INFO:** could simplify steps, split demo from test data, or use a clearer Blueprint pattern

## File-Type Specific Checks

### Blueprint Files

- CRITICAL: Missing required setup step that makes the Blueprint non-functional
- WARNING: No explicit `preferredVersions` when version compatibility matters
- WARNING: Repro depends on files adjacent to the Blueprint without documentation
- INFO: Could set a clearer `landingPage`

### Playground CLI Workflows

- WARNING: Local workflow uses `server` or `start` with undocumented mounts
- WARNING: Blueprint path or auto-mount assumptions are implicit
- INFO: Could use `run-blueprint` or `build-snapshot` for more deterministic flows

### Embedded Demos and Repros

- CRITICAL: Demo depends on manual admin setup not captured in the Blueprint
- WARNING: Embedded example is too large or generic for the issue being demonstrated
- INFO: Could split teaching/demo content from bug repro content

## Search Patterns for Quick Detection (PG-21)

Use these `rg` commands to find Playground-related files and setup logic.

### Playground Discovery

```bash
rg -n "playground|blueprint|@wp-playground" . -g '*.{md,json,js,ts,tsx,yml,yaml}'
rg -n "\"steps\"|\"landingPage\"|\"preferredVersions\"" . -g '*.json'
```

### CLI and Embed Flows

```bash
rg -n "run-blueprint|build-snapshot|@wp-playground/cli|npx @wp-playground/cli" . -g '*.{md,js,ts,sh,yml,yaml}'
rg -n "blueprint-url|playground.wordpress.net|wordpress.org/playground" . -g '*.{md,html,js,ts}'
```

### Repro Steps

```bash
rg -n "\"step\": \"(login|wp-cli|installPlugin|installTheme|writeFile|mkdir|cp|mv|enableMultisite)\"" . -g '*.json'
```

## Reference Files

- `references/blueprint-patterns.md` - Blueprint structure, step selection, and deterministic setup
- `references/cli-and-local-workflows.md` - `@wp-playground/cli`, mounts, local workflows, and snapshot usage
- `references/embedding-and-repros.md` - Embedded demos, blueprint URLs, and issue reproduction patterns
- `references/sample-playground-blueprint.json` - Minimal reproducible Blueprint fixture for local testing or adaptation

## Output Format (PG-23)

For each finding include:

1. Severity: `CRITICAL`, `WARNING`, or `INFO`
2. File and line number
3. Repro or demo issue summary
4. Why it matters for Playground reliability or clarity
5. Recommended fix

If no issues are found, say so clearly and mention any residual ambiguity such as version drift, missing repro notes, or fragile local mounts.
