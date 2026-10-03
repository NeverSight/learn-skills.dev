---
name: manuscript-typography
description: 'Audit academic manuscripts for typographic design conventions: booktabs table style, caption placement, dashes/quotes, units and numbers, cross-reference style, page layout, typographic hierarchy, professional polish. Triggers on: "check typography", "fix formatting", "polish my paper", "check my LaTeX", "typographic review", "make it look professional", "check tables", "fix captions". Companion to manuscript-review (content) and arxiv-preflight (compliance).'
metadata:
  version: 1.0.0
  complements: [manuscript-review, arxiv-preflight, figure-table-quality]
  category: review
  tags: [typography, latex, formatting, booktabs, polish]
  difficulty: advanced
  phase: review
---

# Manuscript Typography Audit

**Pipeline position:** Phase 2b (polish audit). Runs in parallel with
manuscript-provenance. Depends on: content settled after Phase 1 fixes.
See `/manuscript-pipeline` for full execution order.

## Purpose

Audit a LaTeX manuscript for widely-accepted academic typographic conventions
that directly affect readability and professional appearance. These are not
venue-specific formatting rules — they are cross-venue norms from decades of
academic publishing that experienced readers and reviewers notice.

A paper with solid content but poor typography signals inexperience. Reviewers
form impressions from visual presentation before reading a single sentence.

## Relationship to Other Skills

| Concern | manuscript-review | manuscript-typography (this) | arxiv-preflight |
|---------|-------------------|------------------------------|-----------------|
| Table content | Data quality, significant figures (§12) | Design: booktabs, alignment, headers, caption placement | Format compliance |
| Figure content | Colorblind, axis labels, chartjunk (§12) | Design: font matching, backgrounds, subfigure style | Format/size compliance |
| Rendered output | Legibility, float proximity, page breaks (§23) | Layout: widows, column balance, spacing, float specifiers | N/A |
| Math notation | Notation consistency, operator formatting (§15) | Spacing, delimiter sizing, display vs inline choices | N/A |
| Cross-refs | Citation hygiene (§11) | Reference style consistency, non-breaking spaces | N/A |
| Typography | N/A | Dashes, quotes, units, micro-typography | N/A |
| Polish | N/A | TODOs, placeholders, metadata, bookmarks | N/A |

**Rule:** This skill audits design and typography. manuscript-review audits
content and communication. arxiv-preflight audits submission compliance.
No overlap — each reads different signals from the same document.

## Workflow

### 1. Ingest

Read all `.tex` files (main + `\input`/`\include` targets). Identify:
- Document class and loaded packages
- Two-column vs single-column layout
- Target venue (if identifiable from class/template)

If compiled PDF is available, use it for rendered inspection checks.

### 2. Audit Passes

For each check:
- **FAIL** — convention violated (document file, line, specific fix with LaTeX code)
- **WARN** — debatable but worth considering
- **PASS** — convention followed
- **N/A** — not applicable

---

### Pass 1 — Table Design

**1.1 Rule structure**
- Use `booktabs` package: `\toprule`, `\midrule`, `\bottomrule`
- No `\hline` (replace with booktabs equivalents)
- No vertical rules (`|` in column spec) — vertical lines in tables are a hallmark of amateur typesetting
- No double horizontal rules
- Exception: if the document class mandates a specific table style, note but don't flag

```latex
% BAD
\begin{tabular}{|l|c|r|}
\hline
Method & Accuracy & F1 \\
\hline\hline
Ours & 0.94 & 0.91 \\
\hline
\end{tabular}

% GOOD
\begin{tabular}{lcr}
\toprule
Method & Accuracy & F1 \\
\midrule
Ours & 0.94 & 0.91 \\
\bottomrule
\end{tabular}
```

**1.2 Column alignment**
- Numeric columns: right-aligned or decimal-aligned (`S` column from `siunitx`)
- Text columns: left-aligned
- Center alignment: only for single characters or very short labels
- Header alignment: matches column alignment or centered

**1.3 Header formatting**
- Headers visually distinct from body (bold is standard: `\textbf{}`)
- No ALL CAPS headers (use bold or small caps)
- Units in headers: parenthesized or bracketed — `Latency (ms)` not `Latency ms`

