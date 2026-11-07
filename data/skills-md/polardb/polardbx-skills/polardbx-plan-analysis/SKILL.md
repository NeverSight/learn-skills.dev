---
name: polardbx-plan-analysis
description: |
  Analyze PolarDB-X execution plans or determine semantic equivalence between SQL and execution plans. Covers EXPLAIN / EXPLAIN COST / EXPLAIN ANALYZE operator interpretation, cost estimation analysis, runtime statistics bottleneck identification, SQL-to-plan equivalence verification, and optional Graphviz plan visualization.
  Use when analyzing execution plans on PolarDB-X, interpreting operator behavior, checking plan cost/performance, or verifying SQL-plan semantic equivalence.
  Triggers: "plan analysis", "执行计划分析", "explain output", "explain cost", "explain analyze", "operator meaning", "算子含义", "equivalence analysis", "等价性分析", "plan equivalence", "计划是否等价", "sql and plan consistency", "sql和plan是否一致", "cost analysis", "代价分析", "rowcount deviation", "rowcount偏差", "draw plan", "画计划图", "plan visualization", "计划可视化"
metadata:
  version: 0.1.1
---

# PolarDB-X Execution Plan Analysis

Analyze PolarDB-X execution plans (EXPLAIN / EXPLAIN COST / EXPLAIN ANALYZE output) and verify semantic equivalence between SQL and execution plans.

## Scope

**Applies to:**

- Operator interpretation of `EXPLAIN` / `EXPLAIN COST` / `EXPLAIN ANALYZE` output
- `EXPLAIN COST` cost estimation (rowcount, cumulative cost) interpretation
- `EXPLAIN ANALYZE` runtime statistics (actual time, actual rowcount, instances) interpretation and bottleneck identification
- SQL-to-execution-plan semantic equivalence verification
- Foundation for phase/rule-level optimizer attribution analysis (operator interpretation capabilities)

**Does NOT apply to:**

- Optimizer rule tuning or phase-level attribution analysis
- SQL rewriting or query optimization suggestions
- Index recommendation or schema design (use `sql-review` or `polardbx-sql`)
- Non-PolarDB-X EXPLAIN output (MySQL, PostgreSQL, etc.)
- DN-level (storage node) internal execution details

**Verification** — confirm you are working with PolarDB-X EXPLAIN output:

```sql
SELECT version();          -- should contain "PolarDB-X" or "TDDL"
SHOW STORAGE;              -- PolarDB-X specific command, confirms distributed topology
```

---

## Mode 1: Plan Interpretation

### Workflow

1. **Receive input** — User pastes EXPLAIN output. If not provided, guide them to run `EXPLAIN <sql>` / `EXPLAIN COST <sql>` / `EXPLAIN ANALYZE <sql>`
2. **Identify mode** — Contains `rowcount =` -> EXPLAIN COST; contains `actual time =` -> EXPLAIN ANALYZE. See `references/explain-cost-analyze.md` for field definitions
3. **Parse plan tree** — One operator per line, indentation indicates parent-child relationship, operator name is the text before the first `(`
4. **Separate metadata** — Identify non-operator lines at the end of the plan tree (`HitCache:`, `Source:`, `TemplateId:`, etc.), process them separately as metadata
5. **Classify operators** — Match against `references/operator-taxonomy.md` into 17 categories (note: display names may differ from class names, see mapping table)
6. **Interpret each operator** — Explain bottom-up: name, category, function, key attributes. See corresponding reference files for operator attribute definitions
7. **Cost/performance analysis** (COST/ANALYZE mode) — rowcount deviation, actual time bottlenecks, instances, spill
8. **Plan description** — One paragraph summarizing data flow (scan -> output), stating plan type and key strategies
9. **Metadata interpretation** — Parse HitCache/Source/TemplateId/BaselineInfo fields, provide cache hit and plan source conclusions

### Output Format

Output three sections (four when metadata is present): **Raw Plan** -> **Plan Description** -> **Operator Analysis** -> **Plan Metadata** (if applicable).

