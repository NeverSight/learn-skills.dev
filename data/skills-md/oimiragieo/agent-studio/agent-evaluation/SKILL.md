---
name: agent-evaluation
description: LLM-as-judge evaluation framework with 5-dimension rubric (accuracy, groundedness, coherence, completeness, helpfulness) for scoring AI-generated content quality with weighted composite scores and evidence citations
version: 1.2.0
model: sonnet
invoked_by: both
user_invocable: true
tools: [Read, Write, Bash, Glob, Grep]
agents: [qa, code-reviewer, reflection-agent]
category: 'Validation & Quality'
tags: [evaluation, llm-judge, quality, rubric, scoring, ai-output]
verified: true
lastVerifiedAt: '2026-03-01'
best_practices:
  - Always evaluate all 5 dimensions before computing composite score
  - Cite specific evidence from the output being evaluated for each dimension score
  - Use the weighted composite (not simple average) for final verdict
  - Pair with verification-before-completion for pre-completion quality gates
  - Document evaluation verdicts in task metadata for traceability
error_handling: graceful
streaming: supported
---

# Agent Evaluation

## Overview

LLM-as-judge evaluation framework that scores AI-generated content on 5 dimensions using a 1-5 rubric. Agents evaluate outputs, compute a weighted composite score, and emit a structured verdict with evidence citations.

**Core principle:** Systematic quality verification before claiming completion. Agent-studio currently has no way to verify agent output quality — this skill fills that gap.

## When to Use

**Always:**

- Before marking a task complete (pair with `verification-before-completion`)
- After a plan is generated (evaluate plan quality)
- After code review outputs (evaluate review quality)
- During reflection cycles (evaluate agent responses)
- When comparing multiple agent outputs

**Don't Use:**

- For binary pass/fail checks (use `verification-before-completion` instead)
- For security audits (use `security-architect` skill)
- For syntax/lint checking (use `pnpm lint:fix`)

## The 5-Dimension Rubric

Every evaluation scores all 5 dimensions on a 1-5 scale:

| Dimension        | Weight | What It Measures                                                                  |
| ---------------- | ------ | --------------------------------------------------------------------------------- |
| **Accuracy**     | 30%    | Factual correctness; no hallucinations; claims are verifiable                     |
| **Groundedness** | 25%    | Claims are supported by citations, file references, or evidence from the codebase |
| **Coherence**    | 15%    | Logical flow; internally consistent; no contradictions                            |
| **Completeness** | 20%    | All required aspects addressed; no critical gaps                                  |
| **Helpfulness**  | 10%    | Actionable; provides concrete next steps; reduces ambiguity                       |

### Scoring Scale (1-5)

| Score | Meaning                                                       |
| ----- | ------------------------------------------------------------- |
| **5** | Excellent — fully meets the dimension's criteria with no gaps |
| **4** | Good — meets criteria with minor gaps                         |
| **3** | Adequate — partially meets criteria; some gaps present        |
| **2** | Poor — significant gaps or errors in this dimension           |
| **1** | Failing — does not meet the dimension's criteria              |

## Execution Process

### Step 1: Load the Output to Evaluate

Identify what is being evaluated:

```
- Agent response (text)
- Plan document (file path)
- Code review output (text/file)
- Skill invocation result (text)
- Task completion claim (TaskGet metadata)
```

### Step 2: Score Each Dimension

For each of the 5 dimensions, provide:

1. **Score (1-5)**: The numeric score
2. **Evidence**: Direct quote or file reference from the evaluated output
3. **Rationale**: Why this score was given (1-2 sentences)

**Dimension 1: Accuracy**

```
Checklist:
- [ ] Claims are factually correct (verify against codebase if possible)
- [ ] No hallucinated file paths, function names, or API calls
- [ ] Numbers and counts are accurate
- [ ] No contradictions with existing documentation
```

**Dimension 2: Groundedness**

```
Checklist:
- [ ] Claims cite specific files, line numbers, or task IDs
- [ ] Recommendations reference observable evidence
- [ ] No unsupported assertions ("this is probably X")
- [ ] Code examples use actual project patterns
```

**Dimension 3: Coherence**

```
Checklist:
- [ ] Logical flow from problem → analysis → recommendation
- [ ] No internal contradictions
- [ ] Terminology is consistent throughout
- [ ] Steps are in a rational order
```

**Dimension 4: Completeness**

```
Checklist:
- [ ] All required aspects of the task are addressed
- [ ] Edge cases are mentioned (if relevant)
- [ ] No critical gaps that would block action
- [ ] Follow-up steps are included
```

**Dimension 5: Helpfulness**

```
Checklist:
- [ ] Provides actionable next steps (not just observations)
- [ ] Concrete enough to act on without further clarification
- [ ] Reduces ambiguity rather than adding it
- [ ] Appropriate for the intended audience
```

### Step 3: Compute Weighted Composite Score

```
composite = (accuracy × 0.30) + (groundedness × 0.25) + (completeness × 0.20) + (coherence × 0.15) + (helpfulness × 0.10)
```

### Step 4: Determine Verdict

| Composite Score | Verdict   | Action                              |
| --------------- | --------- | ----------------------------------- |
| 4.5 – 5.0       | EXCELLENT | Approve; proceed                    |
| 3.5 – 4.4       | GOOD      | Approve with minor notes            |
| 2.5 – 3.4       | ADEQUATE  | Request targeted improvements       |
| 1.5 – 2.4       | POOR      | Reject; requires significant rework |
| 1.0 – 1.4       | FAILING   | Reject; restart task                |

### Step 5: Emit Structured Verdict

