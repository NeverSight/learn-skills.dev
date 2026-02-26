---
name: beautiful-data-viz
description: Create publication-quality matplotlib/seaborn charts with readable axes, tight layout, and curated palettes.
argument-hint: "[medium=notebook|paper|slides] [background=light|dark]"
---

# Beautiful Data Viz

Create polished, publication-ready visualizations in Python/Jupyter with strong typography, clean layout, and accessible color choices.

## Instructions

1. Clarify the message, audience, and medium (notebook/paper/slides).
2. Choose the simplest chart type that answers the question.
3. Select an appropriate palette type (categorical/sequential/diverging).
4. Apply the shared style helpers, then build the plot.
5. Validate readability at target size and export with tight bounds.

## Quick Reference

| Task | Action |
|------|--------|
| Apply style | Use `assets/beautiful_style.py` helpers |
| Pick palette | See `references/palettes.md` |
| QA checklist | See `references/checklist.md` |
| Plot recipes | See `examples/recipes.md` |

## Input Requirements

- Data in a tabular form (pandas DataFrame or similar)
- Clear statement of the primary message
- Target medium and background preference

## Output

- Publication-ready figure(s) (PNG/SVG/PDF)
- Consistent styling and labeling

## Quality Gates

- [ ] Message is clear in 3 seconds at target size
- [ ] Labels and units are readable and accurate
- [ ] Color choice is colorblind-safe and grayscale-tolerant
- [ ] Layout is tight with minimal whitespace

## Examples

### Example 1: Apply the shared style helper

```python
from assets.beautiful_style import set_beautiful_style, finalize_axes
set_beautiful_style(medium="notebook", background="light")
# build plot here
finalize_axes(ax, title="Example", subtitle="", tight=True)
```

## Troubleshooting

**Issue**: Labels overlap or are unreadable
**Solution**: Reduce tick count, rotate labels, or increase figure width.

**Issue**: Colors are hard to distinguish
**Solution**: Use a colorblind-safe categorical palette and limit categories.
