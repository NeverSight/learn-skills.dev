---
name: awesome-phd-cv
description: LaTeX CV/resume templates for PhD students and researchers, covering ATS-optimized industry resumes and full academic CVs.
triggers:
  - help me make a PhD CV in LaTeX
  - create an academic CV template
  - convert my academic CV to industry resume
  - ATS-safe LaTeX resume for big tech
  - latex resume template for PhD student
  - faculty job application CV LaTeX
  - deedy or jakes resume template
  - academic to industry resume conversion
---

# Awesome PhD CV

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

A curated collection of LaTeX CV/resume templates for PhD students, postdocs, and researchers. Covers three distinct use cases: ATS-safe industry resumes (Jake's format), high-density two-column resumes (Deedy format), and full multi-page academic CVs (Awesome-CV format).

---

## What This Project Provides

| Template | Use Case | Engine | Columns | Pages |
|----------|----------|--------|---------|-------|
| `research-cv/` (Awesome-CV) | Faculty, postdoc, academic CV | XeLaTeX | 1 | Multi |
| `jakes-format/` | Industry SWE, big tech, ATS-critical | pdfLaTeX | 1 | 1 |
| `deedy-format/` | Experienced tech professionals | XeLaTeX | 2 | 1 |

---

## Installation & Setup

### Prerequisites

Install a full TeX distribution:

```bash
# macOS
brew install --cask mactex

# Ubuntu/Debian
sudo apt-get install texlive-full

# Windows — download MiKTeX from https://miktex.org/
```

For XeLaTeX templates (Awesome-CV, Deedy), ensure font packages are available:

```bash
# Ubuntu
sudo apt-get install fonts-font-awesome texlive-xetex
```

### Clone the Repo

```bash
git clone https://github.com/LimHyungTae/Awesome-PhD-CV.git
cd Awesome-PhD-CV
```

---

## Template 1: Jake's Format (Industry / ATS-Safe)

**File:** `jakes-format/resume.tex`  
**Engine:** pdfLaTeX — no custom fonts, no multi-column, passes ATS parsers at Google, Meta, Amazon, Apple, Microsoft.

### Compile

```bash
cd jakes-format
pdflatex resume.tex
```

### Key Commands in Jake's Format

```latex
% Section header
\section{Experience}

% Job/project entry
\resumeSubheading
  {Company or Institution Name}{City, Country}
  {Your Title}{Start Date -- End Date}
  \resumeItemListStart
    \resumeItem{Built X system achieving Y metric on Z dataset/platform.}
    \resumeItem{Deployed model to production serving N requests/day.}
  \resumeItemListEnd

% Education entry (same command)
\resumeSubheading
  {Massachusetts Institute of Technology}{Cambridge, MA}
  {Postdoctoral Associate, CSAIL}{Jan 2025 -- Present}

% Skills section
\resumeSubHeadingListStart
  \resumeSubItem{Languages}{Python, C++, CUDA, Bash}
  \resumeSubItem{Frameworks}{PyTorch, ROS2, Open3D, PCL}
\resumeSubHeadingListEnd
```

### Full Minimal Example: Jake's Format

```latex
\documentclass[letterpaper,11pt]{article}
\usepackage{latexsym}
\usepackage[empty]{fullpage}
\usepackage{titlesec}
\usepackage{marvosym}
\usepackage[usenames,dvipsnames]{color}
\usepackage{verbatim}
\usepackage{enumitem}
\usepackage[hidelinks]{hyperref}
\usepackage{fancyhdr}
\usepackage[english]{babel}
\usepackage{tabularx}

\pagestyle{fancy}
\fancyhf{}
\fancyfoot{}
\renewcommand{\headrulewidth}{0pt}
\renewcommand{\footrulewidth}{0pt}

\addtolength{\oddsidemargin}{-0.5in}
\addtolength{\evensidemargin}{-0.5in}
\addtolength{\textwidth}{1in}
\addtolength{\topmargin}{-.5in}
\addtolength{\textheight}{1.0in}

\urlstyle{same}
\raggedbottom
\raggedright
\setlength{\tabcolsep}{0in}

% Section formatting
\titleformat{\section}{
  \vspace{-4pt}\scshape\raggedright\large
}{}{0em}{}[\color{black}\titlerule \vspace{-5pt}]

% Custom commands
\newcommand{\resumeItem}[1]{\item\small{#1 \vspace{-2pt}}}
\newcommand{\resumeSubheading}[4]{
  \vspace{-2pt}\item
    \begin{tabular*}{0.97\textwidth}[t]{l@{\extracolsep{\fill}}r}
      \textbf{#1} & #2 \\
      \textit{\small#3} & \textit{\small #4} \\
    \end{tabular*}\vspace{-7pt}
}
\newcommand{\resumeItemListStart}{\begin{itemize}}
\newcommand{\resumeItemListEnd}{\end{itemize}\vspace{-5pt}}
\newcommand{\resumeSubHeadingListStart}{\begin{itemize}[leftmargin=0.15in, label={}]}
\newcommand{\resumeSubHeadingListEnd}{\end{itemize}}

\begin{document}

%-----------HEADER-----------
\begin{center}
    \textbf{\Huge \scshape Hyungtae Lim} \\ \vspace{1pt}
    \small +1-617-000-0000 $|$
    \href{mailto:htlim@mit.edu}{htlim@mit.edu} $|$
    \href{https://linkedin.com/in/yourprofile}{linkedin.com/in/yourprofile} $|$
    \href{https://github.com/LimHyungTae}{github.com/LimHyungTae}
\end{center}

%-----------EDUCATION-----------
\section{Education}
\resumeSubHeadingListStart
  \resumeSubheading
    {Korea Advanced Institute of Science and Technology (KAIST)}{Daejeon, South Korea}
    {Ph.D., Electrical Engineering (Robotics)}{Mar. 2019 -- Feb. 2024}
  \resumeSubheading
    {Massachusetts Institute of Technology (MIT)}{Cambridge, MA}
    {Postdoctoral Associate, CSAIL}{Jan. 2024 -- Dec. 2024}
\resumeSubHeadingListEnd

%-----------SELECTED PROJECTS-----------
\section{Selected Projects}
\resumeSubHeadingListStart
  \resumeSubheading
    {KISS-ICP — LiDAR Odometry System}
      {\href{https://github.com/PRBonn/KISS-ICP}{\underline{GitHub ★3.1k}}}
    {Core Contributor}{2022 -- 2023}
    \resumeItemListStart
      \resumeItem{Designed adaptive threshold module reducing localization drift by 30\% on KITTI benchmark.}
      \resumeItem{Maintained C++/Python codebase used in production AV pipelines at 3 companies.}
    \resumeItemListEnd
\resumeSubHeadingListEnd

%-----------SKILLS-----------
\section{Technical Skills}
\resumeSubHeadingListStart
  \item{
    \textbf{Languages}{: C++17, Python, CUDA, CMake} \\
    \textbf{Frameworks}{: PyTorch, ROS2, Open3D, PCL, Eigen} \\
    \textbf{Tools}{: Docker, Git, AWS, GCP}
  }
\resumeSubHeadingListEnd

\end{document}
```

---

## Template 2: Awesome-CV Format (Academic / Faculty Applications)

**Directory:** `research-cv/`  
**Engine:** XeLaTeX  
**Structure:** Modular — each section lives in `cv/` subdirectory.

### Compile

```bash
cd awesome-cv-format
xelatex cv.tex
```

### Directory Layout

```
awesome-cv-format/
├── cv.tex                  # Main file — includes section files
├── awesome-cv.cls          # Class file (do not edit unless customizing)
└── cv/
    ├── education.tex
    ├── experience.tex
    ├── publications.tex
    ├── honors.tex
    ├── projects.tex
    └── skills.tex
```

### Main File Structure (`cv.tex`)

```latex
\documentclass[11pt, a4paper]{awesome-cv}

% Personal info
\name{Hyungtae}{Lim}
\position{Ph.D. Candidate{\enskip\cdotp\enskip}Robotics Researcher}
\address{Daejeon, South Korea}
\email{shapelim@kaist.ac.kr}
\homepage{limhyungtae.github.io}
\github{LimHyungTae}
\googlescholar{your-scholar-id}{Google Scholar}

% Optional: accent color
\colorlet{awesome}{awesome-skyblue}

\begin{document}

\makecvheader

\cvsection{Education}
\input{cv/education.tex}

\cvsection{Research Experience}
\input{cv/experience.tex}

\cvsection{Publications}
\input{cv/publications.tex}

\cvsection{Honors \& Awards}
\input{cv/honors.tex}

\end{document}
```

### Section File Examples

**`cv/education.tex`**

```latex
\begin{cventries}
  \cventry
    {Ph.D. in Electrical Engineering}
    {Korea Advanced Institute of Science and Technology}
    {Daejeon, South Korea}
    {Mar. 2019 -- Feb. 2024}
    {
      \begin{cvitems}
        \item {Dissertation: \textit{Robust LiDAR Odometry and Mapping for Outdoor Environments}}
        \item {Advisor: Prof. Hyun Myung, Urban Robotics Laboratory}
        \item {GPA: 4.1/4.3}
      \end{cvitems}
    }
\end{cventries}
```

**`cv/publications.tex`**

```latex
\begin{cvpubs}
  \cvpub
    {\textbf{H. Lim}, S. Jung, H. Myung}
    {ERASOR: Egocentric Ratio of Pseudo Occupancy-based Dynamic Object Removal for Static 3D Point Cloud Map Building}
    {IEEE Robotics and Automation Letters (RA-L) + ICRA 2021}
    {2021}
    {Citations: 280+, \href{https://github.com/LimHyungTae/ERASOR}{GitHub ★500+}}
\end{cvpubs}
```

**`cv/honors.tex`**

```latex
\begin{cvhonors}
  \cvhonor
    {Best Paper Award}
    {IEEE International Conference on Robotics and Automation (ICRA)}
    {Philadelphia, PA}
    {2022}
  \cvhonor
    {Korea Presidential Science Scholarship}
    {Korea Student Aid Foundation}
    {South Korea}
    {2019 -- 2024}
\end{cvhonors}
```

---

## Template 3: Deedy Format (Two-Column, High Density)

**File:** `deedy-format/resume.tex`  
**Engine:** XeLaTeX  
**Note:** Requires `deedy-resume.cls` from [deedy/Deedy-Resume](https://github.com/deedy/Deedy-Resume).

### Compile

```bash
cd deedy-format
xelatex resume.tex
```

### Key Commands

```latex
% Left column (narrow — education, skills, links)
\begin{minipage}[t]{0.33\textwidth}

\section{Education}
\subsection{MIT}
\descript{Postdoc | CSAIL}
\location{Jan 2024 – Dec 2024 | Cambridge, MA}
\sectionsep

\subsection{KAIST}
\descript{PhD | Electrical Eng.}
\location{Mar 2019 – Feb 2024 | Daejeon, KR}
\sectionsep

\section{Skills}
\subsection{Programming}
C++ \textbullet{} Python \textbullet{} CUDA \\
ROS2 \textbullet{} PyTorch \textbullet{} Open3D
\sectionsep

\end{minipage}
\hfill
% Right column (wide — experience, projects)
\begin{minipage}[t]{0.66\textwidth}

\section{Experience}
\runsubsection{Google DeepMind}
\descript{| Senior Research Engineer}
\location{Jan 2025 – Present | Mountain View, CA}
\begin{tightemize}
  \item Built real-time 3D scene understanding pipeline for robotics team.
  \item Reduced inference latency by 40\% via CUDA kernel optimization.
\end{tightemize}
\sectionsep

\section{Selected Projects}
\runsubsection{ERASOR}
\descript{| Dynamic Object Removal for LiDAR Maps}
\location{GitHub ★500+ | RA-L 2021 | 280+ citations}
\begin{tightemize}
  \item Designed ego-ratio occupancy method; first open-source tool for this task.
  \item Adopted by 3 autonomous driving companies in production mapping pipelines.
\end{tightemize}
\sectionsep

\end{minipage}
```

---

## Core Insight: Academic CV → Industry Resume Conversion

### The Mindset Shift

| Academic CV | Industry Resume |
|-------------|----------------|
| Publication-driven | Project-driven |
| Venue and novelty | Impact, scale, deployment |
| Full paper titles + co-authors | One-line signal: venue + citations |
| Long, multi-page | One page, ATS-parseable |
| Human reviewer (domain expert) | ATS first → recruiter → engineer |

### What to Keep, Cut, and Reframe

```
KEEP (reframed as impact):
  ✓ Open-source projects with GitHub stars → proves production-quality code
  ✓ Deployed systems / real-world validation
  ✓ Quantified results: "30% reduction in drift on KITTI"
  ✓ Scale: "serves N users / processes N points/sec"

CUT or COMPRESS:
  ✗ Full publication list → keep top 2-3 most relevant
  ✗ Teaching history → omit unless applying to EdTech
  ✗ Conference reviewer service
  ✗ Verbose paper abstracts as bullet points

REFRAME:
  Before: "Published paper on real-time LiDAR odometry at IROS 2023"
  After:  "Built real-time LiDAR odometry system (30ms/frame on embedded GPU);
           open-sourced with 800+ GitHub stars; adopted by 2 AV startups"
```

### Tailoring Projects Per Application

```latex
% For an AV Perception team — lead with detection/segmentation work
\resumeSubheading{3D Object Detection System}{GitHub ★420}
  {Lead Developer}{2022 -- 2023}
  \resumeItemListStart
    \resumeItem{Implemented PointPillars variant achieving 72.1 mAP on nuScenes val set.}
  \resumeItemListEnd

% For a Mapping/Localization team — lead with SLAM work
\resumeSubheading{KISS-ICP Contribution}{GitHub ★3.1k}
  {Core Contributor}{2022 -- 2023}
  \resumeItemListStart
    \resumeItem{Designed adaptive threshold reducing drift 30\% on KITTI; merged upstream.}
  \resumeItemListEnd
```

---

## Common Patterns

### Adding GitHub Stars to Entries (Any Template)

```latex
% Jake's format — in the right-hand date position
\resumeSubheading
  {ERASOR — Dynamic Object Removal}{\href{https://github.com/LimHyungTae/ERASOR}{\underline{★ 500+ stars}}}
  {Lead Developer, Open Source}{2020 -- 2021}
```

```latex
% Awesome-CV format — in the description items
\begin{cvitems}
  \item {Open-sourced at \href{https://github.com/LimHyungTae/ERASOR}{GitHub ★500+};
         adopted in 3 production AV pipelines.}
\end{cvitems}
```

### Hyperlinks in PDFs

```latex
% Jake's / pdfLaTeX — use \href with \underline for visibility
\href{https://github.com/LimHyungTae}{\underline{github.com/LimHyungTae}}

% Awesome-CV / XeLaTeX — \href renders colored by default via class
\href{https://limhyungtae.github.io}{limhyungtae.github.io}
```

### Controlling Page Breaks in Awesome-CV

```latex
% Force new page between major sections
\newpage
\cvsection{Publications}
\input{cv/publications.tex}
```

### Custom Accent Color in Awesome-CV

```latex
% In cv.tex preamble — choose a preset
\colorlet{awesome}{awesome-red}       % red
\colorlet{awesome}{awesome-skyblue}   % sky blue (default)
\colorlet{awesome}{awesome-emerald}   % emerald
\colorlet{awesome}{awesome-concrete}  % gray

% Or define your own
\definecolor{awesome}{HTML}{0E76A8}   % LinkedIn blue
```

---

## Troubleshooting

### XeLaTeX: Font Not Found

```
! fontspec error: "font-not-found"
```

**Fix:**

```bash
# Install FontAwesome system-wide
sudo apt-get install fonts-font-awesome   # Ubuntu
fc-cache -fv                              # Rebuild font cache
```

Or inside the `.cls` file, comment out `\newfontfamily` lines for missing fonts and substitute system fonts.

---

### pdfLaTeX: Undefined Control Sequence `\resumeSubheading`

```
! Undefined control sequence \resumeSubheading
```

**Fix:** Ensure all custom `\newcommand` definitions appear in the preamble before `\begin{document}`. Jake's template is self-contained — do not split across files without copying the command definitions.

---

### ATS Rejects Resume (No Text Extracted)

If an ATS returns your resume blank:

- Switch to `jakes-format/` (pdfLaTeX, no custom fonts).
- Remove `\includegraphics` (profile photos).
- Avoid `tabular`-heavy layouts; use plain `itemize`.
- Test extraction: `pdftotext resume.pdf -` should return readable text.

```bash
# Install poppler-utils then test
pdftotext jakes-format/resume.pdf -
```

---

### Overleaf Compilation

- Jake's format: set compiler to **pdfLaTeX** in Overleaf settings.
- Awesome-CV and Deedy: set compiler to **XeLaTeX**.
- Upload the `.cls` file alongside `.tex` if Overleaf can't find it.

---

## Quick Reference

```bash
# Jake's (pdfLaTeX)
cd jakes-format && pdflatex resume.tex

# Awesome-CV (XeLaTeX)
cd awesome-cv-format && xelatex cv.tex

# Deedy (XeLaTeX)
cd deedy-format && xelatex resume.tex

# Check ATS text extraction
pdftotext <output>.pdf -

# Clean auxiliary files
rm -f *.aux *.log *.out *.toc *.fls *.fdb_latexmk
```