**1.4 Best-result indication**
- If highlighting best results: consistent method across all tables (bold, underline, or marker)
- Define the convention in the first table's caption or a footnote
- Do not mix bold-for-best and underline-for-best across tables

**1.5 Table notes**
- Footnotes/notes below the table, not in the caption
- Use `\tablenotes` (threeparttable) or manual footnotes with consistent markers

**1.6 Caption placement**
- Table captions ABOVE the table (universal convention)
- `\caption{}` before `\begin{tabular}`
- Not below — below is for figures

**1.7 Caption formatting**
- Caption label ("Table 1:" / "Table 1.") in **bold** or **small caps** — visually distinct from the description text
- Caption description text smaller than body text — `\small` (one step down) is standard; `\footnotesize` acceptable
- Use the `caption` package to control this consistently:

```latex
\usepackage[font=small, labelfont=bf]{caption}
% label ("Table 1:") = bold, description = \small
% applies uniformly to all figures AND tables
```

- Never caption text at full body size — it visually competes with the main text and makes the document look untypeset
- Never caption text below `\footnotesize` — becomes unreadable
- Consistent across ALL captions (tables and figures use the same size/weight scheme)

**1.8 Caption style**
- Consistent prefix: "Table 1:" or "Table 1." — not mixed (controlled by `labelsep` in `caption` package)
- First sentence describes what the table shows
- Caption is self-contained (interpretable without body text)

**1.9 Spacing**
- `\addlinespace` (booktabs) for logical row groups, not empty rows
- No `\\[6pt]` manual spacing hacks inside tables
- Column separation adequate — use `@{\hspace{...}}` or `\setlength{\tabcolsep}` if too compressed

**1.10 Long tables**
- Tables exceeding one page: use `longtable` or `supertabular`
- Repeated headers on continuation pages
- No font-size reduction to force a table onto one page (below `\small` is unreadable)

---

### Pass 2 — Figure Design

**2.1 Caption placement**
- Figure captions BELOW the figure (universal convention)
- `\caption{}` after `\includegraphics`
- Not above — above is for tables

**2.2 Caption formatting**
- Same size/weight scheme as table captions — the `caption` package applies uniformly
- Caption label ("Figure 1:") bold or small caps (matches table label style)
- Caption description text at `\small` or `\footnotesize` (matches table caption size)
- If not using `caption` package: verify manually that figure and table captions use identical formatting

**2.3 Caption style**
- Consistent prefix: "Figure 1:" or "Figure 1." or "Fig. 1:" — pick one for all figures
- Matches table caption style (if tables use "Table 1:", figures use "Figure 1:")
- Caption self-contained

**2.4 Subfigure labeling**
- Consistent style: (a), (b), (c) — not mixed with (i), (ii), (iii) or a), b), c)
- Use `subcaption` or `subfigure` package — not manual lettering
- Subfigure labels referenced consistently in text: "Figure 1(a)" not "Figure 1a" or "Figure 1 (a)" mixed

**2.5 Font consistency**
- Text within figures (axis labels, annotations, legends) uses a font that complements the body text
- Matching the body serif (Computer Modern, Times) or a clean sans-serif (Helvetica, CMSans) is standard
- Matplotlib/R/MATLAB default fonts are visually distinct from LaTeX body text — flag when obvious
- Font size in figures after scaling: readable at rendered size (cross-reference with manuscript-review §23)
- Figure-internal text should be comparable to caption text size — not larger than body text, not smaller than footnotes

**2.6 Background**
- White or transparent background — no gray plot backgrounds (matplotlib default `axes.facecolor`)
- No colored frame/border unless it serves a purpose

**2.7 Aspect ratio**
- Plots not stretched or compressed
- Standard aspect ratios: 4:3, 16:9, golden ratio, or square
- All panels in a multi-panel figure use the same aspect ratio

**2.8 Consistent framing**
- All figures use the same border/frame approach (all framed or all unframed)
- Consistent padding/margins around figure content

---

### Pass 3 — LaTeX Typography

