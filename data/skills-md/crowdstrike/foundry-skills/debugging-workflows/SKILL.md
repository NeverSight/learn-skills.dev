---
name: debugging-workflows
description: Systematic troubleshooting for Falcon Foundry CLI errors, manifest validation failures, deploy failures, artifact runtime errors, and development server issues. TRIGGER when user encounters CLI errors, `foundry ui run` not working, deploy failures, authentication issues, function execution failures, "debug my function", "why did this fail", or any unexpected behavior during Foundry app development. Also trigger for headless/CI environment setup failures.
version: 1.6.0
updated: 2026-10-01
tags: [foundry, debugging, cli, deployment, artifacts, functions, logs, execution]
author: CrowdStrike
license: MIT
compatibility: Claude Code >=1.0
metadata:
  category: troubleshooting
---

# Foundry Debugging Workflows

Systematic procedures for diagnosing and resolving common CrowdStrike Falcon Foundry development issues.

> **Part of a suite.** If `development-workflow` has not already run, and this is a new app or its first capability, load the `development-workflow` skill first — it owns the CLI prerequisite check, scaffolding order, and manifest coordination.

## Quick Diagnosis

```
What's happening?

CLI command hangs
├── In headless/CI environment → Missing --no-prompt or required flags (see Headless section)
└── In interactive terminal   → Check network/auth with foundry profile active

Deploy fails
├── Validation error → Check manifest YAML syntax, then deploy again
├── "Unknown error"  → Duplicate workflow name across apps in tenant
├── "no deployable artifacts found" → Diff is only manifest/logo/metadata; deploy needs an artifact change (function/collection/UI/agent). No --force; bundle it or put the logo in the first deploy
├── "Failed" with no reason in the CLI → Falcon console: App manager > app > "Show errors (N)" (per capability)
├── validate says "deployment is currently in progress" → A deploy is still running; poll list-deployments, then retry
└── Silent failure   → Tenant may be missing required module (SKU) for requested scopes

foundry ui run fails
├── On new app              → Deploy backend capabilities first (API integrations, functions, collections resolve from cloud)
├── Permission errors       → Check manifest OAuth scopes, restart server, verify auth
└── Blank page / CORS error → noAttr() or base path removed from vite.config.js (see ui-development)

Function execution fails
├── Status 500 + "Server Error"  → Check function logs: foundry functions logs <exec_id>
├── Status 202 + no result       → Async execution: foundry functions exec status <exec_id>
├── 403 "app is not installed"   → Deployed but not released + installed from App Catalog; FalconPy calls need an installed app
├── 401 on every FalconPy call, scopes correct → Client constructed at module scope; move it inside the handler
├── "authorization failed"       → Confirm the CLI profile's API client has Apps read + write; if it does, it's a platform permission problem: report the trace ID, don't edit scopes
├── "artifact is not deployed"   → Deploy first: foundry apps deploy --no-prompt
├── No logs available            → Wait 5-10 min, then: foundry functions logs <exec_id> --refresh
│   └── Still "Log query failed"   → Temporarily return the diagnostic values in the handler's response body, redeploy, exec once, then remove them
├── UI page: repeated 404s on /api2/faas-gateway/entities/execution/v1 in the browser console → foundry-js polling for the cloud-function result before it is ready; non-fatal if the data still loads, not a failure
└── Unexpected response          → Read logs + source, correlate timestamps against handler code

Auth fails
├── 401/403 from API   → Check OAuth scopes in manifest
├── Login hangs        → Headless environment, no browser — use env vars or profile create --no-prompt
└── Works locally, fails in CI → Set FOUNDRY_API_CLIENT_ID env vars in CI config
```

## Local Testing

### Function Testing

```bash
# Via Foundry CLI with Docker (random ports, closest to production)
foundry functions run --name my-function

# Direct Go execution (port 8081, no Docker)
cd functions/my-function && go run main.go

# Direct Python execution (port 8081, no Docker)
cd functions/my-function && python3 main.py
curl -X POST http://localhost:8081/api/process -d '{"key":"value"}'

# With configuration file (local only)
CS_FN_CONFIG_PATH=./config.json python3 main.py
```

### Function Execution & Log Retrieval (Deployed Functions)

> **Requires Foundry CLI 2.1.0+.** These commands do not exist in CLI 2.0.x.

For testing against the deployed Lambda (not local Docker), use the execution commands:

