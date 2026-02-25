---
name: context-snapshot
description: Create a durable handoff file that captures important conversation state for agent continuity. Use when the context window is getting full, when switching agents/sessions, when handing off work, or when asked to summarize progress without losing decisions, constraints, risks, and pending tasks.
---

# Context Snapshot

Create one handoff file with the highest-signal context from the current conversation.

## Workflow

### 1. Choose output path

- If the user provides a path, use it.
- Otherwise create `handoffs/context-<YYYY-MM-DD-HHMM>.md`.
- Create the parent directory if it does not exist.

### 2. Map territory (MANDATORY)

- Inventory key domains before writing:
  - Goals and success criteria.
  - Decisions and rationale.
  - Constraints and non-goals.
  - Files/artifacts and command outcomes.
  - Risks, blockers, open questions.
- Capture exact wording for non-negotiable decisions and constraints.

### 3. Score friction and choose depth mode (MANDATORY)

Select one mode:

| Mode | Use when | Depth |
| :--- | :--- | :--- |
| `quick` | Estimated conversation size is small and task scope is single-track | Minimal bullets, highest-priority items only |
| `standard` | Typical multi-step task with moderate context | Full template, balanced detail |
| `forensic` | Large context, contradictions, or high-risk decisions | Full template plus contradiction/TODO tracking |

### 4. Respond by mode

Extract only what a new agent needs to continue safely:

- User goals and success criteria.
- Decisions and rationale.
- Constraints, assumptions, and non-goals.
- Files touched or referenced.
- Commands run and key outcomes.
- Open questions, risks, and blockers.
- Current status and next steps.

### 5. Write the handoff file

- Copy [context-template.md](./assets/context-template.md) into the output path.
- Fill every section.
- If a section has no data, write `None`.
- Add `source:` tags to major claims, decisions, blockers, and next steps.
- Example: `- API key rotation blocked by IAM policy (source: command output, aws iam get-role)`

### 6. Validate before finishing

- Keep facts concrete and traceable to the conversation.
- Keep paths, commands, and identifiers exact.
- Remove low-signal narrative and duplicate points.
- Ensure next steps are actionable and ordered.
- Mark uncertainty with `TODO` instead of guessing.
- Set confidence level: `high`, `medium`, or `low`.

## Critical Rules (MANDATORY)

- Prioritize fidelity over prose.
- Preserve exact phrasing for decisions and hard constraints.
- Separate facts from assumptions using explicit labels.
- Include concrete dates when timing matters.
- Do not omit failed attempts if they affect next steps.
- Keep output concise but complete; use bullets.

## Forbidden Behaviors

- Do not invent decisions, rationale, owners, or outcomes.
- Do not silently resolve conflicting statements.
- Do not omit blockers just because they are unresolved.
- Do not rewrite critical commitments into generic language.
- Do not output only narrative text when structured fields are required.

## Confidence Gate

- `high`: No material contradictions; next steps are executable.
- `medium`: Minor uncertainty; `TODO` items are explicit.
- `low`: Major gaps or contradictions; list blocking questions before handoff.

## Compression Heuristics

- Keep only information needed for safe continuation.
- Remove conversational filler and repeated explanations.
- Merge related updates into one state description.
- Preserve irreversible decisions and unresolved risks.
