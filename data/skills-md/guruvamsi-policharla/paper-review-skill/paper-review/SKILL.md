---
name: paper-review
description: Systematic LaTeX paper review for correctness, clarity, and consistency. Builds overview from intro sections, then reviews each section in parallel.
license: MIT
---

# Paper Review Skill

You are a meticulous academic paper reviewer specializing in computer science research papers. Your task is to systematically review a LaTeX paper for correctness, clarity, and consistency.

## Overview

This skill orchestrates a comprehensive paper review through:
1. **Discovery**: Parse LaTeX structure to identify all sections
2. **Overview Building**: Extract high-level understanding from introduction/overview sections
3. **Parallel Review**: Dispatch sub-agents to review individual sections with shared context
4. **Report Generation**: Aggregate findings into a structured `report.md`

---

## Phase 1: LaTeX Discovery

### Step 1.1: Find the Main Document

Locate the main LaTeX file by searching for files containing `\documentclass`:

```
Search for: \documentclass
In files: *.tex
```

If multiple matches exist, prefer:
1. `main.tex`
2. `paper.tex`
3. File with the shortest path
4. Ask user if ambiguous

### Step 1.2: Resolve All Includes

Parse the main document and recursively resolve all `\input{}` and `\include{}` commands:

**Pattern matching:**
```
\input{filename}      → filename.tex (if no extension)
\input{filename.tex}  → filename.tex
\include{filename}    → filename.tex (if no extension)
```

**Important considerations:**
- Paths may be relative to the main file's directory
- Some projects use `\input{sections/intro}` style paths
- Handle both with and without `.tex` extension
- Skip commented-out includes (lines starting with `%`)

Build a complete file manifest:
```
main.tex
├── abstract.tex (if included)
├── sections/introduction.tex
├── sections/related.tex
├── sections/methods.tex
├── sections/results.tex
├── sections/conclusion.tex
└── appendix.tex (if included)
```

### Step 1.3: Extract Section Structure

Parse all resolved files to build the section hierarchy:

**Section commands to detect:**
```latex
\section{Title}
\section*{Title}
\subsection{Title}
\subsection*{Title}
\subsubsection{Title}
\paragraph{Title}
```

For each section, record:
- **Name**: The section title
- **Level**: section (1), subsection (2), subsubsection (3), paragraph (4)
- **File**: Source file containing this section
- **Line**: Starting line number
- **Content**: All text until the next section of equal or higher level

**Output format:**
```
SECTION STRUCTURE:
1. Introduction [sections/intro.tex:1-89]
2. Related Work [sections/related.tex:1-156]
   2.1 Formal Methods [sections/related.tex:45-89]
   2.2 Machine Learning Approaches [sections/related.tex:90-156]
3. Technical Overview [sections/overview.tex:1-203]
...
```

### Step 1.4: Identify Overview Sections

For building the paper overview, identify sections matching these patterns (case-insensitive):

**Primary (must include at least one):**
- `Introduction`
- `Intro`

**Secondary (include if present):**
- `Technical Overview`
- `Overview`
- `Our Approach`
- `Approach`
- `Our Method`
- `Problem Statement`
- `Background` (only first part, for notation)
- `Preliminaries` (only first part, for notation)

**Selection logic:**
1. Always include Introduction
2. Include Technical Overview/Overview/Approach if exists (prefer "Technical Overview")
3. Include first ~500 lines of Background/Preliminaries for notation definitions
4. If user specified sections for overview, use those instead

---

## Phase 2: Build Paper Overview

Using the identified overview sections, construct a comprehensive paper summary that will serve as context for all section reviewers.

### Step 2.1: Read Overview Sections

Read the full content of:
- Introduction section
- Technical Overview section (or equivalent)
- Notation-relevant portions of Background/Preliminaries

### Step 2.2: Extract Structured Overview

Use the prompt template in `prompts/overview-builder.md` to extract:

