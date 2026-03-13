---
name: incremental-plan
description: Break a product or feature spec into a sequence of small, independently testable implementation steps. Use when the user has a spec document and wants to implement it incrementally rather than all at once — building and verifying one piece at a time before moving on. Triggers on requests like "break this spec into steps", "create an incremental plan", "split this into parts I can test", "how should I implement this step by step", "create a build plan", or when a user has a spec and wants a phased implementation approach.
---

# Incremental Plan

Break a spec into 2-4 big steps that each deliver a working, end-to-end slice of the product.

## Why

A big spec implemented in one pass is hard to debug and course-correct. But splitting it into too many tiny steps (DB schema, page shell, config inputs, etc.) creates busywork — each step is too small to be meaningful on its own and the plan becomes a rigid checklist instead of a useful guide. The sweet spot is 2-4 substantial steps where each one produces something a user can actually try.

## Workflow

### 1. Read the Spec

Read the spec document the user provides. Identify:

- The core mechanism (the fundamental thing that makes the product work)
- The distinct technical layers (e.g., backend service, database, frontend UI, external integrations, auth)
- Dependencies between features (what requires what)

### 2. Ask Clarifying Questions (if needed)

Usually the spec has everything needed. But ask if:

- The spec doesn't mention what's already built (greenfield vs. adding to existing product)
- It's unclear which parts the user considers highest-risk or most uncertain
- There are multiple valid orderings and the user might have a preference

Keep this light — 1-2 questions max. This is not an interview.

### 3. Decompose into Steps

Split the spec into **2-4 big steps**. Each step should deliver a complete, working vertical slice — schema, server logic, UI, and wiring all included. The user should be able to use the result of each step, not just inspect plumbing.

**Splitting principles:**

- **Target 2-4 total steps.** This is the hard constraint. If you have more than 4 steps, merge related ones. A step can (and should) be substantial — it's fine for a single step to touch DB schema, server actions, UI components, and wiring if they all serve one cohesive goal.

- **Each step = a usable vertical slice.** Step 1 should be "the basic thing works end-to-end" — schema, page, UI, server logic, the whole path from user action to visible result. Not "set up the schema" followed by "build the shell" followed by "add inputs" followed by "wire it up". All of that is one step: "basic end-to-end flow works."

- **Never make a step that only sets up plumbing.** DB schema alone is not a step. A page shell alone is not a step. Config inputs that don't do anything are not a step. These are implementation details within a step, not steps themselves.

- **After the core works, expand in big chunks.** Step 2+ should each add a substantial set of related capabilities. Group features by user workflow, not by technical layer. For example, "multi-model generation + batch controls + result card actions" is one step, not three.

- **Defer auth, polish, and edge cases** to later steps — but still merge them into bigger chunks rather than giving each its own step.

- **Each step must be testable by a human.** Every step ends with something the engineer can manually use and verify end-to-end.

**Typical shape (adapt to the specific spec):**

1. **Core end-to-end** — the basic thing works: schema + UI + server logic + wiring, minimal but functional
2. **Power features** — multi-select, batch operations, advanced controls, card actions — everything that makes it actually useful
3. **Persistence + history** — if applicable, load from DB on refresh, filters, presets
4. **Secondary mode or polish** — e.g. video support if the core was images, or a second major workflow

Most specs will need 2-3 steps. Only use 4 if there's a genuinely separate mode or workflow.

### 4. Write the Plan

Write the plan to `plan-<spec-name>.md` in the same directory as the spec.

**Format for each step:**

```markdown
## Step N: [Short Title]

**Goal:** One sentence — what this step achieves.

**Build:**

- Concrete list of what to implement
- Specific enough that an AI coding agent or engineer could start working from this

**Scope cutoffs:**

- What's intentionally deferred, stubbed, or hardcoded in this step
- Prevents scope creep and makes it clear what "done" means for this step

**Verify:**

- Concrete actions the engineer takes to confirm this step works
- "Start the server, open localhost:3000, you should see X"
- "Run this curl command, expect Y response"
- "Click the button, observe Z"

**Spec coverage:** Which sections/features of the original spec this step addresses (by name or reference).
```

**Plan structure:**

```markdown
# [Product/Feature Name] — Incremental Build Plan

**Source spec:** `<filename>`

**Overview:** 1-2 sentences on the overall approach — why the steps are ordered this way.

**Steps at a glance:**

1. [Step 1 title] — [one-line summary]
2. [Step 2 title] — [one-line summary]
   ...

---

## Step 1: [Title]

[full step detail]

## Step 2: [Title]

[full step detail]

...

---

> Step boundaries may shift during implementation — the point is a clear path, not a rigid checklist. If a feature fits better in an adjacent step, move it.
>
> After completing each step, write a short handoff doc noting what was built, any manual steps required (e.g. run migrations, set env vars), manual tests to verify, and what the next step expects. This makes it easy to resume in a new session.
```

## Key Principles

1. **2-4 steps, no more.** This is the most important rule. If you find yourself writing step 5, stop and merge.
2. **Vertical slices, not horizontal layers.** Every step cuts through the full stack. No step should be "just schema" or "just UI" — each one delivers a working feature the user can try.
3. **Err on the side of bigger steps.** When unsure whether to split, don't. A meaty step that delivers a lot is better than several thin steps that each do a little.
4. **Stay at the right altitude.** The plan describes _what_ to build per step, not _how_ to implement it line by line. Leave implementation details to the engineer or coding agent. But be specific enough about scope and boundaries that there's no ambiguity about what's in vs. out.
5. **No orphan steps.** Every step must produce something usable. If a step exists only to "set up" the next step with no way to use it alone, merge it into the next step.
6. **The plan is a guide, not a contract.** Note in the document that step boundaries may shift during implementation — the point is to provide a clear path, not a rigid checklist.
