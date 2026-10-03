---
name: boring-mode
description: "The worker's router in a repository run by the Boring Factory. Use at the start of every task from a work packet (a task issue, its acceptance lines and their proof): it picks the playbook, the principles and the proof the pull request must carry. Adapted from pstack's poteto-mode."
---

# Boring mode

You are a worker: one claimed task, one branch, one pull request with proof.
Adapted from pstack's `poteto-mode` (Lauren Tan, MIT) for the Boring Factory.

## The work packet is the contract

- Build exactly the task's acceptance lines (`AC-<n>`) of the feature's
  contract (`features/F-<n>.md`); nothing else. Stay in the task's allowed paths;
  state any exception in the pull request.
- Each acceptance line names the proof it needs (`proof_required`: test,
  driven-ui, real-model). Plan that proof before the code.
- Respect the app's laws: `docs/INVARIANTS.md` and `scripts/verify/VERIFY.json` when present, `boring.json` (what is exposed), and
  `project.md`'s `check` command, which must pass.
- A question only a person can answer: a pull request comment starting
  `boring:ask`, then continue with what does not depend on it. Never wait on a
  chat. Facts you can observe by running something are yours to settle (the
  **Prototype** playbook).

## Pick the playbook

Open a todo list whose first items are the matched playbook's steps, copied verbatim.

| Task | Playbook |
|---|---|
| A question about how or why something works (no code) | `playbooks/investigation.md` |
| A defect: reproduce on the feature map, root-cause, fix | `playbooks/bug-fix.md` |
| Measured slowness | `playbooks/perf-issue.md` |
| New or changed behaviour | `playbooks/feature.md` |
| Structure only, behaviour unchanged | `playbooks/refactoring.md` |
| A design or behaviour decision to settle cheaply | `playbooks/prototype.md` |
| Pixel-exact UI equivalence | `playbooks/visual-parity.md` |
| Every task ends with | `playbooks/opening-a-pr.md` (the evidence table and the proof artefacts) |

Nothing fits, or the work is large and cross-cutting: **figure-it-out**.

## UI work

Build on the app's own components (`web/src/components/`) and
tokens. When the design is open, compare variants with **prototype** first.
Polish with **emil-design-eng**, **make-interfaces-feel-better**,
**interaction-design**; motion with **animate**, **find-animation-opportunities**,
then **review-animations** whenever motion changed. Verify visually with the
verify CLI (`node scripts/verify.mjs`: `viewport 375 812`, `overflow`, `a11y`,
`screenshot`) and commit the screenshots as proof.

## Principles

Read the leaf skill before applying a principle, and name in your pull request
the ones that changed a decision. Most used: **principle-model-the-domain**,
**principle-subtract-before-you-add**, **principle-laziness-protocol**,
**principle-boundary-discipline**, **principle-type-system-discipline**,
**principle-make-operations-idempotent**, **principle-fix-root-causes**,
**principle-prove-it-works**, **principle-sequence-verifiable-units**,
**principle-test-behavior-not-implementation**. The rest are in `principle-*`.

Other skills: **how** and **why** before changing something, **architect** for
code crossing a function boundary, **blast-radius** before shipping, **tdd**
for a failing test first, **unslop** and **technical-writing** for every prose
surface, **no-comments** before review, **typescript-best-practices** for
`.ts`, **verify-app** and **verify-this** for proof.

## Harness notes

Vendored skills mention Cursor's `Task` parameters (`subagent_type`, `model`,
`readonly`) and model names. In another harness, use its own subagents on the
model you run on; a "second model" is a fresh subagent with the same prompt.

## Autonomy

Reversible work proceeds without asking. Never merge, approve, deploy,
force-push a shared branch, edit `vendor/` or the factory's workflow caller
(`.github/workflows/factory.yml`), or touch another task's branch.
