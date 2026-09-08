---
name: paper-policy
description: Resolve, validate, and audit hard and soft constraints for academic manuscripts and paper artifacts. Use when Codex needs to determine active paper rules from manuscript state, paper type, venue, submission stage, or workflow mode; lint a LaTeX paper project; assess submission readiness; create or update a paper policy profile; explain why a rule is active; or validate the paper-policy registries. Do not use as the primary skill for prose drafting, peer review, rebuttal writing, citation discovery, or figure/table creation.
---

# Paper Policy

Use this skill as the shared policy kernel for `paper-writing`, `paper-review`, and `paper-figures-tables`. Keep evidence management in the user-selected evidence workflow and keep artifact production in the owning skill.

## Authority

Read `references/authority-model.md` before resolving conflicts. Core integrity rules outrank style preferences. Reliable venue or template requirements may override house style, but they cannot authorize fabrication or unsupported claims.

## Constraint Model

Read `references/constraint-schema.md` when editing registries, profiles, statuses, or waiver behavior.

Keep these axes independent:

```text
force: hard | soft
check: deterministic | semantic | manual
```

Conditional rules remain `force: hard`; express conditionality through `activation` or a profile. Never use `P` as a third force value.

Hard outcomes are `PASS`, `FAIL`, `UNVERIFIED`, `NOT_APPLICABLE`, or `WAIVED`. A semantic or manual hard rule without evidence is `UNVERIFIED`, never `PASS`.

Soft outcomes are `APPLIED`, `ADAPTED`, or `SKIPPED`. Adapt soft rules from the manuscript state without silently crossing a hard boundary.

## Workflow

1. Establish context from user instructions, manuscript/template files, and then cautious inference.
2. Load `references/policy-sets.yaml`, `references/hard-rules.yaml`, `references/soft-rules.yaml`, and `references/profiles.yaml` as needed.
3. Use the public default policy sets unless the context explicitly opts into another set. `strict-house-style` is disabled by default; once enabled, its hard rules remain hard.
4. Activate profiles only from reliable context. Inference may change soft choices, but it must not silently activate venue, anonymity, submission, or optional house hard rules.
5. Apply hard rules before soft guidance.
6. Resolve a context file before writing or audit work:

```bash
python3 scripts/resolve_policy.py /path/to/paper_context.yaml
```

7. Run deterministic checks when a manuscript project is available:

```bash
python3 scripts/validate_registry.py
python3 scripts/lint_project.py /path/to/paper
```

The standalone linter uses public defaults. Add `--strict-house-style` only for
an explicitly opted-in strict project; prefer `run_project_validation.py` when
a context file is available so the exact resolved hard-rule set is used.

8. For evidence-backed compliance and final-stage readiness, read
   `references/compliance-schema.md` and run:

```bash
python3 scripts/assess_compliance.py /path/to/paper_context.yaml \
  --project /path/to/paper --evidence /path/to/compliance-evidence.yaml
```

For the first pass on a supplied manuscript copy, use the project-local runner:

```bash
python3 scripts/run_project_validation.py /path/to/paper_context.yaml \
  /path/to/paper --output-dir /path/to/validation-output
```

It produces an evidence worklist, not fabricated compliance evidence.
When a project contains more than one document root or duplicate submission
copies, set `primary_tex` and optional `additional_tex` in context. Never merge
all `.tex`/`.bib` files recursively: the runner follows only selected include
trees and their referenced bibliographies and records the boundary in its
manifest.
It also writes a guarded `artifact-manifest-skeleton.yaml`; auto-discovered
records remain unusable as evidence until a reviewer changes
`discovery_status` from `needs_confirmation` to `confirmed` after checking the
record. A full-paper run may set
`artifact_mode: [final_figure, final_table]` to compose both final profiles.
Inspect `soft-review-worklist.yaml` to review adaptive rules by actual section
and artifact rather than as one flat ID list. Treat it as a plan, not evidence.
Use locator-rich `unused-bibtex-keys.yaml` entries for cleanup decisions without
automatic deletion.

