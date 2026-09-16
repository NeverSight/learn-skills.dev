---
name: zephyr-grafana-links
description: Build or refresh the two Grafana dashboard links (overall and bulk ferment) in a Zephyr bake log's grafana section. Use when asked to add, update, or fix the Grafana links in a bake log, or to pin the link end times once a bake has finished.
---

## Overview

Grafana links give a bake log two ready-made views of the dashboard: one spanning the whole bake, one spanning bulk fermentation.

This skill is deliberately self-contained so it can be replaced with a different link implementation without touching the [[zephyr]] skill.

Filename resolution, event_time tags, the Starter peak duration block, and parameter precedence are owned by the [[zephyr]] skill — this skill consumes those rules, it does not restate them.

Read the [[zephyr]] skill before building links, for the bake log naming convention and the parameter defaults.

Annotations are a different concern entirely and belong to the [[grafana-bake-annotation]] skill. See Section Ownership below.

## Parameters

- dashboard base URL — `https://taylormonacelli1.grafana.net/d/tatmmtv/new-dashboard`
- fixed query parameters — `orgId=1`, `timezone=browser`, `refresh=30m`
- bake log directory — resolved per the Parameters section of the [[zephyr]] skill

## Trigger

Build or refresh links only when explicitly asked.

Never regenerate links automatically just because a bake log is open.

Requests that trigger this component:

- "Update the grafana links in this log"
- "Add the grafana links to bake log 7-20"
- "The bake is done, fix the grafana links"
- "Apply zephyr to bake log 7-20" — the compound request defined in the [[zephyr]] skill

Requests that do NOT trigger it:

- "Apply Grafana annotations" — that is the [[grafana-bake-annotation]] skill
- "Route the Zephyr entries in this log" — that is the [[zephyr-routing]] skill
- Reading a bake log for any other purpose

## Framing the Window

The window brackets the bake rather than sitting flush against it.

Each link opens one hour before its own starting event and closes roughly one hour after the bake ends.

That headroom keeps the trace from being clipped at the edges of the plot, so the run-up and the tail are both visible.

## Choosing the End Time

The `to` parameter depends on whether the bake is still running.

While the bake is in progress, use `to=now` so the graph keeps extending as new readings arrive and always shows data up to the present moment.

Once the bake is finished, `to=now` is wrong: the window keeps growing after the last reading, so the bake compresses into an ever-shrinking sliver on the left while empty time fills the rest of the graph.

For a finished bake, pin `to` to a fixed timestamp roughly one hour after the bake ended.

Decide which case applies by looking for an end-of-bake entry in the `## bake log` section — the loaves coming out of the oven, or the final loaf's bake finishing.

The annotation label for this event is `bake_done`; the log may instead phrase it as "out of the oven", "finished baking", or "the last loaf".

If no end-of-bake entry exists, the bake is still running — use `to=now` for both links.

If one exists, take its event time, add one hour, convert to UTC, and use that fixed timestamp as `to` for both links.

If only the start of the final loaf's bake is recorded and not its finish, treat the bake as ending 45 minutes after that start, then add the one hour of headroom.

Both links always share the same `to` value.

## Choosing the Start Times

Two links are written, each with its own `from`.

| link | starts one hour before | source |
| ---- | ---------------------- | ------ |
| overall | the levain feeding | the `fed` field in the `## Starter peak duration` block |
| bulk ferment | the start of bulk fermentation | the event time of the entry where the flour is mixed in |

The bulk ferment start is the `mix` event — bulk fermentation begins when the dough comes together, not at `long_bulk_start`.

When a required source is missing or still `[TBD]`, write `[TBD]` in place of that URL rather than guessing a time.

A missing source affects only its own link; the other is still written.

## Time Zone

Bake log times are local wall-clock times.

Grafana `from` and `to` take UTC, so convert before writing — during Pacific Daylight Time that means subtracting 7 hours.

Format as ISO 8601 with milliseconds and a trailing `Z`, matching the dashboard's own format: `2026-07-21T02:02:47.000Z`.

The literal `now` is never converted.

## Section Ownership

The links live at the top of the `## grafana` section of the bake log, in this exact shape:

```
overall
<URL or [TBD]>

bulk ferment
<URL or [TBD]>
```

Replace the whole links block on every run, whatever it currently holds — treat it as regenerated output, not as text to patch.

Everything else in the `## grafana` section belongs to the [[grafana-bake-annotation]] skill, in particular the fenced `annotate-grafana.py` command blocks.

Never delete, reorder, or edit those blocks while updating links.

Do not assume the section already has placeholders or any particular content — it may be empty, links-only, annotations-only, or both.

## Refreshing a Finished Bake

Links written mid-bake carry `to=now` and go stale the moment the bake ends.

When the end-of-bake entry lands in a log whose links still say `to=now`, rewrite both links with the pinned end time.

This is the common case for this component: it usually runs twice per bake, once early and once after the bake finishes.

## Commit

Commit the bake log after updating the links.
