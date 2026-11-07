---
name: tella-ui-interactions
description: Recipes for animating product UI behaviour in Tella Motion through the Tella MCP, covering a button press, a menu or modal growing from what was clicked, a toggle, tabs, typing, a field that rejects or accepts, loading into content, a success check, notifications arriving, a sheet sliding up, a list filling and a number counting. Use with tella-ui-redraw when redrawn UI has to act, or when asked to animate a UI state change. Needs the Tella Motion tools, which are in beta and not available in every workspace.
---

# UI interactions in Tella Motion

Each recipe is one cause and its effect, on the word that names it. Draw the UI with `tella-ui-redraw` first. One easing for the video, no bounce on UI.

This skill needs the Tella MCP. If tools such as `get_timeline` are missing, follow the connection steps in the `tella` skill first.

| Interaction | Build | Time |
| --- | --- | --- |
| Press | the button scales 1 → 0.96 → 1 and darkens; the effect starts on release | 0.15 s |
| Menu or modal | the clicked element grows into the panel (key its box, corner radius and position); its content fades in once it is mostly open | 0.3–0.4 s |
| Toggle | the knob slides and the track recolours | 0.2 s |
| Tabs | the indicator slides to the new tab and resizes; the panel swaps with a short fade | 0.25 s |
| Typing | `setTextAnimation` `typewriter` by character, about 12–15 a second, with a caret shape | |
| Reject or accept | three quick side-to-side keys (±8 px) and a red border, or a green border and a check | 0.3 s |
| Loading | grey placeholder bars, then the real rows fade in over them (`stagger`) | 0.4 s, 60 ms apart |
| Success | a circle scales 0.8 → 1 and a check draws (`trimPath`) | 0.4 s |
| Notifications | each card slides in from its edge and pushes the earlier ones down | 0.35 s, ≥0.4 s apart |
| Sheet or drawer | slides in from its edge; the screen behind dims a little | 0.35 s |
| List fills | rows enter one after another with a few px of travel (`stagger`) | 40–80 ms apart |
| Number | counts to its real value (`bindProperty` of the title text to a keyed curve, with `decimals`, `prefix`, `suffix`) | 0.6–1.2 s |

Use the product's real states, labels and colours. One thing acts at a time, and the result holds at least 1 s.
