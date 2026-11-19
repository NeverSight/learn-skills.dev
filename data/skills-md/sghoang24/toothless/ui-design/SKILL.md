---
name: ui-design
description: "You MUST use this in the Design phase whenever a spec has a UI, AFTER the spec is agreed and BEFORE planning and any implementation. The goal is to turn the spec into the screens, flows, states, and a visual direction, mocked as static HTML in Lavish for the user to annotate. You are not allowed to write product code. Skip it for a spec with no user-facing surface and say so. Trigger phrases: ui design, ux, screen design, mockup, wireframe, user flow, design system."
argument-hint: "Point at the agreed spec, e.g. specs/001-auth/2026-11-12-auth.md"
---

# UI Design

`system-design` decides _how the pieces fit together_; UI design decides _what the user sees and does_. It is the other half of the Design phase: system design answers the system, UI design answers the screen. It runs when a spec has a user interface — a CLI tool or a headless service has none, and skips it.

**Self-contained.** Use it whenever a UI needs designing, whether or not `fight` is driving; `fight` (via `system-design`) simply calls it when it's active.

**No product code.** The output is a design and a static mock, not components wired into the app. The `<HARD-GATE>` from brainstorming still holds: nothing is built until the design is approved.

## The Model

| Thing             | What it is                                                    | Where it lives                      |
| ----------------- | ------------------------------------------------------------- | ----------------------------------- |
| **Spec**          | Agreed requirements. The _what_ the UI must serve.            | `specs/NNN-slug/YYYY-MM-DD-*.md`    |
| **Screens**       | The surfaces the user sees.                                   | named in the design                 |
| **Flows**         | The paths between screens for a user goal.                    | named in the design                 |
| **Design system** | The visual direction — style, palette, type, spacing, states. | `docs/design/`                      |
| **Mock**          | A static HTML page showing a screen, for review only.         | `docs/design/` or a Lavish artifact |

## When to Use

- The Design phase of a spec that has a user interface (web, mobile, desktop, or a TUI).
- The user asks to "design the interface", "mock this up", "show me how it looks", or "define the design system".

**Do NOT use** for a spec with no user-facing surface (CLI without a UI, headless service, data pipeline) — skip it and say so. Do not use it to **implement** the UI: that is the loop's `implement`, after the design is agreed.

## Core Rules

- **Design from the spec, not from taste.** Every screen and flow traces to a requirement. A screen no requirement asks for is speculative — cut it, or send the requirement gap back to brainstorming.
- **Mocks are static and throwaway.** HTML that shows the design. It is reviewed, not merged into the app. No real code in the Design phase.
- **Reuse, don't fork the visual language.** If the project has an existing design system or tokens, extend it. Only define a new one when there is none, and say so.
- **Reconcile with the system design.** The screens depend on the interfaces system design defined. Whatever data a screen needs must exist in a contract; feed the gap back before agreeing either.
- **Right-size the design.** A one-screen tool does not need a full design system. Match the depth to the spec, like `system-design` does.
- **Always show it and wait.** Every UI design goes through the Lavish review. A screen the user never saw is not agreed.
- **Design intelligence is a tool, not a dependency.** Use the `ui-ux-pro-max` skill when it's installed; fall back to plain design reasoning when it isn't, and say which you used.

## Procedure

### 1. Load the spec, roadmap position, and system design

Read the newest spec revision and its acceptance criteria, the feature's place in `specs/_roadmap.md` + `specs/_state.md`, and the parts of `docs/architecture/architecture.md` the screens touch. List the user-facing features and, for each, what the user is trying to do. Read any existing `docs/design/` and design tokens so you extend, not fork.

### 2. Decide the design scope

Name the screens and the flows between them that the spec requires — no more. State whether this is a light touch (a screen or two, reuse the existing look) or a full design (several flows, a new design system). Say which and why.

### 3. Get the visual direction (use ui-ux-pro-max if installed)

If the `ui-ux-pro-max` skill is available, use it in **design-system mode** to derive the visual direction from the product type:

```bash
python3 ~/.agents/skills/ui-ux-pro-max/scripts/search.py "<product type> <industry> <keywords>" --design-system -p "<App>"
```

