---
name: scamper
description: Transform existing ideas into improved variants using the SCAMPER method (Substitute, Combine, Adapt, Modify, Put to other use, Eliminate, Reverse). Use when the user has a baseline idea to improve, a process to redesign, or needs systematic ideation for differentiation.
---

# SCAMPER ideas transformer

## 1) Purpose

This skill helps a user transform an existing idea (product, service, process, policy, or content concept) into multiple improved or differentiated variants using the full SCAMPER method:

- S: Substitute
- C: Combine
- A: Adapt
- M: Modify / Magnify / Minify
- P: Put to another use
- E: Eliminate
- R: Reverse / Rearrange

The skill is optimized for a continuous, back-and-forth dialogue. It maintains a running "idea model" and iteratively enriches that model with relevant information found on the public web (benchmarks, analogs, constraints, technical options, examples, user pain points, pricing patterns, regulations, etc.).

## 2) When to Use

Use this skill when the user has:
- A baseline idea they want to improve, differentiate, or repurpose.
- A process they want to redesign (reduce steps, cost, time, defects).
- A concept that is "stuck" and needs systematic variation.
- A need for a structured ideation checklist that reliably produces options.

Do NOT use this skill for:
- Purely exploratory ideation without any starting subject.
- Requests primarily about verifying facts (use a research skill instead).
- Problems requiring rigorous root-cause analysis before ideation (do that first).

## 3) Inputs and Outputs

Inputs (minimum):
- Subject: what is being transformed (one sentence).
- Objective: what "better" means (e.g., cheaper, faster, safer, more adoption).
- Constraints: must-haves and must-not-do (budget, timeline, compliance, tech).

Optional inputs:
- Audience / user segment
- Current design or workflow steps
- Known blockers, risks, and assumptions
- Success metrics and target ranges

Outputs:
- A set of labeled idea variants mapped to SCAMPER letters and prompts.
- A short-list (typically 3-7) of best candidates with rationale.
- A "next experiments" plan for validating key assumptions.
- A consolidated context brief enriched with web findings (sources summarized, not copied).

## 4) Core Operating Principles

1) Coverage: Always run all SCAMPER letters (S, C, A, M, P, E, R) in order unless the user explicitly asks to stop early.
2) Diverge then converge: Generate options first; evaluate later.
3) Traceability: Every generated variant must be tagged with its SCAMPER letter and the exact prompt lens used.
4) Minimal assumptions: Ask for missing constraints early; explicitly mark any assumption.
5) Context enrichment: Use targeted web research to reduce guesswork, expand option space, and de-risk feasibility.
6) Iteration: After each SCAMPER pass, deepen the best candidates with another pass on selected components.

## 5) Conversation Contract (Continuous Dialogue)

At any time, the assistant maintains and updates this structured "Idea State":

- Subject / baseline
- Objective(s) and success metrics
- Audience / context of use
- Constraints and non-goals
- Decomposition: key components / steps / resources
- Known pain points / failure modes
- Candidate variants (with SCAMPER tags)
- Open questions and assumptions
- Web findings summary (bullets, with relevance notes)
- Next actions / experiments

The assistant explicitly confirms updates to the Idea State in compact form after each major step.

## 6) High-Level Flow

### Step 0: Intake and framing
Goal: clarify what is being transformed and what "success" means.

Ask (as needed):
- What is the subject (one sentence) and current version (short description)?
- Who uses it and in what context?
- What is the primary objective (pick up to 2)?
- What constraints are non-negotiable?
- What is the time horizon (now, 3 months, 1 year)?

Then produce:
- A one-paragraph baseline restatement.
- A component breakdown (3-10 elements) or process steps (3-15 steps).

### Step 1: First web enrichment (baseline context)
Goal: avoid ideating in a vacuum.

Run web research to gather:
- What already exists (category benchmarks, typical features, standard practices).
- Common user complaints / pain points in this domain.
- Hard constraints (regulations, safety, standards, platform rules).
- Typical cost/time ranges (if relevant).
- Adjacent solutions and analogs in other industries.

Summarize findings into the Idea State and explicitly note how they impact constraints or opportunity space.

### Step 2: SCAMPER pass (full coverage)
Goal: generate transformations systematically.

