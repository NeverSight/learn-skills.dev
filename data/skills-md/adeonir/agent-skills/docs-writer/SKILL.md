---
name: docs-writer
description: Generate structured product and technical documents through guided discovery. 8 document types (PRD, Brief, Issue, Task, User Story, RFC, ADR, TDD). Use when defining products, reporting bugs, planning tasks, writing stories, proposing changes, recording decisions, designing systems. Also use when the user wants to document a feature idea, write requirements, formalize a decision, describe a bug they found, plan technical architecture, or needs any structured document for a project. Triggers on "create PRD", "create issue", "report bug", "feature request", "create task", "create user story", "create RFC", "create ADR", "create TDD", "create document", "write doc", "document this", "need a spec", "write requirements".
metadata:
  author: github.com/adeonir
  version: "1.0.0"
---

# Docs Writer

Generate structured documents through guided discovery. 8 document types, each with its own workflow depth.

## Workflow

```
trigger --> detect type --> load reference --> discovery --> drafting
```

Detect document type from the trigger. If ambiguous, ask the user which type they want.

## Document Types

| Type | Workflow | Reference | Template |
|------|----------|-----------|----------|
| PRD | discovery -> validation -> synthesis -> drafting | [prd.md](references/prd.md) | [prd.md](templates/prd.md) |
| Brief | generated with PRD (no separate trigger) | [brief.md](references/brief.md) | [brief.md](templates/brief.md) |
| Issue | classification -> [clarification] -> drafting | [issue.md](references/issue.md) | [issue.md](templates/issue.md) |
| Task | direct drafting | [task.md](references/task.md) | [task.md](templates/task.md) |
| User Story | [clarification] -> drafting | [user-story.md](references/user-story.md) | [user-story.md](templates/user-story.md) |
| RFC | [clarification] -> analysis -> drafting | [rfc.md](references/rfc.md) | [rfc.md](templates/rfc.md) |
| ADR | [clarification] -> drafting | [adr.md](references/adr.md) | [adr.md](templates/adr.md) |
| TDD | discovery -> analysis -> drafting | [tdd.md](references/tdd.md) | [tdd.md](templates/tdd.md) |

## Context Loading Strategy

Load the reference and template matching the detected document type. For types that require discovery, also load [discovery.md](references/discovery.md).

**Never simultaneous:**
- Multiple document type references
- Templates for different document types

## Triggers

| Trigger Pattern | Type | Reference |
|-----------------|------|-----------|
| Create PRD, define product, product requirements, write PRD | PRD | [prd.md](references/prd.md) |
| Create issue, report bug, feature request, create discussion | Issue | [issue.md](references/issue.md) |
| Create task, new task | Task | [task.md](references/task.md) |
| Create user story, write story, new story | User Story | [user-story.md](references/user-story.md) |
| Create RFC, propose change, request for comments | RFC | [rfc.md](references/rfc.md) |
| Create ADR, record decision, architecture decision | ADR | [adr.md](references/adr.md) |
| Create TDD, technical design, design document | TDD | [tdd.md](references/tdd.md) |
| Create document, write doc | Ask user | -- |

## Shared Discovery Patterns

**LOAD:** [discovery.md](references/discovery.md) before starting any type that requires discovery.

Discovery applies to: PRD, TDD.
Clarification (lightweight, only when input is incomplete) applies to: RFC, ADR, Issue (feature/discussion subtypes), User Story.
Neither applies to: Task, Issue (bug subtype -- uses structured collection instead), Brief (generated as part of PRD workflow).

## Output

All documents save to `.artifacts/docs/`. Create the directory if it doesn't exist.

| Type | Filename |
|------|----------|
| PRD | `prd.md` |
| Brief | `brief.md` |
| Issue | `issue.md` |
| Task | `task.md` |
| User Story | `story.md` |
| RFC | `rfc.md` |
| ADR | `adr-{number}-{name}.md` |
| TDD | `tdd.md` |

For ADR, use kebab-case for `{name}` and auto-detect the next sequential number from existing files in `.artifacts/docs/`.

## Quality Standards

Requirements must be concrete and measurable across all document types.

| Bad | Good |
|-----|------|
| "Search should be fast" | "Search returns results within 200ms" |
| "Easy to use" | "New users complete onboarding in under 2 minutes" |
| "Intuitive interface" | "Task completion rate above 90% without help text" |

## Cross-References

```
PRD -------------> TDD            (PRD feeds requirements, journeys, rules into TDD)
PRD -------------> design-builder (PRD + Brief inform copy and design extraction)
PRD -------------> spec-driven    (PRD milestones feed spec initialization)
RFC -------------> ADR            (accepted RFC generates ADR)
TDD -------------> ADR            (references relevant decisions)
```

Notes:

- **design-builder**: PRD sections 1, 3-4 (problem, personas, scope) and Brief (value prop, market) inform copy extraction and design extraction
- **spec-driven**: PRD milestones feed feature initialization -- each milestone can generate a spec with its own tasks

## Guidelines

**DO:**
- Always complete discovery before drafting (for types that require it)
- Present draft for user feedback before saving
- Mark unknowns as TBD rather than inventing constraints
- Use concrete, measurable requirements
- Use fixed filenames per type (ADR keeps `{name}` suffix in kebab-case)

**DON'T:**
- Skip discovery for types that require it
- Assume document type -- detect from trigger or ask
- Include visual/design direction (that belongs in design-builder)
- Use vague adjectives as requirements ("fast", "easy", "intuitive")
- Mix document types in a single file

## Error Handling

- No `.artifacts/docs/`: Create the directory
- Ambiguous trigger: Ask user which document type
- Missing context for discovery: Ask questions, never assume
- ADR numbering conflict: Scan existing files and use next available number
