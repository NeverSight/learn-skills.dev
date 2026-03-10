---
name: repair-broken-references
description: >
  Find and fix broken internal links, dead external URLs, stale imports,
  missing cross-references, and orphaned files. Ensures all project references
  remain valid and up-to-date. Use when documentation contains broken internal
  links, external URLs return 404 errors, import statements reference moved or
  deleted modules, cross-references between files are out of sync, or files
  exist but are never referenced anywhere in the project.
license: MIT
allowed-tools: Read Write Edit Bash Grep Glob
metadata:
  author: Philipp Thoss
  version: "1.0"
  domain: maintenance
  complexity: intermediate
  language: multi
  tags: maintenance, links, imports, references, orphans
---

# repair-broken-references

## When to Use

Use this skill when project references have become stale:

- Documentation contains broken internal links
- External URLs return 404 errors
- Import statements reference moved or deleted modules
- Cross-references between files are out of sync
- Files exist but are never referenced anywhere

**Do NOT use** for refactoring module dependencies or redesigning information architecture. This skill repairs existing references, not restructures them.

## Inputs

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `project_path` | string | Yes | Absolute path to project root |
| `check_external` | boolean | No | Verify external URLs (default: true, slow) |
| `fix_mode` | enum | No | `auto` (fix obvious), `report` (document only), `interactive` (prompt) |
| `orphan_threshold` | integer | No | Days since last modified to flag as orphan (default: 180) |

## Procedure

### Step 1: Scan for Broken Internal Links

Find all markdown links pointing to non-existent files.

```bash
# Find all markdown files
find . -name "*.md" -type f > markdown_files.txt

# Extract all markdown links: [text](path)
grep -oP '\[.*?\]\(\K[^)]+' *.md | sort | uniq > all_links.txt

# For each link:
while read link; do
  # Skip external URLs (http/https)
  if [[ "$link" =~ ^https?:// ]]; then
    continue
  fi

  # Resolve relative path
  target=$(realpath -m "$link")

  # Check if target exists
  if [ ! -e "$target" ]; then
    echo "BROKEN: $link (referenced in $file)" >> broken_internal.txt
  fi
done < all_links.txt
```

**Expected:** `broken_internal.txt` lists all broken internal references

**On failure:** If `realpath` unavailable, manually check each link

### Step 2: Check External URLs

Verify that external links are still accessible (HTTP 200 response).

```bash
# Extract external URLs
grep -ohP 'https?://[^\s\)]+' *.md | sort | uniq > external_urls.txt

# Check each URL (rate-limit to avoid bans)
while read url; do
  status=$(curl -o /dev/null -s -w "%{http_code}" "$url")

  if [ "$status" -ge 400 ]; then
    echo "DEAD ($status): $url" >> dead_urls.txt
  fi

  sleep 0.5  # Rate limit
done < external_urls.txt
```

**Expected:** `dead_urls.txt` lists URLs returning 4xx/5xx errors

**On failure:** If curl unavailable or blocked, use online link checker or skip

**Note**: Some URLs may return 403 due to bot detection but work in browsers. Manual review required.

### Step 3: Find Broken Imports

Check that all import/require statements reference existing modules.

**JavaScript/TypeScript**:
```bash
# Find all import statements
grep -rh "^import.*from ['\"]" . | sed -E "s/.*from ['\"]([^'\"]+)['\"].*/\1/" > imports.txt

# For each import:
while read import; do
  # Skip node_modules and external packages
  if [[ "$import" =~ ^[./] ]]; then
    # Resolve to file path
    target="${import}.js"  # Try .js, .ts, .jsx, .tsx

    if [ ! -e "$target" ]; then
      echo "BROKEN IMPORT: $import" >> broken_imports.txt
    fi
  fi
done < imports.txt
```

**Python**:
```bash
# Find all import statements
grep -rh "^from .* import\|^import " . --include="*.py" | \
  sed -E "s/from ([^ ]+) import.*/\1/" | \
  sed -E "s/import ([^ ]+)/\1/" > imports.txt

# For each local import (starts with .)
# Check if module file exists
```

**R**:
```bash
# Find library() and source() calls
grep -rh "library(\\|source(" . --include="*.R" | \
  sed -E 's/.*library\("([^"]+)"\).*/\1/' > packages.txt

# For source() calls, check if file exists
# For library() calls, check if package installed
Rscript -e "installed.packages()[,'Package']" > installed_packages.txt
```

**Expected:** `broken_imports.txt` lists all references to deleted/moved modules

**On failure:** If language-specific tool unavailable, manually review recent refactoring commits

### Step 4: Find Orphaned Files

Identify files that exist but are never referenced anywhere.

```bash
# Find all code files
find . -type f \( -name "*.js" -o -name "*.py" -o -name "*.R" \) > all_files.txt

# For each file:
while read file; do
  basename=$(basename "$file")

  # Search for references (import, require, source, href, link)
  refs=$(grep -r "$basename" . --exclude-dir=node_modules --exclude-dir=.git | wc -l)

  # If only 1 reference (itself):
  if [ "$refs" -le 1 ]; then
    # Check last modified date
    last_mod=$(git log -1 --format="%ci" "$file")

    # If modified more than orphan_threshold days ago
    # Flag as potential orphan
    echo "ORPHAN: $file (last modified: $last_mod)" >> orphans.txt
  fi
done < all_files.txt
```

**Expected:** `orphans.txt` lists files not referenced elsewhere

**On failure:** If git log fails, use filesystem mtime instead

