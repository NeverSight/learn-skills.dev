---
name: tella-data-callouts
description: Show the numbers a speaker says in a Tella video as animated graphics, through the Tella MCP, as big stats, before-and-after comparisons, bars, percentages and count-ups, each timed to the spoken number and checked against the transcript. Use when asked to visualize stats, metrics, results, growth, pricing or any numbers in a video, or for data callouts or animated charts. Builds on tella-motion-design. A single stat can be a text overlay; charts use the Tella Motion tools, which are in beta and not available in every workspace.
---

# Data callouts for a Tella video

When the speaker says a number that matters, make it visible: the number large, what it measures beside it, and, for a comparison, its shape. Follow `tella-motion-design` for the look, timing, placement and checks; load it first if you haven't.

This skill needs the Tella MCP. If tools such as `get_timeline` are missing, follow the connection steps in the `tella` skill first.

- **Accuracy first.** Show each number exactly as said, with its unit and sign ("3 days → 4 hours", not "3 → 4"). Never invent data: one number said means one number shown, not a chart with made-up neighbours. Draw bars and blocks to scale from zero.
- **On the number.** A figure appears when it is spoken, never earlier. Figures said together ("200 shops in 12 cities") build up in one callout as each is said, rather than swapping cards.
- **Number first.** The number is the largest thing in the callout, in the accent colour, with a short label of what it measures (a few words) smaller beneath it.
- **Pick the treatment for the figure**: a big stat with its label for a single number, two bars or blocks for a before and after, a ring or bar for a percentage, a count-up only for a total or growth that deserves it.

Check a frame of every callout at its final value against the transcript, and report each with the line it comes from.
