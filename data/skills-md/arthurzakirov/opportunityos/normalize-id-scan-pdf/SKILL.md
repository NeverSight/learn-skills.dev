---
name: normalize-id-scan-pdf
description: "Repair low-quality or awkwardly laid-out ID scan PDFs. Use when a PDF of a personal ID, passport, or driver's license needs page content rotated without changing the page orientation, scaled up to use more of the page without clipping, renamed with stable bronze/silver/gold filenames, self-checked for cut-off content, or opened locally for final review."
---

# Normalize ID Scan PDF

## Overview

Turn a bad ID scan PDF into a readable, portable output PDF. Prefer a deterministic transform plus autonomous validation over ad hoc manual tweaking.

## Workflow

1. Work from the bronze source file. Do not overwrite it.
2. If `pypdf` is unavailable, create a local virtualenv and install `pypdf` there instead of touching the system interpreter.
3. Run `python "${CODEX_HOME:-$HOME/.codex}/skills/normalize-id-scan-pdf/scripts/fix_id_scan_pdf.py" ...` against the source PDF.
4. Review the script output paths and geometry summary.
5. If the output still clips or uses the page poorly, iterate from the bronze file again. Do not keep transforming the silver or gold output.
6. After the PDF passes self-check, open the gold PDF locally for final human review if local browser or desktop open access is available. Prefer Chrome when it is installed and reachable.

## Command Pattern

Use:

```bash
python fix_id_scan_pdf.py "/path/to/source.pdf" --output-dir "/path/to/output"
```

Common options:

- `--page-mode portrait`: keep a portrait page and rotate the content within it. This is the default and the safe choice for ID scans like the one that motivated this skill.
- `--margin-pt 24`: reserve a fixed visual margin so the output does not ride the page edge.
- `--doc-type personal_id`: force the gold filename document type slug.
- `--gold-name arthur_zakirov__personal_id.pdf`: override the inferred gold filename when you already know the canonical delivery name.

## Validation Rules

The script must be treated as a first-pass fixer plus a geometry validator.

- Measure the visible content box from embedded images and text origins.
- Choose the rotation and scale that maximize page usage inside the requested orientation.
- Re-measure the output page after writing the transform.
- If the output crosses the requested margins, reduce the scale and retry automatically until it fits.
- Prefer re-running from bronze with adjusted options over stacking transforms on a previously fixed PDF.

If you need a filename decision, read `references/naming-convention.md`.

## Final Review

After producing the gold file, try to open it for review.

- Prefer Chrome when available. Otherwise use the local browser or desktop open mechanism that matches the machine: `xdg-open`, `open`, `powershell.exe`, or an installed browser automation skill.
- Ask for approval if the environment requires elevated GUI access.
- If local open is unavailable, report the final path clearly instead of pretending the review happened.
