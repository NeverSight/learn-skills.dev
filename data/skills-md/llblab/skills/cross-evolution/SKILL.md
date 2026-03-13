---
name: cross-evolution
description: Horizontal Gene Transfer protocol for skills. Synchronizes best practices and architectural patterns across the skill library.
metadata:
  version: 1.0.0
---

# Cross-Evolution

## Purpose

Maintain a high evolutionary standard across all agent skills by identifying "Genes" (best practices), transferring them to skills that lack these features, and discovering new high-value genes from existing skills.

## Axioms

### 1. Atomic Independence (No Cross-Skill Glue)

Skills and their scripts must be 'atomic'.

- 'FORBIDDEN': Any logic inside a skill's script that explicitly checks for or calls tools from another skill.
- 'The Agent is the Glue': Only the AI Agent is responsible for coordination.

### 2. Pragmatic Evolution (Occam's Razor)

- 'Just-In-Time Transfer': A gene is transferred only when it solves a recurring problem.
- 'KISS Compliance': Avoid bloating skills with genes they don't need.
- 'Fitness-Driven': Prioritize genes with highest weight for maximum fitness gain.

### 3. Living Protocol

This skill proactively evolves itself and its gene registry upon discovering new constraints.

## Core Concepts

### Gene

A modular implementation or documentation pattern that improves skill quality.
Genes have a 'lifecycle': `Proposed → Active → Deprecated → Extinct`.
Full registry with weights, detection rules, and conflicts: [`docs/genes.md`](./docs/genes.md)

### Horizontal Gene Transfer (HGT)

Copying a gene from a donor skill to a recipient without rewriting the recipient's core purpose.

### Gene Discovery

Scanning existing skills for repeated high-value patterns not yet represented in the registry.
If a candidate passes thresholds, it is automatically written into `docs/genes.md` under "Proposed Genes".

### Genetic Drift

Genes carried by zero skills are candidates for deprecation. After sustained non-adoption, they go extinct.

### Fitness

Quantitative health score per skill: `earned_weight / applicable_weight × 100%`.
Domain-specific genes (recommend=`none`) only count if already present — reward, not penalty.

### Recombination

When two genes conflict in the same skill, selective pressure creates a new hybrid gene.

## Operating Modes

### Mode 1: Scan & Audit

'Automated': `bash "${SKILL_DIR}/scripts/audit-genes"`

Produces: Gene × Skill matrix, fitness scores, genetic drift warnings, conflict alerts, recommendations, and discovered gene candidates (with registry sync).

Useful flags:

- `--no-discovery` — skip discovery phase.
- `--no-sync-discovery` — discover candidates without writing to registry.

### Mode 2: Mutation (Update)

Inject missing/extra genes into a target skill. Prioritize by weight × fitness impact.

'Value guard': Before transferring a gene, ask: "Does this gene solve a real problem
the skill has encountered, or are we just making the fitness number go up?" If the latter —
skip the transfer. Fitness score is a heuristic, not a goal. Optimizing the score
instead of skill quality is the Farmville trap.

### Mode 3: Speciation (Creation)

Create a new gene/skill by combining existing patterns (triggered by gene conflicts or recombination).
