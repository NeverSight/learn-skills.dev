---
name: backward-traceability
description: Make every number in the final PDF traceable to the exact code line that produced it. Uses \hypertarget/\hyperlink LaTeX commands and \num{formula} evaluated at compile time. Use for reproducibility and data integrity verification.
argument-hint: [paper-directory]
---

# Backward Traceability

Make every number in the final PDF hyperlink back to the exact code line that produced it.

## Input

- `$0` — Paper project directory containing code and LaTeX files

## References

- Traceability patterns and LaTeX commands: `~/.claude/skills/backward-traceability/references/traceability-patterns.md`

## Scripts

### Scan hypertarget/hyperlink references
```bash
python ~/.claude/skills/backward-traceability/scripts/ref_numeric_values.py \
  --scan paper/main.tex --output report.json
```

Reports: all hypertargets, hyperlinks, orphan references, unreferenced numeric values.

### Verify cross-reference integrity
```bash
python ~/.claude/skills/backward-traceability/scripts/ref_numeric_values.py \
  --verify paper/main.tex --code-output results.txt
```

Cross-checks values between paper text and code output. Reports mismatches.

## Workflow

### Step 1: Tag Code Outputs
For every numeric value produced by experiment code, add hypertarget tags:

```python
# In experiment code output:
print(f"\\hypertarget{{R1a}}{{45.3}}")  # Mean accuracy
print(f"\\hypertarget{{R1b}}{{2.1}}")   # Std deviation
```

Label format: `{prefix}{line_number}{letter}` where letter = a, b, c... for multiple values on same line.

### Step 2: Reference in Paper Text
Use `\hyperlink` to create clickable references in the paper:

```latex
Our method achieves \hyperlink{R1a}{45.3}\% accuracy
($\pm$\hyperlink{R1b}{2.1}).
```

### Step 3: Use \num for Computed Values
For values derived from other values, use `\num{}` for compile-time evaluation:

```latex
% \num{formula, "explanation"} → evaluated at compile time
The improvement is \num{45.3 - 38.7, "accuracy gain"}\%.
```

### Step 4: Generate Appendix Code Listing
Create an appendix with the full code listing, with `\hypertarget` anchors at relevant lines:

```latex
\section*{Appendix: Code Listing}
\begin{lstlisting}[escapechar=@]
@\hypertarget{code1}{}@result = model.evaluate(test_data)
@\hypertarget{code2}{}@accuracy = result['accuracy']
\end{lstlisting}
```

### Step 5: Verify Traceability
- Every number in the paper text must have a corresponding `\hypertarget` in the code
- Every `\num{}` formula must evaluate correctly
- Click-test: every hyperlink in the PDF must jump to the correct code line

## LaTeX Setup

Required packages:
```latex
\usepackage{hyperref}
\usepackage{listings}
```

## Rules

- Every numeric result in the paper MUST trace to code output
- Never manually type numbers — always reference tagged outputs
- Use `\num{}` for any derived/computed values
- Code listing in appendix must match actual executed code
- Verify all hyperlinks resolve correctly after compilation

## Related Skills
- Upstream: [experiment-code](../experiment-code/), [data-analysis](../data-analysis/)
- Downstream: [paper-compilation](../paper-compilation/)
- See also: [paper-assembly](../paper-assembly/)
