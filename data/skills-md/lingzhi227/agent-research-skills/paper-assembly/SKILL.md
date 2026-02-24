---
name: paper-assembly
description: Orchestrate the full paper pipeline end-to-end. Manage state propagation between phases (literature → plan → code → experiments → figures → tables → writing → review), support checkpointing and resumption. Use for assembling a complete paper from components.
argument-hint: [paper-directory]
---

# Paper Assembly

Orchestrate the entire paper pipeline end-to-end with state management and checkpointing.

## Input

- `$0` — Paper project directory or paper plan

## References

- Orchestration patterns and state management: `~/.claude/skills/paper-assembly/references/orchestration-patterns.md`

## Scripts

### Check pipeline completeness
```bash
python ~/.claude/skills/paper-assembly/scripts/assembly_checker.py --dir paper/ --output checkpoint.json
python ~/.claude/skills/paper-assembly/scripts/assembly_checker.py --dir paper/ --verbose
```

Scans paper directory, checks 9 pipeline phases, reports missing artifacts, suggests next steps.

## Workflow

### Step 1: Assess Current State
1. Scan the paper directory for existing artifacts
2. Identify which phases are complete vs pending
3. Build a dependency graph of remaining work

### Step 2: Execute Pipeline Phases
Run phases in dependency order:

| Phase | Skill | Input | Output |
|-------|-------|-------|--------|
| 1. Literature | literature-search, literature-review | Topic | Knowledge base, BibTeX |
| 2. Planning | research-planning | Knowledge base | Paper structure, task list |
| 3. Code | experiment-code | Plan | Training/eval pipeline |
| 4. Experiments | experiment-design | Code | Results JSON/CSV |
| 5. Figures | figure-generation | Results | PNG figures |
| 6. Tables | table-generation | Results | LaTeX tables |
| 7. Writing | paper-writing-section | All above | main.tex sections |
| 8. Citations | citation-management | Draft | references.bib |
| 9. Formatting | latex-formatting | Draft | Formatted LaTeX |
| 10. Compilation | paper-compilation | All | PDF |
| 11. Review | self-review | PDF | Review scores |

### Step 3: State Propagation
After each phase completes:
1. Save output artifacts to the paper directory
2. Propagate results to downstream phases
3. Update the progress checkpoint file

### Step 4: Quality Gates
Before proceeding to the next phase:
- Verify all required outputs exist
- Check for consistency (e.g., all cited keys in .bib)
- Validate figures/tables match experimental results

### Step 5: Final Assembly
1. Merge all sections into main.tex
2. Verify all \includegraphics files exist
3. Verify all \cite keys exist in .bib
4. Compile to PDF
5. Run self-review for quality check

## Orchestration Patterns

### Sequential Pipeline (AI-Scientist)
```
generate_ideas → experiments → writeup → review
```

### Multi-Agent State Broadcasting (AgentLaboratory)
```python
# Propagate results to all downstream agents
set_agent_attr("dataset_code", code)
set_agent_attr("results", results_json)
```

### Copilot Mode (AgentLaboratory)
Human can intervene at any phase boundary for review/correction.

## Checkpoint Format

```json
{
  "project": "paper-name",
  "phases_completed": ["literature", "planning", "code"],
  "current_phase": "experiments",
  "artifacts": {
    "literature": "knowledge_base.json",
    "plan": "research_plan.json",
    "code": "experiments/",
    "results": null
  },
  "last_updated": "2024-01-15T10:30:00Z"
}
```

## Rules

- Never skip phases — each depends on previous outputs
- Save checkpoints after every phase completion
- Human review is recommended at phase boundaries
- All numbers in the paper must trace to actual experiment logs
- Re-run downstream phases if upstream changes

## Related Skills
- Upstream: all other skills (this is the orchestrator)
- Downstream: [paper-compilation](../paper-compilation/), [self-review](../self-review/)
- See also: [research-planning](../research-planning/)
