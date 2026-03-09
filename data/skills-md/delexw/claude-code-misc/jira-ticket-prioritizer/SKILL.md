---
name: jira-ticket-prioritizer
description: Analyze JIRA tickets to determine priority and dependency order. Outputs an ordered JIRA ID list. Use before implement/forge, or when asked to "prioritize tickets", "order these JIRAs", "what should I work on first".
argument-hint: 'TICKET-KEY1,TICKET-KEY2,... [additional-context]'
allowed-tools: Read, Bash, Write
---

# JIRA Ticket Prioritizer

Analyze a set of JIRA tickets to determine optimal execution order based on dependencies and priority. Produces an ordered list usable standalone or as a pre-step before `implement`/`forge`.

## Arguments
- `$ARGUMENTS[0]` — Comma-separated ticket keys (e.g. `EC-100,EC-101,EC-102`) OR a JQL query (detected by presence of `=`, `AND`, `OR`)
- `$ARGUMENTS[1]` — (optional) Additional context for prioritization (e.g. "focus on backend", "frontend first")

## System Requirements
- `jira` CLI installed and configured (https://github.com/ankitpokhrel/jira-cli)
- Environment variable `JIRA_API_TOKEN` set with a valid Jira API token. **Important:** When checking this variable, verify at least 2 times before concluding it is not set. **Never expose the value** — use existence checks only.

## Execution

### Step 1 — Parse Input
- Check if `$ARGUMENTS[0]` contains `=`, `AND`, or `OR` (case-insensitive) to detect JQL
- **If JQL detected**: run `jira issue list --jql "$ARGUMENTS[0]" --plain --columns key --no-headers` to resolve to ticket keys
- **If comma-separated**: split on `,` and trim whitespace
- Validate each key matches `[A-Z]+-\d+`
- If fewer than 2 valid tickets, report the single ticket and exit

### Step 2 — Fetch All Tickets
- Create temp directory: `mkdir -p .jira-ticket-prioritizer-tmp/tickets`
- For each ticket key, fetch via jira CLI:
  ```
  jira issue view {KEY} --raw > .jira-ticket-prioritizer-tmp/tickets/{KEY}.json
  ```
- Parse each ticket using the jira-ticket-viewer parse script:
  ```
  node ../jira-ticket-viewer/scripts/parse-ticket.js < .jira-ticket-prioritizer-tmp/tickets/{KEY}.json > .jira-ticket-prioritizer-tmp/tickets/{KEY}-parsed.json
  ```
- Collect all parsed outputs into a single JSON array and write to `.jira-ticket-prioritizer-tmp/all-tickets.json`

### Step 3 — Build Dependency Graph
- Run: `node ./scripts/build-dependency-graph.js < .jira-ticket-prioritizer-tmp/all-tickets.json > .jira-ticket-prioritizer-tmp/graph.json`
- Review graph output for cycles or warnings
- See [references/dependency-analysis.md](references/dependency-analysis.md) for relationship mapping rules

### Step 4 — Semantic Dependency Analysis
- For tickets flagged with `"relates to"` links or no explicit links in the graph output, analyze their `description`, `summary`, and `commentSummary` for implicit dependencies
- Look for:
  - References to other ticket keys in the input set
  - Shared component or module mentions
  - Functional ordering hints ("builds on", "requires", "after", "depends on")
- Add soft edges with confidence levels (high/medium/low) to the graph
- Re-run topological sort if new edges were added:
  - Update `all-tickets.json` with additional `softEdges` and re-run `build-dependency-graph.js`

### Step 5 — Priority Scoring
- For tickets at the same dependency layer, score using weights from [references/priority-weights.md](references/priority-weights.md)
- Skip tickets with status "Done" — list them as excluded in the report
- Sort within each layer by descending score
- Apply `$ARGUMENTS[1]` context as a tiebreaker or boost (e.g. "focus on backend" boosts tickets with backend labels/components)

### Step 6 — Generate Output
- Write `.jira-ticket-prioritizer-tmp/detailed-report.json` — full details including scores, justifications, dependency graph, excluded tickets, and warnings (see [references/output-format.md](references/output-format.md) for schema)
- Write `.jira-ticket-prioritizer-tmp/output.json` — a JSON object `{ "layers": [...] }` where `layers` contains ticket keys grouped by dependency layer (array of arrays), sorted by priority score within each layer
- **Present only `output.json`** (the simple layers object) to the user. The detailed report is saved for reference but not displayed.

## Reference Files

| Name | When to Read |
|------|-------------|
| [references/priority-weights.md](references/priority-weights.md) | Step 5 — scoring rules and factor weights |
| [references/output-format.md](references/output-format.md) | Step 6 — report template and JSON schema |
| [references/dependency-analysis.md](references/dependency-analysis.md) | Steps 3-4 — dependency detection rules |

<tags>
   <mode>think</mode>
   <custom>yes</custom>
</tags>