```markdown
## Paper Overview

### Title and Authors
[Extract from \title{} and \author{} commands]

### Main Goal
[One paragraph describing the paper's primary objective]

### Key Contributions
1. [First contribution]
2. [Second contribution]
3. [Third contribution]
...

### Methodology Summary
[2-3 paragraphs outlining the technical approach]

### Notation Dictionary
| Symbol | Meaning | First Defined |
|--------|---------|---------------|
| $\mathcal{D}$ | Dataset | Section 2.1 |
| $\theta$ | Model parameters | Section 3 |
| ... | ... | ... |

### Key Claims and Theorems
1. **Theorem 1** (Section X): [Brief statement]
2. **Claim** (Section Y): [Brief statement]
...

### Evaluation Metrics
- [Metric 1]: [What it measures]
- [Metric 2]: [What it measures]
```

This overview becomes the **shared context** for all section reviewers.

---

## Phase 3: Section Review Dispatch

### Step 3.1: Determine Sections to Review

**If user specified sections:**
- Review only those sections
- Match by section name (fuzzy matching OK)

**If no sections specified:**
- Review ALL sections except:
  - Abstract (usually just summary)
  - Acknowledgments
  - References/Bibliography

### Step 3.2: Classify Section Types

Classify each section to customize the review focus:

| Section Type | Patterns | Review Focus |
|--------------|----------|--------------|
| `introduction` | Introduction, Intro | Claims clarity, contribution clarity, scope |
| `related_work` | Related Work, Related, Prior Work, Background | Coverage, fair comparison, positioning |
| `methodology` | Methods, Methodology, Approach, Our Approach, Technical, System, Design, Architecture | Technical correctness, completeness, reproducibility |
| `theoretical` | Theory, Analysis, Proofs, Formal | Proof correctness, assumption clarity, theorem statements |
| `experimental` | Experiments, Evaluation, Results, Empirical | Methodology validity, statistical rigor, fair comparison |
| `discussion` | Discussion, Limitations, Future Work | Honesty, scope acknowledgment |
| `conclusion` | Conclusion, Summary, Concluding | Consistency with claims, no new claims |
| `appendix` | Appendix | Completeness, reference clarity |

### Step 3.3: Dispatch Parallel Reviews

For each section to review, spawn a sub-agent with:

**Context provided:**
1. The Paper Overview (from Phase 2)
2. The section content
3. The section type classification
4. The review prompt template (`prompts/section-reviewer.md`)

**Instruction:**
```
Review the following section of an academic paper.

PAPER CONTEXT:
[Insert Paper Overview from Phase 2]

SECTION TO REVIEW:
Name: [Section Name]
Type: [Section Type]
File: [filename.tex]
Lines: [start-end]

CONTENT:
[Full section content]

Follow the review guidelines in the section reviewer prompt.
Return your findings in the specified format.
```

**Parallelization:**
- Launch all section reviews simultaneously if possible
- Each review is independent given the shared overview context
- Collect all results before proceeding to Phase 4

---

## Phase 4: Report Generation

### Step 4.1: Collect All Reviews

Gather the structured output from each section reviewer:
```
Section: [Name]
- Critical Issues: [list]
- Major Issues: [list]
- Minor Issues: [list]
- Suggestions: [list]
```

### Step 4.2: Generate report.md

Create `report.md` in the paper's root directory with the following structure:

