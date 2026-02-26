---
name: export-and-analyze-jira-data
description: |
  Exports Jira issues with flexible filtering and analyzes data using multiple formats (JSON, CSV, JSONL).
  Use when asked to "export Jira data", "bulk export tickets", "analyze Jira metrics", "extract issues to CSV",
  "get all issues from project", "export with filters", "analyze issue trends", or "prepare Jira data for reporting".
  Covers export patterns, format selection, pagination, filtering strategies, and analysis workflows for large datasets.
  Works with jira-tool CLI, JQL queries, and Python analysis scripts.
---

# Export and Analyze Jira Data

## When to Use This Skill

**Explicit Triggers:**
- "Export Jira issues to CSV"
- "Bulk export all tickets from project X"
- "Get all issues with status Y"
- "Extract Jira data for analysis"
- "Export with changelog for state analysis"
- "Analyze Jira metrics and trends"
- "Prepare Jira data for BI tool"

**Implicit Triggers:**
- Need to analyze issue distribution by status/priority/assignee
- Want to create weekly/monthly metrics reports
- Need to archive historical data
- Preparing data for external tools (Excel, Tableau, Power BI)
- Investigating workflow bottlenecks
- Comparing multiple projects

**Debugging Context:**
- "How do I export large datasets without timeout?"
- "What format should I use for streaming analysis?"
- "Why is my export missing issues?"
- "How to include changelog in export?"

## What This Skill Does

This skill provides expertise in extracting and analyzing Jira data at scale. It covers:
- Exporting issues with complex filters and JQL queries
- Choosing the right format (JSON, CSV, JSONL, Table) for your use case
- Handling pagination for large datasets (1000+ issues)
- Expanding fields (changelog, transitions) for deep analysis
- Transforming and filtering exported data with jq and Python
- Generating insights (status distribution, workload, age analysis)
- Integrating Jira data into external tools and reports

The complete pipeline: query → export → transform → analyze → report.

## Quick Start

Export all active issues to CSV:

```bash
uv run jira-tool export --format csv -o tickets.csv
```

Export high-priority issues in JSON for analysis:

```bash
uv run jira-tool export --priority High --status "In Progress" \
  --format json -o important_tickets.json
```

Analyze state durations for a project:

```bash
# Step 1: Export with changelog
uv run jira-tool search "project = PROJ" \
  --expand changelog \
  --format json \
  -o issues_with_history.json

# Step 2: Analyze
uv run jira-tool analyze state-durations issues_with_history.json \
  -o durations.csv --business-hours
```

## Instructions

### Step 1: Understand Export Filters and Query Strategy

Before exporting, define what data you need. Think about:

**1. Scope Dimension**:
- **Project**: Which project? (e.g., `PROJ`, `WPCW`)
- **Date Range**: Created/updated when? (e.g., last 30 days, specific quarter)
- **Status**: What states? (open only, all states, specific workflow stages)
- **Type**: What issue types? (bugs, stories, tasks, all)

**2. Quality Dimension**:
- **Assignee**: Who? (you, unassigned, specific team, all)
- **Priority**: Importance level? (high/medium/low, P0-P3)
- **Labels**: How categorized? (urgent, backend, frontend, etc.)
- **Components**: Which parts of system? (API, UI, Database, etc.)

**3. Complexity Dimension**:
- **Expansion**: Include changelog? (needed for state analysis)
- **Fields**: All fields or specific ones? (optimize for export size)
- **Pagination**: Results within limits? (avoid timeouts on large exports)

**Query Building**:

Simple query (project only):
```bash
uv run jira-tool export --project PROJ --format csv -o all_tickets.csv
```

Complex query with multiple filters:
```bash
uv run jira-tool export \
  --project WPCW \
  --status "In Progress" \
  --priority High \
  --assignee "team-member@company.com" \
  --type Bug \
  --created "2024-01-01" \
  --format json \
  -o filtered_issues.json
```

**Using Custom JQL** (most flexible):
```bash
uv run jira-tool search "project = PROJ AND created >= -30d AND labels = urgent" \
  --format csv \
  -o recent_urgent.csv
```

### Step 2: Choose the Right Export Format

Pick format based on your use case:

