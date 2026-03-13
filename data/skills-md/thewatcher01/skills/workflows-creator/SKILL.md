---
name: workflows-creator
description: Expert guide for creating state-of-the-art chainskills workflows following MCP and agent skills standards. Use when designing multi-step agent workflows, converting processes to .workflow.md format, or building production-grade automation pipelines.
---

# Workflows Creator — chainskills

**Create world-class `.workflow.md` files following SOTA design patterns.**

## When to Use This Skill

Triggers:
- "create workflow", "chainskills workflow", "new .workflow.md"  
- "design agent pipeline", "convert to workflow"
- "workflow best practices", "production workflow"

Use when:
- Creating new chainskills workflows from scratch
- Converting existing scripts/processes to declarative format
- Designing complex multi-step agent orchestrations
- Building MCP-compatible workflow tools
- Architecting parallel execution pipelines

---

## Quick Start

### 1. Basic Workflow Structure

```markdown
---
name: my-workflow
description: Clear one-sentence purpose
version: 0.1.0
inputs:
  - name: target
    type: string
    required: true
    description: What to process
outputs:
  - name: result
    type: object
    description: Final output
env:
  - API_KEY
tags:
  - automation
---

## Validate Input

@assert $target != ""
@env API_KEY

## Process Data

@try:
  @call mcp.fetch_data($target) → $data
@on-error: retry
  @repeat max:3:
    @call mcp.fetch_data($target) → $data

## Declare Output

@output: $data
```

### 2. Key Commands

```bash
# Validate syntax
chainskills validate workflow.md

# Inspect DAG
chainskills inspect workflow.md

# Dry run
chainskills run workflow.md --dry-run

# Execute
chainskills run workflow.md --input target=value
```

---

## Core Principles

### 1. Hexagonal Design
- **Pure declarative** — Workflows are data, not code
- **Composable** — Use `@use` to import sub-workflows/skills  
- **Testable** — Clear inputs/outputs/assertions
- **Resilient** — `@try/@on-error` around risky operations
- **Observable** — Emit meaningful state at each step
- **Parallel-by-default** — Let DAG auto-detect opportunities

### 2. Frontmatter Standards (MCP-inspired)

**Required:**
- `name` — kebab-case unique identifier
- `description` — One action-oriented sentence
- `version` — SemVer (0.1.0 for new)
- `inputs[]` — name, type, required, description, default
- `outputs[]` — name, type, description

**Recommended:**
- `env[]` — All env vars used (security)
- `tags[]` — Discovery & categorization
- `metadata` — author, license, dependencies

**See:** [guides/frontmatter.md](guides/frontmatter.md) for full specification

### 3. Step Structure

Each step = Markdown heading with clear, actionable title:

```markdown
## Step 1: Validate Input

Check format and set defaults.

@assert $target != ""
@if $depth < 1:
  @output: error="Invalid depth"
```

**Conventions:**
- Action verbs: "Validate", "Fetch", "Process", "Aggregate"
- Clear scope: What + Why
- Numbered if sequential, named if reusable

### 4. Variable Naming

```
$snake_case          — All variables
$input_*             — Raw inputs
$validated_*         — After validation
$processed_*         — After transformation
$final_*             — Ready for output
$_error              — Error state (reserved)
$_iteration          — Loop counter (reserved)
```

**Avoid:** `$data`, `$result`, `$temp` (too generic)

### 5. Output Declaration (Always Last)

```markdown
## Declare Outputs

@output: $final_result, $execution_metrics, $warnings
```

---

## Directive Quick Reference

### Essential Patterns

```markdown
@call tool.method($arg) → $result    # Invoke tool
@if $condition:                      # Branch
@for $item in $list:                 # Loop
@parallel:                           # Parallel block
@try: ... @on-error: action          # Error handling
@agent name: "prompt" → $var         # Agent delegation
@assert $condition                   # Validation
@env VAR_NAME                        # Load env var
@output: $var1, $var2                # Declare outputs
@use skill-name                      # Import skill
@workflow path: $input → $output     # Sub-workflow
```