```bash
# Execute a deployed function handler
foundry functions exec --handler my_handler '{"key": "value"}' --no-prompt

# Execute and wait for logs
foundry functions exec --handler my_handler --logs '{"payload": "data"}' --no-prompt

# Check status of an async (202) execution
foundry functions exec status <exec_id>

# Retrieve logs for a past execution
foundry functions logs <exec_id>

# List recent executions to find one to debug
foundry functions exec list --function my-fn --no-prompt
```

### Function Runtime Debugging

When a deployed function returns unexpected results or errors:

**Step 1: Execute and observe**
```bash
foundry functions exec --handler <handler> --logs '{"test": "input"}' --no-prompt
```

Note the exec_id and status code from the output.

**Step 2: Retrieve logs if not already displayed**
```bash
foundry functions logs <exec_id>
```

Logs arrive 5-10 minutes after execution via the Firehose pipeline. The CLI polls automatically with a countdown.

**Step 3: Correlate logs against source**

The function source lives at the path in `manifest.yml`:
```yaml
functions:
  - name: my-function
    path: functions/my-function
    handlers:
      - name: my_handler
        method: POST
        api_path: /api/process
```

Read the handler source and compare against log timestamps and error messages.

**Step 4: Common runtime failures**

| Log Pattern | Likely Cause | Fix |
|-------------|-------------|-----|
| `ImportError: No module named X` | Missing from `requirements.txt` | Add dependency, redeploy |
| `KeyError: 'field'` | Missing field in request body | Add input validation |
| `401 Unauthorized` from FalconPy | Missing OAuth scope in manifest | Add scope, redeploy |
| `401 Unauthorized` on every call, scopes correct | FalconPy client constructed at module scope (no request token at import) | Construct the client inside the handler |
| `403` with `app is not installed` | App deployed but not released and installed | `foundry apps release`, then install from the App Catalog |
| `Timeout` / no logs appear | Function exceeded `max_exec_duration_seconds` | Increase timeout or optimize |
| Status 202, no result | Async execution | Poll: `foundry functions exec status <exec_id>` |
| Logs say "available" but empty | Logs not yet in pipeline | Wait 5-10 min or use `--refresh` |

**Step 5: Fix, redeploy, verify**
```bash
# After fixing the code:
foundry apps deploy --change-type Patch --change-log "fix handler error" --no-prompt

# Re-execute to verify
foundry functions exec --handler <handler> --logs '{"test": "input"}' --no-prompt
```

### RTR Script Testing

RTR scripts can only be tested via the CLI (not the Falcon console):

```bash
foundry rtr-scripts run --name my-script
```

Platforms: Windows (`script.ps1`), Linux (`script.sh`), macOS (`script.zsh`). Script size limit ~40KB. Deletion requires Falcon Administrator role in Falcon console UI.

### Workflow Mock Testing

```bash
foundry workflows triggers view --mock
foundry workflows actions view --mock
foundry workflows executions validate --mocks mymocks.json
foundry workflows executions start --definition my-workflow --mocks mymocks.json
foundry workflows executions view <execution_id>
```

### Deployment Diagnostics

Deployment is two-phase: validation (checks manifest and schemas) then artifact build. Use `foundry apps validate --no-prompt` to dry-run the validation phase after adding API integrations or collections (catches spec/schema issues in seconds). Don't validate right before deploy — deploy runs the same validation plus workflow semantics and name uniqueness checks.

## CLI Troubleshooting

### Step 1: Environment Validation

```bash
foundry version         # Check CLI version
foundry profile list    # Check available profiles
foundry profile active  # Verify active profile
```

### Step 2: Authentication

```bash
foundry login                                    # Re-authenticate via browser (interactive)
foundry profile delete --name <name> --no-prompt # Reset corrupted profile
foundry login                                    # Re-authenticate
```

### `connection issue` on Tenant Commands (Sandboxed Agents)

**Check the token cache write first — it is the usual cause and it is not a network problem.**

The CLI keeps its short-lived access token in `~/.config/foundry/token.json`, separate from the credentials in `configuration.yml`. The token lasts about 30 minutes, and the next tenant command after it expires writes a fresh one back to that file. That write is expected and is the safer design: a rotating 30-minute token beats a long-lived one, and keeping it out of the workspace means it never gets committed.

Assistants that confine writes to the workspace are denied that write, and the CLI reports only `connection issue` — the symptom, not the cause. Since a session usually begins with an already-expired token, this appears within the first few seconds, not after half an hour.

