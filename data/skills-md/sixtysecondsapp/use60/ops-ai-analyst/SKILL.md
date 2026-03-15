---
name: Ops AI Analyst
description: |
  Run natural language queries on Ops table data and generate AI-powered insights.
  Use when a user asks "query my table", "find leads where", "analyze this table",
  "show insights", "who are the best leads", or needs to search, filter, or analyze
  their ops table data using plain English questions.
  Returns filtered query results and AI-generated analytical insights.
metadata:
  author: sixty-ai
  version: "2"
  category: data-access
  skill_type: atomic
  is_active: true
  context_profile: sales
  agent_affinity:
    - prospecting
    - research
  triggers:
    - pattern: "query my table"
      intent: "ai_query_ops_table"
      confidence: 0.85
      examples:
        - "query this table"
        - "search my table"
        - "run a query on the table"
        - "ask the table"
    - pattern: "find leads where"
      intent: "ai_query_ops_table"
      confidence: 0.90
      examples:
        - "find leads with"
        - "show me leads who"
        - "which leads have"
        - "filter leads by"
    - pattern: "analyze table"
      intent: "get_ops_insights"
      confidence: 0.85
      examples:
        - "analyze this table"
        - "analyze my data"
        - "what patterns do you see"
        - "give me an analysis"
    - pattern: "show insights"
      intent: "get_ops_insights"
      confidence: 0.85
      examples:
        - "show me insights"
        - "table insights"
        - "what can you tell me about this data"
        - "any interesting patterns"
    - pattern: "who are the best leads"
      intent: "ai_query_ops_table"
      confidence: 0.85
      examples:
        - "who should I reach out to first"
        - "rank my leads"
        - "top prospects"
        - "best leads to contact"
  keywords:
    - "query"
    - "find"
    - "search"
    - "analyze"
    - "insights"
    - "filter"
    - "leads"
    - "pattern"
    - "best"
    - "top"
    - "where"
  required_context: []
  optional_context:
    - table_id
    - table_name
  inputs:
    - name: table_id
      type: string
      description: "ID of the ops table to query or analyze"
      required: false
    - name: query
      type: string
      description: "Natural language query to run against the table data"
      required: false
  outputs:
    - name: query_results
      type: object
      description: "Filtered rows matching the natural language query"
    - name: insights
      type: object
      description: "AI-generated insights about the table data including patterns, distributions, and recommendations"
  requires_capabilities:
    - ops_tables
  execution_mode: sync
  timeout_ms: 30000
  priority: high
  tags:
    - ops
    - AI
    - analytics
    - prospecting
    - query
---

## Available Context
@_platform-references/org-variables.md

# Ops AI Analyst

## Goal

Enable sales reps to ask natural language questions about their Ops table data and receive AI-powered insights. Instead of manually scrolling through rows or building complex filters, reps can ask questions like "who are my highest-scoring VP-level leads?" or "show me companies in fintech with more than 100 employees" and get instant answers.

This skill bridges the gap between structured data and conversational interaction -- making ops tables feel like talking to a smart analyst who knows your prospect database inside out.

## Required Capabilities
- **Ops Tables**: Access to AI query and insights APIs

## Inputs
- `table_id`: ID of the ops table to query or analyze
- `query`: Natural language question to ask about the data (e.g., "Which leads are VPs at companies with 50+ employees?")

## Instructions

### Natural Language Queries

When the user asks a question about their table data:

1. Identify the target table. If not specified, check if there's a table in the current conversation context.
2. Formulate the query from the user's question. Pass it as-is -- the AI query engine handles natural language natively.
3. Call `execute_action("ai_query_ops_table", { table_id: "<id>", query: "<user's question>" })`
4. Present results in a clean format:
   - Show the matching rows in a scannable table
   - Include the total count: "Found 12 leads matching your query"
   - Highlight the relevant columns that the query is filtering on
5. Suggest follow-up actions: "Want me to enrich these leads? Or narrow the search further?"

### Common Query Patterns

Help the user by understanding these natural patterns:

