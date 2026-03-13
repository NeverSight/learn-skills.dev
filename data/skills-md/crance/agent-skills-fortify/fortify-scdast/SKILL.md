---
name: fortify-scdast
description: ScanCentral DAST guide for MCP tools. Run dynamic application security testing (DAST) scans, list and filter scan results, discover scan settings and policies, and manage web application security scanning using Fortify ScanCentral DAST. Triggers include any mention of 'SC-DAST', 'ScanCentral DAST', 'DAST scan', 'web scan', 'dynamic scan', 'run DAST scan', 'list scans', and similar requests indicating interaction with SC-DAST for dynamic application security scanning.
metadata:
  version: "0.0.1"
---

# Fortify ScanCentral DAST Skill
Fortify ScanCentral DAST (SC-DAST) integration via Model Context Protocol (MCP).

## When to Use This Skill
- Run dynamic application security testing (DAST) scans
- List and monitor scan status
- Pause/resume running scans
- Discover available scan settings and policies
- Manage scan sensors and sensor pools
- View scan results in SSC using SSC skill

## Available MCP Tools
Only key MCP tools for SC-DAST are listed here.

| Tool | Description | When to Use |
|------|-------------|-------------|
| `fcli_sc_dast_scan_start` | Start a new DAST scan | When user wants to run/start a DAST scan |
| `fcli_sc_dast_scan_list` | List all scans | List scans, check scan status |
| `fcli_sc_dast_scan_get` | Get details of a specific scan | Get scan details by ID |
| `fcli_sc_dast_scan_wait_for` | Wait for scan condition | Monitor scan until condition met |
| `fcli_sc_dast_scan_pause` | Pause a running scan | Temporarily stop a scan |
| `fcli_sc_dast_scan_resume` | Resume a paused scan | Continue a paused scan |
| `fcli_sc_dast_scan_settings_list` | List available scan settings | Discover scan configuration options |
| `fcli_sc_dast_scan_settings_get` | Get scan settings details | Get specific settings by ID or CICD token |
| `fcli_sc_dast_scan_policy_list` | List available scan policies | Discover scan policy options |
| `fcli_sc_dast_scan_policy_get` | Get scan policy details | Get specific policy by name or ID |
| `fcli_sc_dast_sensor_list` | List available sensors | View available scan sensors |
| `fcli_sc_dast_sensor_get` | Get sensor details | View specific sensor information |
| `fcli_sc_dast_sensor_enable` | Enable a sensor | Enable a disabled sensor |
| `fcli_sc_dast_mcp_job` | Background job handler | Handle pagination and background tasks |
| `fcli_ssc_session_list` | Check SSC session status | Verify authentication before operations |

## Parameter Formats

| Parameter | Format | Example |
|-----------|--------|---------|
| `--settings` | CICD token or ID | `"MY_SCAN_SETTINGS"` or `"12345"` |
| `--name` | Scan name | `"MyApp Security Scan"` |
| `--policy` | Policy name or ID | `"Standard"` or `"67890"` |
| `--overwrite-scan-mode` | Boolean flag | `true` (mutually exclusive with priority-scan-mode) |
| `--priority-scan-mode` | Boolean flag | `true` (mutually exclusive with overwrite-scan-mode) |
| `--login-macro` | Login macro ID | `"98765"` (optional) |
| `--server-queries` | Key-value filtering | `"status=Running"` or `"name~MyApp"` |
| `--until` | Wait condition | `"status=Complete"` or `"status=Failed"` |
| `--while` | Wait condition (inverse) | `"status=Running"` |
| `scanIds` | Scan identifier(s) | Single or multiple scan IDs from list/get operations |
| `query` | Client-side filtering (SpEL) | `"status == 'Complete' && scanVersion > 5"` |

## Authentication

SC-DAST uses SSC authentication (simplest authentication model - no additional tokens required).

**Session Check:**
Always check SSC session status before SC-DAST operations:
```
Tool: fcli_ssc_session_list
Parameters: { "refresh-cache": true }
```

**If session expired or missing:**  
Ask the user to run this command locally in their terminal:
```bash
fcli ssc session login --url <SSC_URL> -u <username> -p <password>
```

**Default Session:**  
If the user doesn't specify a session name, inform them that the `default` session will be used.

## Domain-Specific Guidance: Scan Workflow

SC-DAST scans follow a straightforward workflow:

### Phase 1: Discovery
- List available scan settings: `scan_settings_list`
- List available scan policies: `scan_policy_list`
- Get specific settings/policy details if needed

### Phase 2: Start Scan
Start scan with required parameters:
- `--settings` (CICD token or ID) - **REQUIRED**
- `--name` (scan name) - **REQUIRED**
- `--policy` (policy name or ID) - *optional*
- `--overwrite-scan-mode` or `--priority-scan-mode` (boolean flags, mutually exclusive) - *optional*
- `--login-macro` (login macro ID) - *optional*

