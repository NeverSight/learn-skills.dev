---
name: implement-paper
description: Implement a research paper as an interactive marimo notebook. Starts by understanding what the user wants to explore, fetches the paper via alphaxiv, then builds a focused notebook.
---

# Implement Paper

Turn a research paper into an interactive marimo notebook. For general marimo notebook conventions (cell structure, PEP 723 metadata, output rendering, `marimo check`, variable naming, etc.), refer to the `marimo-notebook` skill.

## Step 1: Understand what the user wants

Before fetching or reading anything, have a short conversation to scope the work. Ask the user:

- **Which part of the paper interests you most?** A paper may have multiple contributions — the user likely cares about one or two. Don't implement the whole thing.
- **What's the goal?** Are they trying to understand the method, reproduce a result, adapt it to their own data, or teach it to someone else? This changes the notebook's tone and depth.
- **Do they want to use a specific dataset?** If it's relevant, ask. Otherwise, suggest simulating data.
- **Does this require PyTorch?** Some papers need it, many don't. Ask if unclear — it's a heavy dependency.
- **What's their background?** The paper aims to fill a knowledge gap — gauge what the user already knows so the notebook can meet them where they are. Skip basics they're familiar with, explain prerequisites they're not.

Only move on once you have a clear picture of what to build.

## Step 2: Fetch the paper

See [references/fetching-papers.md](references/fetching-papers.md) for how to retrieve paper content via alphaxiv.org. This avoids reading raw PDFs and gives you structured markdown.

## Step 3: Plan the notebook

After reading the paper, outline the notebook structure for the user before writing code.

**Keep the notebook as small as possible.** Sometimes the idea is best conveyed with just a single interactive widget — if you need a custom one, consider the `anywidget` skill. Other times you need a full training loop — if so, consider using the `marimo-batch` skill for heavy computation. The goal is the minimum amount of code needed to get the idea across.

A typical arc:

| Section | Purpose | Typical elements |
|---------|---------|------------------|
| Title & context | Orient the reader | `mo.md()` with paper title, authors, link |
| Background | Set up prerequisites | Markdown + equations |
| Method | Core algorithm step-by-step | Code + markdown interleaved |
| Experiments | Reproduce key results | Interactive widgets + plots |
| Conclusion | Summarize takeaways | `mo.md()` |

Not every notebook needs all sections. Share the outline with the user and adjust before writing code.

## Step 4: Build the notebook

Create the marimo notebook following the `marimo-notebook` skill conventions.

Key guidelines:

- **Never assume the dataset.** Use whatever the user specified in Step 1. If they didn't specify one, simulate data.
- **Make it self-contained.** A reader should understand the notebook without reading the full paper.
- **Use KaTeX for equations.** Render key equations with `mo.md(r"""$...$""")` so the notebook mirrors the paper's notation. Keep notation consistent with the paper.
- **Add interactivity where it aids understanding.** Sliders for hyperparameters, dropdowns for dataset variants, or toggles for ablations help readers build intuition.
- **Show, don't just tell.** Prefer a plot or table over a paragraph of explanation.
- **Name variables to match the paper's notation** where practical (e.g., `alpha`, `X`, `W`), and add comments mapping them to equation numbers.

## Tips

- **Don't reproduce the entire paper.** Focus on what the user asked about in Step 1.
- **Iterate visually.** Build up figures incrementally (e.g., show data → show model fit → show residuals) rather than dumping everything into one plot.
- **If the paper uses heavy notation**, include a small "notation reference" cell with a markdown table mapping symbols to descriptions.
