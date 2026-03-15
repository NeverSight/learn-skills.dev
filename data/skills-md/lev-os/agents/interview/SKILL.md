---
name: interview
description: Wizard-mode questioning skill for structured decision-making. Uses framework library (SCAMPER, First Principles, Systems Thinking, etc.) to guide users through complex decisions one question at a time.
version: 1.2.0
skill_type: playbook
category: process-ask
extends: []
related_skills:
  - think
  - work
  - lev-cdo
---

# Interview: Wizard-Mode Questioning

**Framework-powered interactive decision-making.** Guides users through complex problems using strategic, creative, and philosophical frameworks.

## Quick Start

```bash
/interview                    # Start new interview session
/interview --framework=SCAMPER  # Start with specific framework
```

## Hard Requirements (Non-Optional)

1. **Research between every question** — run fresh evidence-gathering before each new question.
2. **Work lifecycle coupling** — when `.lev/pm/` exists, treat interview as part of `work` lifecycle and update active artifacts.
3. **Context-rich questions only** — never ask "ingredient-only" option prompts without decision context and consequences.
4. **Trade-off transparency** — always surface trade-offs, validation-gate impact, and side effects.

## How It Works

1. **Context Analysis** - Detect complexity and classify decision level (strategic/integrative/tactical).
2. **Framework Selection** - Choose one primary framework and one cross-check lens.
3. **Per-Question Research (required)** - Before each question, collect new evidence from workspace, prior answers, and constraints.
4. **Lifecycle Sync (required with `work`)** - Track entities/decisions and iterate handoff/spec/proposal docs as context evolves.
5. **Question Loop (reciprocal)** - Ask one structured question, answer one reciprocal user question, then continue.
6. **Decision Assimilation** - After each answer, update artifacts and convert resolved questions into explicit decisions.
7. **MBTI Overlay** (optional) - Use only when perspective-testing is useful.

## Per-Question Research Protocol (Required)

Before each question, do all of:

1. Pull evidence from current workspace context (specs, handoffs, plans, code).
2. Check active constraints and quality gates.
3. Validate whether the next question still matters based on newly discovered facts.

Minimum evidence set per question:

- One artifact fact from `.lev/pm/` (spec/handoff/proposal/plan).
- One implementation or architecture fact from code/docs.
- One validation constraint from `.lev/validation-gates.yaml` when present.

If no new evidence exists, explicitly state that and why the next question is still needed.

## Work Lifecycle Coupling (Required when `.lev/pm/` exists)

Interview mode is not standalone Q&A. It is a foreground intake loop inside `work` DISCOVER/ALIGN.

When active:

1. Locate active handoff under `.lev/pm/handoffs/` and keep it current.
2. Track entities (state changes, blockers, decisions) using lifecycle language.
3. Iterate affected docs after each major answer:
   - specs (`.lev/pm/specs/`)
   - proposals (`.lev/pm/proposals/`)
   - handoffs (`.lev/pm/handoffs/`)
4. Convert resolved open questions into decisions with rationale and consequence.
5. Carry unresolved items forward with explicit owner/next action.

Degrade gracefully if artifacts are missing, but do not skip lifecycle sync silently.

## Session Handoff Bootstrap (Hard Rule)

If there is no active session handoff, the interview must not proceed as normal Q&A.

Required behavior:

1. Load `$work` and run DISCOVER lifecycle preflight.
2. Create or update the active handoff under `.lev/pm/handoffs/`.
3. Record stage, objective, and initial evidence before asking decision questions.
4. Resume interview loop only after handoff continuity exists.

Enforcement:

- If `$work` cannot be loaded, stop and ask the user to resolve the blocker.
- Do not run fallback interview behavior without `work` lifecycle initialization.

## Framework Library

### Strategic/Systems Thinking
- SWOT, First Principles, Systems Thinking, Theory of Constraints
- McKinsey 7S, Cynefin, Jobs to Be Done

