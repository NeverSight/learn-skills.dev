---
name: academic-researcher
description: Expert-level academic research and LaTeX paper writing with IEEE/APA citation support. Creates peer-reviewed research papers, literature reviews, and theses with proper scholarly standards.
license: MIT
compatibility: opencode, claude-code, gemini-cli, codex
metadata:
  audience: researchers, academics, graduate-students
  workflow: research-paper-writing
  fields: computer-science, stem, social-sciences, humanities
---

## What I Do

I help you create expert-level academic research documents with:
- Peer-reviewed source discovery and verification
- Proper IMRaD structure and academic writing conventions
- IEEE (primary) and APA (secondary) citation formats
- LaTeX output for professional mathematical typesetting
- Quality assurance against scholarly standards

## Non-Negotiables (Research Integrity)

- **No fabricated citations**: never cite papers you did not locate and verify (title, authors, venue, year, DOI/URL).
- **Label source status precisely**: distinguish peer-reviewed articles from preprints (e.g., arXiv) and from non-academic web sources.
- **Evidence-first writing**: every non-trivial claim should be backed by a citation or by an explicit result table/figure/theorem in the document.
- **Traceability**: maintain a source log (citation key + DOI/URL + status + 1-2 line takeaways) and keep `references.bib` as the single source of truth.

## When to Use Me

