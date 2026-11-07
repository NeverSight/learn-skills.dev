---
name: sql-review
description: |
  Scan codebase for table schemas (DDL) and SQL statements, create a PolarDB-X test instance with mock data, analyze index usage via EXPLAIN, and provide index optimization recommendations. Works with any language/framework.
  Use when user says "sql review", "SQL审查", "索引分析", "索引推荐", "index review", "SQL优化", "检查索引", "review sql", "分析SQL", "explain分析", "慢查询分析", "sql performance".
metadata:
  version: 0.5.1
---

# SQL Review - Index Analysis & Recommendations

Scan codebase for DDL and SQL queries, create tables on a PolarDB-X test instance, populate mock data, analyze index usage via EXPLAIN, and output optimization recommendations.

## Prerequisites

- `curl` must be available (for PolarDB-X Zero API calls to create/destroy instances)
- `mysql` CLI client must be available (to connect and execute SQL)
- If `mysql` is not available, prompt the user to install it (brew install mysql-client / apt install mysql-client / scoop install mysql)
- If user chooses **Aliyun instance mode**, `aliyun` CLI must be available and configured with valid credentials (`aliyun configure list`)
- All temporary files use the `sql_review_` prefix. `$TMPDIR` in this document refers to a writable temp directory — determine the appropriate path for the current OS (e.g. `/tmp` on Linux/macOS, `%TEMP%` on Windows)

## Progress File

**Critical for long sessions**: Initialize `$TMPDIR/sql_review_progress.md` at the start of Step 2 and **append incrementally** throughout the entire workflow.

- After scanning each mapper/table (Step 2): append that table's SQL inventory immediately.
- After EXPLAIN analysis per table (Step 5): append that table's EXPLAIN results and recommended DDL immediately.
- In Step 6 (Report): read the progress file as the **single source of truth** to assemble the final report.

**Rule**: Never batch multiple tables before saving. Process one table, save results, then move to the next. This prevents loss of work if the agent session runs out of context.

## Workflow

Track progress on the following steps. Each step has a dedicated reference file — **Read it when starting the step**, then discard after completion.

### Step 1-2: Confirm Scope & Scan Codebase

Confirm scan scope and database edition with the user, detect framework (MyBatis auto-detection), then collect all DDL and SQL statements via multi-round search. For MyBatis projects, extract SQL from XML mapper tags and generate multi-path variants for dynamic WHERE queries.

Scan scope options: **Full repository**, **Specific module/directory**, **Recent Git commits**, or **Aliyun instance** (collect SQL insights and slow queries via `aliyun` CLI, no codebase needed).

- If user selects **Aliyun instance**: skip code scanning, execute the **Aliyun collection path** instead.
- Otherwise: proceed with standard code scanning.

**Read [references/step-scan.md](references/step-scan.md) for detailed instructions.**

### Step 2: Aliyun Data Source Collection (Aliyun mode only)

Verify `aliyun` CLI availability, collect instance info from user, retrieve DDL from the instance, fetch SQL insight statistics (DAS API), slow query records, and optionally SQL audit logs (SLS API). Merge and deduplicate results, save to progress file with execution frequency and latency metrics.

**Read [references/step-aliyun.md](references/step-aliyun.md) for detailed instructions.**

### Step 3: Name Anonymization

Build randomized name mapping for all tables, columns, indexes (and MyBatis statement IDs). Persist mapping file. Transform all SQL to use anonymous names.

**Read [references/step-anonymize.md](references/step-anonymize.md) for detailed instructions.**

### Step 4: Test Instance Setup

Analyze data characteristics from code, create PolarDB-X test instance, create tables with anonymized DDL, and populate mock data via stored procedures.

**Read [references/step-instance.md](references/step-instance.md) for detailed instructions.**

### Step 5: EXPLAIN Analysis

Run EXPLAIN on each query (and each variant for multi-path queries). For problematic queries, explore multiple candidate indexes via CREATE -> EXPLAIN -> DROP cycles. Cross-validate indexes against all variants.

**Read [references/step-explain.md](references/step-explain.md) for detailed instructions.**

### Step 6: Report & Cleanup

Map anonymous names back to real names. Generate `sql-review-report.md` with 7 sections (overview, schema, inventory, query analysis, index recommendations, security notes, caveats). Clean up test instance and temp files.

**Read [references/step-report.md](references/step-report.md) for detailed instructions.**

## Reference Documents

| Document | Content |
|----------|---------|
| [references/index-design.md](references/index-design.md) | EXPLAIN metrics, composite index principles, index exploration method, common patterns, mock data rules |
| [references/mybatis.md](references/mybatis.md) | MyBatis dynamic SQL tag expansion rules, multi-path analysis algorithm, parameter placeholders |