Fix: **request write access to `~/.config/foundry/` and retry the same command.** Say why — the CLI is refreshing its own token cache — and treat it as a routine low-risk escalation rather than a blocker. Do not ask the user to relaunch their assistant, and do not rewrite the profile, redirect the config path into the workspace, or copy credentials; those hide working credentials instead of granting the one needed write.

If the write succeeds and tenant commands still fail, then treat it as network: ask the user to run the command in their own terminal, and if it works there, request unsandboxed network access and retry once.

### Manifest Validation

Use `foundry apps validate --no-prompt` to validate the manifest and schemas without deploying. For OpenAPI specs, use `npx @redocly/cli lint` to validate structure locally.

If deploy fails with validation errors:
1. Check the error message — validation errors appear first
2. Comment out capabilities one by one to isolate the issue
3. Fix and re-validate incrementally

## Headless / Non-Interactive Environments

This is the most common failure mode when Foundry CLI is driven by agents (Claude Code) or CI/CD pipelines. Most commands default to interactive mode, which blocks indefinitely.

### `foundry login` Hangs or Fails

`foundry login` opens a browser for OAuth. In headless environments, use one of these alternatives:

**Option 1: Environment variables** (no login needed):
```bash
export FOUNDRY_API_CLIENT_ID="<client-id>"
export FOUNDRY_API_CLIENT_SECRET="<client-secret>"
export FOUNDRY_CID="<customer-id>"
export FOUNDRY_CLOUD_REGION="us-1"
```

**Option 2: Non-interactive profile creation**:
```bash
foundry profile create \
  --name "ci-profile" \
  --api-client-id "<id>" \
  --api-client-secret "<secret>" \
  --cid "<cid>" \
  --cloud-region "us-1" \
  --no-prompt
foundry profile activate --name "ci-profile"
```

**Option 3: Pre-populated config file** at `~/.config/foundry/configuration.yml`:
```yaml
profiles:
- name: ci-profile
  cloud_region: us-1
  credentials:
    cid: <customer-id>
    api_client_id: <client-id>
    api_client_secret: <client-secret>
active_profile: ci-profile
```

### Command Hangs Waiting for Input

Add `--no-prompt` to prevent interactive prompts. Nearly all commands support it: `apps create`, `apps validate`, `apps deploy`, `apps release`, `apps delete` (also needs `--force-delete`), `functions create`, `collections create`, `ui pages create`, `ui extensions create`, `rtr-scripts create`, `profile create`, `profile delete`, `workflows create`, and `api-integrations create`. Provide all required flags explicitly — run `foundry <command> --help` to identify them.

### Auth Works Locally but Fails in CI

The CI environment has no `~/.config/foundry/configuration.yml`. Set environment variables in CI pipeline configuration — they override local config.

## Common Issue Patterns

| Symptom | Likely Cause | First Action |
|---------|--------------|--------------|
| `foundry login` hangs | Headless environment | Use env vars or `profile create --no-prompt` |
| Any command hangs | Missing `--no-prompt` or required flags | Add flags, run `--help` |
| Deploy hangs indefinitely | Manifest validation issue | Check YAML syntax, deploy again |
| `foundry ui run` fails on new app | Backend not deployed | Run `foundry apps deploy` first |
| API calls return 403 | Insufficient OAuth scopes | Review manifest oauth section |
| Deploy fails silently | Tenant missing required module (SKU) | Verify tenant has Falcon module for scopes |
| Deployment `Failed`, CLI gives no reason | Reasons are console-only | App manager > app > "Show errors (N)" |
| `deployment is currently in progress` from `validate` | A deploy is still running | Poll `foundry apps list-deployments` until it settles, then retry |
| Local server won't start | Port conflicts | Use `--port` flag or kill existing processes |
| Auth works locally, fails in CI | No config file in CI | Set `FOUNDRY_API_CLIENT_ID` env vars |
| `connection issue` in a sandboxed agent | Denied write to the CLI's token cache | Grant write to `~/.config/foundry/`; the token refresh is expected |
| Tenant command works for user, not agent | Agent network sandbox | Request elevation, then retry once |
| Page 404 after deploy/release | App not installed from App Catalog | Install from catalog, wait for propagation |
| Page 404 on new cloud only | Cloud-specific IDs in manifest | Strip IDs with yq before deploying to new cloud |
| Blank page, no CORS errors | Vite `root` changed from `src` | Restore `root: 'src'` in vite.config.js |
| Blank page with CORS errors | `noAttr()` removed from vite.config.js | Restore the `noAttr()` plugin in vite.config.js |
| Blank page, no errors in console | `falcon.connect()` not awaited | The platform iframe stays blank until the postMessage handshake completes — add `await falcon.connect()` before any rendering |
| Data not appearing after writes | Schema mismatch or missing error check | Verify field names/enums match schema exactly; check `result?.errors?.length` after writes |
| Dialog white background in dark mode | Shoelace panel defaults | Override `--sl-panel-background-color` with `var(--ground-floor)` |
| App install fails with no detail | Workflow CEL expression error | Test API integration in console, then inspect workflow editor for errors |

