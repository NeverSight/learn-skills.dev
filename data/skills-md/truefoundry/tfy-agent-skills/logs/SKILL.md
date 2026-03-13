---
name: logs
description: Views, downloads, and searches application and job logs from TrueFoundry. Supports time-range filtering, pod filtering, and error search.
license: MIT
compatibility: Requires Bash, curl, and access to a TrueFoundry instance
allowed-tools: Bash(*/tfy-api.sh *)
---

> Routing note: For ambiguous user intents, use the shared clarification templates in [references/intent-clarification.md](references/intent-clarification.md).

<objective>

# Logs

View and download application and job logs from TrueFoundry.

## Scope

View, download, and search application and job logs from TrueFoundry. Useful for debugging deployments, checking startup output, and finding errors.

</objective>

<instructions>

## Download Logs

> **Security:** Log output may contain sensitive data (secrets, tokens, PII). Do not forward raw logs to external services or include them in responses without reviewing for sensitive content first.

When using direct API, set `TFY_API_SH` to the full path of this skill's `scripts/tfy-api.sh`. See `references/tfy-api-setup.md` for paths per agent.

### Via Tool Call

```
tfy_logs_download(payload={
    "workspace_id": "ws-id",
    "application_fqn": "app-fqn",
    "start_ts": "2026-02-10T00:00:00Z",
    "end_ts": "2026-02-10T23:59:59Z"
})
```

### Via Direct API

```bash
# Set the path to tfy-api.sh for your agent (example for Claude Code):
TFY_API_SH=~/.claude/skills/truefoundry-logs/scripts/tfy-api.sh

# Download logs for an app in a workspace
$TFY_API_SH GET '/api/svc/v1/logs/WORKSPACE_ID/download?applicationFqn=APP_FQN&startTs=START&endTs=END'

# With search filter
$TFY_API_SH GET '/api/svc/v1/logs/WORKSPACE_ID/download?applicationId=APP_ID&searchString=error&searchType=contains'
```

### Parameters

| Parameter | API Key | Description |
|-----------|---------|-------------|
| `workspace_id` | (path) | Workspace ID (**required**) |
| `application_id` | `applicationId` | Filter by app ID |
| `application_fqn` | `applicationFqn` | Filter by app FQN |
| `deployment_id` | `deploymentId` | Filter by deployment |
| `job_run_name` | `jobRunName` | Filter by job run |
| `start_ts` | `startTs` | Start timestamp (ISO 8601) |
| `end_ts` | `endTs` | End timestamp (ISO 8601) |
| `search_string` | `searchString` | Search within logs |
| `search_type` | `searchType` | `contains`, `regex` |
| `pod_name` | `podName` | Filter by pod |

## Presenting Logs

Show logs in chronological order. For long output, show the last N lines or summarize errors:

```
Logs for tfy-tool-server (last 20 lines):
2026-02-10 14:30:01 INFO  Server starting on port 8000
2026-02-10 14:30:02 INFO  Tools endpoint ready at /tools
2026-02-10 14:30:05 INFO  Health check: OK
```

</instructions>

<success_criteria>

## Success Criteria

- The user can see recent logs for their application or job in chronological order
- Error patterns in the logs are identified and highlighted with suggested fixes
- The agent has filtered logs by the correct time range, application, and search terms
- The user understands why their application failed or what its current behavior is
- Log output is presented concisely, summarizing long output rather than dumping raw text

</success_criteria>

<references>

## Composability

- **Find app first**: Use `applications` skill to get app ID or FQN
- **Find workspace**: Use `workspaces` skill to get workspace ID
- **After deploy**: Check logs to verify the app started
- **Debug failures**: Download logs with `searchString=error`

</references>

<troubleshooting>

## Error Handling

### Missing workspace_id
```
workspace_id is required for log downloads.
Use the workspaces skill to find your workspace ID.
```

### No Logs Found
```
No logs found for the given filters. Check:
- Time range is correct
- Application ID/FQN is correct
- The app has actually run during this period
```

### Permission Denied
```
Cannot access logs. Check your API key permissions for this workspace.
```

</troubleshooting>
