---
name: good-design
description: Design and audit product experiences for ethical conversion, activation, retention, and expansion using product and behavioral-design principles. Use for SaaS UX, landing pages, onboarding, dashboards, forms, pricing, and feature decisions—not for visual styling alone.
---

# Good Design

Use this skill to make a product experience easier to understand, quicker to deliver its promised value, and worth returning to. The desired outcome is durable user value and a healthier business—not engagement tricks, coerced consent, or harder cancellation.

This skill brings together product and behavioral-design guidance for conversion, activation, retention, and expansion. Read [references/fontes.md](references/fontes.md) for the scope and evidence criteria.

## Start with the decision, not the pixels

Before proposing a layout, obtain or state the best available answers to these questions. Do not invent certainty; identify an assumption and propose how to test it.

1. **Who is the ICP here?** What is their urgent job, context, level of awareness, and actual willingness to invest effort?
2. **What promise got them here?** Is the product able to show the corresponding result—not merely its mechanics—within a credible time?
3. **What one behavior predicts durable value?** Define the activation event, its expected time-to-value (TTV), and the next repeat action.
4. **Where does the journey actually fail?** Use funnel data, support issues, interviews, usability sessions, and session replays. The intended Figma flow is a hypothesis, not evidence.
5. **What is the single next action?** Can someone scanning the screen tell what to do, why it matters, and what happens after?
6. **What mental work is unnecessary?** Count choices, fields, jargon, steps, waits, and competing visual signals. Remove or defer administrative friction; preserve only effort that creates commitment, intent, safety, or a better personalized path.
7. **What doubt, risk, or loss is present at this moment?** Put honest proof, specificity, privacy/payment reassurance, progress, or recovery next to the decision—rather than hiding it in generic marketing copy.
8. **How does continued use compound value?** Look for useful history, personalization, workflow embedding, collaboration, habit, and recurring real-world events. Never simulate lock-in through dark patterns; communicate accumulated value transparently and keep cancellation easy.
9. **What business result should improve, and what guardrail protects users?** Name one measurable hypothesis (for example activation rate, TTV, D7 retention, paid conversion, expansion) plus a guardrail such as completion quality, complaints, refund/chargeback rate, or accessibility.

If the request is visual-only and no goal or user context is supplied, ask these questions briefly or make the scope explicit: visual polish can support trust and hierarchy, but it cannot manufacture demand or repair a mismatched promise.

## Core operating principles

- **Design owns the journey.** Bring it upstream into requirements, information order, states, copy, and recovery—not only the final interface coat.
- **Direct rather than decorate.** Visual hierarchy, contrast, defaults, and copy should make the valuable, reversible next step obvious. Equal visual weight for every option creates decision cost.
- **Deliver proof before asking for effort.** Shorten the route to a meaningful result. A feature tour, blank dashboard, or long setup sequence makes people work before they know why.
- **Promise and delivery are one experience.** Landing page, sales conversation, trial, product, billing, and cancellation must describe the same ICP, effort, mechanism, and outcome. Expectation debt becomes churn.
- **Treat defaults as product decisions.** Most people keep them. Choose helpful, explainable defaults based on the ICP; make consequential choices visible and easily reversible.
- **Make progress legible.** Break difficult work into small, closable loops; acknowledge meaningful completion and show the value produced. Avoid artificial streaks, fake urgency, or progress that does not represent real work.
- **Retention is earned through compounding usefulness.** Design for real accumulated value and recurring jobs. At offboarding, state the real consequence clearly but never obstruct the exit.
- **Expansion follows use.** Present an upgrade when the user encounters a genuine value limit, explain the new capability in outcome language, and avoid interrupting someone before value appears.
- **Prefer subtraction to feature creep.** A new feature needs a specific user pain, adoption evidence, and a clear place in the primary mental model. A larger product can become functionally worse.
- **Treat interface changes as hypotheses.** Start from behavior and economics, test with enough signal, and avoid declaring a visual preference a win.

Read [references/fundamentos.md](references/fundamentos.md) for the decision framework, behavioral guardrails, and stages of product maturity.

## Choose the right review lens

Use the relevant section of [references/jornadas-e-superficies.md](references/jornadas-e-superficies.md):

- **Landing page / acquisition:** five-second comprehension, ICP filtering, problem-to-outcome narrative, demonstrable proof, one clear CTA, and fast loading.
- **Signup, forms, checkout:** minimize fields and input effort, show reassurance at the point of risk, delay qualification until behavior can reveal it, and make errors recoverable.
- **Onboarding and trial:** map every step to first value; fix the largest observed drop; use a guided, active first action; never strand new people in an empty dashboard.
- **Dashboard / data product:** answer “what should I do now?”; lead with insight and action, not a wall of numbers; reserve visual weight for the north-star metric.
- **Pricing / upgrade:** build one coherent value axis, make comparisons understandable, choose an ethical helpful default, and offer expansion at a real limit.
- **Retention / cancellation:** diagnose the lifecycle cause before reacting at the cancel screen; show genuine progress and accumulated value; make upgrade/migration discoverable before someone wants to leave.
- **Feature or redesign decision:** verify the user problem and current adoption. Protect well-learned, heavily used paths; improve around them unless evidence says the mental model itself is failing.

## Produce an actionable design review

For an audit, redesign, product spec, or design brief, deliver this compact structure unless the user requests another format:

1. **Objective and user:** ICP, job, moment, business metric, and user guardrail.
2. **Evidence and assumptions:** observed behavior versus hypotheses; the largest verified journey leak.
3. **Experience thesis:** one sentence connecting the promise to the first valuable action.
4. **Flow changes:** ordered screens/states, primary action, progressive disclosure, empty/loading/error/recovery states, and accessibility implications.
5. **Copy and trust moments:** only the essential words next to commitment, uncertainty, payment, privacy, and success.
6. **Retention / expansion implication:** how value compounds or which real limit triggers an upgrade, if applicable.
7. **Experiment:** variant or usability task, primary metric, guardrails, expected direction, and stopping criterion.

Distinguish an inference from evidence. Do not cite a cognitive-bias label as proof that a change works; it generates a testable hypothesis.

## Ethics and boundaries

Use behavioral design to reduce effort and clarify value, never to exploit confusion, hide terms, create false scarcity, block cancellation, preselect harmful choices, or induce compulsive use. For sensitive financial, health, children’s, or high-consequence workflows, prioritize comprehension, consent, accessibility, error recovery, and user control over conversion.
