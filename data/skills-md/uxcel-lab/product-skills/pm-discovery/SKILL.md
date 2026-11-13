---
name: pm-discovery
description: Plan or critique a product discovery process — figuring out what to build before building it. Establishes which risk you're de-risking and how much certainty the decision needs, applies the always-true core (continuous not phased, outcomes over output, problem before solution, ask about past behavior, match evidence to risk, generate solutions from validated problems, research ethically) and gates the context-dependent decisions (problem vs. solution research, qual vs. quant, lightweight vs. deep, how much certainty before committing). Trigger when asked to plan discovery, "figure out what to build," set up continuous discovery, design a research plan, do customer/user research, find problems worth solving, or de-risk a product direction before committing.
license: MIT
metadata:
  author: uxcel
  version: "1.0.0"
---

# Product Discovery Skill

## How this skill behaves (read first)

This is a **generative** skill, and "do some discovery" hides several default traps. The instinctive moves are: treat discovery as a one-time research phase before building (then never revisit it), jump straight to solutions and features, run a generic "interview a few users + send a survey" plan without matching the rigor to what's actually at stake, measure success by what shipped rather than what changed, and ask users "would you use this?" (everyone says yes). The result is a feature factory that's busy but not learning. Good discovery is **continuous, problem-first, outcome-oriented, and evidence-matched-to-risk**. So this skill gates:

1. **Establish which risk you're de-risking and how much certainty the decision needs** — value, usability, feasibility, or business-viability risk; a cheap reversible call needs far less evidence than an expensive irreversible bet.
2. **Apply the always-true core** — continuous cadence, outcomes over output, problem before solution, past behavior over hypotheticals, evidence matched to risk, solutions from validated problems, ethical research.
3. **Surface the context-dependent decisions** (problem vs. solution research, qual vs. quant, lightweight vs. deep, DIY vs. specialist, how much certainty before committing) with trade-offs.

Then it **hands off to `pm-assumption-rigor-audit`, `pm-okr-metric-validity-audit`, and `pm-prioritization-rigor-audit`** for validation. The actual **test/experiment design** for a specific assumption belongs to the generative `pm-assumption-testing` skill — discovery decides *what to learn and how much it matters*; assumption-testing designs the *test*.

---

## Step 0 — Establish context before planning discovery

Ask if not known; state the assumption if proceeding without an answer:

- **Which of the four risks is most uncertain?** **Value** (will anyone want it?), **usability** (can they use it?), **feasibility** (can we build it?), **business viability** (does it fit the business?). Discovery exists to retire whichever risk is highest — name it before choosing activities.
- **Are you in the problem space or the solution space?** "Does anyone care about this problem?" is a different question, with different methods, from "does this solution work?" Don't skip to solution discovery before the problem is validated.
- **How reversible and expensive is the decision this informs?** This sets how much certainty to buy. Over-researching a one-way-door reversible tweak wastes the quarter; under-researching an irreversible, costly bet is how teams ship the wrong thing.
- **Who's involved, and at what cadence?** The product trio (PM + designer + engineer) plus cross-functional partners; is this a continuous habit or a one-off study? Default toward continuous.

---

## The always-apply core (true for any discovery effort)

