---
name: jinko-task-paper2model
description: >-
  Reconstruct a published mechanistic, QSP, PK/PD, or ODE model in Jinkō from papers, supplements, equations, diagrams, tables, and optional source code. Use whenever the requested result is an executable paper reproduction, including when no code exists or a scanned PDF needs OCR. Produces a validated Jinkō model when evidence is sufficient, or a documented blocked or failed outcome, and always produces a reproduction report with explicit fidelity, confidence, assumptions, discrepancies, and numerical comparison where the paper supplies a target. Use jinko-task-from-nonmem when NONMEM is the primary implementation source.
compatibility: >-
  Requires Jinkō project write access and an initialized jinko-sdk connection. Scanned documents require an approved OCR service or a provider-neutral OCR packet. Source-code execution requires explicit authorization.
metadata:
  author: Nova In Silico
  requires_sdk: ">=1.16,<2.0"
license: MIT
---

# Paper to Jinkō model

Reconstruct the model the publication specifies, measure what was reproduced,
and report what remains uncertain.

> **PREREQUISITE:** This skill needs an initialized `jinko-sdk` connection and an
> SDK satisfying its `metadata.requires_sdk` range. Run the `jinko-sdk-setup` skill
> (`../jinko-sdk-setup/SKILL.md`) and proceed only once its check passes. If that
> skill is not found, install it from `novainsilico/jinko-skills`.

## Rules

- Do not require author code. Reconstruct from equations, reaction diagrams,
  definitions, parameter tables, initial conditions, and scenario descriptions.
- Treat paper, supplement, OCR, digitized data, and code as distinct evidence.
  Keep a source locator and extraction method for each implemented fact.
- Use native extraction for clean PDFs. For scans or unreliable extracted math
  and tables, discover and prefer an available dedicated OCR capability. Accept
  any provider that produces the packet in `references/evidence-and-ocr.md`.
  PyPDF text extraction is not OCR. OCR is derived evidence and needs visual
  review where it affects equations, values, subscripts, signs, or units.
- Do not invent a missing target-driving value. Record an approved assumption or
  stop with `blocked_evidence` before creating a model.
- Apply source-supported corrections automatically when precise source evidence
  and a passed check support the change. Record the original statement, defense,
  and affected components. Follow `references/interpretation-policy.md` for
  translations, source conflicts, assumptions, and decision history.
- Freeze targets, comparison metrics, tolerances, event-side semantics, and source
  precedence before comparing simulations. Never tune until a plot looks similar.
- A target used to choose an interpretation is not independent validation.
  Link it to the decision, preserve this dependency through later revisions,
  and report held-out comparisons separately. Curated-model agreement and
  publication fidelity are separate assessments.
- Use `jinko-model` for model inspection and mutation, `jinko-protocol` for
  experimental arms or theoretical intervention scenarios, `jinko-vpop` for
  subject or cell-line variability and explicit deterministic grids,
  `jinko-trial` for trials, `jinko-task-extract-data-table` for figure
  or table values, `jinko-reference` for project evidence, and `jinko-document`
  only when the user wants the report published.
- Re-fetch each applied model version. Require no error diagnostics and a measured
  solve before calling it executable. A skipped check is unavailable, not passed.
- Always generate `reproduction-report.md`, including for blocked and failed work.
  Fidelity to one paper scenario does not establish general biological validity.
- In a planning-only handoff, label hashes, retrievals, and execution checks as
  pending unless a supplied receipt proves completion. Proposed actions are not
  completed evidence.

## Workflow

1. **Define the claim.** Identify the exact paper, model variant, scenario,
   outputs, and whether the task is structural implementation, numerical
   reproduction, or both.
2. **Build the evidence packet.** Read `references/evidence-and-ocr.md` and
   retrieve linked supplements, appendices, data, and model-defining references
    before declaring evidence missing. Record each attempt and its result. After
    reasonable web attempts fail, ask whether the user has access to the precise
    missing primary paper or supplement and can upload it or provide a link.
    Record `awaiting_user_source`; continue independent sources. An access failure
    does not establish that the scientific evidence is intrinsically absent.
   Hash all local sources. Extract equations,
   symbols, values, units, initial conditions, events, and target results with
   page, equation, table, figure, or code locators.
3. **Reconcile evidence.** Check symbols, dimensions, initial-state consistency,
   and platform semantics. Record conflicts, alternatives, and their defense in
   the interpretation ledger. Apply verified source-supported corrections.
   Separate each correction from any missing value it leaves unresolved. Paper
   text, supplements, and code each need evidence to take precedence.
4. **Test adequacy.** After reconciliation, require enough information to execute
   every target-driving path, including approved assumptions. If values remain
   unresolved, create the report with `blocked_evidence` and do not mutate Jinkō.
