---
name: study-guide
description: Generates study guides from source materials with quiz questions, essay prompts, and glossaries. Produces ten short-answer questions with an answer key, five essay-format questions, and a comprehensive glossary of key terms. Use when creating a study guide, generating quiz questions, reviewing reading material, preparing for an exam, or asking "create a study guide."
---

# Study Guide

Generate study materials for reviewing and testing comprehension of source content.

## Workflow

```text
Study guide progress:
- [ ] Step 1: Gather sources
- [ ] Step 2: Analyze content and identify key concepts
- [ ] Step 3: Generate study guide
- [ ] Step 4: Validate quality
```

### Step 1: Gather sources

Read files, fetch URLs, or accept pasted text. Ask the user for sources if none are provided. Read every source completely before writing anything.

### Step 2: Analyze content and identify key concepts

- Identify core concepts, arguments, and frameworks in the sources.
- Track specialized terminology and definitions used by the sources.
- Note relationships between concepts (causes, comparisons, dependencies).
- Flag areas where sources provide different perspectives on the same topic.

### Step 3: Generate study guide

Follow this structure exactly:

```markdown
# [Topic]: Study Guide

## Overview

[1-2 paragraphs orienting the reader to what the sources cover and the
key areas of focus.]

## Short-Answer Quiz

1. [Question requiring a 2-3 sentence answer]
2. [Question]
...
10. [Question]

## Answer Key

1. [Answer with source attribution]
2. [Answer]
...
10. [Answer]

## Essay Questions

1. [Open-ended question with scope guidance, e.g., "Discuss at least
   two perspectives from the readings..."]
2. [Question]
...
5. [Question]

## Glossary

**[Term A]**: [Definition drawn from sources, 1-2 sentences.]

**[Term B]**: [Definition drawn from sources, 1-2 sentences.]

[Continue alphabetically for every specialized term in the sources.]
```

### Step 4: Validate quality

```text
Before finalizing, verify:
- [ ] All 10 short-answer questions are answerable from the sources
- [ ] Answer key is accurate with source attribution
- [ ] Questions use varied stems (define, explain, compare, evaluate)
- [ ] No yes/no or trivial questions
- [ ] Essay questions require synthesis, not just recall
- [ ] Essay questions include scope guidance
- [ ] Glossary covers every specialized term in the sources
- [ ] Glossary is alphabetical with 1-2 sentence definitions
- [ ] Markdown renders correctly
```

## Question design

**Short-answer questions:**
- Test comprehension of key concepts, not trivia or minor details.
- Vary question stems: "Define...", "Explain how...", "Compare...", "What is the significance of...", "Describe the relationship between..."
- Each answer should require 2-3 sentences — not a single word, not a paragraph.
- Spread questions across all major topics in the sources.

**Essay questions:**
- Require synthesis across sources or critical evaluation of arguments.
- Include scope guidance so the student knows the expected depth: "citing at least three examples", "discuss at least two perspectives", "compare and contrast..."
- Avoid questions answerable in one sentence (too narrow) or requiring a dissertation (too broad).
- At least one question should ask the student to evaluate or take a position.

## Glossary rules

- Include every specialized or technical term used in the sources.
- Prefer the source's own definition where one is provided.
- Definitions are 1-2 sentences. Do not use the term in its own definition.
- Alphabetical order. Bold the term, follow with a colon and definition.

## Anti-patterns

- Questions with obvious answers that do not test understanding.
- Questions requiring knowledge not present in the sources.
- Glossary definitions that are circular ("X is the process of doing X").
- Essay questions so narrow they have one correct answer.
- Skipping the Overview section — students need orientation.
- Answers in the Answer Key that do not cite which source supports them.

## Skill handoffs

| When | Run |
|------|-----|
| After study guide is written, audit prose quality | `docs-writing` |
