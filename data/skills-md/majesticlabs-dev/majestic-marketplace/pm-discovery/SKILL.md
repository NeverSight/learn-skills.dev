---
name: pm-discovery
description: Product discovery orchestrator - routes to specialized frameworks for interviews, assumptions, JTBD, and prioritization.
triggers:
  - pm discovery
  - product discovery
---

# PM Discovery Orchestrator

Routes product discovery tasks to specialized frameworks.

## Framework Routing

| Task | Skill | When to Use |
|------|-------|-------------|
| Customer interviews | `pm-customer-interviews` | Conducting or synthesizing user interviews |
| Assumption testing | `pm-assumption-mapping` | Validating product hypotheses |
| Understanding needs | `pm-jobs-to-be-done` | Identifying why customers "hire" solutions |
| Feature prioritization | `pm-prioritization` | RICE/ICE scoring, opportunity mapping |
| Roadmap planning | `pm-roadmap` | Theme-based Now/Next/Later roadmaps |
| Feature briefs & decisions | `pm-one-pager` | Lightweight briefs, decision records |

## When to Use Each

```
Interview synthesis needed? → pm-customer-interviews
Testing assumptions? → pm-assumption-mapping
Understanding motivation? → pm-jobs-to-be-done
Prioritizing features? → pm-prioritization
Planning roadmap? → pm-roadmap
Early exploration or recording decisions? → pm-one-pager
Full feature specification? → /majestic:prd
```

## Discovery Synthesis

After using individual frameworks, synthesize findings:

```markdown
## Discovery Summary: [Feature/Initiative]

### What We Learned
1. [Key insight with evidence]
2. [Key insight with evidence]
3. [Key insight with evidence]

### User Segments & Their Jobs
| Segment | Primary Job | Pain Intensity | Size |
|---------|-------------|----------------|------|
| [Segment A] | [JTBD] | [1-5] | [N users] |

### Prioritized Opportunities
| Rank | Opportunity | Evidence | RICE |
|------|-------------|----------|------|
| 1 | [Opp] | [Quote/data] | [Score] |

### Recommended Next Step
**Do:** [Specific action]
**Test:** [What to validate]
**Success looks like:** [Measurable outcome]

### What We Still Don't Know
- [ ] [Open question to investigate]
- [ ] [Assumption still untested]
```

## Anti-Patterns

| Anti-Pattern | Why It Fails | Instead Do |
|--------------|--------------|------------|
| Leading questions | Confirms bias | Ask open-ended |
| Hypothetical pricing | People lie | Ask current spending |
| Feature requests as truth | Solutions, not problems | Dig for need |
| Small sample decisions | Anecdotes ≠ patterns | 5+ signals minimum |
| Skip competitor research | Reinvent wheel | Research first |

## Integration

- **Before:** Use `problem-research` for market pain points
- **After:** Use `/majestic:prd` for requirements documentation
- **After:** Use `/majestic:plan` for implementation planning
