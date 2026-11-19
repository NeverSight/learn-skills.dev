---
name: plagiarism-checker
description: Detect text originality and AI-generated content.
---

# Plagiarism Checker

Detect whether text is plagiarized or AI-generated. Provides content originality analysis to help identify copied content and machine-generated text.

## Use Cases

Use this skill when users mention "plagiarism check," "detect plagiarism," "check AI rate," "article originality," "text originality detection," "content originality degree," or request similarity/AI rate analysis for a piece of text.

## Core Script

Use `scripts/check_plagiarism.py` to perform detection:

```bash
python scripts/check_plagiarism.py --text "Text content to detect"
```

Optional parameters:
- `--text`: Text to detect (required, or use `--file`)
- `--file`: Read text from file (.txt, .md, .docx)
- `--output`: Output report path (prints to terminal by default)

**Windows Example:**
```powershell
python scripts/check_plagiarism.py --text "Your text here..."
```

## Output Format

The script returns a structured report:
```
=== Originality Detection Report ===
Originality Score: 92%
AI Generation Probability: 12%

[Paragraph Analysis]
  ✓ Paragraph 1: Original content, no match
  ⚠ Paragraph 2: 47% similarity, rewriting recommended
  ⚠ Paragraph 3: 31% AI generation probability
```

## References

- `references/detection-guide.md` — Detection methods, threshold standards, and best practices
- `references/report-template.md` — Report template and examples

## Workflow

1. **Collect Text**: User pastes text or uploads a file
2. **Execute Detection**: Run `check_plagiarism.py`
3. **Interpret Report**: Provide recommendations based on originality score and AI probability
4. **Provide Rewriting Suggestions**: Offer optimization advice for low-scoring paragraphs