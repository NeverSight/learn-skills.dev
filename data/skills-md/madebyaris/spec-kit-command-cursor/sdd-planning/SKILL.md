---
name: sdd-planning
description: Generate technical plans from specifications. Use when creating architecture documents, designing system components, or preparing for implementation.
---

# SDD Planning Skill

Transform specifications into actionable technical plans.

## When to Use

- Spec exists but plan doesn't
- Designing system architecture
- Breaking down features into components
- After research is complete

## Planning Protocol

### Step 1: Understand Requirements
Read `spec.md`, note functional/non-functional requirements, review research findings.

### Step 2: Design Architecture
Identify components, define responsibilities, design interfaces, plan data flow.

### Step 3: Select Technology
Evaluate against requirements, consider existing stack, document rationale.

### Step 4: Plan Implementation
Break into phases (Setup → Core → Integration → Polish), identify dependencies, estimate effort.

### Step 5: Assess Risks
Identify technical risks, plan mitigations, note assumptions.

## Output Format

Generate `plan.md` with:

```markdown
# Technical Plan: [Task ID]

## Overview
## Architecture (Mermaid diagram)
## Components (table: name, responsibility, dependencies)
## Technology Stack (with rationale)
## API Design
## Data Models
## Security Considerations
## Performance Targets
## Implementation Phases (Setup → Core → Integration → Polish)
## Risks (probability, impact, mitigation)
## Testing Strategy (unit, integration, E2E)
## Open Questions
```

## References

See `assets/diagram-templates.md` for architecture diagram patterns.

## Integration

- Input from: `sdd-research` skill, `sdd-explorer` subagent
- Output to: `/tasks` command, `sdd-implementer` subagent
- Use the ask question tool for architectural decisions with significant tradeoffs
