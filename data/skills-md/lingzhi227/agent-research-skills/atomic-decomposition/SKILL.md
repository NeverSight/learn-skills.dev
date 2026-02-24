---
name: atomic-decomposition
description: Decompose research ideas into atomic, self-contained concepts with bidirectional math-code mapping. For each concept, extract the math formula from papers and find code implementations. Use for complex system papers requiring formal grounding.
argument-hint: [idea-or-paper]
---

# Atomic Decomposition

Decompose research ideas into atomic concepts with math formula <-> code implementation mapping.

## Input

- `$0` — Research idea, paper, or method description

## References

- Decomposition prompts and workflow: `~/.claude/skills/atomic-decomposition/references/decomposition-prompts.md`

## Workflow (from AI-Researcher Survey Agent)

### Step 1: Break Down into Atomic Definitions
Analyze the research idea and decompose into atomic, self-contained concepts:
- Each atom should be a single concept
- Must have clear mathematical foundations
- Must be implementable in code
- Must be traceable to specific papers

### Step 2: For Each Atomic Definition

#### A. Paper Survey (Math Formula)
- Search papers for the mathematical formulation
- Extract the exact LaTeX formula
- Note assumptions and constraints
- Record reference papers

#### B. Code Survey (Implementation)
- Search codebases for implementations
- Extract the corresponding code
- Note implementation details and variations
- Record reference repositories

#### C. Create Knowledge Entry
```json
{
  "definition": "Kernelized Gumbel-Softmax Operator",
  "math_formula": "Z = \\text{softmax}((\\log \\pi + g) / \\tau), g \\sim \\text{Gumbel}(0,1)",
  "code_implementation": "def gumbel_softmax(logits, tau=1.0): ...",
  "reference_papers": ["Paper Title 1"],
  "reference_codebases": ["github_user/repo_name"],
  "assumptions": ["Differentiable relaxation of discrete sampling"],
  "connections": ["Used in Component X of the proposed method"]
}
```

### Step 3: Compile Knowledge Base
- Merge all atomic definitions into a structured knowledge base
- Verify consistency: every math formula has a code implementation
- Verify completeness: every code module traces to a formal definition
- Identify any gaps (formulas without code, or code without theory)

## Rules

- Each atomic definition must be specific enough to trace to concrete formulas and code
- Do not skip or combine definitions — analyze each separately
- If unsure about atomicity, err on the side of breaking down further
- Document breakdown reasoning before analysis
- Every mathematical concept in the paper must have verified code
- Every code module must trace back to a formal mathematical definition

## Related Skills
- Upstream: [research-planning](../research-planning/), [idea-generation](../idea-generation/)
- Downstream: [experiment-code](../experiment-code/), [algorithm-design](../algorithm-design/)
- See also: [math-reasoning](../math-reasoning/)
