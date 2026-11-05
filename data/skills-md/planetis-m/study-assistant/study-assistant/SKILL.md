---
name: study-assistant
description: Study assistant workflow for turning provided study material into exam-focused deliverables such as verbatim transcriptions, study notes, lecture-style explanations, ELI5 explanations, flashcards, Mermaid mind maps, quizzes, and essay questions.
---

# Study Assistant

Follow this workflow exactly when turning provided study material into exam-ready outputs.

## Select Mode

Map the user's request to exactly one mode:

- `transcribe`: Convert provided source text into structured markdown while preserving educational text verbatim.
- `lecture`: Deliver the material as a coherent professor-style lecture.
- `eli5`: Explain the material in plain English without losing technical depth.
- `flashcard`: Generate exam-ready two-column markdown flashcards.
- `mindmap`: Output a Mermaid mindmap.
- `quiz`: Generate a mixed quiz with an answer key.
- `essay`: Generate 3-4 essay prompts with sample answers.
- `study-notes`: Generate exam-focused study notes from the provided content.

## Prepare Source Material

Work only from material already present in the conversation or already extracted into text.

- If the source still needs to be converted into text, use a separate extraction step first.
- Do not prescribe a specific extraction method or file-format tool here.

## Clean Source Text

Before generating, remove only clear metadata:

- Instructor details
- Headers and footers
- Page numbers
- Timestamps
- Course codes

Preserve educational content such as concepts, definitions, and examples. If a fragment is too broken to recover confidently, omit it rather than guess.

## Generate Output

Read and apply the matching mode section in [references/commands.md](references/commands.md).

Across all modes:

- Base all factual content only on user-provided material and prepared source text.
- Do not add outside facts, theories, or claims.
- In `eli5`, short invented examples are allowed only to illustrate an idea already present in the material.
- Do not mention the source material. Present the content directly.
- Output markdown.
- Use LaTeX with `$...$` (inline) and `$$...$$` (display) for math.
- Do not include conversational intros or conclusions.
