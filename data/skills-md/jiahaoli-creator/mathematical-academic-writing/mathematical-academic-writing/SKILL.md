---
name: mathematical-academic-writing
description: Draft, revise, review, or verify prose when the primary deliverable is mathematical writing, statistical writing, a statistical analysis plan or report, or mathematically grounded course material and correctness depends on notation, assumptions, proof logic, study design, inference, diagnostics, source fidelity, or evidence strength. Use for theorem-proof exposition, mathematical and statistical research, probability, stochastic processes, stochastic calculus, statistical analysis, inference and learning, quantitative finance, optimization, numerical analysis, empirical or computational studies, and technical notebooks. Also use to remove repetitive or defensive language without weakening mathematical or statistical meaning. Do not use for general copyediting, literature discovery alone, code-only data processing without statistical judgment, dashboarding, or formatting-only notebook work.
---

# Mathematical Academic Writing

## Aim

Produce source-grounded prose in which every paragraph performs a clear mathematical or statistical task. Preserve definitions, targets, designs, assumptions, results, uncertainty, notation, citations, and evidence strength while improving structure, explanation, directness, and economy.

Learn structural practices from the reference corpus and write original prose. Let the mathematical object, question, result, or evidence govern the presentation.

## Priority order

Resolve competing goals in this order:

1. mathematical and statistical validity;
2. scope and evidence accuracy;
3. source and notation fidelity;
4. genre and reader fit;
5. directness;
6. concision.

## Select task and genre modes

Choose evident modes without asking for confirmation.

Task modes:

- **Draft**: create prose from supplied sources and mathematical content.
- **Analysis**: frame or audit a statistical workflow from question and data structure through target,
  method, diagnostics, sensitivity, and reporting; use conditional branches when evidence is missing.
- **Revision**: improve existing prose while preserving or explicitly correcting its semantics.
- **Review**: classify material issues and recommend actions without silently rewriting the source.
- **Verification**: check claims, derivations, citations, numerical conclusions, or rendered artifacts against governing evidence.

Genre modes:

- research article;
- theorem-proof exposition;
- textbook or lecture explanation;
- statistical analysis plan, methods, or results;
- computational or empirical analysis;
- visual companion.

## Route references

Read only the references required by the task:

- Use [genre profiles](references/genre_profiles.md) to select section structure and authorial stance.
- Use [research-article workflows](references/research_article_workflows.md) for abstracts, introductions, contributions, related work, methods, results, referee reports, or responses.
- Use [mathematical integrity](references/mathematical_integrity.md) whenever formulas, proofs, stochastic claims, citations, or numerical evidence are in scope.
- Use the [statistical source map](references/statistical_source_map.md) to select among the user-designated inference, learning, Bayesian, robust, discretization, and optimization references.
- Use [general statistical analysis workflows](references/statistical_analysis_workflows.md) by default when planning, conducting, reviewing, interpreting, or reporting an analysis of data.
- Use [statistical writing and inference integrity](references/statistical_writing.md) whenever a population, sample, design, model, estimand, estimator, test, interval, prediction, causal claim, or empirical result is in scope.
- Use the [source and derivation audit](references/source_and_derivation_audit.md) for Verification, conflicting sources, suspected errors, or source-authorized correction.
- Use the [anti-defensive audit](references/anti_defensive_audit.md) for revision, review, compression, or generic AI-style prose.
- Use [artifact verification](references/artifact_verification.md) for notebooks, TeX, HTML previews, PDFs, execution claims, or rendered equations.
- Use [visual companion guidance](references/visual_companion.md) for captions, plots, simulations, or beginner-facing course material.
- Use the [MATH3015 profile](project_profiles/math3015.md) for this project's notebooks and previews.
- Use the [Advanced Mathematical Statistics profile](project_profiles/advanced_mathematical_statistics.md) only for that course's recording-to-notes workflow; it is an optional extension, not the default statistical route.
- Use the [quantitative-finance profile](project_profiles/quantitative_finance.md) when pricing, hedging, martingale measures, calibration, or identification is in scope.
- Use the [corpus manifest](references/corpus_manifest.md) only when explaining, evaluating, or updating this skill.
- Use the regression suites when changing or releasing this skill.

## Source grounding and the working register

Use the hierarchy supplied by the user. Treat the designated primary source as authoritative for notation, theorem scope, and topic boundaries; use auxiliary sources to clarify it, not to silently replace it.

Build the working register from [mathematical integrity](references/mathematical_integrity.md): active notation, objects, assumptions, claims, support, evidence rung, claim site, and citation. For statistical work, extend it with task, population, sample and design, variables, model, estimand, estimator, estimate, uncertainty, identification assumptions, and generalization scope. A claim with no support is unsupported.

