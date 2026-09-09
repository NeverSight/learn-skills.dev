---
name: grill-code
description: >
  One-shot code workflow: grill the design, document the domain, force the
  laziest refactoring. Use on "grill-code", "grill the code", "code grill",
  "challenge and refactor this", "review and simplify".
disable-model-invocation: true
argument-hint: "[target: file, module, diff, or design]"
---

# Grill Code

Load these four member skills with the Skill tool, once each, in order;
carry each skill's instructions forward.

## Steps

1. `ponytail` — what may exist. Out: the ladder ruling per piece, cited by
   rung number (1 need to exist / 2 reuse / 3 stdlib / 4 native / 5 installed
   dep / 6 one line / 7 minimum code).
2. `refactoring-coding-standard` — smells to refactorings. Out: one ordered
   refactor path, each step with its verification, plus what you excluded.
3. `grilling` — grill the design. Out: one round of numbered questions, each
   with a recommended answer; the round covers every axis the target has —
   need-to-exist, failure and atomicity, ordering, scale and backpressure,
   rollback — and names any axis it skipped.
4. `domain-modeling` — the docs the answers settle. Out: the CONTEXT.md / ADR
   writes, or "none" plus the one-line reason nothing was writable yet.

Pass the user's arguments through (`/grill-code <target>` → the same target);
ponytail also takes `lite|full|ultra`.

## Output

In this order, no prose between sections:

```
## 1. Grill verdict   — one ruling per piece: delete or keep
## 2. Design questions — Q1..Qn, each with "➡️ <recommended answer>"
## 3. Docs            — files written (CONTEXT.md / ADR path), or "none"
## 4. Refactor plan   — ordered steps: smell → therapy → verification
## 5. Code            — the lazy version, smallest diff
```

For example:

```
| src/pay.js:10-12 dead comment | delete | rung 1: no git here, the "rollback" it protects does not exist |
1. 同体分支 → 合并条件表达式 ch10 → `npm test` 5/5
```

Headings exactly as above; body in the user's language. Section 1 rows cite
`file:line` and the rung; section 4 steps end with the exact command that
proves them (`npm test`, not "tests pass"). Sections 1-4 are bullets and
tables, never paragraphs. Section 5 is the only place with code, code before
its three lines of explanation. "just build it": skip section 2, state
"interview skipped", still emit 1, 4, 5.

## Landing gate

First matching row wins; section 4 says so when section 5 is a paste.

| Situation | Section 5 |
|---|---|
| no code in the target (design doc, prose, config, or a question) | no implementation: at most a ≤10-line patch to the target's own text, or one line saying no change is needed |
| public API, multi-file, or wide scope | paste the plan until the user confirms the summary |
| no test covers the target | paste and name the missing test; the user asked to change the code anyway → write that test first, then land |
| section 2 answered, or the user said "just build it" — one file, no public-API change | write |
| otherwise (section 2 unanswered) | paste; the questions are the deliverable |

Section 3's docs writes (CONTEXT.md, docs/adr/*.md) are step 4's deliverable,
not code: this gate governs section 5 only.

No git and no backup outside the repo → the paste is the rollback; say so.

## If X fails → do Y

| Trigger | First fix | Still stuck |
|---|---|---|
| no argument | exactly one candidate in the workspace → name it in section 1 and say you assumed it; two or more → list them and ask | ask for the path or the pasted source; never invent a target |
| the target is not in the workspace | say which paths you searched | ask for the path or the pasted source |
| the target is pasted (diff, design, snippet), not on disk | work from the paste; cite it as `paste:<line>` | ask for the path only if a ruling needs code the paste does not show |
| a member skill will not load | run that step from its contract, one line, marked `(not loaded)` | name the step that is missing; never skip it silently |
| a wrapper (`grill-code`, `grill-with-docs`, `grill-me`) refused | user-only: load `grilling` then `domain-modeling`; never ask for a slash command | — |
| a comment says "do not delete", the user says delete | user ruling wins; one line | no git repo → say so; the ruling rests on the tests and the plan, not on history |
| no test covers the target | landing gate: paste section 5, name the missing test | the user asked for the change → write that test first, then land; never land untested code |

## Conflicts

User ruling wins. Otherwise: ponytail (what should exist) →
grilling/domain-modeling (what the design should be) → refactoring (how to get
there). Name the conflict and the ruling, one line each. Never re-ask what the
user answered or re-interview what the code settles.

## Checkpoints

- 🔴 Code lands only through the landing gate; plan and paste until then.
- 🛑 One round, then stop: show ruling, plan and verification, then wait. Do
  not start round two on your own.

## Do not

- Do not call the wrappers with the Skill tool — user-only, refused.
- Do not invent a target: with no candidate in the workspace, no refactor.
- Do not edit code outside the landing gate; section 3's docs writes are the one
  exception.
- Do not silently drop a step: one line naming the reason.
- Do not pad the sections with prose or a skills tour.
- Do not open chapters while the cheatsheet can decide the smell.
- Do not offer the full version of a thing the user did not ask for.
