---
name: latex-formatting
description: Handle LaTeX formatting, templates, and styling for academic papers. Set up conference templates (ICML, ICLR, NeurIPS, AAAI, ACL), fix formatting issues, manage packages, and ensure venue-specific compliance. Use when the user needs to set up a paper template, fix LaTeX formatting, or prepare for submission.
argument-hint: [venue-or-file]
---

# LaTeX Formatting

Set up and manage LaTeX formatting for academic papers.

## Input

- `$0` — Action: `setup`, `fix`, `check`
- `$1` — Venue name (for `setup`) or `.tex` file path (for `fix`/`check`)

## Scripts

### Pre-submission format checker
```bash
python ~/.claude/skills/latex-formatting/scripts/latex_checker.py paper/main.tex --venue neurips --check-anon
```

Checks: word count, required sections, TODO markers, anonymization, mismatched environments, content stats.

### Validate citations and references
```bash
python ~/.claude/skills/citation-management/scripts/validate_citations.py \
  --tex paper/main.tex --bib paper/references.bib --check-figures
```

### Clean LaTeX text (fix special characters)
```bash
python ~/.claude/skills/latex-formatting/scripts/clean_latex.py \
  --input paper/main.tex --output paper/main_cleaned.tex
```

Replaces special/non-UTF8 characters with LaTeX equivalents, skips math environments.
Key flags: `--dry-run`, `--tables-only`

### Auto-fix after checking
```bash
python ~/.claude/skills/latex-formatting/scripts/latex_checker.py paper/main.tex --venue neurips --fix
```

Runs checks then applies clean_latex.py fixes, writing to `main_fixed.tex`.

## References

- Venue specs, project structure, packages, commands: `~/.claude/skills/latex-formatting/references/venue-templates.md`

## Action: `setup`
Create the project directory structure and main.tex for the specified venue. Use the template from `references/venue-templates.md`.

## Action: `fix`
Fix common LaTeX issues: unescaped special chars, math mode errors, float placement, overfull/underfull boxes, cross-reference issues.

## Action: `check`
Run `latex_checker.py` for pre-submission validation. Check page count, anonymization, required sections, TODO markers.

## Related Skills
- Upstream: [paper-writing-section](../paper-writing-section/), [table-generation](../table-generation/)
- Downstream: [paper-compilation](../paper-compilation/)
- See also: [citation-management](../citation-management/)