**3.1 Dashes**
- Hyphen (`-`): compound words (well-known, state-of-the-art)
- En-dash (`--`): number ranges (10--20, pages 5--12, 2020--2023). Common error: hyphen used for ranges ("10-20" → "10--20").
- Em-dash (`---`): parenthetical asides and emphatic breaks. Em-dashes are accepted by CMOS 18, APA 7, and MLA 9 in academic prose — flag the following instead of banning the character:
  - **Spacing inconsistency:** CMOS/APA/MLA use closed em-dashes (`text---text`); journalistic AP style uses spaced (`text --- text`). Pick one and apply uniformly. Mixed usage = FAIL.
  - **Overuse:** more than ~1 em-dash per paragraph or ~3 per page tips into conversational register. Flag clusters as WARN; suggest restructuring to commas/colons/parentheses.
  - **Misuse for ranges:** em-dash where en-dash belongs (`pages 5---12` should be `pages 5--12`) = FAIL.
  - **AI-tell heuristic (advisory only, MEDIUM):** dense em-dash usage combined with other AI-pattern markers can indicate unedited LLM output. Defer to `manuscript-review` Pass 7b for that judgment, do not flag em-dashes alone as AI tells.

**3.2 Quotation marks**
- Opening: ` `` ` (backticks)
- Closing: `''` (straight single quotes)
- Not `"straight quotes"` — renders incorrectly in TeX
- Nested: `` `inner' `` inside `` ``outer'' ``

**3.3 Ellipsis**
- `\ldots` or `\dots` — not three periods (`...`)
- `\ldots` produces properly spaced ellipsis

**3.4 Non-breaking spaces**
- Before `\ref`: `Figure~\ref{fig:x}`, `Table~\ref{tab:x}`, `Section~\ref{sec:x}`
- Before `\cite`: `previous work~\cite{smith2020}`
- Between number and unit: `10~ms` or `10\,ms`
- Prevents line breaks that separate a label from its referent

**3.5 Ties and thin spaces**
- Thin space between number and unit: `10\,ms`, `5\,GB`, `100\,K` (use `siunitx` for consistency)
- No space inside parenthetical citations: `\cite{x}` not `\cite{ x }`
- No double spaces in source (harmless but untidy)

**3.6 Semantic markup**
- `\emph{text}` over `{\it text}` or `\textit{text}` — `\emph` nests correctly
- `\textbf{}` for bold, not `{\bf }`
- New-style font commands (`\textbf`, `\textit`, `\textsf`) over old-style (`\bf`, `\it`, `\sf`)
- `\textrm{}` for roman text inside math mode, not manual font switches

**3.7 Micro-typography**
- `\usepackage{microtype}` — enables character protrusion and font expansion
- Dramatically improves line breaking and margin alignment with zero effort
- If not loaded, recommend adding it

**3.8 Special characters**
- `\&` not `&` in text
- `\%` not `%` in text
- `\#` not `#` in text
- `\_` not `_` in text
- Degree symbol: `$^\circ$` or `\textdegree` — not `°` (Unicode)
- Multiplication: `$\times$` — not `x`

**3.9 Ligatures**
- ff, fi, fl, ffi, ffl must render as proper ligatures (default in CM/Latin Modern fonts)
- Flag if `\DisableLigatures` or `microtype` `ligatures=false` is set globally without reason
- Some fonts break ligatures — if text renders "ﬁnd" as "f ind" or similar, the font config is wrong
- Ligatures should NOT cross morpheme boundaries in some compound words (e.g., "shelfful") — minor, WARN only

**3.10 Italic usage — three distinct purposes**
- **Emphasis:** `\emph{important}` — for stress within a sentence
- **Foreign words:** `\textit{in vivo}`, `\textit{a priori}` — for non-English terms not yet naturalized
- **Terms being defined:** `\textit{A convolutional layer is...}` — for the first occurrence of a technical term being introduced
- Using bold, ALL CAPS, or colored text for emphasis in running prose = FAIL
- Consistent: if "in vitro" is italicized on page 3, it must be italicized everywhere (or nowhere if treated as naturalized)