```
## Raw Plan

<Each line prefixed with line number, format: "line_number  operator_text", line numbers right-aligned>

## Plan Description

<One paragraph summarizing data flow, with L<line_number> annotations at key operators for reference>

## Operator Analysis

| # | Operator | Category | Description |
|---|----------|----------|-------------|
| 1 | Project | Project | Computes promo_revenue = 100 * $f0 / $f1. Input: #2 |
| 2 | HashAgg | Agg | Scalar aggregation sum($f0), sum($f1), final stage. Input: #3 |
| ... | ... | ... | ... |
```

### Raw Plan Line Numbering Rules

- Lines are numbered sequentially starting from 1
- Line numbers are right-aligned with space padding (e.g., ` 1`, `10`)
- Two spaces follow the line number, then the original indentation and operator text
- Example:
  ```
   1  Exchange(distribution=single, collation=[])
   2    Project(promo_revenue="?0 * $f0 / $f1")
   3      HashAgg($f0="sum($f0)", $f1="sum($f1)")
  ```

### Plan Description Requirements

1. State the plan type at the beginning: Columnar / MPP / SMP
2. Trace data flow bottom-up, describe in actual flow order
3. Use specific column names and values: annotate shuffle partition count like `shuffle by l_partkey to 96 partitions`
4. Specify join roles: which side builds the hash table, whether partition-wise
5. Annotate key strategies: two-phase aggregation, broadcast small table, large table stays in place
6. Appropriate sentence breaks: 2-4 operation steps per sentence, separated by periods
7. Annotate key nodes with `(L<line_number>)` referencing the raw plan line number for quick lookup. Annotation targets include: Exchange/shuffle, join, aggregation, sort, and other key operators; not every operator needs annotation, only those helpful for understanding data flow

### Operator Analysis Requirements

- Listed in original plan order (root to leaf)
- Append `Input: #N` at the end of the description to indicate data source line number
- Dual-input operators annotated as `Input: #N, #M`
- Leaf nodes have no input annotation

### Example

**Input plan:**

```
Project(promo_revenue="?0 * $f0 / $f1")
  HashAgg($f0="sum($f0)", $f1="sum($f1)")
    Exchange(distribution=single, collation=[])
      PartialHashAgg($f0="sum($f0)", $f1="sum($f1)")
        Project($f0="...", $f1="l_extendedprice * ?4 - l_discount")
          HashJoin(condition="l_partkey = p_partkey", type="inner")
            OSSTableScan(tables="part_col_index[p1,...p96]", shardcount=96, partition=[remote])
            Exchange(distribution=hash[0]96, collation=[])
              OSSTableScan(tables="lineitem_col_index[p1,...p96]", shardcount=96, sql="... where l_shipdate ...")
```

**Output:**

```
## Raw Plan

1  Project(promo_revenue="?0 * $f0 / $f1")
2    HashAgg($f0="sum($f0)", $f1="sum($f1)")
3      Exchange(distribution=single, collation=[])
4        PartialHashAgg($f0="sum($f0)", $f1="sum($f1)")
5          Project($f0="...", $f1="l_extendedprice * ?4 - l_discount")
6            HashJoin(condition="l_partkey = p_partkey", type="inner")
7              OSSTableScan(tables="part_col_index[p1,...p96]", shardcount=96, partition=[remote])
8              Exchange(distribution=hash[0]96, collation=[])
9                OSSTableScan(tables="lineitem_col_index[p1,...p96]", shardcount=96, sql="... where l_shipdate ...")

## Plan Description

Columnar execution plan. Scans lineitem(L9) with l_shipdate filter, then shuffles by l_partkey to 96 partitions(L8), partition-wise hash join(L6) with part(L7). Projects to compute promo/total revenue, then two-phase aggregation (PartialHashAgg(L4) -> Exchange single(L3) -> HashAgg(L2)), finally Project(L1) outputs promo_revenue.

## Operator Analysis

| # | Operator | Category | Description |
|---|----------|----------|-------------|
| 1 | Project | Project | Computes promo_revenue = 100 * $f0 / $f1. Input: #2 |
| 2 | HashAgg | Agg | Scalar aggregation sum, final stage. Input: #3 |
| 3 | Exchange | Exchange | distribution=single, converges to single node. Input: #4 |
| 4 | PartialHashAgg | Agg | Scalar aggregation sum, first stage. Input: #5 |
| 5 | Project | Project | Computes promo revenue and total revenue. Input: #6 |
| 6 | HashJoin | Join | inner, l_partkey = p_partkey. Input: #7, #8 |
| 7 | OSSTableScan | TableScan | part_col_index, 96 shards |
| 8 | Exchange | Exchange | hash[0]96, lineitem shuffled by l_partkey. Input: #9 |
| 9 | OSSTableScan | TableScan | lineitem_col_index, 96 shards, l_shipdate filter |
```

