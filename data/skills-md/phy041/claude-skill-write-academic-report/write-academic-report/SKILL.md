---
name: write-academic-report
description: "Write 40-100+ page academic reports (FYP, thesis, dissertation) with parallel Claude Code subagents. 3-wave pipeline: Wave 0 extracts data from your research repo, Wave 1 writes chapters in parallel (3-4x faster), Wave 2 compiles LaTeX with automated cross-reference auditing. Inherits academic writing standards from Nanda, Gopen & Swan, Lipton."
version: 1.0.0
author: Haoyang Pang
license: MIT
tags: [Academic Report, Thesis Writing, FYP, Dissertation, LaTeX, Parallel Agents, Claude Code Skill]
dependencies: [tectonic]
---

# Academic Report Writer: 40-100+ Page Thesis/FYP with Parallel Agents

Turn a research repository into a **publication-quality LaTeX thesis** in 2-4 hours instead of 8-12 — using a **3-wave parallel agent pipeline** purpose-built for academic reports.

**What this skill does:** You point it at your research repo (code + experiment results). It launches parallel agents to extract data, write chapters simultaneously, then assembles and compiles a complete LaTeX report with proper cross-references, figures, and bibliography.

**Validated:** 86-page FYP report, 6 chapters + 3 appendices + 15 figures, produced in ~6 hours. Writing philosophy inherited from [ml-paper-writing](https://github.com/Orchestra-Research/ml-paper-writing) (Nanda, Farquhar, Gopen & Swan, Lipton, Steinhardt, Perez).

---

## CRITICAL: Never Hallucinate Citations

**This rule is inherited from ml-paper-writing and is non-negotiable.**

### The Problem (Backed by Data)

| Statistic | Source |
|-----------|--------|
| **6-55%** of AI-generated citations are fabricated | Multiple studies (varies by model/domain) |
| **100+** hallucinated refs in NeurIPS 2025 accepted papers | GPTZero analysis, Jan 2026 |
| **50+** hallucinated refs in ICLR 2026 submissions | GPTZero analysis, Feb 2026 |
| Only **26.5%** of AI-generated references are entirely accurate | Paper-Checker 2026 survey |
| **206+** legal sanctions for AI-hallucinated citations in courts | As of July 2025 |
| **3 types**: fully fabricated, chimeric (blended), modified real | CheckIfExist (arXiv 2602.15871) |

Universities increasingly treat fake citations as **academic misconduct** — failed assignments, course failure, or expulsion.

### The Rule

**NEVER generate BibTeX entries from memory. ALWAYS fetch programmatically.**

```
IF you cannot programmatically fetch a citation:
    → Mark it as [CITATION NEEDED] or [PLACEHOLDER - VERIFY]
    → Tell the author explicitly
    → NEVER invent a plausible-sounding reference
```

### Automated Verification: citation_checker.py

After writing, **always run the citation checker** before submission:

```bash
# Check a single .bib file
python scripts/citation_checker.py references.bib

# Check all .bib files in a report directory
python scripts/citation_checker.py path/to/report/

# JSON output (for CI pipelines)
python scripts/citation_checker.py references.bib --json
```

The checker uses a **cascading 3-source verification pipeline**:

```
CrossRef (140M+ DOIs) → Semantic Scholar (200M+ papers) → OpenAlex (240M+ works)
```

For each citation it:
1. Searches by DOI (if available) or title
2. Computes title similarity + author overlap
3. Flags red flags (invalid DOI, generic title, missing fields, chimeric blends)
4. Reports: **verified** (2+ sources), **suspicious** (1 source), or **not found** (likely hallucinated)

**Red flag detection catches:**
- Fully fabricated citations (no match in any database)
- Chimeric hallucinations (title matches but authors don't)
- Invalid DOI formats
- Suspiciously generic titles common in AI output
- Missing critical fields (authors, year)
- Future publication years

See [references/citation-workflow.md](references/citation-workflow.md) for the full API documentation and Python CitationManager class.

---

## When to Use This Skill

| Scenario | Use This Skill | Use ml-paper-writing Instead |
|----------|:-:|:-:|
| FYP / Final Year Project report | Yes | |
| MSc / PhD dissertation | Yes | |
| Technical report (20+ pages) | Yes | |
| Conference paper (8-12 pages) | | Yes |
| Workshop paper (4-6 pages) | | Yes |

**Key difference**: This skill orchestrates **parallel subagents** for long documents. Conference papers are short enough to write sequentially.

---

## Core Architecture: 3-Wave Pipeline

```
Wave 0: DATA PREPARATION          Wave 1: CHAPTER WRITING          Wave 2: ASSEMBLY
(5-6 parallel agents)             (3-4 parallel agents)            (1-2 sequential agents)

┌─ Agent 0A: Data consolidation   ┌─ Agent 1: Template + Ch1-2     ┌─ Agent 6: Merge + cross-ref
├─ Agent 0B: Codebase analysis    ├─ Agent 2: Ch3 (core work)      └─ Agent 7: Compile + review
├─ Agent 0C: System analysis      ├─ Agent 3: Ch4-5 (results)
├─ Agent 0D: Experiment history   └─ Agent 4: Ch6 + Appendices
├─ Agent 0E: Statistics
└─ Agent 0F: Figure generation
```

**Why waves?** Data must exist before prose. Prose must exist before assembly. Violating this order produces agents that hallucinate numbers or write without evidence.

---

## Wave 0: Data Preparation (Before Writing)

**Goal**: Produce all data artifacts that chapter-writing agents will reference. Every claim in the report must trace back to a Wave 0 artifact.

### What Wave 0 Agents Produce

| Agent | Input | Output | Purpose |
|-------|-------|--------|---------|
| **0A: Data Consolidation** | Raw result files (JSON, CSV) | `data/final_results.json` | Single source of truth for all numbers |
| **0B: Codebase Analysis** | Source code | `data/codebase_analysis.md` | Module map, LOC, complexity, key snippets |
| **0C: System Analysis** | Architecture, pipeline code | `data/system_analysis.md` | How components connect, data flow |
| **0D: Experiment History** | All experiment logs | `data/experiment_history.md` | Timeline, what changed, why |
| **0E: Statistics** | Result files | `data/statistics.md` | Aggregate stats, distributions |
| **0F: Figure Generation** | Data artifacts + style config | `figures/*.pdf` + `figures/*.png` | All publication-quality figures |

### Agent 0F: Figure Pipeline (Special)

Figures deserve a dedicated agent because:
1. They must be **consistent** (same color palette, font sizes, style)
2. They must be **vector** (PDF for LaTeX \includegraphics)
3. They must be **colorblind-safe** (Okabe-Ito or Paul Tol palette)
4. They must be **self-contained** (captions tell the full story)

```python
# Recommended figure style
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams.update({
    'font.size': 11,
    'font.family': 'serif',
    'axes.labelsize': 12,
    'axes.titlesize': 13,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'legend.fontsize': 10,
    'figure.figsize': (6.5, 4),
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
})

# Colorblind-safe palette (Okabe-Ito)
COLORS = ['#E69F00', '#56B4E9', '#009E73', '#F0E442',
          '#0072B2', '#D55E00', '#CC79A7', '#000000']
```

**Output both formats**: `figure_name.pdf` (for LaTeX) + `figure_name.png` (for preview).

### Wave 0 Completion Gate

**Do NOT proceed to Wave 1 until:**
- [ ] All data files exist and are non-empty
- [ ] All figures compile (PDF + PNG)
- [ ] Numbers in `final_results.json` match known ground truth
- [ ] Each agent's output has been spot-checked

---

## Wave 1: Chapter Writing (Parallel, After Wave 0)

### Chapter Dependency Graph

```
Independent (can parallelize):
  Ch1 (Introduction) ←→ Ch2 (Literature Review)  [no dependency]
  Ch3 (System/Methods) [needs 0B, 0C]
  Ch6 (Conclusion) [needs 0A summary only]

Sequential (must wait):
  Ch4 (Experimental Setup) → Ch5 (Results) [Ch5 needs Ch4's definitions]
  Ch5 needs: 0A (data), 0D (history), 0E (stats), 0F (figures)
```

### Recommended Agent Assignment

| Agent | Chapters | Depends On | Approx Pages |
|-------|----------|------------|:---:|
| **Agent 1** | Template + Front matter + Ch1 + Ch2 | Plan only | 15-20 |
| **Agent 2** | Ch3 (System Design) | 0B, 0C | 12-18 |
| **Agent 3** | Ch4 + Ch5 (Setup + Results) | 0A, 0D, 0E, 0F | 15-25 |
| **Agent 4** | Ch6 + Appendices | 0A (summary) | 5-10 |

### Writing Philosophy (Inherited)

These principles from ml-paper-writing apply to every chapter:

**The Narrative Principle** (Nanda): Your report tells one story. Every chapter advances that story. If a section doesn't connect to the core contribution, cut it.

**Sentence-Level Clarity** (Gopen & Swan):

| Principle | Rule | Mnemonic |
|-----------|------|----------|
| Subject-verb proximity | Keep subject and verb close | "Don't interrupt yourself" |
| Stress position | Emphasis at sentence end | "Save the best for last" |
| Topic position | Context at sentence start | "First things first" |
| Old before new | Familiar then unfamiliar | "Build on known ground" |
| One unit, one function | Each paragraph = one point | "One idea per container" |
| Action in verb | Use verbs, not nominalizations | "Verbs do, nouns sit" |
| Context before new | Explain before presenting | "Set the stage first" |

**Word Choice** (Lipton, Steinhardt):
- Be specific: "accuracy" not "performance"
- Eliminate hedging: drop "may" and "can" unless genuinely uncertain
- Consistent terminology: pick one term per concept, stick with it
- Delete filler: "actually," "very," "basically," "essentially"

**Micro-Level Tips** (Perez):
- Minimize pronouns: "This result shows..." not "This shows..."
- Position verbs early in sentences
- Active voice always: "We show..." not "It is shown..."
- One idea per sentence

### Thesis-Specific Adaptations (Beyond ml-paper-writing)

| Conference Paper | Thesis/Report |
|-----------------|---------------|
| 1-1.5 page intro | 3-5 page intro with motivation + scope |
| Related Work section | Full Literature Review chapter |
| 8-12 pages total | 40-100+ pages total |
| 5-sentence abstract | 250-400 word abstract |
| Contribution bullets | Objectives & scope section |
| No project timeline | Gantt chart / project schedule |
| No appendices (usually) | 2-5 appendices with supplementary material |

### Chapter Templates

#### Chapter 1: Introduction (3-5 pages)

```latex
\chapter{Introduction}

\section{Background}
% 1-2 pages: Establish the problem domain
% Start specific, not generic. No "AI has revolutionized..."

\section{Motivation}
% 0.5-1 page: Why this problem matters NOW
% Use the "map analogy" or similar concrete framing

\section{Objectives and Scope}
% 0.5 page: Numbered list of objectives
% Explicitly state what is IN and OUT of scope

\section{Project Schedule}
% Gantt chart figure (generated in Wave 0)

\section{Report Organization}
% Brief roadmap of remaining chapters
```

#### Chapter 2: Literature Review (8-15 pages)

```latex
\chapter{Literature Review}

% Organize METHODOLOGICALLY, not paper-by-paper
% Group: "One line of work uses X [refs] whereas we use Y because..."

\section{Topic Area 1}
\section{Topic Area 2}
\section{Topic Area 3}
\section{Research Gap and Our Position}
% Explicitly state what's missing and how you fill it
% Include positioning figure/table if helpful
```

#### Chapter 3: System Design / Methodology (10-18 pages)

```latex
\chapter{System Design and Implementation}

\section{System Architecture}
% Architecture diagram (FIGURE — from Wave 0)

\section{Core Component 1}
% Code listings where relevant (use lstlisting or minted)

\section{Core Component 2}

\section{Technology Stack}
% TABLE: libraries, versions, purpose
```

#### Chapter 4: Experimental Setup (5-8 pages)

```latex
\chapter{Experimental Setup}

\section{Dataset / Data Collection}
\section{Evaluation Methodology}
\section{Baselines and Conditions}
\section{Statistical Methods}
% TABLE: which test, why, assumptions
```

#### Chapter 5: Results and Analysis (8-15 pages)

```latex
\chapter{Results and Analysis}

% For EACH result, explicitly state:
% 1. What claim it supports
% 2. The specific numbers
% 3. Statistical significance

\section{Main Results}
% FIGURE + TABLE for primary ablation/comparison

\section{Detailed Analysis 1}
\section{Detailed Analysis 2}
\section{Discussion}
% What worked, what didn't, WHY
```

#### Chapter 6: Conclusion (3-5 pages)

```latex
\chapter{Conclusion and Future Work}

\section{Summary of Contributions}
% 3-5 numbered contributions, each 2-3 sentences

\section{Limitations}
% HONEST assessment. Claude undersells weaknesses by default.
% Explicitly prompt: "What are the real limitations?"
% Pre-empt criticisms. Honesty builds trust.

\section{Future Work}
% 2-4 concrete, actionable directions
% Not vague "further research" — specific next steps
```

### Limitations Section Guidance (Critical)

**Claude has a documented tendency to understate limitations.** When writing the limitations section:

1. Ask yourself: "What would a skeptical examiner criticize?"
2. List ALL weaknesses, not just minor ones
3. Quantify where possible: "Judge variance is ~5pp between re-judgings"
4. Explain WHY the limitation doesn't invalidate the core contribution
5. Distinguish between "fundamental limitation" and "scope limitation"

---

## Wave 2: Assembly & Compilation

### Step 1: Merge Chapters

Use `\input{}` in `main.tex` to include chapter files:

```latex
\documentclass[12pt,a4paper]{report}
\input{preamble}

\begin{document}
\input{front_matter}
\tableofcontents
\listoffigures
\listoftables

\input{chapters/ch1_introduction}
\input{chapters/ch2_literature_review}
\input{chapters/ch3_system_design}
\input{chapters/ch4_experimental_setup}
\input{chapters/ch5_results}
\input{chapters/ch6_conclusion}

\bibliographystyle{plain}
\bibliography{references}

\appendix
\input{appendices/appendix_a}
\input{appendices/appendix_b}
\end{document}
```

### Step 2: Cross-Reference Audit (Mandatory)

With parallel agents writing chapters independently, **duplicate labels are inevitable**.

Run the automated audit script:

```bash
python scripts/cross_ref_audit.py report_dir/
```

This checks:
- Duplicate `\label{}` definitions
- Undefined `\ref{}` and `\cite{}` references
- Orphaned labels (defined but never referenced)
- Figure/table numbering consistency
- BibTeX key duplicates

See [scripts/cross_ref_audit.py](scripts/cross_ref_audit.py) for the full script.

### Step 3: Compile with Tectonic

**Tectonic** is strongly recommended over BasicTeX/TeX Live for local compilation:

```bash
# Install (macOS)
brew install tectonic

# Compile (handles all passes automatically)
tectonic main.tex

# Or with verbose output
tectonic -X compile main.tex
```

**Why Tectonic?**
- No `sudo`, no `tlmgr install`
- Handles BibTeX + multiple passes automatically
- Downloads packages on-demand
- Single binary, no distribution management

See [references/compilation-guide.md](references/compilation-guide.md) for alternatives and troubleshooting.

### Step 4: Quality Review

Final quality checks:

```
Post-Compilation Checklist:
- [ ] No undefined references (\ref, \cite)
- [ ] No duplicate labels
- [ ] All figures render at correct size
- [ ] Table of Contents is accurate
- [ ] List of Figures / Tables is complete
- [ ] Page numbers are correct
- [ ] Bibliography entries are complete
- [ ] Appendices are properly lettered
- [ ] No overfull/underfull hbox warnings (major ones)
- [ ] Consistent formatting across all chapters
```

---

## Tables and Figures

### Tables

Use `booktabs` for professional tables:

```latex
\usepackage{booktabs}
\begin{table}[t]
\centering
\caption{Comparison of conditions. Best results in \textbf{bold}.}
\label{tab:main_results}
\begin{tabular}{lcc}
\toprule
Condition & Success Rate $\uparrow$ & p-value \\
\midrule
Baseline & 25.6\% & --- \\
Summary & 27.8\% & 0.839 \\
\textbf{URL} & \textbf{50.0\%} & $<$0.001 \\
\textbf{Tools} & \textbf{50.0\%} & $<$0.001 \\
\bottomrule
\end{tabular}
\end{table}
```

**Rules:**
- Bold best value per metric
- Include direction symbols (higher/lower is better)
- Right-align numerical columns
- Consistent decimal precision
- Caption ABOVE table (convention for tables)

### Figures

- **Vector graphics** (PDF) for all plots and diagrams
- **Raster** (PNG 300+ DPI) only for screenshots/photographs
- **Colorblind-safe palettes** (Okabe-Ito recommended)
- **No title inside figure** — the caption serves this function
- **Self-contained captions** — reader should understand without main text
- Caption BELOW figure (convention for figures)

```latex
\begin{figure}[t]
\centering
\includegraphics[width=0.85\textwidth]{figures/architecture.pdf}
\caption{System architecture showing the five core modules.
         Arrows indicate data flow from browser automation (left)
         through state abstraction to the output graph (right).}
\label{fig:architecture}
\end{figure}
```

---

## University Template Handling

### Generic Thesis Template

A minimal, clean university thesis template is provided in `templates/university-thesis/`. It includes:
- A4 paper, 12pt, report class
- Front matter (title page, abstract, acknowledgements, TOC)
- Chapter structure with `\input{}`
- Bibliography with natbib
- Appendix support

### Adapting to Your University

Most universities provide their own LaTeX template. To adapt:

1. **Start from your university's template** (not ours)
2. Copy the `\input{}` chapter structure from our template
3. Keep university style files untouched
4. Add only necessary packages

| University Feature | Where to Adapt |
|-------------------|----------------|
| Title page format | `front_matter.tex` — follow university spec exactly |
| Margin requirements | `preamble.tex` — use university's geometry settings |
| Font requirements | `preamble.tex` — usually Times New Roman or Computer Modern |
| Citation style | `\bibliographystyle{}` — university specifies (Harvard, APA, IEEE, etc.) |
| Appendix format | Check if university wants lettered (A, B, C) or numbered |

---

## Workflow: End-to-End

### Step-by-Step Execution

```
1. UNDERSTAND THE PROJECT
   - Read the codebase, results, existing docs
   - Identify the core contribution

2. PLAN THE REPORT
   - Define chapter structure
   - Map: which data → which chapter
   - Identify figures needed
   - Create the execution plan

3. WAVE 0: DATA PREPARATION
   - Launch 5-6 parallel agents
   - Wait for ALL to complete
   - Verify outputs (spot-check numbers)

4. WAVE 1: CHAPTER WRITING
   - Launch 3-4 parallel agents
   - Each agent gets: chapter template + relevant Wave 0 data
   - Independent chapters can run in parallel

5. WAVE 2: ASSEMBLY
   - Merge chapters into main.tex
   - Run cross_ref_audit.py
   - Fix duplicate labels, undefined refs
   - Compile with tectonic
   - Quality review

6. ITERATE
   - Author reviews output
   - Targeted revisions (specific chapters/sections)
   - Re-compile and verify
```

### Time Estimates (Based on Validated Run)

| Wave | Agents | Typical Duration | Notes |
|------|:------:|:----------------:|-------|
| Wave 0 | 5-6 | 30-60 min | Depends on codebase size |
| Wave 1 | 3-4 | 60-90 min | Longest wave |
| Wave 2 | 1-2 | 20-40 min | Mostly automated |
| **Total** | | **2-4 hours** | For ~80 page report |

Without parallel agents, the same report takes 8-12 hours.

---

## Key Lessons (From Production Use)

1. **Data before prose**: Agents write poorly without concrete numbers. Wave 0 is essential.
2. **Tectonic over BasicTeX**: `brew install tectonic` — no sudo, handles packages automatically.
3. **Cross-ref audit is mandatory**: Parallel agents create duplicate labels. Automated script catches them.
4. **Figure pipeline separate**: Generate all figures first, reference later. Don't embed matplotlib in chapter agents.
5. **Honest limitations**: Explicitly prompt for limitations — Claude undersells weaknesses by default.
6. **zsh gotcha**: `grep '!'` breaks in zsh due to history expansion. Use Python scripts for pattern matching.
7. **Plan file as source of truth**: Write the full execution plan before launching any agents.
8. **Spot-check Wave 0**: Don't blindly pass data artifacts to writing agents. Verify key numbers.

---

## Common Issues and Solutions

| Issue | Solution |
|-------|----------|
| Duplicate `\label{}` across chapters | Run `cross_ref_audit.py`, rename with chapter prefix |
| Missing package in tectonic | Tectonic auto-downloads; if stuck, try `tectonic -X compile` |
| Figures too large / overlapping text | Use `[width=0.85\textwidth]` and `[htbp]` float placement |
| BibTeX not resolving | Run tectonic twice, or check `.bib` file syntax |
| Inconsistent notation across chapters | Define macros in `preamble.tex`, shared across all `\input{}` files |
| Agent writes without evidence | Wave 0 completion gate — never skip data preparation |
| Abstract too long for university | Keep to word limit; conference 5-sentence formula still works |
| Examiner criticizes missing limitations | Use the explicit limitations prompting strategy |

---

## References

### Inherited from ml-paper-writing

| Document | Contents |
|----------|----------|
| [references/writing-guide.md](references/writing-guide.md) | Gopen & Swan 7 principles, micro-tips, word choice |
| [references/citation-workflow.md](references/citation-workflow.md) | Citation APIs, Python code, BibTeX management |

### New for write-report

| Document | Contents |
|----------|----------|
| [references/compilation-guide.md](references/compilation-guide.md) | Tectonic, latexmk, cross-ref audit, local compilation |
| [references/parallel-pipeline.md](references/parallel-pipeline.md) | Wave architecture, agent orchestration, dependency graph |
| [scripts/cross_ref_audit.py](scripts/cross_ref_audit.py) | Automated cross-reference and duplicate label checker |
| [templates/university-thesis/](templates/university-thesis/) | Generic university thesis LaTeX template |
