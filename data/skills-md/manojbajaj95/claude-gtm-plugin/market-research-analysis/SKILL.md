---
name: market-research-analysis
description: |
  Comprehensive market research and analysis skill. Use when sizing markets, conducting competitive analysis, generating professional market research reports, analyzing consumer behavior, or identifying market opportunities. Activates for: market research, market analysis, market report, TAM SAM SOM, market sizing, industry analysis, market landscape, competitive landscape, market trends, consumer research, Porter's Five Forces, PESTLE, SWOT, BCG Matrix, McKinsey-style report, consulting report, market opportunity, industry report, due diligence, M&A analysis, GTM market analysis, product-market fit validation.
---

# Market Research & Analysis

Expert market research skill — from market sizing and competitive analysis through consumer research and professional consulting-grade reports with LaTeX formatting and visual generation.

---

## Quick Start

**Choose your workflow:**
1. **Market Sizing** — TAM/SAM/SOM calculations
2. **Competitive Analysis** — Landscape mapping and positioning
3. **Consumer Research** — Surveys, interviews, behavior analysis
4. **Professional Report** — 50+ page consulting-style report with LaTeX + visuals

---

## Market Sizing (TAM → SAM → SOM)

### Step 1: Define Scope
- Product/service being analyzed
- Geography (target regions)
- Customer segment (who specifically)
- Time frame (current year or 5-year projection)

### Step 2: Calculate TAM (Top-Down)
```
TAM = Total market demand at 100% market share
= (Total potential customer base) × (avg contract value)

Data sources: Gartner, Forrester, IBISWorld, government statistics, trade associations
```

### Step 3: Calculate SAM
```
SAM = Portion of TAM you can realistically serve
Apply filters: geographic constraints, product limitations, customer size constraints
Typically 5-20% of TAM
```

### Step 4: Calculate SOM
```
SOM = Realistic near-term market share (1-3 years)
Conservative benchmarks:
  Year 1: 0.1-0.5% of SAM
  Year 2: 0.5-2% of SAM
  Year 3: 1-5% of SAM
```

### Step 5: Bottom-Up Validation
```
Bottom-up = (realistic target customers) × (conversion rate) × (ACV)
If top-down SOM / bottom-up > 3x → revisit top-down assumptions
```

---

## Competitive Landscape Analysis

### Competitor Categories

| Type | Definition | Example |
|------|------------|---------|
| **Direct** | Same product, same customer | Asana vs Monday.com |
| **Indirect** | Different product, same problem | Asana vs Excel |
| **Substitute** | Alternative way to address need | Asana vs consultants |
| **Potential** | Could enter market easily | Microsoft, Google |

### Competitive Intelligence Sources