Output the verdict in this format:

```markdown
## Evaluation Verdict

**Output Evaluated**: [Brief description of what was evaluated]
**Evaluator**: [Agent name / task ID]
**Date**: [ISO 8601 date]

### Dimension Scores

| Dimension     | Score | Weight | Weighted Score |
| ------------- | ----- | ------ | -------------- |
| Accuracy      | X/5   | 30%    | X.X            |
| Groundedness  | X/5   | 25%    | X.X            |
| Completeness  | X/5   | 20%    | X.X            |
| Coherence     | X/5   | 15%    | X.X            |
| Helpfulness   | X/5   | 10%    | X.X            |
| **Composite** |       |        | **X.X / 5.0**  |

### Evidence Citations

**Accuracy (X/5)**:

> [Direct quote or file:line reference]
> Rationale: [Why this score]

**Groundedness (X/5)**:

> [Direct quote or file:line reference]
> Rationale: [Why this score]

**Completeness (X/5)**:

> [Direct quote or file:line reference]
> Rationale: [Why this score]

**Coherence (X/5)**:

> [Direct quote or file:line reference]
> Rationale: [Why this score]

**Helpfulness (X/5)**:

> [Direct quote or file:line reference]
> Rationale: [Why this score]

### Verdict: [EXCELLENT | GOOD | ADEQUATE | POOR | FAILING]

**Summary**: [1-2 sentence overall assessment]

**Required Actions** (if verdict is ADEQUATE or worse):

1. [Specific improvement needed]
2. [Specific improvement needed]
```

## Usage Examples

### Evaluate a Plan Document

```javascript
// Load plan document
Read({ file_path: '.claude/context/plans/auth-design-plan-2026-02-21.md' });

// Evaluate against 5-dimension rubric
Skill({ skill: 'agent-evaluation' });
// Provide the plan content as the output to evaluate
```

### Evaluate Agent Response Before Completion

```javascript
// Agent generates implementation summary
// Before marking task complete, evaluate the summary quality
Skill({ skill: 'agent-evaluation' });
// If composite < 3.5, request improvements before TaskUpdate(completed)
```

### Evaluate Code Review Output

```javascript
// After code-reviewer runs, evaluate the review quality
Skill({ skill: 'agent-evaluation' });
// Ensures review is grounded in actual code evidence, not assertions
```

### Batch Evaluation (comparing two outputs)

```javascript
// Evaluate output A
// Save verdict A
// Evaluate output B
// Save verdict B
// Compare composites → choose higher scoring output
```

## Integration with Verification-Before-Completion

The recommended quality gate pattern:

```javascript
// Step 1: Do the work
// Step 2: Evaluate with agent-evaluation
Skill({ skill: 'agent-evaluation' });
// If verdict is POOR or FAILING → rework before proceeding
// If verdict is ADEQUATE or better → proceed to verification
// Step 3: Final gate
Skill({ skill: 'verification-before-completion' });
// Step 4: Mark complete
TaskUpdate({ taskId: 'X', status: 'completed' });
```

## Iron Laws

1. **NO COMPLETION CLAIM WITHOUT EVALUATION EVIDENCE** — If composite score < 2.5 (POOR or FAILING), rework the output before marking any task complete.
2. **ALWAYS score all 5 dimensions** — never skip dimensions to save time; each dimension catches different failure modes (accuracy ≠ completeness ≠ groundedness).
3. **ALWAYS cite specific evidence** for every dimension score — `"Evidence: [file:line or direct quote]"` is mandatory, not optional. Assertions without grounding are invalid.
4. **ALWAYS use the weighted composite** — `accuracy×0.30 + groundedness×0.25 + completeness×0.20 + coherence×0.15 + helpfulness×0.10`. Never use simple average.
5. **NEVER evaluate before the work is complete** — evaluating incomplete outputs produces falsely low scores and wastes context budget.

## Anti-Patterns

| Anti-Pattern                       | Why It Fails                                                 | Correct Approach                                         |
| ---------------------------------- | ------------------------------------------------------------ | -------------------------------------------------------- |
| Skipping dimensions to save time   | Each dimension catches different failures                    | Always score all 5 dimensions                            |
| No evidence citation per dimension | Assertions without grounding are invalid                     | Quote specific text or file:line for every score         |
| Using simple average for composite | Accuracy (30%) matters more than helpfulness (10%)           | Use the weighted composite formula                       |
| Only checking EXCELLENT vs FAILING | ADEQUATE outputs need targeted improvements, not full rework | Use all 5 verdict tiers with appropriate action per tier |
| Evaluating before work is done     | Incomplete outputs score falsely low                         | Evaluate completed outputs only                          |
| Treating evaluation as binary gate | Quality is a spectrum; binary pass/fail loses nuance         | Use composite score + per-dimension breakdown together   |

## Assigned Agents

This skill is used by:

- `qa` — Primary: validates test outputs and QA reports before completion
- `code-reviewer` — Supporting: evaluates code review quality
- `reflection-agent` — Supporting: evaluates agent responses during reflection cycles

## Memory Protocol (MANDATORY)

**Before starting:**

```bash
cat .claude/context/memory/learnings.md
```

Check for:

- Previous evaluation scores for similar outputs
- Known quality patterns in this codebase
- Common failure modes for this task type

**After completing:**

- Evaluation pattern found -> `.claude/context/memory/learnings.md`
- Quality issue identified -> `.claude/context/memory/issues.md`
- Decision about rubric weights -> `.claude/context/memory/decisions.md`

> ASSUME INTERRUPTION: Your context may reset. If it's not in memory, it didn't happen.
