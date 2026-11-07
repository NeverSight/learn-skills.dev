---
name: fortify-ssc
description: "Perform tasks against Fortify SSC (Software Security Center): query applications/application versions; query & triage existing security issues in SSC; start & monitor full ScanCentral SAST/DAST scans or upload FPR artifacts; create app versions; policy and portfolio analysis. NOT for lightweight AI review of local code changes/diffs (use fortify-change-review)."
license: MIT
metadata:
  version: "1.2.2"
  tested-with:
    fcli: "3.23"
    ssc: "26.2"
---

>SSC may also be referred to as "Fortify Software Security Center".

## Disambiguate "scan" / "review" first

These terms are overloaded. If ambiguous ("run a Fortify scan/review", "run a security review"), confirm user intent first:

- **scan** → 1) full ScanCentral SAST/DAST scan of the codebase (this skill), or 2) lightweight AI review of local code changes (`fortify-change-review`).
- **review** → 1) triage issues already found by SSC (this skill), or 2) lightweight AI review of local code changes (`fortify-change-review`).

## Verify Active SSC Session (skip if already confirmed this conversation)

```bash
fcli ssc session ls --query "expired=='No'"
```

**No active SSC session found:** Instruct the user to run `fcli ssc session login` and confirm successful login before proceeding.

**fcli not found:** You interact with SSC using `fcli`. It must already be on the PATH. If it is not installed, load `references/fcli-install.md`.

---

## SSC Logical Structure and Nomenclature

- **Applications** — top-level organizational unit; one per software project. **In fcli `--query` expressions and fcli output, the field is always `application` (e.g., `application.name`, `application.id`) — never `project.name`.** The "project" wording only appears in raw REST paths (`/api/v1/projects/`) and a handful of legacy ID-only fields like `projectVersionId`. Do not use `project.*` as a query field.
- **Application Versions** — versions/branches within an application (e.g., `main`, `v2.1`); each holds independent scan results and issues. A version can be seeded by copying state from another.
- **Artifacts** — FPR files uploaded to an application version containing scan results from one or more scan engines. After SSC processes an artifact, issues are updated on the version.
- **Issues** — vulnerabilities found by scans; always scoped to an application version.
- **Custom Tags** — tenant-defined metadata fields for auditing issues (e.g., `Analysis`, `Comment`). These are the primary mechanism for recording audit decisions in SSC.
- **Filter Sets** — rulesets that control how issues are grouped into priority folders. The default is "Security Auditor View" (Critical/High/Medium/Low).
- **Performance Indicators** — computed percentage metrics (e.g., % Critical Audited).
- **Variables** — tenant-defined numeric metrics derived from issue counts.

Teams typically structure SSC with one application per repo and versions per branch or environment (e.g., `main`, `v25.1`, `staging`).

## Key Concepts

### Issue Priority (Fortify Priority Order)
SSC organizes issues into named folders within a filter set using the **Fortify Priority Order (FPO)**: `Critical`, `High`, `Medium`, `Low`. The `friority` field (note: historical typo) is the primary priority indicator used in the UI and in queries. Do not confuse with the raw `severity` score (0.0–5.0).

### Scan Status (system-assigned per scan cycle)
`NEW` (first seen in latest scan), `UPDATED` (seen before, seen again), `REINTRODUCED` (was removed, now re-detected). Use `--query "scanStatus=='NEW'"` etc.

### Issue Visibility and `--include`
By default `fcli ssc issue list` returns **visible (non-suppressed, non-removed) issues only**.
- `--include=visible,suppressed` — add suppressed issues
- `--include=visible,removed` — add fixed/removed issues
- `--include=visible,suppressed,removed,hidden` — all issues

Visibility states: `visible`, `suppressed` (audit decision), `removed` (not found in latest scan), `hidden` (filtered by active filter).

### Audit Decisions — Custom Tags
SSC audit decisions are recorded via **custom tags**, not a fixed status enum. The most common is the `Analysis` tag with values like `Not an Issue`, `Exploitable`, `Reliability Issue`, `Suspicious`. The exact tags and values available depend on the tenant configuration. Use `fcli ssc custom-tag list --av=<appVersionNameOrId>` to discover them.

Suppression in SSC is an explicit boolean: `--suppress=true` via `fcli ssc issue update`. It is independent of custom tag values.

### Stable Issue Identity
Always use `issueInstanceId` (32-character hex string) as the canonical key for correlating the same issue across scans or versions. Do NOT use `id` (numeric, changes on reprocessing) for deduplication. Note: FoD calls the equivalent field `instanceId`.

### `--av`: The Only Version Identifier for Issue and Artifact Commands
`fcli ssc issue list`, `fcli ssc issue get`, `fcli ssc issue update`, `fcli ssc artifact list`, and all other version-scoped commands use **`--av` as the sole version identifier**. There is no separate `--app` or `--version` flag on these commands — do not invent one.

`--av` accepts a bare numeric version ID **or** a name string:
- Numeric ID (preferred when known): `--av=20001`
- Name string: `--av="MyApp:main"`

**When the user supplies a numeric version ID, use it directly as `--av=<id>` and skip all name-resolution steps.** A numeric version ID is globally unique in SSC — no application context is required alongside it.

### Querying Applications and Versions — Use `--query`, Not `--app`

`fcli ssc app list` and `fcli ssc appversion list` have **no `--app` flag** either. To filter them by application name, use `--query`:

