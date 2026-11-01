---
name: fable-council
description: "Convene a council of AI coding agents before finalizing a plan. The agent you're talking to — whichever CLI is the lead (claude, codex, cursor, gemini, grok, opencode) — drafts a plan, presents it independently to every other agent CLI installed on the machine, each member gives ONE reply per turn, and the lead revises the plan for X turns before answering. Trigger words: council, convene the council, consult the other agents, ask the council, ask codex/cursor/gemini/grok what they think, second opinion from other agents, N turns of deliberation, deliberate before planning."
version: 1.0.0
pack: system
inputs:
  - draft_plan
  - member_clis
requires:
  - installed_agent_clis
produces:
  - counciled_plan
  - deliberation_transcript
gates:
  - multi_agent_consensus
  - rounds_completed
fallback: fable-plan
mutatesWorkspace: false
parallelSafe: false
neural_links:
  precursors:
    - fable-plan
  continuations:
    - fable-execute
  lateral_peers:
    - fable-delegate
  recovery: fable-recover
---

# Fable Council

Convene a council of AI coding agents before finalizing an architectural plan. Propose → hear independent assessments from each installed agent CLI → revise, repeated across bounded deliberation rounds.

## Purpose

Enforce multi-agent deliberation and cross-model consensus on complex plans. Leverage complementary models (Claude, Codex, Cursor, Gemini, Grok, OpenCode) to detect blind spots, challenge flawed assumptions, and converge on robust engineering plans.

## When to Use

- When planning high-stakes architectural changes, major refactorings, or migrations.
- When the user asks to convene the council or get second opinions ("ask the council", "consult the other agents").
- When deliberating between multiple competing implementation strategies.

## When NOT to Use

- Bounded single-file bugfixes or routine implementation tasks (use `fable-execute` or `fable-tdd`).
- When no other agent CLIs are installed on the local system (fall back to solo `fable-plan`).
- Post-implementation diff verification or code review (use `fable-review` or `fable-judge`).

## Inputs

- `draft_plan`: The lead agent's initial architectural proposal.
- `member_clis`: List of detected or user-specified agent CLI binaries on the host machine.
- `rounds_count`: Number of deliberation turns requested (default: 1).

## Expected Outputs

- `counciled_plan`: The final synthesized plan refined through multi-agent critiques.
- `deliberation_transcript`: Structured conversational record of member critiques, adopted changes, and rejected arguments.

## Procedure

1. **Parse Request**: Extract the core task, requested number of turns (X), and identify the host lead runtime (`SELF`).
2. **Detect Members**: Probe available CLIs on PATH (`claude`, `codex`, `cursor-agent`, `gemini`, `grok`, `opencode`) minus `SELF`.
3. **Initialize Session**: Create `~/.council/<timestamp>-<slug>` and persist the verbatim task to `task.md` and initial plan to `plan-v1.md`.
4. **Deliberation Loop (1..X)**:
   - Generate prompt per member with strict read-only execution flags.
   - Invoke all members concurrently in background processes with a ~300s timeout.
   - Collect and parse member responses.
   - Revise the plan: adopt valid critiques, reject flawed suggestions with explicit technical reasoning.
   - Produce `plan-v(R+1).md` and `changes-v(R+1).md`.
5. **Format Final Answer**: Present the deliberation conversation followed by the finalized consensus plan.

## Decision Rules

- The lead agent never implements changes during a council run; planning and deliberation only.
- Council members are invoked in read-only mode (`--mode plan`, `-s read-only`, `--skip-trust`).
- All member suggestions are evaluated on technical merit, not model authority.
- Retaining original positions is permitted when supported by concrete technical rationale.

## Tool Policy

- Execute member CLI binaries in parallel using non-interactive flags.
- Enforce strict timeouts (e.g. via Perl alarm or process managers on macOS).
- Pass system prompt overrides to headless models (e.g. Grok) to prevent unauthorized tool-use stalls.

## Evidence Requirements

- Deliberation session artifacts saved under `~/.council/`.
- Verbatim quotes and rationale for accepted vs rejected recommendations.

## Failure Handling

- If a member CLI times out or errors, record the timeout and proceed without blocking the round.
- If no secondary agent CLIs exist on the machine, explicitly declare a solo un-counciled plan.

## Completion Criteria

- All X deliberation rounds completed without deadlock.
- Deliberation transcript and final synthesized plan presented clearly.
- Deliverable ready for human sign-off before any execution begins.