**See:** [guides/directives.md](guides/directives.md) for all 17 directives with examples

---

## Templates

Copy, customize, and deploy instantly:

- **[Data Pipeline](templates/data-pipeline.md)** — ETL with validation/transformation/enrichment
- **[Agent Research](templates/agent-research.md)** — AI-powered research with synthesis
- **[Service Integration](templates/service-integration.md)** — Circuit breaker + fallback + cache

---

## Best Practices Checklist

### Before Creating
- [ ] Clear single purpose (one sentence)
- [ ] Named inputs with types
- [ ] Named outputs with types
- [ ] All env vars declared
- [ ] Appropriate tags

### During Creation
- [ ] Input validation first
- [ ] `@try/@on-error` around risky ops
- [ ] `@parallel` for independent steps
- [ ] `@assert` for invariants
- [ ] Clear variable names
- [ ] Modular sub-workflows

### After Creation
- [ ] `chainskills validate`
- [ ] `chainskills inspect`
- [ ] `--dry-run` test
- [ ] Real execution test
- [ ] Document usage

**See:** [guides/best-practices.md](guides/best-practices.md) for anti-patterns & conventions

---

## Integration Guidelines

### MCP Tools
```markdown
env:
  - MCP_SERVERS
@call mcp.tool_name($param) → $result
```

### Agents
```markdown
env:
  - AGENT_API_KEY
@agent copilot: "Prompt with $var" → $response
```

### Skills
```markdown
@use ./common/validators
@workflow ./common/validators: $input → $validated
```

**See:** [guides/integration.md](guides/integration.md) for details

---

## Examples

**[Production-Grade Workflow](examples/production-grade.md)** — Enterprise data pipeline with circuit breaker, batch processing, quality checks, observability, and error recovery.

---

## Common Patterns

### Circuit Breaker
```markdown
@repeat max:3 until $success == true:
  @try:
    @call service → $result
    @call shell.exec("echo 'success'") → $success
  @on-error: log and continue
    @call shell.exec("sleep 1")
```

### Map-Reduce
```markdown
@for $item in $items:
  @call process($item) → $processed_item
@call aggregate($items_results) → $final
```

### Pipeline with Checkpoints
```markdown
@workflow step1 → $checkpoint1
@assert $checkpoint1.valid == true
@workflow step2: $checkpoint1 → $checkpoint2
```

---

## Security Checklist

- ✅ Declare all `env` vars in frontmatter
- ✅ Validate inputs with `@assert`
- ✅ Wrap external calls in `@try/@on-error`
- ✅ Use scoped env access (not `process.env`)
- ✅ No secrets in workflow files (use env vars)

---

## When NOT to Use Workflows

❌ NOT suitable for:
- Real-time latency-critical ops (< 100ms)
- Streaming data processing
- Stateful interactive sessions
- Binary data manipulation

✅ USE workflows for:
- Automation pipelines (CI/CD, ETL, monitoring)
- Agent orchestration (research, analysis, content)
- Service integration (API composition, multi-step)
- Batch processing (reports, migrations, audits)
- Complex decision trees (approval flows, routing)

---

## Modular Structure

```
workflows-creator/
├── SKILL.md                    # This file (quick reference)
├── guides/
│   ├── frontmatter.md         # YAML frontmatter standards
│   ├── directives.md          # All 17 directives with examples
│   ├── best-practices.md      # Checklist, conventions, anti-patterns
│   └── integration.md         # MCP, agent, skill composition
├── templates/
│   ├── data-pipeline.md       # ETL template
│   ├── agent-research.md      # AI research template
│   └── service-integration.md # Circuit breaker template
└── examples/
    └── production-grade.md    # Full production example
```

---

## Next Steps

1. **Read** [guides/directives.md](guides/directives.md) for directive patterns
2. **Copy** a [template](templates/) that fits your use case
3. **Validate** with `chainskills validate`
4. **Inspect** DAG with `chainskills inspect`
5. **Test** with `--dry-run` before production

Always validate with `chainskills validate`, inspect with `chainskills inspect`, and test with `--dry-run` before deployment.
