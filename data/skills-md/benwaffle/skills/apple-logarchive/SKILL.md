---
name: apple-logarchive
description: Query and analyze Apple .logarchive files using the macOS `log show` command
user-invocable: true
allowed-tools:
  - Bash(/usr/bin/log show *)
  - Bash(/usr/bin/log stats *)
  - Bash(/usr/bin/log help *)
  - Bash(ls *)
  - Bash(wc *)
  - Bash(head *)
  - Bash(tail *)
---

# Apple Log Archive Skill

You are an expert at analyzing macOS/iOS unified log archives (`.logarchive` bundles) using the `/usr/bin/log` command.

## When to Use

Activate when the user wants to:
- Search, filter, or analyze a `.logarchive` file
- Find errors, faults, or crashes in system logs
- Investigate a specific process, subsystem, or category in logs
- Understand what happened during a time window
- Count or summarize log activity

## Step 1 — Locate the Archive

Ask the user for the path to their `.logarchive` if not already provided. Verify it exists:

```
ls <path>.logarchive/Info.plist
```

## Step 2 — Determine Time Range

Get the first and last timestamps to understand the archive's span:

```
/usr/bin/log show --style ndjson --no-pager <archive> | head -1
/usr/bin/log show --style ndjson --no-pager <archive> | tail -1
```

## Step 3 — Query the Archive

Use `/usr/bin/log show` with appropriate filters. **Always pass `--no-pager`** to prevent interactive mode.

### Command Structure

```
/usr/bin/log show [options] <archive>
```

### Key Options

| Option | Description |
|---|---|
| `--predicate '<filter>'` | Filter using NSPredicate or shorthand syntax |
| `--style <format>` | Output format: `default`, `syslog`, `json`, `ndjson`, `compact` |
| `--start 'Y-M-D H:m:s'` | Show events from this time |
| `--end 'Y-M-D H:m:s'` | Show events up to this time |
| `--last <N>m\|h\|d` | Show last N minutes/hours/days |
| `--info` | Include Info-level messages (excluded by default) |
| `--debug` | Include Debug-level messages (excluded by default) |
| `--source` | Annotate with source file and line number |
| `--process <name\|pid>` | Filter by process name or PID |
| `--no-pager` | **Always use this** — prevents interactive less |

### Predicate Fields

| Field | Type | Description |
|---|---|---|
| `process` (shorthand: `p`) | string | Process name |
| `processIdentifier` (shorthand: `pid`) | integer | Process ID |
| `subsystem` (shorthand: `s`) | string | Subsystem (e.g. `com.apple.xpc`) |
| `category` (shorthand: `c`, `cat`) | string | Category within subsystem |
| `composedMessage` (shorthand: `m`) | string | Log message text |
| `sender` (shorthand: `l`, `lib`) | string | Library/sender name |
| `logType` | log type | `default`, `info`, `debug`, `error`, `fault` |
| `type` (shorthand only) | event type | `default`, `info`, `debug`, `error`, `fault`, `loss`, `signpost` |
| `senderImagePath` | string | Full path to sender library |
| `processImagePath` | string | Full path to process binary |
| `threadIdentifier` (shorthand: `tid`) | integer | Thread ID |
| `eventType` | string | `logEvent`, `signpostEvent`, `stateEvent`, `activityCreateEvent`, `timesyncEvent`, `lossEvent` |

### Predicate Syntax — Shorthand (preferred for simple queries)

```
# By process
'p=Safari'
'p=foo|bar'                    # multiple processes (OR)

# By message content
'"error loading"'              # message contains (field omitted = message)
'm:"timeout"'                  # explicit message contains
'm~/"regex pattern"'           # regex match

# By subsystem/category
's=com.apple.xpc'
'c=connection'

# By log level
'type=error'
'type>=error'                  # error + fault

# Combined
'p=CommCenter AND type>=error'
'pid=100 AND "connection"'
's=com.apple.xpc AND c=connection AND type=error'
```

### Predicate Syntax — NSPredicate (for complex queries)

```
'process == "Safari"'
'composedMessage CONTAINS "error"'
'subsystem == "com.apple.xpc" AND category == "connection"'
'logType == "fault" OR logType == "error"'
'composedMessage MATCHES ".*timeout.*"'
'processImagePath ENDSWITH "CommCenter"'
'eventType == "signpostEvent"'
```

### Comparison Operators

| Operator | Description |
|---|---|
| `==`, `=` | Equality |
| `!=`, `<>` | Inequality |
| `CONTAINS`, `:` | Contains substring |
| `BEGINSWITH`, `:^` | Starts with |
| `ENDSWITH` | Ends with |
| `LIKE` | Wildcard match (`?` = 1 char, `*` = 0+ chars) |
| `MATCHES`, `~/` | Regex match |
| `AND`, `OR`, `NOT` | Logical operators |

## Output Guidelines

- Use `--style ndjson` when you need to parse or count results programmatically (pipe to `wc -l`, `head`, `tail`, etc.)
- Use `--style default` (or omit) for human-readable output to show the user
- Use `--style compact` for a denser human-readable view
- **Always pipe through `head -N`** for initial exploration to avoid overwhelming output — logarchives can contain millions of entries
- For counting: `/usr/bin/log show --no-pager --style ndjson --predicate '...' <archive> | wc -l`

## Common Workflows

### Find all errors and faults
```
/usr/bin/log show --no-pager --predicate 'type>=error' <archive> | head -50
```

### Investigate a specific process
```
/usr/bin/log show --no-pager --predicate 'p=SpringBoard' --info --debug <archive> | head -100
```

### Search for a keyword in messages
```
/usr/bin/log show --no-pager --predicate '"crash"' <archive> | head -50
```

### Logs from a specific subsystem during a time window
```
/usr/bin/log show --no-pager --start '2026-03-01 10:00:00' --end '2026-03-01 10:05:00' --predicate 's=com.apple.xpc' <archive>
```

### Count events by type
```
/usr/bin/log show --no-pager --style ndjson --predicate 'type=error' <archive> | wc -l
/usr/bin/log show --no-pager --style ndjson --predicate 'type=fault' <archive> | wc -l
```

### List unique processes in the archive
```
/usr/bin/log show --no-pager --style ndjson <archive> | head -1000 | python3 -c "import sys,json; procs=set(); [procs.add(json.loads(l).get('processImagePath','')) for l in sys.stdin]; print('\n'.join(sorted(procs)))"
```

## Important Notes

- **Always use `--no-pager`** — interactive pagers hang in non-interactive shells
- **Always pipe through `head`** on first query — archives can be enormous
- By default only `Default` and `Error`/`Fault` level messages are shown; pass `--info` and/or `--debug` to include lower-severity messages
- Time format for `--start`/`--end`: `'Y-M-D H:m:s'` or `'Y-M-D'`
- Use shorthand predicates for simple queries; use NSPredicate syntax when you need `MATCHES`, `ENDSWITH`, `LIKE`, or complex nesting
- The `eventMessage` field in JSON output corresponds to `composedMessage` in predicates
