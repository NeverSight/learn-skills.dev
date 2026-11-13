---
name: pm-problem-statement
description: Write or critique a product problem statement — turning a vague prompt, signal, or feature request into a clear, evidence-grounded, testable statement of the real problem before any solution. Separates the problem from solutions, symptoms, goals, and constraints; applies the always-true core (gap not feature, root cause not symptom, specific and measurable, grounded in evidence, bridges user and business) and gates context-dependent decisions (which definition tool, how much measurability, reasoned vs. validated cause, scope). Trigger when asked to write a problem statement, define or frame a problem, identify the "real/true problem," turn a request or metric into a problem, or sharpen a vague product prompt before solving.
license: MIT
metadata:
  author: uxcel
  version: "1.0.0"
---

# Problem Statement Skill

## How this skill behaves (read first)

This is a **generative** skill, and a problem statement is where most product work quietly goes wrong. Claude's default is to restate a request as a problem and move on — producing the four classic failures: a **solution in disguise** ("users need a better search"), a **vagueness** ("the UX is bad," "the process is inefficient"), a **business outcome posing as a problem** ("we need to increase revenue"), or a **symptom mistaken for the cause** (churn is up → "fix churn"). Each one locks the team into solving the wrong thing, well. A good problem statement is a *gap a real user experiences, in context, grounded in evidence, measurable, and free of any named solution*. So this skill gates:

1. **Establish what you actually have** — a validated problem, or a prompt / signal / request / metric that only looks like one.
2. **Apply the always-true core** — separate problem from solution/symptom/goal, find the true cause, make it specific and measurable, ground it in evidence, bridge user and business.
3. **Surface the context-dependent decisions** (which definition tool, how much measurability now, reasoned vs. evidence-validated cause, scope) with trade-offs.

Then it **hands off to `pm-okr-metric-validity-audit` (the measurable element) and `pm-assumption-rigor-audit` (the assumed root cause)** for validation.

Scope: this skill owns the **problem-statement artifact**. It defers the broader **problem-finding process** to `pm-discovery`, **hypothesis/experiment design** to `pm-assumption-testing`, turning the statement into a full **spec** to `pm-product-spec` (audited by `pm-spec-quality-audit`), **ranking which problem to tackle** to `pm-prioritization-rigor-audit` / `pm-prioritization`, **personas depth** to `pm-personas-jtbd`, and **user stories** to `pm-user-story`.

---

## Step 0 — Establish context before writing the statement

Ask if not known; state the assumption if proceeding without an answer:

- **What do you actually have in hand?** A moving metric, a feature request ("add X"), or a vague directive ("improve onboarding") is a *signal or a solution*, not a problem. Restate it without metrics, tools, or desired outcomes first. The test: *could the sentence plausibly be said by the person experiencing the issue?*
- **Whose problem, and in what context?** A problem needs a specific group, moment, and difficulty. "Improve engagement" becomes workable only as "new users abandon setup because the required steps are unclear."
- **What evidence backs it — and is the cause known or assumed?** Distinguish what you've verified from what you're inferring. The root cause at this stage is usually a *reasoned* claim, not a proven one.
- **What is the statement feeding?** A spec, a discovery effort, an OKR, or an interview/case answer — this sets how measurable and formal it needs to be.

---

## The always-apply core (true for any problem statement)

- **A problem is a gap, never a feature.** It describes the distance between the current and desired state from the user's point of view, with no solution named. Translate "we need to add / we should build / the product lacks…" into a neutral description of what is difficult, slow, confusing, or risky. *Test:* if only one solution could address it, it's a solution in disguise — a real problem leaves room for several.
- **Separate the problem from symptoms, goals, and constraints.** A moving metric (churn, low adoption) is a *symptom*; "increase retention/revenue" is a *goal or business outcome*; budget and timeline are *constraints*. The problem sits underneath them — the user difficulty that *causes* the symptom. "We need to increase revenue" is never the problem.
- **Find the true cause, not the surface.** Use 5 Whys / reasoning to get from symptom to root. The cause must logically explain the symptom and survive being challenged ("the feature is already shown in onboarding, so 'users don't know it exists' doesn't hold — more likely it appears at the wrong moment"). Treat the cause as an explanation that has to stay consistent under questioning.
- **Be specific and fact-based.** "Users are unhappy" hides the cause and the impact. Name who is affected, when/where it happens, the concrete obstacle, and the measurable consequence. ❌ "We need to redesign the app." ✅ "Users fail to complete purchases because navigation between product and checkout pages is unclear."
- **Make it measurable.** Include a metric so success is checkable and scope is bounded ("decrease cart abandonment 15% within a month"). The measurable element doubles as a future key result. Without it, you can't know if you succeeded — but keep it a real outcome, not a vanity count.
- **Ground it in evidence, not internal assumption.** Verify the problem against user signals — interviews, support tickets, analytics, session replays — and synthesize patterns. Coding qualitative feedback into quantitative findings ("45% of reports mention a checkout error") turns opinion into evidence. A statement built only on what the team believes is the failure mode.
- **Bridge user and business.** Connect the user difficulty to its business impact (lost conversions, churn, cost, risk) so it earns attention — without treating user needs and business goals as competing. Translate a business problem into the user problem beneath it: "not enough signups" → *why* aren't users signing up (unclear value? complex flow? trust?).
- **Test the statement before using it.** Can design, engineering, and leadership each understand *who* is affected, *why* it matters, and *what's wrong* — without extra explanation, and without a solution baked in? If it keeps needing reinterpretation, it isn't done.

