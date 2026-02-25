---
name: build-docs
description: Build documentation packages from configs. Downloads docs, filters with AI, generates SKILL.md. Use when setting up or updating local documentation.
---

# Build Docs

Build documentation packages from configs in `vault/configs/`.

## Usage

```
/build-docs                      # All configs, all versions
/build-docs prisma               # All versions for prisma config
/build-docs prisma@latest        # Specific version only
/build-docs prisma zod           # Multiple configs
/build-docs prisma --force       # Re-download even if exists
```

## Workflow

### Phase 1: Parse Arguments

Parse `$ARGUMENTS`:
- No args → Process all configs in `vault/configs/*.json`
- `name` without `@` → All versions for that config
- `name@version` → Specific version only
- `--force` flag → Re-download even if exists

### Phase 2: Discover Work

For each config, list versions and check what needs building:

```bash
# List configs
ls vault/configs/*.json

# Get versions from a config
jq -r '.versions | keys[]' vault/configs/{name}.json

# Check if version is built (olore-lock.json exists)
test -f vault/packages/{name}/{version}/olore-lock.json
```

**Built** = `vault/packages/{name}/{version}/olore-lock.json` exists
**Work** = versions without olore-lock.json (unless `--force`)

### Phase 3: Report Plan and Confirm

Show what will be built and ask for confirmation:

```
Build plan:
  prisma@latest - not built
  zod@latest - exists (skip)
  nextjs@16.1.3 - not built

Will build 2 packages. Proceed?
```

### Phase 4: Spawn Subagents (PARALLEL)

**CRITICAL: Spawn ALL subagents in a SINGLE message for parallel execution.**

For each package that needs building, spawn a `package-builder` subagent:

```
Use package-builder agent: prisma@latest
Use package-builder agent: nextjs@16.1.3
```

If `--force` flag was set, pass it to subagents:
```
Use package-builder agent: prisma@latest --force
```

**Example with 3 packages:**
In ONE message, spawn THREE subagents:
- `package-builder: prisma@latest`
- `package-builder: zod@latest`
- `package-builder: nextjs@16.1.3`

All subagents run in parallel. Each handles:
1. Download docs from source
2. Filter files (if needed)
3. Generate TOC.md
4. Generate SKILL.md

### Phase 5: Summary

Collect results from all subagents and report:

```
Build complete:
  ✅ prisma@latest - 312 files (126 filtered), tier 3
  ✅ zod@latest - 17 files, tier 1
  ⏭️  nextjs@16.1.3 - skipped (exists)

Install with: olore install ./vault/packages/prisma/latest
```

## Config Structure

Config file: `vault/configs/prisma.json`
```json
{
  "name": "prisma",
  "_source": { "type": "github", "repo": "prisma/docs", "path": "content" },
  "versions": {
    "latest": { "ref": "main" }
  }
}
```

## Package Structure (after build)

```
vault/packages/{name}/{version}/
├── olore-lock.json    # Build metadata
├── SKILL.md           # Skill definition (generated)
├── TOC.md             # Table of contents (generated)
└── contents/
    └── *.md           # Documentation files
```

## After Build

**For development** (changes immediately visible):
```
olore link ./vault/packages/prisma/latest
```

**For testing final package** (copies to ~/.olore):
```
olore install ./vault/packages/prisma/latest
```

After install/link, skills are available as `/olore-<name>-<version>` (e.g., `/olore-prisma-latest`).

## Standalone Skills

Individual phases can be run independently without the full pipeline:

```
/download-docs prisma@latest         # Download + filter only
/build-artifacts prisma@latest       # Regenerate SKILL.md + TOC.md only
/build-index prisma@latest           # Regenerate INDEX.md only
```

Use `--force` on any standalone skill to regenerate even if output exists.

**Dependencies:**
- `/download-docs` has no dependencies (runs first)
- `/build-artifacts` requires `contents/` from `/download-docs`
- `/build-index` requires `contents/` from `/download-docs`
- `/build-artifacts` and `/build-index` are independent of each other

## Reference

- [Adding new documentation](adding-docs.md) - Config file format, GitHub/URL sources
- [Conventions](conventions.md) - Config vs lock files, naming rules
- Templates: `vault/packages/docs-packager/1.0.0/templates/` (single source of truth)

## Requirements

- `jq` - JSON parsing
- `git` - GitHub cloning
- `curl` - URL downloads
