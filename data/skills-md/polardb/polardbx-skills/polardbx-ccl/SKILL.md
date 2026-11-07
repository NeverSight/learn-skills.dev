---
name: polardbx-ccl
description: |
  Explain, write, and review PolarDB-X Enterprise Edition CCL SQL, including template and keyword matching, account and table scope, per-CN concurrency, waiting, rejection, rule observation, and removal effects. Use for CCL syntax questions, rule reviews, unexpected matching, and throttling behavior. This is a knowledge skill; incident mitigation and CLI execution belong to a separately installed polardbx-emergency skill.
  Triggers: "CCL", "SQL throttling", "concurrency control", "CCL syntax", "CCL 语法", "限流规则", "模板限流", "关键词限流", "限流未命中", "排队超时".
metadata:
  version: "2.0.0"
---

# PolarDB-X CCL

Explain CCL semantics and produce or review SQL without executing incident interventions.

## Scope

- PolarDB-X Enterprise Edition with CN version `5.4.9-16167266` or later for ordinary CCL; slow-SQL triggers require `5.4.11-16251897` or later.
- Do not apply this syntax to Standard Edition. For version-specific advice, use supplied instance metadata or an authorized SQL connection with `SELECT VERSION();`, then confirm the edition and CN build.
- General knowledge questions do not require an instance ID or a live connection. An example is not permission to create a rule or a test resource.

## Core Workflow

1. Identify whether the request asks for an explanation, SQL review, or live intervention. Explain knowledge questions directly; generate SQL as a proposal, not as an executed change.
2. Establish the intended SQL type, table/account scope, and template or keyword filter. Use a verified template ID from SQL logs (`sql_code`), `SHOW FULL PROCESSLIST`, or `EXPLAIN`; do not invent a hash or substitute a DAS SQL ID.
3. Explain per-CN concurrency, waiting capacity, and timeout using the quick reference below. Check wildcards, keyword overmatching, overlapping rules, and node coverage. Use [the detailed reference](references/ccl-sql.md) for examples and observation fields.
4. For a live limit/removal request, use `polardbx-emergency` if installed. That separate skill owns authorization, supported CLI parameters, execution receipts, and recovery checks. If unavailable, provide the proposed SQL and state the missing execution workflow; do not improvise a write channel. Use `polardbx-diagnostics`, when available, for incident evidence rather than inferring root cause from a rule alone.

## SQL and Behavior Quick Reference

Illustrative template rule; replace all example identifiers and values using actual evidence:

```sql
CREATE CCL_RULE `example_template_rule`
ON `example_db`.`example_table`
TO 'example_user'@'%'
FOR SELECT
FILTER BY TEMPLATE('9037e5e2')
WITH MAX_CONCURRENCY=2, WAIT_QUEUE_SIZE=0, WAIT_TIMEOUT=1;
```

For a query such as `SELECT example_column FROM example_table`, replace the filter clause with `FILTER BY KEYWORD('example_column', 'example_table')`; preserve the order in which the tokens occur in the SQL. Native rules combine SQL type, table/account scope, and optional filters. Native types include SELECT, INSERT, UPDATE, and DELETE; each rule selects one type.

| Setting or command | Meaning |
|---|---|
| `MAX_CONCURRENCY` | Concurrent matching executions per CN, not QPS or a shared instance-wide quota. Set explicitly; default 0 can reject all matches. |
| `WAIT_QUEUE_SIZE` | Waiting capacity per CN; default 0. Waiting consumes thread resources. |
| `WAIT_TIMEOUT` | Queue wait in seconds, default 600; neither execution timeout nor rule TTL. |
| `FAST_MATCH` | Matching-cache switch: 0 off, 1 on; default 1. |
| `SHOW CCL_RULES;` | Inspect all rules. |
| `SHOW CCL_RULE example_template_rule;` | Inspect a named rule and its counters. |
| `DROP CCL_RULE IF EXISTS example_template_rule;` | Remove that rule; queued requests may then run. |

Below the concurrency cap, a match runs. At the cap it waits if queue capacity remains; a full queue or expired wait causes an error. Ordinary CCL does not guarantee immediate termination of in-flight work. Slow-SQL triggers are a separate mechanism that can also terminate excess slow queries.

## Best Practices

1. Distinguish native engine capabilities from management-interface parameters. The separately verified DAS create path exposes keyword filtering; this does not mean native CCL supports only keywords.
2. Preserve keyword order and verify identifier spelling against actual SQL samples. On tested build `5.7.25-TDDL-5.4.21-20260701`, keyword lists matched in SQL token order; parameter values and backtick-quoted identifiers were case-sensitive, while unquoted identifier tokens matched case-insensitively. Exact table scope also failed to match a differently cased table reference. Do not generalize these observations to every version or assume `FAST_MATCH=0` fixes them. See [version-scoped matching evidence](references/ccl-sql.md#matching-boundaries-tested-2026-10-21).
   Do not sort or lowercase the keyword list, treat it as a regex, or widen the table scope to `*` merely to make a rule match. A template filter does not bypass the rule's table/account conditions.
3. Interpret `NO.` as priority, not a DAS ItemId. Separate current running/waiting counts from cumulative match/rejection counters and use window deltas.
4. Explain retry amplification and post-removal bursts. A rule disappearing is not proof that normal business has recovered; configuration read-back alone is not proof of actual throttling.
5. Do not use `CLEAR CCL_RULES` as a substitute for removing one rule. Do not silently enable slow-SQL triggers when the user requests ordinary CCL advice.

## References

| Reference | Contents |
|---|---|
| [references/ccl-sql.md](references/ccl-sql.md) | Detailed SQL examples, matching semantics, observation fields, removal effects, and official sources. |
