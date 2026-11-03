---
name: dt-obs-extensions
description: >-
  Dynatrace extension status checks and troubleshooting. Use when checking extension monitoring
  configuration status, diagnosing extension errors, or interpreting extension error codes.
  Trigger: "extension status", "extension not working", "extension error", "monitoring configuration
  status", "EEC error", "extension troubleshooting", "DEC error code", "extension startup failed",
  "high memory extension", "extension verification error".
  Do NOT use for explaining existing queries, product documentation questions,
  or OneAgent/ActiveGate installation issues unrelated to extensions.
license: Apache-2.0
---

# Dynatrace Extensions Skill

## Overview

Dynatrace extensions allow you to extend the functionality of Dynatrace by integrating with external systems and custom data sources. 

**When to use this skill:**

- Checking the status of installed extensions and their monitoring configurations
- Troubleshooting extension configuration issues using DQL queries and event logs

## Extensions lifecycle
Extensions are first installed, which brings assets (dashboards, alert templates, OpenPipeline rules etc). Once installed, each extension can have multiple activation - Monitoring Configurations. Configurations can run on ActiveGate or OneAgent, and can be enabled/disabled independently. Each configuration has its own status, which can be queried using this skill.

## Extensions Monitoring Configurations and Statuses

### Extensions Statuses

To check the status of an extension, you can run following DQL query:

```dql
timeseries count(dt.sfm.extension.config.status), by: {dt.extension.name, dt.extension.config.id, dt.extension.status}
```

- `dt.extension.name` — extension name
- `dt.extension.config.id` — monitoring configuration ID
- `dt.extension.status` — current status value

### 2. Retrieve Extension Event Logs

If a status is not `OK`, get detailed logs:

```dql
fetch dt.system.events
| filter dt.extension.name == "<extension_name>" AND dt.extension.config.id == "<config_id>"
```

Look for error codes in the `content` field. Error codes have the format `DEC:[A-Z0-9_]+`.

→ For error code meanings and remediation, search `references/extensions-error-codes.md` for the exact code (see [Error Code Reference](#error-code-reference)).

---

## Extension Status Reference

| Status | Meaning | Remediation |
|--------|---------|-------------|
| `OK` | Running without issues | None |
| `STARTUP` / `STARTUP_PENDING` / `STARTUP_SCHEDULED` | Extension is starting | Wait for startup to complete |
| `RESTART` / `TIMED_OUT_RESTART` | Extension restarting | Monitor; if recurring, check logs |
| `IDLE` | Working but no status produced | Usually transient |
| `WARNING` | Warning state | Check extension logs |
| `GENERIC_ERROR` | Error state | Check extension logs |
| `STARTUP_ERROR` | Error during startup | Check extension logs and configuration |
| `HIGH_CPU` / `HIGH_CPU_RESTART` | Excessive CPU usage | Switch Performance Profile in ActiveGate settings |
| `HIGH_MEMORY` / `HIGH_MEMORY_RESTART` | Excessive memory usage | Switch Performance Profile in ActiveGate settings |
| `EEC_HARD_LIMIT_REJECTION` / `EEC_HARD_LIMIT_RESTART` | Resource hard limit hit | Switch Performance Profile in ActiveGate settings |
| `EEC_RESTSERVER_ERROR` | REST API port conflict | Check for port conflicts on the host |
| `EXTENSIONS_CACHE_ERROR` | Cannot download extension | Check disk space on ActiveGate/OneAgent |
| `EXTENSION_VERIFICATION_ERROR` | Malformed extension.yaml | Validate extension.yaml syntax |
| `CUSTOM_CODE_EXTENSION_NOT_ALLOWED` | Custom code blocked | Update ActiveGate or OneAgent |
| `INCOMPATIBLE_API_ERROR` | API version mismatch | Update ActiveGate/OneAgent or check extension docs |
| `MAX_TASKS_LIMIT_REJECTION` | Too many tasks | Add ActiveGates to the group or split groups |
| `MISSING_BINARY` / `MISSING_DATASOURCE` | Malformed installation | Reinstall ActiveGate or OneAgent |
| `GROUP_NAME_CHANGE` | Temporary rebalancing | Wait for rebalancing to complete |

---

## Troubleshooting

### Common Issues

1. **Extension shows non-OK status**
   - Run the status query above to identify the specific status code
   - Check the status reference table for remediation
   - If unclear, fetch event logs for the extension

2. **Error codes in event logs**
   - Error codes follow the pattern `DEC:[A-Z0-9_]+`
   - Search for the code in `references/extensions-error-codes.md` (see [Error Code Reference](#error-code-reference) below)
   - If no error code is present, read the event `content` for details

3. **Extension keeps restarting**
   - Check for `HIGH_CPU_RESTART`, `HIGH_MEMORY_RESTART`, or `TIMED_OUT_RESTART`
   - Switch to a higher Performance Profile in ActiveGate settings
   - Review extension configuration for excessive scope

4. **Extension not producing data**
   - Verify status is `OK` (not `IDLE` or error state)
   - Check that the monitoring configuration is enabled
   - Verify network connectivity to the monitored system

---

## Error Code Reference

`references/extensions-error-codes.md` is a large generated file. Each entry follows this structure:

```
## Error Code DEC:<code>

### Error Description: <description>

### Suggestions:

1. ...
```

**Do not load the full file.** Search for the specific error code heading (e.g. `## Error Code DEC:1D6`) in `references/extensions-error-codes.md` and read the next ~50 lines. Stop at the next `## Error Code` header.

---

## References

- [extensions-error-codes.md](references/extensions-error-codes.md) — Complete list of DEC error codes with descriptions and troubleshooting steps

