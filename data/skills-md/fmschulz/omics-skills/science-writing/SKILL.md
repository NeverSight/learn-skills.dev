---
name: science-writing
description: Write publication-quality scientific manuscripts with DOI validation and structured reference management.
allowed-tools: [Read, Write, Edit, Bash, WebFetch]
---

# Science Writing

Create clear, evidence-based scientific prose with validated citations and reproducible methods.

## Instructions

1. Clarify target venue and manuscript scope.
2. Outline the section before writing prose.
3. Write in full paragraphs with precise, evidence-backed claims.
4. Validate DOIs and citation metadata.
5. Check structure against IMRAD or venue requirements.

## Quick Reference

| Task | Action |
|------|--------|
| DOI validation | `python scripts/crossref_validator.py --doi <doi>` |
| Writing guidance | See `references/` |
| Examples | See `examples/` |

## Input Requirements

- Manuscript section(s) or outline
- Target journal or venue (if known)
- Citation list or DOI inputs

## Output

- Publication-quality prose
- Validated references (DOI-checked)
- Consistent citation formatting

## Quality Gates

- [ ] Claims are supported by citations
- [ ] Paragraph structure and flow are clear
- [ ] DOIs validated where available

## Examples

### Example 1: Validate a DOI

```bash
python scripts/crossref_validator.py --doi "10.1038/d41586-018-02404-4"
```

## Troubleshooting

**Issue**: Missing DOI metadata
**Solution**: Search by title and verify the source before citing.
