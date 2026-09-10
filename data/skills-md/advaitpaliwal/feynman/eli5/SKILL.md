---
name: eli5
description: Explain research, papers, or technical ideas in plain English with minimal jargon, concrete analogies, and clear takeaways. Use when the user says "ELI5 this", asks for a simple explanation of a paper or research result, wants jargon removed, or asks what something technically dense actually means.
---

# ELI5

Use Feynman's alpha tools first when the user names a specific paper, arXiv id, DOI, or paper URL. In shell, call `feynman alpha ...`, not a bare global `alpha` binary.

If the user gives only a topic, identify 1-3 representative papers and anchor the explanation around the clearest or most important one.

Structure the answer with:
- `One-Sentence Summary`
- `Big Idea`
- `How It Works`
- `Why It Matters`
- `What To Be Skeptical Of`
- `If You Remember 3 Things`

Guidelines:
- Use short sentences and concrete words.
- Define jargon immediately or remove it.
- Prefer one good analogy over several weak ones.
- Separate what the paper actually shows from speculation or interpretation.
- Keep the explanation inline unless the user explicitly asks to save it as an artifact.
