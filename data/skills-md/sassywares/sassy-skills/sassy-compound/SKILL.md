---
name: sassy-compound
description: >-
  Document a solved problem as a durable repo learning. Use after a bug is fixed,
  a problem is solved, or a fresh finding is made. Writes the learning, and also
  maintains the project's concepts file and a pointer in AGENTS.md when useful.
  Lean on purpose.
argument-hint: "[optional context] [mode:manual|auto]"
disable-model-invocation: true
---

# Sassy Compound

**Outcome:** one durable learning written for a solved problem, the concepts file updated if new terms were learned, and `AGENTS.md` pointed at the knowledge store when that pointer is missing and useful.

**Modes.** Default `mode:manual` asks before the `AGENTS.md` pointer edit; `mode:auto` applies that edit silently. Ship passes `mode:auto` after its own gate. Never toggle it yourself.

**Config.** Resolve `.sassywares/config.yaml` (nearest, walking up) per the `sassy-setup` skill's `references/config.md`. Precedence: explicit token > session instruction > config > skill default. Paths come from `artifacts.solutions` and `artifacts.concepts`; never hardcode them.

## When it qualifies — the durable bar

A learning earns a doc only when it holds reasoning that is **not recoverable** from the final code, tests, types, comments, or existing docs, and losing it would plausibly cause a repeat mistake or substantial rediscovery.

Apply the counterfactual: *if this learning disappeared, would a future engineer reading the final implementation still likely repeat the mistake or redo the investigation?* If no, write nothing and say why. Completion, effort, and diff size do not qualify a learning.

## One learning per run

If several problems were solved, run once per learning. Never batch them into one doc.

## Where things go (repo root)

| Artifact | Path |
|----------|------|
| Learning | `<artifacts.solutions>/<category>/<slug>.md` |
| Vocabulary | `<artifacts.concepts>` |
| Discoverability pointer | `AGENTS.md` (edit only; never create) |

`knowledge.write: false` means this project takes no learnings: say so and write nothing.

## Workflow

1. **Identify the learning.** Extract the problem and the verified solution from the conversation. Ground every behavior claim against the code (read the defining line) or soften/attribute it. Redact secrets.
2. **Classify.** Bug track (a defect fixed) or knowledge track (a durable insight or pattern). Pick a `category` and a descriptive `slug`. If the exact path exists and covers the same problem, update it (refresh `updated:`); otherwise create it.
3. **Write the doc.** Read `references/templates.md` now and use the matching template.
4. **Concepts.** If the learning surfaced a term a new engineer would need defined, read `references/concepts.md` now and follow its rules to add or refine it in the configured concepts file. Create the file if absent. Skip cleanly when nothing qualifies.
5. **AGENTS.md pointer.** If a project instruction file exists (`AGENTS.md` or `CLAUDE.md`) and does not already mention the configured solutions path or concepts file, add one short line pointing at them. Edit only; never create the file. With `mode:auto`, do it silently; with `mode:manual` (default), ask.
6. **Report.** Path, create vs update, concepts touched, and whether an AGENTS.md pointer was added.

## Hard rules

| Rule | Requirement |
|------|-------------|
| Solved and verified only | Never document an unsolved or unverified problem. |
| One learning per run | Sequential runs, never a batch. |
| Grounded | Every claim checked against the tree, or softened. |
| Write boundary | Only the configured solutions path, the configured concepts file, and a one-line `AGENTS.md` edit. Never touch code. |
