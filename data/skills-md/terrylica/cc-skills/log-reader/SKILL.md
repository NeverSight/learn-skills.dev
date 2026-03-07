---
name: log-reader
description: Read MetaTrader 5 log files. TRIGGERS - MT5 logs, Experts pane, indicator errors, compilation errors.
allowed-tools: Read, Bash, Grep
---

# MT5 Log Reader

Read MetaTrader 5 log files directly to access Print() output from indicators, scripts, and expert advisors without requiring manual Experts pane inspection.

## Purpose

Implement "Option 3" dual logging pattern:

- **Print()** - MT5 log files (human-readable via Experts pane)
- **CSV files** - Structured data (programmatic analysis)

Claude Code CLI can autonomously read both outputs without user intervention.

## When to Use This Skill

Use this skill when:

- Validating MT5 indicator/script execution
- Checking compilation or runtime errors
- Analyzing Print() debug output
- Verifying unit test results (Test_PatternDetector, Test_ArrowManager)
- User mentions checking "Experts pane" manually

## Log File Location

MT5 logs are stored at:

```
$MQL5_ROOT/Program Files/MetaTrader 5/MQL5/Logs/YYYYMMDD.log
```

**File Format**:

- Encoding: UTF-16LE (Little Endian)
- Structure: Tab-separated fields (timestamp, source, message)
- Size: Grows throughout day (typically 10-100KB)

## Instructions

### 1. Construct today's log path

```bash
/usr/bin/env bash << 'SKILL_SCRIPT_EOF'
# Determine current date
TODAY=$(date +"%Y%m%d")

# Build absolute path
LOG_FILE="$MQL5_ROOT/Program Files/MetaTrader 5/MQL5/Logs/${TODAY}.log"
SKILL_SCRIPT_EOF
```

### 2. Read the entire log file

Use Read tool:

- File path: Absolute path from step 1
- The file contains all Print() statements from MT5 indicators/scripts
- UTF-16LE encoding is automatically handled by Read tool

### 3. Search for specific content (optional)

Use Grep to filter entries:

```
Pattern: indicator name, "error", "test.*passed", etc.
Path: Log file path from step 1
Output mode: "content" with -n (line numbers)
Context: -A 5 for 5 lines after matches
```

### 4. Analyze recent entries (optional)

Use Bash with tail for latest output:

```bash
tail -n 50 "$LOG_FILE"
```

## Common Validation Patterns

### Check unit test results

Search for test pass/fail indicators:

```
Pattern: test.*passed|test.*failed|Tests Passed|Tests Failed|ALL TESTS PASSED
Output mode: content
Context: -B 2 -A 2
```

### Find compilation errors

```
Pattern: error|ERROR|warning|WARNING|failed to create
Output mode: content
Context: -A 3
```

### Monitor specific indicator

```
Pattern: CCI Rising Test|PatternDetector|ArrowManager
Output mode: content
Context: -A 2
```

### View initialization messages

```
Pattern: OnInit|initialization|Initialization complete|Phase \d+
Output mode: content
```

## Examples

### Example 1: Validate unit test completion

```
Input: User compiled Test_PatternDetector.mq5
Action:
  1. Read today's log file
  2. Grep for "Test.*PatternDetector|Tests Passed|Tests Failed"
  3. Report results (e.g., "17 tests passed, 0 failed")
Output: Test status without user checking Experts pane
```

### Example 2: Check for runtime errors

```
Input: User reports indicator not working
Action:
  1. Read today's log file
  2. Grep for "ERROR|error|failed" with -A 3 context
  3. Analyze error messages
Output: Specific error details and line numbers
```

### Example 3: Verify Phase 2 arrow creation

```
Input: User asks "did the test arrow get created?"
Action:
  1. Read today's log file
  2. Grep for "Phase 2|Test arrow created|Failed to create"
  3. Check for success/failure messages
Output: Arrow creation status with timestamp
```

## Security Considerations

- Log files may contain sensitive trading data (symbol names, account info)
- Restricted to Read, Bash, Grep tools only (no network access via WebFetch)
- Do not expose absolute paths unnecessarily in user-facing output
- Filter sensitive information when reporting results
- No file modification operations allowed

## Integration with Dual Logging

This skill enables programmatic access to one half of the dual logging pattern:

1. **MT5 Log Files** (this skill) - Human-readable Print() output
2. **CSV Files** (CSVLogger.mqh) - Structured audit trails for validation

Both are accessible without user intervention:

- MT5 logs: Read via this skill
- CSV files: Read directly via Read tool or validate_export.py

## Validation Checklist

When using this skill:

- [ ] Log file exists for today's date
- [ ] File size > 0 (not empty)
- [ ] Contains expected indicator/script output
- [ ] Timestamps match execution time
- [ ] Error messages (if any) are actionable
- [ ] Test results (if applicable) show pass/fail counts

## References

- MT5 file locations: `docs/guides/MT5_FILE_LOCATIONS.md`
- Dual logging implementation: `docs/plans/cci-rising-pattern-marker.yaml` Phase 3-4
- CSVLogger library: `Program Files/MetaTrader 5/MQL5/Indicators/Custom/Development/CCINeutrality/lib/CSVLogger.mqh`

---

## Troubleshooting

| Issue                  | Cause                        | Solution                                          |
| ---------------------- | ---------------------------- | ------------------------------------------------- |
| Log file not found     | Wrong date or path           | Verify YYYYMMDD.log format and MQL5_ROOT env var  |
| Empty log file         | MT5 not running or no output | Ensure MT5 is running and Print() is being called |
| Encoding errors        | UTF-16LE not handled         | Read tool handles encoding automatically          |
| Missing test results   | Test not executed            | Compile and run test script in MT5 first          |
| Grep finds nothing     | Wrong pattern                | Use case-insensitive (-i) or broader pattern      |
| Old log data           | Log rotation                 | Each day creates new YYYYMMDD.log file            |
| Path contains spaces   | Unquoted path variable       | Quote paths: "$LOG_FILE"                          |
| Sensitive data exposed | Trading info in logs         | Filter sensitive fields when reporting to user    |
