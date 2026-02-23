---
name: analysis-swarm
description: Multi-perspective code analysis using three AI personas (RYAN, FLASH, SOCRATES) for comprehensive decision-making. Use when complex code decisions need analysis from multiple viewpoints, or when avoiding single-perspective blind spots is critical.
---

# Analysis Swarm

Multi-perspective code analysis using three AI personas (RYAN, FLASH, SOCRATES) for comprehensive decision-making.

## Quick Reference

- **[Personas](personas.md)** - RYAN, FLASH, SOCRATES descriptions
- **[Orchestration](orchestration.md)** - Activation sequence and rules
- **[Discourse](discourse.md)** - Questioning patterns and synthesis
- **[Examples](examples.md)** - Complete swarm examples

## When to Use

- Complex architectural decisions (security vs speed vs maintainability)
- Trade-off analysis with multiple perspectives
- Risk assessment (conservative + aggressive viewpoints)
- Code review avoiding single-perspective blind spots
- Design decisions with long-term implications
- High-stakes features requiring comprehensive analysis

## NOT Appropriate For

- Simple bug fixes with obvious solutions
- Trivial refactoring
- Standard feature additions
- Time-sensitive hotfixes (use FLASH alone)

## The Three Personas

| Persona | Approach | Strengths |
|---------|----------|-----------|
| **RYAN** | Methodical analyst | Security, scalability, evidence-based |
| **FLASH** | Rapid innovator | Speed, user impact, pragmatic solutions |
| **SOCRATES** | Questioning facilitator | Exposes assumptions, facilitates agreement |

See **[personas.md](personas.md)** for detailed persona descriptions and **[orchestration.md](orchestration.md)** for the swarm protocol.
