---
name: pm-personas-jtbd
description: Build or critique an audience-understanding artifact — research-based user personas, a Jobs-to-Be-Done framing, or the choice between them. Grounds the work in real research (never invented demographic fiction), keeps only detail that changes a decision, and picks the lens by research objective, stage, and resources. Applies the always-true core and gates context-dependent decisions (personas vs. JTBD vs. both, research-based vs. proto, how many personas, which details, segmentation depth, AI's role). Trigger when asked to create user personas, define a target audience/segment, apply Jobs-to-Be-Done, decide who the product is for, or review existing personas.
license: MIT
metadata:
  author: uxcel
  version: "1.0.0"
---

# Personas & Jobs-to-Be-Done Skill

## How this skill behaves (read first)

This is a **generative** skill, and personas are where an AI assistant is most tempted to do exactly the wrong thing. Asked to "make some personas," the default is to invent plausible demographic fiction — "Sarah, 32, marketing manager, loves yoga and oat-milk lattes" — with no research basis, needs *inferred from* demographics, and a pile of irrelevant lifestyle detail. Uxcel's own source is blunt about it: LLM-generated personas reflect generic internet stereotypes and underrepresent edge cases and minority users. A useful persona instead **synthesizes real research into a memorable character whose every detail could change a design decision** — or, when what matters is the *progress a user is trying to make*, a **Job-to-Be-Done** is the better lens. So this skill gates:

1. **Establish the research objective, the stage/data you have, and the resources** — these decide whether to use personas, JTBD, or both, and whether you even have the evidence to build one yet.
2. **Apply the always-true core** — ground in real research, keep only decision-relevant detail, use JTBD for the job and personas for the who, keep the set small, build as a team, and keep it alive.
3. **Surface the context-dependent decisions** (lens choice, research-based vs. proto, count, which details, segmentation depth, AI's role) with trade-offs.

Then it **hands off to `pm-assumption-rigor-audit`** — the check that the persona's claimed needs and behaviors rest on evidence, not assumption.

Scope: this skill owns the **audience-understanding artifact**. It defers the **research process that feeds it** to `pm-discovery` (including ethical/inclusive recruitment), **framing the user problem** to `pm-problem-statement`, **turning a persona + job into stories** to `pm-user-story`, and **behavioral/cohort analytics depth** to `pm-analytics`.

---

## Step 0 — Establish context before building

Ask if not known; state the assumption if proceeding without an answer:

- **What's the research objective?** Understanding *motivations and unmet needs* → JTBD. *Targeted marketing / team alignment around who* → personas. *Guiding product development* → both. The objective picks the lens.
- **What stage are you at, and what data exists?** Early stage with only qualitative interviews → JTBD or a clearly-labeled proto-persona. Established product with analytics + research → research-based personas. *Do not fabricate what you don't have.*
- **What resources and time?** JTBD leans on deeper qualitative interviews (more costly); personas can start from analytics and short surveys (quicker, broader).
- **Who is the artifact for?** A diverse team that needs a shared, relatable reference → personas. A team hunting unmet needs and innovation → JTBD.

---

## The always-apply core (true for any persona or JTBD work)

- **Ground it in real research — never fiction, never AI stereotype.** A persona synthesizes patterns found in interviews, field studies, surveys, and analytics. If no research exists yet, build a **proto-persona** *labeled as an assumption placeholder* and test it — don't pass it off as validated. AI (including this assistant) is a *synthesis and drafting* aid once you have real data; it is not a research substitute, because generated personas reproduce generic stereotypes and erase edge cases.
- **Every detail must change a design decision.** The test for any attribute: *would it change a decision?* If not, cut it. Lead with **psychographics** (goals, pain points, motivations, behaviors) — the layer that drives decisions — and include demographics only when relevant to how the person uses the product. Irrelevant detail doesn't add richness; it erodes the team's trust in the whole persona.
- **Don't derive needs from demographics.** Two people of the same age and income behave differently. Demographics are a *starting point* for segmentation, not the source of needs — build needs from research insight.
- **Use JTBD for the job, personas for the who.** JTBD asks what progress the user is "hiring" the product to make ("users hire it, and fire it when it disappoints") — focused on the outcome, more stable than demographics, and strong for innovation and differentiation. Personas add the empathy, context, and feelings JTBD misses. They're complementary: a job like "find a product quickly" may span several personas, which is exactly what makes it worth prioritizing.
- **Keep the set small, with a clear primary.** Most products need ~3–5 (up to 7) personas. Merge groups that would make the same design demands; drop segments too small to influence decisions. Designate one **primary** persona per product area (decisions default to serving it) and treat others as **secondary** (accommodated, never overriding).
- **Build as a team and test with scenarios.** Involving researchers, designers, and PMs surfaces assumptions and earns trust. Write short scenarios (a persona pursuing a goal) to anchor requirements in real context and to pressure-test whether the persona is credible.
- **Keep it alive.** A persona is a snapshot, not a permanent record. Merge two that have converged, split one that's gotten too broad, and revise as the product, market, or user base shifts — teams that revise more often rate their personas as far more impactful. Having a persona is not an excuse to stop talking to users.

To narrow from "everyone": define the **target market** (who has the strongest need *and* access), then the **target audience** (the specific segment for a given release), layering demographic → psychographic → behavioral data before giving the segment life as a persona or job.

---

## The context-dependent decisions (surface, don't auto-apply)

Present each with its trade-off and a recommendation tied to Step 0; let the user choose. **Defaulting to "generate three demographic personas" is the failure mode.**

| Decision | Apply when | Avoid / adapt when | Default recommendation |
|---|---|---|---|
| **Personas vs. JTBD vs. both** | JTBD for motivation/unmet-needs/innovation and early-stage; personas for team alignment, marketing, and the "who" of an established product | Forcing one lens regardless of the objective | Match to research objective + stage; use **both** for product development (personas = who, JTBD = what) |
| **Research-based vs. proto-persona** | Proto-persona only as a labeled placeholder when research doesn't exist yet | Presenting a proto-persona (or an AI-drafted one) as validated | Proto only to make assumptions visible; replace with research-grounded as soon as data arrives |
| **How many / primary–secondary** | Multiple personas only for genuinely distinct user groups | A persona per micro-segment — unmemorable and unmaintainable | As few as cover meaningful variation (~3–5); one primary per product area |
| **Which details to include** | Only attributes that would change a design decision; demographics when relevant to use | Demographic fiction, lifestyle filler, idealized stock-photo stereotypes | Psychographics-first; keep it to 1–2 pages; cut anything that wouldn't move a decision |
| **Segmentation depth** | Demographics as a starting frame, then psychographics (*why*) and behavior (*how*) for real groups | Segmenting on demographics alone and inferring needs from them | Layer demographic + psychographic + behavioral, grounded in first-party data |
| **AI's role** | AI to cluster transcripts, surface patterns, and draft profiles *after* real data is collected | AI to invent the persona from a prompt (generic stereotypes, missing edge cases) | Use AI for synthesis and formatting; the starting point is always fieldwork |

---

## Validate the result (orchestration)

> Hand-offs name each lens by its installable skill `name`. Invoke one only if that skill is installed; if it isn't, this skill's own core already carries these rules — proceed without it rather than blocking.

After producing or revising, hand it to the audit lenses rather than declaring it done. These are **candidate** lenses — posture per `docs/orchestration-policy.md`, or route the whole artifact through `pm-product-review`. Here **`assumption-rigor` is the always-relevant lens (auto-runs)**; the others are **offered**, tied to what the artifact actually contains. If the user invoked this skill for one specific thing, respect that scope.

- **`pm-assumption-rigor-audit`** *(auto-runs)* — the core check: are the persona's needs, goals, and behaviors (or the job's desired outcome) grounded in evidence and a real pattern, or quietly assumed — inferred from demographics, carried over from a proto-persona, or generated from generic priors? Flag the load-bearing claims that haven't been validated and need a research pass.

**Composition (per `docs/orchestration-policy.md` §9):** the artifact then feeds the rest of PM work rather than being audited by it. The **research that grounds it** (`pm-discovery`) is an upstream input. The **problem framing** (`pm-problem-statement`) and the **user stories** (`pm-user-story`) the persona + job become are downstream (offer to produce next, don't auto-generate). If the audit shows the persona is mostly assumption, resolve toward the purpose: **a persona exists to keep a real, specific user present in every decision — if it isn't grounded in research, it's a stereotype wearing a name tag, and it will mislead the team.** For a full idea-to-plan build, `pm-idea-to-plan` is the compositional front door that sequences this step with the rest of the ladder and enforces evidence before the spec.

---

## Common do/don't patterns

| ❌ Don't | ✅ Do |
|---|---|
| Invent "Sarah, 32, loves yoga" from a prompt | Synthesize a persona from real interviews, analytics, and field research |
| Treat an AI-generated persona as research | Use AI to cluster/draft *your* data; fieldwork is the starting point |
| Infer needs from age/gender/income | Build needs from research; demographics are only a segmentation starting point |
| Stuff the persona with lifestyle trivia | Include only detail that would change a design decision; psychographics first |
| Pick personas because they're familiar | Choose the lens by objective — JTBD for the job, personas for the who, both for product dev |
| Ship a proto-persona as fact | Label assumptions as a placeholder and test them |
| Spin up a persona per micro-segment | ~3–5, merge similar, drop peripheral, name one primary |
| Create personas once and frame them on a wall | Build as a team, test with scenarios, revise as data shifts |
| Ship the persona unchecked | Hand off to assumption-rigor to flag unvalidated claims |

---

## Source lessons (Uxcel)

- [Personas vs. Jobs to Be Done](https://uxcel.com/lessons/personas-vs-jobs-to-be-done-026)
- [Personas in UX Research](https://uxcel.com/lessons/personas-205)
- [13 Tips for Creating User Personas](https://uxcel.com/lessons/best-tips-to-create-a-user-persona-928)
- [Defining Target Audience](https://uxcel.com/lessons/defining-target-audience-932)
