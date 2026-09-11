---
name: dont-make-me-think
description: Audita e reconstrói um fluxo ou tela para reduzir atrito e fricção de UX.
---

# Don't Make Me Think

Audit an existing journey, then rebuild it so the user never has to think. Three engines drive every decision:

1. **Clarity** (Krug/Nielsen) — every screen self-evident, one obvious next step.
2. **Simplicity** (Maeda/Tesler) — hide complexity until it's needed; the product absorbs it, never the user.
3. **Flow** (game-feel, calibrated) — clear goal, instant feedback, visible progress, celebrated wins. Never dark patterns.

**The unit of work is the JOURNEY (a flow), not the isolated screen.** Zoom into screens only after walking the flow end to end.

**Announce at start:** "Using dont-make-me-think to audit and rebuild [journey]."

## The Process — 3 phases, 1 gate

```
AUDIT ──► Friction Map ──► BLUEPRINT ──► 🚦 user approves? ──► REBUILD ──► re-run audit on result
                                              │ no
                                              ▼
                                        revise blueprint
```

### Phase 1 — AUDIT → Friction Map
Read `reference/audit.md` and follow it. Walk the journey in code AND live in the browser (Playwright) when a URL is reachable. Produce a prioritized Friction Map (P0–P3) with evidence. Do NOT propose fixes yet — this phase only collects friction.

### Phase 2 — BLUEPRINT → approval gate 🚦
Read `reference/clarity.md`, `reference/simplicity.md`, `reference/flow.md` (the three engines), then `reference/blueprint.md` (the output format). Rebuild the journey ON PAPER. Present the blueprint and STOP. Do not touch code until the user explicitly approves.

### Phase 3 — REBUILD → verified code
Implement the approved blueprint following the repo's existing patterns. Verify by RE-RUNNING the Phase 1 walkthrough and trunk test on the result — the audit is the acceptance test. Delegate purely visual work (palette, typography, ornament) to impeccable/frontend-design when it makes sense: dont-make-me-think owns the experience decision, not the pixels. Commit in atomic units per the repo's conventions.

## Surface calibration — declare it at the top of every blueprint

| Surface | Examples | Game-feel dose |
|---|---|---|
| **Serious tool** | admin panels, tax/finance, settings, internal dashboards | Fundamentals only: instant feedback, clear goal, visible progress, proper success state |
| **Consumer product** | e-commerce, SaaS, content apps, games' shell UI | Fundamentals + engineered peak-end, celebration on real wins, empty-state-as-level-1 |
| **Engagement app** | habit trackers, education, fitness, games | All of the above + hand off deep mechanics (XP, levels, quests) to the `gamification` skill |

Fundamentals apply ALWAYS — they are what makes any app feel good. Strong mechanics (streaks, variable rewards, levels) NEVER appear by default outside the third row. If the user explicitly asks to crank it up, move one row down.

## Red flags — stop and reconsider

| Thought | Reality |
|---|---|
| "I'll just fix this one screen" | The journey is the unit. Walk the flow first. |
| "Users will read this explanation" | Nobody reads. Redesign until no instructions are needed. |
| "One more option won't hurt" | Every option is a decision tax (Hick's Law). The burden of proof is on adding. |
| "A tutorial carousel will fix onboarding" | Teach just-in-time, at first contact with each feature. |
| "A streak/badge would spice this up" | Wrong row in the calibration table = dark pattern. |
| "The user can configure it" | That's the user absorbing complexity. Absorb it with a smart default instead (Tesler). |
| "It's fine, it's consistent with the rest" | Clarity trumps consistency. |
| "Fewer clicks is always better" | Certainty per click beats click count. Three mindless clicks beat one confusing mega-screen. |
| "Skipping the gate, the fix is obvious" | The blueprint gate is mandatory. Present, then wait. |
