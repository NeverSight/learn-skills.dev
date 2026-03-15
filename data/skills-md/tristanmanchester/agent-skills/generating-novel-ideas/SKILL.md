---
name: generating-novel-ideas
description: "Generates genuinely novel, useful ideas for products, businesses, features, campaigns, names, research directions, and process redesign. Use when the user asks to brainstorm, ideate, improve a weak concept, escape generic answers, find differentiated options under real constraints, or turn a vague opportunity into a shortlist of strong concepts with wedges and tests. Preserves diversity with independent idea pools, analogy transfer, contradiction solving, critique-and-repair, and reality checks. Do not use for simple rewriting, proofreading, or purely factual research."
compatibility: "No required external tools. Optional web access improves grounding. Optional Python 3 enables scripts/diversity_audit.py for large raw idea sets."
metadata:
  author: OpenAI
  version: "2.0.0"
  category: creativity
  tags: ideation, brainstorming, innovation, strategy, research
---

# Generating Novel Ideas

This skill turns ideation into a search process, not a list-making exercise. The job is to
discover a portfolio of distinct, high-potential concepts, not ten polished variations
of the first plausible answer.

## Critical rules

- Fight collapse. LLMs drift towards fluent sameness. Use independent idea pools before
  comparing ideas.
- Prefer concrete mechanisms over vibes. Every finalist needs a sharp twist, an entry
  wedge, and a cheap test.
- Separate divergence from judgement. Do not score too early.
- Use ordinary stakeholder or practitioner perspectives when using personas. Do not
  imitate celebrity innovators.
- Research late enough to preserve breadth, but early enough to kill obvious
  reinventions before the final recommendation.
- Final outputs should usually be a portfolio with spread across mechanism, audience,
  and risk, unless the user explicitly asks for a single winner.

## Internal roles

Run these roles in sequence. Keep them separate until synthesis.

1. Explorers widen the search space.
2. Critics attack weak, generic, or unrealistic ideas.
3. The synthesiser assembles the final portfolio.

Do not let the critic appear too early. Do not let the synthesiser merge everything into
one blurry compromise.

## Default workflow

1. Build an opportunity model
2. Partition the search space
3. Generate independent idea pools
4. Run an analogy transfer pass
5. Resolve key contradictions
6. Audit diversity and regenerate missing directions
7. Critique and repair finalists
8. Ground against reality
9. Present a portfolio and experiments

## Step 1: Build an opportunity model

Capture the minimum useful brief:

- User goal
- Target user or audience
- Current status quo and what is frustrating, expensive, risky, slow, or emotionally flat
- Hard constraints
- Success criteria
- Available assets, unfair advantages, channels, or capabilities
- Hidden tensions and trade-offs
- What to avoid

When the prompt is sparse, infer reasonable assumptions and state them briefly.

When the user brings an existing idea, do not start by polishing it directly. First
extract the underlying job and generate at least two alternative mechanisms.

## Step 2: Partition the search space

Choose 3 to 5 independent pools. Pools must differ on at least two axes.

Good axes include:

- stakeholder viewpoint or ordinary persona
- mechanism or value type
- user moment or time horizon
- adoption path or channel
- ambition level
- trust model or ownership model

Examples of useful pool labels:

- frontline operator, zero new habit
- approver or buyer, proof and risk reduction
- novice user, immediate win
- partner or embedded channel
- bold long-shot system shift

Rules:

- Generate each pool as if it has not seen the others.
- Do not compare, deduplicate, or score until all pools are finished.
- Produce 2 to 4 ideas per pool.
- Keep raw ideas short at first: name, one-line concept, primary user, non-obvious move.

This blind partitioning is the main defence against idea collapse.

## Step 3: Generate the pools

Inside each pool:

1. Write 2 to 3 fertile reframing questions.
2. Choose two lenses from `references/LENSES.md`.
3. Generate the first pass.
4. Do a second internal pass and add at least one idea clearly outside the dominant
   pattern.

Always include one practical lens and one novelty lens.

If the task is complex, breadth comes before depth. Add new mechanism families before
expanding any single family.

## Step 4: Run an analogy transfer pass

Do not borrow surface style. Borrow mechanism.

1. Abstract the problem into a mechanism, tension, or pattern.
2. Pick 2 to 4 distant domains.
3. Extract what makes those domains work.
4. Map the mechanism back into the problem.
5. Adapt it for the actual constraints and adoption path.

Every strong final set should contain at least one idea born from far analogy, unless the
user explicitly wants only safe, incremental options.

For source domains and transfer patterns, use `references/LENSES.md`.

## Step 5: Resolve key contradictions

