---
name: reading-logs
description: Analyzes logs efficiently through targeted search and iterative refinement. Use when investigating errors, debugging incidents, or analyzing patterns in application logs.
---

# Reading Logs

**IRON LAW:** Filter first, then read. Never open a large log file without narrowing it first.

## Delegation

For log files over a few hundred lines, delegate to the `@ce:log-reader` agent. It runs on haiku to keep costs low and context clean. Prompt it with:
- What to investigate (error text, time window, correlation IDs)
- Which log files or directories to search
- The `scripts/` utilities available (see [Utility Scripts](#utility-scripts) below)

The agent has this skill preloaded, so it already knows the methodology. Keep your prompt tight and specific - don't paste log contents into the delegation message.

## Core Principles

1. **Filter first** - Search/filter before reading
2. **Iterative narrowing** - Start broad (severity), refine with patterns/time
3. **Small context windows** - Fetch 5-10 lines around matches, not entire files
4. **Summaries over dumps** - Present findings concisely, not raw output

## Tool Strategy

### 1. Find Logs (Glob)

```bash
**/*.log
**/logs/**
**/*.log.*  # Rotated logs
```

### 2. Filter with Grep

```bash
# Severity search
grep -Ei "error|warn" app.log

# Exclude noise
grep -i "ERROR" app.log | grep -v "known-benign"

# Context around matches
grep -C 5 "ERROR" app.log  # 5 lines before/after

# Time window
grep "2025-12-04T11:" app.log | grep "ERROR"

# Count occurrences
grep -c "connection refused" app.log
```

### 3. Chain with Bash

```bash
# Recent only
tail -n 2000 app.log | grep -Ei "error"

# Top recurring
grep -i "ERROR" app.log | sort | uniq -c | sort -nr | head -20
```

### 4. Read Last

Only after narrowing with Grep. Use context flags (`-C`, `-A`, `-B`) to grab targeted chunks.

## Investigation Workflows

### Single Incident

1. Get time window, error text, correlation IDs
2. Find logs covering that time (`Glob`)
3. Time-window grep: `grep "2025-12-04T11:" service.log | grep -i "timeout"`
4. Trace by ID: `grep "req-abc123" *.log`
5. Expand context: `grep -C 10 "req-abc123" app.log`

### Recurring Patterns

1. Filter by severity: `grep -Ei "error|warn" app.log`
2. Group and count: `grep -i "ERROR" app.log | sort | uniq -c | sort -nr | head`
3. Exclude known noise
4. Drill into top patterns with context

## Red Flags

- Opening >10MB file without filtering
- Using Read before Grep
- Dumping raw output without summarizing
- Searching without time bounds on multi-day logs

## Utility Scripts

For complex operations, use the scripts in `scripts/`:

```bash
# Aggregate errors by frequency (normalizes timestamps/IDs)
bash scripts/aggregate-errors.sh app.log "ERROR" 20

# Extract and group stack traces by type
bash scripts/extract-stack-traces.sh app.log "NullPointer"

# Parse JSON logs with jq filter
bash scripts/parse-json-logs.sh app.log 'select(.level == "error")'

# Show error distribution over time (hourly/minute buckets)
bash scripts/timeline.sh app.log "ERROR" hour

# Trace a request ID across multiple log files
bash scripts/trace-request.sh req-abc123 logs/

# Find slow operations by duration
bash scripts/slow-requests.sh app.log 1000 20
```

## Output Format

1. State what you searched (files, patterns)
2. Provide short snippets illustrating the issue
3. Explain what likely happened and why
4. Suggest next steps
