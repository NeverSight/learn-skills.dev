---
name: think-analysis-of-competing-hypotheses
description: Handles a by-name request for ACH (Analysis of Competing Hypotheses), the evidence-by-hypothesis disconfirmation matrix, honestly. Controlled trials found ACH raises confidence with no accuracy gain and does not reduce confirmation bias, so this skill does NOT build the matrix as if valid. It leads with that evidence, then routes to the evidence-based move the job actually needs (think-red-team-light, think-evidence-vs-inference-sort, or think-what-would-have-to-be-true). Use only when someone asks for ACH or a competing-hypotheses matrix by name.
license: Apache-2.0
metadata:
  id: thinking-framework-skills.analysis-of-competing-hypotheses
  family: assumption-and-belief-challenge
  evidence-tier: "X"
  version: 0.1.0
  standard: "0.8"
  caveat-first: true
  posture: warn_redirect
  recommendation-policy: explicit_request_only
---
<!-- thinking-framework-skills | https://github.com/product-on-purpose/thinking-framework-skills | Apache-2.0 -->
# Analysis of Competing Hypotheses (ACH)

ACH builds an evidence-by-hypothesis matrix, scores each item of evidence for how well it disconfirms each hypothesis, and favors the hypothesis with the least inconsistent evidence. It is a famous intelligence-analysis technique, and it was tested and found wanting: in randomized controlled studies it raised participants' confidence without improving accuracy, and showed no debiasing or judgment-quality gain. This skill therefore does not reproduce the matrix as if it were valid. It owns the request, leads with what the controlled evidence shows, and routes you to the evidence-based move your actual job needs. The output is an honest redirect brief, not a disconfirmation matrix with a declared winner.

## Before you run this: what the controlled evidence shows

ACH is tier **X** (tested and found wanting, not merely undertested). On its own home population and stated purpose, the controlled record is null-to-negative:

- Otzipka (2025, *Applied Cognitive Psychology*): applying ACH significantly raised participants' confidence with no accuracy gain (confidence without accuracy).
- Dhami, Belton and Mandel (2019, *Applied Cognitive Psychology*): 50 intelligence analysts randomized; steps were skipped, bias effects were mixed, and ACH may have increased judgment inconsistency and error.
- Karvetski and Mandel (2020, *Judgment and Decision Making*, N=227): no gain in additivity, coherence, or consistency, and slightly reduced reliability.
- Whitesmith (2019); Maegherman et al. (2021); Dhami et al. (2024, the matrix layout specifically failed to reduce bias); Otzipka and Volbert (2026): no debiasing.

The mechanism's documented flaw: counting inconsistencies treats evidence items as independent and equally weighted, which they almost never are. Institutional adoption is not outcome evidence. So this skill will not hand you a filled matrix and a "least-inconsistent" verdict, because that artifact is exactly what the trials condemned. It states the caveat and redirects.

## When to Use

- The user asks for ACH (or a "competing hypotheses matrix") by name, and an honest warning plus a redirect serves them better than silently building the discredited artifact or refusing outright.

## When NOT to Use

- As a way to actually run the disconfirmation matrix and pick a winner (the move the controlled trials found raises confidence without accuracy).
- When the user has not named ACH: route generic "which explanation is right" work straight to the evidence-based skills below.

## Instructions

When asked to run ACH, follow these steps:

1. **Lead with the caveat.** State that ACH was tested and found wanting (raises confidence without accuracy; no bias reduction) and that you will not build the matrix as if valid.
2. **Name the real job.** What decision is behind the request? Disconfirming a leading thesis, auditing a claim set, or testing one option's conditions?
3. **Redirect to the evidence-based move** that fits the job (see the next section). Do not produce a disconfirmation matrix with a declared winner.
4. **If genuine rival-hypothesis discrimination is needed,** note that the better-grounded move is per-item necessity/sufficiency testing within one case (process tracing), not ACH's inconsistency arithmetic, and still do not present a matrix verdict as valid.
5. **Emit the honest redirect brief** per `references/TEMPLATE.md`.

## What to do instead

Route to the shipped, better-grounded move the job actually needs:

- Attack the leading thesis to find where it breaks: `think-red-team-light`.
- Separate what is evidence from what is inference in the claim set: `think-evidence-vs-inference-sort`.
- Test a named option's load-bearing conditions: `think-what-would-have-to-be-true`.

## Output Format

Use the template in `references/TEMPLATE.md`. The deliverable is the honest redirect brief (caveat, real job, evidence-based move), not a disconfirmation matrix.

## Quality Checklist

Before finalizing, verify:

- [ ] The controlled-evidence caveat leads the output.
- [ ] No disconfirmation matrix is presented as a valid conclusion or "least-inconsistent winner."
- [ ] The real decision behind the request is named.
- [ ] The output redirects to a specific evidence-based shipped skill that fits the job.
- [ ] Institutional adoption is not cited as if it were outcome evidence.

## Evidence

Tier **X** (tested and found wanting on direct, controlled, repeatedly replicated trials of the actual move). It ships as a contested lens, warn-and-redirect and explicit-request-only, so a by-name request gets an honest answer (the caveat plus the right alternative) rather than a flat refusal or the discredited artifact. The mechanism is genuinely distinct, but distinctness cannot rescue a failed evidence gate. Evidence is the controlled human-subject record above. Full grading: `evidence/dossier.md`.

## Examples

See `references/EXAMPLE.md` for a completed honest redirect brief.