| Format | Command | Best For | Characteristics |
|--------|---------|----------|-----------------|
| **CSV** | `--format csv` | Excel, spreadsheets | Flat structure, easy to open, lossy |
| **JSON** | `--format json` | Human reading, processing | Full structure, pretty-printed, memory-intensive |
| **JSONL** | `--format jsonl` | Large datasets (10K+ issues) | One issue per line, streaming-friendly |
| **Table** | `--format table` | Quick console viewing | Color-coded, cannot save to file |

**Quick Decision**:
- Excel analysis → CSV
- < 1000 issues → JSON
- 1000+ issues → JSONL
- Just checking → Table

**JSONL Processing Example**:
```bash
# Count issues
wc -l issues.jsonl

# Filter with jq
jq 'select(.fields.status.name == "In Progress")' issues.jsonl > filtered.jsonl

# Python streaming (process line-by-line without loading entire file)
python3 -c "import json; \
  print(sum(1 for line in open('issues.jsonl') \
  if json.loads(line)['fields']['status']['name'] == 'In Progress'))"
```

### Step 3: Handle Pagination and Large Datasets

The Jira API limits results. You need to handle pagination for large exports.

**Problem**: Default limit is 100 issues per request

```bash
# Gets ONLY first 100
uv run jira-tool export --format json -o issues.json

# Gets 100 (limit applies!)
uv run jira-tool export --limit 50 --format json -o issues.json
```

**Solution 1: Use --all flag** (recommended)
```bash
# Gets all, handles pagination automatically
uv run jira-tool export --all --format json -o all_issues.json
```

**Solution 2: Use --limit strategically**
```bash
# Get only top 1000 (faster than --all)
uv run jira-tool export --limit 1000 --format json -o top_issues.json
```

**Solution 3: Filter to reduce results**
```bash
# Get only recent, unfinished issues (smaller subset)
uv run jira-tool search "project = PROJ AND created >= -30d AND status NOT IN (Done, Closed)" \
  --format json \
  -o recent_active.json
```

**Rule of Thumb**:
- < 1000 issues: Use `--limit` or default
- 1000-10000 issues: Use `--all` with JSONL
- > 10000 issues: Filter first, then use `--all` with JSONL

### Step 4: Export with Expanded Fields for Analysis

Some analysis requires expanded data (changelog, transitions, etc.).

**Export for State Analysis** (must have changelog):
```bash
uv run jira-tool search "project = PROJ" \
  --expand changelog \
  --format json \
  -o issues_with_history.json
```

The `--expand changelog` adds complete state transition history to each issue.

**Export for Workflow Analysis** (transitions):
```bash
uv run jira-tool search "project = PROJ" \
  --expand transitions \
  --format json \
  -o issues_with_transitions.json
```

The `--expand transitions` shows what states are available next.

**Export Multiple Expansions**:
```bash
uv run jira-tool search "project = PROJ" \
  --expand "changelog,transitions" \
  --format json \
  -o enriched.json
```

**Important**: Expanded data significantly increases file size:
- Without expand: ~5KB per issue
- With changelog: ~20-50KB per issue (can be 10x larger!)

Use filters to reduce before expanding:
```bash
# Export LAST 30 DAYS with changelog (smaller set)
uv run jira-tool search "project = PROJ AND created >= -30d" \
  --expand changelog \
  --format jsonl \
  -o recent_with_history.jsonl
```

### Step 5: Filter and Prepare Data

Export is just the first step. Transform data for analysis.

**Filter with jq** (extract open issues):
```bash
jq '.issues[] | select(.fields.status.name == "Open")' issues.json > open_issues.json
```

**Convert with Python** (JSON to CSV):
```python
import json
import csv

with open('issues.json') as f:
    data = json.load(f)

with open('issues_simple.csv', 'w', newline='') as out:
    writer = csv.DictWriter(out, fieldnames=['key', 'summary', 'status', 'priority'])
    writer.writeheader()
    for issue in data['issues']:
        writer.writerow({
            'key': issue['key'],
            'summary': issue['fields']['summary'],
            'status': issue['fields']['status']['name'],
            'priority': issue['fields']['priority']['name'] if issue['fields'].get('priority') else 'N/A'
        })
```

