---
name: gnuplot
description: 'This skill should be used when the user invokes "/gnuplot" to plot data from the current context using gnuplot and output the resulting image path.'
tools: Bash
disable-model-invocation: true
---

# Plot data with gnuplot

Plot data from the most recent interaction context using gnuplot. Generate a PNG image with a transparent background and output it as a markdown image so it renders inline.

## How to plot

1. Extract or derive plottable data from the current context.
2. If the Emacs foreground color is not already known from a previous plot in this session, query it:
   ```sh
   emacsclient --eval '
   (face-foreground (quote default))'
   ```
   This returns a hex color like `"#eeffff"`. Reuse it for all subsequent plots.
3. Write a gnuplot script to a temporary file using that color.
4. Run gnuplot on the script.
5. Output the result as a markdown image on its own line:
   ```
   ![description](/tmp/agent-plot-XXXX.png)
   ```

```sh
gnuplot /tmp/agent-plot-XXXX.gp
```

## Gnuplot script template

```gnuplot
set terminal pngcairo transparent enhanced size 800,500
set output "/tmp/agent-plot-XXXX.png"

FG = "#eeffff"  # from emacsclient query
set border lc rgb FG
set key textcolor rgb FG
set xlabel textcolor rgb FG
set ylabel textcolor rgb FG
set title textcolor rgb FG
set xtics textcolor rgb FG
set ytics textcolor rgb FG

# ... plot commands using the data ...
```

## Rules

- Query the Emacs foreground color once per session and reuse it for all subsequent plots. Only query again if the color is not already known.
- Always use `pngcairo transparent` terminal for transparent background.
- Always use a timestamp in the filename (e.g., `/tmp/agent-plot-$(date +%s).png`). Never use descriptive names like `agent-plot-lorenz.png`.
- Use inline data (`$DATA << EOD ... EOD`) when practical. For large datasets, write a separate data file.
- After gnuplot runs successfully, output a markdown image (`![description](path)`) on its own line.
- Choose an appropriate plot type for the data (lines, bars, histogram, scatter, etc.).
- Include a title, axis labels, and a legend when they add clarity.
- Use `enhanced` text mode for subscripts/superscripts when needed.
- If no plottable data exists in the recent context, inform the user.
