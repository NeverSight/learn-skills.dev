---
name: plan-prd
description: Create a Product Requirements Document (PRD) with user stories, state matrix, and accessibility requirements. Use for large features requiring full UX specification.
---

# Plan PRD

Create a comprehensive Product Requirements Document.

## When to Use
- Large features or epics
- New user-facing functionality
- Features requiring UX exploration

## Artifacts
- `PRD-[EPIC-NAME].md` in `docs/working/`
- `task.md` updated via `task_boundary`

## Approach

### Phase 1: Discovery & Scope
1. **Proof of Understanding**: Summarize core user problem in one sentence.
2. **User Stories**: "As a [user], I want [action], so that [benefit]"
3. **Non-Goals**: Explicitly state out-of-scope items.

### Phase 2: Design Options (Forced Diversity)
Generate **4-6 architecturally distinct options** varying:
- Information architecture
- Interaction model
- Visual hierarchy

Use Socratic Debate for complex decisions:
- Proponent argues for option
- Adversary critiques
- Synthesis resolves

### Phase 3: Detailed UX Specification

#### State Matrix
| State | Visual | Behavior |
|-------|--------|----------|
| Default | ... | ... |
| Hover | ... | ... |
| Focus | ... | ... |
| Active | ... | ... |
| Disabled | ... | ... |
| Empty | ... | ... |
| Loading | ... | ... |
| Error | ... | ... |

#### ASCII Wireframes
Use `var(--token-name)` syntax. Reference existing patterns.

#### Accessibility Requirements
- Keyboard navigation path
- ARIA labels/roles
- Screen reader announcements
- Reduced motion considerations

### Phase 4: Validation
- UX Risks & Mitigations table
- Definition of Done checklist
- Reflexion: Hostile Accessibility Auditor critique

## Constraints
- No technical architecture — handled in `plan/architecture`
- All options must consider light/dark mode, accessibility
- Flag as "Hallucination" if using non-existent design tokens
