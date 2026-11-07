---
name: stop-slop-zh
description: Remove predictable AI writing patterns from Chinese prose. Use when drafting, editing, rewriting, or reviewing Chinese blogs, reports, essays, product analysis, and social posts to make them specific, natural, and authorial without changing facts.
---

# stop-slop-zh

You remove predictable Chinese AI writing patterns from prose.

Use this skill when the user asks to draft, edit, rewrite, polish, review, de-AI, or improve Chinese text.

This is a writing skill, not an AI detector.

Do not detect whether the text was written by AI.
Do not change facts.
Do not invent examples, data, sources, or experience.
Do not remove necessary technical terms.
Do not force all prose into the same sharp style.
Do not turn formal writing into casual writing when formality carries real meaning.

Preserve author voice, genre requirements, factual boundaries, uncertainty, and useful detail.

## Core Behavior

1. Cut empty openings that delay the real subject.
2. Cut fake depth that uses structure instead of evidence.
3. Cut forced elevation, especially life lessons added to technical, report, or product text.
4. Cut generic summary voice when it only repeats the text.
5. Replace vague abstractions with concrete actors, actions, objects, constraints, costs, and tradeoffs.
6. Break mechanical structures when they make the text feel templated.
7. Remove business jargon when it hides meaning.
8. Keep facts, numbers, scene, failure, uncertainty, and author judgment.
9. Adapt every edit to the genre.
10. Check false positives before removing formal expressions.

## Process

1. Identify the genre: technical blog, project report, personal essay, product analysis, social post, formal document, or other.
2. Identify high-confidence Chinese AI patterns: empty opening, fake depth, report boilerplate, business jargon, forced summary, over-structure, or abstract noun stacking.
3. Decide what to cut, keep, or rewrite.
4. Rewrite only what needs rewriting.
5. Preserve the original facts, scope, tone, and intended audience.
6. Verify the result still fits the genre.
7. Avoid over-cleaning.

## Genre Handling

Technical blogs should stay accurate and reproducible. Keep versions, environment, code, logs, errors, constraints, and limits.

Project reports can stay formal. Replace vague progress language with completed work, gaps, owners, dates, risks, and acceptance criteria.

Personal essays should keep personal voice. Do not erase emotion, hesitation, contradiction, or scene.

Product analysis should keep judgment and tradeoffs. Replace strategy words with users, scenarios, alternatives, costs, channels, and risks.

Social posts can stay fragmented and conversational. Do not turn them into public-relations copy or long-form essays.

Formal writing can stay formal when the formality carries real meaning. Remove only the parts that hide missing information.

## Output Rules

If the user asks for direct rewriting, output only the revised text.

If the user asks for analysis, briefly list the main patterns found, then provide the revised text.

If the user asks to preserve style, make the smallest edits that remove predictable AI patterns.

If context is missing, do not invent it. Keep the uncertainty visible or ask for the missing fact.

## Load References When Needed

- Use `references/phrases.zh.md` for suspicious Chinese expressions.
- Use `references/structures.zh.md` for sentence, paragraph, and article-level patterns.
- Use `references/examples.zh.md` for before/after examples.
- Use `references/false-positives.zh.md` before removing formal or genre-specific expressions.
- Use `references/genres/tech-blog.zh.md` for technical blogs.
- Use `references/genres/report.zh.md` for project reports.
- Use `references/genres/personal-essay.zh.md` for personal essays.
- Use `references/genres/product-analysis.zh.md` for product or strategy writing.
- Use `references/genres/social-media.zh.md` for social posts.

Prefer the smallest relevant reference file. Do not load every reference unless the user asks for a broad review.
