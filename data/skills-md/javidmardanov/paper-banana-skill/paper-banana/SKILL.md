---
name: paper-banana
description: >-
  Generates publication-ready academic illustrations using the PaperBanana
  five-agent pipeline (arXiv:2601.23265). Diagram mode runs 5 Gemini API
  agents with multimodal in-context learning from curated reference images.
  Plot mode generates executable Python matplotlib/seaborn code.
  Use when the user asks for: research paper figures, academic diagrams,
  methodology illustrations, architecture diagrams, statistical plots,
  conference-quality visualizations, flowcharts for papers, NeurIPS/ICML/CVPR
  figures, or improving existing paper figures.
---

# PaperBanana: Academic Illustration Pipeline

Automates publication-ready academic illustrations via 5 specialized agents, each implemented as a separate Gemini API call:
**Retriever** (categorize & select references) -> **Planner** (multimodal description) -> **Stylist** (polish) -> **Visualizer** (render) -> **Critic** (evaluate & refine).

Two output modes:
- **DIAGRAM MODE**: Each agent is a Python script calling Gemini VLM/image APIs. Run `scripts/orchestrate.py` for end-to-end execution.
- **PLOT MODE**: Statistical plots generated as executable Python matplotlib/seaborn code (code-based to eliminate data hallucination).

**Requirements**: `GOOGLE_API_KEY` env var (used for VLM calls in retriever/planner/stylist/critic AND image generation in visualizer), Python 3.10+ with `google-genai`, `matplotlib`, `seaborn`, `numpy`, `pillow`.

Paper: *PaperBanana: Automating Academic Illustrations with Multi-Agent Systems* (arXiv:2601.23265, Google/PKU)

---

## Step 1: Determine Output Mode

Decide which track to follow:

| Signal | Mode |
|--------|------|
| User provides raw data, table, CSV + visual intent (bar chart, scatter, etc.) | **PLOT MODE** |
| User provides methodology text, description, or figure caption | **DIAGRAM MODE** |
| User provides existing figure to improve | Match original type |

**Critical rule**: PLOT MODE always generates Python code (never image generation for data visualizations). Code-based generation eliminates data hallucination errors that corrupt numerical accuracy in image-based approaches.

---

## Step 2: Execute Pipeline

### DIAGRAM MODE — Automated Pipeline

**Primary entry point**: Run the end-to-end orchestrator:

```bash
python scripts/orchestrate.py \
  --methodology-file methodology.txt \
  --caption "Figure 1: Overview of proposed framework" \
  --mode diagram \
  --output output/diagram.png
```

Or with inline text:
```bash
python scripts/orchestrate.py \
  --methodology "Our framework consists of three modules..." \
  --caption "Figure 1: System overview" \
  --mode diagram \
  --output output/diagram.png
```

The orchestrator chains all 5 agents automatically and handles the Critic's refinement loop (up to 3 iterations). Intermediate outputs are saved to `output/work/` for inspection.

#### Pipeline Details

Read `references/DIAGRAM-PROMPTS.md` for the actual Gemini prompt templates used by each agent.

**Phase 1: RETRIEVER** (`scripts/retriever.py`) — Gemini VLM call
- Classifies methodology into 1 of 4 categories from `references/DIAGRAM-CATEGORIES.md`
- Selects 2 most relevant reference diagrams from the 13 curated examples in `assets/references/`
- Identifies visual intent: Framework Overview, Pipeline/Flow, Detailed Module, Architecture Diagram

**Phase 2: PLANNER** (`scripts/planner.py`) — Multimodal Gemini VLM call
- Sends the 2 selected reference images + methodology text to Gemini as a multimodal prompt
- The VLM "sees" what good methodology diagrams look like (in-context learning from images)
- Generates an extremely detailed textual description of the target diagram
- **Critical**: Natural language only for all visual attributes. NEVER hex codes or pixel dimensions

**Phase 3: STYLIST** (`scripts/stylist.py`) — Gemini VLM call
- Takes the Planner's description + full NeurIPS 2025 style guide
- Applies domain-specific styling based on the category from Phase 1
- Follows 5 critical rules: preserve aesthetics, intervene minimally, respect domain, enrich details, preserve content
- Outputs the polished description only

**Phase 4: VISUALIZER** (`scripts/generate_image.py`) — Gemini Image API call
- Uses `gemini-3-pro-image-preview` to generate the diagram image from the styled description
- Prepends quality prefix (high-res, legible text, clean background, no watermarks)
- Aspect ratio selected based on visual intent (16:9 for pipelines, 3:2 for modules)

**Phase 5: CRITIC** (`scripts/critic.py`) — Multimodal Gemini VLM call
- Sends the generated image + methodology text to Gemini for multimodal evaluation
- Scores on 4 dimensions (faithfulness, readability, conciseness, aesthetics)
- If faithfulness < 7 OR readability < 7: generates revised description → loops to Phase 4
- Maximum 3 refinement iterations

---

### DIAGRAM MODE — Manual Execution

You can also run each agent individually for more control:

```bash
# Phase 1: Retriever
python scripts/retriever.py --methodology-file text.txt --output work/retriever.json

# Phase 2: Planner
python scripts/planner.py --methodology-file text.txt --caption "Figure 1: ..." \
  --references work/retriever.json --output work/planner.json

# Phase 3: Stylist
python scripts/stylist.py --description work/planner.json --output work/stylist.json

# Phase 4: Visualizer (extract styled_description from JSON, pass to generate_image.py)
python scripts/generate_image.py --prompt-file work/styled_desc.txt --output output/diagram.png

# Phase 5: Critic
python scripts/critic.py --image output/diagram.png --methodology-file text.txt \
  --description work/stylist.json --output work/critic.json
```

