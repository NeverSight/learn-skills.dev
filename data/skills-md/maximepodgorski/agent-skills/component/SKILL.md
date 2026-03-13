---
name: component
description: |
  Design system component workflow. Structure, document, implement, review, and audit
  DS components with Figma as primary input.
  5 actions: structure, doc, dev, review, audit.
  Auto-activates on: "component", "structure component", "doc component",
  "dev component", "review component", "audit component", "design system",
  "ds component", "component structure", "component doc", "component dev",
  "component review", "component audit".
license: MIT
compatibility: "Agent-agnostic. Works with Claude Code, OpenCode, Windsurf, Cursor, Codex, Aider, or any agent supporting SKILL.md."
metadata:
  version: "1.0"
---

# Component

Design system component workflow. Figma to production, DS-compliant.

## Agent Capabilities

| Capability | Used For | Required | Fallback |
|------------|----------|----------|----------|
| File read/write | Specs, docs, audit reports | Yes | — |
| Code search (grep/glob) | Token scan, pattern discovery, codebase conventions | Yes | — |
| Shell/command execution | Quality gates (lint, typecheck) | Recommended | List commands for user to run |
| Task/todo tracking | Ship loop progress | Recommended | Track in spec Progress section |
| User interaction | Token creation approval, stuck escalation | Yes | — |
| Figma MCP | Design context extraction (code, screenshot, hints) | Recommended | User provides spec manually |

**Fallback rule:** If Figma MCP is unavailable, the skill works from text input and codebase analysis. Warn the user and proceed.

## Actions

| Action | Input | Output | Reference |
|--------|-------|--------|-----------|
| `structure {name} [figma-link]` | Component name + optional Figma link | Spec in `ds/specs/active/` | [structure.md](references/actions/structure.md) |
| `doc {path\|name}` | File path or component name | `doc.md` co-located in component folder | [doc.md](references/actions/doc.md) |
| `dev {name} [figma-link]` | Component name + optional Figma link | Implemented component (ship loop) | [dev.md](references/actions/dev.md) |
| `review {path\|figma-link}` | File path or Figma link | DS compliance report | [review.md](references/actions/review.md) |
| `audit {path\|figma-link}` | Directory path or Figma link | Report in `ds/audits/active/` | [audit.md](references/actions/audit.md) |

## Flow

```
Recommended (new component):
  structure → doc → dev → review

Quick (simple component):
  dev {name} [figma-link]

Maintenance (existing component):
  review {path}    or    doc {path}

System-wide:
  audit {directory}    or    audit {figma-link}
```

Each action is **standalone** — usable independently without requiring prior actions.

## Philosophy

- **Figma-first**: Figma is the primary input. Design context drives structure, API, and implementation.
- **Principles over opinions**: Grounded in Atomic Design, BEM, DTCG, WCAG — not arbitrary preferences.
- **Reuse > create**: Scan existing tokens, variables, typography BEFORE generating. Never invent.
- **Human-in-the-loop**: Never create a new token without user approval.
- **Zero hardcoded values**: Every hex, px, hardcoded spacing/color/radius is a CRITICAL violation.
- **Adapt to project**: Read `CLAUDE.md` + codebase. Match the project's naming, not the skill's.
- **Stack-agnostic**: Works with React, Vue, Svelte, Angular, Web Components — no hardcoded framework.

## Figma Integration

When a Figma link is provided, the skill calls `get_design_context` from Figma MCP:

```
Figma link provided?
  │
  ├─ YES → Call get_design_context(fileKey, nodeId)
  │         → Receives: code + screenshot + contextual hints
  │         → Extract: component hierarchy, props, variants, tokens used
  │         → Cross-reference with codebase conventions
  │         → Proceed with enriched context
  │
  └─ NO  → Proceed from codebase / manual input only

Combined failure state:
  Figma MCP unavailable AND no component in codebase AND no spec in ds/specs/active/?
    → Error: "No context available. Provide a Figma link with MCP configured,
       create the component first, or run /component structure {name} with a description."
```

**URL parsing:**
- `figma.com/design/:fileKey/:fileName?node-id=:nodeId` → convert `-` to `:` in nodeId
- `figma.com/design/:fileKey/branch/:branchKey/:fileName` → use branchKey as fileKey

## Token Scan Protocol

Before any `dev` or `review` action, scan the project for existing design tokens:

