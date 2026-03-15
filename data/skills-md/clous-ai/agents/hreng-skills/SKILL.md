---
name: hreng-skills
description: Use when the user wants to assess engineering team skills, build a skills matrix, identify gaps vs. roadmap, and design training or hiring plans.
version: 1.0.0
license: MIT
---

# HR Engineering Skills Inventory

## Overview

Map engineering team capabilities, identify gaps against current and future roadmap needs, and turn that into a concrete training and hiring plan.

## When to Use

Use this skill when:
- You need a **skills matrix** for a team or org.
- You’re planning **roadmap delivery** and want to check if skills coverage is sufficient.
- You want to reduce **key-person dependencies** and plan knowledge transfer.
- You’re deciding between **training vs. hiring vs. outsourcing**.

Do **not** use this skill when:
- The focus is an **individual’s promotion or level expectations** → use `hreng-ladder`.
- You’re diagnosing **performance or burnout issues** → use `hreng-perf-diagnose` or `hreng-burnout`.

## Inputs Required

- Team roster and roles (names, titles, levels).
- Roadmap initiatives and timelines (next 6–18 months).
- Any existing skill assessments or certifications.
- Constraints: budget, time for training, hiring freezes, vendor policies.

## Outputs Produced

- A **structured skills matrix JSON** per `templates/skills-matrix.json`.
- A **manager-readable matrix** (`templates/skills-matrix.md`).
- A **gap analysis + training/hiring plan** (`templates/skills-gap-analysis.md`, `templates/training-plan.md`).

## Tooling Rule

- If MCP tools are available, prefer them for roster/org data (HRIS, Slack groups, GitHub org).
- Always base outputs on the provided templates before adding freeform commentary.

## Core Pattern

1. **Inventory current skills** (self-assessment + manager calibration).
2. **Map roadmap needs** (what capabilities are required when).
3. **Compute gaps** (coverage vs. required level and timing).
4. **Prioritize** gaps by impact and urgency.
5. **Choose mitigations**: training, hiring, role changes, or vendor support.

## Skills Matrix Template

Use `templates/skills-matrix.json` as the canonical structure. A typical instance:

```json
{
  "team": "Platform Engineering",
  "assessment_date": "2026-01-22",
  "skills": [
    {
      "category": "Backend",
      "skills": [
        {
          "name": "Python",
          "team_coverage": {
            "expert": ["Alice", "Bob"],
            "proficient": ["Carol", "Dave"],
            "learning": ["Eve"],
            "none": []
          },
          "criticality": "high",
          "roadmap_need": "high"
        },
        {
          "name": "Go",
          "team_coverage": {
            "expert": [],
            "proficient": ["Alice"],
            "learning": ["Bob"],
            "none": ["Carol", "Dave", "Eve"]
          },
          "criticality": "medium",
          "roadmap_need": "high",
          "gap": "Need 2 experts for Q2 microservices rewrite"
        }
      ]
    }
  ],
  "training_plan": [
    {
      "skill": "Go",
      "priority": "high",
      "action": "2 engineers to complete Go training by Q2",
      "budget": "$2,000",
      "timeline": "12 weeks"
    }
  ]
}
```

## Gap Analysis Process

1. **Map current skills**
   - Start with **self-assessments** (e.g., learning/proficient/expert).
   - Calibrate with manager/lead to avoid inflated or under-stated levels.
   - Capture **breadth vs. depth** (e.g., “proficient in React, expert in Django”).
2. **Map roadmap requirements**
   - For each major initiative, list required skills and depth (e.g., “2 experts in Kubernetes by Q3”).
   - Include non-technical skills: product sense, stakeholder management, security, reliability.
3. **Identify gaps**
   - Skills with high roadmap need but few/no experts.
   - Single-point-of-failure skills (only one expert across team/org).
   - Emerging capabilities (e.g., ML, data platform) with no coverage yet.
4. **Prioritize gaps**
   - Prioritize by **criticality × time-to-need**:
     - High criticality + near-term → urgent.
     - Medium criticality + long-term → plan but don’t panic.
5. **Plan mitigation**
   - Training: courses, pairing, stretch projects, internal workshops.
   - Hiring: new roles or backfills (coordinate with `hreng-hire-intake`).
   - Vendors/consultants: short-term coverage while building internal capability.

## Using Supporting Resources

### Templates
- **`templates/skills-matrix.json`** – Structured team skills inventory.
- **`templates/skills-matrix.md`** – Human-readable matrix for managers.
- **`templates/skills-gap-analysis.md`** – Gap analysis and roadmap risk view.
- **`templates/training-plan.md`** – Structured training roadmap.

### References
- **`references/overview.md`**, **`references/checklist.md`**, **`references/data-sources.md`** – Process and data sources.
- **`references/mitigation-playbook.md`** – Training, hiring, and vendor mitigation options.
- **`references/output-schema.md`** – Skills matrix and gap output structure.

### Scripts
- **`scripts/check-hreng-skills.sh`** – Pre-run checks for the skill.
- **`scripts/validate-hreng-skills.py`** – Validate skills matrix JSON and gap analysis structure.

## Common Mistakes

- Treating **self-assessment as ground truth** without calibration.
- Focusing only on **current stack**, ignoring planned roadmap changes.
- Ignoring **soft skills and leadership capabilities** needed for scale.
- Over-relying on **a single expert** instead of building a bench.
- Creating a matrix but **not turning it into concrete training or hiring actions**.

The output should make it obvious which 3–5 skill gaps matter most and exactly what the team plans to do about each one.