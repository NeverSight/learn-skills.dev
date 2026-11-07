---
name: team-design
description: 'Use for drafting technical designs with independent review.'
effort: medium
argument-hint: "[docs/plans/<id>/]"
---

Before this operation, read [artifact schema](../team/references/artifacts.md).
Before each consuming step, read its linked shared rules. Resolve links from this installed `SKILL.md` directory.
If a required read fails, stop that step and report its resolved path. Never use checkout fallback or recursive loading.

Before each dispatch or retry, read [host dispatch](../team/references/15-host-dispatch.md) and supply its resolved installed paths.

Before review dispatch, supply the installed plugin root, the resolved `skills/team/references/design-reviewer.md` path, the absolute installed `skills/team/` directory as the base of that brief's links, and the resolved paths of the manuals its `## Review brief` links, all in `skills/team/references/`: `code-reviewer.md`, `code-standards.md`, `design-template.md`, `decisions.md`, `findings.md`, `writing.md`, and `cross-model-review.md` when the prompt carries `## External review input`. Require reads before work.

# Team Design

Before finalizing prose you author, read the [writing standards](../team/references/writing.md). Relay completed review reports unchanged.

No mid-run prompt fires.

## Input

`$ARGUMENTS` is the artifact directory `docs/plans/<id>/`; if empty, the
discovery command resolves it. Resolve `<team-skill-dir>` to the absolute directory containing
`skills/team/SKILL.md`. From the repository root, run:

```sh
"<team-skill-dir>/discover-topic.sh" "${ARGUMENTS:-}" "5-research.md"
```

- **Printed a path:** use it as `$ARGUMENTS`; announce it when no explicit
  arg was given.
- **Printed nothing:** do not hard-error. Fire `AskUserQuestion` with a
  `Setup` header and labeled options:
  - **Run the producer** — run `/team-research docs/plans/<id>/` to produce
    `5-research.md`.
  - **Give a path** — the user supplies the `docs/plans/<id>/` directory.

## Execution

1. Use the directory resolved in `## Input`.
2. If `$ARGUMENTS/6-design.md` already exists, skip to step 3 — never re-draft
   an existing design ([durable state rules](../team/principles/durable-state.md)).
   Otherwise dispatch `design-author`; it writes `$ARGUMENTS/6-design.md`
   with frontmatter `revision: 0`.
3. **Design review gate.** Run
   `"<team-skill-dir>/scripts/design-review-status.sh" "$ARGUMENTS"`.
   Exit 0 (`passed`): skip to step 4 — never re-review a passed design.
   Exit 1 (`pending`): its second field `<n>` is this round's number.
   Exit 2: stop and report its stderr.

   Each round:

   a. **Cross-model pass.** Read the
      [cross-model review](../team/references/cross-model-review.md) and run
      its `## Design-review pass` (gate: `TEAM_DISABLE_CROSS_MODEL`). Any
      skip continues with the reviewer alone; the pass never blocks the gate.
   b. **Review.** Read the `## Review brief` from the
      [design reviewer brief](../team/references/design-reviewer.md),
      substitute the artifact directory, attach the paths named at the top of
      this file, and give it to a read-only `Explore` subagent in a
      [fresh context window](../team/references/step-delegation.md#fresh-context).
   c. **Record.** Write the reviewer's report verbatim to a scratch file
      outside `$ARGUMENTS` with the Write tool, then run
      `node "<team-skill-dir>/scripts/record-design-review.mjs" --dir "$ARGUMENTS" --report <report-file>`.
      Its JSON line names the `round` and `verdict`. Exit 3 is an
      unparseable verdict (below); any other non-zero exit halts loudly with
      its stderr.
   d. **Act on the verdict:**
      - **APPROVE or COMMENT** — the review passes. Advance.
      - **REQUEST CHANGES** — re-dispatch `design-author` with the reviewer's
        findings verbatim; it re-drafts and increments `revision: <n+1>`, then
        a fresh round runs. No round cap; the loop ends on the verdict.
      - **Unparseable verdict or reviewer crash** — retry the review once with
        the error; on second failure, halt loudly. Fail closed — never advance
        on a missing verdict ([verified results rules](../team/principles/verified-results.md)).
4. **Stop once `$ARGUMENTS/6-design.md` exists and
   `design-review-status.sh` exits 0.**

Report design path and tell the user:
**"Next: run `/team-structure docs/plans/<id>/`"**
