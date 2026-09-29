---
name: gaozhong-english-answer-parser
description: Extract answer keys from Chinese Gaozhong-style English exam papers (PDF or image) and format them into a standardized structured output. Trigger when the user sends an English exam paper, answer key, mock test answer sheet, or similar file and asks to extract, organize, or structure the answers. Trigger even for casual requests like "look at the answers", "extract answers", or "organize this".
metadata:
  skill_version: "0.1.0"
---

# Structured Answer Extraction for Gaozhong English Exam Papers

## Execution Rule

Start processing the user's request directly without pre-checking whether the format is supported or asking for confirmation. If the file can't be read or parsed as expected, adapt and fix then — not before.

## Fixed Question Number Distribution

This skill strictly follows the question numbering scheme below. **Do not assume, adjust, or infer question ranges from the source text.**

| Section | Question Range | Grouping |
|---------|---------------|----------|
| Listening | 1-20 | 1-5, 6-10, 11-15, 16-20 |
| Reading A | 21-23 | One per question |
| Reading B | 24-27 | One per question |
| Reading C | 28-31 | One per question |
| Reading D | 32-35 | One per question |
| Seven-of-Five (Gap Fill) | 36-40 | One per question |
| Cloze | 41-55 | 41-45, 46-50, 51-55 |
| Grammar Fill-in | 56-65 | One per question |

## Processing Flow

### Step 1: Read the file content

**PDF files:**
1. First try `pdfplumber` to extract text
2. If the text lacks answer information (scanned document), convert pages with `pdftoppm` and use visual recognition (`view_image`)

**Image files:**
1. Use `view_image` to inspect directly
2. If incomplete, supplement with OCR

### Step 2: Extract raw answers

Locate the answer key area in the text by searching for keywords (参考答案, 答案, Answer Key, etc.). Extract only the answers:
- Multiple choice: letters only (A-G)
- Fill-in-the-blank: the word/phrase to be filled in
- **Completely ignore explanatory text**, regardless of how closely it is mixed with the answers

### Step 3: Output in fixed structure

Output as Markdown — **no code blocks**, no file generation. Reply directly in the chat.

## Output Template

## Answer Key

### Listening
| 1-5 | 6-10 | 11-15 | 16-20 |
|-----|------|-------|-------|
| BCBAC | BCCAA | BACAB | CACBB |

### Reading Comprehension
**Passage A**
**21**.B  **22**.A  **23**.C

**Passage B**
**24**.C  **25**.B  **26**.D  **27**.A

**Passage C**
**28**.C  **29**.B  **30**.A  **31**.C

**Passage D**
**32**.D  **33**.A  **34**.B  **35**.C

**Seven-of-Five (Gap Fill)**
**36**.F  **37**.D  **38**.A  **39**.E  **40**.G

### Language Use

**Cloze**
| 41-45 | 46-50 | 51-55 |
|-------|-------|-------|
| BACDB | AACDC | BCABD |

**Grammar Fill-in**
| No. | Answer |
|-----|--------|
| 56 | to |
| 57 | a |
| 58 | playful |
| 59 | combining |
| 60 | introduction |
| 61 | which |
| 62 | surprisingly |
| 63 | to reflect |
| 64 | has created |
| 65 | hidden |

## Output Rules

1. **Strictly follow the fixed question number distribution.** Do not adjust question ranges or groupings based on the source text. If the source groups 21-35 in continuous blocks of 5 (e.g., `21-25 DDBBB`), remap to the fixed groups: Passage A 21-23, Passage B 24-27, Passage C 28-31, Passage D 32-35.
2. **Listening**: 4 groups of 5 questions each, presented as a table row with 5 consecutive letters per cell.
3. **Reading Comprehension**: Passage A (3 questions), Passage B (4), Passage C (4), Passage D (4) — grouped by passage, each question on its own line.
4. **Seven-of-Five**: 5 questions, one per line.
5. **Cloze**: 3 groups of 5 questions each, presented as a table row.
6. **Grammar Fill-in**: 10 questions in a vertical table — first column question number, second column answer.
7. **Output answers only, no explanations.**
8. **Output as Markdown, no code blocks, no file generation.**
9. **Continuation writing / composition sections are not included in the answer structure.**
10. **Match the user's language.** The output language (section headers, explanatory labels like "Passage A", "Cloze", etc.) MUST match the language of the user's question. If the user asks in Chinese, output headers in Chinese; if in English, output headers in English. The answer content (letters, words) itself remains unchanged.