**3.11 No color for emphasis**
- Colored text in running prose for emphasis (red for important, blue for terms) = FAIL
- Color belongs in figures, tables, and hyperlinks — not in body text
- Exception: `hyperref` link colors for cross-references and URLs

**3.12 Sentence spacing**
- LaTeX default: extra space after periods (end-of-sentence). This is traditional TeX behavior.
- `\frenchspacing` disables it (uniform spacing). Both are acceptable — but be deliberate.
- If using abbreviations with periods (e.g., "et al.", "Fig.", "vs.") without `\frenchspacing`, add `\ ` or `~` after the period to prevent LaTeX from treating it as end-of-sentence: `et al.\ ` or use `\@.` before a true sentence-ending period after a capital letter.
- Common bug: "...by Dr. Smith" — LaTeX adds extra space after "Dr." thinking it's end-of-sentence. Fix: `Dr.\ Smith`

**3.13 Display vs inline math**
- Expressions with fractions (`\frac`), sums (`\sum`), products (`\prod`), integrals, or matrices should be displayed, not inline — inline rendering compresses them and disrupts line spacing
- Short expressions (single variables, simple subscripts, brief equalities like `$x = 5$`) stay inline
- Rule of thumb: if the expression changes the line height, display it
- Display equations that are part of a sentence still need proper punctuation
- `\[ ... \]` or `equation` environment — not `$$ ... $$` (which is plain TeX, not LaTeX, and has incorrect spacing)

**3.14 URL handling**
- URLs in `\url{}` or `\href{}` — never bare text or `\texttt{}`
- `\url{}` enables line breaking at appropriate characters (/, ., -, etc.)
- `\texttt{https://...}` does NOT break across lines → overfull boxes
- Load `url` or `hyperref` package (hyperref includes url functionality)
- If `hyperref` is loaded: verify `breaklinks=true` is set in `\hypersetup`
- Long URLs in bibliography entries need additional break points. Check for `\UrlBreaks`:
```latex
\makeatletter
\g@addto@macro{\UrlBreaks}{\UrlOrds}
\makeatother
```
- Without this, URLs with long path segments (common in blog posts and documentation) will overflow margins in the bibliography even when wrapped in `\url{}`

---

### Pass 4 — Units and Numbers

**4.1 Number-unit spacing**
- Space between number and unit: "10 ms" not "10ms"
- Best: `siunitx` package — `\SI{10}{\milli\second}` or `\qty{10}{ms}`
- Consistent across the entire document
- Exception: percentages and degrees can touch the number (convention varies — pick one and stick to it)

**4.2 Unit typography**
- Units in upright/roman font, not italic: "10 ms" not "10 *ms*"
- In math mode: `$t = 10\,\mathrm{ms}$` not `$t = 10\,ms$` (italic)
- Compound units: `m/s` or `m\,s$^{-1}$` — consistent style

**4.3 Number formatting**
- Consistent decimal separator (period in English)
- Large numbers: consistent thousands separator (comma, thin space, or none)
- Ranges: en-dash (`10--20`) not hyphen (`10-20`)
- Negative numbers: proper minus (`$-5$`) not hyphen (`-5`) in running text

**4.4 Significant figures**
- Same metric → same number of decimal places across all tables and text
- Cross-reference with manuscript-review §12 (content consistency)
- Precision should not exceed measurement precision

**4.5 Percentages**
- Consistent: "14.3%" or "14.3 %" — pick one
- "Percentage points" vs "percent" distinction when comparing percentages

**4.6 Inline fractions**
- In running text: `\nicefrac{1}{2}` or `\sfrac{1}{2}` (from `xfrac`) — not `$\frac{1}{2}$`
- `$\frac{}{}$` inline disrupts line spacing by creating a tall element
- Display fractions (`\frac`) are correct in display math and equations
- Alternative: "1/2" is acceptable in informal contexts — consistent style across document

---

### Pass 5 — Cross-References and Citations

**5.1 Reference abbreviation consistency**
- Pick one and use it everywhere:
  - Full: "Figure", "Table", "Section", "Equation"
  - Abbreviated: "Fig.", "Tab.", "Sec.", "Eq."
  - Mixed within the same category is a FAIL
