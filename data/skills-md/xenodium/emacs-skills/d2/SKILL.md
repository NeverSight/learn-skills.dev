---
name: d2
description: 'This skill should be used when the user invokes "/d2" to create a diagram from the current context using D2 and output the resulting image path.'
tools: Bash
disable-model-invocation: true
---

# Create diagrams with D2

Create a diagram from the most recent interaction context using D2. Generate a PNG image and output it as a markdown image so it renders inline.

## How to create a diagram

1. Extract or derive diagrammable data from the current context.
2. If the Emacs foreground color and background mode are not already known from a previous diagram in this session, query them:
   ```sh
   emacsclient --eval '(face-foreground (quote default))'
   emacsclient --eval '(frame-parameter nil (quote background-mode))'
   ```
   The first returns a hex color like `"#eeffff"`. The second returns `dark` or `light`. Reuse both for all subsequent diagrams.
3. Write a D2 file to a temporary file using the foreground color.
4. Run D2 with `--theme 200` if background mode is `dark`, or `--theme 0` if `light`.
5. Output the result as a markdown image on its own line:
   ```
   ![description](/tmp/agent-diagram-XXXX.png)
   ```

```sh
# Use --theme 200 for dark, --theme 0 for light
d2 --theme 200 --pad 40 /tmp/agent-diagram-XXXX.d2 /tmp/agent-diagram-XXXX.png
```

## D2 template

Use `--theme 200` for dark or `--theme 0` for light, based on the Emacs background mode. Apply the queried foreground color to `style.font-color` and `style.stroke` on nodes and edges.

```d2
direction: right

node1: Label {
  style.font-color: "#eeffff"
  style.fill: "#2d3748"
  style.stroke: "#eeffff"
}

node2: Label {
  style.font-color: "#eeffff"
  style.fill: "#2d3748"
  style.stroke: "#eeffff"
}

node1 -> node2: label {style.stroke: "#eeffff"; style.font-color: "#eeffff"}
```

## Rules

- Query the Emacs foreground color once per session and reuse it for all subsequent diagrams. Only query again if the color is not already known.
- Query the Emacs background mode once per session via `(frame-parameter nil 'background-mode)`. Use `--theme 200` for `dark` or `--theme 0` for `light`. Always use `--pad 40`.
- Always use a timestamp in the filename (e.g., `/tmp/agent-diagram-$(date +%s).png`). Never use descriptive names.
- Set the queried foreground color on `style.font-color` and `style.stroke` for all nodes and edges so the diagram is readable on the user's Emacs background.
- Use meaningful fill colors to distinguish different types of elements.
- After D2 runs successfully, output a markdown image (`![description](path)`) on its own line.
- Choose an appropriate layout direction and structure for the data.
- Include labels on edges when they add clarity.
- If no diagrammable data exists in the recent context, inform the user.
