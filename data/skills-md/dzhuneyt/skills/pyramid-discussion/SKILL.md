---
name: pyramid-discussion
description: Facilitates a top-down pyramid discussion that calibrates the user's topic depth, then starts at high-level goals and progressively descends to concrete actionables, sharpening gaps and assumptions at each layer. Use when the user wants to break down a goal, explore a vision, elicit requirements, or mentions pyramid discussion, top-down planning, or progressive breakdown.
---

# Progressive Pyramid Discussion

Top-down elicitation: start at the apex (high-level goals), descend layer by layer, and end at concrete actionables (the base). Calibrate the user's depth on the topic first, then adapt pacing and scaffolding for the rest of the session.

**Task:** $ARGUMENTS

## Scope and stance

- **General-purpose** — product ideas, personal goals, project plans, org decisions; not software-specific.
- **Facilitator, not solver** — structure and questions; don't implement or over-recommend unless asked.
- **Not grill-me** — grill-me walks a decision tree and recommends answers; this skill follows fixed top-down layers and proposes structure for the user to refine.
- **Conversation artifact** — the final pyramid lives in chat unless the user asks for a file.

## Entry

- If `$ARGUMENTS` or the user's message includes a topic, reflect it back as a provisional Apex.
- If no topic, ask: "What high-level goal do you want to break down?"
- If resuming mid-session, state the current layer and what's already locked in; skip the depth probe if already calibrated.

## Depth calibration (before Layer 1)

Run once the topic is known. Goal: infer how deep the user's knowledge goes so the pyramid matches their level.

Ask all three probe questions in one turn, labeled by depth:

1. **Surface** — "In one sentence, what is [topic] to you?"
2. **Applied** — "What's one concrete challenge or decision you're facing with this?"
3. **Expert** — "What tradeoff or nuance do most people get wrong about [topic]?"

Infer a depth level from the answers (use internally — never announce a score or label):

| Level | Signals | How the pyramid adapts |
| --- | --- | --- |
| **Exploring** | Vague surface answer, can't name challenges, defers on expert question | More scaffolding; define terms; offer 2–3 pillar options to react to; slower pace |
| **Practicing** | Clear surface + real challenge, partial nuance | Balanced — propose structure, sharpen gaps, one-at-a-time on contentious points |
| **Deep** | Precise framing, names tradeoffs unprompted, challenges the probe | Skip basics; sharper, fewer questions; propose pillars/blocks as drafts for critique |

**Rules:**
- Keep probes short — calibration, not the pyramid itself.
- Contradictory answers (expert vocabulary, no applied experience) → lean **Practicing**; note the mismatch gently.
- User override ("I know this area well — skip the basics") → treat as **Deep**.
- Re-probe only if the topic pivots mid-session.

## The pyramid layers

Descend strictly one layer at a time. Do not jump to the base or ask for all details upfront.

| Layer | Purpose | Agent delivers |
| --- | --- | --- |
| **Apex** | Ultimate goal / vision | Restated goal, success criteria, explicit out-of-scope |
| **Pillars** | 2–4 strategic components | Named pillars + exposed assumptions |
| **Blocks** | Tactical requirements per pillar | Dependencies, edge cases, missing links |
| **Base** | Concrete actionables | Discrete tasks, each traceable upward |

**Per-layer exit criteria** — do not descend until:
- the user explicitly confirms alignment, OR
- you state "provisional — flag disagreements" and the user does not object.

### Layer 1: Apex

1. Reflect the goal back; sharpen boundaries — what does success look like? What is out of scope?
2. Run the sharpening protocol (below).
3. Confirm exit criteria before Layer 2.

### Layer 2: Pillars

1. Break the Apex into 2–4 pillars or strategic components.
2. Expose implicit assumptions and gaps within each pillar.
3. If sharpening reveals flaws in the Apex, stop and revise the Apex with the user.
4. Confirm exit criteria before Layer 3.

### Layer 3: Blocks

1. Deconstruct each pillar into tactical requirements, flows, or needs.
2. Look for missing links, edge cases, and cross-pillar dependencies.
3. Confirm exit criteria before Layer 4.

### Layer 4: Base

1. Translate tactical requirements into concrete, actionable steps.
2. Render the final pyramid summary (below).
3. Ask: "Anything to adjust before we close the pyramid?"

## Sharpening protocol

At every layer, explicitly surface:
- **Gaps** — what's undefined or hand-wavy
- **Assumptions** — what's being taken for granted
- **Conflicts** — tension between this layer and the one above

**Upward propagation:** if sharpening at Layer N invalidates Layer N−1, stop descending. State what changed, revise the upper layer with the user, re-confirm, then continue.

## Interaction pacing

Combine **depth level** (from probe) with **layer complexity**:

| Depth | Default pacing |
| --- | --- |
| Exploring | One question at a time; offer examples/options |
| Practicing | Layer draft + 2–4 sharpen questions; one-at-a-time for hot gaps |
| Deep | Layer draft + 1–2 pointed challenges; minimal hand-holding |

Within any depth level:
- **Simple / clear context** → batch questions OK
- **Contentious / high uncertainty** → one question at a time regardless of depth

Never ask more than 4 questions in a single turn (depth probe excepted — its 3 questions are fixed).

## Final pyramid summary

When Base is confirmed, render:

```markdown
## Pyramid: [topic]

### Apex
[one sentence goal + success criteria]

### Pillars
1. **[Pillar]** — [one line]
   - Assumption: …

### Blocks
- **[Pillar]** → [tactical items]

### Base (actionables)
- [ ] Task — supports [block/pillar]
```

## Anti-patterns

- Don't skip depth calibration (unless resuming or the user says they know the topic cold).
- Don't label the user "beginner" or "expert" out loud — adapt silently.
- Don't skip to implementation or code.
- Don't collapse layers (no tasks before pillars are agreed).
- Don't accept a vague apex ("make it better") without sharpening success criteria.
- Don't produce a pyramid when the user only wanted a quick answer — offer to exit early.
