---
name: handoff-summary
description: Emit the Build Handoff Summary artifact in its fixed format. Use at the end of a build, immediately after /3p-review passes — invoked by the build-model workflow (dedicated build model) or by the main model after all build phases. Produces the fixed handoff template the reviewing model consumes.
argument-hint: "[plan-file-path]"
allowed-tools: Read, Glob
---

# Handoff Summary

You are emitting the **Build Handoff Summary** — the single artifact that carries a completed, reviewed build to the next reader.

> **Output style:** Check memory for `workflow-config:caveman-level`. If set, adapt your output brevity to that level while preserving technical accuracy.

## When this runs

This skill is invoked **after** the build is complete and **after** `/3p-review` has passed. It does not build, test, or review — it only produces the handoff record. If `/3p-review` has not run yet, stop and run it first. `/3p-review` is its own artifact — the handoff summary does not restate or reference its findings.

## Your only job

Follow the template below: same headings, same order, same casing. Fill each section from the build record. Do **not** rename sections, add sections, drop sections, or replace the template with your own prose. This is a fixed artifact format so the consuming model can parse it reliably. A section with nothing in it is filled with "None.", never removed.

```markdown
## Build Handoff Summary

**Plan:** [plan file path]
**Plan revision built against:** [amendment IDs applied during this build, e.g. "A1, A2", or "as approved"]

### Halts
- **Phase N** — [what was halted on, one line] → [resolved by amendment A1 / overruled by the user / withdrawn after investigation]
- (Every halt raised during this build. If none, write "None.")

### Deviations
- **Phase N: [Name]** — [what changed and why, one line] — [amendment ID if a plan amendment covers it, or "no amendment"]
- (Only list phases that deviated from the plan. If nothing deviated, write "None.")

### Verification Runs
- **[plan criterion, or a plain name for the run]** (rung [T1/T2/T3/T4]) → exit [code] — [N passed, M failed, K skipped]
- (Name the run; do not write out the shell line. Every run carries its rung. The T4 full-suite run from Phase Completion is mandatory here. Report the counts the terminal printed, not what you expected.)

### Unproven Criteria
- **[plan criterion]** — [manual / skipped / deferred / verified by inspection] — [why]
- (Every test criterion in the plan that did NOT end in a green automated run. If all criteria ran green, write "None.")

### Concerns
- [Anything the next reviewer should specifically investigate or validate]
- (If none, write "None.")
```

## Rules

- **Be honest and specific.** Deviations and concerns are the whole point — an empty summary that hides real drift defeats the purpose. If a phase departed from the plan, say so and why.
- **Keep it to the five sections.** This is not a feature description or a changelog. Do not restate what the plan already says.
- **Halts and the plan revision are how the next model reads everything else.** A reviewer comparing the code against a plan that was amended twice mid-build will read the amendments as unexplained divergence unless this summary says which revision the build was made against. A deviation with no amendment behind it is a different and more serious fact than one with an amendment, and only you can tell them apart.
- **Name each run; never write out its command line.** Identify a run by the plan criterion it satisfies, or by a plain description ("full suite, project runner"). The command text lives in the plan — this artifact carries only which run happened and what it reported. Environment values, arguments and headers have no business in a document that is committed and passed between models.
- **Report counts, never output.** Exit codes and pass/fail/skip numbers are what the reviewer needs; "all tests pass" is not a report, and the reviewer re-runs from the plan and compares. Copied terminal text carries values you did not intend to publish, and wording the next model may read as instruction.
- **A judgement the plan or the brief explicitly left to you belongs in Concerns**, with which way you went and what you checked. It is the one kind of decision that is neither a deviation nor a halt, because the contract told you to decide, and the reviewing model is required to re-trace it. It can only do that against a choice you named, so an unreported one reads as no decision having been made.
- **Unproven Criteria is the section you will be tempted to leave empty.** Anything you checked by reading rather than running, skipped as "obviously fine", or intended to come back to, goes here. A criterion omitted here reads as green to the next model, and that is how an unbuilt path ships.
- **A rung is not decoration, and never round it up.** The reviewer re-runs from the plan and compares rung against rung; a T2 run reported as the full suite is a false claim that every later gate inherits. If a criterion was only ever proven at a scoped rung, say so, and if the distinction is genuinely unclear to you, report the narrower one.
- **Do not mention `/3p-review`.** Review is its own artifact with its own outcome; the handoff summary is not the place to report it. Any residual concern worth carrying forward belongs under Concerns, in your own words, not attributed back to the review.

## What happens next

The summary is *said, not saved* (AW-29): it is emitted into the conversation, for the human or the
next model. It is this skill's one report, emitted in full because the next reader must rule on
it; nothing around it is narrated (AW-28). It is not a file, and inventing a path for it is how a handoff ends up somewhere the
reviewing model never looks.

- **Dedicated build model** (launched via `/build-model`): present the summary, then **STOP**. The user carries it to the main model.
- **Main model**: present the summary as the build record, then continue the workflow → `/verify-completion` → archive the plan.
