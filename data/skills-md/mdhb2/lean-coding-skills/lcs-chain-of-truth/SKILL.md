---
name: lcs-chain-of-truth
description: 'Meta-skill protocol that enforces auditable evidence chains across all LCS skills. Activated when any LCS skill needs to produce verifiable, traceable output — not a standalone skill, but a protocol injected into execution flows requiring auditability.'
---

# LCS Chain of Truth

## Purpose

`lcs-chain-of-truth` is a **meta-skill** — it does not replace other skills. It is a protocol injected by other LCS skills when they need to produce **auditable, verifiable, traceable evidence** of their work.

Use it as a layer added on top of skill execution, not as a standalone flow.

---

## Trigger

Activate this protocol when any LCS skill:
- Produces output that will be committed or shipped
- Makes decisions that affect contracts, specs, or plans
- Executes code changes, reviews, or finalizations
- Requires a verifiable audit trail for human review

---

## Chain of Truth Flow

Every Chain of Truth report must traverse these 6 stages in order:

```
Source → Assumption → Plan → Action → Verification → Report
```

| Stage | Description |
|---|---|
| **Source** | Identify the raw inputs: files read, user inputs, prior artifacts, external references. Quote exact paths and line numbers. |
| **Assumption** | List every assumption made about inputs, context, or behavior. Flag assumptions that could not be verified. |
| **Plan** | State the intended actions before executing them. No hidden reasoning. |
| **Action** | Record what was actually done — commands run, files written, edits applied. |
| **Verification** | Run available checks. Record exact command output. Use fallbacks if verification tools unavailable. |
| **Report** | Summarize: what passed, what failed, what remains unverified, and confidence level. |

---

## Chain of Thought Warning

**Prohibition**: Do NOT expose hidden internal chain-of-thought in outputs.

Chain of Truth is about **external, auditable evidence** — sources, actions, and verifiable results. It is not a dump of internal reasoning steps.

- Allowed: "Read file X line 12. Found pattern Y. Wrote Z."
- Prohibited: "I think this probably works because intuitively…"
- Prohibited: Claiming verification passed without running it.
- Prohibited: Skipping source identification.

---

## Four Levels

Choose the level based on risk and context. Declare it at the start of the Chain of Truth Report.

### Level 1 — Light

**Use for**: Exploratory or conversational skills (lcs-explore, early brainstorming).

Requirements:
- Source: identify key inputs
- Assumption: list top 2–3 assumptions
- Plan: brief intent statement
- Action: summary of what was done
- Verification: manual check or "not applicable"
- Report: 1–3 sentences

### Level 2 — Standard

**Use for**: Planning and documentation skills (lcs-new, lcs-toprd, lcs-onboarding, lcs-task-slicer, lcs-self-improvement).

Requirements:
- Source: all files read, with paths
- Assumption: full list, flagging unverified ones
- Plan: enumerated steps
- Action: per-step record of what was done
- Verification: command output or manual review result
- Report: structured summary with confidence rating

### Level 3 — Strict

**Use for**: Contracts, reviews, finalization (lcs-prd-reviewer, lcs-doc-finalizer, lcs-codebase-doc).

Requirements:
- All Level 2 requirements, plus:
- Source: exact line references for all quoted content
- Assumption: each assumption must be labeled `[verified]` or `[unverified]`
- Verification: must attempt automated checks; document every failure
- Report: explicit pass/fail per acceptance criterion

### Level 4 — Very Strict

**Use for**: Code changes, debugging, implementation (lcs-task-executor, lcs-debug-ext).

Requirements:
- All Level 3 requirements, plus:
- Action: exact commands run with stdout/stderr captured
- Verification: all test and lint commands must be run; results quoted verbatim
- Report: blocked items listed explicitly; no "assumed passing" allowed
- Confidence must be stated as `high`, `medium`, or `low` with justification

---

## Report Placement Rule

The **Chain of Truth Report** section must appear **before** the `## Handoff` section in any artifact that uses this protocol.

```markdown
## Chain of Truth Report
Level: <1–4>
...

## Handoff
...
```

---

## Verification Rules

1. **Attempt verification if tools are available**: run linter, test suite, or `Test-Path` as appropriate.
2. **Fallbacks for markdown/docs repos**: if no test suite exists, use `Select-String` pattern checks or manual read confirmation.
3. **Never skip**: record "not applicable" with a reason rather than silently omitting verification.
4. **Never claim pass without running**: if a check was not executed, mark it `[unverified]`.

---

## Anti-Patterns

| Anti-Pattern | Why Prohibited |
|---|---|
| Claiming verification passed without running it | Breaks auditability |
| Exposing internal chain-of-thought reasoning | Pollutes the evidence chain with speculation |
| Skipping source identification | Makes the report unreproducible |
| Writing Report before Action completes | Report must reflect reality, not intent |
| Omitting failed checks from Report | Hides risk from reviewers |

---

## Skill Level Mapping

Each LCS skill declares its Chain of Truth level:

| Skill | Level | Rationale |
|---|---|---|
| `lcs-explore` | Light (1) | Exploratory, conversational, low-stakes |
| `lcs-toprd` | Standard (2) | Planning artifact, structured output |
| `lcs-tosrs` | Strict (3) | Spec derivation from PRD |
| `lcs-onboarding` | Standard (2) | Documentation generation |
| `lcs-task-slicer` | Strict (3) | Task breakdown planning |
| `lcs-self-improvement` | Standard (2) | Diagnostic analysis and recommendations |
| `lcs-prd-reviewer` | Strict (3) | Reviews contracts, flags acceptance criteria |
| `lcs-doc-finalizer` | Strict (3) | Finalizes and archives canonical docs |
| `lcs-codebase-doc` | Strict (3) | Codebase mapping and onboarding documentation |
| `lcs-debug` | Standard (2) | Question-asking investigation skill, no code changes applied |
| `lcs-debug-ext` | Very Strict (4) | Evidence-based debug reports without code changes |
| `lcs-task-executor` | Very Strict (4) | Code implementation with tests and lint (canonical spelling) |
| `lcs-new` | Standard (2) | Blank work-item registration, no artifacts created |
| `lcs-chain-of-truth` | — | Meta-protocol, not self-applied |

---

## Chain of Truth Level

Level: Meta

This skill defines the LCS Chain of Truth protocol and is not self-applied.

## Handoff

Next recommended skill: lcs-shared
Next file to read: `skills/lcs-shared/contract.md`
Current phase: reference
Current confidence: high
Blocking questions: None
Risks to carry forward: None
Source of Truth Bundle: skills/lcs-chain-of-truth/SKILL.md (reference, not self-applied)
Must Preserve IDs: None
Unresolved IDs: None
Suggested next command: N/A — reference skill, no execution flow
