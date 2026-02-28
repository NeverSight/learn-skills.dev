---
name: perplexity-search
description: A skill for performing web searches, research, and reasoning using the Perplexity API. Handles real-time web information retrieval, deep research analysis, and advanced reasoning tasks. Use when the user asks for web searches, research, or says things like "look up", "search for", "latest information", "research", or "analyze".
---

# Perplexity Search Skill

A skill for executing real-time web searches and research using the Perplexity API.

## Purpose

This skill provides the following capabilities:

1. **perplexity_ask** - Answer general questions (using sonar-pro model)
2. **perplexity_research** - Deep research and comprehensive reports (using sonar-deep-research model)
3. **perplexity_reason** - Advanced reasoning and analysis (using sonar-reasoning-pro model)
4. **perplexity_search** - Retrieve web search results

## When to Use

Use this skill in the following situations:

- User needs up-to-date information
- Received a question requiring web search
- Asked to perform deep research or investigation
- Complex analysis or reasoning is required
- Keywords like "look up", "search for", "latest..." are included

## Prerequisites

- `PERPLEXITY_API_KEY` environment variable must be set
- Internet connection must be available

## Usage

### Basic Usage

Use the `scripts/perplexity_api.py` script to call the API.

```bash
# General questions (ask)
python3 scripts/perplexity_api.py ask "your question"

# Deep research (research)
python3 scripts/perplexity_api.py research "research topic"

# Advanced reasoning (reason)
python3 scripts/perplexity_api.py reason "reasoning task"

# Web search (search)
python3 scripts/perplexity_api.py search "search query" [--max-results 10] [--country JP]
```

### Command Options

#### ask / research / reason
- First argument: question, research topic, or reasoning task
- `--strip-thinking`: Remove `<think>...</think>` tags to save context tokens (research/reason only)

#### search
- First argument: search query
- `--max-results`: Maximum number of results to return (1-20, default: 10)
- `--max-tokens-per-page`: Maximum tokens per page (256-2048, default: 1024)
- `--country`: ISO code for regional results (e.g., JP, US, GB)

## Workflow

### Standard Search Flow

1. Analyze the user's question and select the appropriate tool
   - Simple questions → `ask`
   - Deep research → `research`
   - Complex analysis → `reason`
   - Information gathering → `search`

2. Execute the script to call the API

3. Present results to the user, citing sources when available

### Tool Selection Guidelines

| Use Case | Tool | Description |
|----------|------|-------------|
| Current weather, news | ask | When quick answers are needed |
| Technical topic research | research | When comprehensive analysis is needed |
| Complex problem analysis | reason | When logical reasoning is needed |
| Collecting sources | search | When URLs or snippets are needed |

## API Details

For detailed API specifications, see `references/api_reference.md`.

## Troubleshooting

- **API Key Error**: Verify the `PERPLEXITY_API_KEY` environment variable
- **Timeout**: Increase `PERPLEXITY_TIMEOUT_MS` (default: 300000ms)
- **Proxy Issues**: Set `PERPLEXITY_PROXY` or `HTTPS_PROXY`