## Debugging App Install Failures

When a Foundry app fails to install with no useful error message, isolate the problem by testing each component in the Falcon console:

1. **Test the API integration first** — In the Falcon console, use the credentials from the install config to test the operation directly (e.g., run `listUsers` with the Okta domain and API key). This proves whether the spec and credentials work independently of the app.

2. **Eliminate unlikely suspects** — Static UI files (extensions, pages) don't cause install failures. If the API integration works, the problem is almost certainly in a workflow.

3. **Inspect the workflow in the console** — Open Falcon Fusion SOAR, edit the workflow, and look at each action's configuration. The workflow editor shows validation errors (like unknown variable references in CEL expressions) that the install API doesn't surface.

> **Example:** Apps failed to install with no detail. API integration tested fine. Editing the workflow in the console revealed "unknown variable" on the Print data action — the CEL variable path was missing the `Custom_` prefix the platform adds to all API integration names. The install error gave no hint; the workflow editor showed it immediately.

## Visual Debugging with Screenshots

Claude Code can read images directly. When the Falcon console shows something unexpected — a blank page, an error modal, a disabled button — a screenshot is often the fastest way to diagnose the issue.

**Without Playwright MCP (fastest):** Ask the user to take a screenshot of what they're seeing and paste or drag it into the conversation. Claude reads it immediately and can identify error messages, missing elements, wrong page states, or styling issues without any setup.

**With Playwright MCP:** If Playwright MCP is configured (`claude mcp add playwright -- npx @playwright/mcp@latest`), Claude can take screenshots directly via `browser_take_screenshot`. This is useful for interactive debugging sessions. See `e2e-testing/references/debugging-with-mcp.md` for details.

**From test failure artifacts:** When e2e tests fail, Playwright saves screenshots to `test-results/`. Read the `.png` file directly — it shows the exact page state at the moment of failure.

Screenshots are particularly effective for:
- Blank pages after deploy (missing iframe, broken Vite config)
- Extension buttons that don't appear or expand
- Error banners or modals with messages not surfaced by the CLI
- `foundry ui run` rendering issues (dark mode, missing Shoelace styles)
- App install dialogs with unexpected form fields

## Recovery Strategies

### Profile Corruption
1. Delete corrupted profile: `foundry profile delete --name <name> --no-prompt`
2. Re-authenticate with `foundry login`
3. Validate with test deployment

### Development Server
1. Kill existing processes: `pkill -f "foundry ui"`
2. Clear node_modules and reinstall
3. Restart with clean environment

### Manifest Issues
Don't restore `manifest.yml` from git (`git checkout manifest.yml`) after a deploy. The deploy writes `app_id` and artifact IDs back into the file, and discarding them breaks the link to the deployed app: `exec`/`test` fail with `app_id not found in manifest`, and the next deploy fails with `an app with the provided name already exists`. In testing, putting back only `app_id` wasn't enough (`exec` then reported `artifact is not deployed` and later deploys failed); deleting the app (`foundry apps delete --force-delete --no-prompt`) and deploying fresh worked. Commit or discard the deploy-written IDs deliberately instead.

1. Backup current `manifest.yml`
2. Start with minimal working manifest
3. Incrementally add capabilities back, deploying after each addition

## Pre-Escalation Checklist

Before seeking external help:

- [ ] Verified CLI version with `foundry version`
- [ ] Checked authentication with `foundry profile active`
- [ ] Validated OpenAPI specs with `npx @redocly/cli lint` (if applicable)
- [ ] Tested with minimal configuration
- [ ] Reviewed CLI error messages
- [ ] Attempted recovery procedures
- [ ] Documented reproduction steps
