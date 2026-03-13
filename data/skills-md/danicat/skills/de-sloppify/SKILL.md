---
name: de-sloppify
description: Inspects and refines AI-generated texts (articles, blog posts, codelabs, READMEs) to remove or rewrite typical "AI slop" language, ensuring a human, authentic, and professional tone. Use when asked to review an article, improve wording, or make a text better.
---

# De-sloppify Skill

This skill helps remove "AI slop" from texts—the repetitive, grandiose, and overly verbose language often produced by default LLM outputs. Your goal is to make the text sound like a competent human peer: clear, concise, and grounded in reality.

## Core Mandates

1.  **Authenticity over Polish:** Prefer natural phrasing over corporate or marketing speak. Avoid passive voice when possible.
2.  **Eradicate Grandiosity:** Remove words like "revolutionary", "shines", "unparalleled", "game-changer", "magic", "tapestry", "seamlessly", "supercharge", "unleash", or "delve". Replace them with specific, evidence-based descriptions.
3.  **Kill the Filler:** State facts directly. Remove transitional fluff like "In conclusion", "Furthermore", "Surprisingly", "Interestingly", "It's important to note that", and "Additionally".
4.  **No Minimizing Language:** Remove patronizing words like "simply", "just", "obviously", and "easy". State the action without judging its difficulty.
5.  **Fix Metaphors:** Eliminate clichéd metaphors like "silver bullet", "missing link", or "piece of the puzzle". Describe the actual connection or realization instead.

## Workflow

When asked to review or improve a text:

1.  **Analyze the Tone:** Read the provided text and identify instances of AI slop, grandiosity, filler, and minimizing language.
                *   **Optional but highly recommended:** If the text is in a file, you can calculate the "Slop Score" and extract slop metrics by running the provided script using `uv run`. `uv` will automatically manage the virtual environment and dependencies (NLTK, etc.) for you:
        ```bash
        uv run scripts/slop_score.py <path_to_file>
        ```
    *   Review the JSON output to identify areas (lexical, structural, statistical) that need the most attention.
2.  **Refine & Rewrite:** Apply the core mandates. Simplify complex sentences, ground abstract claims in concrete examples, and adjust the tone to be professional but conversational.
3.  **Explain the Edits (Optional but recommended):** If you make significant structural changes or remove large chunks of hyperbole, briefly explain why the new phrasing is more authentic and readable.

## Execution

Apply these rules directly to the text provided by the user. If the text is contained in a file, read the file, apply the edits, and either propose the changes or use `smart_edit`/`write_file` to save them (depending on user instructions).