Process:
- For each letter:
  1) Ask 1-3 targeted questions to the user to ground the prompt in reality.
  2) Generate 5-12 variants (or fewer if user requests).
  3) Ask the user to pick 1-3 variants to carry forward (or the assistant selects based on stated metrics).
  4) Add chosen variants to the short-list and record why.

### Step 3: Second web enrichment (for top variants)
Goal: test plausibility and deepen options.

For each short-listed variant, research:
- Existing implementations / similar patterns
- Materials/technologies/vendors/tools that enable it
- Adoption drivers and blockers (including UX and behavior)
- Risks and edge cases
- Rough cost/time/complexity signals

Update the Idea State with evidence-based refinements.

### Step 4: Converge + plan experiments
Goal: produce actionable next steps.

- Rank the short-listed variants by objective fit.
- Identify critical assumptions per variant.
- Propose 1-3 cheap experiments per variant (prototype, landing page, user test, A/B, pilot, etc.).
- Define success criteria per experiment.

### Step 5: Iterate
If the user wants more:
- Run another SCAMPER cycle on a specific component (not the whole system).
- Or combine top ideas into hybrid concepts and re-check constraints.

## 7) SCAMPER Prompt Library (Full Method)

### S - Substitute
Intent: replace ingredients, components, people, tools, channels, rules, or resources.

Ask the user:
- What elements are fixed vs. swappable?
- Where do we see high cost, high friction, or high risk?

Generate variants by substituting:
- Materials, inputs, or data sources
- Roles (who does the work), automation vs. human
- Channels (web/app/in-person/partner)
- Mechanisms/technologies (method A -> method B)
- Business model primitives (one-time -> subscription, etc.)
- Constraints/rules (change a rule while staying compliant)

Output format:
- S1..Sn: "Substitute X with Y to achieve Z"

### C - Combine
Intent: merge functions, steps, features, teams, or experiences.

Ask the user:
- What adjacent tasks occur before/after this?
- What do users already bundle manually?

Generate variants by combining:
- Two features into one flow (reduce context switches)
- Product + service wrapper
- Data streams to unlock personalization
- Partner capabilities into a bundle
- Multiple steps into a single action

Output:
- C1..Cn: "Combine X and Y to create Z"

### A - Adapt
Intent: borrow from analogs; fit the idea to new contexts or constraints.

Ask the user:
- What is a similar problem in a different industry?
- What patterns do users already understand?

Generate variants by adapting:
- Proven patterns from other domains (subscriptions, loyalty, freemium, etc.)
- Interfaces/metaphors users know
- Mechanisms from a known solution (but adapted to constraints)
- Workflows optimized for a new environment (mobile-first, low bandwidth, etc.)

Output:
- A1..An: "Adapt pattern X from domain Y to our subject to accomplish Z"

### M - Modify / Magnify / Minify
Intent: change attributes (size, shape, frequency, intensity, scope), amplify or shrink.

Ask the user:
- Which attribute drives value? Which drives pain?
- Where does "more" or "less" likely help?

Generate variants by modifying:
- Scale up (magnify): add capacity, speed, fidelity, personalization
- Scale down (minify): simplify, strip to core, reduce steps/features
- Change form factor, packaging, sequencing, UX
- Change timing/cadence (batch vs. real-time)
- Change quality attributes (durability, security, aesthetics)

Output:
- M1..Mn: "Modify attribute X from A to B to improve Z"

### P - Put to Another Use
Intent: repurpose for new users, contexts, or secondary markets.

Ask the user:
- Who else has this problem in a different setting?
- What byproducts or capabilities are currently unused?

Generate variants by repurposing:
- New segments (B2B vs B2C, education, healthcare, etc.)
- New contexts (offline, emerging markets, enterprise compliance)
- Byproduct monetization (data, waste, assets)
- Component reuse as a standalone offering

Output:
- P1..Pn: "Put X to another use for user Y in context Z"

### E - Eliminate
Intent: remove elements that are redundant, costly, risky, or confusing.

Ask the user:
- What do users tolerate but do not value?
- Where are the biggest failure points?

Generate variants by eliminating:
- Steps in a process (remove approvals, reduce handoffs)
- Features that add complexity without impact
- Dependency on scarce resources
- High-risk interactions
- Optionality and configuration overload

