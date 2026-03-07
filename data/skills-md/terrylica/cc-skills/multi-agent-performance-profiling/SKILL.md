---
name: multi-agent-performance-profiling
description: Multi-agent performance profiling for pipeline bottlenecks. TRIGGERS - performance profiling, bottleneck analysis, pipeline optimization.
allowed-tools: Bash, Read, Write, Glob, Grep
---

# Multi-Agent Performance Profiling

## Overview

Prescriptive workflow for spawning parallel profiling agents to comprehensively identify performance bottlenecks across multiple system layers. Successfully discovered that QuestDB ingests at 1.1M rows/sec (11x faster than target), proving database was NOT the bottleneck - CloudFront download was 90% of pipeline time.

## When to Use This Skill

Use this skill when:

- Performance below SLO (e.g., 47K vs 100K rows/sec target)
- Multi-stage pipeline optimization (download → extract → parse → ingest)
- Database performance investigation
- Bottleneck identification in complex workflows
- Pre-optimization analysis (before making changes)

**Key outcomes:**

- Identify true bottleneck (vs assumed bottleneck)
- Quantify each stage's contribution to total time
- Prioritize optimizations by impact (P0/P1/P2)
- Avoid premature optimization of non-bottlenecks

## Core Methodology

### 1. Multi-Layer Profiling Model (5-Agent Pattern)

**Agent 1: Profiling (Instrumentation)**

- Empirical timing of each pipeline stage
- Phase-boundary instrumentation with time.perf_counter()
- Memory profiling (peak usage, allocations)
- Bottleneck identification (% of total time)

**Agent 2: Database Configuration Analysis**

- Server settings review (WAL, heap, commit intervals)
- Production vs development config comparison
- Expected impact quantification (<5%, 10%, 50%)

**Agent 3: Client Library Analysis**

- API usage patterns (dataframe vs row-by-row)
- Buffer size tuning opportunities
- Auto-flush behavior analysis

**Agent 4: Batch Size Analysis**

- Current batch size validation
- Optimal batch range determination
- Memory overhead vs throughput tradeoff

**Agent 5: Integration & Synthesis**

- Consensus-building across agents
- Prioritization (P0/P1/P2) with impact quantification
- Implementation roadmap creation

### 2. Agent Orchestration Pattern

**Parallel Execution** (all 5 agents run simultaneously):

```
Agent 1 (Profiling)          → [PARALLEL]
Agent 2 (DB Config)          → [PARALLEL]
Agent 3 (Client Library)     → [PARALLEL]
Agent 4 (Batch Size)         → [PARALLEL]
Agent 5 (Integration)        → [PARALLEL - reads tmp/ outputs from others]
```

**Key Principle**: No dependencies between investigation agents (1-4). Integration agent synthesizes findings.

**Dynamic Todo Management:**

- Start with investigation plan (5 agents)
- Spawn agents in parallel using single message with multiple Task tool calls
- Update todos as each agent completes
- Integration agent waits for all findings before synthesizing

### 3. Profiling Script Structure

Each agent produces:

1. **Investigation Script** (e.g., `profile_pipeline.py`)
   - time.perf_counter() instrumentation at phase boundaries
   - Memory profiling with tracemalloc
   - Structured output (phase, duration, % of total)
2. **Report** (markdown with findings, recommendations, impact quantification)
3. **Evidence** (benchmark results, config dumps, API traces)

**Example Profiling Code:**

```python
import time

# Profile multi-stage pipeline
def profile_pipeline():
    results = {}

    # Phase 1: Download
    start = time.perf_counter()
    data = download_from_cdn(url)
    results["download"] = time.perf_counter() - start

    # Phase 2: Extract
    start = time.perf_counter()
    csv_data = extract_zip(data)
    results["extract"] = time.perf_counter() - start

    # Phase 3: Parse
    start = time.perf_counter()
    df = parse_csv(csv_data)
    results["parse"] = time.perf_counter() - start

    # Phase 4: Ingest
    start = time.perf_counter()
    ingest_to_db(df)
    results["ingest"] = time.perf_counter() - start

    # Analysis
    total = sum(results.values())
    for phase, duration in results.items():
        pct = (duration / total) * 100
        print(f"{phase}: {duration:.3f}s ({pct:.1f}%)")

    return results
```

### 4. Impact Quantification Framework

