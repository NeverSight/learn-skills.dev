---
name: altimate-data-engineering-skills
description: Claude Code skills for analytics and data engineers working with dbt, Snowflake, and data pipelines
triggers:
  - "help me create a dbt model"
  - "debug this dbt compilation error"
  - "optimize this Snowflake query"
  - "add tests to my dbt models"
  - "document my dbt models"
  - "convert this SQL to dbt"
  - "find expensive queries in Snowflake"
  - "refactor this dbt model safely"
---

# Altimate Data Engineering Skills

> Skill by [ara.so](https://ara.so) — Data Skills collection.

Altimate Data Engineering Skills is a collection of Claude Code skills that encode the workflows and best practices of experienced analytics engineers. These skills transform Claude from a code generator into a capable data engineering assistant by teaching **how to approach tasks**, not just what syntax to use.

The project demonstrates 53% accuracy on ADE-bench (43 real-world dbt tasks), 3x improvement on model creation tasks, and 84% pass rate on Snowflake query optimization.

## What This Project Does

Data Engineering Skills provides:
- **7 dbt skills**: Model creation, debugging, testing, documentation, migration, refactoring, incremental models
- **3 Snowflake skills**: Cost analysis, query optimization by ID, query optimization by text
- **1 delegation skill**: Hand off complex tasks to altimate-code CLI tool
- **Workflow automation**: Skills trigger automatically based on user intent
- **Best practices**: Encoded patterns from experienced analytics engineers

Skills are markdown files with YAML frontmatter that define trigger conditions and step-by-step workflows.

## Installation

### Installing Skills in Claude Code

```bash
# Add the marketplace plugin
/plugin marketplace add AltimateAI/data-engineering-skills

# Install all skills
/plugin install dbt-skills@data-engineering-skills
/plugin install snowflake-skills@data-engineering-skills
/plugin install altimate-code@data-engineering-skills
```

### Installing Kits

Kits bundle skills, MCP servers, and instructions:

```bash
# Install altimate-code CLI (required for kits)
npm install -g altimate-code

# Install kit system
altimate-code kit install AltimateAI/data-engineering-skills

# Activate the dbt-snowflake kit
altimate-code kit activate dbt-snowflake

# Check status
altimate-code kit status
```

### Manual Installation

Clone and reference skills directly:

```bash
git clone https://github.com/AltimateAI/data-engineering-skills.git
cd data-engineering-skills
```

## Available Skills

### dbt Skills

**creating-dbt-models**: Creates new dbt models following project conventions
- Discovers existing patterns before writing
- Runs `dbt build` after creation (not just compile)
- Verifies output with `dbt show`
- Handles staging, intermediate, and mart models

**debugging-dbt-errors**: Troubleshoots dbt compilation and runtime errors
- Reads full error messages carefully
- Checks upstream dependencies
- Applies fixes and rebuilds
- Stops after 3 failed attempts to reassess

**testing-dbt-models**: Adds schema tests to models
- Studies existing test patterns in project
- Matches project testing style
- Covers uniqueness, not_null, relationships, accepted_values

**documenting-dbt-models**: Generates dbt model documentation
- Analyzes model logic and columns
- Creates descriptions for models and fields
- Follows project documentation patterns

**migrating-sql-to-dbt**: Converts legacy SQL to dbt models
- Parses raw SQL queries
- Creates proper dbt model structure
- Handles CTEs, refs, and sources

**refactoring-dbt-models**: Safely restructures dbt models
- Tracks all dependencies before changes
- Applies refactoring
- Verifies downstream models still work

**developing-incremental-models**: Creates incremental dbt models
- Selects appropriate strategy (append, merge, delete+insert)
- Designs proper unique_key
- Handles late-arriving data and edge cases

### Snowflake Skills

**finding-expensive-queries**: Identifies costly Snowflake queries
- Finds queries by cost, time, or data scanned
- Ranks by impact
- Provides query IDs for optimization

**optimizing-query-by-id**: Optimizes using Snowflake query history ID
- Retrieves query profile from ID
- Applies optimization patterns
- Validates semantic preservation

**optimizing-query-text**: Optimizes raw SQL query text
- Profiles query execution
- Identifies bottlenecks (scans, joins, aggregations)
- Applies anti-pattern fixes
- Tests performance improvement

### Delegation Skill

**altimate-code**: Delegates complex data tasks to altimate-code CLI
- Verifies altimate-code installation
- Invokes `altimate-code run --yolo` non-interactively
- Reads output file and summarizes results
- Requires: `npm install -g altimate-code` (Node 20+)

## Skill Structure

Skills are markdown files with YAML frontmatter:

```yaml
---
name: creating-dbt-models
description: |
  Guide for creating dbt models. ALWAYS use this skill when:
  (1) Creating ANY new model (staging, intermediate, mart)
  (2) Task mentions "create", "build", "add" with model/table
  (3) Modifying model logic or columns
---
```

Followed by workflow instructions:

```markdown
# dbt Model Development

**Read before you write. Build after you write. Verify your output.**

## Critical Rules
1. ALWAYS run `dbt build` after creating models - compile is NOT enough
2. ALWAYS verify output after build using `dbt show`
3. If build fails 3+ times, stop and reassess your approach

## Workflow
1. Discover Conventions
   - Check existing models in same layer (staging/intermediate/mart)
   - Note naming patterns, CTE style, column ordering
   
2. Write Model
   - Follow discovered patterns
   - Use proper refs and sources
   
3. Build and Verify
   ```bash
   dbt build --select model_name
   dbt show --select model_name --limit 10
   ```
```

## Usage Examples

### Creating a dbt Model

```yaml
# User request:
"Create a staging model for raw customers data"

# Skill triggers: creating-dbt-models
# AI workflow:
# 1. Checks models/staging/ for naming patterns
# 2. Creates models/staging/stg_customers.sql
# 3. Runs: dbt build --select stg_customers
# 4. Verifies: dbt show --select stg_customers
```

Example model created:

```sql
-- models/staging/stg_customers.sql
with source as (
    select * from {{ source('jaffle_shop', 'customers') }}
),

renamed as (
    select
        id as customer_id,
        first_name,
        last_name,
        email,
        created_at
    from source
)

select * from renamed
```

### Debugging dbt Errors

```yaml
# User request:
"Fix this error: Compilation Error in model customers (models/customers.sql)"

# Skill triggers: debugging-dbt-errors
# AI workflow:
# 1. Reads full error message
# 2. Checks upstream model dependencies
# 3. Identifies issue (e.g., missing ref)
# 4. Applies fix
# 5. Rebuilds: dbt build --select customers
```

### Optimizing Snowflake Query

```yaml
# User request:
"This query is taking 5 minutes, can you optimize it?"

# Skill triggers: optimizing-query-text
# AI workflow:
# 1. Profiles query (EXPLAIN, execution stats)
# 2. Identifies bottlenecks (table scans, inefficient joins)
# 3. Applies optimizations (clustering, filters, join order)
# 4. Tests and measures improvement
```

Example optimization:

```sql
-- Before (slow)
SELECT 
    o.order_id,
    c.customer_name,
    SUM(oi.amount) as total
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
JOIN order_items oi ON o.order_id = oi.order_id
WHERE o.order_date >= '2024-01-01'
GROUP BY 1, 2;

-- After (optimized)
SELECT 
    o.order_id,
    c.customer_name,
    SUM(oi.amount) as total
FROM orders o
INNER JOIN order_items oi ON o.order_id = oi.order_id
LEFT JOIN customers c ON o.customer_id = c.customer_id
WHERE o.order_date >= '2024-01-01'
  AND o.order_date < '2024-12-31'  -- Added upper bound for partition pruning
GROUP BY 1, 2;
-- Assumes orders table is clustered by order_date
```

### Using Kits

```bash
# Activate dbt-snowflake kit for a project
cd /path/to/dbt-project
altimate-code kit activate dbt-snowflake

# This configures:
# - All dbt and Snowflake skills
# - MCP server for dbt (live project access)
# - Project-specific instructions

# Deactivate when done
altimate-code kit deactivate
```

Kit configuration (`.altimate/kits/active.yaml`):

```yaml
kit: dbt-snowflake
version: 1.0.0
skills:
  - creating-dbt-models
  - debugging-dbt-errors
  - testing-dbt-models
  - documenting-dbt-models
  - migrating-sql-to-dbt
  - refactoring-dbt-models
  - developing-incremental-models
  - finding-expensive-queries
  - optimizing-query-by-id
  - optimizing-query-text
mcp_servers:
  - dbt
instructions: |
  You are working on a dbt + Snowflake project.
  Always check project conventions before creating models.
  Run dbt build (not compile) after creating models.
```

## Configuration

### Skill Configuration

Skills are auto-triggered based on user requests. No explicit configuration needed.

### MCP Integration

Skills work best with Altimate MCP server for live project access:

```json
// claude_desktop_config.json or similar
{
  "mcpServers": {
    "altimate-dbt": {
      "command": "npx",
      "args": ["-y", "@altimate/mcp-server-dbt"],
      "env": {
        "DBT_PROJECT_DIR": "/path/to/dbt/project",
        "DBT_PROFILES_DIR": "/path/to/.dbt"
      }
    }
  }
}
```

MCP tools available to skills:
- `dbt_project_info`: Project structure, model list, sources
- `dbt_model_details`: Column types, dependencies, compiled SQL
- `dbt_compile`: Compile models without CLI
- `snowflake_query_history`: Recent query executions and stats
- `snowflake_table_stats`: Row counts, clustering info

## Common Patterns

### Pattern 1: Multi-Step Model Creation

```yaml
# User: "Create a mart model for monthly revenue by customer"
# Skills auto-chains:
# 1. creating-dbt-models: Creates initial model
# 2. testing-dbt-models: Adds schema tests
# 3. documenting-dbt-models: Adds documentation
```

### Pattern 2: Debug-Fix-Verify Loop

```yaml
# User: "My model won't compile"
# Skill: debugging-dbt-errors
# Workflow:
# 1. Read error
# 2. Check dependencies
# 3. Apply fix
# 4. Rebuild
# 5. If still fails, repeat up to 3x
# 6. If 3x fails, stop and reassess approach
```

### Pattern 3: Safe Refactoring

```yaml
# User: "Break this large model into smaller ones"
# Skill: refactoring-dbt-models
# Workflow:
# 1. Map all downstream dependencies
# 2. Create new intermediate models
# 3. Update refs in downstream models
# 4. Run dbt build on entire DAG
# 5. Verify no breakage
```

### Pattern 4: Incremental Model Development

```sql
-- Pattern: merge strategy with unique_key
{{ config(
    materialized='incremental',
    unique_key='event_id',
    merge_update_columns=['status', 'updated_at']
) }}

select
    event_id,
    user_id,
    event_type,
    status,
    created_at,
    updated_at
from {{ source('events', 'raw_events') }}
{% if is_incremental() %}
    where updated_at > (select max(updated_at) from {{ this }})
{% endif %}
```

### Pattern 5: Query Optimization Workflow

```python
# Skill: optimizing-query-text
# Steps encoded:
# 1. Profile query
# 2. Identify bottleneck type:
#    - Full table scan → Add filters/clustering
#    - Inefficient join → Reorder, change type
#    - Large aggregation → Pre-aggregate or partition
# 3. Apply pattern-based fix
# 4. Validate semantics unchanged
# 5. Measure improvement
```

## Troubleshooting

### Skills Not Triggering

**Problem**: Skills don't activate for your request

**Solution**: 
- Be explicit: "Create a dbt model" not "make a model"
- Check skill installation: `/plugin list`
- Review trigger phrases in skill YAML
- Use exact trigger phrases from skill description

### dbt Build Failures

**Problem**: Models fail to build after creation

**Solution**:
- Skill will auto-retry up to 3 times
- After 3 failures, skill stops to reassess
- Check `dbt debug` for connection issues
- Verify refs and sources exist
- Check for SQL syntax errors

### MCP Server Not Connected

**Problem**: Skills can't access live project data

**Solution**:
```bash
# Check MCP server config
cat claude_desktop_config.json | grep altimate

# Verify dbt project path
export DBT_PROJECT_DIR=/correct/path
export DBT_PROFILES_DIR=/correct/.dbt/path

# Restart Claude Code
```

### altimate-code Delegation Fails

**Problem**: "altimate-code not found" error

**Solution**:
```bash
# Install altimate-code CLI
npm install -g altimate-code

# Verify installation
altimate-code --version

# Check Node version (requires 20+)
node --version
```

### Query Optimization No Improvement

**Problem**: Optimized query performs the same

**Solution**:
- Skill checks for anti-patterns but can't fix all issues
- May need manual clustering/indexing setup
- Check if bottleneck is data volume (consider aggregation)
- Review Snowflake warehouse size
- Use `finding-expensive-queries` to compare before/after

### Kit Activation Issues

**Problem**: Kit won't activate

**Solution**:
```bash
# Check kit is installed
altimate-code kit list

# Reinstall if needed
altimate-code kit install AltimateAI/data-engineering-skills

# Check for conflicting active kits
altimate-code kit status

# Deactivate others first
altimate-code kit deactivate
```

## Performance

Benchmark results (ADE-bench, 43 real-world dbt tasks):
- **Baseline Claude**: 46.5% accuracy (20/43 tasks)
- **Claude + Skills**: 53.5% accuracy (23/43 tasks)
- **Model Creation**: 3x improvement (40% → 65%)

Snowflake optimization (TPC-H SF1000, 62 queries):
- **Baseline**: 77.4% pass rate, 4.7% avg improvement
- **With Skills**: 83.9% pass rate, 16.8% avg improvement (3.6x better)

## Additional Resources

- Documentation: https://docs.myaltimate.com/
- ADE-bench Framework: https://github.com/dbt-labs/ade-bench
- altimate-code CLI: https://github.com/AltimateAI/altimate-code
- dbt Slack: https://getdbt.slack.com/archives/C05KPDGRMDW
- Contact: https://app.myaltimate.com/contactus