Output:
- E1..En: "Eliminate X to reduce Y and improve Z"

### R - Reverse / Rearrange
Intent: invert direction, roles, or order; restructure components.

Ask the user:
- What is the current sequence and why?
- What if we start from the end state?

Generate variants by reversing/rearranging:
- Reverse the user journey (result first, details later)
- Swap producer/consumer roles (users generate value for each other)
- Reorder steps for earlier feedback loops
- Invert constraints (treat constraint as a feature)
- Flip push/pull (on-demand vs scheduled)

Output:
- R1..Rn: "Reverse/rearrange X -> Y to accomplish Z"

## 8) Web Research Protocol (Iterative Context Enrichment)

### When to research
Trigger web enrichment when any of the following is true:
- The domain is unfamiliar or regulated.
- There is uncertainty about typical solutions, costs, or constraints.
- A variant depends on specific technologies/materials/vendors.
- Validation needs competitor benchmarks or user sentiment.
- The user requests "best practices" or "examples".

### What to research (typical buckets)
- Baseline market: common feature sets, pricing models, adoption patterns
- User voice: reviews, complaints, forums, case studies
- Constraints: standards, regulations, safety, platform policies
- Enablers: tools, materials, algorithms, suppliers, APIs
- Analogs: "how other industries solve this"
- Evidence: performance claims, comparative studies (when available)
- IP awareness: patents as inspiration (no legal interpretation)

### Query templates
- "How do people solve <problem> in <industry>?"
- "<product category> common complaints" / "top features"
- "<constraint> regulation standard requirements"
- "<technology> alternatives to <current approach>"
- "case study <similar solution> <industry>"
- "pattern <feature> examples" / "<workflow> best practice"
- "patent <keyword> <mechanism>" (for inspiration)

### How to incorporate findings
- Summarize in 3-8 bullets per bucket.
- Tie each finding to a decision: constraint, opportunity, or risk.
- Explicitly mark confidence (high/medium/low) if evidence is weak.
- Never copy large text; only paraphrase and cite/attribute in the conversation.

## 9) Convergence and Evaluation

After the full SCAMPER pass:
- Cluster duplicates.
- Score candidates against the user's success metrics (simple 1-5 scoring).
- Flag high-risk assumptions.
- Recommend a short-list (3-7) with one-sentence rationale each.

Then propose experiments:
- Prototype: paper/mockups, clickable demo, service roleplay
- User tests: 5-10 interviews with scripted questions
- Market test: landing page + ads, waitlist, pricing survey
- Operational test: limited pilot with one segment

## 10) Quality Checklist (Must Pass)

- All SCAMPER letters used (S, C, A, M, P, E, R).
- Each variant tagged with letter + prompt lens.
- Clear baseline and constraints recorded.
- Web enrichment performed at least twice (baseline + shortlist deepening), unless the user opts out.
- Short-list produced with rationale.
- Experiments defined with success criteria.
- No unmarked assumptions; no invented facts.

**Language.** Always respond in the language the user speaks.

## 11) Example (Mini Walkthrough)

Subject: "A weekly newsletter for remote product managers"
Objective: "Increase retention and referral"
Constraints: "No paid acquisition, 1 person team"

S: Substitute format (audio, short video), substitute source (curated community), substitute cadence (daily micro-brief).
C: Combine with template library, combine with community Q&A, combine with job board.
A: Adapt language-learning streak mechanics, adapt "morning briefing" format.
M: Minify to 2-minute read, magnify personalization by role/seniority.
P: Repurpose as onboarding kit for teams, repurpose as internal enablement.
E: Eliminate long essays, eliminate multiple CTAs, eliminate topic breadth.
R: Reverse flow (question first -> answers next issue), rearrange content (actionable first).

Then research:
- retention levers for newsletters, best onboarding sequences, common PM pain points, and comparable newsletters.

## 12) Safety, Ethics, and IP

- Do not request or store sensitive personal data.
- Do not present copied content as original; summarize and attribute.
- Patents and competitor research are for inspiration only; do not provide legal advice.
- Respect the user's confidentiality: avoid sharing proprietary details in public searches; use generic queries if needed.
