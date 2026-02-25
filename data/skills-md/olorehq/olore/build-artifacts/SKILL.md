---
name: build-artifacts
description: Generate SKILL.md and TOC.md for a documentation package. Use standalone to regenerate artifacts without re-downloading.
---

# Build Artifacts

Generate SKILL.md and TOC.md for an existing documentation package.

## Usage

```
/build-artifacts prisma@latest         # Generate artifacts
/build-artifacts prisma@latest --force  # Regenerate even if exists
```

## Input

`$ARGUMENTS` format: `{config_name}@{version}` (e.g., `prisma@latest`, `nextjs@16.1.3`)

Optional flags:
- `--force` - Regenerate even if artifacts already exist

## Prerequisites

The `contents/` directory and `olore-lock.json` must already exist at `vault/packages/{config_name}/{version}/`. Run `/download-docs` first if they don't.

```bash
test -d vault/packages/{config_name}/{version}/contents && echo "OK" || echo "NOT_FOUND"
```

If `contents/` not found:
```
error: {config_name}@{version} contents/ not found - run /download-docs first
```

## Execution Steps

### Step 1: Parse Arguments and Load Metadata

Parse `$ARGUMENTS`:
- Extract `config_name` and `version` from `{config_name}@{version}`
- Check for `--force` flag

Read metadata:
```bash
cat vault/packages/{config_name}/{version}/olore-lock.json
cat vault/configs/{config_name}.json
```

### Step 2: Check if Already Built

```bash
test -f vault/packages/{config_name}/{version}/SKILL.md && test -f vault/packages/{config_name}/{version}/TOC.md && echo "EXISTS" || echo "NOT_FOUND"
```

If both exist and no `--force` flag:
```
skip: {config_name}@{version} artifacts already built (use --force to rebuild)
```
Return early.

### Step 3: Determine Tier

```bash
file_count=$(find vault/packages/{config_name}/{version}/contents -type f \( -name "*.md" -o -name "*.mdx" \) | wc -l)
total_size=$(du -sk vault/packages/{config_name}/{version}/contents | cut -f1)
```

| Tier | Criteria |
|------|----------|
| 1 | < 30 files AND < 500KB |
| 2 | 30-100 files OR 500KB-2MB |
| 3 | > 100 files OR > 2MB |

### Step 4: Generate TOC.md

Read the appropriate template based on tier:

```bash
# Tier 1
cat vault/packages/docs-packager/1.0.0/templates/toc-tier1.md

# Tier 2
cat vault/packages/docs-packager/1.0.0/templates/toc-tier2.md

# Tier 3
cat vault/packages/docs-packager/1.0.0/templates/toc-tier3.md
```

Create `vault/packages/{config_name}/{version}/TOC.md` following the template structure.

### Step 5: Generate SKILL.md

**IMPORTANT:** The `name` field MUST be `olore-{config_name}-{version}` to match the installed folder name.

Read the appropriate template based on tier:

```bash
# Tier 1
cat vault/packages/docs-packager/1.0.0/templates/skill-tier1.md

# Tier 2
cat vault/packages/docs-packager/1.0.0/templates/skill-tier2.md

# Tier 3
cat vault/packages/docs-packager/1.0.0/templates/skill-tier3.md
```

Create `vault/packages/{config_name}/{version}/SKILL.md` following the template structure.

### Step 6: Return Summary

Return ONLY a brief summary:

```
done: {config_name}@{version} artifacts built (SKILL.md + TOC.md), tier {tier}
```

## Outputs

- `vault/packages/{config_name}/{version}/SKILL.md` - Skill definition
- `vault/packages/{config_name}/{version}/TOC.md` - Table of contents
