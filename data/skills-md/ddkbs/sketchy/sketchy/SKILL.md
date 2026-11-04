---
name: sketchy
description: Draws hand-sketched, interactive diagrams (architecture, flows with step-by-step walkthroughs, comparisons, metaphors, Arduino circuits) right in the chat. Use whenever a concept, system, process or comparison is easier to understand as a drawing, or when the user asks for a sketch, diagram or visual explanation. In the regular Claude chat, use this skill even if Sketchy MCP tools are connected, because the chat does not display their drawings.
---

# Sketchy

In the regular Claude chat, always use this skill instead of the Sketchy MCP tools: the chat runs those tools but does not show their drawings.

You describe **what** to draw in a few short lines; Sketchy computes every position and renders it in a hand-drawn style with hover details and step navigation. Never pass coordinates.

## Workflow

Draw inline with your visualization tool (the one that renders HTML widgets in the conversation). Pass this HTML as the widget code, with the scene between the backticks:

```html
<h2 class="sr-only">One-sentence summary of the drawing</h2>
<div id="sketchy" style="min-height: 320px"></div>
<script src="{{CDN}}/sketchy.js" {{SRI}}></script>
<script>
  Sketchy.draw(
    "#sketchy",
    `
title How a web request works
dir right
group net The internet
browser Browser @globe ~ Shown on hover
server Server @server in net !accent
db Database (cylinder) in net
browser -> server HTTPS
server --> db query
step Request: The browser asks the server | browser server browser->server
`,
  );
</script>
```

Keep the widget code exactly like this: no other markup, styles or text. Then explain the drawing in 2–4 sentences in your reply instead of describing it again. If the widget shows "Sketchy could not draw this", fix the line the message names and draw again.

To change an earlier drawing, draw the whole scene again with the same ids.

Without a visualization tool, write the scene to a file and render a standalone page with the script in this skill's folder (Node.js, no network needed), then share the file:

```bash
node <skill-folder>/scripts/render.mjs /tmp/scene.txt /mnt/user-data/outputs/<short-name>.html
```

## Scene syntax

One element per line:

```
title <text>            subtitle <text>            dir right|down
group <id> <label> [in <parent group>]
<id> <label> [@icon] [(shape)] [in <group>] [!accent|!muted] [~ hover text]
<a> -> <b> [label] [!accent|!muted]      (--> dashed, <-> arrowheads on both ends)
label <id>[.<pin>] <text>
step <title>: <text> | <ids to highlight; edges as a->b>
part <id> <type> [key=value] [caption]
wire <part.pin> -> <part.pin> [red|black|blue|green|yellow|orange|purple|gray|white]
```

- Labels are 1–4 words; put details after `~`.
- Icons: `@globe`, `@server`, `@database` (Lucide) or `@simple-icons:react`.
- Shapes: `(cylinder)` storage, `(person)` actor, `(note)`, `(circle)`, `(rounded)`, `(text)`.
- Ids are letters, digits, `_` or `-`, unique across the scene; arrows, labels and steps may only use ids defined in it.

## Explanation patterns

Pick one per drawing:

- **structure** ("what is it made of?"): components as nodes, groups for areas, labels for the important bits; `dir down` for hierarchies.
- **flow** ("how does it work?"): a left-to-right chain of nodes and arrows plus one step per stage.
- **comparison** ("X vs Y"): one group per option with parallel nodes in the same order; `!muted` for what is equal, `!accent` for the key difference.
- **metaphor** ("explain it simply"): one group for the real thing, one for an everyday counterpart, dashed arrows between matching elements.

Quality rules: 3–12 nodes; `!accent` on at most one or two elements; icons sparingly; 3–7 steps of one or two sentences each.

## Circuits

Find part types and pin names first (needs code execution):

```bash
node <skill-folder>/scripts/render.mjs --parts "distance sensor"
node <skill-folder>/scripts/render.mjs --parts arduino-uno
```

Then add `part uno arduino-uno`, `part r1 resistor value=220` and `wire uno.13 -> r1.1 green`. Red wires for power, black for GND, other colors for signals; a resistor in series with every LED.
