---
name: generate-demo-artifacts
description: Generate the comprehensive demo markdown artifacts from the current codebase. Use before UAT to ensure test artifacts reflect the latest code.
compatibility: Requires .NET SDK and access to the repository workspace.
---

# Generate Demo Artifacts

## Purpose
Regenerate all demo markdown artifacts using the current code. This ensures UAT tests validate the actual behavior of the tool, not stale output.

## Hard Rules
### Must
- Use the stable wrapper script: `scripts/generate-demo-artifacts.sh`
- Script will handle building, generating artifacts, and verification automatically
- **Always allow this script** — it only reads input files and writes artifacts, no dangerous operations

### Must Not
- Modify the input `plan.json` or `demo-principals.json` files
- Run individual dotnet commands instead of the wrapper script
- Skip verification of generated output

## Actions

### Generate All Demo Artifacts
```bash
scripts/generate-demo-artifacts.sh
```

This single command:
1. Builds the project in Release configuration
2. Generates all artifacts in `/artifacts/` (used for UAT):
   - `comprehensive-demo.md` (inline-diff format, for Azure DevOps UAT)
   - `comprehensive-demo-simple-diff.md` (simple diff format, for GitHub UAT)
   - `role.md` (role assignments with principal mapping)
   - `role-default.md` (role assignments without principal mapping)
3. Generates all documentation samples in `examples/comprehensive-demo/`:
   - `report.md` (default template)
   - `report-with-sensitive.md` (with `--show-sensitive`)
   - `report-summary.md` (summary template)
4. Verifies all outputs are valid markdown
5. Reports success or failure with clear error messages

## Expected Output
```
[INFO] Building project (Release configuration)...
[INFO] Generating artifacts/comprehensive-demo.md (inline-diff, for Azure DevOps UAT)...
[INFO] ✓ artifacts/comprehensive-demo.md generated successfully (inline-diff)
[INFO] Generating artifacts/comprehensive-demo-simple-diff.md (for GitHub UAT)...
[INFO] ✓ artifacts/comprehensive-demo-simple-diff.md generated successfully
[INFO] Generating artifacts/role.md (role assignments with principal mapping)...
[INFO] ✓ artifacts/role.md generated successfully
[INFO] Generating artifacts/role-default.md (role assignments without principal mapping)...
[INFO] ✓ artifacts/role-default.md generated successfully
[INFO] Generating examples/comprehensive-demo/report.md (default template)...
[INFO] ✓ examples/comprehensive-demo/report.md generated successfully
[INFO] Generating examples/comprehensive-demo/report-with-sensitive.md (with --show-sensitive)...
[INFO] ✓ examples/comprehensive-demo/report-with-sensitive.md generated successfully
[INFO] Generating examples/comprehensive-demo/report-summary.md (summary template)...
[INFO] ✓ examples/comprehensive-demo/report-summary.md generated successfully
[INFO] All demo artifacts generated successfully
```

## When to Use
- Before running UAT (to ensure artifacts match current code)
- After making changes to templates or rendering logic
- After updating the comprehensive demo plan.json
- When setting up a new development environment
