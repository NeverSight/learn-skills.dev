---
name: fortify-scsast
description: ScanCentral SAST guide for MCP tools. Package source code, run SAST scans on ScanCentral sensors, monitor scan progress, and retrieve results from SSC.
metadata:
  version: "0.0.1"
---

# Fortify ScanCentral SAST Skill
Fortify ScanCentral SAST (SC-SAST) integration via Model Context Protocol (MCP). Enables distributed SAST scanning using ScanCentral sensors with results published to SSC.

## Available MCP Tools
Only key MCP tools for ScanCentral SAST are listed here.
| Tool | Description | When to Use |
|-----------|-------------|-------------|
| `fcli_ssc_action_package` | Package source code for scanning | Before starting a scan - creates scan package |
| `fcli_sc_sast_scan_start` | Start SAST scan on ScanCentral | After packaging - submits scan to sensor pool |
| `fcli_sc_sast_scan_status` | Check scan status | Monitor specific scan progress |
| `fcli_sc_sast_scan_wait_for` | Wait for scan completion | Block until scan reaches desired state |
| `fcli_sc_sast_scan_list` | List scans | View scan history, find scans by status |
| `fcli_sc_sast_scan_download` | Download scan artifacts | Retrieve FPR or logs after completion |
| `fcli_sc_sast_sensor_list` | List available sensors | Check sensor availability |
| `fcli_sc_sast_sensor_pool_list` | List sensor pools | Verify pool availability for scans |

## Parameter Formats
| Parameter | Format | Example |
|-----------|--------|---------|
| `scanJobToken` | UUID string (for scan_status) | `"550e8400-e29b-41d4-a716-446655440000"` |
| `scanJobTokens` | UUID string (for scan_wait_for) | `"550e8400-e29b-41d4-a716-446655440000"` |
| `appVersionNameOrId` | Application:Version (for appversion_get) | `"MyApp:1.0"` |
| `--appversion` | Application:Version (for issue_list) | `"MyApp:1.0"` |
| `--sc-client-version` | Version string or latest | `"latest"` (recommended - auto-matches sensors), `"25.4"`, `"26.1"` (explicit control) |
| `--sensor-version` | Version string (optional) | Omit for auto-match. Only use for explicit control: `"25.4"`, `"26.1"` |
| `--publish-to` | Application:Version | `"MyApp:1.0"`, `"WebApp:main"` |
| `--file` | File path (package file) | `"package.zip"`, `"./scans/app.zip"` |
| `--sensor-pool` | UUID string | `"550e8400-e29b-41d4-a716-446655440000"` |
| `--source-dir` | Directory path | `"."`, `"./src"` |
| `--output` | File path | `"package.zip"` |

## Authentication
ScanCentral SAST uses SSC authentication with an additional client auth token for sensor communication.

**Check session:**

**Tool:** `fcli_ssc_session_list`

**Parameters:**
```json
{
  "refresh-cache": true
}
```

**If session expired or missing:**
Ask user to run locally:
```bash
fcli ssc session login --url <SSC-URL> -u <username> -p <password> --sc-sast-url <SC-SAST-URL> --client-auth-token <TOKEN>
```

**Note:** The `--client-auth-token` is a ScanCentral-specific token obtained from SSC Administration → Settings → ScanCentral Client. This token is required for sensor communication.

## Filtering
Use client-side filtering with `query` JSON parameter:

**Filter by status:**
```json
{
  "query": {"status": "RUNNING"}
}
```

**Filter by application version:**
```json
{
  "query": {"publishToApplicationVersion": "MyApp:1.0"}
}
```

## Pagination
Handle large result sets using `pagination-offset` parameter:

**First page:**
```json
{
  "pagination-offset": 0
}
```

**Next page:**
```json
{
  "pagination-offset": 50
}
```

Continue with incremented offset until no more results.

