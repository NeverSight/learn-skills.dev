---
name: adk-agent-evaluation
description: >-
  Build, adapt or audit a Python ADK agent's test strategy: deterministic tool
  and Runner tests, live eval sets, simulated conversations, conformance
  replay, strict result checks and quote or citation support. Use for agent
  behaviour, regression coverage, eval reliability, fixing a failed stage
  without re-running paid earlier ones, holdout budgets, error analysis on a
  labelled dev set to fix wrong decisions, measuring each prompt, exemplar or
  model change, and subject-matter expert labelling: failure taxonomy,
  inter-rater agreement and judge calibration. Do not activate for non-agent
  unit tests, standalone model benchmarks, deployment or cleanup alone, prompt
  wording or exemplar design (adk-agent-instructions), model settings
  (adk-model-and-output-contracts), wiring eval gates into CI
  (adk-release-engineering), production telemetry (adk-agent-observability),
  adversarial suites (adk-agent-security) or presenting results
  (adk-presenter).
license: MIT
metadata:
  author: Ruslan Khissamiyev
  source-book: Agentic Engineering
  source-chapter: "7"
  last-tested: "2026-09-16"
  compatibility: See references/compatibility.md for exact tested versions and limits
  verified-against: "google-adk 2.8.0 companion run 2026-09-13; 2.12.0 offline spikes 2026-10-22 and 2026-10-25"
  version: "2026.10.28"
---

# ADK agent evaluation

Produce evidence about an agent's decisions, executed effects and final account of those effects. Adapt the target project; keep its business domain, architecture, dependency pins and test conventions. This skill works without the book or its companion repository.

## Inspect and define the job

