---
name: plotly-dashboard-skill
description: Build production-ready Plotly Dash dashboards with consistent theming, clear layouts, and performant callbacks.
---

# Plotly Dashboard Skill

Create interactive dashboards with a single source of truth for UI and figure styling.

## Instructions

1. Capture audience, questions, and data constraints.
2. Pick a layout pattern and component library.
3. Define a theme and Plotly figure template.
4. Build the layout skeleton before callbacks.
5. Implement callbacks with clear inputs/outputs.
6. Optimize slow callbacks with caching or pre-aggregation.

## Quick Reference

| Task | Action |
|------|--------|
| UI style guide | See `STYLE_GUIDE.md` |
| Figure template | See `FIGURE_STYLE.md` |
| Palettes | See `PALETTES.md` |
| App architecture | See `DASH_ARCHITECTURE.md` |
| Performance | See `PERFORMANCE.md` |

## Input Requirements

- Audience and key decisions
- Data sources and update cadence
- Required filters and views
- Deployment constraints

## Output

- Dash app scaffold (layout + callbacks)
- Consistent theming and figure templates
- README with usage notes

## Quality Gates

- [ ] Layout communicates hierarchy and intent
- [ ] Callbacks are small and focused
- [ ] p95 interaction latency acceptable
- [ ] Styling is consistent across charts

## Examples

### Example 1: Layout-first workflow

```text
Header + filters + KPI row + primary trends + breakdown table
```

## Troubleshooting

**Issue**: Slow callbacks
**Solution**: Cache expensive steps or pre-aggregate data.
