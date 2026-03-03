---
name: gemini-token-optimization
description: Optimize token usage when delegating to Gemini CLI. Covers token caching, batch queries, model selection (Flash vs Pro), and cost tracking. Use when planning bulk Gemini operations.
allowed-tools: Read, Skill
---

# Gemini Token Optimization

## 🚨 MANDATORY: Invoke gemini-cli-docs First

> **STOP - Before providing ANY response about Gemini token usage:**
>
> 1. **INVOKE** `gemini-cli-docs` skill
> 2. **QUERY** for the specific token or pricing topic
> 3. **BASE** all responses EXCLUSIVELY on official documentation loaded

## Overview

Skill for optimizing cost and token usage when delegating to Gemini CLI. Essential for efficient bulk operations and cost-conscious workflows.

## When to Use This Skill

**Keywords:** token usage, cost optimization, gemini cost, model selection, flash vs pro, caching, batch queries, reduce tokens

**Use this skill when:**

- Planning bulk Gemini operations
- Optimizing costs for large-scale analysis
- Choosing between Flash and Pro models
- Understanding token caching benefits
- Tracking usage across sessions

## Token Caching

Gemini CLI automatically caches context to reduce costs by reusing previously processed content.

### Availability

| Auth Method | Caching Available |
| --- | --- |
| API key (Gemini API) | YES |
| Vertex AI | YES |
| OAuth (personal/enterprise) | NO |

### How It Works

- System instructions and repeated context are cached
- Cached tokens don't count toward billing
- View savings via `/stats` command or JSON output

### Maximizing Cache Hits

1. **Use consistent system prompts** - Same prefix increases cache reuse
2. **Batch similar queries** - Group related analysis together
3. **Reuse context files** - Same files in same order

### Monitoring Cache Usage

```bash
result=$(gemini "query" --output-format json)
total=$(echo "$result" | jq '.stats.models | to_entries | map(.value.tokens.total) | add // 0')
cached=$(echo "$result" | jq '.stats.models | to_entries | map(.value.tokens.cached) | add // 0')
billable=$((total - cached))
savings=$((cached * 100 / total))

echo "Total: $total tokens"
echo "Cached: $cached tokens ($savings% savings)"
echo "Billable: $billable tokens"
```

## Model Selection

### Model Comparison

| Model | Context Window | Speed | Cost | Quality |
| --- | --- | --- | --- | --- |
| gemini-2.5-flash | Large | Fast | Lower | Good |
| gemini-2.5-pro | Very large | Slower | Higher | Best |

### Selection Criteria

**Use Flash (`-m gemini-2.5-flash`) when:**

- Processing large files (bulk analysis)
- Simple extraction tasks
- Cost is a primary concern
- Speed is critical
- Task is straightforward

**Use Pro (`-m gemini-2.5-pro`) when:**

- Complex reasoning required
- Quality is critical
- Nuanced analysis needed
- Task requires deep understanding
- Context exceeds 1M tokens

### Model Selection Examples

```bash
# Bulk file analysis - use Flash
for file in src/*.ts; do
  gemini "List all exports" -m gemini-2.5-flash --output-format json < "$file"
done

# Security audit - use Pro for quality
gemini "Deep security analysis" -m gemini-2.5-pro --output-format json < critical-auth.ts

# Cost tracking with model info
result=$(gemini "query" --output-format json)
model=$(echo "$result" | jq -r '.stats.models | keys[0]')
tokens=$(echo "$result" | jq '.stats.models | to_entries[0].value.tokens.total')
echo "Used $model: $tokens tokens"
```

## Batching Strategy

### Why Batch?

- Reduces API overhead
- Increases cache hit rate
- Provides consistent context

### Batching Patterns

#### Pattern 1: Concatenate Files

```bash
# Instead of N separate calls
# Do one call with all files
cat src/*.ts | gemini "Analyze all TypeScript files for patterns" --output-format json
```

#### Pattern 2: Batch Prompts

```bash
# Combine related questions
gemini "Answer these questions about the codebase:
1. What is the main architecture pattern?
2. How is authentication handled?
3. What database is used?" --output-format json
```

#### Pattern 3: Staged Analysis

```bash
# First pass: Quick overview with Flash
overview=$(cat src/*.ts | gemini "List all modules" -m gemini-2.5-flash --output-format json)

# Second pass: Deep dive critical areas with Pro
echo "$overview" | jq -r '.response' | grep "auth\|security" | while read module; do
  gemini "Deep analysis of $module" -m gemini-2.5-pro --output-format json
done
```

