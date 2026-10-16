---
name: show-me-diagram
description: Explain the current topic, a status or a concept as one designed diagram made with the diagram-design skill. Use when the user asks to see it as a diagram or with diagram-design. For a quick view in plain text, use show-me; for a report or decision page to read later, use show-me-artifact.
---

Show the topic as one diagram the user opens in a browser. The diagram is for the user's own understanding, so stay with plain text when you only need to explain something to another agent.

1. **Load the `diagram-design` skill** and follow it for the build. Don't restate or replace its rules, since it changes upstream.
2. **Use the profile the user names; otherwise use the default** that `profiles/index.md` marks. Read that profile from `profiles/` beside this file and apply its choices on top of diagram-design's style guide for this diagram. Don't save it into diagram-design's install or profile library, since other projects share them.
3. **Pick the diagram type that fits the point,** from the types `diagram-design` lists: a flowchart or sequence for a process, a state machine for status, a tree or layer stack for structure, a timeline for progress. Make one diagram per point. Above about nine nodes, split it.
4. **Check the borders before you show it.** Draw each outline after every fill next to it, and put focal outlines last in the SVG, since a later fill paints over half of an earlier border. Export or screenshot at 2x, since 1px lines smear across two pixels at 1x. Zoom in and check that every border is the same width on all sides.
5. **Open the file for the user,** with one or two lines on what it shows. Keep the rest of the reply short, since the diagram carries the point.

## References

- `profiles/index.md`: the profiles, which one is the default, and the layers every profile fills in, and how to check one.