**Important:** Ensure scan settings are configured to automatically publish results to SSC. This is typically configured in the scan settings by the administrator.

### Phase 3: Monitor Progress
- Use `scan_wait_for` with `--until: "status=Complete"` or `--while: "status=Running"`
- Use `scan_list` with `--server-queries: "status=Running"` to check all running scans
- **Unique capability:** Use `scan_pause` and `scan_resume` to control scan execution

### Phase 4: View Results
- Once scan completes, findings automatically appear in SSC (if configured)
- View findings in SSC using SSC skill (fcli_ssc_issue_list, fcli_ssc_issue_count, etc.)

## Filtering

SC-DAST supports both server-side and client-side filtering:

**Server-Side Filtering (Preferred):**
Use `--server-queries` parameter with key-value pairs:
- Single filter: `"status=Running"`
- Contains match: `"name~MyApp"`
- Multiple filters: `"status=Complete,name~Security"`

**Client-Side Filtering:**
Use `query` parameter for complex filtering with SpEL (Spring Expression Language):
```
query: "status == 'Complete' && scanVersion > 5"
```

**When to use each:**
- **Server-side (`--server-queries`):** Preferred for performance, especially with large datasets
- **Client-side (`query`):** Use for complex expressions not supported by server-side filtering

## Pagination

SC-DAST uses job_token-based pagination (same pattern as SSC):

**When pagination.totalRecords is null:**
1. Call `fcli_sc_dast_mcp_job`:
   ```
   Parameters: {
     "operation": "wait",
     "job_token": "<job_token from previous response>"
   }
   ```

2. After job completes, retry the original list call to get results.

**Example Flow:**
```
1. Call scan_list → Response has totalRecords: null, job_token: "abc123..."
2. Call mcp_job with operation: "wait", job_token: "abc123..."
3. Retry scan_list → Response now has full results with totalRecords populated
```

## Error Recovery

| Error | Recovery |
|-------|----------|
| "Session expired" | Ask user to run `fcli ssc session login` locally |
| "Scan settings not found" | Use `scan_settings_list` to discover available settings |
| "Policy not found" | Use `scan_policy_list` to discover available policies |
| "Scan cannot be completed" | Check scan status - may still be running or failed |
| "No sensors available" | Use `sensor_list` to check available sensors |
| "Import failed" | Ensure scan was completed and published first |
| Pagination `totalRecords: null` | Use `mcp_job` with `operation: "wait"` and `job_token` |

## Decision Tree: Choosing the Right Approach

| User Intent | Action |
|-------------|--------|
| "Run a DAST scan" | Discovery workflow: `scan_settings_list` → `scan_policy_list` → `scan_start` → `scan_wait_for` → view results in SSC |
| "List scans" / "Show my scans" | `scan_list` with optional `--server-queries` filtering |
| "Check scan status" | `scan_get` with scan ID OR `scan_list` with `--server-queries: "name~<scan-name>"` |
| "Pause a scan" | `scan_pause` with scan ID |
| "Resume a scan" | `scan_resume` with scan ID |
| "View scan results" | Use SSC skill: `fcli_ssc_issue_list` or `fcli_ssc_issue_count` |
| "Find scan settings" | `scan_settings_list` optionally with `server-queries` |
| "Check sensors" | `sensor_list` to view available sensors |

## Best Practices

**DO:**
- ✅ Always check SSC session status before SC-DAST operations
- ✅ Use discovery workflow (list settings/policies) before starting scans
- ✅ Use server-side filtering (`--server-queries`) for performance
- ✅ Ensure scan settings are configured to auto-publish to SSC
- ✅ Use `scan_wait_for` with appropriate timeouts for long-running scans (typically 30min-2hrs)
- ✅ Leverage pause/resume capability for scan management
- ✅ Use CICD token for scan settings in automation scenarios
- ✅ Handle pagination with job_token pattern when totalRecords is null
- ✅ View results in SSC using SSC skill after scan completes

**DO NOT:**
- ❌ Start scans without verifying settings/policy existence
- ❌ Use client-side filtering for large datasets (prefer `--server-queries`)
- ❌ Poll scan status manually - use `scan_wait_for` instead
- ❌ Forget to verify scan settings are configured to publish to SSC
- ❌ Ignore pagination when totalRecords is null

## References

### Example Workflows
| Workflow | Use When User Says... |
|----------|----------------------|
| [Run DAST Scan](references/run-dast-scan.md) | "run scan", "start DAST scan", "web scan", "scan my application", "dynamic scan" |
| [List and Monitor Scans](references/list-monitor-scans.md) | "list scans", "monitor progress", "check status", "pause scan", "resume scan" |
| [Discover Scan Settings and Policies](references/discover-scan-settings-policies.md) | "scan settings", "scan policy", "configuration", "CICD token", "available settings" |

### External Resources
- [FCLI Documentation](https://fortify.github.io/fcli/)
- [SC-DAST User Guide](https://www.microfocus.com/documentation/fortify-scancentral-dast/)