- **Make discovery continuous, not a phase.** Research done once upfront goes stale within months. Integrate lightweight customer contact into the weekly rhythm — short interviews, support-ticket reviews, silent-observer sales calls — and treat it as non-negotiable as sprint planning. Automate recruiting (a standing booking link, in-product intercepts) so a busy week doesn't kill it. *Episodic discovery produces insights that expire; continuous discovery compounds.*
- **Orient to outcomes, not output.** Define the change in user behavior you want (a *product outcome*, a leading indicator you can influence) that ladders up to a *business outcome* (revenue/retention, a lagging indicator). "Launch the help center" is output; "reduce support tickets 15%" is an outcome. Vanity-metric test: *"Could a happy, successful user never do this action?"* If yes, it's vanity. This is the defense against the build trap.
- **Start in the problem space; separate problems from symptoms.** A feature request or a complaint ("users abandon carts") is a symptom; the root problem (confusing checkout? late shipping costs? payment distrust?) is what you design against. Validate the problem is real and significant *before* solving it.
- **Ask about past behavior, not hypothetical intent (the Mom Test).** "Would you use this?" gets a polite yes — a false positive. "Walk me through the last time you dealt with this" gets something verifiable. Ask about their life, not your idea; specifics in the past, not hypotheticals in the future; listen for problems, not their proposed solutions. Stay quiet after they finish — the silence surfaces the real insight.
- **Match evidence to the decision's risk, and tell signal from noise.** The "truth curve": lightweight methods (surveys, interviews, paper prototypes) are cheap but filtered through your judgment; live behavior is the strongest truth. Pick the method that gives *enough* certainty for *this* decision. Filter requests by **pattern, not urgency** (a recurring theme across support + sales + interviews beats the loudest single client) and by **blocker vs. nice-to-have**. Cross-check **quantitative (what's happening)** with **qualitative (why)** — agreement is a green light, conflict means run another test before committing.
- **Generate solutions from validated problems — plural, then compare.** Once a problem is validated, explore several distinct solution directions and compare them on **desirability × feasibility × viability**, each traceable to a user insight and framed as a hypothesis to test, not a foregone conclusion. Jumping from request straight to one feature is order-taking, not problem-solving, and breeds feature creep.
- **Research ethically and inclusively.** Get genuine informed consent (plain language, easy withdrawal, granular recording choices, mindful of power dynamics). Recruit beyond convenient echo chambers (your existing power users skew the problem frame). Watch for bias in *problem framing* ("users need faster checkout" already assumes who the user is). Apply cultural sensitivity and extra safeguards for vulnerable populations, and keep competitive analysis to honest, public sources.
- **Align stakeholders continuously — no surprises.** Treat the stakeholder hand-off as a collaborative checkpoint, not a reveal: involve them in research sessions early, align on the *problem* before the solution, make trade-offs visible (impact vs. effort), and let them watch real user struggle rather than reading slides. Stakeholders who saw the evidence become champions, not blockers.

---

## The context-dependent decisions (surface, don't auto-apply)

Present each with its trade-off and a recommendation tied to Step 0; let the user choose. **Running every method at full depth on every question is the failure mode — buy the certainty the decision needs, no more.**

| Decision | Apply when | Avoid / adapt when | Default recommendation |
|---|---|---|---|
| **Problem research vs. solution testing** | Problem-space methods (interviews, observation, support logs) when "does anyone care?" is still open | Testing a solution's usability before the underlying problem is validated | Validate the problem first; move to solution testing only once it's real |
| **Qualitative vs. quantitative** | Qual (interviews, open responses) for *why* and early signal; quant (analytics, large-n, behavior) for *what* and scale | Relying on one alone — pure-quant misses why; pure-qual chases the loudest voice | Cross-check both; when they conflict, run another test before deciding |
| **Continuous lightweight vs. periodic deep study** | Weekly touchpoints for ongoing signal; a deeper dedicated study for a big or unfamiliar bet | Letting a one-off study stand in for ongoing contact; or over-studying a small reversible call | Continuous baseline cadence + targeted deep dives for high-risk decisions |
| **DIY (PM/trio-led) vs. dedicated researcher** | PM-led lightweight research for speed and staying close to users | Complex, high-stakes, regulated, or vulnerable-population studies that need specialist rigor | Build the habit yourself; bring specialists in where rigor is decision-critical |
| **How much certainty before committing** | Scale evidence to the decision's risk and reversibility (truth curve) | Over-researching a reversible tweak; under-researching an irreversible, costly bet | Buy exactly the certainty the decision needs; hand the specific assumption test to `pm-assumption-testing` |
| **Whose voices to weight** | Patterns across multiple sources; representative + inclusive recruitment; blockers over nice-to-haves | Weighting by volume/urgency or the single loudest client; convenient echo-chamber samples | Weight by pattern and representativeness, not noise |

---

## Validate the result (orchestration)

> Hand-offs name each lens by its installable skill `name`. Invoke one only if that skill is installed; if it isn't, this skill's own core already carries these rules — proceed without it rather than blocking.

After producing or revising, hand it to the audit lenses rather than declaring it done. These are **candidate** lenses — posture per `docs/orchestration-policy.md`, or route the whole artifact through `pm-product-review`. Here **`assumption-rigor` is the always-relevant lens (auto-runs)**; the others are **offered**, tied to what the artifact actually contains. If the user invoked this skill for one specific thing, respect that scope.

