---
name: pm-assumption-testing
description: Plan how to test the assumptions behind a product idea before building — decompose the idea into its load-bearing beliefs, prioritize the riskiest, phrase them as falsifiable hypotheses, and pick the cheapest method that answers the question. Or critique an existing validation plan. Trigger when asked to validate an idea, de-risk a feature, plan discovery/experiments, test assumptions or a hypothesis, design an MVP test, or decide "how do we know this will work?"
license: MIT
metadata:
  author: uxcel
  version: "1.0.0"
---

# Assumption Testing Skill

## How this skill behaves (read first)

This is a **generative** skill, and "validate our idea" is a default trap. The instinctive move is to jump to a method — build an MVP, run a survey, ship an A/B test — or to test *the idea* ("do you like this?", which everyone says yes to) instead of the **assumptions the idea depends on**. The other failure is investment mismatch: writing code to answer a question a one-day test would settle, or betting the quarter on a hallway poll. So this skill gates:

1. **Establish the decision and its stakes** — what choice does this inform, and how reversible/expensive is it? That sets how much rigor is warranted.
2. **Apply the always-true core** — decompose into testable assumptions, prioritize the riskiest, phrase them falsifiably, set success criteria up front.
3. **Choose the method deliberately** — surface the fidelity/method decision with trade-offs; don't default to "build it and see."

Then it **hands the plan to `pm-assumption-rigor-audit`** to validate (and `pm-okr-metric-validity-audit` for the success metric). **Applying every test type to every assumption is the failure mode** — match one good method to each risky belief.

---

## Step 0 — Establish context before planning tests

Ask if not known; state the assumption if proceeding without an answer:

- **What decision does this inform, and how reversible is it?** A cheap, reversible tweak needs a fast low-fi check; a costly, hard-to-undo bet earns stronger evidence. Rigor scales to stakes — over-testing a trivial call is as wrong as under-testing a big one.
- **What stage are we at?** Testing *the problem* (does anyone care?) vs. *the solution* (can they use/engage with it?) vs. *viability/scale* (will they pay, does it hold up?). Each stage points to a different method tier.
- **What's the leap-of-faith belief?** The one assumption that, if false, sinks the idea. Name it before anything else.
- **Resources & timeline** — what can realistically be run now? The cheapest method that answers the question wins.

---

## The always-apply core (true for any assumption test)

- **Test assumptions, not the idea.** Decompose the idea into the beliefs that must be true for it to succeed. "Do you like this concept?" gets a polite yes; "users will pay a premium for curated meals" is a belief you can actually check.
- **Cover the five assumption types; find which are at risk.** **Desirability** (do they want it?), **viability** (good for the business?), **feasibility** (can we build it?), **usability** (can they use it?), **ethical** (could it cause harm?). Generate assumptions via story mapping, the opportunity-solution tree, or the ideal-customer profile.
- **Prioritize by importance × certainty — test the riskiest first.** Map assumptions on a grid; the **high-importance, low-certainty** ones carry the risk. Test those before the comfortable ones. (A practical alternative ranking: high-impact *and* easy-to-test first, for quick wins.)
- **Phrase each as a falsifiable hypothesis.** Use **"We believe [change] for [user] will result in [outcome]; we'll know we're right when [metric] changes by [amount]."** Phrase positively (what users *will* do) and specifically — it forces a real fail condition and blocks confirmation bias.
- **Define success before you test.** Agree the pass/fail threshold with the team up front, so results can't be reinterpreted afterward.
- **Start with the cheapest method that answers the question.** Don't build code when a prototype works; don't build a prototype when a description works. Match investment to the certainty you need.
- **Ask about past behavior, not hypothetical intent.** "Tell me about the last time you dealt with this" beats "would you use this?" Stated intent is a false positive; real actions (clicks, sign-ups, pre-orders, purchases) are signal.
- **Prepare to be wrong.** Treat every test as learning; have a backup if the assumption fails. Invalidation is a win — it saves a wrong build.
- **Document and decide the next step.** Record assumption, method, pre-set criteria, result, and what you learned → confirm, adjust, or pivot. Test early and **continuously**, not as a one-off phase that goes stale.

---

## The context-dependent decisions (surface, don't auto-apply)

Match **one** method to each risky assumption based on what you need to learn and the stakes. **Don't run every test on every assumption.**

