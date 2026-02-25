---
name: fortify-fod
description: "use this skill whenever the user wants to list and filter application security findings, run SAST/SCA/DAST scans, discover applications and releases, and manage security scanning using Fortify on Demand (FoD). Triggers include: any mention of 'FoD', 'Fortify on Demand', 'list vulnerabilities', 'run SAST scan', 'run SCA scan', 'run DAST scan', 'list applications', 'list releases', 'package source code', 'security scan', and similar requests indicating interaction with FoD for application security scanning and vulnerability management."
compatibility: Requires Fortify MCP configured for FoD, and authenticated session to FoD.
metadata:
  author: crance
  version: "0.0.1"
---

# Fortify on Demand (FoD) Skill
Fortify on Demand (FoD) integration via Model Context Protocol (MCP).

## When to Use This Skill
- List applications and releases
- Run security scans (SAST, SCA, DAST, MAST)
- List security issues/vulnerabilities with filtering by severity, category, etc.
- Count issues grouped by severity, category, etc.
- Manage scan configurations and monitor scan progress
- Generate and download security reports

## Available MCP Tools
Only key MCP tools for FoD are listed here.
| Tool | Description | When to Use |
|-----------|-------------|-------------|
| `fcli_fod_session_list` | List authentication sessions | Check authentication status |
| `fcli_fod_app_list` | List applications | Discover available applications |
| `fcli_fod_app_get` | Get details of a specific application | Retrieve detailed information about an application |
| `fcli_fod_release_list` | List releases | Discover available releases |
| `fcli_fod_release_get` | Get details of a specific release | Retrieve detailed information about a release |
| `fcli_fod_release_list_assessment_types` | List available scan types for release | Discover which scan types are available |
| `fcli_fod_issue_list` | List issues/vulnerabilities | Retrieve security findings |
| `fcli_fod_issue_update` | Update vulnerability status | Change analysis tags, add comments, suppress issues |
| `fcli_fod_action_package` | Package source code for scanning | Prepare source code for SAST/SCA scans |
| `fcli_fod_sast_scan_setup` | Configure SAST scan settings | Set up static analysis scan parameters |
| `fcli_fod_sast_scan_start` | Start SAST scan | Upload package and initiate static scan |
| `fcli_fod_sast_scan_get_config` | Get SAST scan configuration | Retrieve current SAST scan settings (uses release name) |
| `fcli_fod_sast_scan_get` | Get SAST scan details by scan ID | Check specific scan status (requires scan ID from start response or scan list) |
| `fcli_fod_sast_scan_wait_for` | Wait for SAST scan completion | Monitor scan until finished |
| `fcli_fod_oss_scan_start` | Start SCA/OSS scan | Upload package and initiate open source scan |
| `fcli_fod_oss_scan_get` | Get SCA scan details by scan ID | Check specific SCA scan status (requires scan ID from start response or scan list) |
| `fcli_fod_oss_scan_list_components` | List detected open source components | View OSS components found in scan |
| `fcli_fod_dast_scan_setup_website` | Configure website DAST scan | Set up dynamic analysis for web apps |
| `fcli_fod_dast_scan_setup_api` | Configure API DAST scan | Set up dynamic analysis for APIs |
| `fcli_fod_dast_scan_get_config` | Get DAST scan configuration | Retrieve current DAST scan settings (uses release name) |
| `fcli_fod_dast_scan_start` | Start DAST scan | Initiate dynamic security scan |
| `fcli_fod_report_create` | Create security report | Generate reports from scan results |
| `fcli_fod_report_download` | Download report file | Retrieve generated report |
| `fcli_fod_report_wait_for` | Wait for report generation | Monitor report creation until complete |

## Parameter Formats
Common formats and examples for key parameters:
| Parameter | Format | Example |
|-----------|-------------|-------------|
| `--fod-session` | Session name (REQUIRED for all tools) | `"default"` |
| `--release` | `"<App>:<Release>"` - case-sensitive, colon-separated (for `*_list`, `*_scan_setup`, `*_scan_start`, `*_scan_get_config` tools) |  `"MyApp:MyRelease"` |
| `--qualifiedReleaseNameOrId` | `"<App>:<Release>"` - case-sensitive, colon-separated (for `release_get`, `app_get` tools) |  `"MyApp:MyRelease"` |
| `releaseQualifiedScanOrId` | Scan ID or qualified scan ID (for `*_scan_get` tools) - **Always use scan ID returned from `*_scan_start` or from `*_scan_list`** | `"12345"` or `"MyApp:MyRelease:12345"` |
| `--filters-param` | `"<FilterName>:<Value>"` - server-side filtering | `"severityString:Critical"` |
| `--include` | Control which issue statuses to include. By default, only `visible` issues returned. Comma-separated values: `visible`, `fixed`, `suppressed` | `"visible,fixed"` or `"suppressed"` |
| `--embed` | Comma-separated values to include additional data. Valid values: `allData`, `summary`, `details`, `recommendations`, `history`, `requestResponse`, `headers`, `parameters`, `traces` | `"details,recommendations,history"` |
| `file` | Path to packaged zip or report output | `"package.zip"`, `"report.pdf"` |

## Authentication
**All operations require authentication.** Always verify session before any operation:
```tool
fcli_fod_session_list refresh-cache=true
```
- If `Expired` = `No` → proceed
- If expired → ask user to run locally: `fcli fod session login --url <URL> --client-id <id> --client-secret <secret>`
- When running any FoD tool, if authentication error occurs, prompt user to re-authenticate locally.