## Cost Tracking

### Per-Query Tracking

```bash
result=$(gemini "query" --output-format json)

# Extract all cost-relevant stats
total_tokens=$(echo "$result" | jq '.stats.models | to_entries | map(.value.tokens.total) | add // 0')
cached_tokens=$(echo "$result" | jq '.stats.models | to_entries | map(.value.tokens.cached) | add // 0')
models_used=$(echo "$result" | jq -r '.stats.models | keys | join(", ")')
tool_calls=$(echo "$result" | jq '.stats.tools.totalCalls // 0')
latency=$(echo "$result" | jq '.stats.models | to_entries | map(.value.api.totalLatencyMs) | add // 0')

echo "$(date): tokens=$total_tokens cached=$cached_tokens models=$models_used tools=$tool_calls latency=${latency}ms" >> usage.log
```

### Session Tracking

```bash
# Track cumulative usage across a session
total_session_tokens=0
total_session_cached=0
total_session_calls=0

track_usage() {
  local result="$1"
  local tokens=$(echo "$result" | jq '.stats.models | to_entries | map(.value.tokens.total) | add // 0')
  local cached=$(echo "$result" | jq '.stats.models | to_entries | map(.value.tokens.cached) | add // 0')

  total_session_tokens=$((total_session_tokens + tokens))
  total_session_cached=$((total_session_cached + cached))
  total_session_calls=$((total_session_calls + 1))
}

# Use in workflow
result=$(gemini "query 1" --output-format json)
track_usage "$result"

result=$(gemini "query 2" --output-format json)
track_usage "$result"

echo "Session total: $total_session_tokens tokens ($total_session_cached cached) in $total_session_calls calls"
```

## Optimization Checklist

### Before Large Operations

- [ ] Choose appropriate model (Flash vs Pro)
- [ ] Check if caching is available (API key or Vertex)
- [ ] Plan batching strategy
- [ ] Set up usage tracking

### During Operations

- [ ] Monitor cache hit rates
- [ ] Track per-query costs
- [ ] Adjust model if quality insufficient
- [ ] Batch similar queries

### After Operations

- [ ] Review total usage
- [ ] Calculate effective cost
- [ ] Identify optimization opportunities
- [ ] Document learnings

## Quick Reference

### Cost-Saving Commands

```bash
# Use Flash for bulk
gemini "query" -m gemini-2.5-flash --output-format json

# Check cache effectiveness
gemini "query" --output-format json | jq '{total: .stats.models | to_entries | map(.value.tokens.total) | add, cached: .stats.models | to_entries | map(.value.tokens.cached) | add}'

# Minimal output (fewer output tokens)
gemini "Answer in one sentence: {question}" --output-format json
```

### Cost Estimation

Rough token estimates:

- 1 token ~ 4 characters (English)
- 1 page of code ~ 500-1000 tokens
- Typical source file ~ 200-2000 tokens

## Keyword Registry (Delegates to gemini-cli-docs)

| Topic | Query Keywords |
| --- | --- |
| Caching | `token caching`, `cached tokens`, `/stats` |
| Model selection | `model routing`, `flash vs pro`, `-m flag` |
| Costs | `quota pricing`, `token usage`, `billing` |
| Output control | `output format`, `json output` |

## Test Scenarios

### Scenario 1: Check Token Usage

**Query**: "How do I see how many tokens Gemini used?"
**Expected Behavior**:

- Skill activates on "token usage" or "gemini cost"
- Provides JSON stats extraction pattern
**Success Criteria**: User receives jq commands to extract token counts

### Scenario 2: Reduce Costs

**Query**: "How do I reduce Gemini CLI costs for bulk analysis?"
**Expected Behavior**:

- Skill activates on "cost optimization" or "reduce tokens"
- Recommends Flash model and batching
**Success Criteria**: User receives cost optimization strategies

### Scenario 3: Model Selection

**Query**: "Should I use Flash or Pro for this task?"
**Expected Behavior**:

- Skill activates on "flash vs pro" or "model selection"
- Provides decision criteria table
**Success Criteria**: User receives model comparison and recommendation

## References

Query `gemini-cli-docs` for official documentation on:

- "token caching"
- "model selection"
- "quota and pricing"

## Version History

- v1.1.0 (2025-12-01): Added Test Scenarios section
- v1.0.0 (2025-11-25): Initial release
