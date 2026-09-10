---
name: mathodology-figure-presets
description: Use when selecting, designing, generating or reviewing scientific figures, complex modeling charts, paper illustrations or image2-assisted visuals.
---

# Mathodology Scientific Figure Presets

Choose a figure from the question the reader needs to answer. Complex figures
are useful when their panels expose related evidence; complexity itself is not
a quality measure. Use actual data and the user's paper language.

## Agent-facing guidance

Read [default figure guidance](references/figure-guidance.md) when starting figure
work or briefing another agent. It is the canonical reusable instruction: select
a code template, fill real data, run it and inspect the resulting PNG/PDF. Use
it as adaptable guidance, not a fixed pipeline.

## Before the first figure

Ask once per modeling task, unless the answer is already known:

> 是否有可用的 image2 模型？通过当前工具、已配置接口，还是手动生成使用？

Use the host's question mechanism and continue independent analysis while waiting.
Do not repeat the question in every specialist or turn. Read
[image2 usage](references/image2.md) for available, manual, unavailable and pending
cases. Do not claim a generic image tool is image2 or collect API keys in chat.

## Default rendering route

Without image2, with a pending answer, or with only manual image2 access, use the
[20 callable code templates](templates/README.md) by default. Copy the matching
function into the working task, bind actual data, execute it, and export PNG/PDF.
Do not stop at a plotting prompt or wait for image2. Quantitative figures use
this same data-driven route even when image2 is available. Adapt the closest
template when needed; never substitute synthetic preview values for missing data.

## Choose and build

1. Write the figure's intended conclusion as a question before seeing the result.
   Identify data, units, comparison, uncertainty and the available paper space.
2. Use the [20-preset selector and recipes](references/presets.md). Load the
   relevant cards, not the entire reference collection. If the data cannot
   support a preset, choose its simpler alternative or explain the missing input.
3. Adapt the card's plotting and caption prompts using the actual columns,
   measured results and scientific meaning. Do not force the data to match a
   preview. Follow [style and export guidance](references/style.md).
4. Use numerical plotting tools for quantitative marks. image2 can assist
   illustrations, mechanism diagrams and layout concepts; rebuild quantitative
   layers from data. Never use generated pixels as computed evidence.
5. Inspect the rendered figure at publication size, then inspect its placement
   in the compiled paper. Fix illegibility and misleading encodings; remove
   decorative panels that do not support the argument.

Deliver the figure, a caption, its source-data or calculation location and a
rerun instruction. The format is flexible. State actual limitations; do not
invent statistical significance or claim that appearance implies an award.

## Reference and example library

- [Sources and visual references](references/README.md): six PLOS reference
  figures (including counterexamples), eight Matplotlib source-text snapshots,
  licenses and a per-file provenance manifest. Read snapshots before adaptation;
  they are not executable installation or workflow steps.
- [Synthetic example gallery](examples/README.md): six previews and the optional
  [demonstration script](scripts/render_examples.py). The examples illustrate
  presentation and statistical labeling, not evidence for a contest problem.

```bash
python3 .claude/skills/mathodology-figure-presets/scripts/render_examples.py --output work/figure-examples
```

The demos use NumPy and Matplotlib; the F08 code template additionally requires
SciPy. If dependencies are absent, use the host's available runtime
or install them in an isolated environment; no dependencies are needed just to
read and use the prompts. Existing numerical tools in R, MATLAB or another
language are equally acceptable for task-specific figures.