### Creative Thinking
- SCAMPER, Reverse Brainstorming, Extreme Users
- Six Thinking Hats, Figure Storming, TRIZ, Design Thinking

### Philosophical/Spiritual
- Taoist Wu Wei, Ubuntu, Ayurvedic Doshas
- Buddhist Non-Attachment, Sufi/Rumi Poetry, I Ching, Stoicism

### Psychological/Cognitive
- MBTI (8 Cognitive Functions), Big Five (OCEAN), Ladder of Inference

## Output Format

Single question with grounded options:
```
q1) {Question title}
🎯 Decision Context:
- {What decision is being made}
- {Why this decision is needed now}
- {What gets blocked/unblocked}
- {What could break if wrong}

🧠 {Framework Name} Analysis:
{Framework-based interpretation of the decision and pressure points}

🔎 Evidence (research run this turn):
- {Prior answer + artifact evidence with path}
- {Code/doc fact relevant to this decision}
- {Validation gate(s) impacted from .lev/validation-gates.yaml}
- {Constraint/conflict/assumption check}

⚖️ Trade-off Summary:
| Option | Benefits | Costs/Risks | Gate Impact | Side Effects |
|---|---|---|---|---|
| a | ... | ... | ... | ... |
| b | ... | ... | ... | ... |
| c | ... | ... | ... | ... |  # optional

Options (2-3 researched):
a. {Concrete option A with trade-off}
b. {Concrete option B with trade-off}
c. {Concrete option C with trade-off}  # optional

✅ Recommended: {Option letter} — {Why this best fits evidence and constraints}

🤝 Reciprocal:
User may ask one question; answer directly before next interview question.

🧭 Follow-Up Menu:
1. [{Action for option A}]
2. [{Action for option B}]
3. [{Alternative perspective}]
4. [Deep dive into trade-offs]
5. [Go back]
6. [Switch framework]
```

## Integration

- **Command:** `/interview` (formerly `/guideme`)
- **Skill Route:** `skill://interview`
- **Used by:** `work` skill for wizard-mode context gathering
- **Lifecycle Hook:** In repos with `.lev/pm`, interview must update entities/handoffs/docs as part of `work` progression
- **Gate Awareness:** Interview must consult `.lev/validation-gates.yaml` for option-level compliance and side effects

---

**Status:** v1.2.0
**Migrated from:** /guideme command

## Technique Map

- **Identify scope** — Determine what the skill applies to before executing.
- **Follow workflow** — Use documented steps; avoid ad-hoc shortcuts.
- **Ground every question** — No question without fresh per-turn evidence from context/research.
- **Show research trace** — Make evidence visible in every question.
- **Update lifecycle artifacts** — Maintain handoff/spec/proposal continuity when `.lev/pm` is active.
- **Recommend explicitly** — Always include a best option and rationale.
- **Expose trade-offs** — Include gate impact, side effects, and blast radius.
- **Use reciprocity** — Handle one user counter-question before advancing.
- **Verify outputs** — Check results match expected contract.
- **Handle errors** — Graceful degradation when dependencies missing.
- **Reference docs** — Load references/ when detail needed.
- **Preserve state** — Don't overwrite user config or artifacts.

## Technique Notes

Skill-specific technique rationale. Apply patterns from the skill body. Progressive disclosure: metadata first, body on trigger, references on demand.

## Prompt Architect Overlay

**Role Definition:** Specialist for interview domain. Executes workflows, produces artifacts, routes to related skills when needed.

**Input Contract:** Context, optional config, artifacts from prior steps. Depends on skill.

**Output Contract:** Artifacts, status, next-step recommendations. Format per skill.

**Edge Cases & Fallbacks:** Missing context—ask or infer from workspace. Missing lifecycle artifacts—create minimal continuity notes and continue. Dependency missing—degrade gracefully and state what could not be validated. Ambiguous request—clarify before proceeding.