**More plan description examples:**

- "Columnar execution plan. Filters region(L15) then broadcasts(L14), joins with nation(L13) then broadcasts(L12), customer joins the result(L11). Orders filtered by date, shuffled by o_custkey to 96 partitions(L8) to join customer result(L7), then shuffled by o_orderkey to 96 partitions(L5) to join lineitem(L4). Supplier broadcasts(L3), joins via suppkey + nationkey(L2), two-phase agg groups by n_name, sorts by revenue for output(L1)."
- "Columnar execution plan. Orders filtered by date(L7), partition-wise semi hash join with lineitem(L5). Two-phase agg(L3,L4) counts by o_orderpriority, sorts for output(L1)."
- "SMP execution plan. Orders and lineitem pushed down to DN for join and partial aggregation(L4,L5), Gather(L3) collects results, CN performs final HashAgg(L2), TopN(L1) returns top 10."

### Plan Metadata Parsing

EXPLAIN output may include metadata lines at the end (`HitCache`, `Source`, `TemplateId`, etc.). These lines **are not part of the operator tree**, are not included in line numbering, and are interpreted separately in a `## Plan Metadata` section after the operator analysis table.

See `references/plan-metadata.md` for field definitions, Source enum values, output format, and interpretation guidelines.

---

## Mode 2: Equivalence Analysis

### Workflow

1. **Receive input** — Obtain the SQL and corresponding EXPLAIN plan
2. **Check each dimension** — Verify bottom-up along the 14 dimensions defined in `references/equivalence-analysis.md`
3. **Output conclusion** — Per-dimension verdict; when not equivalent, specify location and reason

### 14 Analysis Dimensions

| # | Dimension | Core Checkpoints |
|---|-----------|-----------------|
| 1 | Filter conditions | WHERE/HAVING predicate completeness, operator direction |
| 2 | Column references & projection | Project expressions match SELECT list, column index misalignment |
| 3 | JOIN conditions & type | condition + type (inner/semi/anti/left/right) |
| 4 | Aggregation | GROUP BY column set, function type, DISTINCT |
| 5 | Sort & LIMIT | ORDER BY direction, LIMIT/OFFSET, two-phase TopN |
| 6 | Exchange/Shuffle | Distribution strategy ensures no data loss or duplication |
| 7 | Subquery decorrelation | CorrelateApply -> Semi/Anti Join transformation correctness |
| 8 | CTE | projects/conditions column indices, execution order |
| 9 | Window functions | PARTITION BY, ORDER BY, function, frame boundary |
| 10 | Set operations | UNION ALL vs DISTINCT, column compatibility |
| 11 | TableScan pushed-down SQL | sql field contains correct push-down logic |
| 12 | Parameterization restoration | ?N corresponds to original literal values |
| 13 | Expand | GROUPING SETS expansion and groupId |
| 14 | TableLookup | Lookup condition and output column completeness |

### Output Format

```
## Equivalence Analysis

### Filter Conditions
- Result: Equivalent
- Explanation: ...

### JOIN Conditions & Type
- Result: Not equivalent
- Explanation: ...

## Conclusion
SQL and plan are [equivalent / not equivalent]. [When not equivalent, describe the issue]
```

---

## Plan Visualization (Optional)

Only execute when the user explicitly requests "draw", "visualize", or similar. **Do not draw by default.**

See `references/plan-visualization.md` for details.

---

## EXPLAIN Display Name -> Operator Class Mapping

