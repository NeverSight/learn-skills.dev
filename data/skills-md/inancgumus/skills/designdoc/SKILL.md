---
name: designdoc
description: Write or rewrite internal technical design docs, RFCs, and proposal docs so a reader with no prior context can quickly understand the problem, the options, the tradeoffs, and the recommendation. Use when drafting a new design doc, restructuring a weak one, comparing proposals, or reviewing a doc that reads like a story instead of a design. Also use when the user mentions RFC, design review, architecture proposal, or ADR.
---

# Write design doc

A design document is a technical report that outlines the implementation strategy of a system in the context of trade-offs and constraints.

The goal is the same as a mathematical proof: convince the reader that the design is the right choice given the situation. The most important reader is the author. Writing adds rigor to vague intuitions. Code will later show how sloppy the writing was.

Someone who knows nothing about the problem reads this. By the end, the solution should feel inevitable. If the proposal is a surprise, the earlier sections failed.

Every design doc must follow the structure in [references/design-doc-template.md](references/design-doc-template.md). Read it before writing. Use its exact heading order and metadata table. If the user's team has a different template, use theirs instead, but never invent a structure from scratch.

Read [references/writing-principles.md](references/writing-principles.md) for prose quality rules. Read [references/company-templates.md](references/company-templates.md) if the user asks for a specific company's RFC format.

## Organization

Think of the doc as a series of bullet points that flow into each other:

- Observation A
- Observation B
- Because B, idea C
- But problems D and E
- Observation F
- Therefore idea G
- And improvement H

Each bullet is a paragraph. Each paragraph can be compressed to one sentence in the reader's memory. This matters because readers juggle finite items in short-term memory.

The reader should never be surprised. Every sentence flows from the previous ones. You anticipate every objection someone would have and show why it fails before the reader thinks to raise it.

This requires modeling the reader's mind. You need to know their starting state (what they already know, what they assume, what they fear) and guide them to the destination state (belief that the design works).

Many engineers get this wrong by assuming readers share their context. A reader from another team opens the doc cold. They need the product situation before any technical detail.

## The three-layer onion

Each layer justifies the next. The problem justifies the goals. The goals justify the proposals. The proposals justify the tradeoffs. A gap in an early layer cannot be fixed by good writing in a later one. A fatal flaw in any layer makes the rest irrelevant.

**Layer 1: Problem, goals, non-goals, requirements.** Functional and non-functional. Identify stakeholders. Describe the current situation so everyone sees the same thing. If the problem is misunderstood, the design is wrong.

**Layer 2: Functional specification.** How the system works from an external perspective. What users see and do. List alternative solutions considered and why they were rejected. If this layer does not meet the requirements, implementation details are irrelevant.

**Layer 3: Technical specification.** The internals. How the design gets implemented. The choice reasoning matters more than the choice itself. This layer can change during implementation. That is fine. The first two layers anchor the project.

## Workflow

### 1. Find the decision

State the choice in one or two plain sentences.

Write it as a neutral fork. A cold reader should see real options, not a disguised recommendation.

If the choice is muddy, answer these first:

- What problem needs a decision?
- What options are on the table?
- What changes for users under each option?

### 2. Set the reader up (Background)

Background prepares the reader for the rest of the doc. Nothing else.

Put the product situation first. Why do users do this? What does this feature do today? What terms will appear later?

Define every term the rest of the doc relies on. Define each term once in a natural sentence, then use it consistently. A reader outside the team should follow without looking anything up.

Do not put problems, tradeoffs, or arguments in Background. Do not dump history. Do not write a glossary. Show concepts through examples when you can.

### 3. State the problem

Before arguing that something should change, show what happens today. What does someone do, what do they expect, and what actually happens? The problem section should leave a reader uncomfortable with the status quo. If it does not, the proposals feel like solutions looking for a problem.

State the current behavior first. Then state why that behavior is a problem for users or teams. Say what happens, to whom, and what it costs. Do not explain a system's internals and leave the "so what" as an exercise.

Separate current facts from product intent and proposal behavior. Mark each clearly.

Show the problem with concrete artifacts: the current command, config, script, or flow, then say what breaks.

### 4. Separate goals from non-goals

Goals are decision criteria. A reader should test every proposal against the same goals.

Write goals as user-visible outcomes or product constraints, not as the chosen proposal in disguise.

