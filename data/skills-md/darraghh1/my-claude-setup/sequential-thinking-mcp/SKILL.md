---
name: sequential-thinking-mcp
description: "Structured multi-step reasoning via Sequential Thinking MCP. Use for complex debugging, architectural trade-offs, or root cause analysis."
metadata:
  version: 1.0.0
  mcp-server: sequential-thinking
---

# Sequential Thinking — Structured Reasoning

You are an expert at using the Sequential Thinking MCP server for structured, revisable multi-step reasoning. This tool helps decompose complex problems into numbered thoughts with support for revision and branching.

## Critical: These Are Direct Tool Calls

MCP tools are **direct tool calls** — exactly like `Read`, `Grep`, or `Bash`. They are NOT CLI commands.

**CORRECT** — call the tool directly:
```
Tool: mcp__sequential-thinking__sequentialthinking
Parameters: {
  "thought": "First, let me identify the possible causes of the RLS policy failure...",
  "thoughtNumber": 1,
  "totalThoughts": 5,
  "nextThoughtNeeded": true
}
```

**WRONG** — do NOT shell out:
```
Bash: claude mcp call sequential-thinking sequentialthinking ...  # This does not work
```

The single tool uses the `mcp__sequential-thinking__sequentialthinking` prefix.

## When to Use (and When NOT to)

| Use Sequential Thinking | Do NOT Use |
|------------------------|------------|
| Bug with 3+ possible causes needing elimination | Simple typo or obvious error |
| Architectural decision with competing trade-offs | Straightforward implementation |
| Multi-factor analysis where factors interact | Single-factor decision |
| Root cause analysis requiring hypothesis testing | Error with clear stack trace |
| Problems where early assumptions might be wrong | Problems with known solutions |

**Rule of thumb:** If you can solve it in your head in one step, don't use this tool. If you need to "think out loud" with potential backtracking, use it.

## Tool Parameters

| Parameter | Type | Required | Purpose |
|-----------|------|----------|---------|
| `thought` | string | Yes | The content of this reasoning step |
| `thoughtNumber` | number | Yes | Current step number (1-indexed) |
| `totalThoughts` | number | Yes | Estimated total steps (can adjust) |
| `nextThoughtNeeded` | boolean | Yes | `true` to continue, `false` when done |
| `isRevision` | boolean | No | `true` if revising an earlier thought |
| `revisesThought` | number | No | Which thought number is being revised |
| `branchFromThought` | number | No | Start an alternative path from this thought |
| `branchId` | string | No | Label for the branch (e.g., "alternative-approach") |
| `needsMoreThoughts` | boolean | No | `true` to extend beyond initial estimate |

## Workflow 1: Problem Decomposition

**Trigger:** Complex bug with multiple possible causes, or a decision requiring systematic analysis.

### Steps

1. **Frame the problem** (thought 1):
   ```
   sequentialthinking({
     thought: "The timesheet approval is failing silently. Three possible causes: (1) RLS policy blocking the update, (2) has_permission() returning false, (3) trigger rejecting the state transition.",
     thoughtNumber: 1,
     totalThoughts: 5,
     nextThoughtNeeded: true
   })
   ```

2. **Analyze each hypothesis** (thoughts 2-4):
   ```
   sequentialthinking({
     thought: "Testing hypothesis 1: The RLS policy for timesheets requires has_role_on_account(account_id) AND the user must be manager_or_above. Let me check if the user has the right role...",
     thoughtNumber: 2,
     totalThoughts: 5,
     nextThoughtNeeded: true
   })
   ```

3. **Revise if earlier thinking was wrong** (optional):
   ```
   sequentialthinking({
     thought: "Revising thought 2: Actually, the new permission system uses has_permission() not has_role_on_account(). The RLS policy might be using the old function.",
     thoughtNumber: 4,
     totalThoughts: 6,
     nextThoughtNeeded: true,
     isRevision: true,
     revisesThought: 2,
     needsMoreThoughts: true
   })
   ```

4. **Conclude** (final thought):
   ```
   sequentialthinking({
     thought: "Root cause identified: The RLS policy uses has_role_on_account() which checks system roles, but the user only has a custom role assigned. Need to update the policy to use has_permission() instead.",
     thoughtNumber: 6,
     totalThoughts: 6,
     nextThoughtNeeded: false
   })
   ```

## Workflow 2: Architectural Decision

**Trigger:** User asks "should we use X or Y?", "what's the best approach for Z?", or there are multiple valid implementation strategies.

### Steps

1. **Define the decision criteria** (thought 1)
2. **Evaluate option A** against criteria (thought 2)
3. **Evaluate option B** against criteria (thought 3)
4. **Branch if a hybrid approach emerges** (optional):
   ```
   sequentialthinking({
     thought: "What if we combine the service pattern from option A with the caching strategy from option B?",
     thoughtNumber: 4,
     totalThoughts: 6,
     nextThoughtNeeded: true,
     branchFromThought: 3,
     branchId: "hybrid-approach"
   })
   ```
5. **Recommend with trade-off summary** (final thought)

## Workflow 3: Multi-Factor Analysis

**Trigger:** Complex decision involving performance, security, maintainability, and other competing concerns.

### Pattern

- **Thought 1:** List all factors and their relative importance
- **Thoughts 2-N:** Analyze each factor independently
- **Revision thoughts:** Update earlier analysis as new interactions between factors emerge
- **Final thought:** Synthesize into a recommendation with explicit trade-offs

## Key Patterns

- **Start with an estimate of `totalThoughts`** — 5 is a good default. Adjust with `needsMoreThoughts: true` if you need more.
- **Use `isRevision: true`** when you realize an earlier thought was wrong or incomplete — don't just silently change direction.
- **Use `branchFromThought`** to explore "what if?" alternatives without abandoning the main analysis.
- **Set `nextThoughtNeeded: false`** only when you have a clear conclusion — not just when you run out of thoughts.
- **Each thought should be substantive** — avoid placeholder thoughts like "Let me think about this more."

## Troubleshooting

### Reasoning Chain Gets Too Long

If you're past thought 10 and still going:
1. Set `nextThoughtNeeded: false` and summarize what you know so far
2. The problem might need breaking into sub-problems — solve each separately
3. Consider if you actually need this tool or if the problem is simpler than you thought

### Losing Track of the Thread

Use `isRevision` and `revisesThought` to explicitly connect corrections to earlier thoughts. This helps maintain a coherent chain rather than just appending unconnected thoughts.

### Tool Seems Unnecessary for This Problem

If you find yourself forcing sequential thinking on a straightforward problem, just stop and solve it directly. This tool adds value for genuinely complex reasoning — not for every problem.
