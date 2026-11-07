---
name: monozukuri-router
description: "Step 0 of consequential software work under Monozukuri, run by monozukuri-core. Classify the task, assess its risk tier, choose execute or sensei mode, and compose the sequence of Monozukuri skills and the Definition of Done for it. Skip for trivial one-line edits, pure questions, and throwaway scripts."
user-invocable: false
---

# Monozukuri router

The router does no engineering work itself. It decides which Monozukuri
practices apply to the task in front of it and in what order, emits a plan
header, and hands off to the composed sequence.

## Use this skill when

- any feature, bugfix, refactor, incident, migration, release, or
  investigation that is more than a one-line change;
- the user asks to be guided or taught;
- the user asks for a review of their own approach; or
- the user asks to set up Monozukuri for a project.

## Do not use when

- the change is a trivial one-liner;
- the request is a pure question with no change to the system; or
- the code is a throwaway script.

## Procedure

1. **Choose interaction mode.** `execute` (default) or `sensei`. Route to
   `sensei` when the user asks to be guided / taught / reviewed / set up.
   Incident or "production is down" language forces `execute`. Detail in
   `monozukuri-core/references/sensei.md`.
2. **Classify the task.** Pick one type: `feature`, `bugfix`, `refactor`,
   `incident`, `migration`, `release`, `investigation`, `docs`, `greenfield`
   (a new project, or a new standalone subsystem, built from scratch). Set
   context flags: `security`, `performance`, `production`, `data`, `auth`.
3. **Assess risk.** Tier `low|medium|high|critical` per
   `monozukuri-core/references/constitution.md`. When signals disagree, take
   the higher tier.
4. **Low-risk fast-path.** If the tier is `low` and no modifier applies
   (documentation work is nearly always this): emit
   `fast-path: apply genchi-genbutsu + kanso + kodawari inline` and stop. Never
   inflate a small task.
5. **Compose.** Look up the playbook in
   `monozukuri-core/references/playbooks.md`; apply the `security` /
   `performance` modifiers matching the context flags; scale verification
   depth by risk tier. For `greenfield`, the sequence begins `nemawashi →
   monozukuri-blueprint`; the four blueprint stages are gated on user
   approval, and phases execute one at a time after stage 4.
6. **Decide execution mode per step.** Default every step to inline. Mark a
   step for delegation only when it matches a row in the inline-vs-delegated
   table in `monozukuri-core/references/orchestration.md` — an independent
   investigation, an independently verifiable implementation step, parallel
   disjoint work, or independent review on high/critical risk. Never delegate
   integration or the final call.
7. **Plan checkpoints.** When the work splits into more than one unit, size
   each unit and order them smallest first within dependency order, each
   ending at a verified checkpoint, per
   `monozukuri-core/references/checkpoints.md`. Skip for single-unit work.
8. **Emit the plan header** (see Output).

## Output

```text
Task: <one line>
Mode: <execute|sensei>
Context: <type> [+security] [+performance]      Risk: <tier> → <human gate>
Monozukuri sequence:
  <skill> → <skill> → [<injected step>] → <skill [subagent: role]> ...
DoD: <n> items (<playbook> [+modifiers], <tier>) — see monozukuri-core/references/definition-of-done.md
Change budget: declare expected file scope before CHANGE (see change-budget.md)
Checkpoints: <n> units, smallest first (multi-unit work only — see checkpoints.md)
```

`[subagent: role]` marks a step delegated per
`monozukuri-core/references/orchestration.md`; an unmarked step runs inline.

Worked example:

```text
Task: add OAuth login
Mode: execute
Context: feature +security      Risk: high → architecture-approval gate
Monozukuri sequence:
  nemawashi → genchi-genbutsu → kanso → [threat-model]
  → poka-yoke (+security test cases) → kata [subagent: implementer]
  → kodawari (+security review) [subagent: reviewer] → andon (+security observability)
  → shukka (+security verification) → hansei
DoD: 11 items (feature + security, high) — see monozukuri-core/references/definition-of-done.md
Change budget: declare expected file scope before CHANGE (see change-budget.md)
```

```text
Task: build a new invoicing service from scratch
Mode: execute
Context: greenfield      Risk: high → architecture-approval gate
Monozukuri sequence:
  nemawashi → monozukuri-blueprint (4 gated stages)
  → per phase: kanso → kata → poka-yoke → kodawari → andon → shukka → hansei
DoD: 8 items (greenfield, high) — see monozukuri-core/references/definition-of-done.md
```

## Handoff

After the header, proceed through the composed sequence using each named
skill in order. `monozukuri-core` remains the umbrella contract
(DISCOVER/CHANGE/PROVE) that governs the whole task.

If a referenced skill is not installed, apply its named lens inline instead of
trying to invoke it.
