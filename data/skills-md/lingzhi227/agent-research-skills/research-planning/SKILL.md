---
name: research-planning
description: Design research plans and paper architectures. Given a research topic or idea, generate structured plans with methodology outlines, paper structure, dependency-ordered task lists, UML diagrams, and experiment designs. Use when starting a new research project or paper.
argument-hint: [topic-or-idea]
---

# Research Planning

Create comprehensive research plans and paper architectures from a research topic or idea.

## Input

- `$0` — Research topic, idea description, or paper to reproduce

## References

- Planning prompts from Paper2Code, AI-Researcher, AgentLaboratory: `~/.claude/skills/research-planning/references/planning-prompts.md`
- Output schemas and templates: `~/.claude/skills/research-planning/references/output-schemas.md`

## Workflow

### Step 1: Understand the Research Context
- Read any provided papers, code, or references
- Identify the core research question and its significance
- Assess available resources (datasets, compute, existing code)

### Step 2: Generate Research Plan
Use the 4-stage planning approach (adapted from Paper2Code):

1. **Overall Plan** — Strategic overview: methodology, key experiments, evaluation metrics
2. **Architecture Design** — File structure, system design, Mermaid class/sequence diagrams
3. **Logic Design** — Task breakdown with dependencies, required packages, shared knowledge
4. **Configuration** — Extract or specify hyperparameters, training details, config.yaml

### Step 3: Structure the Paper
Design the paper structure with section-by-section plan:
- Abstract, Introduction, Background, Related Work, Methods, Experiments, Results, Discussion/Conclusion
- For each section: key points to cover, required figures/tables, target word count

### Step 4: Create Task Dependency Graph
- Order tasks by dependency (data → model → training → evaluation → writing)
- Identify parallelizable tasks
- Flag risks and potential failure modes

## Output Format

```json
{
  "research_question": "...",
  "methodology": "...",
  "paper_structure": {
    "sections": ["Abstract", "Introduction", ...],
    "section_plans": { "Introduction": "..." }
  },
  "task_list": [
    {"task": "...", "depends_on": [], "priority": 1}
  ],
  "baselines": ["..."],
  "datasets": ["..."],
  "evaluation_metrics": ["..."],
  "risks": ["..."]
}
```

## Rules

- Each plan component must be detailed and actionable
- Include specific implementation references when available
- Ensure all components work together coherently
- Always include a testing/evaluation plan
- Flag ambiguities explicitly rather than making assumptions

## Related Skills
- Upstream: [idea-generation](../idea-generation/), [literature-review](../literature-review/)
- Downstream: [experiment-design](../experiment-design/), [paper-assembly](../paper-assembly/)
- See also: [atomic-decomposition](../atomic-decomposition/)