- **`pm-assumption-rigor-audit`** *(auto-runs)* — are the riskiest assumptions surfaced and named, rather than comfortable ones? Discovery's job is to expose leap-of-faith beliefs; this checks they're targeted honestly. (For the *design* of the test that retires each one, use the `pm-assumption-testing` skill.)
- **`pm-okr-metric-validity-audit`** *(offer — if it names outcomes/success metrics)* — the product/business outcomes and success metrics the discovery is steering toward: are they real outcomes (not vanity or output counts), falsifiable, and within the team's influence?
- **`pm-prioritization-rigor-audit`** *(offer — if it ranks problems/opportunities)* — when discovery ranks which problems/opportunities are worth solving: is the ranking evidence-based and strategy-linked, not a feature-factory backlog or HiPPO pick?
- **`pm-decision-quality-audit`** *(offer — if it culminates in a significant, hard-to-reverse build/no-build decision)* — process over outcome, reversibility-matched deliberation, pre-mortem.

**Composition (per `docs/orchestration-policy.md` §9):** this skill produces the discovery *plan and its insights*. **Test/experiment design** (`pm-assumption-testing`) is a peer that owns that sub-part (defer). **Problem-statement craft** (`pm-problem-statement`), **personas/JTBD** (`pm-personas-jtbd`), **competitive/market analysis** (`pm-competitive-analysis`), **detailed prioritization frameworks** (`pm-prioritization`), **roadmapping** (`pm-roadmap`), and **metric/OKR definition** (`pm-okrs-kpis`) are downstream (offer to produce next, don't auto-generate). If the audits surface a conflict (e.g., the cheap method can't actually retire the high-stakes risk), resolve toward the decision at hand: **discovery serves a decision — learn exactly enough to make it well, then decide.** For a full idea-to-plan build, `pm-idea-to-plan` is the compositional front door that runs this rung *before* the spec — it's the evidence step the PRD-rushing default skips.

---

## Common do/don't patterns

| ❌ Don't | ✅ Do |
|---|---|
| Run discovery once upfront, then build | Make it a continuous weekly habit; automate recruiting so it survives busy sprints |
| Measure success by features shipped | Define product outcomes (behavior change) that ladder to business outcomes |
| Jump from a feature request to building it | Find the root problem behind the request; validate it's real first |
| "Would you use this?" / "Would you pay $20?" | "Walk me through the last time you faced this" — past behavior, not hypotheticals |
| Treat the loudest client as the roadmap | Filter by pattern vs. anecdote and blocker vs. nice-to-have |
| Pick qual or quant and trust it alone | Cross-check both; conflict = run another test before committing |
| Commit to the first solution that appears | Generate several, compare on desirability × feasibility × viability, frame as hypotheses |
| Recruit only existing power users | Inclusive, representative recruitment; watch bias in problem framing |
| Reveal findings to stakeholders at the end | Involve them throughout; align on the problem; show real user struggle |
| Over-research a reversible call / under-research an irreversible one | Match certainty to the decision's risk; hand the specific test to assumption-testing |
| Ship the plan as final | Hand off to assumption-rigor + okr-metric-validity + prioritization-rigor |

---

## Source lessons (Uxcel)

- [Intro to Product Discovery](https://uxcel.com/lessons/intro-to-product-discovery-663)
- [Continuous Discovery Mindset](https://uxcel.com/lessons/continuous-discovery-mindset-167)
- [Business Outcomes vs. Product Outcomes](https://uxcel.com/lessons/business-outcomes-vs-product-outcomes-443)
- [Finding Problems to Solve](https://uxcel.com/lessons/finding-problems-to-solve-958)
- [Evidence-Based Product Discovery](https://uxcel.com/lessons/evidence-based-product-discovery-287)
- [Ethics in Product Discovery & Definition](https://uxcel.com/lessons/ethics-in-product-discovery-definition-871)
- [Getting Closer to Customers](https://uxcel.com/lessons/getting-closer-to-customers-817)
- [Generating Strong, User-Centric Solutions](https://uxcel.com/lessons/generating-strong-user-centric-solutions-448)