**Note:** Reference workflows assume authentication has been verified.

## Domain-Specific Guidance

### Scan Workflows: Always Check Settings First
Before starting any scan, follow this sequence:
1. **Check existing scan configuration** using `*_scan_get_config` command
2. **If not configured** → Always ask user for required settings (language, build tool, framework, etc.)
3. **Never infer settings** from workspace - build tools, language versions, and frameworks must be user-confirmed
4. **Package source code** (SAST/SCA only) using `fcli_fod_action_package`
5. **Upload and start scan** using appropriate `*_scan_start` command
6. **Monitor progress** using `*_scan_wait_for` or periodic `*_scan_get` calls

### Packaging Requirements
- **SAST scans**: Package source code with `fcli_fod_action_package`
- **SCA/OSS scans**: Package source code with `fcli_fod_action_package` (same as SAST)
- **DAST scans**: No packaging needed - scans live running application
- **MAST scans**: Upload mobile app binary (APK/IPA file)
- **Note**: To enable Open Source Analysis in a SAST scan, use `--oss` flag in `fcli_fod_sast_scan_setup`

### Filtering: Prefer --filters-param for Server-Side
- **Prefer `--filters-param`** for server-side filtering (fastest, smallest payloads)
- **Optionally use `query`** as a client-side post-filter when you need a simple match on returned fields
- Common filters: `severityString:Critical`, `severityString:High`, `category:SQL Injection`

### Pagination
- If `pagination.hasMore` = true → use `pagination-offset` for next page
- Continue until `pagination.hasMore` = false or `pagination.totalRecords` reached

## Error Recovery
| Error | Recovery |
|-------|----------|
| "Session expired" | Refer to flow in `Authentication` section |
| "Release not found" | Run `release_list` to discover correct names (see [Finding Releases](references/find-release.md)) |
| "Scan not configured" | Ask user for scan settings and run `*_scan_setup` |
| "Package required" | Run `fcli_fod_action_package` to package source code |

## Decision Tree: Choosing the Right Approach

| User Intent | Action |
|-------|----------|
| "run SAST scan" / "static analysis" | Check config → ask settings → package → `sast_scan_start` (see [SAST Workflow](references/run-sast-scan.md)) |
| "run SCA scan" / "open source scan" | Package → `oss_scan_start` (see [SCA Workflow](references/run-sca-scan.md)) |
| "run DAST scan" / "dynamic scan" | Check config → ask settings → `dast_scan_start` (see [DAST Workflow](references/run-dast-scan.md)) |
| "list/show vulnerabilities" | `issue_list` with `--filters-param` + `--embed details,recommendations` |
| "how many / count / summary" | `issue_list` and aggregate results client-side |
| "find release / which release" | `release_list` → `release_get` (see [Finding Releases](references/find-release.md)) |
| "show recommendations / how to fix" | `issue_list` with `--embed recommendations,history` → prioritize Aviator (see [Remediation](references/remediation-workflow.md)) |

## Best Practices
**DO:**
- ✅ Always verify authentication before operations
- ✅ Check scan configuration before starting SAST scans
- ✅ Always ask user for SAST scan settings (language, build tool, framework)
- ✅ Use `--oss` flag in `sast_scan_setup` to enable Open Source Analysis in SAST scans
- ✅ Use `--filters-param` for server-side filtering
- ✅ Use `--embed` to include details, recommendations, and history
- ✅ Prioritize Fortify Aviator code fix suggestions in remediation
- ✅ Use MCP tools over FCLI CLI directly
- ✅ Monitor long-running scans with `*_scan_wait_for`

**DO NOT:**
- ❌ Guess release names - always discover with `release_list` if uncertain
- ❌ Infer SAST scan settings from workspace - always ask user
- ❌ Skip SAST scan configuration validation
- ❌ Prompt user for credentials - ask user to run `fcli fod session login` locally
- ❌ Start scans without confirming settings with user
- ❌ Package source code for DAST scans (not needed)

## References
### Example Workflows
| Workflow | Use When User Says... |
|----------|----------------------|
| [Run SAST Scan](references/run-sast-scan.md) | "run SAST scan", "static analysis", "scan source code", "check for code vulnerabilities" |
| [Run SCA Scan](references/run-sca-scan.md) | "run SCA scan", "open source scan", "check dependencies", "OSS vulnerabilities", "software composition analysis" |
| [Run DAST Scan](references/run-dast-scan.md) | "run DAST scan", "dynamic scan", "test running application", "web application security test" |
| [List and Filter Vulnerabilities](references/list-filter-vulnerabilities.md) | "list vulnerabilities", "show security issues", "filter issues by severity", "critical vulnerabilities" |
| [Find Release](references/find-release.md) | "find release", "which release", "list releases", "search for application" |
| [Vulnerability Summary](references/vulnerability-summary.md) | "count vulnerabilities", "show summary", "breakdown by severity", "how many issues" |
| [Remediation Workflow](references/remediation-workflow.md) | "show recommendations", "how to fix", "remediation advice", "Aviator suggestions", "code fixes" |

### External Resources
- [FCLI Documentation](https://fortify.github.io/fcli/)
- [FoD Documentation](https://www.microfocus.com/documentation/fortify-on-demand/)
- [FoD User Guide](https://www.microfocus.com/documentation/fortify-on-demand/2410/FOD_Help_24.1.0/index.htm)