Keep the register internal for a routine light edit. Show a compact register when the user requests it, when Verification or an audit needs traceability, or when the work changes a material entry. Report only entries that matter to the decision; do not turn the register into boilerplate.

Create no theorem, citation, numerical result, assumption, or attribution absent from the evidence. When sources conflict or a suspected source error matters, follow the source-correction protocol and do not normalize it silently.

In a stylistic revision, preserve the source claim and flag a suspected error separately. Correct mathematics only when substantive correction is requested or explicitly authorized by the governing source.

## Workflow

1. Identify task mode, genre, reader, governing sources, requested length, and verification depth.
2. Lock notation, terminology, assumptions, and claim scope in the working register.
3. Map the dependency chain. For mathematics use object -> assumptions -> claim -> support -> scope. For statistics use question -> provenance, units, and design -> estimand or prediction target -> method -> uncertainty -> diagnostics and sensitivity -> interpretation -> scope.
4. Draft or revise so each paragraph has one governing function; an assertion, its justification, and its immediate consequence may remain together.
5. Match verbs to the type and strength of evidence. When correcting an overclaim, state the nearest
   supported positive interpretation as well as the boundary; a denial alone is incomplete.
6. Site each claim once and make later mentions references rather than re-arguments.
7. Run the anti-defensive functional audit.
8. Compare the result with the register and the mathematical-integrity checklist.

## Verification depth

State or infer the deepest level actually required:

1. **Text-bound**: internal consistency, notation, logic, and claim wording.
2. **Source-bound**: compare with designated sources, theorem statements, citations, or derivations.
3. **Execution-bound**: rerun deterministic computations or notebooks and inspect outputs, seeds, tolerances, and errors.
4. **Render-bound**: inspect the exported HTML, PDF, or notebook preview for visible equations, labels, tables, captions, and hidden-code requirements.

The depth label records the deepest evidence actually inspected, not a deeper level needed to settle an unresolved claim. Never claim a deeper check than was performed. If a necessary source, execution, or render check is unavailable, retain the level reached, classify the affected claim as `unsupported` or `ambiguous`, and name the unavailable deeper check as the next step.

## Paragraph functions

| Function | Main job |
| --- | --- |
| Motivation | Identify a concrete question, obstruction, or computation. |
| Definition | Fix the object, domain, assumptions, quantifiers, and notation. |
| Study question | Fix the population, task, estimand, comparison, or prediction target. |
| Data and design | State the sample, variables, sampling or assignment mechanism, and exclusions. |
| Theorem | State verifiable assumptions and a precise conclusion. |
| Proof | Expose the dependency, construction, estimate, or limiting step. |
| Example | Move from object to computation to consequence. |
| Caption | Identify plotted objects, variables, and encoding. |
| Interpretation | Explain a visible pattern and its mathematical meaning. |
| Statistical result | Report the estimate, units, uncertainty, and design-calibrated interpretation. |
| Limitation | State a specific source, direction, and consequence of uncertainty. |

Let formulas, proofs, examples, captions, and interpretations perform different jobs. Merge or remove prose that only paraphrases an adjacent element.

## Claim siting and evidence vocabulary

State each claim where its support is strongest: the theorem that proves it, the derivation that yields it, or the experiment that measures it. Later mentions should point to the theorem, equation, section, or figure.

Restatement belongs beside the object it translates. Restatement that revisits a settled conclusion after intervening material is recapitulation; delete it. Keep a synthesis only when several separately established dependencies jointly support a new claim.

Use the evidence ladder in [mathematical integrity](references/mathematical_integrity.md). Select the strongest verb justified by the available support, and no stronger. Treat proof-verb density as a review trigger, never as a quota.

## Anti-defensive functional audit

For each potentially defensive sentence, ask:

1. Does it determine truth, scope, evidence, logic, or necessary reader guidance?
2. If yes, retain it as a precise condition, relation, contrast, or limitation.
3. If no, replace it with the mathematical content it delays or delete it.

Place each necessary limitation beside the claim it qualifies and state it once. Retain negation when it belongs to a definition, theorem, counterexample, failed converse, logical distinction, admissibility condition, or model boundary.

## Mathematical-integrity gate

Before returning work, compare source and output for:

- quantifiers, domains, boundary and endpoint cases, and index ranges;
- assumptions, admissibility, measurability, adaptedness, integrability, and regularity;
- population, sample, design or selection mechanism, estimand, estimator, and identification assumptions;
- effect size, units, standard error or interval, multiplicity, missingness, and finite-sample or asymptotic scope;
- descriptive, associational, predictive, causal, and robustness claims against the evidence that supports each;
- implication direction and necessary/sufficient status;
- equality, approximation, bounds, asymptotic notation, and convergence mode;
- theorem numbers, citations, numerical parameters, units, tolerances, seeds, and notation;
- source, execution, and rendering claims actually checked.

