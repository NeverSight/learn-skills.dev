---
name: docs-maker
description: Create and refactor AI-readable structured documentation for any domain, optimized for fast parsing, recall, and reliable execution.
compatibility: Works best with read/edit/write and shell search tools for document analysis and quality checks.
---

@rules/sequential-thinking.md
@rules/context-engineering.md
@rules/forbidden-patterns.md
@rules/required-behaviors.md

# Docs Maker Skill

> Unified documentation skill for both creation and refactoring.

<purpose>

- Build new structured docs that AI can parse and retain quickly.
- Refactor existing docs to improve density, clarity, and retrieval quality.
- Keep docs execution-oriented with explicit rules, workflows, and validation.

</purpose>

<trigger_conditions>

| Situation | Mode |
|------|------|
| New structured guidance is needed | create |
| Existing guidance is too long or repetitive | refactor |
| Existing guidance is vague or hard to scan | refactor |
| Team wants one consistent documentation shape | create/refactor |

</trigger_conditions>

<supported_targets>

- Policy documents
- Playbooks and runbooks
- Technical specs and design notes
- Workflow and process guides
- Prompting and agent-operation guides

</supported_targets>

<mandatory_reasoning>

## Mandatory Sequential Thinking

- Always use `sequential-thinking` before writing.
- In create mode: use it to design section structure and constraints.
- In refactor mode: use it to identify redundancy, ambiguity, and compression opportunities.
- Do not edit documents before this plan is complete.

</mandatory_reasoning>

<context_engineering_application>

Apply context-engineering defaults to every major edit:

- Choose the right instruction altitude (avoid overly low branching and overly high vagueness).
- Treat tokens as finite; keep the core doc compact and push detail into `rules/`.
- Use explicit, concrete directives for Claude 4.x behavior.
- Prefer XML-segmented sections and table compression for stable retrieval.
- Use progressive disclosure: metadata -> core workflow -> deep rules.

</context_engineering_application>

<modes>

## create mode

- Start from a minimal skeleton.
- Add only high-value rules and runnable examples.
- Prefer tables/checklists over long prose.

## refactor mode

- Preserve critical intent and operational behavior.
- Remove repetition and vague guidance.
- Convert explanation-heavy sections into compact tables and examples.

</modes>

<workflow>

| Phase | Task | Output |
|------|------|------|
| 1 | Read target docs and classify mode (`create`/`refactor`) | Scope + mode |
| 2 | Build structure plan with `sequential-thinking` | Section plan |
| 3 | Write/refactor content | Updated document |
| 4 | Validate quality and consistency | Finalized document |

### Phase 3 implementation rules

- Use explicit sections with stable headings.
- Prefer positive directives (`Do X`) over negative-only rules.
- Keep examples copy-paste ready.
- Keep instructions specific (avoid terms like "appropriately", "if needed" without criteria).
- Use consistent terminology for the same concept across the full document.
- Keep sections small and scannable so retrieval is reliable under context pressure.

</workflow>

<forbidden>

| Category | Avoid |
|------|------|
| Structure | Unstructured long paragraphs with mixed concerns |
| Content | Redundant rules repeated in multiple sections |
| Guidance | Ambiguous instructions without decision criteria |
| Quality | Removing key constraints during refactor |

</forbidden>

<required>

| Category | Required |
|------|------|
| Clarity | Clear section hierarchy and concise wording |
| Actionability | Concrete workflow steps and validation checks |
| Examples | Runnable or directly reusable examples |
| Consistency | Same terminology and rule style across sections |

</required>

<structure_blueprint>

Use this default layout unless a better domain-specific layout is required:

1. Objective
2. Scope and assumptions
3. Rules (`forbidden` / `required`)
4. Execution workflow (phase/step based)
5. Examples (good/bad or runnable patterns)
6. Validation checklist

</structure_blueprint>

<validation>

| Check | Rule |
|------|------|
| Structure | Major sections are clearly separated |
| Density | Repetition removed; tables used where helpful |
| Actionability | Steps can be executed without guessing |
| Examples | Examples match actual workflow and tools |
| Safety | Critical constraints preserved after refactor |
| Context quality | Right altitude + explicitness + low redundancy |

Completion checklist:
- [ ] Mode decided (`create` or `refactor`)
- [ ] Sequential-thinking plan created first
- [ ] Context-engineering checks applied (`rules/context-engineering.md`)
- [ ] Document updated with compact structure
- [ ] Validation checks completed

</validation>
