---
name: writing-enhancement
description: Improve writing quality, fix errors, and transform style. Use when asked to proofread, edit, improve clarity, fix grammar/typos, enhance academic writing, analyze prose quality, humanize technical content, or write essays. Triggers include "improve this writing", "fix typos", "proofread", "make this clearer", "academic style", "humanize", "write an essay", "analyze my writing".
---

# Writing Enhancement

Transform and improve written content for clarity, style, and correctness.

## Pattern Selection

| Intent | Pattern | When to Use |
|--------|---------|-------------|
| General improvement | `improve_writing` | Enhance clarity, flow, style |
| Academic writing | `improve_academic_writing` | Scholarly tone, citations, structure |
| Fix errors | `fix_typos` | Spelling, grammar, punctuation |
| Clean formatting | `clean_text` | Fix breaks, normalize punctuation |
| Analyze quality | `analyze_prose` | Rate novelty, clarity, style |
| Pinker analysis | `analyze_prose_pinker` | Steven Pinker's clarity principles |
| Make approachable | `humanize` | Technical → conversational |
| Essay (styled) | `write_essay` | Essays in specific author styles |
| Essay (PG style) | `write_essay_pg` | Paul Graham essay style |
| Micro essay | `write_micro_essay` | Concise single-idea essays |
| Academic paper | `create_academic_paper` | Full LaTeX academic papers |
| LaTeX output | `write_latex` | LaTeX document formatting |

## Decision Flow

```
User request
    │
    ├─ "fix/correct/proofread" ──→ fix_typos
    ├─ "improve/enhance/better" ─┬─ academic context? ──→ improve_academic_writing
    │                            └─ general ──→ improve_writing
    ├─ "analyze/rate/evaluate" ──→ analyze_prose (or analyze_prose_pinker)
    ├─ "humanize/simplify" ──→ humanize
    ├─ "write essay" ─┬─ specific author? ──→ write_essay
    │                 ├─ Paul Graham? ──→ write_essay_pg
    │                 └─ short/micro? ──→ write_micro_essay
    └─ "academic paper/LaTeX" ──→ create_academic_paper or write_latex
```

## Pattern References

See `references/` for full patterns:
- [improve_writing.md](references/improve_writing.md)
- [improve_academic_writing.md](references/improve_academic_writing.md)
- [fix_typos.md](references/fix_typos.md)
- [analyze_prose.md](references/analyze_prose.md)
- [humanize.md](references/humanize.md)
- [write_essay.md](references/write_essay.md)

## Output Guidelines

- Preserve the author's voice unless asked to change it
- For corrections: show changes or provide clean version based on preference
- For analysis: provide actionable feedback, not just ratings
- Match formality level to context (academic vs. blog vs. email)

## Chaining Suggestions

- After `analyze_prose` → offer `improve_writing` to address issues
- After `improve_writing` → offer `fix_typos` for final polish
- After `humanize` → offer `analyze_prose` to verify accessibility
