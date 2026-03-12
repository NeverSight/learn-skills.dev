---
name: n8n-v2
description: Comprehensive n8n v2.0 reference for building workflow automation. Use this skill when working with n8n workflows, especially for (1) creating workflow JSON files for import, (2) implementing human-in-the-loop approval workflows with Wait nodes, (3) troubleshooting Execute Sub-Workflow node issues, (4) setting up API credentials (LinkedIn, Anthropic, NewsAPI), (5) building orchestrator patterns with sub-workflows, (6) using expressions in nodes, (7) understanding MCP server limitations, or (8) any n8n workflow development task.
---

# n8n v2.0 Workflow Development

## Overview

Comprehensive reference for building n8n workflows using v2.0 patterns and best practices. This skill provides complete documentation for nodes, expressions, patterns, troubleshooting, and production-ready examples.

---

## Quick Start Guide

### 1. Test APIs First
```bash
curl -X GET "https://api.example.com/endpoint" \
  -H "Authorization: Bearer $TOKEN"
```

### 2. Create Workflow JSON
Generate workflow JSON with nodes and connections.

### 3. Import into n8n
n8n UI > Settings > Import from File

### 4. Configure & Fix
- Replace Execute Sub-Workflow nodes (if needed)
- Configure credentials
- Test each node

### 5. Test Execution
Use MCP server `mcp__n8n__execute_workflow` or manual trigger

---

## Core Concepts

### n8n MCP Server Integration

**What it CAN do:**
- ✅ Search workflows
- ✅ View workflow details
- ✅ Execute workflows

**What it CANNOT do:**
- ❌ Create workflows
- ❌ Modify workflows
- ❌ Manage credentials

**Workaround:** Generate JSON files, import via UI

📖 **Deep dive:** [references/mcp-limitations.md](references/mcp-limitations.md)

---

### Node Library

Complete reference for all n8n nodes:

**Trigger Nodes:** Manual Trigger, Execute Workflow Trigger
**Data Processing:** Code, Set, Merge, Filter, Split in Batches
**Flow Control:** IF, Wait
**Integration:** HTTP Request, RSS Feed Read
**Action:** Execute Workflow, Respond to Webhook

Each node documented with configuration examples, parameters, and patterns.

📖 **Complete reference:** [references/node-library.md](references/node-library.md)

---

### Expression Syntax

Dynamic values in node parameters using `={{ expression }}`:

```javascript
{{ $json.field }}                      // Current item
{{ $('Node Name').first().json.field }} // Cross-node
{{ $json.url || 'default' }}           // Fallback
{{ new Date().toISOString() }}         // Date/time
`urn:li:person:${$json.sub}`          // Template literal
```

📖 **Complete guide:** [references/expression-syntax.md](references/expression-syntax.md)

---

## Common Workflows

### Human-in-the-Loop Approval

Use **Wait nodes** with forms (NOT respondToWebhook):

```
Trigger → Generate Content → Wait Node (form) → IF → Action
```

📖 **Complete patterns:** [references/wait-nodes-guide.md](references/wait-nodes-guide.md)

---

### Multi-Workflow Orchestration

Orchestrator coordinates sub-workflows:

```
Main Orchestrator
├── Trigger
├── Execute Sub-Workflow: Data Fetcher
├── Wait Node: Review
├── Execute Sub-Workflow: Processor
└── Execute Sub-Workflow: Output
```

📖 **All patterns:** [references/workflow-patterns.md](references/workflow-patterns.md)

---

### News Aggregation

Multi-source data fetch, normalize, merge, deduplicate, rank:

```
Trigger
├── HTTP Request: Source 1 → Normalize
├── HTTP Request: Source 2 → Normalize
└── RSS Feed: Source 3 → Normalize
    → Merge → Deduplicate → Rank
```

