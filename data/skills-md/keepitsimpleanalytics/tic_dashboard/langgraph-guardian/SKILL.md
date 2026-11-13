---
name: langgraph-guardian
description: Prevent and detect code quality issues in LangGraph pipelines. Use when implementing new nodes, debugging state flow issues, troubleshooting empty state keys, or before committing LangGraph code. Triggers on phrases like "validate node", "check node implementation", "trace flow", "why is state empty", "lint langgraph", "check completeness", "validate before commit", "pre-flight check", "debug state flow", "find the bug in my node".
---

# LangGraph Guardian

Prevent silent failures and catch implementation errors in LangGraph pipelines before runtime.

## Core Problem This Solves

LangGraph's decoupled architecture causes silent failures:
- `state.get("extracted_rate")` returns `[]` when key is `"extracted_rates"` - no error
- Node A writes `provider_map`, Node B reads `provider_maps` - silent empty list
- Incomplete returns missing required keys - downstream nodes fail mysteriously
- Copy-paste errors across nodes accumulate over time

## Quick Commands

```bash
# Validate a single node
python scripts/lint_node.py src/langgraph/nodes/layer4/rate_extractor.py

# Trace a flow to find where it breaks
python scripts/trace_flow.py src/langgraph/nodes --flow "layer1,layer2,layer3"

# Check all nodes for completeness
python scripts/check_completeness.py src/langgraph/nodes

# Validate naming consistency across all nodes
python scripts/validate_naming.py src/langgraph/nodes --state-file src/langgraph/state.py

# Pre-commit validation (all checks)
python scripts/preflight.py src/langgraph/nodes --state-file src/langgraph/state.py
```

## Validation Categories

### 1. State Key Validation
- Keys used match TypedDict definition exactly
- No typos in state.get() calls
- No undeclared keys written

### 2. Flow Tracing
- Simulates state propagation through nodes
- Finds where chains break (key written in layer 4, read in layer 3)
- Detects missing dependencies

### 3. Completeness Checks
- Required error handling patterns present
- Escalation creation on failures
- All documented output keys returned
- Logging for long operations

### 4. Naming Consistency
- State keys follow conventions (snake_case, plural for lists)
- Node names match file names
- Layer IDs match directory structure

## Pre-Implementation Checklist

Before writing a new node, verify:

1. [ ] All input keys exist in `TiCPipelineState`
2. [ ] All output keys exist in `TiCPipelineState`
3. [ ] Input keys are written by earlier layers
4. [ ] Output keys are read by later layers (or are terminal)
5. [ ] Error handling returns empty + escalation, not just `{}`
6. [ ] List outputs accumulate, not overwrite

## Common Mistakes Reference

See `references/common_mistakes.md` for patterns like:
- Silent empty returns
- State key typos
- Missing await
- Overwriting vs accumulating lists
- Incomplete error handling

## Integration with Development Workflow

1. **Before implementing**: Run `trace_flow.py` to verify inputs available
2. **While implementing**: Run `lint_node.py` on save
3. **Before commit**: Run `preflight.py` for full validation
4. **When debugging**: Run `trace_flow.py --trace KEY` to find breaks
