---
name: turbo-monitor-debug
description: "Use this skill when the user needs to look up goldsky turbo CLI syntax — flags and options for `inspect`, `logs`, or `list` commands — or wants to know keyboard shortcuts for the `turbo inspect` TUI. Also use for: decoding what a specific error message means (backpressure, connection refused, auth failures, etc.), using the analyze-logs.sh script, or understanding how inspect/logs commands work. Distinguishing factor: this skill provides reference information and explanations. If the user has a broken pipeline and wants step-by-step interactive diagnosis, use /turbo-doctor instead."
---

# Turbo Pipeline Monitoring & Debugging Reference

CLI commands, error patterns, and troubleshooting reference for Turbo pipelines. For interactive pipeline diagnosis (running commands, checking logs, walking through fixes), use `/turbo-doctor` instead.

## Quick Reference

| Action                   | Command                                  |
| ------------------------ | ---------------------------------------- |
| List pipelines           | `goldsky turbo list`                     |
| View live data           | `goldsky turbo inspect <name>`           |
| Inspect specific node    | `goldsky turbo inspect <name> -n <node>` |
| View logs                | `goldsky turbo logs <name>`              |
| Follow logs              | `goldsky turbo logs <name> --follow`     |
| Logs with timestamps     | `goldsky turbo logs <name> --timestamps` |
| Last N lines             | `goldsky turbo logs <name> --tail N`     |
| Logs since N seconds ago | `goldsky turbo logs <name> --since N`    |

## Live Inspect TUI Shortcuts

| Key                     | Action               |
| ----------------------- | -------------------- |
| `Tab`/`→`, `Shift+Tab`/`←` | Next/prev tab    |
| `1`-`9`                 | Jump to tab number   |
| `j`/`k` / `↑`/`↓`     | Scroll               |
| `g`/`Home`, `G`/`End`  | Top/bottom           |
| `Page Up`/`Page Down`  | Scroll by page       |
| `/` → `Enter`          | Search               |
| `n` / `N`              | Next/prev match      |
| `Esc`                   | Clear search         |
| `d`                     | Toggle definition    |
| `w`                     | Open web dashboard   |
| `e`                     | Open web editor      |
| `q` / `Ctrl+C`         | Quit                 |
| `Shift` + mouse         | Select and copy text |

### Auto-Reconnection

The TUI automatically reconnects when the pipeline is updated, paused, resumed, or temporarily unavailable. It displays "Reconnecting..." and preserves previously received data. The TUI has a **30-minute timeout** — if the pipeline remains unreachable for 30 minutes, it closes automatically.

## Error Pattern Reference

> **Detailed error patterns and solutions are in the `data/` folder.**

| File                  | Contents                                           |
| --------------------- | -------------------------------------------------- |
| `error-patterns.json` | All known error patterns with causes and solutions |

**Data location:** `data/` (relative to this skill's directory)

### Log Analysis Script

Use the helper script to quickly analyze pipeline logs:

```bash
./scripts/analyze-logs.sh <pipeline-name>
./scripts/analyze-logs.sh <pipeline-name> --tail 100
```

The script checks for common error patterns and reports findings with recommendations.

---

## Common Error Patterns

| Error Pattern             | Likely Cause               | Fix                                            |
| ------------------------- | -------------------------- | ---------------------------------------------- |
| `connection refused`      | Database unreachable       | Check network/firewall settings                |
| `authentication failed`   | Wrong credentials          | Update secret with correct credentials         |
| `secret not found`        | Missing secret             | Create secret with `goldsky secret create`     |
| `SQL syntax error`        | Invalid transform SQL      | Fix SQL in YAML and redeploy                   |
| `duplicate key`           | Primary key collision      | Ensure unique primary key in transform          |
| `script transform error`  | TypeScript runtime failure | Check script logic, null handling, return types |
| `dynamic_table` error     | Backend connection issue   | Verify dynamic table secret/table exists        |
| `WASM execution failed`   | Script crash in sandbox    | Debug script — check for undefined access       |
| `handler timeout`         | External HTTP endpoint slow| Increase `timeout_ms` or fix handler endpoint   |

## Script Transform Issues

| Issue                        | Fix                                                    |
| ---------------------------- | ------------------------------------------------------ |
| `undefined` property access  | Add null checks: `input.field ?? ''`                   |
| Wrong return type            | Ensure returned object matches `schema` exactly        |
| Missing return fields        | All `schema` fields must be present in returned object |
| `invoke is not a function`   | Ensure script defines `function invoke(data)`          |
| BigInt errors                | Use `BigInt()` constructor, not direct number literals  |

## Dynamic Table Issues

| Issue                      | Fix                                                    |
| -------------------------- | ------------------------------------------------------ |
| Table not found            | Create the table in PostgreSQL before deploying         |
| No matches from check      | Verify data exists in the backing table                 |
| Stale data                 | For postgres backend, verify rows are actually there    |
| Memory pressure            | Large in_memory tables → switch to postgres backend     |

## Common Issues Quick Reference

| Symptom            | Likely Cause           | Quick Fix                           |
| ------------------ | ---------------------- | ----------------------------------- |
| No data flowing    | `start_at: latest`     | Wait for new data or use `earliest` |
| Auth failed        | Wrong credentials      | Update secret with correct password |
| Connection refused | Network/firewall       | Check host, whitelist Goldsky IPs   |
| Storage exceeded   | Neon free tier (512MB) | Upgrade plan or clear data          |
| SQL error          | Bad transform syntax   | Validate YAML first                 |

## Troubleshooting

| Issue                    | Action                                                 |
| ------------------------ | ------------------------------------------------------ |
| Can't connect to inspect | Check pipeline is running with `goldsky turbo list`    |
| Logs are empty           | Pipeline may be new; wait for data or check `start_at` |
| TUI disconnects          | Auto-reconnects within 30 min; check pipeline status   |
| Can't find pipeline      | Verify correct project with `goldsky project list`     |

## Related

- **`/turbo-doctor`** — Interactive diagnostic skill that uses this reference to troubleshoot pipelines
- **`/turbo-builder`** — Build and deploy new pipelines