📖 **Detailed patterns:** [references/workflow-patterns.md](references/workflow-patterns.md#news-aggregation-pattern)

---

### AI Content Generation

Sub-workflow pattern for AI content:

```
Execute Workflow Trigger
→ Code: Build Prompt
→ HTTP Request: AI API
→ Code: Extract Response
```

📖 **Implementation:** [references/workflow-patterns.md](references/workflow-patterns.md#content-generation-with-ai-pattern)

---

## Critical Issues & Solutions

### Execute Sub-Workflow "Out of Date" Error

**Problem:** Imported nodes show error after import

**Solution:**
1. Delete old Execute Sub-Workflow nodes
2. Add fresh nodes from palette
3. Select "Database" and choose workflow

📖 **Detailed troubleshooting:** [references/execute-sub-workflow-issues.md](references/execute-sub-workflow-issues.md)

---

### Wait Node Not Pausing

❌ **Wrong:** respondToWebhook, Set nodes, IF on unset fields
✅ **Correct:** Wait node with `resume: "form"`

📖 **Complete guide:** [references/wait-nodes-guide.md](references/wait-nodes-guide.md)

---

### LinkedIn `unauthorized_scope_error`

❌ Turn OFF both: "Organization Support" and "Legacy" toggles

📖 **All auth issues:** [references/api-credentials.md](references/api-credentials.md)

---

## Templates & Examples

### Basic Templates

Starting points for common structures:

- `assets/templates/wait-node-approval-template.json`
- `assets/templates/orchestrator-template.json`
- `assets/templates/sub-workflow-template.json`

---

### Complete Workflow Examples

Production-ready workflows you can import and use:

- **News Aggregation** - Multi-source fetch, normalize, deduplicate, rank
  `assets/examples/news-aggregation-workflow.json`

- **Content Generation** - AI-powered content creation sub-workflow
  `assets/examples/content-generation-workflow.json`

- **LinkedIn Member ID** - Retrieve your LinkedIn member URN
  `assets/examples/linkedin-member-id-workflow.json`

- **Multi-Source Deduplication** - Merge and deduplicate pattern
  `assets/examples/multi-source-deduplication-workflow.json`

---

## Code Snippet Library

Reusable JavaScript for Code nodes:

- **Deduplication** - Remove duplicates by URL, title, ID, or multiple fields
  `code-snippets/deduplication.js`

- **Ranking Algorithms** - Multi-factor ranking (relevance, recency, engagement)
  `code-snippets/ranking-algorithms.js`

- **Data Normalization** - Unify data from different API sources
  `code-snippets/data-normalization.js`

- **Form Data Preparation** - Format data for Wait node forms
  `code-snippets/form-data-preparation.js`

- **Cross-Node Data Access** - Reference data from other nodes
  `code-snippets/cross-node-data-access.js`

---

## API Credentials Quick Reference

**LinkedIn OAuth2:**
- Scopes: `openid`, `profile`, `w_member_social`
- ❌ OFF: Organization Support, Legacy
- URN format: `urn:li:person:{id}`

**Anthropic API:**
- Header: `x-api-key`
- Model: `claude-3-5-sonnet-20241022`
- Temp: 0.7, Max tokens: 400

**NewsAPI:**
- Header: `X-Api-Key`
- Endpoints: `/v2/everything`, `/v2/top-headlines`
- Free tier: 100 requests/day

📖 **Complete setup:** [references/api-credentials.md](references/api-credentials.md)

---

## Reference Documentation

### Core References
- [node-library.md](references/node-library.md) - Comprehensive node documentation
- [expression-syntax.md](references/expression-syntax.md) - Complete expression guide
- [workflow-patterns.md](references/workflow-patterns.md) - Common workflow architectures
- [wait-nodes-guide.md](references/wait-nodes-guide.md) - Human-in-the-loop patterns
- [api-credentials.md](references/api-credentials.md) - Authentication setup
- [mcp-limitations.md](references/mcp-limitations.md) - MCP server constraints
- [execute-sub-workflow-issues.md](references/execute-sub-workflow-issues.md) - Sub-workflow troubleshooting
- [troubleshooting.md](references/troubleshooting.md) - Common issues and solutions

---

## Official n8n Documentation

- [n8n Documentation](https://docs.n8n.io/)
- [Execute Sub-Workflow Node](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.executeworkflow/)
- [Sub-workflows Guide](https://docs.n8n.io/flow-logic/subworkflows/)
- [Wait Node](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.wait/)