---

### PLOT MODE

Read `references/PLOT-PROMPTS.md` for detailed agent prompts. Read `references/PLOT-STYLE-GUIDE.md` for aesthetic rules.

Plot mode uses Claude (or the host agent) for reasoning and code generation — no Gemini API calls needed for plot generation itself.

#### Phase 1: CATEGORIZE (Retriever)

Match data characteristics and visual intent:

| Data Type | Plot Types |
|-----------|------------|
| Categorical comparison | Bar chart, grouped bar, stacked bar |
| Continuous trends | Line chart, area chart |
| Correlation/distribution | Scatter plot, histogram, box plot, violin |
| Matrix/similarity | Heatmap, confusion matrix |
| Multi-dimensional | Radar/spider chart |
| Proportional | Pie/donut chart, treemap |

#### Phase 2: PLAN (Planner)

Create a detailed specification that explicitly enumerates:
- Every raw data point with exact coordinates/values
- Axis ranges, labels, tick marks, scales (linear/log)
- Color assignments for each series/category
- Font sizes for title, axis labels, tick labels, legend
- Line widths, marker sizes, marker shapes
- Legend placement and formatting
- Grid style (major/minor, dashed/solid)
- Figure dimensions and DPI

#### Phase 3: STYLE (Stylist)

Read `references/PLOT-STYLE-GUIDE.md` for NeurIPS 2025 plot aesthetics.

Key styling rules:
- White backgrounds only
- Colorblind-friendly palettes (see `assets/palettes/colorblind_safe.json`)
- Sans-serif fonts (Helvetica, Arial, or DejaVu Sans)
- Markers on line charts for print readability
- Inward-facing tick marks
- Subtle grid lines (light gray, dashed)

#### Phase 4: VISUALIZE (Visualizer — Code Generation)

Generate complete, self-contained Python matplotlib/seaborn code. Use `scripts/plot_generator.py` as a reference implementation or run it directly with a JSON config:

```bash
python scripts/plot_generator.py --config plot_config.json --output figure.pdf
```

Code requirements:
- Self-contained: all data defined inline, no external file dependencies
- Apply `.mplstyle` from `assets/matplotlib_styles/academic_default.mplstyle`
- Set `OUTPUT_PATH` variable for output file location
- 300 DPI, `bbox_inches='tight'`
- No `plt.show()` — save only
- Support both PDF and PNG output

After generating the code, execute it to produce the plot image.

#### Phase 5: CRITIQUE (Critic)

Same rubric as diagram mode, plus plot-specific checks:
- Data fidelity: Every data point correctly plotted
- Axis accuracy: Ranges, labels, scales match specification
- Layout: No overlapping labels, legends, or data points
- Code correctness: Syntax valid, imports available, output saved

If code execution failed, analyze the error, simplify the approach, and regenerate.

---

## Quick Start Examples

**Diagram (automated)**: Run `scripts/orchestrate.py` with your methodology text file and caption.

**Diagram (via agent)**: "Generate a methodology diagram for my transformer architecture. Here is the methodology section: [paste text]. Caption: Overview of our proposed multi-head attention framework."

**Plot**: "Create a bar chart comparing model performance. Data: {BERT: 92.3, GPT-4: 88.1, Claude: 95.7, Gemini: 91.2}. Intent: F1 score comparison across language models."

**Improve**: "Improve the aesthetics of this diagram: [paste existing description or attach current figure]"

---

## File Reference

| File | Purpose | When to Read |
|------|---------|-------------|
| `scripts/orchestrate.py` | End-to-end pipeline runner | Diagram mode primary entry point |
| `scripts/retriever.py` | VLM-based reference selection | Phase 1 (diagram mode) |
| `scripts/planner.py` | Multimodal description generation | Phase 2 (diagram mode) |
| `scripts/stylist.py` | VLM-based style application | Phase 3 (diagram mode) |
| `scripts/generate_image.py` | Gemini Image API call | Phase 4 (diagram mode) |
| `scripts/critic.py` | VLM-based image evaluation | Phase 5 (diagram mode) |
| `scripts/plot_generator.py` | Template-based matplotlib generator | Phase 4 (plot mode) |
| `scripts/validate_output.py` | Output validation and dependency check | Post-generation validation |
| `references/DIAGRAM-PROMPTS.md` | Actual Gemini prompt templates for diagrams | All diagram phases |
| `references/PLOT-PROMPTS.md` | Agent prompts for plots | All plot phases |
| `references/DIAGRAM-STYLE-GUIDE.md` | NeurIPS 2025 diagram aesthetics | Phase 3 (Style) |
| `references/PLOT-STYLE-GUIDE.md` | NeurIPS 2025 plot aesthetics | Phase 3 (Style) |
| `references/EVALUATION-RUBRIC.md` | Critic scoring criteria (4 dimensions) | Phase 5 (Critique) |
| `references/DIAGRAM-CATEGORIES.md` | 4 diagram categories with keywords | Phase 1 (Categorize) |
| `assets/references/index.json` | 13 curated reference diagram metadata | Phase 1 (Retriever) |
| `assets/references/*.jpg` | 13 curated reference diagram images | Phase 2 (Planner multimodal input) |
| `assets/palettes/*.json` | Color palette definitions | Phase 3 (Style) |
| `assets/matplotlib_styles/*.mplstyle` | Matplotlib style sheets | Phase 4 (plot mode) |

## Environment Setup

```bash
# Required for all Gemini API calls (VLM reasoning + image generation)
export GOOGLE_API_KEY="your-api-key-here"

# Install dependencies
pip install google-genai matplotlib seaborn numpy pillow
```

Verify setup: `python scripts/validate_output.py --check-deps`
