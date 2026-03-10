---
name: update-test-snapshots
description: Regenerate test snapshot files after intentional markdown output changes. Use after modifying templates or rendering logic.
compatibility: Requires .NET SDK and access to the test project.
---

# Update Test Snapshots

## Purpose
Regenerate all test snapshot (golden file) baselines when intentional changes are made to markdown output. This updates the expected outputs that snapshot tests compare against.

## Hard Rules
### Must
- Use the stable wrapper script: `scripts/update-test-snapshots.sh`
- Script will handle deleting old snapshots, running tests, and verification automatically
- **Always allow this script** — it only modifies test snapshot files, no production code
- Review the git diff of snapshot changes before committing

### Must Not
- Manually copy files to update snapshots
- Update snapshots without understanding why they changed
- Run without first verifying the new output is correct
- Skip reviewing snapshot diffs before committing

## Actions

### Regenerate All Snapshots
```bash
scripts/update-test-snapshots.sh
```

This single command:
1. Deletes all existing snapshot files in `src/tests/Oocx.TfPlan2Md.Tests/TestData/Snapshots/`
2. Runs snapshot tests (which will fail but create new snapshots)
3. Counts generated snapshots to verify success
4. Runs snapshot tests again to verify they pass with new baselines
5. Reports success with instructions to review changes

## Expected Output
```
[INFO] Deleting existing snapshot files...
[INFO] ✓ Deleted 6 snapshot files
[INFO] Running snapshot tests to regenerate files...
[INFO] (Tests will fail on first run, but will create new snapshots)
[INFO] ✓ Generated 6 new snapshot files
[INFO] Running snapshot tests again to verify...
[INFO] ✅ All snapshot tests pass!

Snapshots updated successfully. Review changes with:
  scripts/git-diff.sh src/tests/Oocx.TfPlan2Md.Tests/TestData/Snapshots
```

## When to Use
- After intentionally modifying markdown rendering logic (C# renderers)
- After changing markdown rendering logic
- After updating formatting rules (value escaping, table formatting, etc.)
- After adding new snapshot tests
- When snapshot tests fail due to expected changes

## What Gets Updated
Snapshot files in `src/tests/Oocx.TfPlan2Md.Tests/TestData/Snapshots/`:
- `comprehensive-demo.md` - Full comprehensive demo output
- `summary-template.md` - Summary template output
- `breaking-plan.md` - Edge cases with escaping
- `role-assignments.md` - Role assignment rendering
- `firewall-rules.md` - Firewall rule semantic diff
- `multi-module.md` - Multi-module plan output

## After Running
Always review the changes:
```bash
scripts/git-diff.sh src/tests/Oocx.TfPlan2Md.Tests/TestData/Snapshots/
```

Verify the changes match your expectations, then stage and commit:
```bash
git add src/tests/Oocx.TfPlan2Md.Tests/TestData/Snapshots/
git commit -m "test: update snapshots after [describe change]"
```
