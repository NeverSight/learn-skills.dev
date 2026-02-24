---
name: self-review
description: Automatically review an academic paper using the NeurIPS review form with three reviewer personas, ensemble scoring, and reflection refinement. Extracts text from PDF, runs structured review, and outputs actionable feedback. Use when the user wants to review a paper before submission or get feedback on a draft.
argument-hint: [pdf-or-tex-file]
---

# Self-Review

Review an academic paper using a structured review form with multiple reviewer personas.

## Input

- `$ARGUMENTS` — Path to PDF file or `.tex` file

## Scripts

### Extract text from PDF
```bash
python ~/.claude/skills/self-review/scripts/extract_pdf_text.py paper.pdf --output paper_text.txt
python ~/.claude/skills/self-review/scripts/extract_pdf_text.py paper.pdf --format markdown
```

Tries pymupdf4llm (best) → pymupdf → pypdf. Install: `pip install pymupdf4llm pymupdf pypdf`

### Parse PDF into structured sections
```bash
python ~/.claude/skills/self-review/scripts/parse_pdf_sections.py \
  --pdf paper.pdf --output sections.json
```

Extracts title (via font size), section headings, and section text. Requires: `pip install pymupdf`
Key flags: `--format text`, `--verbose`

## Workflow

### Step 1: Load Paper
- If PDF: use `extract_pdf_text.py` to extract text
- If `.tex`: read the LaTeX source directly

### Step 2: Three-Persona Review
Run three independent reviews using different personas (from `references/review-form.md`):

1. **Harsh but fair reviewer**: Expects good experiments that lead to insights
2. **Harsh and critical reviewer**: Looking for impactful ideas in the field
3. **Open-minded reviewer**: Looking for novel ideas not proposed before

For each persona, generate a review following the NeurIPS review JSON format in `references/review-form.md`.

### Step 3: Reflection Refinement (up to 3 rounds per reviewer)
After each review, apply the reflection prompt: re-evaluate accuracy and soundness, refine if needed. Stop when "I am done".

### Step 4: Aggregate
- Combine all three reviews
- Average numerical scores (round to nearest integer)
- Synthesize a meta-review finding consensus
- Weight scores using AgentLaboratory weights: Overall (1.0), Contribution (0.4), Presentation (0.2), others (0.1 each)

### Step 5: Actionable Report

Output format:
```
## Review Summary
- **Overall Score**: X/10 (Weighted: Y/10)
- **Decision**: Accept / Reject
- **Confidence**: Z/5

## Strengths (consensus across reviewers)
1. ...
2. ...

## Weaknesses (consensus across reviewers)
1. ...
2. ...

## Questions for Authors
1. ...

## Specific Suggestions for Improvement
1. [Section X, Page Y]: ...
2. [Section Z, Page W]: ...

## Score Breakdown
| Dimension | R1 | R2 | R3 | Avg |
|-----------|----|----|-----|-----|
| Overall | ... | ... | ... | ... |
| Contribution | ... | ... | ... | ... |
| ... | ... | ... | ... | ... |
```

## References

- NeurIPS review form, scoring weights, personas, reflection prompts: `~/.claude/skills/self-review/references/review-form.md`
- PDF text extraction: `~/.claude/skills/self-review/scripts/extract_pdf_text.py`

## Missing Sections Check
You MUST verify that all required sections are present: Abstract, Introduction, Methods/Approach, Experiments/Results, Discussion/Conclusion. Reduce scores if any are missing.

## Related Skills
- Upstream: [paper-compilation](../paper-compilation/)
- Downstream: [paper-revision](../paper-revision/), [rebuttal-writing](../rebuttal-writing/)
- See also: [slide-generation](../slide-generation/)