1. Read repository instructions, manifests/lockfiles, test configuration and existing agent factories, tools, callbacks, session services and evaluation assets. Use the project's existing interpreter to inspect installed package metadata before importing application code. Imports and test collection can have side effects; inspect their entrypoints first. Check the pinned Python, `google-adk`, `google-genai` and any managed-evaluation SDK versions against [compatibility.md](references/compatibility.md). Preserve pins; a version mismatch requires interface verification or a clearly reported blocked live path, not an automatic dependency change.
2. Locate trusted identity, authorised mutations, idempotency keys, business-store lifetime, conversation-state lifetime and the model-injection seam. Read credential variable **names and presence**, never print secrets or dump `.env`. Identify existing offline/live markers and which commands could reach remote services. Finish inspection with a concise map of these boundaries and missing prerequisites.
3. Translate the user's requirement into observable success and forbidden actions: correct tool/arguments, allowed order, resulting effect, truthful response and bounded work. Distinguish deterministic assertions from model-dependent decisions. For an audit or recommendation, report each gap with its evidence and the concrete change that would close it, and leave implementation for a separate request. For implementation, present a short plan before broad changes and make the smallest coherent change.
4. Before model tuning or a quality cohort, pass an honest reference for each important outcome class through the actual response schema, validators and relevant Runner/served boundary. Include nondecisive issues, required controls and unresolved or contradictory evidence. A pass obtained by inventing associations or dropping obligations is not a solvable contract. Diagnose a failed reference first; [evaluation design](references/evaluation-design.md#establish-an-honest-review-contract) gives the checkpoint.

## Select the mode

Combine modes only when the requested outcome needs them. Read the linked reference when entering that mode, rather than loading every file.

| Request or evidence needed | Mode and resource | Completion criterion |
| --- | --- | --- |
| Enforce business rules, reproduce a bad decision, test callbacks/state or HTTP integration without model variance | [Deterministic tests](references/deterministic-tests.md) | Actual effects and state boundaries asserted through the relevant real runtime layer |
| Measure the real model, build fixed cases, add simulated dialogue or calibrate a judge | [Live evaluations](references/live-evaluations.md) | Version-valid assets and offline checks first; approved live work retains complete results and provenance |
| Record or compare provider exchanges after an integration change | [Conformance](references/conformance.md) | Reviewed baseline, nonzero executed case count, isolated tool effects and explicit replay limits |
| Grade an outcome that many call orders reach (a booking moved, a record updated), or a suite that passes one night and fails the next | [Evaluation design](references/evaluation-design.md#grade-the-end-state-not-the-path), then [Result auditing](references/result-auditing.md) for the reliability figure | Reference trajectory replayed on a fresh backend; whole fixture diffed and effective mutations compared; a [do-nothing control](references/evaluation-design.md#curate-cases-with-a-reason-to-exist) every action case fails; for live runs, repeated trials with an unbiased pass^k and NOT RUN on short cohorts (a deterministic scripted suite runs each case once) |
| No labels yet: subject-matter experts must decide what passes, or two experts' labels and a judge's need checking | [Expert review](references/expert-review.md) | One decision-maker named; failure taxonomy stopped at saturation; versioned criteria with older labels re-reviewed; gold set with provenance; kappa per criterion and adjudicated disagreements; judge TPR and TNR on a held-out split, or NOT REPORTED below the per-class minimum |
| Two judges disagree, or a judge must be checked against human labels | [Evaluation design](references/evaluation-design.md#calibrate-the-judge-on-fixed-evidence), "Calibrate the judge on fixed evidence" | Krippendorff's α at the rubric's level with the level recorded, false accepts and rejects at a stated threshold, an under-filled label set reported as incomplete |
| Run the agent under an external harness (Inspect, Promptfoo) without rewriting it | [Provider compatibility](references/provider-compatibility.md#run-the-same-agent-under-an-external-harness-proven-on-inspect) | The bridge or provider shape, its limits, and ADK's own evaluators kept as the primary evidence |
| Explain a misleading pass, check a CSV, design reliability/holdout gates | [Result auditing](references/result-auditing.md) | Expected coverage checked, failed/incomplete rows retained, conclusions limited to identifiable observations |

Planning a production suite can stop at a reviewable design with cases, budgets and acceptance criteria. Recommendations about holdouts, remote-write reconciliation or production telemetry are not claims those features exist or passed testing.

Load additional implementation detail only for the relevant branch:

- **Wrong decisions or answers, or measuring a prompt, exemplar, output-schema or model change:** [quality iteration](references/quality-iteration.md) runs the labelled-set, error-analysis, one-change loop and measures decision quality before further controls are added. The wording and exemplar design themselves are adk-agent-instructions' work; this loop measures them. Run and categorise errors before editing code; the first change targets the largest category among defects that change a downstream decision, ranked by cost when the brief prices each error type. For example, two outputs that miss an applicable policy and one condition that contradicts its own reason put retrieval first and a consistency check second. Whether a score change is beyond noise, and how many cases a holdout or CI set needs, is its [tell a change from noise](references/quality-iteration.md#tell-a-change-from-noise) section with [paired_difference.py](scripts/paired_difference.py); whether one version's rate is shown to meet a fixed target, such as an acceptance threshold, is its [score one version against a fixed target](references/quality-iteration.md#score-one-version-against-a-fixed-target) section, with the same helper.
- **Labels that do not exist yet, expert time to plan, or criteria that keep changing:** [expert review](references/expert-review.md) runs the session with the [session plan](assets/expert-session-plan.md) and [labelling guide](assets/labelling-guide.md), writes the [gold set](assets/gold-set-schema.md) and checks it with [label_agreement.py](scripts/label_agreement.py) (Cohen's kappa, disagreements to adjudicate, criteria drift, judge TPR and TNR). Read it before quality iteration when the development set has no reviewed labels.
- **Setup, project/provider changes or access failures:** [environment and troubleshooting](references/environment-and-troubleshooting.md) gives configuration tracing, API-state reconciliation and scoped cleanup checks.
- **Grading with a third-party scorer or store (MLflow, deepeval, Opik):** [provider compatibility](references/provider-compatibility.md) for what their ADK scorers record and how to keep results honest; `adk-agent-observability`'s export paths for keeping traces and telemetry in-house.
- **An incident to turn into a regression:** [deterministic tests](references/deterministic-tests.md) for the `fail_to_pass` and `pass_to_pass` lists and their grading rule, then step 2 of [evaluation design](references/evaluation-design.md#curate-cases-with-a-reason-to-exist) for the base-commit and reference-fix runs and the do-nothing control.
- **Runtime wiring, fault injection, observers, deadlines or browser timing:** [execution evidence](references/execution-evidence.md) gives concrete recipes and the checks that make their results trustworthy. For a flaky or failing tool, its fault matrix pairs with the resilience scoring at the end of [evaluation design](references/evaluation-design.md#grade-the-end-state-not-the-path).
- **Dataset curation, judge calibration, work budgets, ambiguous writes or release gates:** [evaluation design](references/evaluation-design.md) gives production implementation procedures and acceptance criteria, explicitly separate from historical companion coverage.
- **A rubric for a multi-stage pipeline, or one an optimiser or iteration loop will climb:** [shape the rubric before writing it](references/evaluation-design.md#shape-the-rubric-before-writing-it). It sets code checks first, scores each stage separately on the input that stage received, judges the work on the outcome measure rather than a rubric score, and, when the brief prices each error type, gates on the priced total against today's process. A judge whose verdict stops the run is re-checked on its costly side ([expert review](references/expert-review.md#calibrate-one-judge-per-failure-mode)).
- **Document-grounded claims or citation judges:** [source-support calibration](references/source-support-calibration.md) provides synthetic contrasts and an offline scorer that separates valid citations from supported conclusions.
- **Dynamic output schemas or provider rejection:** [provider compatibility](references/provider-compatibility.md) checks the actual serialized contract and plans a representative canary. **Recurring structural failures:** [experiment re-entry](references/experiment-reentry.md) records the reproducer, honest reference and new hypothesis before another broad paid cohort.
- **Staged paid failures, saved-stage recovery or repeated full-suite runs:** [progressive validation](references/progressive-validation.md) schedules focused checks, qualified continuation and fresh end-to-end evidence before the frozen release suite.
- **Agents CLI project (`agents-cli-manifest.yaml`, `tests/eval/`):** its dataset, trace and result files are `agentplatform` `EvaluationDataset` and `EvaluationResult` JSON, not ADK `EvalSet` or CSV; [live evaluations](references/live-evaluations.md#agents-cli-projects-use-a-different-asset) maps the assets and [result auditing](references/result-auditing.md#agents-cli-results-are-json-not-csv) the completeness checks. Consult the installed `google-agents-cli-eval` skill for the commands; if it is not installed, adk-engineer explains how to get it. This skill decides the cases and the evidence; Google's skill operates the commands.
- **Mandatory labels, document representations or prompt/schema/validator disagreement:** [contract qualification](references/contract-qualification.md) establishes source-reviewed solvability and the normal-route gate before paid inference.

## Apply the pattern

- Put business permission and validation in tools/backends. Use the real runner with a scripted model to force invalid decisions. When a workflow needs fresh verification, bind it to the intended invocation or validity window; an earlier conversational lookup is not automatically permission for a later write.
- For transactional confirmations, consider rendering from trusted tool receipts. Keep facts dynamic, receipt authority separate from conversation text, and successful effects intact after later failures. Compose existing callbacks. Reserve fixed response templates for transactional confirmations; give open-ended synthesis a schema sized to the judgment it owns.
- Preserve the distinction between a new session and a fresh backend. Reset or namespace business fixtures at the experimental unit being claimed. Assert attempted calls and stored effects separately.
- Choose trajectory matching for meaningful invariants. ADK 2.8.0's relaxed order modes still compare arguments and allow extra calls; a prohibited extra mutation needs its own assertion. ROUGE checks wording overlap, not truthful completion or authorisation.
- Capture the whole invocation and close its streams/runners. Bound synchronous grading in a worker controlled by an external deadline. Timeouts can leave partial evidence and cannot recall accepted provider requests. Model, simulator, judge, retry, tool and time limits are distinct.

## Authorisation and data boundaries

<!-- shared:consequential-operations-brief -->
Inspection is read-only, and code generation authorises no deployment, paid
call or live test. Before any consequential operation (an API, billing or
quota change, a billable resource, a secret, IAM, a data migration, a
deployment, a deletion, or a paid or destructive test), read
[consequential operations](references/operating-rules.md#consequential-operations),
present the exact scope and limits, obtain explicit approval and end the turn
to wait for it. Cleanup is a separate confirmed operation on resources this
workflow created.
<!-- /shared:consequential-operations-brief -->

Permission to implement tests is not permission to make paid calls or deploy them; name the isolated test target and work limits in every request. Never delete shared project resources to obtain a clean test.

## Validate and report

1. Run the project's meaningful offline checks with external access prevented where hermeticity is claimed. Validate eval/config schemas with its pinned ADK models. Check guards and effects, not just expected strings. Keep failing regressions when diagnosing a real defect.
2. For approved live work, follow the planned preflight/canary and cohort protocol within its bounds; include a paid preflight only when covered by that plan. Preserve a fixed cohort's cases, attempts and stop rules. Retain case/trial/metric counts and versioned criteria. Count a skipped paid test, a missing score, a zero-case conformance run and a bare successful process exit as `not run`. The result-auditing reference documents the bundled read-only [CSV checker](scripts/check_eval_results.py).
3. Check a second invocation for duplicate writes, duplicate test registration and needless configuration churn. Run only newly justified checks after a passing validation; retain failed observations instead of rerunning to green.
4. Report files changed, commands and exit/results, actual versions, what used real providers, what used doubles, what remains unverified, and any precise manual action or approval needed. Distinguish implementing a test from executing it successfully. The target project's results come from its own runs.

<!-- shared:evidence-labels-brief -->
Label each result with its tier (`offline`, `local`, `live` or `release`) and
outcome (`pass`, `fail`, `blocked` or `not run`) as
[evidence labels](references/operating-rules.md#evidence-labels) defines them;
earlier, vendor and documentation-only results are `historical`,
`vendor-measured` or `guidance`, never this session's evidence.
<!-- /shared:evidence-labels-brief -->

The skill's own checks and limitations are recorded in [validation.md](references/validation.md). Independent community project; not affiliated with or endorsed by Google.
