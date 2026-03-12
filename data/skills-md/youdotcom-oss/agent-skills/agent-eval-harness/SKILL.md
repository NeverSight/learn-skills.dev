---
name: agent-eval-harness
description: CLI tool for capturing agent trajectories. Execute prompts against headless CLI agents via schema-driven adapters, capture full trajectories (tools, thoughts, plans), and output structured JSONL for downstream scoring.
compatibility: Bun >= 1.2.9
---

# Agent Eval Harness

## Purpose

CLI tool for capturing trajectories from headless CLI agents, optimized for TypeScript/JavaScript projects using Bun.

**The harness captures. You score.**

| Harness Provides | You Provide |
|------------------|-------------|
| Prompt execution via headless adapters | Scoring logic (Braintrust, custom scripts) |
| Full trajectory capture (thoughts, tools, plans) | Pass/fail determination via graders |
| Structured JSONL output | LLM-as-judge prompts |
| Reproducible execution environment | CI integration, golden file comparison |

**Use this when:**
- Capturing trajectories for downstream evaluation
- Generating training data (SFT/DPO) with full context
- Building regression test fixtures for agent behavior
- Comparing agent responses across configurations

## Installation

```bash
# Run without installing (recommended)
bunx @plaited/agent-eval-harness capture prompts.jsonl --schema ./claude.json -o results.jsonl

# Or install as project dependency
bun add @plaited/agent-eval-harness
```

## Core Principle: Capture Once, Derive Many Views

```mermaid
flowchart LR
    Prompts["prompts.jsonl"] --> Capture["capture/trials"]
    Schema["headless schema"] --> Capture
    Capture --> Results["results.jsonl (full trajectory)"]
    Results --> Summarize["summarize"]
    Results --> Calibrate["calibrate"]
    Results --> Custom["(your tools)"]
    Summarize --> Views["summary.jsonl / .md"]
    Calibrate --> Report["calibration.md"]
    Custom --> Pipeline["any scoring platform"]
```

**Single output format:** Full trajectory JSONL (always)
**No `--format` flag:** Derive views with separate commands
**Schema exports:** Zod schemas + JSON Schema for any tooling

## Commands

### Core Commands

| Command | Input | Output | Purpose |
|---------|-------|--------|---------|
| `capture` | prompts.jsonl + schema | results.jsonl | Trajectory capture (full) |
| `trials` | prompts.jsonl + schema | trials.jsonl | Multi-run + optional metrics |
| `summarize` | results.jsonl | summary.jsonl or .md | Derive compact views |
| `calibrate` | results.jsonl | calibration.md | Sample failures for review |
| `validate-refs` | prompts.jsonl | validation.jsonl | Check reference solutions |
| `balance` | prompts.jsonl | balance.json | Analyze test set coverage |
| `schemas` | (none) | JSON Schema | Export schemas for non-TS users |

### Pipeline Commands (Unix-style)

| Command | Input | Output | Purpose |
|---------|-------|--------|---------|
| `run` | prompts.jsonl + schema | raw.jsonl | Execute prompts, raw output |
| `extract` | raw.jsonl + schema | extracted.jsonl | Parse trajectories |
| `grade` | extracted.jsonl + grader | graded.jsonl | Apply grader scoring |
| `format` | results.jsonl | jsonl/markdown/csv | Convert output format |
| `compare` | multiple results.jsonl | comparison.json | Compare runs (aggregate report) |

All commands support optional `--grader ./grader.ts` for scoring.

## Capture Command

### Basic Usage

```bash
bunx @plaited/agent-eval-harness capture <prompts.jsonl> --schema <schema.json> [options]
```

### Arguments

| Argument/Flag | Description | Default |
|------|-------------|---------|
| `prompts.jsonl` | Input file with prompts to execute | Required |
| `-s, --schema` | Path to headless adapter schema | Required |
| `-o, --output` | Output file/path | stdout |
| `-c, --cwd` | Working directory for agent | current |
| `-t, --timeout` | Request timeout in ms | `60000` |
| `-j, --concurrency` | Number of concurrent workers | `1` |
| `--workspace-dir` | Base directory for per-prompt workspace isolation | none |
| `--progress` | Show progress to stderr | false |
| `--append` | Append to output file | false |
| `-g, --grader` | Path to grader module | none |
| `--debug` | Show detailed CLI output for debugging | false |

