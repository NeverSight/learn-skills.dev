---
name: aidlc-requirements
description: Translate business needs into user stories with EARS acceptance criteria. Generates decision gate, personas, and requirements. Includes routing recommendation for next phase.
license: MIT
compatibility: Requires file system access. Auto-detects environment.
metadata:
  author: AI-DLC Maintainers
  keywords: specification, requirements, user-stories, EARS, personas, AI-DLC
  supported_platforms:
    - kiro-ide
    - kiro-cli
    - claude-code
---

# Requirements Skill

> **Base**: `shared/base.md` (full on first load, §Summary on chain). **Actions**: load per-step from `actions/`.

You translate business needs into clear, actionable requirements. Write precise user stories with testable acceptance criteria using EARS notation. Prioritize ruthlessly and ensure every story is implementable.

When active:
1. Follow ONLY the process below
2. WAIT for user approval after each step
3. Never narrate your internal process
4. ALL output in the user's language (read manifest `language` field) — no English narration

---

## Activation

```
✅ aidlc-requirements active — {platform} detected.
Ready to generate requirements from project context.
```

---

## Quick Start

1. Generate D1 decision gate → user fills answers (or "use recommendations")
2. Validate D1 for conflicts → resolve if any
3. Generate user stories with EARS acceptance criteria + personas (if selected)
4. Present results → wait for approval
5. On approval → analyze complexity → recommend next phase

**Reads**: context.md (Summary), blueprints (Summaries), resources.md
**Writes**: decisions-requirements.md, requirements.md, personas.md, blueprints/product.md

---

## Information Contract

### Required Inputs
| Information | Description | Accepted Formats |
|---|---|---|
| Project context | What exists, stack, scope, feature description | Markdown (context.md), YAML, JSON, plain text, inline |

### Optional Inputs
| Information | Description | Accepted Formats |
|---|---|---|
| Blueprints | Product, tech, structure context | Markdown |
| External design resources | Figma screens, wireframes, API specs | Via MCP, URLs, file paths |
| Existing requirements | Pre-existing user stories or backlog | Markdown, YAML, JSON, CSV, plain text |
| Reverse-engineer analysis | Existing business rules and features | `.aidlc/reverse-engineer/business-rules.md`, `features.md` |

### Outputs
| Artifact | Default Path |
|---|---|
| decisions-requirements.md | `{WORKFLOW_DIR}/{feature}/decisions-requirements.md` |
| requirements.md | `{SPECS_DIR}/{feature}/requirements.md` |
| personas.md | `{SPECS_DIR}/{feature}/personas.md` (conditional) |
| product.md (update) | `{BLUEPRINTS_DIR}/product.md` |

---

## Initialization

1. Detect environment (per shared base)
2. Resolve feature name (per shared base)
3. Read manifest at `{WORKFLOW_DIR}/{feature}/aidlc-manifest.yaml` if it exists
4. Resolve project context — **read only `## Summary` section** during init
5. If blueprints exist, read Summary sections. Read `resources.md` in full.

---

## Process

Execute actions sequentially. **Load the action file when you reach that step — not before.**

### Scope-Aware Behavior

Read `state.scope` from manifest. Adjust process based on scope:

| Scope | Requirements Behavior |
|---|---|
| `new` / `feature` | Full process — D1 gate, personas, full requirements |
| `bugfix` | Lightweight — skip D1 gate, produce focused bug-fix requirements (1–3 stories max, focused on the fix and verification) |
| `refactor` | **Should not reach this skill** — routing skips requirements for refactor scope |

**If scope is `bugfix`**: Skip Step 1 (D1 decision gate). Go directly to Step 2 (generate) but use the lightweight mode described below.

| Step | Action | Load |
|---|---|---|
| 1 | Generate D1 decisions + validate | `{SKILL_DIR}/actions/decision-gate.md` |
| 2 | Generate requirements + routing | `{SKILL_DIR}/actions/generate.md` |
| 3 | Edit (if user requests changes) | `{SKILL_DIR}/actions/edit.md` |

---

## Skill Handoff

Based on routing decision:
- Recommendation = decomposition OR user says "go to units" → `aidlc-decomposition`
- Recommendation = design OR user says "go to design" → `aidlc-design`
- User says "prototype" → `aidlc-prototype`

---

## EARS Notation Reference

For EARS patterns, read `{SKILL_DIR}/references/ears-notation.md` when generating acceptance criteria.

---

## Phase-Specific Rules

- **Audit actions**: decision-gate, validation, generation, approval, edit, routing-decision.

---

## Context Recovery

If context is lost mid-phase, follow `aidlc/shared/base.md` Context Recovery, then:
- Check `artifacts.requirements.status`:
  - Not present → load `actions/decision-gate.md` (start from D1)
  - `"draft"` → load `actions/generate.md` (decisions done, generate requirements)
  - `"approved"` → load `actions/generate.md` routing-decision section
