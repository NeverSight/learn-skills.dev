---
name: cledon
description: Manage voice AI agent testing with Cledon's MCP server. Create personas, test cases, scenarios, then run and monitor automated voice tests. Use when working with voice agent testing, SIP calls, test assertions, call transcripts, or Cledon.
license: MIT
metadata:
  author: cledon
  version: "1.0.0"
---

# Cledon — Voice AI Agent Testing

Cledon tests voice AI agents by simulating callers that phone your agent and evaluate responses against assertions.

## Domain Model

```
Agent        — the voice AI being tested (name, phone number, personality)
Persona      — simulated caller profile (voice, age, language, attributes)
Folder       — groups related test cases
Test Case    — defines assertions + expected tool calls for one agent
Scenario     — combines one test case + one persona = one runnable test
Run          — execution of a scenario producing transcript + pass/fail results
```

Relationships: Agent → many Test Cases → many Scenarios ← Persona. Each Scenario produces Runs.

## Available Tools (24)

### Analytics
| Tool | Purpose |
|------|---------|
| `get-overall-stats` | Dashboard summary: total scenarios, runs, pass rate, avg duration |
| `get-run-history` | Recent runs with pass/fail counts (1-90 days lookback) |
| `get-failed-assertions` | Top 10 recurring failures with up to 3 example runs each |

### Agents
| Tool | Purpose |
|------|---------|
| `list-agents` | List all voice agents |
| `get-agent` | Full agent details by ID |
| `create-agent` | Create agent (name, phoneNumber, gender, personality) |
| `update-agent` | Update agent properties |
| `delete-agent` | Delete agent and associated data |

### Personas
| Tool | Purpose |
|------|---------|
| `list-personas` | List all simulated caller personas |
| `get-persona` | Full persona details by ID |
| `create-persona` | Create persona (name, gender, ageRange, language, attributes, voiceDescription, environment) |
| `update-persona` | Update persona properties |
| `delete-persona` | Delete persona |

### Test Cases & Scenarios
| Tool | Purpose |
|------|---------|
| `list-folders` | List test case folders |
| `list-testcases` | List test cases (optional folderId filter) |
| `get-testcase` | Full test case with assertions and expected tool calls |
| `create-testcase` | Create test case with assertions and expected tool calls |
| `update-testcase` | Update test case properties |
| `execute-testcase` | Run all scenarios for a test case |
| `list-scenarios` | List scenarios (optional testCaseId filter) |
| `get-scenario` | Full scenario with caller instructions |

### Execution
| Tool | Purpose |
|------|---------|
| `run-scenario` | Trigger single test → returns runId |
| `run-multiple-scenarios` | Batch trigger → returns array of runIds |
| `get-run-status` | Full run details: transcript, assertions, tool call validation |
| `get-scenario-runs` | Run history for one scenario with pass/fail counts |
| `cancel-run` | Cancel a stuck run (only status=running) |

## Workflows

### Get an overview of testing status
1. `get-overall-stats` → see pass rate, total runs, average duration
2. `get-run-history` with days=7 → see recent individual results
3. `get-failed-assertions` → identify systemic issues

### Run a test and check results
1. `list-scenarios` → find the scenario ID
2. `run-scenario` with scenarioId → get back a runId
3. Wait a moment, then `get-run-status` with runId → see transcript + assertion results
4. If status is still "running", wait and check again

### Run all tests for a test case
1. `list-scenarios` with testCaseId filter → collect all scenario IDs
2. `run-multiple-scenarios` with the ID array
3. `get-run-history` with days=1 → see batch results

### Investigate failures
1. `get-failed-assertions` → find the most common failures
2. Pick a failure, note the example runIds
3. `get-run-status` for each runId → read the transcript to understand what went wrong
4. `get-scenario-runs` for that scenarioId → check if it's a regression or consistent failure

### Drill into a specific test case
1. `get-testcase` with id → see assertions and expected tool calls
2. `list-scenarios` with testCaseId → see all persona combinations
3. `get-scenario` for each → see caller instructions

### Create a new test from scratch
1. `list-agents` → pick the agent to test (or `create-agent`)
2. `list-personas` → pick a persona (or `create-persona` with gender, ageRange, language, attributes, voiceDescription)
3. `create-testcase` with agent ID, assertions, and optional expected tool calls
4. Create a scenario through the Cledon web UI (scenario creation is not yet exposed via MCP)
5. `execute-testcase` → run all scenarios, or `run-scenario` → run a single one

## Key Patterns

- List endpoints return compact data. Use the corresponding get-by-ID tool to see full details.
- `run-scenario` is async: it returns a runId immediately. Poll `get-run-status` to see results.
- Persona `language` accepts "de" or "en". Persona `ageRange` accepts "young", "adult", or "senior".
- All data is scoped to the authenticated user's organization. No cross-tenant access.
- Run `outcome` is either "passed" or "failed". Run `status` progresses: running → completed/failed.
