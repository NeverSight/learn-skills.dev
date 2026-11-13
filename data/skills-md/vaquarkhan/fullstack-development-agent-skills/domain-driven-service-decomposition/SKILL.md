---
name: domain-driven-service-decomposition
description: Decompose systems into service boundaries using domain-driven design, bounded contexts, and team ownership constraints. Use when splitting monoliths or correcting poor service boundaries.
disable-model-invocation: true
---

# Domain Driven Service Decomposition

## Use When

- Service boundaries are unclear or causing coupling
- Teams are planning monolith-to-microservice migration

## Workflow

1. Identify domains, subdomains, and bounded contexts.
2. Map business capabilities to ownership-aligned services.
3. Define context boundaries, contracts, and data ownership.
4. Validate boundaries against team cognitive load and release autonomy.
5. Plan incremental extraction slices with anti-corruption layers.

## Required Checks

- Service boundary avoids shared write ownership
- Cross-context communication contracts are explicit
- Team ownership model supports independent deployment

## Decision Framework

- Derive boundaries from business capabilities and language, not technical layers or CRUD tables.
- One bounded context owns each aggregate's write model; reads may be replicated with explicit lag tolerance.
- Size services for team cognitive load and independent release cadence—not maximal micro-granularity.
- Use anti-corruption layers when integrating legacy or external contexts.

## Common Rationalizations And Rebuttals

- "Split by database table." -> Table splits ignore domain language and create chatty cross-service joins.
- "One service per developer." -> Too-fine services multiply operational cost without autonomy gains.
- "Shared kernel is faster." -> Shared mutable models reintroduce monolith coupling; share only published contracts.

## Evidence Pack

- Context map with bounded contexts, upstream/downstream relationships, and ownership
- Aggregate ownership matrix (write vs read models per context)
- Extraction slice plan with strangler milestones and anti-corruption layer notes
- Team ownership alignment confirming deploy independence per slice

## Exit Criteria

- Service map is implementable and evolvable
- Decomposition roadmap includes measurable migration milestones
