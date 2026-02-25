---
name: knip
description: Run knip to find and remove unused files, dependencies, and exports. Use for cleaning up dead code and unused dependencies.
---

# Knip Code Cleanup

Run knip to find and remove unused files, dependencies, and exports from this codebase.

## Setup

1. Check if knip is available:
   - Run `npx knip --version` to test
   - If it fails or is very slow, check if `knip` is in package.json devDependencies
   - If not installed locally, install with `npm install -D knip` (or pnpm/yarn equivalent based on lockfile present)

2. If no `knip.json` or `knip.jsonc` config exists and knip reports many false positives, consider creating a minimal config based on the frameworks detected in package.json

## Execution

1. Run `npx knip` to get initial report
2. Review the output categories:
   - **Unused files** - files not imported anywhere
   - **Unused dependencies** - packages in package.json not imported
   - **Unused devDependencies** - dev packages not used
   - **Unused exports** - exported functions/variables not imported elsewhere
   - **Unused types** - exported types not used

## Cleanup Strategy

### Auto-delete (high confidence):
- Unused exports that are clearly internal (not part of public API)
- Unused type exports
- Unused dependencies (remove from package.json)
- Unused files that are clearly orphaned (not entry points, not config files)

For these, proceed with deletion without asking. Use `--fix --allow-remove-files` for automated fixes, or manually delete/edit as needed.

### Ask first (needs clarification):
- Files that might be entry points or dynamically imported
- Exports that might be part of a public API (index.ts, lib exports)
- Dependencies that might be used via CLI or peer dependencies
- Anything in paths like `src/index`, `lib/`, or files with "public" or "api" in the name

Use the AskUserQuestion tool to clarify before deleting these.

## Workflow

1. Run knip, capture full output
2. Categorize each issue as auto-delete or needs-clarification
3. Ask about uncertain items in a single batch question
4. Perform all deletions (use Edit tool to remove exports, Bash to remove files/deps)
5. Re-run knip to verify cleanup is complete
6. Repeat until no issues remain or only intentionally-ignored items exist

## Common Commands

```bash
# Basic run
npx knip

# Production only (ignore test files)
npx knip --production

# Auto-fix what's safe
npx knip --fix

# Auto-fix including file deletion
npx knip --fix --allow-remove-files

# JSON output for parsing
npx knip --reporter json
```

## Notes

- If knip config exists, respect its ignore patterns
- Watch for monorepo setups - may need `--workspace` flag
- Some frameworks need plugins enabled in config
- Re-run after each batch of fixes to catch newly-exposed unused code