| Decision | Apply when | Avoid / adapt when | Default recommendation |
|---|---|---|---|
| **Low-fidelity: surveys, interviews, paper prototypes** | Testing *the problem* / desirability — does anyone care? Earliest, cheapest stage | Using stated "would you?" intent as proof of demand | Start here; pair interviews with the Mom Test (past behavior, not hypotheticals) |
| **Painted-door / landing-page / smoke test** | Measuring real *demand* with a behavioral signal (clicks, sign-ups) before building | Treating a click as proof the feature satisfies the need or will retain | Use to gate build/no-build; high CTR validates interest only |
| **Medium-fidelity: clickable mockup, concierge MVP, Wizard of Oz** | Testing *the solution* — can users understand/engage; deliver value manually before automating | Spending weeks polishing a prototype when a sketch answers it | Use to validate the value proposition before writing code |
| **High-fidelity: A/B test, feature flag, live beta** | *Optimizing or scaling* a validated idea; viability and real-condition behavior | Using it to discover whether anyone wants the thing (too expensive, too late) | Reserve for after demand is validated; needs adequate sample/duration. For A/B statistical rigor (sample size, significance, guardrails, peeking), hand off to `pm-experimentation-ab` |
| **Qualitative vs. quantitative** | Qual (interviews, open responses) for *why*; quant (analytics, large-n surveys, A/B) for *what* | Relying on one alone — pure-quant misses *why*, pure-qual chases loud voices | Cross-check both; agreement = green light, conflict = run another test |
| **Sample size / duration / significance** | Scale to the claim — usability bugs need ~5 users; conversion/preference needs many more and enough runtime | Generalizing from n=10 or a one-day window; ignoring significance in A/B | Size the test to the decision; don't over-engineer a reversible call |

---

## Validate the result (orchestration)

> Hand-offs name each lens by its installable skill `name`. Invoke one only if that skill is installed; if it isn't, this skill's own core already carries these rules — proceed without it rather than blocking.

After producing or revising, hand it to the audit lenses rather than declaring it done. These are **candidate** lenses — posture per `docs/orchestration-policy.md`, or route the whole artifact through `pm-product-review`. Here **`assumption-rigor` is the always-relevant lens (auto-runs)**; the others are **offered**, tied to what the artifact actually contains. If the user invoked this skill for one specific thing, respect that scope.

- **`pm-assumption-rigor-audit`** *(auto-runs)* — the core check: was the *riskiest* assumption targeted, phrased falsifiably, matched to a method of the right fidelity, with success criteria set up front and evidence read honestly (sample, duration, pattern vs. anecdote)?
- **`pm-okr-metric-validity-audit`** *(offer — if the hypotheses name success metrics)* — the success metric in each hypothesis: is it a real outcome, falsifiable, and not a vanity or gameable number?

**Composition (per `docs/orchestration-policy.md` §9):** this skill produces the test *plan*; broad discovery method (`pm-discovery`) is an upstream input and spec assumptions (`pm-product-spec`) are a peer that owns that sub-part (defer). If the audits surface a conflict (e.g. the cheap method can't actually answer the high-stakes question), resolve toward the decision at hand: **buy exactly the certainty the decision needs — no more, no less.** For a full idea-to-plan build, `pm-idea-to-plan` is the compositional front door that sequences this test ahead of the spec — and foregrounds it as a build gate rather than burying it in the PRD.

---

## Common do/don't patterns

| ❌ Don't | ✅ Do |
|---|---|
| "Validate the idea" by asking if people like it | Decompose into beliefs; test the assumptions the idea rests on |
| Test the easy/comfortable assumption | Map importance × certainty; test the riskiest (high-importance, low-certainty) first |
| "Users will like it" | "We believe [change] for [user] → [outcome]; right when [metric] moves [amount]" |
| Phrase it as what users won't do | Phrase positively — what users *will* do is easier to test |
| Decide success after seeing results | Set the pass/fail threshold before running the test |
| Build code to find out if anyone wants it | Cheapest method first — painted door / prototype before a build |
| "Would you pay for this?" in an interview | Ask about past behavior; measure a real action |
| Run one test, once, then move on | Test early and continuously; document and re-test |
| Treat a disproven assumption as a setback to ignore | Prepare to be wrong; let it change the decision |
| Ship the plan as final | Hand off to assumption-rigor + okr-metric-validity |

---

## Source lessons (Uxcel)

- [Assumption Testing](https://uxcel.com/lessons/assumption-testing-988)
- [Best Practices for Assumption Testing](https://uxcel.com/lessons/best-practices-for-assumption-testing-486)
- [Evidence-Based Product Discovery](https://uxcel.com/lessons/evidence-based-product-discovery-287)
- [Framing the Problem into Hypotheses](https://uxcel.com/lessons/framing-the-problem-into-hypotheses-415)