```bash
# Find an application by name
fcli ssc app list --query "name=='Solidity Example'" -o json

# Find all versions of an application
fcli ssc appversion list --query "application.name=='Solidity Example'" -o json

# Find one specific version
fcli ssc appversion list --query "application.name=='Solidity Example' && name=='main'" -o json
```

The query field on `appversion list` is **`application.name`** (the version object embeds the parent application as `application`). It is **not** `project.name`, `app.name`, or `applicationName` — those are wrong on SSC. Names are case-sensitive. See `references/resolving-appversion.md` for fuzzy matching, delimiters, and `--store` chaining.

## Reference Files

Load these **only when needed** for the specific task at hand:

| File | When to load |
|------|--------------|
| `references/resolving-appversion.md` | Whenever you need to resolve an app or version name to an `--av` identifier and it isn't already explicit |
| `references/fcli-ssc-output-values.md` | Full field/enum reference for apps, versions, artifacts, issues, filter sets, attributes, performance indicators, variables |
| `references/fcli-ssc-output-samples.md` | Concrete JSON output examples for every object type (app, version, artifact, issue, issue count, filter set) |
| `references/fcli-query-output.md` | Detailed SpEL query syntax, null-safety patterns, output formats, `--store` variable chaining, server-side filtering, date utility functions |
| `references/output-formats.md` | Extended format options (`json-properties`, `--fetch=1`) and JSON processing scripting patterns |
| `references/fcli-install.md` | Full fcli installation and upgrade procedures |
| `references/mutating-operations.md` | Full safety rules for delete, create/update, access control, and REST mutations |
| `references/ssc-openapi-spec.json` | **Only** when constructing `fcli ssc rest` API calls — large file; load targeted sections only |
| `references/scdast-openapi-spec.json` | **Only** when constructing direct SC-DAST REST API calls (via `fcli sc-dast rest`) for operations not covered by named `fcli sc-dast` commands — large file; load targeted sections only |

## Use Case Files

Read the corresponding file before proceeding with any use case. Do not generate commands from memory — these files contain required command patterns, error states, and safety steps specific to each workflow. If a request spans multiple use cases, load all relevant files before proceeding.

| Use Case | When to use | File |
|----------|-------------|------|
| **Portfolio Overview** | Broad view across many applications or versions — listing, counting, grouping by status or activity, identifying versions needing attention at scale | `references/use-case-portfolio-overview.md` |
| **Application Version Context** | Detail about a specific application or version; resolving app/version names and `--av` identifiers; comparing versions within the same app; checking version health and metrics | `references/use-case-application-version-context.md` |
| **Creating a Version** | Creating a new version within an existing SSC application for a branch, release, or environment | `references/use-case-create-version.md` |
| **Artifact Upload & Processing** | Uploading FPR scan results to an application version; monitoring artifact processing status; checking upload history; handling processing errors | `references/use-case-artifact-upload-processing.md` |
| **Issue Investigation** | Vulnerability counts and category breakdowns for a specific version; filtering to specific issues; reading issue details; triaging and bulk-updating audit status or suppression | `references/use-case-issue-investigation.md` |
| **Start a Scan** | Submitting a new SAST scan via ScanCentral SAST or a new DAST scan via ScanCentral DAST; choosing how to run the scan (web UI, CI/CD, IDE plugin, or CLI); packaging code; checking for in-progress scans; waiting for completion; summarizing results | `references/use-case-start-scan.md` |
| **ScanCentral SAST Scan Status** | Observing SC-SAST scan jobs (listing running/queued/completed/failed jobs, filtering by time or submitter, counting throughput); checking sensor and pool utilization; downloading FPRs, logs, or sensor logs from completed jobs | `references/use-case-scsast-scan-status.md` |
| **ScanCentral DAST Scan Status** | Observing SC-DAST scans (listing running/queued/paused/complete/failed scans, filtering by state, time window, app, or URL); checking finding counts; sensor health and pool membership; downloading FPRs, results, logs, settings, or site trees | `references/use-case-scdast-scan-status.md` |
| **Advanced / REST API** | Operations not covered by named fcli commands; direct SSC REST API calls; general fallback | `references/use-case-advanced.md` |

---

## Never bypass fcli for SSC API access

All SSC API access must go through fcli — including when fcli seems slow or limited. **Never** read fcli's session or state files (`~/.fortify/fcli/state`, `$FCLI_STATE_DIR`), extract tokens or credentials from disk, or call SSC APIs directly with `curl`, `wget`, `requests`, `Invoke-WebRequest`, or any other HTTP client. The supported escape hatch for endpoints not covered by a named command is `fcli ssc rest call`. If fcli is genuinely unworkable for the task, tell the user — do not work around it.

---

## Safety Rules for Mutating Operations

> **These rules are mandatory.** Before executing any `create`, `update`, `delete`, or REST mutation command, load and follow `references/mutating-operations.md`. Read-only commands (`list`, `get`, `ls`) are always safe without confirmation.
---

## Output Formats

**Prefer `-o json` for programmatic work.** Parse JSON and summarize rather than relying on table output, which omits fields and truncates values.

For extended format options and JSON processing patterns, see `references/output-formats.md`. For `--query` SpEL syntax and `--store` chaining, see `references/fcli-query-output.md`.

For available fcli ssc modules and sub-commands, run `fcli ssc -h` or `fcli ssc <module> -h`.
