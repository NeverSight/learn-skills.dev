---
name: run-uat
description: Run User Acceptance Testing by creating a PR with rendered markdown on GitHub or Azure DevOps. Use when validating markdown rendering in real platforms.
compatibility: Requires git. GitHub UAT uses repo scripts which require GitHub CLI (gh) authenticated. Azure DevOps UAT requires Azure CLI (az) + azure-devops extension. Network access required.
---

# Run UAT

## Purpose
Execute end-to-end User Acceptance Testing by posting a feature-specific artifact and the comprehensive demo to a real PR on GitHub or Azure DevOps, then validating the rendered output.

## Hard Rules
### Must
- Provide at least one `--report`/`--instructions` pair (feature-specific report and test instructions).
- The comprehensive demo is appended automatically — do NOT add it as a `--report`.
- Artifacts must be up-to-date (generated from current branch code). Run `scripts/generate-demo-artifacts.sh` if needed.
- Clean up (close/abandon) the UAT PR after testing.
- Report platform-specific rendering issues clearly.

### Must Not
- Post a minimal or simulation artifact (reject files containing "minimal" or "simulation" in the name).
- Pass the comprehensive demo as a `--report` argument (added automatically).
- Leave UAT PRs open after testing completes.
- Modify any source code during UAT.

## Pre-requisites
- Git submodules initialized: `git submodule update --init --recursive`
- GitHub UAT: Authentication is automatic for coding agents (uses `GH_UAT_TOKEN`). For local dev: `gh auth login`.
- Azure DevOps UAT: Authentication is automatic for coding agents (uses `AZDO_UAT_TOKEN` → `AZURE_DEVOPS_EXT_PAT`). For local dev: set `AZURE_DEVOPS_EXT_PAT`.

## Recommended: Single Wrapper Command

```bash
# Minimum: one feature-specific report with test instructions
scripts/uat-run.sh \
  --report artifacts/<feature-specific-report>.md \
  --instructions "In azurerm_key_vault_secret.audit_policy, verify key_vault_id displays as 'Key Vault \`kv-name\` in resource group \`rg-name\`' instead of full /subscriptions/ path"

# Multiple feature-specific reports (all with instructions):
scripts/uat-run.sh \
  --report artifacts/feature-a.md \
  --instructions "Verify feature A renders correctly" \
  --report artifacts/feature-b.md \
  --instructions "Verify feature B renders correctly"

# GitHub only:
scripts/uat-run.sh \
  --report artifacts/<feature>.md \
  --instructions "..." \
  --platform github

# Create PRs without polling (for manual review workflow):
scripts/uat-run.sh \
  --report artifacts/<feature>.md \
  --instructions "..." \
  --create-only
# Then later clean up:
scripts/uat-run.sh --cleanup-last
```

## What the Script Does
1. Validates that all provided artifacts are up-to-date (built from current branch code)
2. Auto-configures GitHub/AzDO authentication for coding agent environments
3. Creates a unique UAT branch in the UAT repos
4. Creates UAT PR(s) on GitHub and/or Azure DevOps
5. Posts each feature report as a PR comment with the format:
   ```
   ## Test Instructions
   <instructions you provided>
   
   ## Report
   <artifact content>
   ```
6. Automatically appends `artifacts/comprehensive-demo-simple-diff.md` (GitHub) and `artifacts/comprehensive-demo.md` (AzDO) as the final regression test comment
7. Polls for approval (unless `--create-only`)
8. Cleans up PRs and branches on approval

## 0. Rebase on Latest Main
Before running UAT, ensure your branch is up to date to avoid testing against stale base changes.
Use the `git-rebase-main` skill.

## 1. Generate Fresh Artifacts (if needed)
```bash
# If script fails with "Artifact is outdated":
scripts/generate-demo-artifacts.sh

# For feature-specific artifacts:
dotnet run --project src/Oocx.TfPlan2Md/Oocx.TfPlan2Md.csproj -- \
  [your args] --output artifacts/<feature-specific>.md
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "Artifact is outdated" | Run `scripts/generate-demo-artifacts.sh` to regenerate all demo artifacts |
| "At least one --report/--instructions pair is required" | Provide `--report <file> --instructions "<text>"` |
| "Each --report must have a corresponding --instructions" | Check that `--report` and `--instructions` are properly paired |
| "GH_UAT_TOKEN is not set" | Add secret to Repository Settings > Environments > copilot |
| "AZDO_UAT_TOKEN not set" | Add secret to Repository Settings > Environments > copilot |
| Submodule not initialized | Run `git submodule update --init --recursive` |
| "Branch already exists" | Old UAT branch still present; run `scripts/uat-run.sh --cleanup-last` |
