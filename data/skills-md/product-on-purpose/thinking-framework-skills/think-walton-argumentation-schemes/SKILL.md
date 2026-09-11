---
name: think-walton-argumentation-schemes
description: Evaluates one short defeasible argument by classifying it as a stereotyped reasoning scheme (appeal to expert opinion, analogy, sign, cause to effect, consequences, popular practice, slippery slope, practical reasoning), instantiating the scheme's premise slots to expose its implicit premises, then putting that scheme's keyed critical questions to it and rendering a presumption verdict that stands or falls by burden of proof. Produces a scheme critique sheet. Use when a single presumptive argument rests on an authority's say-so, a load-bearing analogy, a slippery-slope objection, or a consequence-based case, and the question is whether its presumption survives the standard defeaters for that pattern. Not for structurally complex multi-premise arguments (use argument-mapping) and not for deductive or statistical proof.
license: Apache-2.0
metadata:
  id: thinking-framework-skills.walton-argumentation-schemes
  family: reasoning-clarity
  evidence-tier: "P"
  version: 0.1.0
  standard: "0.8"
---
<!-- thinking-framework-skills | https://github.com/product-on-purpose/thinking-framework-skills | Apache-2.0 -->
# Argumentation Schemes with Critical Questions

Most everyday arguments are not deductive proofs. They are defeasible, presumptive moves: an expert says X, so presumably X; this case is like that case, so presumably the same verdict; doing A leads to bad consequence B, so presumably do not do A. Douglas Walton's insight is that these arguments come in a finite set of stereotyped patterns, that each pattern is legitimate (not a fallacy) when its conditions hold, and that each pattern has its own characteristic ways of failing. The durable move is **classify-then-probe-with-keyed-defeaters**: first identify which stereotyped scheme an argument instantiates, then interrogate it with the standard critical questions keyed to that scheme. Two things make this more than generic objection-raising. The defeaters are retrieved, not improvised - each scheme's question set encodes the accumulated knowledge of how that specific pattern fails, so coverage of the standard vulnerabilities does not depend on what occurs to the evaluator in the moment. And the semantics are presumptive - the output is not "valid or invalid" but a burden-of-proof ledger: which questions were answered, which remain open, and whether the presumption survives. The output is a **scheme critique sheet**, not prose.

## When to Use

- A single, usually short, defeasible argument has to be judged for whether its presumption deserves acceptance: a recommendation resting on an authority's say-so, an analogy doing load-bearing work, a slippery-slope objection, a "users are asking for it" popular-practice appeal, or a consequence-based case for or against an action.
- An argument map would be overkill. The scheme method is strongest where a map is weakest: a one-premise pattern argument ("the analyst report says the market is contracting, so we should not enter") maps to a trivial two-node tree, while the scheme method immediately yields the standard expert-opinion probes.
- Critique needs discipline in both directions - to block naive acceptance ("an expert said it") and naive dismissal ("appeal to authority, ignored"). These patterns are not automatic fallacies.

## When NOT to Use

- **Do not use it on structurally complex, multi-premise arguments.** When the question is how the whole argument hangs together and where its weakest links are, that is `think-argument-mapping`'s job. The scheme method evaluates one typed inference at a time and has no view of overall structure. This is the central routing wall.
- **Do not force a deductive or statistical argument into a scheme.** The schemes formalize presumptive reasoning; a mathematical proof or a regression result is not an instance of any of them, and forcing one in degrades the analysis. Route that material out.
- **Do not skip stating the classification, and do not trust a confident mis-type.** Every downstream critical question is keyed to the scheme, so a wrong match (reading an argument from sign as an argument from cause) produces a confident interrogation of the wrong vulnerabilities. State the scheme explicitly, name the runner-up scheme, and flag a low-confidence match. Even the five most common schemes machine-separate at only 63-91% accuracy (Feng and Hirst, 2011), so mis-typing is live, not rare.
- **Do not run it as checklist theater.** Walking the critical questions and recording shallow answers produces the appearance of scrutiny. The presumption verdict is only as good as the honesty of the answers; an answered checklist is not a soundness proof.
- **Do not treat naming the scheme as the verdict.** "Appeal to authority" is a classification, not a refutation. Naming the scheme is the beginning of evaluation, not its end.

## Instructions

When asked to evaluate a single defeasible argument - an authority appeal, an analogy, a slippery slope, a consequence case, or similar - follow these steps:

