---
name: hreng-ladder
description: Use when the user wants to create or refine an engineering career ladder, define level expectations, or design promotion criteria and packets.
version: 1.0.0
license: MIT
---

# HR Engineering Career Ladder

## Overview

Design an engineering career ladder with clear expectations per level, competency definitions, and promotion packet templates that enable fair, consistent decisions.

## When to Use

Use this skill when:
- Creating a **new engineering ladder** for your org.
- Adapting a ladder for a **specific team or track** (e.g., platform, data, management).
- Writing or reviewing **promotion criteria** and **promotion packets**.
- Calibrating expectations across **managers, levels, or locations**.

Do **not** use this skill when:
- You’re diagnosing **performance or burnout** → use `hreng-perf-diagnose` / `hreng-burnout`.
- You’re assessing **team skills vs. roadmap** → use `hreng-skills`.
- You’re defining a **hiring intake** for a new role → use `hreng-hire-intake`.

## Inputs Required

- Current or desired **level structure** (IC and/or management).
- Any existing career frameworks or job descriptions.
- Org size, reporting structure, and growth plans.
- Calibration constraints (pay bands, titles already in use, HR policies).

## Outputs Produced

- A **structured ladder JSON** per `templates/levels-competencies.json`.
- A **levels outline** document (`templates/ladder-levels-outline.md`).
- A **promotion packet template** (`templates/promotion-packet.md`) tailored to your ladder.

## Tooling Rule

- If MCP tools are available, prefer them for org structure, role inventory, and compensation bands.
- Keep **level definitions and expectations in JSON** and generate human-readable views from them.

## Career Ladder Structure

### Level Definitions

Start with the IC and management tracks; adapt titles and years of experience to your context.

**Individual Contributor (IC) Track (example):**

| Level | Title            | Years Exp | Scope            | Impact          |
|-------|------------------|-----------|------------------|-----------------|
| L3    | Junior Engineer  | 0–2       | Individual tasks | Team            |
| L4    | Engineer         | 2–5       | Features         | Team            |
| L5    | Senior Engineer  | 5–8       | Projects         | Multiple teams  |
| L6    | Staff Engineer   | 8–12      | Initiatives      | Org / Product   |
| L7    | Senior Staff     | 12–15     | Strategic areas  | Company         |
| L8    | Principal        | 15+       | Vision           | Industry        |

**Management Track (example):**

| Level | Title               | Years Exp | Team Size | Scope        |
|-------|---------------------|-----------|-----------|-------------|
| M4    | Engineering Manager | 5+        | 4–8 ICs   | Single team |
| M5    | Senior EM           | 8+        | 8–12      | Multi-team  |
| M6    | Director            | 10+       | 15–30     | Department  |
| M7    | Senior Director     | 12+       | 30–60     | Large org   |
| M8    | VP Engineering      | 15+       | 60+       | Eng org     |

Treat “years of experience” as **soft guidance**, not a hard requirement; the real bar is **evidence of impact and behaviors**.

### Competency Framework

Use three primary competencies across levels and adjust weights:
1. **Technical Excellence** – depth, breadth, and quality of engineering work.
2. **Leadership & Influence** – ownership, mentorship, and decision-making scope.
3. **Collaboration & Impact** – cross-functional collaboration and business outcomes.

**Senior Engineer (L5) example (matches JSON in `templates/levels-competencies.json`):**

```json
{
  "level": "L5",
  "title": "Senior Engineer",
  "competencies": {
    "technical": {
      "weight": 0.60,
      "expectations": [
        "Designs and implements complex systems independently",
        "Makes sound architectural decisions for team's domain",
        "Debugs issues across stack/services",
        "Writes high-quality, maintainable code",
        "Considers scale, performance, reliability"
      ],
      "evidence_examples": [
        "Led migration to new database with zero downtime",
        "Designed caching layer that reduced latency 70%",
        "Implemented monitoring that caught production issues before customer impact"
      ]
    },
    "leadership": {
      "weight": 0.25,
      "expectations": [
        "Mentors 2–3 junior/mid engineers",
        "Leads technical design for medium-large projects",
        "Influences technical decisions beyond own team",
        "Improves team processes and practices"
      ],
      "evidence_examples": [
        "Mentored 2 engineers who were promoted",
        "Improved design review process, reducing cycle time 30%",
        "Presented technical deep-dive at engineering all-hands"
      ]
    },
    "collaboration": {
      "weight": 0.15,
      "expectations": [
        "Partners effectively with PM, design, data",
        "Communicates technical concepts to non-technical stakeholders",
        "Drives consensus on technical decisions",
        "Contributes to engineering culture"
      ],
      "evidence_examples": [
        "Led cross-functional project with PM and design",
        "Wrote internal or external technical blog post",
        "Organized engineering learning group or community"
      ]
    }
  }
}
```

## Promotion Packet Template

Use `templates/promotion-packet.md` as the canonical template and ensure it ties **evidence directly to expectations**:

```markdown
# Promotion Packet: [Name] → [Target Level]

## Summary
[1 paragraph: why this person is ready for next level, anchored in competencies]

## Competency Evidence

### Technical Excellence
**Expectation for [Target Level]:** [Paste from ladder]

**Evidence:**
1. [Project/accomplishment with impact]
   - What: [Description]
   - Impact: [Quantified outcome]
   - Level indicator: [Why this demonstrates next-level work]

2. [Project/accomplishment]
   - What: [...]
   - Impact: [...]
   - Level indicator: [...]

### Leadership & Influence
[Same structure]

### Collaboration & Impact
[Same structure]

## Peer Feedback

"[Quote from peer feedback highlighting next-level work]" – [Peer Name, Role]

"[Quote from peer feedback]" – [Peer Name, Role]

## Growth & Trajectory

- [Example of taking on next-level work proactively]
- [Example of consistent performance over time]
- [Example of learning and adaptation]

## Recommendation

[Manager's recommendation: Ready now / Ready in X months / Not yet ready]
[Justification]

## Approval

- [ ] Manager: [Name]
- [ ] Skip-level: [Name]
- [ ] Director: [Name]
- [ ] Calibration committee (if applicable)
```

## Using Supporting Resources

### Templates
- **`templates/levels-competencies.json`** – Full ladder definition (structured).
- **`templates/ladder-levels-outline.md`** – Quick-reference levels outline.
- **`templates/promotion-packet.md`** – Promotion case template.

### References
- **`references/level-examples.md`** – Real-world promotion examples (stub: add org-specific examples).
- **`references/calibration.md`** – Promotion calibration process and committee workflows.
- **`references/checklist.md`**, **`references/overview.md`**, **`references/pitfalls.md`** – Process and pitfalls.

### Scripts
- **`scripts/check-hreng-ladder.sh`** – Pre-run checks for the skill.
- **`scripts/validate-hreng-ladder.py`** – Check ladder completeness and JSON consistency.

## Common Mistakes

- Making expectations **too abstract** (“is a leader”) without concrete behaviors.
- Creating ladders that **don’t match actual promotion decisions** in practice.
- Over-indexing on **project count** instead of impact and scope.
- Ignoring **non-coding contributions** (mentoring, process, culture).
- Allowing different managers to interpret levels **inconsistently** without calibration.

Aim for a ladder where two independent managers would make **the same promotion call** given the same packet and definitions.