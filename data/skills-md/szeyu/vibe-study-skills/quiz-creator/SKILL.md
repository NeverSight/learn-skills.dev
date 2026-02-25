---
name: quiz-creator
description: Generate quizzes from study materials with multiple question types (MCQ, True/False, Fill-in-blank, Short answer, Matching). Supports difficulty levels and answer keys. Use when creating practice quizzes, test prep materials, self-assessment tools, or knowledge checks from notes, textbooks, or any learning content. Triggers - create quiz, generate questions, make practice test, knowledge assessment, quiz from notes.
---

# Quiz Creator

Generate comprehensive quizzes from any study material with varied question types and difficulty levels.

## Workflow

```mermaid
flowchart LR
    A[Source Material] --> B[Extract Key Concepts]
    B --> C[Select Question Types]
    C --> D[Generate Questions]
    D --> E[Create Answer Key]
    E --> F[Format Output]
```

---

## Step 1: Analyze Source Material

1. **Identify key concepts** - Main topics, definitions, processes
2. **Find testable elements** - Facts, relationships, causes, comparisons
3. **Note difficulty progression** - Basic recall → Application → Analysis

---

## Step 2: Question Type Templates

### Multiple Choice (MCQ)

```markdown
**Q1.** [Question stem]

A) [Distractor - common misconception]
B) [Distractor - partially correct]
C) [Correct answer]
D) [Distractor - related but wrong]

<details>
<summary>Answer</summary>
C) [Explanation why correct and why others are wrong]
</details>
```

**Best for:** Definitions, facts, identifying correct procedures

### True/False

```markdown
**Q2.** [Statement to evaluate] _(True/False)_

<details>
<summary>Answer</summary>
**False** - [Explanation of the correct information]
</details>
```

**Best for:** Common misconceptions, verifying understanding

### Fill-in-the-Blank

```markdown
**Q3.** The process of ________ converts glucose into ATP through ________.

<details>
<summary>Answer</summary>
**cellular respiration**, **oxidative phosphorylation**
</details>
```

**Best for:** Terminology, formulas, key vocabulary

### Short Answer

```markdown
**Q4.** Explain the relationship between [concept A] and [concept B].

<details>
<summary>Answer</summary>
[Model answer with key points that should be mentioned]

**Key points to include:**
- Point 1
- Point 2
- Point 3
</details>
```

**Best for:** Conceptual understanding, explanations, analysis

### Matching

```markdown
**Q5.** Match each term with its definition:

| Term | Definition |
|------|------------|
| 1. [Term A] | A. [Definition 3] |
| 2. [Term B] | B. [Definition 1] |
| 3. [Term C] | C. [Definition 2] |

<details>
<summary>Answer</summary>
1-B, 2-C, 3-A
</details>
```

**Best for:** Vocabulary, pairing concepts, classifications

---

## Step 3: Difficulty Levels

| Level | Characteristics | Bloom's Level |
|-------|-----------------|---------------|
| **Easy** | Direct recall, single concept | Remember |
| **Medium** | Application, 2+ concepts combined | Understand/Apply |
| **Hard** | Analysis, synthesis, edge cases | Analyze/Evaluate |

### Difficulty Distribution Recommendation

- **Review quiz:** 60% Easy, 30% Medium, 10% Hard
- **Practice test:** 30% Easy, 50% Medium, 20% Hard
- **Challenge quiz:** 10% Easy, 40% Medium, 50% Hard

---

## Step 4: Quiz Structure Template

```markdown
# [Topic] Quiz

**Subject:** [Subject Name]
**Difficulty:** [Easy/Medium/Hard/Mixed]
**Questions:** [Number]
**Time:** [Suggested minutes]

---

## Section A: Multiple Choice (X points)

[MCQ questions]

## Section B: True/False (X points)

[T/F questions]

## Section C: Short Answer (X points)

[Short answer questions]

---

## Answer Key

[All answers with explanations]

---

*Generated from: [Source material reference]*
```

---

## Step 5: Quality Checklist

- [ ] Questions test understanding, not just memorization
- [ ] MCQ distractors are plausible (not obviously wrong)
- [ ] Difficulty is appropriate for stated level
- [ ] Answer explanations clarify misconceptions
- [ ] Questions cover breadth of source material
- [ ] No ambiguous wording or trick questions