Use this skill when you need to write:
- **Research papers** for conferences (IEEE, ACM) or journals
- **Literature reviews** and survey papers
- **Theses/dissertations** (master's or PhD)
- **Research proposals** and grant applications
- **Technical reports** with academic rigor

## Workflow Overview

```
Phase 1: Requirements → Phase 2: Planning → Phase 3: Discovery
    ↓                   ↓                    ↓
Phase 6: QA ← Phase 5: Writing ← Phase 4: Structure
```

---

## Phase 1: Requirements Clarification

Before starting, clarify with the user:

### Essential Questions

1. **Document Type**
   - Research paper (conference/journal)?
   - Literature review / survey?
   - Thesis / dissertation chapter?
   - Research proposal?

2. **Topic & Scope**
   - What is the main research question or contribution?
   - What is the target word count or page limit?
   - Any specific research questions to address?

3. **Target Venue**
   - Which conference or journal?
   - Any specific formatting requirements?
   - Submission deadline?

4. **Citation Format**
   - IEEE (default for CS/Engineering)?
   - APA (social sciences)?
   - Other (ACM, Chicago)?

### User Input Template

```markdown
## Research Document Request

**Type:** [Research Paper / Literature Review / Thesis]
**Topic:** [Your research topic]
**Target:** [Conference/Journal name or "General"]
**Length:** [X pages or X words]
**Citation:** [IEEE / APA / Other]
**Deadline:** [Date if applicable]
**Special Requirements:** [Any specific guidelines]
```

---

## Phase 2: Research Planning

### Search Strategy Development

1. **Identify core concepts** - Extract key terms from the topic
2. **Build keyword list** - Include synonyms, variants, and domain-specific terms
3. **Select databases** - Choose appropriate sources:

| Database | Best For |
|----------|----------|
| Google Scholar | Broad academic search |
| IEEE Xplore | Engineering, CS |
| ACM Digital Library | Computing |
| arXiv | Preprints, CS, physics |
| PubMed | Medicine, life sciences |
| ScienceDirect | General science |
| JSTOR | Humanities, social sciences |

### Search Command Patterns (Tool-Agnostic)

Use your platform's browsing/search tool. If browsing is unavailable, ask the user to provide PDFs/DOIs/URLs (or an existing `references.bib`) and proceed from those.

Query patterns to use:

- Broad first: `broad topic` + `survey` / `review`
- Recent window: add a year range (e.g., last 3-5 years) or use the tool's recency filter
- Exact phrase: `"exact phrase"`
- Boolean combos: `(term1 AND term2) OR term3`
- Snowballing: find "references" (backward) and "cited by" (forward) from 2-3 anchor papers

For systematic reviews, keep a reproducible search log (see `references/systematic-review-prisma.md`).

---

## Phase 3: Source Discovery & Verification

### Discovery Process

**Step 1: Foundational Sources**
- Search for seminal papers and foundational work
- Look for highly-cited papers (100+ citations)
- Find survey papers on the topic

**Step 2: Recent Work**
- Search for papers from last 2-3 years
- Look for "state of the art" reviews
- Find latest developments and advances

**Step 3: Related Work**
- Papers citing key foundational works
- Papers cited by recent major papers
- Parallel approaches and alternatives

### Verification Checklist

For each source, verify:

- [ ] Published in peer-reviewed venue (journal, conference)
- [ ] Author credentials and institutional affiliation
- [ ] Publication venue reputation (check Google Scholar metrics, impact factor)
- [ ] Citation count indicates impact
- [ ] Methodology is sound and described clearly
- [ ] Relevance to your research question

### Red Flags (Exclude These Sources)

- Predatory journals (check Beall's List or journalquality.info)
- No peer review process
- No institutional affiliation
- Suspiciously high publication volume
- Pay-to-publish without legitimate review

### Source Tracking

Create a source database (and keep `references.bib` as the single source of truth):

```markdown
## Source [N]
- **Citation Key:** [e.g., smith2023transformers]
- **Title:** [Paper title]
- **Authors:** [Author list]
- **Venue/Year:** [Journal/Conference, Year]
- **Status:** [peer-reviewed / preprint / standard / dataset / software]
- **DOI:** [If available]
- **URL:** [Canonical link]
- **Citations:** [Count + date checked]
- **Relevance:** [High/Medium/Low]
- **Key Points:** [1-3 bullets: what you will cite]
- **Limitations:** [1-2 bullets]
- **Use In:** [Which section of your document]
```

See `references/source-evaluation.md` and `references/bibliography-workflows.md`.

### Paper Access Strategy

When you find a relevant paper but cannot access the full text:

1. **Check open access first:**
   - Run `node scripts/resolve-papers.js --doi "10.xxxx/yyyy"` to find legal OA versions
   - Check arXiv (most CS papers have preprints)
   - Check PubMed Central (biomedical papers)
   - Check the authors' personal/lab websites (often host preprints)

2. **Use available metadata:**
   - Abstract + figures from the paper landing page are often sufficient for related-work sections
   - Semantic Scholar provides abstracts and citation context for free

3. **Ask the user:**
   - If a paper is critical and paywalled, ask the user to provide it
   - Users may have institutional access, interlibrary loan, or direct author contact

4. **Be transparent:**
   - If citing a paper you could only read the abstract of, note this limitation
   - Never fabricate content from a paper you haven't read

---

## Phase 4: Document Structure

### Research Paper Structure (IMRaD)

```
1. Title
2. Abstract (150-250 words)
3. Keywords (5-7 terms)
4. Introduction
   - Background and motivation
   - Problem statement
   - Research objectives
   - Contributions (3-5 bullet points)
   - Paper organization
5. Related Work / Literature Review
   - Thematic organization
   - Gap identification
6. Methodology / Approach
   - System design (if applicable)
   - Algorithm description
   - Technical approach
7. Results / Evaluation
   - Experimental setup
   - Metrics
   - Results presentation
8. Discussion
   - Interpretation
   - Implications
   - Limitations
9. Conclusion
   - Summary
   - Future work
10. References
```

### Literature Review Structure

```
1. Title
2. Abstract
3. Introduction
   - Review scope and objectives
   - Methodology (how sources were selected)
4. Thematic Sections (organized by themes)
5. Synthesis and Discussion
   - Trends and patterns
   - Gaps in literature
6. Conclusion
   - Summary
   - Future directions
7. References
```

### Systematic Review Structure (PRISMA-Style)

```
1. Title
2. Abstract
3. Introduction (scope + research questions)
4. Methods (protocol, databases, queries, screening, extraction, appraisal)
5. Results (selection counts + evidence tables + taxonomy)
6. Discussion (implications, limitations, threats to validity)
7. Conclusion (what is known + gaps + future directions)
8. References
9. Appendices (full queries, screening reasons, extraction schema)
```

See `references/systematic-review-prisma.md`.

### Thesis Structure

```
1. Abstract
2. Introduction
   - Background
   - Problem statement
   - Research questions
   - Thesis objectives
   - Contributions
3. Literature Review
   - Theoretical framework
   - Related work
   - Research gap
4. Methodology
   - Research design
   - Data collection
   - Analysis methods
5. Results/Findings
6. Discussion
7. Conclusion
8. References
9. Appendices
```

---

## Phase 5: Writing & LaTeX

### LaTeX Document Setup

For submission, prefer official publisher templates (see `references/official-templates.md`). The templates below are scaffolds for learning the structure.

Included templates:
- `references/templates/ieee-conference.tex` (IEEE conference paper)
- `references/templates/literature-review.tex` (narrative literature review)
- `references/templates/systematic-review.tex` (systematic review)
- `references/templates/thesis.tex` (thesis/dissertation)
- `references/templates/apa7-manuscript.tex` (APA 7 manuscript)
- `references/templates/research-proposal.tex` (research proposal)

Minimal IEEE skeleton (BibTeX):

```latex
\documentclass[conference]{IEEEtran}
\IEEEoverridecommandlockouts

\usepackage{cite}
\usepackage{amsmath,amssymb,amsfonts}
\usepackage{graphicx}
\usepackage{xcolor}

\title{Your Paper Title}

\author{
\IEEEauthorblockN{First Author}
\IEEEauthorblockA{Department, University\\
City, Country\\
email@example.edu}
}

\begin{document}
\maketitle

\begin{abstract}
Your abstract goes here (150--250 words).
\end{abstract}

\begin{IEEEkeywords}
keyword1, keyword2, keyword3
\end{IEEEkeywords}

\section{Introduction}
...

\bibliographystyle{IEEEtran}
\bibliography{references}
\end{document}
```

### Academic Writing Style

**Tone:**
- Formal and objective
- Use "we" for multi-author papers when describing your work (standard in CS/Engineering)
- Use third person for discussing other work ("Smith et al. proposed...")
- Precise technical terminology
- Present tense for established facts, past tense for specific studies

**Avoid:**
- Colloquial language
- Unsupported claims
- Excessive quotations (paraphrase instead)
- Vague terms ("very", "significant") without data

### Citation Integration

**IEEE Style (numbered):**
```latex
Recent work has shown this approach is effective \cite{smith2023}.
Multiple studies support this finding \cite{smith2023, jones2022, doe2021}.
```

**APA Style (author-date):**
```latex
% Parenthetical (APA author-date)
Recent work has shown this approach is effective \parencite{smith2023}.
Multiple studies support this finding \parencite{smith2023,jones2022}.

% Narrative
\textcite{smith2023} demonstrated this approach is effective.
```

### Paragraph Structure

Each paragraph should follow a clear pattern:
1. **Topic sentence** — state the main point
2. **Evidence/Support** — cite sources or present data
3. **Analysis** — explain what the evidence means
4. **Transition** — connect to the next paragraph

### Transition Patterns
- Contrast: "However," "In contrast," "While X focuses on..."
- Extension: "Building on this," "Furthermore," "Similarly,"
- Consequence: "As a result," "Therefore," "This suggests that"
- Gap: "Despite these advances," "However, X remains unexplored"

### Mathematical Typesetting

**Inline math:** `$E = mc^2$`

**Displayed equations:**
```latex
\begin{equation}
f(x) = \sum_{i=1}^{n} a_i x^i
\end{equation}
```

**Multi-line equations:**
```latex
\begin{align}
a &= b + c \\
  &= d + e + f
\end{align}
```

**Matrices:**
```latex
\begin{bmatrix}
a_{11} & a_{12} \\
a_{21} & a_{22}
\end{bmatrix}
```

**Proofs:**
```latex
\begin{proof}
Let $x$ be any element...
Therefore, we conclude...
\end{proof}
```

See `references/latex-math-guide.md` for more examples.

---

## Phase 6: Quality Assurance

### Pre-Submission Checklist

**Content:**
- [ ] Clear research question/objective
- [ ] Logical flow and organization
- [ ] Minimum 15-20 sources for full paper
- [ ] All sources verified and labeled (peer-reviewed vs preprint vs other)
- [ ] All claims supported by citations
- [ ] Methodology clearly explained
- [ ] Results clearly presented with metrics
- [ ] Limitations acknowledged
- [ ] Contributions clearly stated

**Technical (IEEE):**
- [ ] Reference format correct
- [ ] All citations match reference list
- [ ] No missing references
- [ ] Consistent citation numbering
- [ ] Figure/table captions complete
- [ ] Margins match venue requirements

**Writing Quality:**
- [ ] Academic tone maintained
- [ ] No grammatical errors
- [ ] Smooth transitions
- [ ] Abstract matches content
- [ ] Keywords present

**Evidence & Citations:**
- [ ] No invented citations; every reference is verifiable (title/authors/venue/year/DOI or canonical URL)
- [ ] Every citation key used in LaTeX exists in `references.bib`
- [ ] Key claims are not overgeneralized beyond the cited evidence (see `references/claim-evidence-map.md`)

**Reproducibility (If Empirical):**
- [ ] Dataset versions, splits, and preprocessing are specified
- [ ] Baseline selection and tuning budget fairness are stated
- [ ] Seeds/variance reporting policy is stated
- [ ] Compute and environment details are included (see `references/reproducibility-checklist.md`)

**Statistics (If Applicable):**
- [ ] Uncertainty is reported where appropriate (CIs/SE/bootstrap)
- [ ] Statistical tests (if used) are specified with assumptions and multiple-comparison handling
- [ ] Effect sizes are emphasized over p-values alone (see `references/statistical-reporting.md`)

**Threats to Validity:**
- [ ] Threats are enumerated (internal/construct/statistical/external) with concrete mitigations (see `references/threats-to-validity.md`)

---

## Citation Formats

Prefer managing references via `references.bib` (BibTeX/BibLaTeX) and generating the reference list automatically; see `references/bibliography-workflows.md`. The examples below are reference list patterns for manual verification.

### IEEE Format

**Journal Article:**
```latex
[1] A. Author, B. Author, and C. Author, "Title of article," Journal Name, vol. X, no. Y, pp. ZZ-ZZ, Month Year.
```

**Conference Paper:**
```latex
[2] A. Author and B. Author, "Title of paper," in Proc. Conference Name, City, Country, Year, pp. ZZ-ZZ.
```

**Book:**
```latex
[3] A. Author, Title of Book, Edition. City, State: Publisher, Year.
```

See `references/ieee-citation-guide.md` for complete reference.

### APA Format (7th Edition)

**Journal Article:**
```latex
Author, A. A., & Author, B. B. (Year). Title of article. Journal Name, Volume(Issue), pages. https://doi.org/xxxxx
```

**Conference Paper:**
```latex
Author, A. A., & Author, B. B. (Year, Month). Title of paper. In Conference Name (pp. pages). Publisher.
```

See `references/apa-citation-guide.md` for complete reference.

---

## Output

### Primary Output: LaTeX Source

I generate `.tex` files that you can compile with:
- **Overleaf** (online, recommended)
- **Local LaTeX**: TinyTeX, MacTeX, TeX Live
- **VS Code**: LaTeX Workshop extension

### Compilation Commands

```bash
# IEEE-style (BibTeX)
pdflatex paper.tex
bibtex paper
pdflatex paper.tex
pdflatex paper.tex

# APA-style (BibLaTeX + biber)
pdflatex paper.tex
biber paper
pdflatex paper.tex
pdflatex paper.tex

# Or use latexmk (recommended if available)
latexmk -pdf -bibtex paper.tex
latexmk -pdf -usebiber paper.tex
```

### Alternative Outputs

If LaTeX is not suitable, I can also generate:
- **Markdown** with MathJax support
- **DOCX** via Pandoc conversion

---

## Important Notes

- **Quality over quantity** - Fewer well-chosen sources are better than many weak ones
- **Recent sources preferred** - Last 5-7 years unless historical context needed
- **Research integrity** - Always cite properly, never plagiarize
- **Be honest about limitations** - Acknowledge gaps in your research
- **User provides content** - I structure and write; you provide the research contributions

---

## References

- `references/ieee-citation-guide.md` - Complete IEEE reference examples
- `references/apa-citation-guide.md` - Complete APA reference examples
- `references/latex-math-guide.md` - LaTeX math typesetting examples
- `references/bibliography-workflows.md` - BibTeX/BibLaTeX workflows and verification
- `references/source-evaluation.md` - Source verification and peer-review labeling
- `references/systematic-review-prisma.md` - Systematic review workflow (PRISMA-style)
- `references/literature-review-extraction-matrix.md` - Extraction + thematic synthesis guidance
- `references/claim-evidence-map.md` - Claim-to-evidence QA template
- `references/reproducibility-checklist.md` - Reproducibility QA checklist
- `references/statistical-reporting.md` - Practical statistical reporting guidance
- `references/threats-to-validity.md` - Threats-to-validity prompts
- `references/acm-citation-guide.md` - ACM citation format reference
- `references/revision-response-guide.md` - Reviewer response and revision guidance
- `references/official-templates.md` - Links to official publisher LaTeX templates
- `references/templates/` - LaTeX templates (IEEE, APA, thesis, reviews, proposals)
- `examples/` - Protocols and working templates (vocabulary, extraction matrix, claim-evidence map)
- `scripts/resolve-papers.js` - Paper discovery and open-access resolution via Semantic Scholar, Unpaywall, CrossRef
- `scripts/validate-bib.js` - BibTeX entry validation against CrossRef
- `scripts/check-citations.js` - Citation key consistency checker
