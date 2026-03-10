---
name: foundry-research
description: >-
  AI-powered research skill with five workflows - chat (single-model conversation),
  consensus (multi-model synthesis), thinkdeep (systematic investigation), ideate
  (creative brainstorming), and deep (multi-phase web research). Supports persistent
  threads and research sessions.
  TRIGGER when: user asks for research, consultation, brainstorming, investigation,
  or deep research. Always route through this skill — never call
  mcp__plugin_foundry_foundry-mcp__research directly.
  DO NOT TRIGGER when: a <command-name> tag is present in the current turn
  (skill already loaded), called from a subagent, simple factual questions
  answerable from context, or codebase exploration (use Explore agent instead).
---

# Research Skill

## Overview

- **Purpose:** AI-powered research with multiple reasoning strategies
- **Scope:** Five workflows, persistent thread and session management
- **Entry:** `Skill(foundry:foundry-research)` or user invocation

### Flow

> `[x?]`=decision `(GATE)`=user approval `→`=sequence

```
- **Entry** → [route?]
  - [explicit?] → Dispatch → Execute → Persist thread → Response + thread_id
  - [thread-id?] → Resume → Dispatch → Execute → Persist thread → Response + thread_id
  - [research-id?] → SessionMgmt
  - [sessions?] → ListSessions
  - [no args?] → (GATE: choose workflow) → AutoRoute → Dispatch → Execute → Persist thread → Response + thread_id
  - [deep research?] → (GATE: confirm query + params) → Start → Poll → Report (background execution)
```

**CRITICAL for `deep research` workflow:** Read [references/deep-research-workflow.md](./references/deep-research-workflow.md) before execution. Contains required polling strategy and MCP parameters.

### Deep Research Status Monitoring

Call `deep-research-status` with long-poll (`wait=true`). The server blocks until progress occurs or timeout elapses.

1. Report progress to user when each call returns.
2. Repeat until status is `completed` or `failed`.
3. If 2 consecutive responses return `"changed": false`, offer user options via AskUserQuestion (keep waiting, cancel, narrow query).

**CRITICAL — Do NOT supplement deep research with your own searches.** While deep research is running, do NOT call WebSearch, WebFetch, tavily_search, tavily_extract, or any other web/research tools. The deep research workflow handles all source gathering internally. Only use external search tools if the user **explicitly** asks you to search independently. When deep research is in the SUPERVISION phase and progress seems slow, this is normal — report status and keep polling. Do not interpret normal processing time as a failure that needs workaround.

## MCP Tooling

| Router | Actions |
|--------|---------|
| `research` | `chat`, `consensus`, `thinkdeep`, `ideate`, `deep-research`, `deep-research-status`, `deep-research-report`, `deep-research-list`, `deep-research-delete`, `deep-research-evaluate`, `thread-list`, `thread-get`, `thread-delete`, `node-execute`, `node-record`, `node-status`, `node-findings` |

## MCP Contract

| Action | Required | Optional | Errors |
|--------|----------|----------|--------|
| `chat` | `prompt` | `thread_id`, `provider_id` | `THREAD_NOT_FOUND` |
| `consensus` | `prompt` | `providers`, `strategy` | `NO_MODELS_AVAILABLE` |
| `thinkdeep` | `prompt` | `thread_id`, `depth` | `MAX_DEPTH_EXCEEDED` |
| `ideate` | `prompt` | `thread_id`, `phase` | `INVALID_PHASE` |
| `deep-research` | `query` | `max_iterations`, `max_sub_queries`, `max_sources_per_query`, `follow_links` | `RESEARCH_TIMEOUT` |
| `deep-research-status` | `research_id` | - | `RESEARCH_NOT_FOUND` |
| `deep-research-report` | `research_id` | - | `RESEARCH_NOT_FOUND` |
| `deep-research-list` | - | `limit`, `completed_only` | - |
| `deep-research-delete` | `research_id` | - | `RESEARCH_NOT_FOUND` |
| `deep-research-evaluate` | `research_id` | - | `RESEARCH_NOT_FOUND` |
| `thread-*` | `thread_id` | `limit` | `THREAD_NOT_FOUND` |
| `node-status` | `spec_id`, `research_node_id` | - | `NODE_NOT_FOUND` |
| `node-execute` | `spec_id`, `research_node_id` | `prompt` | `NODE_NOT_FOUND`, `INVALID_TYPE` |
| `node-record` | `spec_id`, `research_node_id`, `result` | `summary`, `key_insights`, `recommendations`, `confidence` | `NODE_NOT_FOUND` |
| `node-findings` | `spec_id`, `research_node_id` | - | `NODE_NOT_FOUND`, `NO_FINDINGS` |

## Workflow Selection

| Signal | Workflow |
|--------|----------|
| Follow-up, iteration | `chat` |
| Multiple perspectives | `consensus` |
| Complex problem | `thinkdeep` |
| Brainstorming | `ideate` |
| Comprehensive research, multiple sources | `deep research` |

## User Gates

- No args: workflow selection
- Ambiguous: clarify before auto-route
- Consensus: strategy selection
- Ideate: phase transition
- Deep: **pre-launch query confirmation**, then progress updates during background execution

## Output Formats

| Workflow | Response |
|----------|----------|
| `chat` | `{response, thread_id, model}` |
| `consensus` | `{responses[], synthesis, strategy}` |
| `thinkdeep` | `{findings[], confidence, thread_id}` |
| `ideate` | `{ideas[], phase, selected[]}` |
| `deep research` | `{research_id, status, report{summary, findings[], sources[], topic_research_results[], contradictions[], content_fidelity, evaluation}}` |

## References

- [Chat](./references/chat-workflow.md) | [Consensus](./references/consensus-workflow.md) | [Deep](./references/deep-research-workflow.md)
- [ThinkDeep](./references/thinkdeep-workflow.md) | [Ideate](./references/ideate-workflow.md)
- [Sessions](./references/session-management.md) | [Auto-Route](./references/auto-routing.md)