**Priority Levels:**

- **P0 (Critical)**: >5x improvement, addresses primary bottleneck
- **P1 (High)**: 2-5x improvement, secondary optimizations
- **P2 (Medium)**: 1.2-2x improvement, quick wins
- **P3 (Low)**: <1.2x improvement, minor tuning

**Impact Reporting Format:**

```markdown
### Recommendation: [Optimization Name] (P0/P1/P2) - [IMPACT LEVEL]

**Impact**: 🔴/🟠/🟡 **Nx improvement**
**Effort**: High/Medium/Low (N days)
**Expected Improvement**: CurrentK → TargetK rows/sec

**Rationale**:

- [Why this matters]
- [Supporting evidence from profiling]
- [Comparison to alternatives]

**Implementation**:
[Code snippet or architecture description]
```

### 5. Consensus-Building Pattern

**Integration Agent Responsibilities:**

1. Read all investigation reports (Agents 1-4)
2. Identify consensus recommendations (all agents agree)
3. Flag contradictions (agents disagree)
4. Synthesize master integration report
5. Create implementation roadmap (P0 → P1 → P2)

**Consensus Criteria:**

- ≥3/4 agents recommend same optimization → Consensus
- 2/4 agents recommend, 2/4 neutral → Investigate further
- Agents contradict (one says "optimize X", another says "X is not bottleneck") → Run tie-breaker experiment

## Workflow: Step-by-Step

### Step 1: Define Performance Problem

**Input**: Performance metric below SLO
**Output**: Problem statement with baseline metrics

**Example Problem Statement:**

```
Performance Issue: BTCUSDT 1m ingestion at 47K rows/sec
Target SLO: >100K rows/sec
Gap: 53% below target
Pipeline: CloudFront download → ZIP extract → CSV parse → QuestDB ILP ingest
```

### Step 2: Create Investigation Plan

**Directory Structure:**

```
tmp/perf-optimization/
  profiling/              # Agent 1
    profile_pipeline.py
    PROFILING_REPORT.md
  questdb-config/         # Agent 2
    CONFIG_ANALYSIS.md
  python-client/          # Agent 3
    CLIENT_ANALYSIS.md
  batch-size/             # Agent 4
    BATCH_ANALYSIS.md
  MASTER_INTEGRATION_REPORT.md  # Agent 5
```

**Agent Assignment:**

- Agent 1: Empirical profiling (instrumentation)
- Agent 2: Database configuration analysis
- Agent 3: Client library usage analysis
- Agent 4: Batch size optimization analysis
- Agent 5: Synthesis and integration

### Step 3: Spawn Agents in Parallel

**IMPORTANT**: Use single message with multiple Task tool calls for true parallelism

**Example:**

```
I'm going to spawn 5 parallel investigation agents:

[Uses Task tool 5 times in a single message]
- Agent 1: Profiling
- Agent 2: QuestDB Config
- Agent 3: Python Client
- Agent 4: Batch Size
- Agent 5: Integration (depends on others completing)
```

**Execution:**

```bash
# All agents run simultaneously (user observes 5 parallel tool calls)
# Each agent writes to its own tmp/ subdirectory
# Integration agent polls for completed reports
```

### Step 4: Wait for All Agents to Complete

**Progress Tracking:**

- Update todo list as each agent completes
- Integration agent polls tmp/ directory for report files
- Once 4/4 investigation reports exist → Integration agent synthesizes

**Completion Criteria:**

- All 4 investigation reports written
- Integration report synthesizes findings
- Master recommendations list created

### Step 5: Review Master Integration Report

**Report Structure:**

```markdown
# Master Performance Optimization Integration Report

## Executive Summary

- Critical discovery (what is/isn't the bottleneck)
- Key findings from each agent (1-sentence summary)

## Top 3 Recommendations (Consensus)

1. [P0 Optimization] - HIGHEST IMPACT
2. [P1 Optimization] - HIGH IMPACT
3. [P2 Optimization] - QUICK WIN

## Agent Investigation Summary

### Agent 1: Profiling

### Agent 2: Database Config

### Agent 3: Client Library

### Agent 4: Batch Size

## Implementation Roadmap

### Phase 1: P0 Optimizations (Week 1)

### Phase 2: P1 Optimizations (Week 2)

### Phase 3: P2 Quick Wins (As time permits)
```