Retain every element that changes validity or interpretation. If a requested stylistic change conflicts with mathematical truth, preserve the verified mathematics and explain the conflict briefly.

## Holding a decision under pushback

A `Keep` or `Flag` that protects validity survives a request to reverse it. Name the element at stake—quantifier, admissibility, convergence mode, implication direction, measurability, estimand, design, identification, uncertainty, source conflict, or evidence strength—and ask for substantive ground.

Apply the change when the user supplies source authorization, a corrected statement, or a scope that does not need the protected element. A stylistic preference may change presentation; it cannot turn an unsupported or false claim into source-grounded prose.

## Output contract

### Review

For an explicit line-by-line audit, return the passage, function, material risk, and action: `Keep`, `Rewrite`, `Compress`, `Delete`, or `Flag`. For an ordinary review, return only prioritized findings that materially improve the text.

- `Rewrite` preserves or source-authorizes the claim while changing framing or evidence language.
- A statistical `Rewrite` must identify the supported scale or approximation and, when material, the
  unresolved assumption, estimate, or calculation; merely negating the source claim is incomplete.
- If only an asymptotic theorem supports a reported finite-sample interval or test, name that
  procedure itself as an asymptotic approximation; estimator asymptotic normality alone is insufficient.
- State material source-supplied totals explicitly in reader-facing prose when they affect design or
  interpretation; reconstructibility from component counts is not a substitute for retention.
- `Compress` removes repetition without collapsing distinct paragraph functions. If a caption and
  interpretation both remain necessary, keep the encoding in the caption and the pattern and
  mathematical meaning in a separate interpretation.
- `Delete` applies when the whole target contributes no unique content.
- `Flag` applies when safe revision requires missing source, notation, figure, context, or correction authority. Name the minimal conflicting evidence and what would resolve it.

### Revision

Return the revised text. Include a compact register or decision note only when it exposes a material change, unresolved ambiguity, or evidence boundary.

### Draft

Return prose in the selected genre, with a compact register when traceability is material. If the requested passage would only repeat settled material, return `Omit` with a short reason. If the requested claim lacks governing evidence, return `Flag` and name what is needed instead of manufacturing prose.

Before returning a Draft, cross-check the reader-facing prose—not the working register—against the supplied evidence for every material sample size, exclusion or missingness rate, unit, and analysis target. A value present only in the register is missing from the deliverable.

### Analysis

Return the question and use, unit and population, data structure, target, primary method and uncertainty,
preprocessing and missingness, diagnostics, sensitivity or multiplicity, and reporting boundary. Mark
unknowns and conditional branches; do not invent unavailable data or results.

### Verification

For each material claim, give its assumptions, governing evidence, decisive check, and status: `verified`, `unsupported`, `ambiguous`, or `incorrect`. Distinguish source, derivation, statistical interpretation, study-design, inference, editing, execution, and rendering errors. State the verification depth reached. Supply corrected wording only when substantive correction is requested or authorized.

Fix the verdict target before assigning its status. If a sentence combines an object-level conclusion
with a warrant or implication, assess them as separate claim units. Missing identification,
calibration, source, or execution makes the affected conclusion `unsupported`; use `incorrect` only
when decisive evidence contradicts the target claim or inference. If one verdict is required, name
the claim unit it classifies and do not transfer a verdict from one unit to another.

For `unsupported` or `ambiguous`, name the missing source, check, or correction authority needed to resolve the claim. When correction is authorized, give the smallest evidence-preserving repair; for artifact defects, repair the artifact mechanism without changing valid mathematics.

Keep material numerical evidence in reader-facing verification fields. When subgroup rates,
thresholds, or numerical contrasts support the verdict, report the supplied values rather than only
summarizing them qualitatively.

When a claim asks for an interpretation on a scale the evidence does not supply, state the nearest supported interpretation and name the additional estimate or calculation needed for the requested scale. Do not manufacture that quantity.
For design-limited population claims, identify what the reported quantity still describes—for example, the observed sample—before naming the weighting, dependence, or variance correction needed for population inference.

### Visual companion

Use course notation and only enough formal statement to read the visual. Let figures, experiments, and concise interpretations carry the explanation. Reproduce a lecture proof only when requested.

## Maintenance

When changing or releasing this skill, follow [MAINTENANCE.md](MAINTENANCE.md). Runtime writing tasks do not load maintenance or regression materials.
