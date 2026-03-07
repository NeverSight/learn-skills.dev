---
name: implement-plan-preflight
description: "Run the Preflight phase of the ITP workflow to create ADR and design spec artifacts. Use whenever the user asks to create an ADR, write a design spec, set up MADR-format documentation, or when the /itp:go workflow enters its preflight stage. Do NOT use for general documentation writing or markdown formatting that is unrelated to the ADR-driven development workflow."
allowed-tools: Bash, Read, Write, Edit, Glob, Grep
---

# Implement Plan Preflight

Execute the Preflight phase of the `/itp:go` workflow. Creates ADR and Design Spec artifacts with proper cross-linking and verification.

## When to Use This Skill

- Invoked by `/itp:go` command during Preflight phase
- User asks to create an ADR for a feature
- User mentions "design spec" or "MADR format"
- Manual preflight verification needed

## Preflight Workflow Overview

```
P.1: Create Feature Branch (if -b flag)
         │
         ▼
P.2: Create ADR File (MADR 4.0)
         │
         ▼
P.3: Create Design Spec (from global plan)
         │
         ▼
P.4: Verify Checkpoint (MANDATORY)
```

**CRITICAL**: Do NOT proceed to Phase 1 implementation until ALL preflight steps are complete and verified.

---

## Quick Reference

### ADR ID Format

```
YYYY-MM-DD-slug
```

Example: `2025-12-01-clickhouse-aws-ohlcv-ingestion`

### File Locations

| Artifact    | Path                                 |
| ----------- | ------------------------------------ |
| ADR         | `/docs/adr/$ADR_ID.md`               |
| Design Spec | `/docs/design/$ADR_ID/spec.md`       |
| Global Plan | `~/.claude/plans/<adj-verb-noun>.md` |

### Cross-Links (MANDATORY)

**In ADR header**:

```markdown
**Design Spec**: [Implementation Spec](/docs/design/YYYY-MM-DD-slug/spec.md)
```

**In spec.md header**:

```markdown
**ADR**: [Feature Name ADR](/docs/adr/YYYY-MM-DD-slug.md)
```

---

## Execution Steps

### Step P.1: Create Feature Branch (Optional)

Only if `-b` flag specified. See [Workflow Steps](./references/workflow-steps.md) for details.

### Step P.2: Create ADR File

1. Create `/docs/adr/$ADR_ID.md`
2. Use template from [ADR Template](./references/adr-template.md)
3. Populate frontmatter from session context
4. Select perspectives from [Perspectives Taxonomy](./references/perspectives-taxonomy.md)
5. Use Skill tool to invoke `adr-graph-easy-architect` for diagrams

### Step P.3: Create Design Spec

1. Create folder: `mkdir -p docs/design/$ADR_ID`
2. Copy global plan: `cp ~/.claude/plans/<adj-verb-noun>.md docs/design/$ADR_ID/spec.md`
3. Add ADR backlink to spec header

### Step P.4: Verify Checkpoint

Run validator or manual checklist:

```bash
uv run scripts/preflight_validator.py $ADR_ID
```

**Checklist** (ALL must be true):

- [ ] ADR file exists at `/docs/adr/$ADR_ID.md`
- [ ] ADR has YAML frontmatter with all 7 required fields
- [ ] ADR has `**Design Spec**:` link in header
- [ ] **DIAGRAM CHECK 1**: ADR has **Before/After diagram** (Context section)
- [ ] **DIAGRAM CHECK 2**: ADR has **Architecture diagram** (Architecture section)
- [ ] Design spec exists at `/docs/design/$ADR_ID/spec.md`
- [ ] Design spec has `**ADR**:` backlink in header

**If any item is missing**: Create it now. Do NOT proceed to Phase 1.

---

## YAML Frontmatter Quick Reference

```yaml
---
status: proposed
date: YYYY-MM-DD
decision-maker: [User Name]
consulted: [Agent-1, Agent-2]
research-method: single-agent
clarification-iterations: N
perspectives: [Perspective1, Perspective2]
---
```

See [ADR Template](./references/adr-template.md) for full field descriptions.

---

## Diagram Requirements (2 DIAGRAMS REQUIRED)

**⛔ MANDATORY**: Every ADR must include EXACTLY 2 diagrams:

| Diagram          | Location             | Purpose                       |
| ---------------- | -------------------- | ----------------------------- |
| **Before/After** | Context section      | Shows system state change     |
| **Architecture** | Architecture section | Shows component relationships |

**SKILL INVOCATION**: Invoke `adr-graph-easy-architect` skill NOW to create BOTH diagrams.

**BLOCKING GATE**: Do NOT proceed to design spec until BOTH diagrams are embedded in ADR.

---

## Reference Documentation

- [ADR Template](./references/adr-template.md) - Complete MADR 4.0 template
- [Perspectives Taxonomy](./references/perspectives-taxonomy.md) - 11 perspective types
- [Workflow Steps](./references/workflow-steps.md) - Detailed step-by-step guide

---

## Validation Script

```bash
# Verify preflight artifacts
uv run scripts/preflight_validator.py <adr-id>

# Example
uv run scripts/preflight_validator.py 2025-12-01-my-feature
```

---

## Troubleshooting

| Issue                 | Cause                    | Solution                                     |
| --------------------- | ------------------------ | -------------------------------------------- |
| Validator fails       | Missing ADR or spec      | Create both files before running validator   |
| Frontmatter invalid   | Missing required fields  | Check all 7 ADR fields and 5 spec fields     |
| Diagram not rendering | graph-easy not installed | Run `brew install graph-easy`                |
| Spec phase mismatch   | Wrong phase value        | Use: preflight, phase-1, phase-2, or phase-3 |
| ADR status wrong      | Manual status edit       | Let workflow manage status transitions       |
| Design folder missing | Wrong path structure     | Use docs/design/YYYY-MM-DD-slug/spec.md      |