Write 1 to 3 contradictions at the heart of the task, such as:

- more trust with less friction
- more customisation with less complexity
- more quality with less expert labour
- faster decision-making with lower risk
- more compliance with less manual work

Generate ideas that resolve the contradiction through separation, defaults, staging,
guarantees, modularity, reversible commitment, human review only at critical moments, or
new ownership boundaries.

For technical, scientific, or engineering prompts, use the structured contradiction
method in `references/LENSES.md`.

## Step 6: Audit diversity

Before refinement, check for hidden sameness.

Look for:

- near-duplicates hidden by new wording
- too many ideas using the same mechanism
- too many aimed at the same user moment
- repeated crutches such as AI assistant, dashboard, marketplace, community,
  gamification, personalisation, subscription, or platform
- no spread across pragmatic wedge, strategic differentiator, and bold bet

If the set is clustered, regenerate only the missing directions.

When scripts can run and the set is large, optionally use
`scripts/diversity_audit.py` before convergence.

## Step 7: Critique and repair finalists

Choose 3 to 6 finalists. For each one, write:

- strongest reason it could work
- smartest sceptic objection
- repair if possible
- kill it if repair makes it generic or unrealistic

Every finalist card should contain:

- Name
- One-sentence pitch
- Who it is for
- Hidden insight or tension
- Imported mechanism or pattern
- Why it is not just the obvious solution
- Entry wedge
- Main risk
- Cheapest disconfirming test

## Step 8: Ground against reality

If current market, technical, cultural, or regulatory reality matters and research is
available:

- check whether the idea is already common
- identify incumbents or substitutes
- pressure-test feasibility and compliance
- sharpen the why-now and distribution story
- trim false differentiation claims

Do not research so early that the search space collapses into existing categories.

## Step 9: Present the result

Default response structure:

1. Working brief and assumptions
2. Opportunity tensions
3. Search partitions used
4. Raw idea families
5. Final portfolio
6. Recommended next move

Use a portfolio, not just a ranking:

- one pragmatic wedge
- one strategic differentiator
- one bold bet

If the user asks for a single winner, still mention the strongest runner-up and the
specific reason it lost.

## Hard quality bar

No finalist is complete without:

- a clear non-obvious move
- a believable first user and first context
- a path to adoption or distribution
- a cheap test that could disconfirm it
- an explicit line in this format:

This is not just X. The new move is Y.

If Y is vague, decorative, or generic, the concept is not ready.

For the detailed rubric, use `references/EVALUATION.md`.

## Anti-generic rules

- Do not produce a flat list of features around one core mechanism and call it
  diversity.
- Do not hide weak ideas behind fluent prose.
- Do not use AI, agent, community, marketplace, dashboard, platform,
  personalisation, or gamification as decoration.
- Do not let naming replace concept work.
- Do not overvalue novelty with no adoption path.
- Do not overvalue feasibility when the idea is indistinguishable from existing
  practice.
- Prefer specific trade-offs to magical wins on every dimension.

## Mode switching

For domain-specific workflows, use `references/MODES.md`.

Common modes:

- startup or product opportunity
- research hypothesis or scientific idea
- campaign, content, or creative concept
- naming and verbal concept development
- process, service, or operations redesign

## Common failure modes

If the outputs feel generic:

- widen the partitions
- add a stronger far-analogy pass
- write sharper contradictions
- regenerate only missing mechanism families

If the outputs feel clever but unusable:

- reduce ambition by one step
- sharpen the first user and first context
- attach a cheaper test and a narrower wedge

If the outputs all sound similar:

- stop scoring
- restart with blind pools from new viewpoints
- avoid celebrity personas and vague mission statements

## Examples

### Example 1
User says: I need fresh B2B SaaS ideas for compliance teams.

Actions:
1. Build an opportunity model around buyers, blockers, trust, procurement, and audit.
2. Partition by operator, approver, audit trail, and partner channel.
3. Generate blind pools, then run analogy and contradiction passes.
4. Return a portfolio with wedge, differentiator, bold bet, and tests.

### Example 2
User says: This startup idea feels generic. Make it genuinely better.

Actions:
1. Extract the underlying job from the current idea.
2. Generate at least two alternative mechanisms before improving the original.
3. Keep only ideas with sharper wedges and clearer tests.

### Example 3
User says: Help me come up with novel research directions in battery diagnostics.

Actions:
1. Build tensions, constraints, missing capabilities, and evidence limits.
2. Use scientific mode from `references/MODES.md`.
3. Add structured contradiction solving and feasibility pressure-testing.

For trigger tests and maintenance checks, use `references/VALIDATION.md`.
