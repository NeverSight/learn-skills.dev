---
name: feature-brainstorm
description: >
  Use this skill when brainstorming, designing, or planning any Swift feature. This is the
  right skill whenever the user describes a feature they want to build, asks "how should I
  implement X", wants to think through a design, or starts with something like "I want to
  add..." or "let's plan...". Use it even if they don't explicitly say "brainstorm" — if
  there's a feature to figure out, start here before touching any code.
---

# Feature Brainstorm

Your job is to help the human think through a Swift feature thoroughly — discovering its
shape, exploring the tricky parts, and surfacing a clear plan that respects scope. The goal
is insight before implementation.

**This is a structured conversation, not a monologue.** You move through phases, check in
with the human at each gate, and don't proceed until they give you the green light.

---

## The Flow

```
1. Frame
2. Decompose
3. Explore  ←──────────┐
4. Lessons Learned ────┘ (loop if new aspects surface)
5. Integrate
6. Scope
7. Plan
```

Phases 3 and 4 can loop: if Lessons Learned surfaces new aspects, go back to Explore for
those before continuing to Integrate.

---

## Phase 1: Frame

Start by making sure you understand the feature clearly. Ask clarifying questions if needed.
Your goal: one crisp statement that captures what this feature does and why it matters.

Articulate:
- What the feature does
- Who benefits and in what context
- What "done" looks like at a high level

**Gate:** Show your framing to the human. Ask if this captures it or if anything is off.
Wait for their confirmation before moving on.

---

## Phase 2: Decompose

Break the feature into its distinct aspects — the meaningful sub-problems that each deserve
their own attention. Think across layers like:
- State management
- Data model
- UI and user interaction
- Async behavior and concurrency
- Persistence
- Navigation
- Error handling
- External dependencies

Aim for 3–7 aspects. More usually means you're too granular; fewer might mean something's
being glossed over.

**Gate:** Present the aspects to the human with a sentence on why each matters. Let them
add, remove, or rename aspects before you proceed.

---

## Phase 3: Explore

Work through each aspect one at a time. For each:

1. State the core question this aspect raises
2. Explore at least two approaches or design options
3. Discuss trade-offs, risks, and unknowns
4. Reach a recommendation — or honestly flag it as unresolved
5. Log any ideas that surface but clearly belong to a different scope (don't chase them now)

Be specific to Swift. Think about `@Observable`, actors, `async/await`, SwiftUI state,
value vs reference types, protocol-based injection — whatever's genuinely relevant to this
aspect.

**Gate:** After finishing each aspect, briefly summarize the key finding and ask the human
if the direction feels right before moving to the next one.

---

## Phase 4: Lessons Learned

After exploring all aspects, step back and ask: **what did we discover that changes earlier
thinking?**

- Did exploring one aspect reveal assumptions worth revisiting in another?
- Did an early framing decision look different in hindsight?
- Are there aspects that should have been on the list from the start?

If new aspects surface here, loop back to Phase 3 and explore them. Update earlier findings
where needed. Be honest about reversals — "we assumed X, but actually Y" is more useful
than a plan that ignores what it learned about itself.

**Gate:** Present the lessons and any proposed revisions. Get the human's sign-off before
moving to integration.

---

## Phase 5: Integrate

Pull everything together into a coherent narrative:
- How do the pieces fit together?
- What are the key dependencies between aspects?
- What's the right order to build things, and why?
- What are the biggest remaining risks?

This should read like a design doc summary — clear enough that a developer could pick it up
and know what to build.

**Gate:** Show the integrated design to the human. Ask if anything feels incomplete or
wrong before scoping.

---

## Phase 6: Scope

Decide what's in and what's out for this implementation.

**In scope:** Everything needed for a solid, shippable version of the feature.

**Out of scope — save for later:** Good ideas that don't belong in this version. Log them
as "Future Ideas" — not discarded, just deferred. They'll be carried into the plan.

**Discarded:** Ideas that were explored and found to not add value, add disproportionate
complexity, or contradict the feature's purpose. A brief note on why is enough.

Be direct about cuts. A tight scope done well beats an ambitious scope done poorly.

**Gate:** Present the scope decision and reasoning. Let the human adjust it before
handing off to `writing-plans`.

---

## Phase 7: Hand Off to Planning

The brainstorm is complete. Now invoke the `writing-plans` skill, passing it everything
we've established:

- Feature summary and framing
- Design decisions and their rationale
- Architecture and dependency order
- Risks and open questions
- In-scope / out-of-scope / discarded decisions

The `writing-plans` skill takes this as its input and produces the implementation plan.
From there, `swift-tdd` handles execution.

Your role here is to be a good handoff — give `writing-plans` enough context that it
doesn't have to re-derive decisions already made. The brainstorm is the source of truth
for *what* to build and *why*; the plan is the source of truth for *how*.

---

## Ground Rules

**Check in at every gate.** Don't skip ahead. The human's input shapes the direction —
surprises at the end are expensive.

**Capture everything.** Out-of-scope ideas and discarded ideas both get documented.
Nothing gets silently dropped.

**Be concrete about Swift.** Generic design advice is less useful than specific guidance
about `@Observable`, actors, `async/await`, protocols, value vs reference types, and
SwiftUI state patterns.

**Prefer depth over breadth.** Thoroughly exploring four aspects beats skimming eight.
If the aspect list is long, offer to prioritize the ones with the most uncertainty first.

**Loop when it matters.** Lessons learned aren't a formality. If something genuinely
changes earlier thinking, go back and address it. A plan that ignores its own discoveries
isn't worth much.