1. **Check the gate.** Confirm the argument is a single, short, presumptive inference. If it is structurally complex and multi-premise, route to `think-argument-mapping` and stop. If it is a deductive proof or a statistical result, say so and stop - it is not an instance of any scheme.
2. **Restate the argument.** Extract its conclusion and its stated premises in plain form. This is the object the rest of the procedure works on.
3. **Classify the scheme - explicitly and contestably.** Match the argument against the scheme catalog (appeal to expert opinion, argument from analogy, argument from sign, argument from cause to effect, argument from consequences, argument from popular opinion or practice, slippery slope, practical reasoning, and so on). Name the scheme, name the most plausible runner-up, and flag the match confidence. Do not skip this - every later step depends on it.
4. **Instantiate the premise slots.** Fill the chosen scheme's premise template against the argument. This mechanically exposes the implicit premises the pattern requires (for expert opinion: E is an expert, in the relevant field, E actually asserted X, E is credible and unbiased, X is consistent with other experts and the evidence). Name the implicit premises the argument left unstated.
5. **Put the scheme's keyed critical questions to the argument.** Retrieve the standard critical-question battery for the chosen scheme and answer each: answered (the argument or context discharges it), open (unaddressed), or defeated (a question shifts a burden the argument cannot meet). Record who carries the burden for each open question.
6. **Render the presumption verdict.** State whether the presumption STANDS (critical questions answered or dischargeable), STANDS-PENDING (survives but with named open questions to discharge), or FALLS (a question shifts a burden that goes unmet). Name the single binding open question that most controls the verdict.
7. **Emit the scheme critique sheet** per `references/TEMPLATE.md`: the restated argument, the named scheme with its runner-up and confidence, the instantiated premise slots with the implicit premises, the keyed critical questions with answer status and burden, and the presumption verdict with the binding open question. Carry the pre-printed evidence caveat into the sheet. Never present an answered checklist as a soundness proof, and never present the scheme name as a refutation.

## Output Format

Use the template in `references/TEMPLATE.md`. The deliverable is the filled scheme critique sheet - the restated argument, the contestable scheme classification, the instantiated premise slots, the keyed critical questions with answer status and burden, and the presumption verdict with its binding open question - not a prose essay. The verdict is a presumptive, burden-of-proof read, never a verdict of valid or invalid.

## Quality Checklist

Before finalizing, verify:

- [ ] The gate held: the argument is a single short presumptive inference, not a multi-premise structure (which routes to `think-argument-mapping`) and not a deductive or statistical proof.
- [ ] The argument is restated as a conclusion plus stated premises.
- [ ] The scheme is named explicitly, the runner-up scheme is named, and the match confidence is flagged - the classification is contestable, not hidden.
- [ ] The scheme's premise slots are instantiated, and the implicit premises the pattern requires are surfaced.
- [ ] Each keyed critical question for that scheme is answered with a status (answered / open / defeated) and a burden note - not skipped, not given a shallow rubber-stamp answer.
- [ ] A presumption verdict (stands / stands-pending / falls) is rendered, with the single binding open question named.
- [ ] The scheme name is not presented as a refutation, and the answered checklist is not presented as a soundness proof.
- [ ] No overclaiming: the verdict is a presumptive burden-of-proof read at tier P on transferred human-subjects evidence; it is not a soundness proof and not a measured gain in evaluation accuracy (see `evidence/dossier.md`).

## Evidence

Tier **P** (governing). The method rests on a 30-year theoretical literature (Walton 1996; Walton, Reed and Macagno 2008), a formal AI-and-law adoption line that models critical questions as typed premises carrying burden of proof (Gordon, Prakken and Walton 2007), software embodiments (Reed and Rowe 2004), an annotated corpus with an honest measure of how confusable the scheme types are (Feng and Hirst 2011: 63-91% one-against-others), and an active LLM benchmark showing the keyed-question apparatus is not already free in a plain-prompted model (Calvo Figueras and Agerri 2025: top system 67.6). There are two positive controlled classroom studies, but they measure weeks of scheme-and-critical-question INSTRUCTION on student writing and discussion (Song and Ferretti 2013, the cleanest; Nussbaum and Edwards 2011) - an adjacent claim to "applying the schemes once improves an evaluation," and human-subjects only. No study measures single-application evaluation accuracy, and nothing is validated on AI agents; the transfer is an explicit, untested assumption. Per this library's conservative rule the governing grade is P, not M. The skill ships as an argument-evaluation aid with hard walls, never as a soundness proof. Full grading, sources, and caveats: `evidence/dossier.md`.

## Examples

See `references/EXAMPLE.md` for a completed scheme critique sheet on a real decision.