That returns the style, palette, typography, layout pattern, anti-patterns, and a pre-delivery checklist. **Do not let it generate components** — take the guidance, not code. If it isn't installed, derive the direction with plain reasoning and record the choice.

To install it, use the `find-skills` skill (or `npx skills find ui-ux-pro-max`, then `npx skills add <owner/repo@skill>`).

### 4. Draft the design

Write the design to `docs/design/`: the screens, their states (empty, loading, error, success), the flows between them, and the design system (tokens, components, interaction states). Note which decisions are hard to reverse (information architecture, a new token system) versus reversible.

### 5. Mock the screens (static HTML)

Produce a **static HTML mock** for the key screens — no framework, no product code, no data wiring. It shows the design so the user can picture it. One file per screen, or a single file with all screens.

### 6. Review with Lavish (always)

Open the mock with the **`lavish`** skill so the user can annotate elements and send feedback. Show the screens, the flows, the design system, and the states. This is **not optional**. Then **listen**: run `lavish-axi poll <html-file>` and keep it in the **foreground** — it stays silent until the user sends feedback or ends the session. Don't end your turn or kill the poll while they review (the browser then shows "Your agent is not listening"). **Answer back**: after handling the feedback, run `lavish-axi reply <html-file> --agent-reply "..."` so the board stops showing `Working` and the notes are marked Done (or fold both into `lavish-axi poll <html-file> --agent-reply "..."` to reply and keep listening). Fold the feedback back in and repeat only while it's still changing the design.

### 7. Reconcile with the system design

Before either design is agreed, check them against each other: does every screen's data need map to an interface in `docs/architecture/architecture.md`? Feed gaps back into the system design. UI and interfaces are agreed together, not separately.

### 8. Gate

Stop at the design. Hand off to Plan only after `docs/design/` reflects the agreed UI and the mock has been reviewed — then `planning` cuts it into tasks. Update the feature's `specs/NNN-slug/status.md` (`next`, `notes`).

## Red Flags

| Thought                                         | Reality                                                                                                       |
| ----------------------------------------------- | ------------------------------------------------------------------------------------------------------------- |
| "Let me build the components, it's faster"      | No product code in Design. That's `implement`, after the gate.                                                |
| "I'll invent a new design system"               | Reuse the project's tokens unless there's none. Forking the language is a defect.                             |
| "The mock is a prototype, I'll wire it up"      | Mocks are static and throwaway. Wiring it up is a new task through the gate.                                  |
| "I'll design every screen I can imagine"        | Only the screens the spec requires. The rest is speculative.                                                  |
| "UI and architecture can be designed apart"     | Screens depend on contracts. Reconcile them, or you'll build to a shape that doesn't exist.                   |
| "The user saw it in a screenshot, that counts"  | Shown ≠ reviewed. Put it in Lavish so they can annotate, and wait.                                            |
| "I opened the Lavish mock, my job's done"       | Opened ≠ listening. Run `lavish-axi poll` (foreground) and keep it alive until they send feedback.            |
| "I handled the feedback, so I'm done"           | Handled ≠ replied. Run `lavish-axi reply` (or re-poll with `--agent-reply`) or the board sticks on `Working`. |
| "ui-ux-pro-max isn't installed, so I'm blocked" | It's a tool, not a dependency. Fall back to plain design reasoning and say so.                                |

## Completion Check

UI design is done when ALL are true:

- [ ] Every screen and flow traces to a spec requirement; nothing speculative.
- [ ] A design scope was stated (light touch vs. full design) and matches the spec.
- [ ] The visual direction was derived (via `ui-ux-pro-max` if installed, else plain reasoning, and it's recorded which).
- [ ] `docs/design/` holds the screens, states, flows, and design system; existing tokens extended, not forked.
- [ ] Static HTML mocks were reviewed in Lavish and the feedback was folded in (the poll was kept alive until they answered, and you replied so the board isn't stuck on `Working`).
- [ ] The design was reconciled with `docs/architecture/architecture.md` — every screen's data need maps to a contract.
- [ ] No product code was written; the feature's `specs/NNN-slug/status.md` updated.

If any box is unchecked, keep designing — do not start planning or building.