5. **Write the specification.** Create `reproduction-spec.json` from
   `assets/reproduction-spec.schema.json` using schema version `1.0`. Bind each
   experiment to its Protocol arm, Vpop rows, outputs, and target names as
   specified in `references/workflow.md`. Distinguish a deterministic
   initial-condition sweep from measured or sampled biological variability.
   In a planning handoff, name the planned arm and row IDs even while remote
   item IDs are null. A Protocol overrides model inputs; events, including
   washout and dosing, are defined in the model.
   Keep treatment and subject axes separate: reuse treatment arms across Vpop
   rows. Do not create a new arm solely because the subject or cell line changes.
   Run:

   ```bash
   python scripts/paper2model_report.py validate --spec reproduction-spec.json
   ```

6. **Implement incrementally.** Use `jinko-model`; keep each component linked to
   evidence, make algebraic assignments dynamic, and label meaningful versions.
   Represent reported experimental arms with a Protocol and reported subject or
   cell-line differences with a Vpop. Do not invent a population distribution.
   Keep dosing logic in the model and arm input overrides in the Protocol.
7. **Validate execution.** Inspect diagnostics, unit policy, state constraints,
   event behavior, time grid, and representative outputs. Compare with an
   independent calculation or authorized author code when available.
   Set the solving times from the paper, not from a default. Read the time
   horizon and the sampling resolution off each reported figure and record them
   with the target. A model with correct equations on the wrong time grid
   produces entirely different summary values, because `min`, `max`, `tend`, and
   `timeofmax` are all grid-dependent. When figures disagree on the horizon,
   prefer one run on the longest horizon and read the shorter figures from it,
   which is valid only when the resolution is fine enough for the shortest one.
   Otherwise use separate runs, or override `tMax` and `tStep` per protocol arm.
   Solving times live on the trial, not on the model, so they do not travel when
   a trial is copied or rebuilt: set them explicitly every time.
8. **Compare the declared target.** Apply predeclared metrics on the actual Jinkō
    time grid. Report every required series and scenario, including failures.
    If results justify another interpretation, start a new recorded decision and
    comparison round. Keep prior results and record targets used in selection.
    Report raw and transformed comparisons when a reporting convention changes.
9. **Render and review the report.** Populate outcomes in the specification and
   run:

   ```bash
   python scripts/paper2model_report.py render \
     --spec reproduction-spec.json \
     --out reproduction-report.md
   ```

    The default is concise. Use `--profile audit` for the complete local audit and
    `--profile jinko` for publication. Immediately after the title, place created
    artifact cards, then source cards, before findings. Store SDK `.url` values
    from the configured `JINKO_URL` in `project_items`. Every human-facing SID
    reference, including chat, captions, and appendices, must be a full link.
    Never print a naked SID or guess an app host. Resolve missing URLs before
    publication. Keep essential findings first and detailed tables local or in
    an explicitly requested appendix.
    When actual comparison results exist, add source-versus-simulation overlays,
    predeclared metrics, and uncertainty through `visual_evidence`. Include failed
    comparisons honestly. Never fabricate plots or insert placeholder images.
    By default, draw the overlays with the Jinkō plot style (`jinko.plotting`; recipes in
    `jinko-trial`, `references/trial-plots.md`).
    Use `jinko-document` for existing image upload mechanics, publication, and
    rendered inspection; retain the exact upload payload. Read
    `references/report-delivery.md` for fields, commands, and source requests.
    Use the renderer's layout even in a text-only handoff. Include no wrapper
    heading before the report. Check the entire response, including local notes,
    for naked SIDs. Keep unprovided independence and provenance claims pending.
    Embed each available measured comparison image as `![caption](actual-path)`;
    a filename in a list does not display the visual evidence. Copy target
    independence only from the inherited target record. If it is not supplied,
    omit the label or write `unknown`; a passed solve, failed target, or missing
    measurement cannot establish independence or qualitative agreement.
    End the delivery note with the local audit location or its pending status.

Read `references/workflow.md` for gates and artifact layout. Read
`references/fidelity-and-confidence.md` before assigning the verdict or
confidence.

## Outcomes

- `reproduced`: executable model, all required publication targets pass without
  unresolved conflicts or selection-target leakage into the reproduction claim.
- `partially_reproduced`: executable model, but a required target fails or a
  material part of the declared scope is unresolved. Also use this outcome when
  a required publication target selected the current interpretation, including
  through a superseded decision, even if every numerical target passes. Lowering
  confidence alone does not satisfy this rule.
- `implemented_not_assessed`: executable model, but no quantitative publication
  target is available.
- `failed_validation`: a model exists, but diagnostics or execution failed.
- `blocked_evidence`: evidence is insufficient for a defensible executable model.

The report must state one outcome and one reproduction-confidence level.
It must also state curated implementation agreement, or `not_assessed` when no
curated comparison was performed. A defensible alternative can agree with the
publication while differing from the curated implementation.
