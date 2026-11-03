---
name: kafka-consumer-lag
description: Analyse Kafka consumer group lag using the Lenses MCP server. Diagnoses lag causes (throughput bottlenecks, rebalancing, partition skew, stalled consumers) and suggests remediation. Use when user says "check consumer lag", "why are consumers slow", "lag report" or asks about consumer group health or offset progress. Do NOT use for resetting offsets or managing consumer groups.
license: MIT
allowed-tools: Read, Grep, Glob, Bash, mcp__Lenses__list_consumer_groups, mcp__Lenses__list_consumer_groups_by_topic, mcp__Lenses__get_topic_partitions, mcp__Lenses__get_dataset_message_metrics, mcp__Lenses__execute_sql
argument-hint: "[required: environment name] [optional: topic name to filter by]"
compatibility: Recommended - the Lenses MCP server (lenses-mcp) connected and configured with a valid environment. Any Kafka MCP that exposes an equivalent tool surface (list_consumer_groups, get_consumer_group, etc.) will also work; without an MCP server, the skill falls back to codebase-only inspection and skips live-cluster checks.
metadata:
  author: Tun Shwe
  version: 1.0.0
  mcp-server: lenses-mcp
  category: mcp-enhancement
  approach: problem-first
  patterns: sequential-workflow, domain-intelligence
  tags: [kafka, consumers, lag, monitoring, diagnostics]
---

# Kafka Consumer Lag Analysis

Analyses consumer group lag across all groups and diagnoses potential causes. Consumer lag is the most commonly monitored Kafka metric and the first thing engineers check during incidents.

Target environment: $ARGUMENTS

## Workflow

Copy this checklist and track your progress:

```
Lag Analysis Progress:
- [ ] Step 1: Fetch all consumer groups
- [ ] Step 2: Identify problematic groups
- [ ] Step 3: Diagnose root causes
- [ ] Step 4: Generate report
```

1. **Fetch all consumer groups** with state and lag info
2. **Identify problematic groups** (high lag, idle, rebalancing)
3. **Diagnose root causes** using partition and throughput data
4. **Report findings** with per-group remediation steps

## Step 1: Fetch Consumer Groups

Use the Lenses MCP `list_consumer_groups` tool to get all consumer groups with:
- Group state (Stable, Rebalancing, Empty, Dead)
- Lag per topic-partition
- Active member count
- Coordinator info

For topic-specific analysis, use `list_consumer_groups_by_topic` to narrow the scope.

Expected output: List of all consumer groups with state, lag and member count.

**Validation**: If no consumer groups are returned, report this finding and stop - the cluster may have no active consumers.

## Step 2: Identify Problematic Groups

Flag consumer groups in these categories:

### Critical
- Groups in **Dead** or **Empty** state with committed offsets (consumer has stopped)
- Groups with lag growing over time (compare current lag against partition end offsets using `get_topic_partitions`)

### Warning
- Groups in **Rebalancing** state (consumption paused)
- Groups with uneven partition assignment (some consumers have significantly more partitions than others)
- Groups with no committed offsets (consumer may never have started successfully)

### Suggestion
- Groups with very high member count relative to partition count (idle consumers)
- Groups consuming from topics with no recent messages (use `get_dataset_message_metrics` to check producer throughput)

## Step 3: Diagnose Root Causes

For each problematic group, determine the likely cause:

### Growing Lag + Stable Producer Rate
- Consumer throughput bottleneck
- **Remediation**: Scale consumers, increase `max.poll.records`, reduce processing time per message, check for synchronous blocking calls

### Lag Spikes + Rebalancing
- Rebalancing is pausing consumption
- **Remediation**: Switch to cooperative sticky assignor, increase `session.timeout.ms`, reduce `max.poll.interval.ms` risk

### Single-Partition Lag (others are fine)
- Hot partition / key skew
- **Remediation**: Review partitioning strategy, check for hot keys, consider custom partitioner

### All Partitions Lagging Equally
- Overall consumer slowness
- **Remediation**: Profile consumer processing, check for external dependencies (database, API calls), increase consumer instances

### Zero Lag but Empty Group
- Consumer crashed or was decommissioned
- **Remediation**: Check consumer process health, restart if needed, clean up stale groups

## Step 4: Verify Data Flow

Use the Lenses MCP `execute_sql` tool to sample recent messages from lagging topics:
```sql
SELECT * FROM {topic} LIMIT 5
```
This confirms the topic has active producers and messages are flowing.

## Success Criteria

### Quantitative
- Triggers on 90% of lag-related queries (test with 10-20 varied phrasings)
- Completes analysis in under 12 MCP tool calls
- 0 failed MCP calls per run

### Qualitative
- Each flagged group has a specific diagnosis and remediation
- Report distinguishes symptom from root cause
- Consistent results when re-run on the same environment

## Examples

### Example 1: Incident investigation

User says: "Consumers are falling behind, check the lag"

Actions:
1. Fetch all consumer groups for the environment
2. Sort by total lag descending to find the worst offenders
3. Diagnose root causes for each critical group
Result: Prioritised report with per-group diagnosis and remediation

### Example 2: Topic-specific lag check

User says: "Check consumer lag for orders.payment.completed"

Actions:
1. Use `list_consumer_groups_by_topic` to get groups consuming from that topic
2. Check partition-level lag distribution
3. Verify data flow with `execute_sql`
Result: Focused report on a single topic's consumer groups

### Example 3: Stale group cleanup

User says: "Find any dead or empty consumer groups"

Actions:
1. Fetch all consumer groups
2. Filter for Dead or Empty state with committed offsets
3. Report stale groups that can be safely cleaned up
Result: List of candidate groups for deletion

## Troubleshooting

### Consumer groups list is empty
Cause: No consumer groups exist in the environment or permissions are restricted.
Solution: Verify consumers are running. Check Lenses agent permissions allow listing consumer groups.

### Lag numbers seem incorrect
Cause: Consumer group offsets may be stale if the consumer recently stopped.
Solution: Compare lag against partition end offsets from `get_topic_partitions`. Note when offsets were last committed.

### execute_sql returns no data
Cause: Topic is empty or has very old messages beyond the query window.
Solution: Use `get_dataset_message_metrics` to check if the topic has recent throughput. An empty topic with lagging consumers indicates a producer issue.

## Output Format

```
## Consumer Lag Report

### Environment: {name}

### Critical (immediate action)
| Consumer Group | Topic | Total Lag | State | Diagnosis | Remediation |
|---------------|-------|-----------|-------|-----------|-------------|
| group-name | topic | 50000 | Stable | Throughput bottleneck | Scale consumers |

### Warning (investigate)
| Consumer Group | Topic | Total Lag | State | Diagnosis | Remediation |
|---------------|-------|-----------|-------|-----------|-------------|

### Suggestion (optimise)
| Consumer Group | Topic | Total Lag | State | Diagnosis | Remediation |
|---------------|-------|-----------|-------|-----------|-------------|

### Summary
- X consumer groups analysed
- Y groups with critical lag
- Z groups with warnings
- Stale/empty groups: N
```
