---
name: figures4papers-playbook
description: Locate and adapt real plotting examples from the figures4papers repository. Use when users ask for a figure in the style of specific papers/projects, want the closest existing script template, or need fast script selection by chart type/domain before customization.
---

# Figures4papers Playbook

Use this skill to find the closest figures4papers example and convert it into a user-specific plotting script quickly.

## Workflow

1. Parse user intent into chart type and domain (for example: grouped bar + benchmark comparison).
2. Run `scripts/example_locator.py` to shortlist candidate scripts.
3. Read `references/example_index.md` for folder-level context and naming patterns.
4. Choose one base script and adapt data, labels, and file outputs.
5. If style consistency is required, co-use `scientific-figure-pro` for final polishing.

## Locator Script

Use keyword and chart filters:

```bash
python skills/figures4papers-playbook/scripts/example_locator.py --keyword bar --chart-type grouped_bar
```

Output includes:

- Folder and domain.
- Matching script paths.
- Recommended run commands.
- Notes about the intended figure purpose.

## Selection Rules

- Prefer exact chart-type match first.
- Then prefer domain match (biomed, LLM eval, vision survey, etc.).
- If no exact match exists, choose the simplest script with nearest visual grammar.
- Keep output paths under a dedicated `figures/` directory in the target project.

## References

- `references/example_index.md`: curated index of available figure folders and scripts.

## Handoff Pattern

After locating a base script, provide:

1. Selected template path.
2. What to replace (data arrays, labels, colors, limits).
3. Command to run.
4. Expected output files (`.png` and `.pdf`).
