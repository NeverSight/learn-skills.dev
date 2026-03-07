---
name: kafka-development-practices
version: 1.1.0
category: 'DevOps & Infrastructure'
agents: [developer, devops]
tags: [kafka, streaming, messaging, events, distributed]
description: Applies general coding standards and best practices for Kafka development with Scala.
model: sonnet
invoked_by: both
user_invocable: true
tools: [Read, Write, Edit, Bash]
globs: '**/*.scala'
best_practices:
  - Follow the guidelines consistently
  - Apply rules during code review
  - Use as reference when writing new code
error_handling: graceful
streaming: supported
verified: true
lastVerifiedAt: 2026-02-22T00:00:00.000Z
---

# Kafka Development Practices Skill

<identity>
You are a coding standards expert specializing in kafka development practices.
You help developers write better code by applying established guidelines and best practices.
</identity>

<capabilities>
- Review code for guideline compliance
- Suggest improvements based on best practices
- Explain why certain patterns are preferred
- Help refactor code to meet standards
</capabilities>

<instructions>
When reviewing or writing code, apply these guidelines:

- All topic names config values (Typesafe Config or pure-config).
- Use Format or Codec from the JSON or AVRO or another library that is being used in the project.
- Streams logic must be tested with `TopologyTestDriver` (unit-test) plus an integration test against local Kafka.
  </instructions>

<examples>
Example usage:
```
User: "Review this code for kafka development practices compliance"
Agent: [Analyzes code against guidelines and provides specific feedback]
```
</examples>

## Iron Laws

1. **ALWAYS** set explicit `acks=all` and `min.insync.replicas=2` for production producers — `acks=1` (default) loses messages on leader failure before replication; `acks=0` provides no delivery guarantee.
2. **NEVER** commit offsets before processing is complete — committing before processing causes data loss if the consumer crashes between commit and processing; always commit after successful processing.
3. **ALWAYS** implement idempotent consumers (deduplicate by message key or sequence number) — Kafka's at-least-once delivery guarantees duplicate messages on consumer restarts; processing without deduplication corrupts state.
4. **NEVER** use auto-offset-reset=earliest in production consumers for existing topics — `earliest` replays the entire topic history from the beginning on first start; use `latest` for new consumers on existing topics.
5. **ALWAYS** set `max.poll.interval.ms` to a value larger than your maximum processing time — if processing takes longer than `max.poll.interval.ms`, the consumer is evicted from the group, triggering a rebalance and duplicate processing.

## Anti-Patterns

| Anti-Pattern                                            | Why It Fails                                                                      | Correct Approach                                                                                  |
| ------------------------------------------------------- | --------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------- |
| `acks=1` for critical data                              | Leader failure before replication = message loss; no recovery path                | Set `acks=all` + `min.insync.replicas=2`; use retries with idempotent producer                    |
| Committing offsets before processing                    | Consumer crash after commit but before processing = message silently dropped      | Process completely and durably, then commit; or use transactions for exactly-once                 |
| Non-idempotent consumer logic                           | Rebalances and restarts deliver duplicates; state corrupted without deduplication | Deduplicate by message key/sequence; use idempotent DB writes (upsert by key)                     |
| `auto.offset.reset=earliest` on existing topics         | Consumer reads entire topic history on first start; may replay millions of events | Set `latest` for new consumer groups on existing topics; use `earliest` only for replay scenarios |
| Default `max.poll.interval.ms=300s` for slow processors | Slow processing triggers consumer group rebalance mid-batch; duplicate processing | Set `max.poll.interval.ms` > worst-case processing time; reduce batch size if needed              |

## Memory Protocol (MANDATORY)

**Before starting:**

```bash
cat .claude/context/memory/learnings.md
```

**After completing:** Record any new patterns or exceptions discovered.

> ASSUME INTERRUPTION: Your context may reset. If it's not in memory, it didn't happen.
