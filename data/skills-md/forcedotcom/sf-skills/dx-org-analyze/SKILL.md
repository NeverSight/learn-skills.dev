---
name: dx-org-analyze
description: "Compare two Salesforce orgs side-by-side and produce a comparison report with drift score, or analyze a single org to produce an inventory covering metadata components, org permissions, system permissions, profiles, installed packages, licenses, and org limits. Use this skill when the user wants to compare orgs, diff orgs, audit configuration drift, find what changed between two environments, compare sandbox against production, or analyze a single org. Trigger phrases include: 'compare orgs', 'compare these 2 orgs', 'compare my orgs', 'diff orgs', 'org diff', 'what is different between these orgs', 'compare metadata', 'org comparison', 'audit org differences', 'compare sandbox to production', 'introspect org', 'org inventory', 'what is in my org', 'analyze org', 'org analysis', 'analyze my org', 'analyze my Salesforce org'. Do NOT use for retrieving metadata (use platform-metadata-retrieve), deploying metadata (use platform-metadata-deploy), or switching orgs (use dx-org-switch)."
allowed-tools: Bash Read
metadata:
  version: "1.0"
  minApiVersion: "62.0"
  domains: ["Developer Experience"]
  relatedSkills:
    - "dx-org-manage"
    - "dx-org-switch"
    - "platform-metadata-deploy"
    - "platform-metadata-retrieve"
  cliTools:
    - tool: ["python3"]
      semver: ">=3.10"
    - tool: ["sf"]
      semver: ">=2.0.0"
---

## Tool Restrictions

**Use ONLY the Bash tool** to execute all `sf` CLI commands and Python scripts. Always include `--json` for `sf` commands. Do NOT use `mcp__salesforce_dx__*` tools.

**Output artifacts for eval/testing:** When an output directory is available, write results there. After executing the skill: (1) if the user specified an output path, write there immediately; (2) otherwise run `[ -d force-app/main/adk-eval-output/ ] && echo 'force-app/main/adk-eval-output'` to detect the eval directory; (3) write the full JSON result to `<output-dir>/dx-org-analyze-result.json` and the markdown report to `<output-dir>/dx-org-analyze-result.md`.

---

## Data Access Hierarchy

When querying org data, always follow this priority order:

1. **SF CLI commands** — Preferred. Use `sf org list metadata-types`, `sf org list metadata`, `sf org display`, `sf data query`, `sf limits api display`, etc.
2. **Direct REST/Tooling API calls** — Last resort, only when SF CLI cannot provide the data.

Never bypass this hierarchy. If an SF CLI command exists for the operation, use it even if a direct API call would be simpler.

---

## Authentication Rules

- **All authentication MUST go through SF CLI** (`sf org login web`, `sf org login jwt`, `sf org login access-token`).
- Never accept raw credentials (username + password), session IDs, or access tokens directly from the user.
- The collection script obtains its access token exclusively via `sf org display --json`.

---

## Workflow

### Step 0: List Authenticated Orgs

Run this command to discover all authenticated orgs:

```bash
sf org list --json --skip-connection-status
```

Parse the JSON output. Collect orgs from **all buckets** (`devHubs`, `nonScratchOrgs`, `scratchOrgs`, `sandboxes`, `other`). Present authenticated orgs in a readable table:

| # | Alias | Username | Instance URL | Org ID | Type |
|---|-------|----------|--------------|--------|------|

If fewer than 2 orgs are authenticated but at least 1 is available, offer the **single-org introspect** mode (see Introspect Workflow below). If no orgs are authenticated, STOP and advise:
> You need at least 1 authenticated org. Run `sf org login web --alias <name>` to authenticate.

If the user explicitly requests a single-org introspection or inventory, use the **Introspect Workflow** regardless of how many orgs are available.

### Step 1: User Selects Two Orgs

Ask the user to select two orgs from the list. Both must be explicitly named — do NOT allow implicit/default orgs.

