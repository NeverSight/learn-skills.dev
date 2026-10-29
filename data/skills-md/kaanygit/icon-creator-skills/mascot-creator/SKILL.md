---
name: mascot-creator
description: Generate brand mascots and character packages with type/preset selection, master images, multi-view sheets, pose variants, expression variants, outfit variants, optional pose-expression matrix, and style-guide.md output.
---

# Mascot Creator

Use this skill when the user wants a mascot, character, brand character, mascot pack, pose sheet, expression sheet, outfit variants, or a reusable character style guide.

## Workflow

1. Collect `description` and `--type`.
   - Valid types: `stylized`, `realistic`, `artistic`.
   - If `--preset` is omitted, defaults are `flat-vector`, `photoreal-3d`, and `watercolor`.
2. Run `icon-skills estimate mascot` if variants are requested.
3. Run `icon-skills create-mascot`.
4. Return the output directory and key files: `master.png`, `character-sheet.png` when variants exist, `style-guide.md`, and `metadata.json`.
5. If the user asks to inspect the result, copy the run folder to Desktop.

## CLI

```bash
icon-skills estimate mascot --variants 1 --views front,side,3-quarter,back --poses idle,waving,thinking --expressions happy,surprised --outfits casual,formal --best-of-n 1

icon-skills create-mascot \
  --description "wise old owl, professor, glasses" \
  --type stylized \
  --preset 3d-toon \
  --views front,side,3-quarter,back \
  --poses idle,waving,thinking \
  --expressions happy,surprised \
  --outfits casual,formal
```

Use `--variants 1` for cheap smoke tests. Use `--best-of-n 1` when the user explicitly wants to limit provider calls.
Use `--provider openrouter|openai|google` and `--model <model-id>` to override the configured provider/model for one run.

## Output

The run folder contains:

- `master.png`
- `variants/`
- `views/`, `poses/`, `expressions/`, `outfits/` when requested
- `pose-expression-matrix/` when `--matrix` is set
- `character-sheet.png` when view/pose/expression variants exist
- `style-guide.md`
- `metadata.json`

## Cost Discipline

Mascot variants multiply calls quickly. Before live testing, summarize the call count. If the user asks for one live test, run only a master generation or explicitly set `--variants 1 --best-of-n 1` and avoid requested variant fan-out unless they approve.