### Examples

```bash
# Basic capture
bunx @plaited/agent-eval-harness capture prompts.jsonl --schema ./claude.json -o results.jsonl

# Parallel execution (4x faster with 4 workers)
bunx @plaited/agent-eval-harness capture prompts.jsonl --schema ./claude.json -j 4 -o results.jsonl

# With workspace isolation for code generation tasks
bunx @plaited/agent-eval-harness capture prompts.jsonl --schema ./claude.json \
  -j 4 --workspace-dir ./workspaces -o results.jsonl

# Using a local adapter script
bunx @plaited/agent-eval-harness capture prompts.jsonl bun ./my-adapter.ts -o results.jsonl

# With grader (adds score to each result)
bunx @plaited/agent-eval-harness capture prompts.jsonl --schema ./claude.json --grader ./grader.ts -o results.jsonl
```

## Trials Command

Run each prompt multiple times for pass@k/pass^k analysis.

```bash
# Capture only (no grader)
bunx @plaited/agent-eval-harness trials prompts.jsonl --schema ./claude.json -k 5 -o trials.jsonl

# With grader (computes pass@k, pass^k)
bunx @plaited/agent-eval-harness trials prompts.jsonl --schema ./claude.json -k 5 --grader ./grader.ts -o trials.jsonl

# Parallel execution (4 prompts' trials run concurrently)
bunx @plaited/agent-eval-harness trials prompts.jsonl --schema ./claude.json -k 5 -j 4 -o trials.jsonl

# With workspace isolation (each trial gets its own directory)
bunx @plaited/agent-eval-harness trials prompts.jsonl --schema ./claude.json -k 5 -j 4 \
  --workspace-dir ./workspaces -o trials.jsonl
```

**Parallelization notes:**
- `-j/--concurrency` parallelizes across prompts (not trials within a prompt)
- Each prompt's k trials still run sequentially (required for aggregation)
- With 151 prompts and `-j 4`, you get 4 prompts running trials concurrently
- `--workspace-dir` creates `{workspace-dir}/prompt-{id}-trial-{n}/` for each trial
- Progress logging shows aggregate completion (e.g., `12/50 prompts completed`)

**Workspace cleanup:**
Directories persist after completion for debugging. Clean up manually:
```bash
# After capture
rm -rf ./workspaces

# In CI (add as post-step)
- run: rm -rf ./workspaces
  if: always()
```

### Output

Without grader:
```jsonl
{"id":"search-001","input":"Find the CEO","k":5,"trials":[{"trialNum":1,"output":"...","trajectory":[...],"duration":1234},...]}
```

With grader:
```jsonl
{"id":"search-001","input":"Find the CEO","k":5,"passRate":0.8,"passAtK":0.99,"passExpK":0.33,"trials":[{"trialNum":1,"output":"...","pass":true,"score":1.0},...]}
```

## Summarize Command

Derive compact views from full trajectory results.

```bash
# Summary JSONL (for jq analysis)
bunx @plaited/agent-eval-harness summarize results.jsonl -o summary.jsonl

# Markdown (for LLM-as-judge)
bunx @plaited/agent-eval-harness summarize results.jsonl --markdown -o results.md
```

## Calibrate Command

Sample failures for grader review. Calibration helps you distinguish between **agent failures** (agent did wrong thing) and **grader bugs** (agent was correct, grader too strict).

```bash
# Sample failures for human review
bunx @plaited/agent-eval-harness calibrate results.jsonl --sample 10 -o calibration.md

# Re-score with different grader to compare
bunx @plaited/agent-eval-harness calibrate results.jsonl --grader ./loose-grader.ts --sample 10 -o comparison.md
```