> Select two orgs to compare. Which is the **source** (reference/expected state)? Which is the **target** (to compare against)?

Accept: alias, username, or number from the list. Resolve each selection to a concrete **username**. If an org lacks an alias, prompt the user to assign one. Confirm:

> Comparing:
> - **Source**: `<alias>` (`<username>`)
> - **Target**: `<alias>` (`<username>`)

### Step 2: Validate Connectivity

For each org, confirm reachability with a lightweight query that does not expose secrets:

```bash
sf data query --target-org <alias-or-username> --query "SELECT Id FROM Organization LIMIT 1" --json
```

If the query succeeds (exit 0 and a record is returned), the org is connected. If it fails with `INVALID_SESSION_ID` or auth errors:
```bash
sf org login web --alias <alias>
```

### Step 3: Collect Data (per org)

Generate a unique run ID and run the collection script for each org:

```bash
RUN_ID=$(date +%Y%m%d-%H%M%S)

python3 ./scripts/collect_org_data.py \
  --org-alias "$SOURCE_ORG" \
  --output /tmp/dx-org-comparison-${RUN_ID}-source

python3 ./scripts/collect_org_data.py \
  --org-alias "$TARGET_ORG" \
  --output /tmp/dx-org-comparison-${RUN_ID}-target
```

**Exit codes:** `0` = success, `1` = fatal error (report stderr to user), `2` = session expired (re-authenticate Step 2 and retry).

For details on what the collection script gathers, see `references/collection-details.md`.

### Step 4: Compute Diff and Report

```bash
python3 ./scripts/compute_diff.py \
  --org-a /tmp/dx-org-comparison-${RUN_ID}-source \
  --org-b /tmp/dx-org-comparison-${RUN_ID}-target \
  --output /tmp/dx-org-comparison-${RUN_ID} \
  --format both \
  --org-a-label "Source" \
  --org-b-label "Target"
```

Use `--show-shared` if the user wants shared components listed in detail.

### Step 5: Present Results

Read `/tmp/dx-org-comparison-${RUN_ID}.md` and present to the user. If the user asks follow-up questions, use `/tmp/dx-org-comparison-${RUN_ID}.json` for data lookups. Then resolve the output directory and copy both files there:

```bash
OUTPUT_DIR=""
if [ -n "$USER_OUTPUT_PATH" ]; then
  OUTPUT_DIR="$USER_OUTPUT_PATH"
elif [ -d "force-app/main/adk-eval-output" ]; then
  OUTPUT_DIR="force-app/main/adk-eval-output"
fi

if [ -n "$OUTPUT_DIR" ]; then
  cp /tmp/dx-org-comparison-${RUN_ID}.json "$OUTPUT_DIR/dx-org-analyze-result.json"
  cp /tmp/dx-org-comparison-${RUN_ID}.md "$OUTPUT_DIR/dx-org-analyze-result.md"
fi
```

---

## Introspect Workflow (Single-Org Mode)

Use this workflow when the user wants to inspect a single org's configuration, or when only one org is authenticated.

### Introspect Step 1: Validate Connectivity

```bash
sf data query --target-org <alias-or-username> --query "SELECT Id FROM Organization LIMIT 1" --json
```

### Introspect Step 2: Collect Data

```bash
RUN_ID=$(date +%Y%m%d-%H%M%S)

python3 ./scripts/collect_org_data.py \
  --org-alias "$ORG" \
  --output /tmp/dx-org-analysis-${RUN_ID}
```

### Introspect Step 3: Generate Report

```bash
python3 ./scripts/introspect_org.py \
  --org /tmp/dx-org-analysis-${RUN_ID} \
  --output /tmp/dx-org-analysis-${RUN_ID} \
  --format both \
  --label "OrgName"
```

### Introspect Step 4: Present Results

