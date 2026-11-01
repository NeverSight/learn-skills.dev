---
name: product-designer
description: Design a feature top-down for any project (problem, logic, process, UX, then UI), stopping after each layer to settle it with the user. Use when the user asks for product design, a five-layer design flow, or names product-designer.
disable-model-invocation: true
license: MIT
---

Design a feature the way a product designer does: the UI comes **last**. Work five **layers** in order, each one resting on the layers above it:

1. **Problem**: what's actually broken, and for whom.
2. **Logic**: rules, states, edge cases.
3. **Process**: who owns what, what happens when.
4. **UX**: flows and structure.
5. **UI**: screens, on whatever design surface this session can actually reach.

Each layer ends at a **gate**: post a summary of what you settled, then wait for the user to confirm it before you open the next layer. A question that belongs to a lower layer gets parked as an open question for that layer. When a lower layer exposes a flaw in a settled one, say so, reopen that layer, and re-gate it.

This skill works best with Matt Pocock's `grilling` skill ([mattpocock/skills](https://github.com/mattpocock/skills) — `npx skills add mattpocock/skills --skill grilling`). Use it on Layer 1 when it is available.

## Gate summary

Close every layer with this block, carrying forward everything settled so far so the latest gate is always the whole brief:

```
### ✅ Layer N settled: <name>

**Decided**
- <each decision, one line>

**Assumptions** (unverified, flag to confirm later)
- …

**Parked for later layers**
- Layer M: <question>

Confirm, or tell me what to change, and I'll open Layer N+1.
```

## Layer 1: Problem (grill)

Ground yourself in the project before the first question. Find its sources of truth and read the ones this feature touches:

- The docs index, README, or architecture doc the repo points agents at
- The domain glossary and any recorded decisions
- The relevant spec and plan, if they exist
- The ticket, if one is named

Look at what the product does today in this area: routes, entities, and the persona each surface serves.

Then stress-test the problem only: who hits it (persona, role, scope), what they do today instead, what breaks and how often, what evidence exists, and what "solved" looks like. A proposed solution is a symptom; trace it back to the need it serves. If a `grilling` or `grill-me` skill is available in this session, invoke it for that pass. If not, ask the same hard questions yourself — do not stall waiting for a grill skill.

Done when you can state the problem in one sentence, name the persona it hurts, and give the success measure, and the user agrees with all three. A conflict with a recorded product decision goes to the user as a new decision, never resolved silently.

## Layer 2: Logic

Grill the rules the feature lives by: the entities involved and their **states**, every transition and what triggers it, invariants that must always hold, and **edge cases** (empty, first-time, duplicate, concurrent edit, partial data, the reversal of every action). Reuse the project's glossary and existing domain models; name each new term explicitly.

Done when every state has its entry and exit transitions, and every edge case has an outcome. A state diagram or table in the gate summary is the check.

## Layer 3: Process

Map ownership and time: which persona or role performs each transition, who is notified, who approves, what runs automatically, and what happens when someone doesn't act. Tie each actor to this project's authorization model (roles, relations, scope, and any tenant or account boundary) and name each write the project already records, such as an audit event.

Done when every transition from Layer 2 has an owner, a trigger, and a permission.

## Layer 4: UX

Turn the process into flows: the entry point for each actor, the steps in each flow, the decision points, and where each flow lands on success, failure and cancel. Place each flow in the existing structure: which app or surface, which route, which existing page or feature it extends. Plan the empty, loading, error and permission-denied states.

Done when every flow runs from entry to an exit, and you have a list of the screens Layer 5 must draw, each with its states.

## Layer 5: UI

Draw the screens from the Layer 4 list. Build on the project's look: its design-system tokens and components (read that package's README, or the style source the repo treats as canonical), and every locale and writing direction the product already ships. Draw each screen in its main state, then the states Layer 4 named.

**Prefer Claude Design** when this session can use it (for example Claude's Artifact tool with `action: "quickstart"` and `intent: "design"`, then follow the instructions it returns). Say so in the gate summary.

If Claude Design is unavailable, or the user wants something else, offer **agent-agnostic** alternatives and use the best one they pick (or the best one available if they don't care):

1. A connected design tool the session can drive (for example Figma, or another design MCP / plugin already available).
2. A visual artifact the host supports (HTML/CSS prototype file, generated image, canvas, or similar).
3. Annotated wireframes in chat: layout, hierarchy, copy, and which design-system components each region uses — enough for a designer or implementer to build from.

Do not invent a tool that isn't there. If the user names a specific surface, use that when available. Always say which surface you used in the gate summary.

Done when every screen on the list is drawn (or wireframed) in every listed state, and the user has reviewed the design. Close with the final gate summary and offer the project's next spec step (for example a `/to-spec` skill, a ticket draft, or a written brief) if one exists.
