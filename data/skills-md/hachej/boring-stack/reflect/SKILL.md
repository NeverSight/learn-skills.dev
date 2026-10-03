---
name: reflect
description: "Turn what this session learned into durable changes to the repository: a lint rule, a test, a check, a skill edit, AGENTS.md or docs/DECISIONS.md. Use when wrapping up a task, after a mistake or a correction, or when the person says reflect or remember this."
---

# Reflect

Adapted from Poteto's brainmaxxing `reflect` (MIT, see THIRD_PARTY.md). This
repository has no separate memory vault: what the next agent must know lives in
the repository itself, where it is reviewed like code.

## Process

1. Scan the session for:
   - mistakes made and corrections received;
   - the product owner's preferences (how they want the app to behave or read);
   - codebase knowledge gained (gotchas, why something is the way it is);
   - library or tool quirks (`vendor/boring/`, Flue, the model provider);
   - friction in a skill (verify-app, new-agent) or in the verify CLI;
   - repeated manual steps.
2. Skip anything trivial or already written down (grep AGENTS.md, docs/, the skills).
3. Route each learning (below), smallest durable form first.
4. Put the changes in the current branch, or a new one, and say what you changed.

## Routing, in this order

1. **Structure** (principle-encode-lessons-in-structure): can it be a lint rule
   (`.oxlintrc.json`), an architecture rule (`scripts/verify/ARCHITECTURE.json`), a unit test, a
   `verify check` step, a validator in an agent's `index.mjs`, a law with its
   evidence (`docs/INVARIANTS.md` + `scripts/verify/VERIFY.json`) or a model (`formal/`)? Then
   encode it there and write no prose. **A mistake an agent repeats becomes a
   rule in `scripts/verify/ARCHITECTURE.json`**, with the law or decision it enforces, a fix
   hint, and a fixture in `test/unit/architecture.test.mjs` proving it fires;
   better still, make the mistake impossible (a type, a single helper, a
   constraint) so no rule is needed.
2. **A skill** (a pull request on hachej/boring-stack, `skills/<skill>/SKILL.md`): the learning is about how a
   skill's procedure works: fix the procedure.
3. **The feature map** (`docs/verify/<area>.md`): a gotcha about driving a feature.
4. **docs/DECISIONS.md**: a decision and its reason ("we do X because Y; not Z because W").
5. **AGENTS.md**: a rule every agent needs on every task. Keep it short: move detail to a skill.
6. **Upstream**: a gap in `@boring/agent`, `@boring/files` or `@boring/chat` goes to
   hachej/boring-ui-v3 as an issue or a pull request, never as an edit of `vendor/`.
7. **The template** (hachej/boring-app): a lesson every new app needs. Say so,
   so it lands in the template; existing apps take it by a normal pull request.

## Summary

```
## Reflect summary
- Structural: [rules, tests, checks added]
- Skills: [skill files changed, one line each]
- Docs: [DECISIONS / AGENTS / feature map entries]
- Upstream or template: [issues or PRs to open]
```