- Company websites (pricing, features, positioning)
- App store reviews (G2, Capterra — look for "appears X times" keywords)
- Crunchbase (funding, valuation, growth trajectory)
- Job postings (what they're investing in)
- LinkedIn (employee count trends, key hires)
- Gartner Magic Quadrant (market positioning)

### Positioning Map Template

Create a 2D matrix:
- **X-axis:** Price (Low → High)
- **Y-axis:** Feature complexity / target segment (Simple → Advanced)

Plot all competitors. **Look for gaps** — unserved or underserved quadrants = market opportunity.

---

## Core Analysis Frameworks

### Porter's Five Forces (rate each High / Medium / Low)

1. **Threat of New Entrants** — Barriers to entry, capital requirements, brand loyalty
2. **Supplier Power** — Concentration, switching costs, substitute inputs
3. **Buyer Power** — Concentration, price sensitivity, switching costs
4. **Threat of Substitutes** — Alternatives, switching costs, price/performance tradeoff
5. **Competitive Rivalry** — Number of competitors, industry growth, differentiation

### PESTLE Analysis

| Dimension | Key Questions |
|-----------|---------------|
| **Political** | Regulatory environment, trade policies |
| **Economic** | Growth rates, inflation, currency risks |
| **Social** | Demographics, consumer behavior shifts |
| **Technological** | Disruptive technologies, R&D activity |
| **Legal** | Compliance requirements, IP landscape |
| **Environmental** | Sustainability trends, regulations |

### SWOT + BCG Matrix

For competitive landscape: map competitors on BCG Matrix (market growth vs market share) to identify Stars, Cash Cows, Question Marks, Dogs.

---

## Consumer Research

### Survey Design

**Van Westendorp Pricing:**
Ask customers 4 questions to find optimal price point:
1. At what price is this too expensive to consider?
2. At what price is this so cheap you doubt the quality?
3. At what price does this start to feel expensive (but not off the table)?
4. At what price is this a great value/bargain?

Plot cumulative % — OPP (Optimal Price Point) = intersection of "too expensive" and "too cheap."

**Anti-pattern:** Never use leading questions ("Don't you think our innovative product..."). Always include negative response options.

### Interview Framework

For qualitative research:
- Define clear research objectives first
- Minimum 5-10 interviews for directional insight, 15-20 for patterns
- Focus on jobs to be done and pain points, not feature preferences
- Capture verbatim language — exact phrases are more valuable than summaries

### Quality Checklist

- [ ] Research objectives clearly defined and measurable
- [ ] Sample is representative of target market
- [ ] Mix of qualitative (why) and quantitative (how many) methods
- [ ] No leading or biased questions
- [ ] Insights are actionable, not just "interesting facts"
- [ ] Limitations acknowledged

---

## Professional Market Research Reports

Generates consulting-grade reports (50+ pages) modeled on McKinsey, BCG, Gartner deliverables.

### Report Structure (~66 pages target)

**Front Matter (~5 pages):** Cover page · Table of Contents · Executive Summary (investment thesis, key findings, top 5 recommendations)

**Core Analysis (~35 pages):**

| Chapter | Pages | Key Frameworks |
|---------|-------|----------------|
| Market Overview & Definition | 4-5 | Industry structure |
| Market Size & Growth | 6-8 | TAM/SAM/SOM, regional breakdown |
| Industry Drivers & Trends | 5-6 | PESTLE, driver impact matrix |
| Competitive Landscape | 6-8 | Porter's Five Forces, positioning matrix |
| Customer Analysis | 4-5 | Segmentation, customer journey |
| Technology & Innovation | 4-5 | Technology roadmap, adoption curve |
| Regulatory & Policy | 3-4 | Regulatory timeline |
| Risk Analysis | 3-4 | Risk heatmap, mitigation matrix |

**Strategic Recommendations (~10 pages):** Opportunity matrix · Implementation roadmap · Investment thesis

**Back Matter (~5 pages):** Methodology · Data tables · Company profiles · Bibliography

### Visual Generation (generate 6 priority visuals first)

```bash
# Batch generate all core visuals
python scripts/generate_market_visuals.py \
  --topic "[MARKET NAME]" --output-dir figures/
```

| Priority | Visual | Tool |
|----------|--------|------|
| 1 | Market growth trajectory | scientific-schematics |
| 2 | TAM/SAM/SOM concentric circles | scientific-schematics |
| 3 | Porter's Five Forces | scientific-schematics |
| 4 | Competitive positioning matrix (2×2) | scientific-schematics |
| 5 | Risk heatmap | scientific-schematics |
| 6 | Executive summary infographic | generate-image |

### LaTeX Compilation

```bash
# Initialize project structure
writing_outputs/YYYYMMDD_HHMMSS_market_report_[topic]/
├── drafts/v1_market_report.tex  ← use assets/market_report_template.tex as base
├── figures/
├── references/references.bib
└── final/

# Compile
cd drafts/
xelatex v1_market_report.tex && bibtex v1_market_report
xelatex v1_market_report.tex && xelatex v1_market_report.tex
```

Use `\usepackage{market_research}` (from `assets/market_research.sty`).

**Colored box environments:**
```latex
\begin{keyinsightbox}[Key Finding]...\end{keyinsightbox}       % blue
\begin{marketdatabox}[Market Snapshot]...\end{marketdatabox}   % green
\begin{riskbox}[Critical Risk]...\end{riskbox}                 % orange
\begin{recommendationbox}[Recommendation]...\end{recommendationbox} % purple
```

See `assets/FORMATTING_GUIDE.md` for complete LaTeX reference.
See `assets/market_report_template.tex` for the full report template.

### Report Quality Standards

- **Data:** No older than 2 years; all statistics attributed; projections state assumptions
- **Writing:** Specific numbers over vague qualifiers; insights first, then data; active voice
- **Visuals:** 300 DPI minimum; colorblind-friendly palette; all axes/legends labeled; sources in captions
- **Length:** 50+ pages — if under, expand appendix data tables and add regional breakdowns

### Pre-Submission Checklist

- [ ] Cover page, ToC, List of Figures, Executive Summary
- [ ] All 11 chapters present (no placeholder sections)
- [ ] 6 core visuals generated and rendering
- [ ] All statistics sourced; projections include assumptions
- [ ] PDF compiles without errors; cross-references work
- [ ] Page count >50

---

## References & Assets

- `scripts/generate_market_visuals.py` — Batch visual generation for reports
- `assets/market_research.sty` — LaTeX style package
- `assets/market_report_template.tex` — Full report template
- `assets/FORMATTING_GUIDE.md` — Complete LaTeX formatting reference
- `references/report_structure_guide.md` — Detailed chapter-by-chapter guidance
- `references/data_analysis_patterns.md` — Analysis patterns and common calculations
- `references/visual_generation_guide.md` — Visual creation workflows

---

## Related Skills

- `product-strategy-and-marketing` — Market opportunity within product strategy
- `go-to-market-strategy` — Applying market research to launch planning
- `pricing-strategy` — Using market research for pricing decisions
