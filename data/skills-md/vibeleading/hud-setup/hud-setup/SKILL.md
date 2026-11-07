---
name: hud-setup
description: Design and calibrate the Vibe Leading Scoreboard HUD (Heads-Up Display) with IRA thresholds and Circuit Delta targets. Use when a leader/team wants to replace status meetings with real-time telemetry, or when defining what "winning" looks like for an AI-assisted squad.
version: 0.1.0
license: MIT
---

# HUD Setup

The scoreboard replaces the 30-minute status meeting. The Pilot does not manage by the clock; the Pilot leads by the Scoreboard.

> Source: "Vibe Leading The AI: The Corporate Race Against Machines" (Jean Machuca). Framework concept: the Heads-Up Display and real-time telemetry.

## Death of the status meeting

A status meeting is a 30-minute delay on what the scoreboard already knows. Standing rituals were a substitute for telemetry. When the HUD is live, the meeting has nothing left to say.

## The three HUD signals

When the Pilot looks up, they look for three things:

1. **Traction** — Intent-Result Alignment (IRA). Does the output match the Vibe? IRA 100%: agents delivered exactly what was intended. IRA 60%: drifted or hallucinated.
2. **Circuit Delta** — the difference in Lap Time between today and yesterday. Are we solving problems faster than last Lap?
3. **Hallucination Debt** — is the machine drifting into creative fiction? Debt compounds: a hallucinated assumption in Lap 1 becomes a sales pipeline crisis in Lap 12.

## The Pilot's Rule

- **Telemetry green:** the meeting is cancelled. The HUD already told you.
- **Drift:** do not discuss. Adjust the Vibe and re-run the Lap.

## IRA thresholds

- **IRA >= 95%:** stay quiet. Double Tenaza holding: trust the machine, keep the pace.
- **IRA ~70%:** investigate the Mission Script. The Vibe, not the machine, is the usual cause of drift. Rewrite it and re-run, don't re-explain.

## Spreadsheets are the rearview mirror

A weekly spreadsheet is historical fiction written in a formula. The HUD is live. If a metric can only be produced on Monday for what happened last week, it is explaining the crash, not preventing it.

## View-Only Observer Access

Replace vertical reporting with "Displaying Out": hand the boss and stakeholders View-Only HUD access. They see live telemetry instead of rehearsed summaries. Vertical Reporting is Performance Art. Stop "Reporting Up," start "Displaying Out."

The one who sees the HUD needs no meeting. The one making decisions needs current numbers, not a deck.

## HUD calibration workflow

1. **Define metrics.** Pick the three signals (Traction/IRA, Circuit Delta, Hallucination Debt). Define exactly how each is computed. Exact formulas in `references/hud-metrics.md`.
2. **Set thresholds.** Green/yellow/red bands per metric. IRA >= 95% green, ~70% yellow, below 60% red. Circuit Delta target: negative is winning (Lap times shrinking).
3. **Define escalation triggers.** The moment a metric crosses a band, a named owner acts — no meeting required. "If Hallucination Debt >= 4 alerts, the Risk Spotter freezes that agent."
4. **Grant Observer Access.** Everyone who used to attend the status meeting gets View-Only access to the HUD. There is nothing left to report.

## How to use this skill

1. Compute the three signals honestly (formulas in the reference).
2. Set the green/yellow/red bands and the escalation triggers first, before any numbers embarrass anyone.
3. Put the HUD where the Pilot looks. If the HUD is not visible, the meeting is already back.
4. When telemetry is green, cancel the meeting. When it drifts, adjust the Vibe, not the calendar.