**Note**: Some files (e.g., CLI entry points, top-level scripts) are legitimately unreferenced but not orphans. Requires manual review.

### Step 5: Fix Internal Links

Repair broken internal references using one of three strategies:

**Strategy 1: Find Moved Files**
```bash
# For each broken link, search for file by name
while read broken_link; do
  filename=$(basename "$broken_link")

  # Search for file in project
  found=$(find . -name "$filename" | head -1)

  if [ -n "$found" ]; then
    # Update link to new path
    old_path="$broken_link"
    new_path="$found"

    # Use Edit tool to replace in all markdown files
    echo "FIX: $old_path -> $new_path"
  fi
done < broken_internal.txt
```

**Strategy 2: Create Redirect Stub**
```bash
# If file was deleted intentionally, create redirect stub
echo "# Moved" > "$broken_link"
echo "This content moved to [new location](new_path.md)" >> "$broken_link"
```

**Strategy 3: Remove Dead Link**
```bash
# If content no longer exists, remove link (keep text)
# Replace [text](broken_link) with text (plain)
```

**Expected:** All broken internal links either fixed, redirected, or removed

**On failure:** If automated fix breaks context, escalate for manual review

### Step 6: Fix Broken Imports

Update import statements to reference correct paths after moves.

**JavaScript Example**:
```javascript
// Before (broken)
import { helper } from './utils/helper';

// After (fixed — file moved to lib/)
import { helper } from './lib/helper';
```

For each broken import:
1. Locate the moved module (similar to Step 5)
2. Update import path in all files referencing it
3. Run linter/type checker to verify fix

**Expected:** All imports resolve correctly; no module-not-found errors

**On failure:** If module was truly deleted, escalate to determine if functionality still needed

### Step 7: Document Orphaned Files

For files flagged as orphans, determine disposition:

1. **Keep**: Legitimately unreferenced (entry points, scripts, templates)
2. **Archive**: Old code no longer needed but preserve history
3. **Delete**: Dead code with no value

```markdown
# Orphaned Files Review

| File | Last Modified | Recommendation | Reason |
|------|---------------|----------------|--------|
| scripts/old_deploy.sh | 2024-01-05 | Archive | Replaced by CI/CD |
| src/legacy_api.js | 2023-06-12 | Delete | API v1 fully deprecated |
| bin/cli.py | 2025-12-01 | Keep | CLI entry point (unreferenced by design) |
```

**Expected:** Orphan review document created; automated decisions flagged for human approval

**On failure:** (N/A — document even if no clear disposition)

### Step 8: Generate Repair Report

Summarize all broken references and fixes applied.

```markdown
# Reference Repair Report

**Date**: YYYY-MM-DD
**Project**: <project_name>
**Fix Mode**: auto | report | interactive

## Broken Internal Links

- Total: X
- Fixed: Y
- Redirected: Z
- Escalated: W

Details:
- [file.md](file.md) line 45: Fixed broken link to moved doc
- [another.md](another.md) line 12: Created redirect stub

## Dead External URLs

- Total: X
- Fixed (wayback machine): Y
- Removed: Z

Details:
- https://example.com/old-page (404) → Removed
- https://api.old.com/docs (gone) → Replaced with new docs

## Broken Imports

- Total: X
- Fixed: Y
- Escalated: Z

Details:
- src/main.js line 3: Updated import path after refactor

## Orphaned Files

- Total: X
- Kept: Y
- Archived: Z
- Escalated for review: W

See ORPHAN_REVIEW.md for full analysis.

## Validation

- [x] All tests pass after fixes
- [x] Linter reports no module-not-found errors
- [x] Dead links documented in report
```

**Expected:** Report saved to `REFERENCE_REPAIR_REPORT.md`

**On failure:** (N/A — generate report regardless)

## Validation Checklist

After repairs:

- [ ] No broken internal links in documentation
- [ ] Dead external URLs documented (not all fixable)
- [ ] All imports resolve correctly
- [ ] Orphaned files reviewed and dispositioned
- [ ] Tests pass after import fixes
- [ ] Linter reports no unresolved references
- [ ] Git history preserved (used `git mv` for any moves)

## Common Pitfalls

1. **Automatic URL Fixes Break Context**: Replacing dead links with web.archive.org URLs may not be what the author intended. Some links are better removed.

2. **Over-Aggressive Orphan Deletion**: Entry points, CLI scripts, and templates are often unreferenced by design. Don't delete without review.

3. **Import Path Assumptions**: Assuming all relative imports use the same base path. Different module systems (CommonJS, ES6, TypeScript) handle paths differently.

4. **External URL False Positives**: Some sites block curl/bots but work fine in browsers. Always manually verify dead URLs.

5. **Circular Reference Traps**: File A imports B, B imports A. Updating one breaks the other. Requires simultaneous fix.

6. **Ignoring Fragment Identifiers**: Fixing `[link](#section)` requires checking if `#section` anchor exists, not just if file exists.

## Related Skills

- [clean-codebase](../clean-codebase/SKILL.md) — Remove dead code after confirming orphans
- [tidy-project-structure](../tidy-project-structure/SKILL.md) — Reorganize files (may create broken references)
- [escalate-issues](../escalate-issues/SKILL.md) — Route complex reference issues to specialists
- [compliance/documentation-audit](../../compliance/documentation-audit/SKILL.md) — Comprehensive documentation review
- [web-dev/link-checker](../../web-dev/link-checker/SKILL.md) — Advanced external URL validation