9. Keep semantic/manual hard rules `UNVERIFIED` until admissible evidence exists.
   An agent may record only an anchored semantic/manual FAIL; it cannot clear a
   semantic rule with PASS. PASS requires human, user, or venue evidence.
10. Report failures separately from soft recommendations. Do not claim that registry validation proves manuscript compliance.

## Context Resolution

For full-paper, multi-section, polish, submission, rebuttal, or camera-ready work, consume or create a small `paper_context.yaml` with:

- `paper_type`
- `policy_sets`; omit it for `[integrity-core, academic-defaults]`, or use
  `[strict-house-style]` to opt into the strict set and its dependencies
- `domain`
- `venue`
- `submission_stage`
- `language`
- `double_blind`
- `page_pressure`
- `evidence_maturity`
- `manuscript_state`
- `reader_risk`
- `measurement_bias_status` when a systematic measurement or extraction error is characterized
- `evidence_structure` when evidence sources have distinct substantive, validation, calibration, control, case-study, or exploratory roles
- `table_profile: layered_capability_matrix` when an explicitly selected wide Related Work matrix has semantic column layers
- approved citation sources
- venue source and `as_of` date
- `scopes` and generic `artifacts` for applicability
- `features` for semantic selectors such as `conclusion`, `data_figure`, or
  `limitations_content`
- add `generated_conceptual_figure` alongside `conceptual_figure` when the final
  conceptual artifact is produced by a generative image model

Read `references/context-schema.md` for the complete mapping and provenance rules.
Do not require a persistent context file for a short paragraph rewrite.

Add `threats_to_validity` or `limitations_content` to the context `features`
whenever the requested scope contains load-bearing threat or
limitation analysis. These selectors activate semantic hard checks; they do not
claim that the manuscript passes them.

## Output Contract

For policy resolution or audit, return:

1. Resolved context, active policy sets, informational policy-set notes, and any `UNVERIFIED` fields.
2. Active hard rules with status and evidence/check locator.
3. Active soft rules with `APPLIED`, `ADAPTED`, or `SKIPPED` status.
4. Blocking failures, unresolved hard rules, and authorized waivers.
5. The next owning skill: writing, review, figures/tables, the selected evidence workflow, or citation audit.

Do not rewrite manuscript prose unless the user separately invokes `paper-writing`. Do not automatically edit `.bib` files or apply semantic prose fixes.

## Resources

- `references/authority-model.md`: precedence, waiver, and conflict resolution.
- `references/constraint-schema.md`: registry and profile field contract.
- `references/context-schema.md`: paper context, provenance, and resolution semantics.
- `references/compliance-schema.md`: evidence records, status precedence, waivers, and readiness.
- `references/paper-context.example.yaml`: example context for complex work.
- `references/policy-sets.yaml`: public defaults, optional strict house rules, dependencies, and rule membership.
- `references/hard-rules.yaml`: normalized mandatory rules.
- `references/soft-rules.yaml`: context-sensitive defaults and variants.
- `references/profiles.yaml`: stage, paper-type, artifact, and mode activations.
- `references/decision-baseline.yaml`: machine-readable snapshot of the approved manual decisions.
- `scripts/validate_registry.py`: structural registry validation.
- `scripts/resolve_policy.py`: deterministic activation and soft-selection resolver.
- `scripts/assess_compliance.py`: evidence-backed hard/soft assessment and readiness aggregation.
- `scripts/check_artifacts.py`: artifact-manifest path, format, source-data, final-width coverage, and canonical table-marker checks.
- `scripts/discover_artifacts.py`: guarded LaTeX figure/table discovery and
  evidence-manifest skeleton generation.
- `scripts/build_soft_worklist.py`: primary-section discovery and complete
  section/artifact grouping for active soft rules.
- `scripts/project_files.py`: authoritative main/additional TeX include-tree and
  referenced-bibliography selection.
- `scripts/lint_project.py`: deterministic manuscript checks only.
- `scripts/run_project_validation.py`: project-local resolution, lint,
  assessment, artifact discovery, explicit count summary, locator-rich
  unused-key report, and hard/soft worklist generation.
- `scripts/test_validate_registry.py`: validator fixture tests.
