---
name: sniff-report
description: Show the results from the last sniff scan.
user-invocable: false
---

# /sniff-report - Show last scan results

Display findings from the most recent scan.

This skill is invoked by the `sniff` skill's own flow, not on its own. The `user-invocable: false` frontmatter key is honored by Claude Code only, so in other agents this file may show up as a standalone command; treat it as a step inside a sniff run rather than an entry point.

## What to do

1. Use the unified `sniff` MCP tool with:
   - `mode`: `"report"`
   - `rootDir`: the current project's absolute path
   - `format`: 'summary' for readable output, 'json' for raw data

2. If the unified `sniff` tool is not available, use legacy `sniff_report` with the same rootDir and format.

3. Present the summary to the user:
   - Total findings by severity
   - Top issues with file locations
   - Any corroborated findings (confirmed in source + browser)

## Example

```
User: /sniff-report
You: Here are the results from your last scan:

**Summary:** 12 findings (1 critical, 3 high, 6 medium, 2 low)

**Top issues:**
1. `src/routes.ts:14` - CRITICAL: Hardcoded API key
2. `src/handler.ts:42` - HIGH: debugger statement
3. `README.md:28` - HIGH: Broken internal link

Reports saved to:
- .sniff/reports/report.html
- .sniff/reports/report.json
```