| Display Name | Operator Class | Category |
|-------------|---------------|----------|
| LogicalView | LogicalView | TableScan |
| IndexScan | LogicalIndexScan | TableScan |
| OSSTableScan | OSSTableScan | TableScan |
| HashJoin | HashJoin | Join |
| NLJoin | NLJoin | Join |
| BKAJoin | BKAJoin | Join |
| SortMergeJoin | SortMergeJoin | Join |
| SemiHashJoin | SemiHashJoin | Join |
| SemiNLJoin | SemiNLJoin | Join |
| SemiBKAJoin | SemiBKAJoin | Join |
| MaterializedSemiJoin | MaterializedSemiJoin | Join |
| CorrelateApply | LogicalCorrelate | Join |
| ColCorrelate | LogicalColCorrelate | Join |
| LogicalJoin | LogicalJoin | Join |
| LogicalSemiJoin | LogicalSemiJoin | Join |
| LogicalAgg | LogicalAggregate | Agg |
| HashAgg | HashAgg | Agg |
| SortAgg | SortAgg | Agg |
| LogicalSort | LogicalSort | Sort |
| Limit | Limit / LogicalSort | Sort |
| MergeSort | MergeSort | Sort |
| TopN | TopN | Sort |
| MemSort | MemSort | Sort |
| Window | LogicalWindow | Window |
| HashWindow | HashWindow | Window |
| SortWindow | SortWindow | Window |
| Filter | LogicalFilter / PhysicalFilter | Filter |
| Project | LogicalProject / PhysicalProject | Project |
| Calc | LogicalCalc | Project |
| Values | LogicalValues | Values |
| DynamicValues | LogicalDynamicValues | Values |
| TableLookup | LogicalTableLookup | TableLookup |
| Gather | Gather | Exchange |
| Exchange | MppExchange / ColumnarExchange | Exchange |
| LocalBuffer | LocalBufferNode | Exchange |
| CTEAnchor | PhysicalCTEAnchor | CTE |
| CTEProducer | PhysicalCTEProducer | CTE |
| LogicalCTEConsumer | LogicalCTEConsumer | CTE |
| UnionAll | LogicalUnion (all=true) | SetOp |
| UnionDistinct | LogicalUnion (all=false) | SetOp |
| Intersect | LogicalIntersect | SetOp |
| Minus | LogicalMinus | SetOp |
| Expand | LogicalExpand | Expand |
| LogicalInsert | LogicalInsert | DML |
| LogicalModify | LogicalModify | DML |
| LogicalOutFile | LogicalOutFile | OutFile |
| PhyTableOperation | PhyTableOperation | BaseTableOperation |
| RuntimeFilterBuilder | RuntimeFilterBuilder | Other |

---

## References

| File | Content |
|------|---------|
| `references/operator-taxonomy.md` | Complete 17-category operator taxonomy |
| `references/equivalence-analysis.md` | 14-dimension equivalence analysis and checking procedure |
| `references/explain-cost-analyze.md` | EXPLAIN COST / ANALYZE cost and runtime statistics fields |
| `references/plan-metadata.md` | Plan metadata (HitCache/Source/TemplateId/BaselineInfo, etc.) |
| `references/plan-visualization.md` | Graphviz plan visualization |
| `references/join.md` | Join operator attributes |
| `references/agg.md` | Agg operator attributes |
| `references/sort.md` | Sort operator attributes |
| `references/filter.md` | Filter operator attributes |
| `references/project.md` | Project operator attributes |
| `references/exchange.md` | Exchange operator attributes |
| `references/tablescan.md` | TableScan operator attributes |
| `references/window.md` | Window operator attributes |
| `references/cte.md` | CTE operator attributes |
| `references/tablelookup.md` | TableLookup operator attributes |
| `references/setop.md` | SetOp operator attributes |
| `references/expand.md` | Expand operator attributes |
| `references/values.md` | Values operator attributes |
| `references/dml.md` | DML operator attributes (INSERT/UPDATE/DELETE/REPLACE) |
| `references/outfile.md` | OutFile operator attributes |
| `references/other.md` | Other operator attributes |
| `references/rex-explain-visitor.md` | RexNode expression display rules |
| `references/sql-parameterization.md` | SQL parameterization rules |
