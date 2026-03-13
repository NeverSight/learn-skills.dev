---
name: ascii-boxes
description: Generate and validate ASCII box diagrams with Unicode box-drawing characters. Use when creating architecture diagrams, system overviews, or any box-drawing art in markdown, READMEs, or code comments. Includes a generator (from simple text format) and a validator (checks alignment). Use for any task involving ┌─┐│└─┘ characters.
---

# ASCII Boxes

Two tools: generate perfect boxes, validate existing ones.

## Generate a diagram

Write a simple text file describing the box:

```
Docker Container
[lead] agent-lead | UID 1001 | nono Landlock
[coder] agent-coder | UID 1002 | nono Landlock

supervisor (PID 1)
- Creates users
- Drops privileges
```

Format rules:
- First line = outer box title
- `[tag] col1 | col2 | col3` = inner box (each tag is a separate box, columns are rows)
- `- text` = bullet item (rendered as `· text`)
- Blank line = spacing row

Run:

```bash
python3 SKILL_DIR/scripts/draw-box.py input.txt
```

Pipe output into your file or copy-paste into markdown.

## Validate an existing diagram

```bash
python3 SKILL_DIR/scripts/check-box-align.py <file>
```

Finds blocks with box-drawing corners (`┌`/`╔`), checks all lines have the same display width. Reports mismatches with line numbers.

## Why this exists

LLMs cannot count display columns reliably. Box-drawing characters are 3 bytes UTF-8 but 1 display column. Always validate after writing or editing box art.

## Workflow

1. Generate with `draw-box.py` OR hand-write the diagram
2. Validate with `check-box-align.py`
3. If misaligned, pad short lines with spaces before closing `│`
4. Re-validate until clean