See [eval-concepts.md](references/eval-concepts.md#grader-calibration) for why calibration matters.

## Validate-Refs Command

Check that reference solutions pass your grader before evaluating agents.

```bash
# Validate reference solutions
bunx @plaited/agent-eval-harness validate-refs prompts.jsonl --grader ./grader.ts -o validation.jsonl

# Check for failures
cat validation.jsonl | jq 'select(.pass == false)'
```

### Why Use This?

If your reference solution fails your own grader:
- The task definition is ambiguous
- The grader is too strict
- The hint is wrong

**Fix the eval before evaluating the agent.**

### Input Format

Prompts must include a `reference` field:

```jsonl
{"id":"test-001","input":"Create a button component","hint":"<button>","reference":"export const Button = () => <button>Click</button>"}
```

### Output Format

```jsonl
{"id":"test-001","input":"Create a button component","reference":"export const Button = () => <button>Click</button>","pass":true,"score":1.0,"reasoning":"Contains hint content"}
```

## Balance Command

Analyze test set coverage to ensure balanced evaluation.

```bash
# Analyze prompt distribution
bunx @plaited/agent-eval-harness balance prompts.jsonl -o balance.json

# Pretty print
bunx @plaited/agent-eval-harness balance prompts.jsonl | jq .
```

### Why Use This?

An eval with only "make X work" misses "don't break Y". Balance analysis shows:

- **Category distribution** (from `metadata.category`)
- **Positive/negative case ratio**
- **Coverage gaps**

### Output Format

```json
{
  "totalCases": 50,
  "categories": [
    { "name": "ui", "count": 20, "percentage": 40 },
    { "name": "logic", "count": 15, "percentage": 30 },
    { "name": "api", "count": 10, "percentage": 20 },
    { "name": "edge-case", "count": 5, "percentage": 10 }
  ],
  "underrepresented": ["edge-case"],
  "suggestions": ["Consider adding more test cases for: edge-case"]
}
```

### Balanced Eval Design

Include both positive and negative cases:

| Type | Example | Purpose |
|------|---------|---------|
| Positive | "Add a login button" | Agent should succeed |
| Negative | "Add a button without breaking tests" | Agent should not break things |
| Edge case | "Handle empty input gracefully" | Agent should be robust |

See [eval-concepts.md](references/eval-concepts.md#test-set-balance) for more on balanced test sets.

## Pipeline Workflow

The pipeline commands enable Unix-style composition for flexible evaluation workflows.

### Full Pipeline Example

```bash
# Execute → Extract → Grade → Format in one pipeline
cat prompts.jsonl | \
  bunx @plaited/agent-eval-harness run -s claude.json | \
  bunx @plaited/agent-eval-harness extract -s claude.json | \
  bunx @plaited/agent-eval-harness grade -g ./grader.ts | \
  bunx @plaited/agent-eval-harness format -f markdown > report.md
```

### Run Command

Execute prompts and output raw results. Three modes available:

```bash
# Schema mode (recommended)
bunx @plaited/agent-eval-harness run prompts.jsonl --schema claude.json

# Simple mode: {} placeholder substitution
bunx @plaited/agent-eval-harness run prompts.jsonl --simple "claude -p {} --output-format stream-json"

# Shell mode: $PROMPT environment variable
bunx @plaited/agent-eval-harness run prompts.jsonl --shell 'claude -p "$PROMPT" --output-format stream-json'
```

> **⚠️ Security Warning:** The `--simple` and `--shell` modes execute prompts via shell commands. Prompts are escaped but **do not use untrusted prompt content** with these modes. Malicious prompt text could potentially escape the quoting and execute arbitrary commands. Use `--schema` mode (headless adapter) for untrusted inputs.

### Extract Command

Parse raw output into structured trajectories:

```bash
# From file
bunx @plaited/agent-eval-harness extract raw.jsonl --schema claude.json -o extracted.jsonl

# Piped from run
bunx @plaited/agent-eval-harness run prompts.jsonl -s claude.json | \
  bunx @plaited/agent-eval-harness extract -s claude.json
```

### Grade Command

Apply grader to extracted results:

```bash
bunx @plaited/agent-eval-harness grade extracted.jsonl --grader ./grader.ts -o graded.jsonl
```

### Format Command

Convert results to different output formats:

```bash
# Markdown report
bunx @plaited/agent-eval-harness format results.jsonl --style markdown -o report.md

# CSV for spreadsheets
bunx @plaited/agent-eval-harness format results.jsonl --style csv -o results.csv

# JSONL (pass-through, default)
bunx @plaited/agent-eval-harness format results.jsonl --style jsonl
```

### Compare Command

Compare multiple runs of the same prompts. Supports both **CaptureResult** (single-run) and **TrialResult** (multi-run reliability) formats with auto-detection.

```bash
# Default: auto-detect format, weighted strategy, JSON output
bunx @plaited/agent-eval-harness compare run1.jsonl run2.jsonl -o comparison.json

# Statistical significance strategy
bunx @plaited/agent-eval-harness compare run1.jsonl run2.jsonl --strategy statistical -o comparison.json

# Custom weights via environment variables (CaptureResult)
COMPARE_QUALITY=0.7 COMPARE_LATENCY=0.2 COMPARE_RELIABILITY=0.1 \
  bunx @plaited/agent-eval-harness compare run1.jsonl run2.jsonl -o comparison.json

# Markdown report format
bunx @plaited/agent-eval-harness compare run1.jsonl run2.jsonl --format markdown -o report.md

# Custom grader (LLM-as-Judge)
bunx @plaited/agent-eval-harness compare run1.jsonl run2.jsonl \
  --strategy custom --grader ./my-llm-judge.ts -o comparison.json

# With explicit labels
bunx @plaited/agent-eval-harness compare \
  --run "with-mcp:results-mcp.jsonl" \
  --run "vanilla:results-vanilla.jsonl" \
  -o comparison.json
```

**Use cases for compare:**
- Same agent, different MCP servers
- Same agent, different skills enabled
- Same agent, different model versions
- Different agents entirely

### Trials Comparison (pass@k Analysis)

Compare TrialResult files for reliability analysis:

```bash
# Auto-detect trials format
bunx @plaited/agent-eval-harness compare trials1.jsonl trials2.jsonl -o comparison.json

# Explicit format (skip auto-detection)
bunx @plaited/agent-eval-harness compare trials1.jsonl trials2.jsonl --input-format trials -o comparison.json

# Custom weights for trials comparison
COMPARE_CAPABILITY=0.5 COMPARE_RELIABILITY=0.3 COMPARE_CONSISTENCY=0.2 \
  bunx @plaited/agent-eval-harness compare trials1.jsonl trials2.jsonl -o comparison.json
```

**Trials metrics:**

| Metric | Description | Formula |
|--------|-------------|---------|
| **Capability** (passAtK) | Can solve at least once in K tries | `1 - (1-p)^k` |
| **Reliability** (passExpK) | Solves consistently every time | `p^k` |
| **Flakiness** | Gap between capability and reliability | `passAtK - passExpK` |
| **Quality** (scores) | Aggregate grader scores across trials | avg/median/p25/p75 (only with grader) |
| **Performance** (latency) | Aggregate trial durations | p50/p90/p99/mean/min/max (always present) |

### Built-in Comparison Strategies

**For CaptureResult (single-run):**

| Strategy | Description | Env Vars |
|----------|-------------|----------|
| `weighted` (default) | Quality, latency, reliability | `COMPARE_QUALITY`, `COMPARE_LATENCY`, `COMPARE_RELIABILITY` |
| `statistical` | Bootstrap for confidence intervals | `COMPARE_BOOTSTRAP_ITERATIONS` |
| `custom` | Your own grader | `--grader path` |

**For TrialResult (multi-run):**

| Strategy | Description | Env Vars |
|----------|-------------|----------|
| `weighted` (default) | Capability, reliability, consistency | `COMPARE_CAPABILITY`, `COMPARE_RELIABILITY`, `COMPARE_CONSISTENCY` |
| `statistical` | Bootstrap passAtK confidence intervals | `COMPARE_BOOTSTRAP_ITERATIONS` |
| `custom` | Your own grader | `--grader path` |

### Comparison Report Output

**CaptureResult format** outputs `ComparisonReport`:

```json
{
  "meta": { "generatedAt": "...", "runs": ["baseline", "variant"], "promptCount": 100 },
  "quality": { "baseline": { "avgScore": 0.85, "passRate": 0.82 }, "variant": { ... } },
  "performance": { "baseline": { "latency": { "p50": 1200, "p90": 3400 } }, ... },
  "reliability": { "baseline": { "type": "run", "toolErrors": 5, "completionRate": 0.99 }, ... },
  "headToHead": { "pairwise": [{ "runA": "baseline", "runB": "variant", "aWins": 35, "bWins": 55 }] }
}
```

With `--strategy statistical`, quality and performance metrics include 95% confidence intervals:

```json
{
  "quality": {
    "baseline": {
      "avgScore": 0.85,
      "passRate": 0.82,
      "confidenceIntervals": {
        "avgScore": [0.82, 0.88],
        "passRate": [0.79, 0.85]
      }
    }
  },
  "performance": {
    "baseline": {
      "latency": { "p50": 1200, "mean": 1350 },
      "confidenceIntervals": {
        "latencyMean": [1280, 1420]
      }
    }
  }
}
```

**TrialResult format** outputs `TrialsComparisonReport`:

```json
{
  "meta": { "generatedAt": "...", "runs": ["claude", "gemini"], "promptCount": 50, "trialsPerPrompt": 5, "inputFormat": "trials" },
  "capability": { "claude": { "avgPassAtK": 0.92, "medianPassAtK": 0.95 }, "gemini": { "..." : "..." } },
  "reliability": { "claude": { "type": "trial", "avgPassExpK": 0.78, "medianPassExpK": 0.82 }, "gemini": { "..." : "..." } },
  "flakiness": { "claude": { "avgFlakiness": 0.14, "flakyPromptCount": 12 }, "gemini": { "..." : "..." } },
  "quality": { "claude": { "avgScore": 0.85, "medianScore": 0.90, "p25Score": 0.75, "p75Score": 0.95 }, "gemini": { "..." : "..." } },
  "performance": { "claude": { "latency": { "p50": 1200, "p90": 3400, "p99": 5100, "mean": 1500, "min": 800, "max": 5200 }, "totalDuration": 375000 }, "gemini": { "..." : "..." } },
  "headToHead": {
    "capability": [{ "runA": "claude", "runB": "gemini", "aWins": 28, "bWins": 18, "ties": 4 }],
    "reliability": ["..."],
    "overall": ["..."]
  }
}
```

**Notes:**
- `quality` is only present when a grader was used (trials have `score` fields)
- `performance` is always present (every trial has `duration`)

With `--strategy statistical`, capability, reliability, quality, and performance metrics include 95% confidence intervals:

```json
{
  "capability": {
    "claude": {
      "avgPassAtK": 0.92,
      "confidenceIntervals": { "avgPassAtK": [0.88, 0.95] }
    }
  },
  "reliability": {
    "claude": {
      "type": "trial",
      "avgPassExpK": 0.78,
      "confidenceIntervals": { "avgPassExpK": [0.72, 0.84] }
    }
  },
  "quality": {
    "claude": {
      "avgScore": 0.85,
      "confidenceIntervals": { "avgScore": [0.82, 0.88] }
    }
  },
  "performance": {
    "claude": {
      "latency": { "mean": 1500 },
      "confidenceIntervals": { "latencyMean": [1380, 1620] }
    }
  }
}
```

See [comparison-graders.md](references/comparison-graders.md) for complete comparison grader documentation including LLM-as-Judge patterns.

### Comparison Grader Interface

**CaptureResult grader:**

```typescript
import type { ComparisonGrader } from '@plaited/agent-eval-harness/pipeline'

export const grade: ComparisonGrader = async ({ id, input, hint, runs }) => {
  // runs is Record<string, { output, trajectory?, score?, duration?, toolErrors? }>
  return {
    rankings: [
      { run: 'with-mcp', rank: 1, score: 0.9 },
      { run: 'vanilla', rank: 2, score: 0.7 },
    ],
    reasoning: 'MCP run produced more accurate output'
  }
}
```

**TrialResult grader:**

```typescript
import type { TrialsComparisonGrader } from '@plaited/agent-eval-harness/pipeline'

export const grade: TrialsComparisonGrader = async ({ id, input, hint, runs }) => {
  // runs is Record<string, { passAtK?, passExpK?, k, trials }>
  // Each trial in trials has: { duration, score?, pass?, output, trajectory }
  return {
    rankings: [
      { run: 'claude', rank: 1, score: 0.92 },
      { run: 'gemini', rank: 2, score: 0.85 },
    ],
    reasoning: 'Claude has higher reliability with lower flakiness'
  }
}
```

### Pipeline Workflow Diagram

```mermaid
flowchart LR
    Prompts["prompts.jsonl"] --> Run["run"]
    Schema["headless schema"] --> Run
    Run --> Raw["raw.jsonl"]
    Raw --> Extract["extract"]
    Schema --> Extract
    Extract --> Extracted["extracted.jsonl"]
    Extracted --> Grade["grade"]
    Grader["grader.ts"] --> Grade
    Grade --> Graded["graded.jsonl"]
    Graded --> Format["format"]
    Format --> Output["report.md / .csv / .jsonl"]

    Graded --> Compare["compare"]
    Results2["other runs..."] --> Compare
    CompareGrader["compare-grader.ts"] --> Compare
    Compare --> Comparison["comparison.jsonl"]
```

## Schemas Command

Export JSON schemas for non-TypeScript tools.

```bash
# List available schemas
bunx @plaited/agent-eval-harness schemas

# Export all schemas as JSON
bunx @plaited/agent-eval-harness schemas --json -o schemas.json

# Export specific schema
bunx @plaited/agent-eval-harness schemas CaptureResult --json
bunx @plaited/agent-eval-harness schemas TrialResult --json
bunx @plaited/agent-eval-harness schemas GraderResult --json
```

### Available Schemas

| Schema | Description |
|--------|-------------|
| `CaptureResult` | Single capture output (id, input, output, trajectory, timing) |
| `TrialResult` | Multi-run trial output (includes passAtK, passExpK) |
| `GraderResult` | Grader return value (pass, score, reasoning) |
| `PromptInput` | Input prompt format |
| `TrajectoryStep` | Single step in trajectory array |
| `SummaryResult` | Compact summary format |

### Usage in Other Languages

Export schemas for validation in Python, Go, etc.:

```bash
# Export all schemas
bunx @plaited/agent-eval-harness schemas --json -o schemas.json

# Use in Python with jsonschema
python -c "
import json
from jsonschema import validate

with open('schemas.json') as f:
    schemas = json.load(f)

with open('results.jsonl') as f:
    for line in f:
        result = json.loads(line)
        validate(result, schemas['CaptureResult'])
        print(f'{result[\"id\"]}: valid')
"
```

## Grader Interface

Graders provide semantic pass/fail scoring for captured trajectories. The harness supports graders written in **any language**.

### Git-Based Grading (Recommended for Coding Tasks)

**Grade outcomes, not paths.** Use the optional `cwd` parameter to detect environmental changes with git:

```typescript
// git-grader.ts
import type { Grader } from '@plaited/agent-eval-harness/schemas'

export const grade: Grader = async ({ output, hint, cwd }) => {
  if (!cwd) return { pass: false, score: 0, reasoning: 'No cwd' }
  
  // Detect file changes
  const status = await Bun.$`git -C ${cwd} status --porcelain`.text()
  const filesCreated = status
    .split('\n')
    .filter(line => line.startsWith('??'))
    .map(line => line.slice(3).trim())
  
  // Verify tests pass
  const testResult = await Bun.$`cd ${cwd} && bun test`.nothrow()
  
  return {
    pass: filesCreated.length > 0 && testResult.exitCode === 0,
    score: testResult.exitCode === 0 ? 1 : 0,
    reasoning: `Files: ${filesCreated.join(', ')}. Tests: ${testResult.exitCode === 0 ? 'pass' : 'fail'}`,
    outcome: {  // Optional: structured data for analysis
      filesCreated,
      testsPassed: testResult.exitCode === 0,
      type: 'file_creation_with_tests'
    }
  }
}
```

See [inline-graders.md](references/inline-graders.md#git-based-outcome-grading) for comprehensive git-based grading patterns.

### Output-Based Grading (General Purpose)

```typescript
// my-grader.ts
import type { Grader } from '@plaited/agent-eval-harness/schemas'

export const grade: Grader = async ({ input, output, hint, trajectory }) => {
  const pass = output.toLowerCase().includes(hint?.toLowerCase() ?? '')
  return {
    pass,
    score: pass ? 1 : 0,
    reasoning: pass ? 'Contains hint content' : 'Missing hint content'
  }
}
```

**Note:** `input` can be `string` (single turn) or `string[]` (multi-turn). The `hint` field provides grader context (renamed from `expected`).

### Python/Executable Graders

Any executable can be a grader using stdin/stdout JSON protocol:

```python
#!/usr/bin/env python3
import json, sys

data = json.load(sys.stdin)
output = data.get("output", "").lower()
hint = (data.get("hint") or "").lower()

pass_result = hint in output if hint else True
print(json.dumps({
    "pass": pass_result,
    "score": 1.0 if pass_result else 0.0,
    "reasoning": "Contains hint" if pass_result else "Missing hint"
}))
```

```bash
chmod +x ./grader.py
bunx @plaited/agent-eval-harness capture prompts.jsonl --schema ./claude.json --grader ./grader.py -o results.jsonl
```

See [inline-graders.md](references/inline-graders.md) for complete grader documentation including LLM-as-Judge patterns.

## Input Format

Each line in `prompts.jsonl`:

```jsonl
{"id":"test-001","input":"Create a button","hint":"should contain <button>"}
{"id":"test-002","input":["Create a button","Make it blue"],"metadata":{"category":"ui"}}
```

| Field | Required | Description |
|-------|----------|-------------|
| `id` | Yes | Unique identifier |
| `input` | Yes | Single prompt (string) or conversation turns (string[]) |
| `hint` | No | Grader context - what to look for (not strict match) |
| `reference` | No | Reference solution (for validate-refs) |
| `metadata` | No | Tags, category, difficulty for filtering |
| `timeout` | No | Override default timeout for this prompt |

**Session behavior:** Each JSONL entry = 1 fresh session
- `input: string` → 1 session, 1 prompt
- `input: string[]` → 1 session, N prompts (sequential turns)

## Output Format

Full trajectory JSONL (always):

```jsonl
{
  "id": "test-001",
  "input": "Find the CEO of Anthropic",
  "output": "The CEO of Anthropic is Dario Amodei.",
  "hint": "should mention Dario Amodei",
  "trajectory": [
    {"type": "thought", "content": "I'll search for this...", "timestamp": 100},
    {"type": "tool_call", "name": "WebSearch", "status": "completed", "input": {...}, "output": {...}, "duration": 500},
    {"type": "message", "content": "The CEO of Anthropic is Dario Amodei.", "timestamp": 700}
  ],
  "metadata": {
    "category": "search",
    "agent": "--schema ./claude.json",
    "trajectoryRichness": "full",
    "turnCount": 1
  },
  "timing": {
    "start": 1704067200000,
    "end": 1704067201234,
    "firstResponse": 100,
    "sessionCreation": 234,
    "total": 1234,
    "inputTokens": 150,
    "outputTokens": 85
  },
  "toolErrors": false
}
```

### Output Fields

| Field | Description |
|-------|-------------|
| `input` | Original prompt (string or string[] for multi-turn) |
| `hint` | Grader context hint (if provided) |
| `metadata.trajectoryRichness` | `"full"` \| `"messages-only"` \| `"minimal"` |
| `metadata.turnCount` | Number of conversation turns (1 for string, N for array) |
| `timing.sessionCreation` | Time to create session (ms) |
| `timing.total` | Total duration (end - start) |
| `timing.inputTokens` | Input tokens consumed (if available from adapter) |
| `timing.outputTokens` | Output tokens generated (if available from adapter) |
| `toolErrors` | Whether any tool calls failed |

**Note:** `toolErrors` replaces misleading `status: 'passed'|'failed'`. Real pass/fail comes from YOUR grader.

## Schema Exports

Consumers can import Zod schemas directly:

```typescript
import { CaptureResultSchema, TrialResultSchema } from '@plaited/agent-eval-harness/schemas'

// Validate external data
const result = CaptureResultSchema.parse(jsonData)

// Generate JSON Schema (Zod 4 native)
import { z } from 'zod'
const jsonSchema = z.toJSONSchema(CaptureResultSchema)
```

### Discriminated Unions for Reliability Metrics

Reliability metrics include a `type` discriminator for type-safe parsing:

```typescript
import { z } from 'zod'
import {
  ReliabilityMetricsSchema,       // type: 'run'
  TrialsReliabilityMetricsSchema  // type: 'trial'
} from '@plaited/agent-eval-harness/schemas'

// Create a unified schema for both metric types
const UnifiedReliabilitySchema = z.discriminatedUnion('type', [
  ReliabilityMetricsSchema,
  TrialsReliabilityMetricsSchema,
])

// Type-safe parsing with automatic narrowing
const metrics = UnifiedReliabilitySchema.parse(data)
if (metrics.type === 'run') {
  // TypeScript knows: ReliabilityMetrics
  console.log(metrics.toolErrors, metrics.completionRate)
} else {
  // TypeScript knows: TrialsReliabilityMetrics
  console.log(metrics.avgPassExpK, metrics.medianPassExpK)
}
```

Or export JSON schemas for non-TypeScript tools:

```bash
bunx @plaited/agent-eval-harness schemas --json -o schemas.json
bunx @plaited/agent-eval-harness schemas CaptureResult --json
```

## Execution Environment

**Recommendation:** Run the harness in Docker containers for consistent, isolated execution.

```bash
# Run integration tests via Docker
docker compose -f docker-compose.test.yml run --rm test

# Or with explicit API keys
ANTHROPIC_API_KEY=sk-... GEMINI_API_KEY=... docker compose -f docker-compose.test.yml run --rm test
```

### Docker Requirements

| Requirement | Reason |
|-------------|--------|
| **Node.js 24+** | Gemini CLI uses modern JS features (optional chaining) |
| **Non-root user** | Claude CLI blocks `--dangerously-skip-permissions` as root |
| **Gemini API key** | Pass `GEMINI_API_KEY` for Gemini CLI |

See [docker-evals.md](references/docker-evals.md) for complete Docker setup guide, debugging tips, and CI integration patterns.

### Multi-turn Conversations

Use `input: string[]` to execute multi-turn conversations within a single session:

```jsonl
{"id":"context-001","input":["Remember this number: 42","What number did I ask you to remember?"],"hint":"42"}
{"id":"context-002","input":["My name is Alice","What is my name?"],"hint":"Alice"}
```

Run with the headless adapter:

```bash
# Using Claude Code via headless adapter
bunx @plaited/agent-eval-harness capture multi-turn.jsonl \
  bunx @plaited/agent-eval-harness headless --schema ./claude-headless.json \
  -o results.jsonl

# Using Gemini CLI via headless adapter
GEMINI_API_KEY=... bunx @plaited/agent-eval-harness capture multi-turn.jsonl \
  bunx @plaited/agent-eval-harness headless --schema ./gemini-headless.json \
  -o results.jsonl
```

**Key points:**
- Each JSONL entry = 1 fresh session
- `input: string[]` sends sequential turns to the **same session**
- Works with both `stream` mode (Claude) and `iterative` mode (Gemini)
- The adapter handles context preservation automatically

## Downstream Integration

The harness outputs standard JSONL that pipes to any tool:

```bash
# Filter with jq
cat results.jsonl | jq 'select(.metadata.category == "ui")'

# Count tool usage
cat results.jsonl | jq -s 'map(.trajectory | map(select(.type == "tool_call")) | length) | add'

# Summarize for quick analysis
bunx @plaited/agent-eval-harness summarize results.jsonl -o summary.jsonl

# Compare runs with built-in strategies
bunx @plaited/agent-eval-harness compare run1.jsonl run2.jsonl -o comparison.json
```

## Quick Reference

| Resource | Description |
|----------|-------------|
| `bunx @plaited/agent-eval-harness` | CLI help |
| [output-formats.md](references/output-formats.md) | JSONL schemas, command details |
| [inline-graders.md](references/inline-graders.md) | Single input/output graders (TypeScript, Python, shell) |
| [comparison-graders.md](references/comparison-graders.md) | Comparison strategies (weighted, statistical, LLM-as-Judge) |
| [calibration.md](references/calibration.md) | Grader calibration workflow |
| [eval-concepts.md](references/eval-concepts.md) | Evaluation concepts (pass@k, pass^k) |
| [docker-evals.md](references/docker-evals.md) | Docker setup, debugging, CI integration |

## Related

- **[headless-adapters skill](../headless-adapters/SKILL.md)** - Schema-driven adapters for headless CLI agents