- Common convention: abbreviated in parentheticals, full in running prose
  ("As shown in Fig. 1" but "Figure 1 shows...")

**5.2 Non-breaking spaces**
- `Figure~\ref{fig:x}` — prevents "Figure" at end of line, "3" at start of next
- `Eq.~\eqref{eq:x}` — same
- This is the single most common LaTeX typography mistake

**5.3 Equation references**
- Consistent: parenthesized `(\ref{eq:x})` or `\eqref{eq:x}` — not mixed
- Consistent: "Equation (1)" or "Eq. (1)" or "(1)" — pick one

**5.4 Citation style**
- Consistent bracket style throughout (author-year or numeric — determined by `\bibliographystyle`)
- No manual citation formatting (`[1]` hardcoded) — always `\cite`
- Multiple citations in one bracket: `\cite{a,b,c}` not `\cite{a}\cite{b}\cite{c}`
- Citation-text integration: "Smith et al. \cite{smith}" or "\citet{smith}" — not both styles

**5.5 Latin abbreviations and common shorthands**
- "e.g.," and "i.e.," — always followed by a comma (CMOS). Consistent across document.
- "et al." — period after "al" (it's an abbreviation of "alia"). No italics (naturalized).
- "vs." — period after. "Versus" in formal prose, "vs." in parentheticals and tables.
- "cf." — period after. Means "compare," not "see."
- "etc." — period after. Avoid in formal academic prose (prefer explicit enumeration).
- If not using `\frenchspacing`: add `\ ` after abbreviation periods mid-sentence to prevent extra spacing (see 3.12)

**5.6 Hyperref consistency**
- If using `hyperref`: link colors consistent (all blue, all black, or all boxed)
- No mix of colored and non-colored cross-references
- Link targets resolve correctly (no "??" in output)

---

### Pass 6 — Page Layout and Spacing

**6.1 Float specifiers**
- Prefer `[htbp]` over `[H]` — `[H]` forces placement and often creates bad page breaks with large whitespace gaps
- `[t]` or `[tb]` acceptable for top/bottom placement
- `[h]` alone is fragile (LaTeX often ignores it)
- No `[h!]` or `[H]` unless there is a specific reason

**6.2 Widow and orphan control**
- No single line of a paragraph stranded at top of page (widow) or bottom of page (orphan)
- `\widowpenalty=10000` and `\clubpenalty=10000` in preamble
- Or per-instance `\needspace` commands

**6.3 Column balance** (two-column layouts)
- Final page: columns balanced (use `\usepackage{balance}` or `\usepackage{flushend}`)
- Unbalanced final page (full left, empty right) looks unfinished

**6.4 Manual spacing**
- Flag excessive `\vspace{}`, `\hspace{}`, `\\[Xpt]`, `\bigskip`, `\smallskip`
- These are band-aids for layout problems that should be solved structurally
- Acceptable: minimal use in specific float or title contexts

**6.5 Page breaks**
- No `\newpage` or `\clearpage` in the middle of sections without justification
- `\clearpage` before bibliography is acceptable

**6.6 Paragraph spacing vs indentation**
- Standard LaTeX: paragraph indentation + no extra spacing (default)
- Alternative: no indentation + vertical spacing (`\usepackage{parskip}`)
- Mixing both (indentation AND extra spacing) is a FAIL — pick one

**6.7 Paragraph indentation size**
- Standard: 1em to 1.5em (LaTeX default `\parindent` is ~1.5em)
- Too large (>2em): wastes space and looks exaggerated
- Too small (<0.5em): indentation is invisible and fails its purpose
- Do not manually set `\parindent` to unusual values without reason

**6.8 First paragraph after heading**
- First paragraph after a section/subsection heading should NOT be indented (LaTeX default behavior)
- If someone adds `\indent` or `\hspace{\parindent}` to first paragraphs: FAIL
- If a package or manual setting indents first paragraphs (`\usepackage{indentfirst}`): WARN — non-standard in English academic typesetting. Standard in French/some European traditions — acceptable if intentional.

**6.9 Line spacing / leading**
- Standard: single spacing with the line height set by the document class (default `\baselinestretch` = 1.0)
- Double-spacing via `\linespread{1.6}` or `\usepackage[doublespacing]{setspace}` = FAIL for submission — this is referee/draft mode, not camera-ready
- If the document class is `article` and double-spacing is active, flag it — likely a forgotten draft setting
- `\linespread{1.05}` to `\linespread{1.1}` is acceptable fine-tuning for some fonts

**6.10 Line length / characters per line**
- Optimal: 45--75 characters per line (Bringhurst). 66 is ideal.
- Two-column layouts at standard column widths (~3.3 inches / 84mm) naturally achieve this
- Single-column layouts with narrow margins can exceed 90 characters per line → reduced readability
- Fix: wider margins, or switch to two-column, or use `\usepackage{geometry}` to set appropriate text width
- If the document class sets the margins (most conference classes do), do not override

**6.11 Deferred float accumulation**
- Read the compiled PDF. Check whether floats (tables, figures) from earlier subsections
  land in the middle of a later subsection, breaking paragraph continuity.
- Symptom: a sentence starts, then 1+ pages of floats appear, then the sentence continues.
  The reader loses the thread.
- Common cause: many `[t]` floats in a section with dense content. LaTeX defers floats it
  cannot place, and they pile into the next available space.
- Diagnosis: count pending floats at each subsection boundary. If floats from subsection N
  appear after the start of subsection N+2 or later, flag as FAIL.
- Fix: add `\usepackage{placeins}` and insert `\FloatBarrier` before subsections that
  should start with clean text flow (especially methodology/statistics/discussion sections
  that follow data-heavy sections with many floats).
- Alternative: `\usepackage[section]{placeins}` prevents floats from crossing `\section`
  boundaries automatically. For `\subsection`-level control, manual `\FloatBarrier` is needed.
- Do NOT fix by changing all floats to `[H]` — this creates worse layout problems (large
  whitespace gaps). `\FloatBarrier` at strategic points is the correct solution.
- Category: AUTO-FIX (add `\usepackage{placeins}` + `\FloatBarrier` before affected subsections)

**6.12 Consecutive hyphenated lines**
- More than 2--3 consecutive line-ending hyphens = visual defect ("pig bristle" or "ladder" in typography)
- Fix: `\hyphenpenalty=50` (default), increase to reduce hyphenation frequency, or rephrase locally
- `\usepackage[none]{hyphenat}` disables hyphenation entirely — rarely desirable in academic text
- `\hyphenation{spe-ci-fic-word}` for individual problem words

---

### Pass 7 — Code and Algorithms

**7.1 Inline code**
- Use `\texttt{}` or `\verb||` for inline code/identifiers
- Consistent: all inline code uses the same formatting
- Not: sometimes typewriter, sometimes italic, sometimes nothing

**7.2 Code listings**
- Use `listings` or `minted` package — not manual `\texttt` blocks
- Consistent syntax highlighting style
- Line numbers if code lines are referenced in text
- Font size: `\small` or `\footnotesize` — not body size (too large) or `\scriptsize` (too small)

**7.3 Algorithm pseudocode**
- Use `algorithm2e`, `algorithmic`, or `algorithmicx` package
- Consistent indentation
- Line numbering if referenced
- Input/output clearly stated
- Caption above (follows table convention — algorithms are procedural tables)

---

### Pass 8 — Typographic Hierarchy

The document's font sizes and weights must form a clear visual hierarchy.
Readers unconsciously use size/weight differences to parse document structure.
When elements are the same size, the hierarchy collapses and the page looks flat.

**8.1 Size hierarchy reference**

Standard academic LaTeX size hierarchy (relative to body text):

| Element | Size relative to body | Weight | Style |
|---------|----------------------|--------|-------|
| Chapter/Part title | +4--6pt | Bold | Roman |
| Section heading | +2--3pt | Bold | Roman |
| Subsection heading | +1--2pt | Bold | Roman |
| Subsubsection heading | same as body | Bold or italic | Roman |
| Body text | base (10pt, 11pt, or 12pt) | Normal | Roman |
| Caption label ("Figure 1:") | 1 step below body (`\small`) | **Bold** | Roman |
| Caption description | 1 step below body (`\small`) | Normal | Roman |
| Table body text | same as body or `\small` | Normal | Roman |
| Figure-internal text | comparable to caption size | Normal | Sans-serif or body font |
| Footnotes | 2 steps below body (`\footnotesize`) | Normal | Roman |
| Code listings | 1--2 steps below body | Normal | Monospace |
| Header/footer | 1--2 steps below body | Normal | Roman or italic |

Most document classes set this hierarchy automatically. The skill checks
that the author hasn't overridden it incorrectly.

**8.2 Caption size must be smaller than body**
- Captions at full body size (e.g., 12pt captions with 12pt body) = FAIL
- Captions should be 1 step down: `\small` (10.95pt for 12pt body, 9.5pt for 11pt, 9pt for 10pt)
- `\footnotesize` is also acceptable (slightly smaller)
- The `caption` package is the correct way to enforce this:

```latex
% Standard professional setup
\usepackage[font=small, labelfont=bf]{caption}

% Alternative: slightly smaller
\usepackage[font=footnotesize, labelfont=bf]{caption}

% With label separator control
\usepackage[font=small, labelfont=bf, labelsep=period]{caption}
% produces "Figure 1. Description" with bold "Figure 1."
```

**8.3 Caption label must be visually distinct from description**
- Label ("Table 1:" / "Figure 1.") in **bold** — this is the dominant convention
- Alternatives: small caps (`labelfont=sc`) or bold small caps
- Label at the same weight as description text = FAIL — the reader can't quickly find the figure number
- The label is a reference anchor; the description is prose. They serve different functions and must look different.

**8.4 Heading weight and size decrease with depth**
- `\section` > `\subsection` > `\subsubsection` in both size and visual weight
- If the document class provides this (most do), do not override with manual font commands
- Manual `{\Large\textbf{...}}` instead of `\section{}` = FAIL — breaks numbering, bookmarks, and TOC

**8.5 Footnote size**
- Footnotes should be smaller than body text (standard LaTeX default: `\footnotesize`)
- Footnotes at body size = FAIL
- Footnote reference markers: superscript numbers (default) — consistent style

**8.6 Table body text size**
- Table body text at same size as body text or one step down (`\small`)
- Tables should NOT be at `\footnotesize` or smaller to fit — redesign the table instead (fewer columns, abbreviate headers, split into two tables)
- Exception: appendix tables with many columns where space is genuinely constrained — `\small` is the floor

**8.7 Header/footer text**
- Running headers/footers at smaller size than body (standard in most document classes)
- Manual headers at body size = visual noise competing with content

**8.8 No manual font-size overrides in body**
- Flag `{\large ...}` or `{\Large ...}` in running text (not headings)
- Flag `{\small ...}` wrapping entire sections to fit page limits
- These override the hierarchy and create visual inconsistency
- Exception: `\small` inside specific floats/environments is acceptable

---

### Pass 9 — Professional Polish

**9.1 Placeholder detection**
- No "TODO", "FIXME", "XXX", "PLACEHOLDER", "TBD" in any `.tex` file
- No "Lorem ipsum" or filler text
- No commented-out paragraphs that are clearly draft remnants (as opposed to intentional version tracking)

**9.2 PDF metadata** (if PDF available)
- Title set in PDF properties (not "main.tex" or blank)
- Author set in PDF properties
- `\hypersetup{pdftitle={...}, pdfauthor={...}}` configured

**9.3 PDF bookmarks**
- `hyperref` loaded with bookmarks enabled (default)
- Section structure navigable via PDF reader sidebar
- Bookmark text matches section titles

**9.4 Consistent package loading**
- No duplicate `\usepackage` calls for the same package
- No conflicting package options
- Package loading order follows conventions (hyperref last or near-last)

**9.5 Overfull/underfull box warnings (MANDATORY — do not skip)**
- Read the `.log` file (same name as main tex, e.g., `main.log` or `yuj.log`)
- Grep for `Overfull \\hbox` — each is text extending past the margin
- Report every instance with the line number and badness value
- Common causes: long URLs in bibliography, unbreakable inline math, wide `\resizebox` tables, long `\texttt{}` strings
- Fix per cause:
  - URLs: `breaklinks=true` + `\UrlBreaks{\UrlOrds}` (see 3.14)
  - Inline math: break with `\allowbreak` or move to display
  - Tables: check `\resizebox` scaling, consider `\small` or redesign
  - `\texttt{}`: replace with `\url{}` for URLs, add `\allowbreak` for paths
- Also check for `Underfull \\hbox` with badness > 5000 — these produce visibly loose lines

**9.6 Unresolved references**
- No `??` in rendered output from unresolved `\ref` or `\cite`
- No `[?]` from missing bibliography entries
- Check `.log` for "Reference ... undefined" and "Citation ... undefined"

---

### 3. Generate Report

```markdown
# Typography Audit Report

**Manuscript:** [main tex file]
**Document class:** [detected class]
**Layout:** [single/two-column]
**Date:** [date]
**Verdict:** [Professional | Needs Polish | Significant Issues]

## Summary

| Category | Pass | Fail | Warn |
|----------|------|------|------|
| Table Design | | | |
| Figure Design | | | |
| LaTeX Typography | | | |
| Units & Numbers | | | |
| Cross-References | | | |
| Page Layout | | | |
| Code & Algorithms | | | |
| Typographic Hierarchy | | | |
| Professional Polish | | | |

## Fixes (ordered by impact)

### High Impact (visual professionalism)

[Issues that experienced readers/reviewers will notice immediately]

### Medium Impact (readability)

[Issues that affect reading experience but may not be consciously noticed]

### Low Impact (polish)

[Micro-issues that matter for camera-ready / final versions]

## Quick Fixes

[One-line fixes: add microtype, add booktabs, fix non-breaking spaces —
 items that take <1 minute each and improve the document noticeably]
```

### 4. Output

Save report as `[manuscript-name]-typography-report.md` in the project directory.

Present:
- Verdict
- Count of high/medium/low issues
- Top 5 quick fixes (highest impact for least effort)
- Specific LaTeX code for each fix

## LaTeX Quick-Fix Reference

Common one-line preamble additions that resolve multiple issues:

```latex
% Micro-typography: better line breaks, margin alignment
\usepackage{microtype}

% Professional tables: \toprule, \midrule, \bottomrule
\usepackage{booktabs}

% Proper SI units: \SI{10}{\milli\second}
\usepackage{siunitx}

% Subfigures with consistent labeling
\usepackage[labelformat=parens]{subcaption}

% Widow/orphan prevention
\widowpenalty=10000
\clubpenalty=10000

% Two-column balance on last page
\usepackage{balance}  % add \balance before \bibliography

% Caption formatting: bold label, small text
\usepackage[font=small, labelfont=bf]{caption}

% Inline fractions: \nicefrac{1}{2}
\usepackage{nicefrac}

% PDF metadata
\hypersetup{
  pdftitle={Your Paper Title},
  pdfauthor={Author Names},
}
```

## Core Principles

- **Conventions, not preferences.** Every check in this audit reflects a norm
  practiced by the majority of well-typeset academic papers across venues.
  Where conventions genuinely vary (e.g., percentage spacing), flag as WARN
  with both options and ask for consistency.

- **Document class awareness.** Some document classes override default
  conventions (e.g., `IEEEtran` has its own table style). When the class
  dictates a style, follow it — do not impose conflicting conventions.

- **Fix the source, not the symptom.** `\vspace{-3mm}` to fix spacing is a
  symptom-level hack. Fixing the float specifier or package configuration
  that caused the bad spacing is the real fix.

- **Quick wins first.** The report prioritizes fixes by impact-to-effort ratio.
  Adding `\usepackage{microtype}` takes 5 seconds and improves every page.
  That goes before suggestions to redesign all tables.

- **No style imposition.** This skill does not enforce "my preferred style."
  It enforces consistency within the document and adherence to conventions
  that have broad consensus. Where the author has made a deliberate,
  consistent choice, respect it.
