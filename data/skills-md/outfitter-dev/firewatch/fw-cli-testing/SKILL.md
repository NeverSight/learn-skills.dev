---
name: fw-cli-testing
description: Parallel CLI stress testing using orchestrated subagents. Spawns specialized agents to test different CLI domains simultaneously, aggregating results into structured reports. Supports discovery mode (agents analyze CLI structure) and directive mode (runbooks specify tests). Use when stress testing the Firewatch CLI, validating commands, or running comprehensive test coverage.
user-invocable: true
compatibility: Requires Bun runtime and firewatch project structure (apps/cli/)
metadata:
  author: outfitter-dev
  version: "1.1"
---

# Firewatch CLI Stress Testing

Orchestrate parallel subagents to comprehensively test the Firewatch CLI surface area.

## Contents

- [Overview](#overview)
- [Modes](#modes)
- [Running Tests](#running-tests)
- [Agent Categories](#agent-categories)
- [Report Format](#report-format)
- [Runbooks](#runbooks)
- [Aggregating Results](#aggregating-results)

## Overview

Instead of sequential testing, spawn multiple specialized agents in parallel. Each agent focuses on a specific domain and returns a structured report. This provides:

- **Speed**: 4x faster than sequential testing
- **Coverage**: Dedicated focus per domain catches more edge cases
- **Isolation**: One agent's issues don't block others
- **Structured output**: Easy to aggregate and compare

**CLI under test**: `bun apps/cli/bin/fw.ts`
**Test repo**: `outfitter-dev/firewatch` (has cached data)

## CLI Structure

The Firewatch CLI has this command structure:

```
fw [options]              # Root command - query/filter cached activity
├── pr                    # PR operations subgroup
│   ├── list              # List PRs with filters
│   ├── edit              # Edit PR metadata
│   ├── comment           # Add PR comment
│   └── review            # Submit review
├── fb                    # Feedback abstraction
├── ack                   # Acknowledge feedback
├── close                 # Close/resolve threads (alias: resolve)
├── cache                 # Cache management
│   ├── status            # Cache statistics
│   └── clear             # Clear cache
├── status                # Firewatch state info
├── config                # View/edit configuration
├── doctor                # Diagnose setup
├── schema                # Print JSON schemas
├── examples              # Show jq patterns
├── mcp                   # Start MCP server
└── claude-plugin         # Install/uninstall plugin
```

## Modes

### Discovery Mode

Agents analyze the CLI structure to determine what to test:

```
You: "Stress test the Firewatch CLI"

1. Agent scans apps/cli/src/commands/ to find all commands
2. Agent analyzes each command's options and flags
3. Agent generates test cases based on discovered surface
4. Agent executes and reports
```

Use when: You want comprehensive coverage without specifying what to test.

### Directive Mode

Use runbooks to specify focused test suites:

```
You: "Run the query operations runbook"

1. Load runbooks/query-operations.md
2. Execute specified test cases
3. Report results
```

Use when: You want targeted testing of specific functionality.

### Hybrid Mode

Combine both: run discovery on some areas, runbooks on others:

```
You: "Run the edge cases runbook, then discover-test any commands not covered"
```

## Running Tests

### Full Discovery Test

Launch 4 parallel agents to discover and test different domains:

```markdown
## Agent Prompts

Launch these agents in parallel using `run_in_background: true`:

### 1. Query Operations Agent

Analyze the root `fw` command and its filtering options.
Test all flags: --type, --since, --author, --pr, --open, --active, --mine, --reviews, --limit, --summary.
Focus: Read-only operations, filtering, output modes.

### 2. Status/Info Agent

Analyze apps/cli/src/commands/ for informational commands.
Test: status, config, doctor, schema, cache status, help.
Focus: Diagnostic and configuration commands.

### 3. Edge Cases Agent

Test boundary conditions across all commands.
Focus: Invalid inputs, missing args, conflicting flags, exit codes.

### 4. Mutation Agent

Analyze pr subcommands (edit, comment, review) and feedback commands (fb, ack, close).
Test help text, validation, error messages (avoid actual mutations).
Focus: Write operations in dry-run/help mode.
```

### Directive Test with Runbook

```markdown
Load runbooks/query-operations.md and execute each test case.
Report results in the standard format.
```

## Agent Categories

### Query Operations

Tests read-only query commands on the root `fw` command:

| Area             | Tests                                            |
| ---------------- | ------------------------------------------------ |
| Basic output     | `--jsonl`, `--summary`, JSONL validation         |
| Type filtering   | `--type comment`, `--type review`, invalid types |
| Time filtering   | `--since 24h`, `--since 7d`, invalid durations   |
| Author filtering | `--author name`, `--author '!name'` exclusion    |
| PR filtering     | `--pr 42`, multiple PRs                          |
| State filtering  | `--open`, `--active`, `--state merged`           |
| Combined filters | Multiple flags together                          |
| Special flags    | `--no-bots`, `--limit`, `--mine`, `--reviews`    |

### Status/Config/Doctor

Tests informational commands:

| Area   | Tests                                |
| ------ | ------------------------------------ |
| status | Default, `--short`, `--jsonl`        |
| config | Read, `--path`, `--local`, `--edit`  |
| doctor | Default, `--fix`, `--jsonl`          |
| schema | `query`, `fb`, `status`, `config`    |
| cache  | `cache status`, `cache clear --help` |
| Help   | All commands have help text          |

### Edge Cases/Errors

Tests boundary conditions:

| Area              | Tests                              |
| ----------------- | ---------------------------------- |
| Missing args      | Required arguments omitted         |
| Invalid formats   | Bad repo slugs, invalid durations  |
| Conflicting flags | `--draft --ready` together         |
| Empty results     | Filters that match nothing         |
| Special chars     | Arguments with quotes, spaces      |
| Exit codes        | 0 for success, non-zero for errors |

### Mutation Commands

Tests write operations (validation only, no actual mutations):

| Area       | Tests                                |
| ---------- | ------------------------------------ |
| pr comment | Help text, required args, validation |
| pr edit    | Help text, conflicting options       |
| pr review  | Help text, target validation         |
| close      | Help text, ID validation, --all      |
| ack        | Help text, --list, --clear           |
| fb         | Help text, --stack, --resolve        |

## Report Format

Each agent must return results in this structure:

```markdown
## Results: [CATEGORY]

### Test Results

| Test         | Command             | Result | Notes               |
| ------------ | ------------------- | ------ | ------------------- |
| Basic query  | `fw --limit 5`      | PASS   | Returns valid JSONL |
| Invalid type | `fw --type invalid` | PASS   | Exits with error    |
| ...          | ...                 | ...    | ...                 |

### Summary

- **Total**: X tests
- **Pass**: X
- **Warn**: X (unexpected but not broken)
- **Fail**: X (broken behavior)

### Issues Found

#### Failures (must fix)

- [Description of broken behavior]

#### Warnings (should investigate)

- [Description of unexpected behavior]

#### Recommendations

- [Suggested improvements]
```

### Result Classifications

| Result   | Meaning                                         |
| -------- | ----------------------------------------------- |
| **PASS** | Behaves as expected                             |
| **WARN** | Works but unexpected (doc mismatch, odd output) |
| **FAIL** | Broken behavior, errors, crashes                |

## Runbooks

Runbooks live in `runbooks/` subdirectory. Each defines a focused test suite.

### Runbook Format

```markdown
---
name: [runbook-name]
focus: [what this tests]
estimated-tests: [approximate count]
---

# [Runbook Name]

## Setup

[Any prerequisites]

## Test Cases

### [Test Name]

**Command**: `fw ...`
**Expected**: [what should happen]
**Validates**: [what this proves]

### [Test Name]

...
```

### Available Runbooks

| Runbook               | Focus                         |
| --------------------- | ----------------------------- |
| `query-operations.md` | Query filtering and output    |
| `edge-cases.md`       | Error handling and boundaries |
| `status-info.md`      | Diagnostic commands           |
| `mutations.md`        | Write operation validation    |

## Aggregating Results

After agents complete, aggregate into a summary:

```markdown
## CLI Stress Test Summary

| Agent            | Pass   | Warn  | Fail  |
| ---------------- | ------ | ----- | ----- |
| Query Operations | 22     | 1     | 1     |
| Status/Config    | 18     | 2     | 0     |
| Edge Cases       | 15     | 3     | 0     |
| Mutations        | 12     | 2     | 0     |
| **TOTAL**        | **67** | **8** | **1** |

### Failures (Priority 1)

- [List failures that need immediate fixes]

### Warnings (Priority 2)

- [List warnings to investigate]

### Recommendations

- [List improvements to consider]
```

## When to Use

- After major CLI refactors
- Before releases
- When adding new commands
- To validate error handling
- After changing option parsing

## Example Orchestration

```markdown
# Full stress test orchestration

1. Launch 4 discovery agents in parallel (background)
2. Wait for all agents to complete
3. Collect results from each agent
4. Aggregate into summary table
5. Categorize findings by severity
6. Present prioritized action items
```

## Agent Tips

1. **Use `--help` liberally** — Every command should have help
2. **Test exit codes** — `echo $?` after commands
3. **Validate JSONL** — Pipe to `jq .` to check valid JSON
4. **Document unexpected** — Even "works" can be WARN if surprising
5. **Compare to docs** — Flag mismatches are common findings
6. **Use env vars** — `FIREWATCH_JSONL=0` forces human output