Non-goals are things that could reasonably be goals but the team chose to exclude. They bound the solution space. Without them, the solution space overwhelms. ("In IT, it's all virtual, so in theory anything is possible. Setting hard limits is necessary.")

### 5. Write proposals as behavior

Each proposal proposes one thing. No hedging with "could do X or Y." Pick a concrete behavior.

For each proposal:

1. Open with the behavior itself. The heading already says "Proposal N." Use the first sentence for what happens.
2. State what the proposal preserves, what it changes, and what happens in the main cases.
3. Put Pros and Cons right after.
4. Put examples after Pros and Cons.

Proposal 0: do nothing. Describe what stays the same and how the problem continues or grows.

Make each proposal self-contained. A reader should understand it without following an issue link, a prototype branch, or a stakeholder quote.

Write pros and cons as concrete product, business, or user impact. Say who benefits or pays the cost, and what changes for them. Be specific.

Good:
- "Users stay logged in during infrastructure outages because tokens validate locally."
- "The ops team stops getting paged for poll-related DB alerts."
- "Customers behind corporate NATs are not penalized because limits are per API key, not per IP."

Weak:
- "Token validation is stateless."
- "It is easy to explain."
- "No Redis dependency."

The weak versions describe system properties. The good versions say what those properties mean for someone. A reader skimming pros and cons should understand the tradeoff without reading the proposal text.

When proposals share a dimension (latency, cost, migration effort, reliability), write the pro or con so it shows where this proposal sits relative to the others. A reader comparing proposals should see the tradeoff directly, not piece it together across sections.

### 6. Alternatives considered

One of the most important sections. For each rejected alternative, explain the trade-offs that led to the selected design. The act of choosing among possibilities is what makes it a design. The doc should lay out the choices made, and sometimes the choices not made, and why.

### 7. End with the decision

State which proposal is recommended, why it wins, and what tradeoff the team accepts.

If the doc is open, say what remains unresolved and what input is needed.

Do not recap the whole doc.

## Diagrams

Use diagrams. Engineers have used drawings for millennia. Software developers underuse them.

A system-context diagram, a sequence diagram, or a simple box-and-arrow sketch can make the architecture obvious where prose takes paragraphs.

Include diagrams for: system architecture, component relationships, data flow, state transitions, API interactions. Use Mermaid, ASCII art, or describe the diagram for the author to create.

## Fair comparison

Give each proposal a fair shot.

Keep Background, Problem, and Goals proposal-neutral. They set up the decision. They do not pick the winner in advance.

If one proposal wins most comparison points, check whether the losing proposal is in its strongest form. A lopsided comparison often means one side was strawmanned.

If you recommend a proposal, own it in the recommendation section. If you present options for alignment, make the tradeoffs real on both sides.

## Scope

Focus on user-visible behavior and cross-team alignment.

Include implementation detail only when it changes user behavior, product meaning, or team alignment.

Good design-doc detail: user-visible behavior, compatibility rules, flag interactions, limits that affect whether the design is acceptable.

Cut unless it matters to the decision: internal function names, prototype quirks, output formatting trivia, details that only matter to the implementor.

Complex calculations, simulations, and detailed analyses belong in an appendix. The main doc should stand on its own for understanding conclusions. The appendix is for readers who want to check your work.

## Editing

Remove every word that can be removed. Readers' attention is scarce. Unless you are an unusually terse writer, you can cut ~30% from a first draft without losing information.

Ask two questions about each section:

1. "Will this get bikeshedded?" If yes, and it matters, strengthen the argument. If yes and it does not matter, cut it or move it to an appendix.
2. "So what?" Read each statement from the reader's perspective. Does it help them make a better decision? If not, cut it.

## Review pass

Before delivering, check:

- Can a cold reader explain the problem after the first two sections?
- Do Background and Problem each do their own job?
- Do the goals read as decision criteria, not one proposal in disguise?
- Does each proposal say what happens?
- Does each proposal explain itself without outside links?
- Are pros and cons concrete effects, not judgments?
- Does each proposal propose one thing?
- Do examples make comparison easy where it matters?
- Is the comparison fair?
- Does any section repeat another section?
- Does the doc stay on behavior, not implementation?
- Does the recommendation make a choice, not restate the options?
- Are all technical terms defined before first use?
- Would someone outside the team follow without looking anything up?
- Are claims validated or labeled as product intent?