| User Says | Query Intent |
|-----------|-------------|
| "Find leads at enterprise companies" | Filter by company size |
| "Who has a VP or Director title?" | Filter by title/seniority |
| "Show leads we haven't emailed yet" | Filter by empty email status column |
| "Which companies are in healthcare?" | Filter by industry |
| "Top 10 leads by score" | Sort + limit |
| "Leads added this week" | Filter by date |
| "Companies with more than 200 employees" | Filter by size threshold |

### AI Insights

When the user wants broader analysis:

1. Call `execute_action("get_ops_insights", { table_id: "<id>" })`
2. Present the insights in a structured format covering:
   - **Data quality**: Completeness of columns, missing data patterns
   - **Distribution**: Industry breakdown, title seniority mix, company size spread
   - **Patterns**: Clusters, commonalities among high-scoring leads
   - **Recommendations**: Which segments to prioritize, gaps to fill, enrichment suggestions
3. Make insights actionable: each insight should connect to a next step

### Combining Queries with Actions

After showing query results, proactively suggest relevant next steps:
- "Want me to add these 12 leads to a separate table?"
- "Should I enrich the company data for these results?"
- "Want me to start a sequence for the top 5?"

## Available Actions

| Action | Parameters | Returns |
|--------|-----------|---------|
| `ai_query_ops_table` | `{ table_id: string, query: string }` | Matching rows with relevance context |
| `get_ops_insights` | `{ table_id: string }` | AI-generated insights about the data |

## Output Format

### Query Results
```
QUERY: "VP or Director level leads at companies with 50+ employees"
FOUND: 12 leads

Name              Title              Company         Size    Score
Sarah Chen        VP Engineering     TechFlow        120     92
James Park        Director Sales     DataBridge      85      88
Maria Garcia      VP Product         CloudScale      200     85
Lisa Wong         Director Ops       FinServ Inc     150     81
...

Showing top 12 results. Want to narrow this further or take action on these leads?
```

### Insights Response
```
TABLE INSIGHTS: Lead Prospects (142 rows)

DATA QUALITY
  Overall completeness: 78%
  Missing emails: 23 rows (16%)
  Missing titles: 8 rows (6%)

DISTRIBUTION
  Top industries: SaaS (34%), Fintech (22%), Healthcare (15%)
  Seniority: VP+ (28%), Director (31%), Manager (24%), IC (17%)
  Company size: 1-50 (18%), 51-200 (45%), 201-500 (27%), 500+ (10%)

PATTERNS
  High-scoring leads (80+) are concentrated in SaaS and Fintech
  VP-level contacts have 2.3x higher engagement scores
  Companies with 51-200 employees show the strongest response rates

RECOMMENDATIONS
  1. Prioritize the 18 VP+ leads in SaaS -- highest score cluster
  2. Enrich the 23 rows missing email addresses before outreach
  3. Consider adding more Healthcare leads -- strong scores but small sample
```

## Error Handling

### Ambiguous query
If the query is too vague to produce useful results: "That's a broad query -- could you be more specific? For example: 'Find leads with VP titles at fintech companies' or 'Show companies with over 100 employees.'"

### No results
If the query returns zero matches: "No leads match that query. Here's what I see in the table: [brief summary of data distribution]. Want to try a different filter?"

### Table too small for insights
If the table has fewer than 10 rows: "This table only has X rows -- not enough data for meaningful statistical insights. Want me to help add more leads first?"

### Query on empty table
If the table has no data: "This table is empty. Let me help you populate it first -- I can import from Apollo, HubSpot, or add leads manually."

## Guidelines
- Pass the user's natural language query directly to the AI query engine -- don't try to pre-process it into SQL or filters
- When showing query results, only display the most relevant columns (max 5-6) to keep output scannable
- Always include the total count of matches, even when paginating
- For insights, focus on actionable patterns, not just statistics -- "VP leads score 2x higher" is better than "average VP score is 84"
- Suggest next steps after every query -- queries should lead to action, not just information
- If the user asks a follow-up question, maintain the table context from the previous query