**Aggregate** (count by status):
```python
from collections import defaultdict
import json

with open('issues.json') as f:
    data = json.load(f)

by_status = defaultdict(int)
for issue in data['issues']:
    by_status[issue['fields']['status']['name']] += 1

for status, count in sorted(by_status.items(), key=lambda x: x[1], reverse=True):
    print(f"{status}: {count}")
```

See `references/detailed-analysis-patterns.md` for comprehensive filtering and analysis examples.

### Step 6: Analyze and Generate Insights

Quick analysis patterns:

**Status Distribution**:
```python
from collections import Counter
import json

with open('issues.json') as f:
    data = json.load(f)

statuses = Counter(issue['fields']['status']['name'] for issue in data['issues'])
for status, count in statuses.most_common():
    print(f"{status}: {count} ({count/len(data['issues'])*100:.1f}%)")
```

**Workload by Assignee**:
```python
from collections import Counter
import json

with open('issues.json') as f:
    data = json.load(f)

assignees = Counter()
for issue in data['issues']:
    assignee = issue['fields']['assignee']
    if assignee:
        assignees[assignee['displayName']] += 1

for name, count in assignees.most_common(10):
    print(f"{name}: {count}")
```

For more analysis patterns including age calculation, priority correlation, and trend analysis, see `references/detailed-analysis-patterns.md`.

### Step 7: Export for External Tools

Target specific systems:

**BI Tools** (Tableau, Power BI):
```bash
uv run jira-tool export --all --format csv -o issues_for_bi.csv
```

**Spreadsheets** (Excel, Google Sheets):
```bash
uv run jira-tool export --format csv -o team_metrics.csv
```

**Reports** (Markdown):
```python
import json

with open('issues.json') as f:
    data = json.load(f)

with open('report.md', 'w') as out:
    out.write("# Jira Export Report\n\n")
    out.write(f"Total Issues: {len(data['issues'])}\n\n")
    out.write("| Key | Summary | Status |\n")
    out.write("|-----|---------|--------|\n")
    for issue in data['issues'][:20]:
        out.write(f"| {issue['key']} | {issue['fields']['summary']} | {issue['fields']['status']['name']} |\n")
```

**Archive** (full backup):
```bash
uv run jira-tool export --all --expand "changelog,transitions" --format json -o archive_$(date +%Y%m%d).json
```

## Common Workflows

### Weekly Metrics Report

```bash
# Export and analyze in one command chain
uv run jira-tool export --project PROJ --created "-7d" --format json -o weekly.json && \
  python3 -c "import json; from collections import Counter; \
  data = json.load(open('weekly.json')); \
  statuses = Counter(i['fields']['status']['name'] for i in data['issues']); \
  print(f'Total: {len(data[\"issues\"])}'); \
  [print(f'{s}: {c}') for s, c in statuses.items()]"
```

### Archive Closed Issues

```bash
# Export with changelog for complete archive
uv run jira-tool search "status = Done AND updated <= -30d" \
  --expand changelog --format jsonl -o archived_issues.jsonl
```

### Sprint Analysis for Excel

```bash
# Export sprint data, then use Python to convert to CSV
uv run jira-tool search "sprint in openSprints()" \
  --expand changelog --format json -o sprint.json
# (CSV conversion script in references/detailed-analysis-patterns.md)
```

For complete examples including project comparison, trend analysis, and advanced workflows, see `references/detailed-analysis-patterns.md`.

## Requirements

**Core:**
- Jira Cloud instance with REST API v3 access
- Python 3.10+ (for jira-tool CLI)
- Environment variables: `JIRA_BASE_URL`, `JIRA_USERNAME`, `JIRA_API_TOKEN`

**Optional Tools:**
- `jq` for JSON processing: `brew install jq`
- Python `pandas` for advanced analysis

**Data Requirements:**
- State analysis: Export with `--expand changelog`
- Trend analysis: Use `--created` or `--updated` filters
- Large datasets: Use JSONL format

## Supporting Files

- `references/detailed-analysis-patterns.md` - Complete analysis examples, filtering patterns, and external tool integration workflows

## Related Skills

- [Design Jira State Analyzer](../design-jira-state-analyzer/SKILL.md) - Analyze state transitions and cycle time
- [Jira REST API](../jira-api/SKILL.md) - API reference for filter and expand options
- [Build Jira Document Format](../build-jira-document-format/SKILL.md) - Create formatted reports