### Step 6: Implement Optimizations (P0 First)

**For each recommendation:**

1. Implement highest-priority optimization (P0)
2. Re-run profiling script
3. Verify expected improvement achieved
4. Update report with actual results
5. Move to next priority (P1, P2, P3)

**Example Implementation:**

```bash
# Before optimization
uv run python tmp/perf-optimization/profiling/profile_pipeline.py
# Output: 47K rows/sec, download=857ms (90%)

# Implement P0 recommendation (concurrent downloads)
# [Make code changes]

# After optimization
uv run python tmp/perf-optimization/profiling/profile_pipeline.py
# Output: 450K rows/sec, download=90ms per symbol * 10 concurrent (90%)
```

## Real-World Example: QuestDB Refactor Performance Investigation

**Context**: Pipeline achieving 47K rows/sec, target 100K rows/sec (53% below SLO)

**Assumptions Before Investigation:**

- QuestDB ILP ingestion is the bottleneck (4% of time)
- Need to tune database configuration
- Need to optimize Sender API usage

**Findings After 5-Agent Investigation:**

1. **Profiling Agent**: CloudFront download is 90% of time (857ms), ILP ingest only 4% (40ms)
2. **QuestDB Config Agent**: Database already optimal, tuning provides <5% improvement
3. **Python Client Agent**: Sender API already optimal (using dataframe() bulk ingestion)
4. **Batch Size Agent**: 44K batch size is within optimal range
5. **Integration Agent**: Consensus recommendation - optimize download, NOT database

**Top 3 Recommendations:**

1. 🔴 **P0**: Concurrent multi-symbol downloads (10-20x improvement)
2. 🟠 **P1**: Multi-month pipeline parallelism (2x improvement)
3. 🟡 **P2**: Streaming ZIP extraction (1.3x improvement)

**Impact**: Discovered database ingests at 1.1M rows/sec (11x faster than target) - proving database was never the bottleneck

**Outcome**: Avoided wasting 2-3 weeks optimizing database when download was the real bottleneck

## Common Pitfalls

### 1. Profiling Only One Layer

❌ **Bad**: Profile database only, assume it's the bottleneck
✅ **Good**: Profile entire pipeline (download → extract → parse → ingest)

### 2. Serial Agent Execution

❌ **Bad**: Run Agent 1, wait, then run Agent 2, wait, etc.
✅ **Good**: Spawn all 5 agents in parallel using single message with multiple Task calls

### 3. Optimizing Without Profiling

❌ **Bad**: "Let's optimize the database config first" (assumption-driven)
✅ **Good**: Profile first, discover database is only 4% of time, optimize download instead

### 4. Ignoring Low-Hanging Fruit

❌ **Bad**: Only implement P0 (highest impact, highest effort)
✅ **Good**: Implement P2 quick wins (1.3x for 4-8 hours effort) while planning P0

### 5. Not Re-Profiling After Changes

❌ **Bad**: Implement optimization, assume it worked
✅ **Good**: Re-run profiling script, verify expected improvement achieved

## Resources

### scripts/

Not applicable - profiling scripts are project-specific (stored in `tmp/perf-optimization/`)

### references/

- `profiling_template.py` - Template for phase-boundary instrumentation
- `integration_report_template.md` - Template for master integration report
- `impact_quantification_guide.md` - How to assess P0/P1/P2 priorities

### assets/

Not applicable - profiling artifacts are project-specific

---

## Troubleshooting

| Issue                       | Cause                     | Solution                                            |
| --------------------------- | ------------------------- | --------------------------------------------------- |
| Agents running sequentially | Using separate messages   | Spawn all agents in single message with multi-Task  |
| Integration report empty    | Agent reports not written | Wait for all 4 investigation agents to complete     |
| Wrong bottleneck identified | Single-layer profiling    | Profile entire pipeline, not just assumed layer     |
| Profiling results vary      | No warmup runs            | Run 3-5 warmup iterations before measuring          |
| Memory not profiled         | Missing tracemalloc       | Add tracemalloc instrumentation to profiling script |
| P0/P1 priority unclear      | No impact quantification  | Include expected Nx improvement for each finding    |
| Consensus missing           | Agents not compared       | Integration agent must synthesize all 4 reports     |
| Re-profile shows no change  | Caching effects           | Clear caches, restart services before re-profiling  |
