---
name: typography
description: Improve typography for prose-heavy content in documents and web UIs using Practical Typography principles. Use when asked to review or rewrite text layout, choose or replace fonts, tune body text metrics (size, leading, line length), clean punctuation and symbols, or produce CSS/style-guide changes for readability and professional polish.
---

# Typography

Apply Practical Typography-inspired rules to make text more readable and professional across print docs and web pages.

Read `references/practical-typography-checklist.md` before making recommendations. Use it as the source of truth for numeric targets and audit checks.

## Workflow

### 1. Determine Medium And Constraints
- Identify medium: print, web, or mixed.
- Capture hard constraints: mandated font, page count, brand system, accessibility requirements, language support.
- If constraints conflict with ideal typography, prioritize constraints and document tradeoffs.

### 2. Set Body Text First
- Choose font, point size, line spacing, and line length before tuning headings.
- Start with targets from `references/practical-typography-checklist.md`:
  - Print: 10-12 pt body text.
  - Web: 15-25 px equivalent body text.
  - Line spacing: 120-145% of body size.
  - Line length: 45-90 characters including spaces.
- Adjust by eye for the specific typeface because equal point sizes do not look equally large across fonts.

### 3. Audit Style Mechanics
- Replace straight quotes with curly quotes where appropriate.
- Enforce one space between sentences and avoid repeated whitespace.
- Avoid underline except links.
- Use bold or italic sparingly; avoid combining both unless required.
- Use dashes, ellipses, apostrophes, and inch/foot marks correctly.

### 4. Tune Hierarchy And Paragraph Flow
- Use a restrained heading scale; avoid oversized display jumps.
- Use either first-line indents or paragraph spacing for body flow, not both.
- Use centered text and all-caps only for short, intentional fragments.
- For justified text, require hyphenation.

### 5. Deliver Actionable Output
- Provide one of:
  - Typography audit (issues, severity, and fixes)
  - Direct CSS/style-token rewrite
  - Document-formatting change list (Word/Pages/Docs steps)
- Include before/after values for every numeric change and one sentence of rationale per change.

## Output Format

Return output in this order:
1. Context summary (medium and constraints).
2. Findings table with `Issue`, `Current`, `Target`, `Reason`.
3. Patch plan or direct edits.
4. Residual risks and tradeoffs.

## Guardrails

- Preserve voice and semantics; modify form, not meaning.
- Prefer minimal, high-leverage changes before broad redesign.
- Do not invent font availability; verify installed or licensed fonts before naming specific families.
- If a strict design system exists, adapt these rules to that system instead of overriding it.
- If accessibility conflicts arise, prioritize legibility and stated accessibility requirements.
