---
name: speed-loop
description: A structured framework for optimizing complex data processing systems through systematic speed loops. Use when you need to improve performance of data-intensive applications.
---

# Speed Loop Framework

A systematic approach to optimizing complex data processing systems while maintaining correctness.

## Quick Flow

```
START
 │
 │ 1. Read references/start.txt
 │ 2. Create 10 Optimization Commandments for your codebase
 │ 3. Read sacred_rules.md + phase_rules/*
 ▼
┌────────────────────────────────────────────────────────────────────┐
│                    SPEED LOOP                                      │
│                                                                    │
│  Phase1 ──► Phase2 ──► Phase3 ──► Phase4 ──► Phase5 ──► Phase6     │
│  Understand  Decompose   Analyze   Implement  Verify    Integrate  │
│       ▲                                                            │
│       └────────────────────────────────────────────────────────────┤
│             REPEAT (one optimization per iteration)                │
└────────────────────────────────────────────────────────────────────┘
```

## When to Use

- Improving performance of data processing pipelines
- Optimizing database queries or data transformations
- Need a structured methodology for performance improvements
- Want to measure and verify optimizations scientifically

## Sacred Rules

See `references/sacred_rules.md` - These are **INVIOLABLE**:

1. **Output Integrity Must Be Preserved** - Same inputs must produce same outputs
2. **Verification Checkpoints Are Mandatory** - Every optimization must be measured
3. **Speed Gains Without Correctness Are Rejected** - Wrong results = failure
4. **Test Environment Isolation** - Test in isolation before integration
5. **One Optimization Per Iteration** - Isolate variables
6. **Document Everything** - Future iterations depend on documentation
7. **Rollback Readiness** - Every change must be reversible

## The Six Phases

See `references/phase_rules/` for detailed phase instructions:

### Phase 1: Understand
- Identify fundamental pieces of the system
- Read current implementation
- Establish baseline metrics

### Phase 2: Decompose
- Break down each component into sub-components
- Identify costs (time, complexity, allocations)
- Rank optimization opportunities

### Phase 3: Analyze
- Select top candidates
- Deep dive analysis
- Design verification approach

### Phase 4: Implement
- Set up isolated test environment
- Add checkpoint instrumentation
- Implement one optimization

### Phase 5: Verify
- Output integrity verification
- Performance measurement
- Statistical significance

### Phase 6: Integrate
- Apply verified changes to main codebase
- Create commits and tags
- Archive loop artifacts

## Getting Started

See `references/start.txt` for agent instructions:

1. Conduct web research on optimizing data systems
2. Create The 10 Optimization Commandments document
3. Read sacred rules and phase rules
4. Begin first iteration with Phase 1

## Key Principles

- **Correctness First**: Same inputs must produce same outputs
- **One Optimization Per Iteration**: Isolate variables to understand impact
- **Measure Everything**: Quantitative evidence required for all improvements
- **Verify Before Integrating**: Test in isolation before main codebase changes

## Framework Agnostic

This skill is designed to work with:
- Any programming language
- Any web framework
- Any database or storage system
- Any data processing pipeline