## Error Recovery
| Error | Recovery |
|-------|----------|
| "Session expired" | Ask user to run `fcli ssc session login` locally with `--sc-sast-url` and `--client-auth-token` |
| "No sensors available" | Use `sensor_pool_list` to check pool availability, verify pool UUID |
| "Version mismatch" / scan won't start | Repackage with `--sc-client-version "latest"` and restart scan (omit `--sensor-version`). For explicit control, use `sensor_list` to find sensor versions and specify matching `--sc-client-version` and `--sensor-version`. |
| "Application version not found" | Use `fcli_ssc_appversion_get` to verify SSC target exists |
| "Package file not found" | Verify packaging step completed successfully, check file path |
| "Scan timeout" | Increase `--timeout` value in `scan_wait_for`, scans can take 30-60 minutes |

## Decision Tree: Choosing the Right Approach
| User Intent | Action |
|-------------|--------|
| "run SAST scan" | 1. Package (`action_package`) → 2. Start scan (`scan_start`) → 3. Wait (`scan_wait_for`) → 4. View issues (`fcli_ssc_issue_list`) |
| "package source code" | Use `action_package` with `--sc-client-version: "latest"`, `--source-dir`, `--output` |
| "check scan status" | Use `scan_status` with `scanJobToken` parameter |
| "list scans" | Use `scan_list` with optional `query` parameter |
| "list running scans" | Use `scan_list` with `query: {"status": "RUNNING"}` |
| "monitor scan" | Use `scan_wait_for` with `scanJobTokens` and `--until` parameters |
| "download scan results" | Use `scan_download` for FPR or view issues via `fcli_ssc_issue_list` |
| "check sensors" | Use `sensor_list` or `sensor_pool_list` |
| "view vulnerabilities" | After scan publishes: Use `fcli_ssc_issue_list` with `--appversion` parameter |

## Best Practices
**DO:**
- ✅ **Use `"latest"` for `sc-client-version`**: Preferred approach - automatically installs the most recent client version (e.g., 25.4.0) that matches current sensors
- ✅ **Omit `sensor-version` parameter**: When using modern clients (24.2+), ScanCentral auto-selects the matching sensor version
- ✅ **Optional explicit control**: Only use `sensor_list` to check versions if you need to manually specify both `sc-client-version` and `sensor-version`
- ✅ Validate SSC application version exists before starting scan
- ✅ Use `embed: "scSastScan"` in `scan_list` for detailed scan information
- ✅ Use `query` parameter for client-side filtering (e.g., `{"status": "RUNNING"}`)
- ✅ Set appropriate timeouts on `scan_wait_for` (scans typically take 15-60 minutes)
- ✅ Capture `scanJobToken` from `scan_start` response for monitoring
- ✅ Use `--publish-to` parameter to automatically publish results to SSC
- ✅ Check sensor pool availability before starting scans

**Do NOT:**
- ❌ Assume scans complete quickly - SAST scans can take significant time
- ❌ Mix `scanJobToken` and `scan-id` terminology (use `scanJobToken` consistently)
- ❌ Forget `--publish-to` parameter - results won't appear in SSC without it
- ❌ Try to retrieve scan results before scan reaches COMPLETED state
- ❌ **Use `sc-client-version: "auto"`** - it uses older hardcoded defaults (e.g., 24.4.0) that may not match current sensors, causing scan failures. Always use `"latest"` instead.
- ❌ Specify `sensor-version` unnecessarily - omit it for auto-matching (recommended for modern clients 24.2+)
- ❌ Skip authentication verification - sensor operations require valid SSC session

## References
### Example Workflows
| Workflow | Use When User Says... |
|----------|----------------------|
| [Run SAST Scan](references/run-sast-scan.md) | "run SAST scan", "scan my code", "package and scan", "start scan", "upload for scanning", "SAST analysis" |
| [List and Monitor Scans](references/list-monitor-scans.md) | "list scans", "scan history", "check scan status", "monitor scan", "scan progress", "running scans" |

### External Resources
- [FCLI Documentation](https://fortify.github.io/fcli/)
- [SCSAST User Guide](https://www.microfocus.com/documentation/fortify-software-security-center/2540/sc-sast-ugd-html-25.4.0/index.html#/home)