```
1. SCAN sources (in order):
   - CSS custom properties (--*)
   - SCSS/LESS variables ($*, @*)
   - Tailwind config (tailwind.config.*)
   - CSS-in-JS theme objects
   - Design token files (tokens.json, *.tokens.*)

2. DETECT naming pattern:
   - Prefix convention (--color-*, --bg-*, $spacing-*)
   - Tier structure (primitive → semantic → component)
   - Categorization (color, spacing, typography, radius, shadow)

3. MATCH Figma values to existing tokens:
   - Color: match hex/rgba to nearest token
   - Spacing: match px values to spacing scale
   - Typography: match font-size/weight/family to type tokens
   - Radius: match border-radius to radius tokens

4. FLAG missing tokens:
   - Value needed but no token exists → ASK user
   - Present options: closest match, create new, custom
   - NEVER create a token without user approval
```

## Action Router

```
User input
  │
  ├─ "structure", "spec component",
  │  "component structure"              → Load references/actions/structure.md
  │
  ├─ "doc", "document component",
  │  "component doc"                    → Load references/actions/doc.md
  │
  ├─ "dev", "develop component",
  │  "implement component",
  │  "component dev"                    → Load references/actions/dev.md
  │
  ├─ "review", "review component",
  │  "component review",
  │  "check component"                  → Load references/actions/review.md
  │
  └─ "audit", "audit component",
     "component audit",
     "audit ds", "audit design system"  → Load references/actions/audit.md
```

**Loading rule:** Read the action file BEFORE executing. The action file contains all logic, principles references, and templates needed.

**Input detection:**
```
Input contains figma.com URL?
  YES → Extract fileKey + nodeId, call Figma MCP
  NO  → Check if input is a file path (contains / or .)
    YES → Load from codebase
    NO  → Treat as component name, search codebase
```

## Project Structure (in user's project)

```
ds/
├── specs/
│   ├── active/       ← Current specs (from structure action)
│   ├── shipped/      ← Components delivered
│   └── dropped/      ← Abandoned specs
└── audits/
    ├── active/       ← Current audit findings
    ├── shipped/      ← Fixes applied
    └── dropped/      ← Won't fix

ComponentName/
├── ComponentName.{ext}  (detected from project)
├── doc.md             ← Generated by doc action
├── ComponentName.test.ts
└── index.ts
```

## Principles

Standards that inform every action. Loaded by `review` and `audit` for compliance checks.

| Principle | Standard | Reference |
|-----------|----------|-----------|
| Composition | Atomic Design (Brad Frost) | [composition.md](references/principles/composition.md) |
| Naming | BEM (Block Element Modifier) | [naming.md](references/principles/naming.md) |
| Tokens | DTCG (W3C Design Token Community Group) | [tokens.md](references/principles/tokens.md) |
| Props API | Component API patterns | [props-api.md](references/principles/props-api.md) |
| Accessibility | WCAG 2.1 AA | [accessibility.md](references/principles/accessibility.md) |

## Templates

### File Templates (generated output files)

| Template | Used by | Reference |
|----------|---------|-----------|
| Component spec | `structure` | [spec.md](references/templates/spec.md) |
| Component doc | `doc` | [doc.md](references/templates/doc.md) |
| Audit report | `audit` | [audit-report.md](references/templates/audit-report.md) |

### Output Templates (chat status messages)

| Template | Used by | Reference |
|----------|---------|-----------|
| Structure output | `structure` | [structure-output.md](references/templates/structure-output.md) |
| Doc output | `doc` | [doc-output.md](references/templates/doc-output.md) |
| Dev output | `dev` | [dev-output.md](references/templates/dev-output.md) |
| Review output | `review` | [review-output.md](references/templates/review-output.md) |
| Audit output | `audit` | [audit-output.md](references/templates/audit-output.md) |

## Configuration

All behavior is configurable by editing the skill files directly.

| What to change | Edit |
|----------------|------|
| Action logic | `references/actions/{action}.md` |
| DS principles | `references/principles/{principle}.md` |
| Output templates | `references/templates/{template}.md` |

## References

Actions:
- [Structure](references/actions/structure.md) | [Doc](references/actions/doc.md) | [Dev](references/actions/dev.md) | [Review](references/actions/review.md) | [Audit](references/actions/audit.md)

Principles:
- [Composition](references/principles/composition.md) | [Naming](references/principles/naming.md) | [Tokens](references/principles/tokens.md) | [Props API](references/principles/props-api.md) | [Accessibility](references/principles/accessibility.md)

Templates (files):
- [Spec](references/templates/spec.md) | [Doc](references/templates/doc.md) | [Audit Report](references/templates/audit-report.md)

Output (chat):
- [Structure](references/templates/structure-output.md) | [Doc](references/templates/doc-output.md) | [Dev](references/templates/dev-output.md) | [Review](references/templates/review-output.md) | [Audit](references/templates/audit-output.md)