Read `/tmp/dx-org-analysis-${RUN_ID}.md` and present to the user. The report covers: metadata inventory, org settings, org limits, installed packages, licenses, system permissions, and deep data records. Then resolve the output directory and copy both files there:

```bash
OUTPUT_DIR=""
if [ -n "$USER_OUTPUT_PATH" ]; then
  OUTPUT_DIR="$USER_OUTPUT_PATH"
elif [ -d "force-app/main/adk-eval-output" ]; then
  OUTPUT_DIR="force-app/main/adk-eval-output"
fi

if [ -n "$OUTPUT_DIR" ]; then
  cp /tmp/dx-org-analysis-${RUN_ID}.json "$OUTPUT_DIR/dx-org-analyze-result.json"
  cp /tmp/dx-org-analysis-${RUN_ID}.md "$OUTPUT_DIR/dx-org-analyze-result.md"
fi
```

---

## Report Structure

The generated report includes:

1. **Drift Score** — Weighted overall score (60% metadata, 30% permissions, 10% profiles) with severity level (LOW/MODERATE/HIGH/CRITICAL)
2. **Summary Statistics** — Counts per metadata type with Identical/Different columns from deep data
3. **Metadata Components by Type** — Only-in-Source, only-in-Target, shared per type
4. **Profiles** — Shared, source-only, target-only
5. **Installed Packages** — Version comparison, only-in-Source, only-in-Target
6. **Package Components** — Namespaced components grouped by namespace
7. **Org Permissions** — Boolean enabled/disabled diffs by category, plus value diffs
8. **System Permissions** — PermissionsXxx fields on PermissionSet, per-set diffs
9. **Org Values & Limits** — Grouped by Identity, Storage, API, Feature Limits
10. **Licenses** — User, Permission Set, Package license quantity diffs
11. **Deep Data** — Content-level diffs for Apex, Flows, Validation Rules, Custom Fields, etc.

---

## Rules / Constraints

| Constraint | Rationale |
|-----------|-----------|
| Always use `--json` with sf commands | Structured output for reliable parsing |
| Resolve orgs to usernames, not aliases | Aliases can be ambiguous; usernames are unique |
| Skip expired and disconnected orgs | Cannot query metadata from inaccessible orgs |
| Read-only — never deploy or modify | This skill compares only, never mutates either org |
| SF CLI auth only | All authentication through SF CLI credential store |
| Both orgs must be explicit | Never compare unnamed or implicit/default orgs |

---

## Troubleshooting

| Issue | Resolution |
|-------|------------|
| "No org found for \<alias\>" | Org not authenticated — run `sf org login web --alias <name>` |
| Fewer than 2 authenticated orgs | Authenticate additional orgs before comparing |
| "INVALID_SESSION_ID" or auth errors | Session expired — re-run `sf org login web --alias <name>` |
| Collection script exits with code 2 | Session expired — re-authenticate and retry |
| API limit errors during metadata listing | Use `--skip-deep-data` for a faster pass with less detail |
| Edition differences (DE vs EE) | Many differences are edition-inherent, not configuration drift |
| Large orgs timeout on deep data | Use `--skip-deep-data` flag; run full deep data on targeted follow-ups |

---

## Cross-Skill Integration

| Need | Delegate to |
|------|-------------|
| Retrieve specific metadata from an org | `platform-metadata-retrieve` |
| Deploy metadata to an org | `platform-metadata-deploy` |
| Create a scratch org for comparison | `dx-org-manage` |
| Switch default org after comparison | `dx-org-switch` |

---

## Reference File Index

| File | When to read |
|------|-------------|
| `references/collection-details.md` | For details on what the collection script gathers and how |
| `references/report-format.md` | For drift score formula and report section details |
| `scripts/collect_org_data.py` | Data collection script (per org) |
| `scripts/compute_diff.py` | Diff computation and report generation script |
| `scripts/introspect_org.py` | Single-org introspection report script |