A workable structure: **problem + consequence/impact + intended goal**, carrying *who / when-context / measurable element* — or the **4 Ws** (Who, What, Where, Why) for the user-centric framing.

---

## The context-dependent decisions (surface, don't auto-apply)

Present each with its trade-off and a recommendation tied to Step 0; let the user choose. **Running every framework on every prompt is the failure mode — reach for the tool that closes the specific gap.**

| Decision | Apply when | Avoid / adapt when | Default recommendation |
|---|---|---|---|
| **Which definition tool** | Match to the gap: personas / empathy map (who & feelings unclear), journey map (where in the flow), 5 Whys / affinity (cause unclear), assumption mapping (team beliefs unchecked) | Running every framework as ritual, which buries the problem in artifacts | A 5 Whys pass + a Who/What/Where/Why framing; add others only if a specific gap remains |
| **How much measurability now** | Feeding a spec or committing resources — include a metric and tie it to an OKR | Earliest framing where any number would be a guess | Add the measurable element once the problem is validated; keep it falsifiable, not vanity |
| **Reasoned vs. evidence-validated cause** | A reasoned cause is fine for interviews, case work, or early low-stakes framing | Committing real build resources on a cause that's never been checked against users | Reason first, then validate with user evidence before the spec; scale rigor to the stakes |
| **Ambiguity: assume vs. ask** | Ask only the 1–2 questions that would *change* the framing; otherwise state a grounded assumption | Asking about every unknown (stalls) or silently guessing (hidden risk) | State explicit assumptions; ask only what moves the framing |
| **Scope / granularity** | Narrow to a specific segment + moment so analysis can proceed | Too broad ("improve UX") or arbitrarily narrow | One clear group, situation, and difficulty — broad enough for multiple solutions, narrow enough to act |

---

## Validate the result (orchestration)

> Hand-offs name each lens by its installable skill `name`. Invoke one only if that skill is installed; if it isn't, this skill's own core already carries these rules — proceed without it rather than blocking.

After producing or revising, hand it to the audit lenses rather than declaring it done. These are **candidate** lenses — posture per `docs/orchestration-policy.md`, or route the whole artifact through `pm-product-review`. Here **`assumption-rigor` is the always-relevant lens (auto-runs)**; the others are **offered**, tied to what the artifact actually contains. If the user invoked this skill for one specific thing, respect that scope.

- **`pm-assumption-rigor-audit`** *(auto-runs)* — the root cause is an *assumption* until validated. Is the riskiest cause-claim named honestly, and is the evidence behind it real (a pattern across sources) rather than a single anecdote or an internal belief?
- **`pm-okr-metric-validity-audit`** *(offer — if it names a measurable element)* — the measurable element: is it a real outcome that reflects the user's success, falsifiable, and not a vanity or gameable number? (This is also the metric that will likely become a key result.)

**Composition (per `docs/orchestration-policy.md` §9):** if discovery hasn't yet surfaced the underlying problems, that work (`pm-discovery`) is an upstream input; the **test designed for the statement** (`pm-assumption-testing`) and the **spec** it becomes (`pm-product-spec`) are downstream (offer to produce next, don't auto-generate). If the audits surface a conflict (e.g., the only available metric is a vanity number, or the cause can't be evidenced), resolve toward the purpose: **a problem statement exists to point the whole team at the right problem — keep it true, specific, and provable, not convenient.** For a full idea-to-plan build, `pm-idea-to-plan` is the compositional front door that sequences this step with the rest of the ladder and enforces evidence before the spec.

---

## Common do/don't patterns

| ❌ Don't | ✅ Do |
|---|---|
| "Users need a better search function" | "New users can't find relevant products because categories don't match how they think, so 40% leave without buying" |
| "The UX is bad" / "the process is inefficient" | Name who, when, the concrete obstacle, and the measurable impact |
| "We need to increase revenue" (business outcome) | Translate to the user problem beneath it ("users abandon checkout before paying") |
| Treat the symptom (churn) as the problem | Trace to the cause via 5 Whys; the symptom is a signal, not the problem |
| Bake the solution into the problem | Describe the gap so multiple solutions could address it |
| Leave it unmeasurable | Include a falsifiable metric; it becomes a key result |
| Build it on team assumptions | Ground it in user evidence; code qual feedback into quantitative findings |
| Accept a reasoned cause as proven | Reason first, then validate before committing real resources |
| Too-broad ("improve onboarding") | Narrow to a specific group, moment, and difficulty |
| Ship the statement unchecked | Hand off to okr-metric-validity + assumption-rigor |

---

## Source lessons (Uxcel)

- [Identifying the True Problem](https://uxcel.com/lessons/identifying-the-true-problem-542)
- [Defining Problems for Effective Specifications](https://uxcel.com/lessons/defining-problems-for-effective-specifications-501)
- [Problem Definition Tools](https://uxcel.com/lessons/tools-for-problem-definition-425)
- [Framing the Problem into Hypotheses](https://uxcel.com/lessons/framing-the-problem-into-hypotheses-415)