```markdown
# Paper Review Report

**Generated:** [YYYY-MM-DD HH:MM]
**Paper:** [Paper title from \title{}]
**Main File:** [main.tex path]
**Sections Reviewed:** [count] of [total]

---

## Executive Summary

[2-3 paragraph high-level assessment including:]
- Overall paper quality assessment
- Most critical issues requiring immediate attention
- Key strengths of the paper
- Recommendation summary

---

## Paper Overview

[Insert the Paper Overview from Phase 2]

---

## Detailed Section Reviews

### 1. [Section Name]

**File:** `[filename.tex]` | **Lines:** [start]-[end] | **Type:** [section_type]

#### Critical Issues
> Issues that indicate potential incorrectness or fundamental problems

- **[C1]** [Issue description]
  - *Location:* Line [X] or "[quoted text]"
  - *Problem:* [Detailed explanation]
  - *Suggestion:* [How to fix]

- **[C2]** ...

#### Major Issues
> Significant problems affecting clarity, completeness, or validity

- **[M1]** [Issue description]
  - *Location:* ...
  - *Problem:* ...
  - *Suggestion:* ...

#### Minor Issues
> Small improvements that would enhance quality

- **[m1]** [Brief description] — [location]
- **[m2]** ...

#### Suggestions
> Optional enhancements and style improvements

- [Suggestion 1]
- [Suggestion 2]

---

### 2. [Next Section Name]
...

---

## Summary Statistics

| Severity | Count | Sections Affected |
|----------|-------|-------------------|
| Critical | [X]   | [list]            |
| Major    | [Y]   | [list]            |
| Minor    | [Z]   | [list]            |
| Suggestions | [W] | [list]           |

**Total Issues:** [X + Y + Z + W]

---

## Cross-Cutting Concerns

[Issues that span multiple sections:]

### Notation Consistency
- [Any notation used inconsistently across sections]

### Terminology Consistency  
- [Any terms used with different meanings]

### Flow and Coherence
- [Any logical gaps between sections]

### Missing References
- [Any forward/backward references that don't resolve]

---

## Prioritized Action Items

Based on severity and impact, here are the recommended actions in priority order:

### Must Fix (Critical)
1. [Most important critical issue]
2. [Second most important]
...

### Should Fix (Major)
1. [Most important major issue]
2. ...

### Consider Fixing (Minor + Suggestions)
1. [Highest impact minor issues]
2. ...

---

## Review Methodology

This review was conducted using automated analysis with the following checks:
- Technical correctness and logical consistency
- Notation consistency with definitions in [overview sections]
- Writing clarity and precision
- Structural flow and completeness

**Sections used for context:** [list overview sections]
**Sections reviewed:** [list all reviewed sections]

---

*Report generated by Paper Review Skill*
```

---

## Handling Edge Cases

### Missing Introduction
If no clear Introduction section exists:
1. Look for "Overview" or first numbered section
2. Use abstract + first section as overview context
3. Note this limitation in the report

### Very Long Sections
If a section exceeds reasonable length (>1000 lines):
1. Split at subsection boundaries
2. Review subsections as separate units
3. Add cross-subsection consistency check

### Heavy Use of Macros
If the paper uses many custom LaTeX macros:
1. Locate macro definitions in preamble or `.sty` files
2. Build a macro dictionary
3. Expand macros mentally when reviewing (or note undefined macros)

### Math-Heavy Content
For sections with heavy mathematical notation:
1. Pay special attention to notation dictionary
2. Flag any symbol used before definition
3. Check theorem/lemma numbering consistency
4. Verify proof structure (assumptions → steps → conclusion)

### Code Listings
If the paper includes code:
1. Check code-text consistency
2. Verify algorithm descriptions match pseudocode
3. Flag any undefined functions/variables in code

---

## User Interaction Points

### Before Starting
Ask user (if not specified):
- "Should I review all sections or specific ones?"
- "Are there any sections I should prioritize?"

### During Review
Report progress:
- "Found [N] sections across [M] files"
- "Building paper overview from Introduction and [X]..."
- "Reviewing section [N] of [Total]: [Name]"

### After Completion
- Notify: "Review complete! Report saved to report.md"
- Offer: "Would you like me to elaborate on any specific issue?"

---

## Quick Start Checklist

When invoked, execute these steps in order:

- [ ] Find main .tex file
- [ ] Resolve all \input{} and \include{} 
- [ ] Build section structure map
- [ ] Identify overview sections (intro + technical overview)
- [ ] Read and parse overview sections
- [ ] Generate Paper Overview using `prompts/overview-builder.md`
- [ ] Determine which sections to review
- [ ] Classify each section by type
- [ ] For each section: dispatch review with Paper Overview as context
- [ ] Collect all section reviews
- [ ] Identify cross-cutting concerns
- [ ] Generate final report.md
- [ ] Report completion to user
