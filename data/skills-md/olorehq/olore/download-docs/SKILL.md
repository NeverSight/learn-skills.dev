---
name: download-docs
description: Download and filter documentation from source configs. Use standalone to re-download without rebuilding artifacts.
---

# Download Docs

Download documentation files from a source config and filter non-useful files.

## Usage

```
/download-docs prisma@latest         # Download specific version
/download-docs prisma@latest --force  # Re-download even if exists
```

## Input

`$ARGUMENTS` format: `{config_name}@{version}` (e.g., `prisma@latest`, `nextjs@16.1.3`)

Optional flags:
- `--force` - Re-download even if already built

## Execution Steps

### Step 1: Parse Arguments and Load Config

Parse `$ARGUMENTS`:
- Extract `config_name` and `version` from `{config_name}@{version}`
- Check for `--force` flag

Load config file:
```bash
cat vault/configs/{config_name}.json
```

Extract:
- `name` - Package name
- `_source.type` - Source type (`github` or `url`)
- `_source.repo` - GitHub repo (if github type)
- `versions.{version}.ref` - Git ref for the version

### Step 2: Check if Already Built

```bash
test -f vault/packages/{config_name}/{version}/olore-lock.json && echo "EXISTS" || echo "NOT_FOUND"
```

If exists and no `--force` flag:
```
skip: {config_name}@{version} already built (use --force to rebuild)
```
Return early.

### Step 3: Download Documentation

**For GitHub sources:**
```bash
bash -c 'source .claude/skills/build-docs/scripts/github.sh && download_from_github "vault/configs/{config_name}.json" "vault/packages" "{version}"'
```

**For URL sources:**
```bash
bash -c 'source .claude/skills/build-docs/scripts/url.sh && download_from_urls "vault/configs/{config_name}.json" "vault/packages" "{version}"'
```

Verify download succeeded:
```bash
test -f vault/packages/{config_name}/{version}/olore-lock.json && echo "OK" || echo "FAILED"
```

If download failed, return error:
```
error: {config_name}@{version} download failed
```

### Step 4: Count Files and Determine Tier

```bash
file_count=$(find vault/packages/{config_name}/{version}/contents -type f \( -name "*.md" -o -name "*.mdx" \) | wc -l)
total_size=$(du -sk vault/packages/{config_name}/{version}/contents | cut -f1)
```

| Tier | Criteria |
|------|----------|
| 1 | < 30 files AND < 500KB |
| 2 | 30-100 files OR 500KB-2MB |
| 3 | > 100 files OR > 2MB |

### Step 5: Filter Files (GitHub sources with >50 files only)

**Skip this step if:**
- Source type is `url`
- File count is <= 50

**For GitHub sources with >50 files:**

1. For each file, read only the **first 20-30 lines** to make filtering decisions:
   - Frontmatter/metadata (YAML block)
   - Title and first heading
   - Opening paragraph describing the content

   This is sufficient to identify file type (changelog, RFC, API doc, tutorial, etc.).
   **Do NOT read entire files for filtering** - it wastes tokens on large repos.

2. Evaluate each file against criteria:

**KEEP** - Files that help developers USE the library:
- API reference documentation
- Usage guides and tutorials
- Configuration and setup docs
- Code examples and patterns
- Integration guides
- Troubleshooting guides

**DELETE** - Files NOT useful for using the library:
- Internal development docs
- Contribution guidelines
- Release notes and changelogs
- Meeting notes, RFCs, proposals
- Marketing and landing pages
- Duplicate or stub files
- Auto-generated index files with no content

3. Delete files that should be removed:
```bash
rm "vault/packages/{config_name}/{version}/contents/{path_to_delete}"
```

4. Remove empty directories:
```bash
find vault/packages/{config_name}/{version}/contents -type d -empty -delete
```

### Step 6: Update olore-lock.json

Update the lock file with final file count:

```bash
# Get final count
final_count=$(find vault/packages/{config_name}/{version}/contents -type f \( -name "*.md" -o -name "*.mdx" \) | wc -l)
```

Update `files` field in olore-lock.json if filtering occurred.

### Step 7: Return Summary

Return ONLY a brief summary:

```
done: {config_name}@{version} downloaded, {final_count} files{filtered_info}, tier {tier}
```

Examples:
- `done: prisma@latest downloaded, 312 files (126 filtered), tier 3`
- `done: zod@latest downloaded, 17 files, tier 1`

## Outputs

- `vault/packages/{config_name}/{version}/contents/` - Downloaded documentation files
- `vault/packages/{config_name}/{version}/olore-lock.json` - Build metadata
