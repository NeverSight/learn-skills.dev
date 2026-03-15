---
name: reading-cloze-builder
description: "Build Chinese-English reading cloze worksheets from an article markdown template. Use when a user provides a reading passage or a Day_test-style markdown file and wants: (1) 20 core B1-or-below vocabulary items, (2) full-text masking with ==word== markup, (3) a second-pass selection of 10 assessment words with balanced distribution, (4) numbered cloze blanks like `1________`, and (5) a final completed markdown output ready for teaching, homework, or exams."
---

# Reading Cloze Builder

Create a completed Day_test-style worksheet from an article and keep the five tasks internally consistent.

## Workflow

1. Read the source markdown and identify the article body plus the five task slots.
2. Read `assets/group_format_template.md` before generating Task 1.
3. Extract 20 core words that most affect comprehension.
4. Mark all 20 words in the full article with `==word==`.
5. Select 10 words from the 20-word group for testing.
6. Replace those 10 words once each with numbered blanks in reading order.
7. Produce Task 5 by marking those same 10 words with `==word==` in the original article.
8. Save the completed markdown as a new file instead of overwriting the original unless the user explicitly asks.

## Selection Rules

### Task 1: 20 core words

Follow these rules:
- Exclude proper nouns such as people, countries, dates, and publication names.
- Keep difficulty at B1 or below when possible.
- Prefer words that affect comprehension of policy, action, cause/effect, attitude, and evidence.
- Keep inflected forms if the article uses them and that form matters for downstream masking.
- Strictly follow `assets/group_format_template.md` for the Group block layout.
- Keep the same visual style as the template, including the heading pattern, frequency tag, Chinese gloss line, example sentence line, optional collocation/translation/derived-word lines, and separator line.
- If some fields are unavailable, preserve the template structure as closely as possible and omit only the missing content itself.

### Task 2: full-group masking

- Mask every Task 1 word in the article with `==word==`.
- Preserve the original paragraphing and punctuation.
- Keep the article readable; do not restructure sentences.

### Task 3: 10 assessment words

Select 10 words from Task 1 using these constraints:
- Do not select more than one word from the same sentence.
- Spread selections across the article as evenly as possible.
- Mix parts of speech when possible.
- Favor words that test comprehension, spelling, grammar form, or context.
- Keep the exact surface form that will later be blanked or highlighted.

### Task 4: numbered cloze blanks

- Replace each of the 10 Task 3 words exactly once.
- Number blanks in reading order as `` `1________` ``, `` `2________` `` and so on.
- Use one blank per chosen word and do not blank the same word twice.
- Preserve all other wording, punctuation, and paragraph breaks.

### Task 5: final 10-word highlighting

- Return to the original article.
- Mark only the 10 Task 3 words with `==word==`.
- Do not carry over Task 1-only masking.

## Consistency Checks

Before delivering:
- Verify Task 3 words are a subset of Task 1.
- Verify Task 4 contains exactly 10 numbered blanks.
- Verify each Task 4 blank corresponds to one Task 3 word in order.
- Verify Task 5 highlights the same 10 words selected in Task 3.
- Verify no sentence contributes more than one Task 3 word.
- Verify Task 1 visually matches the Group template style.

## Output Pattern

Unless the user gives a stricter format, use this structure:
- A Group block that matches `assets/group_format_template.md` for Task 1.
- A fully rendered article block for Tasks 2, 4, and 5.
- A numbered list for Task 3.

## Resources

### assets/

- `assets/day_test_template_v2.md`: blank worksheet template mirroring the provided Day_test layout.
- `assets/group_format_template.md`: required formatting reference for the Task 1 Group block.

### scripts/

- `scripts/build_output.py`: assemble a final markdown file from prepared Task 1-5 outputs. Use this when you already completed the reasoning steps and want a clean deterministic export.

Run example:

```bash
python3 scripts/build_output.py \
  --template assets/day_test_template_v2.md \
  --article article.md \
  --group task1.txt \
  --task2 task2.txt \
  --task3 task3.txt \
  --task4 task4.txt \
  --task5 task5.txt \
  --output completed.md
```