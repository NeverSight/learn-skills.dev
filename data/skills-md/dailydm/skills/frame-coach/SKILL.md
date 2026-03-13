---
name: frame-coach
description: "Frame Coach: Evaluate and recommend improvements to framing statements"
disable-model-invocation: true
---

# Frame Coach: Evaluate and recommend improvements to framing statements
When the user types `/frame-coach` and describes a problem, idea, or opportunity, do the following:

## 1) Show the user:
**Model Recommendation**: For best results with this evaluation task, use a flagship thinking/reasoning model like Gemini Pro, GPT 5.2+, Opus 4.5+, etc. if you're using Auto, consider re-running this command.
-------

## 2) Understand the framing statement (required)

- Read the user's input and identify Persona, Pain, Context, and Impact
- Note any company-specific terminology (PSQ, CRO, PREQ, BTS, CS, SquareKit)
- Apply the litmus test: "If we solved this problem perfectly but built a feature completely different from what the user implies, would this statement still hold true?"

## 3) Evaluate using the rubric

Evaluate the input based on three dimensions (scale: 1-3 for each):

### Dimension 1: Structural Integrity
- **Must Haves**: Who (Persona), What (Pain), Where (Context), Why (Impact)
- **Root Cause**: Identifies root friction, not just symptoms
- **Solution Agnostic**: Describes problem space, not a feature request
- **Score 1**: Vague persona, describes symptoms, masquerades solution as problem
- **Score 3**: Specific persona/mindset, identifies root friction, strictly descriptive

### Dimension 2: Persuasiveness
- **Evidence**: Uses data, metrics, or qualitative themes
- **Urgency**: Explains "Why now?" (cost of delay)
- **Empathy**: Makes stakeholder feel user's frustration
- **Score 1**: Relies on intuition, lacks urgency, clinical tone
- **Score 3**: Cites specific metrics, articulates cost of delay, visceral connection

### Dimension 3: Executive Tone
- **Brevity**: Scannable and succinct (BLUF)
- **Alignment**: Ties problem to business goals (OKRs, Revenue, Churn, Efficiency)
- **Language**: Free of jargon, accessible to non-technical leaders
- **Score 1**: Wall of text, rambling, overly technical, focuses only on user annoyance
- **Score 3**: Concise/scannable, explicitly links to strategic pillars, clear plain English

Assign a score (1-3) for each dimension.

## 4) Generate output in required format

Output your response using the following markdown structure:

### Executive Summary
- **Overall Grade**: [Score out of 9]
- **Status**: [Critical / Needs Polish / Ready for Review]
- **Word Count**: [Too short (below 80 words), Good (81-200 words), Too long (over 201 words)]
- **Problem Focus**: [Pass/Fail] - [Briefly explain if describing a problem or asking for a specific feature]

### Detailed Rubric Scoring

| Dimension | Score | Feedback |
| :--- | :--- | :--- |
| **Structure** | [1-3] | [Specific critique on Persona/Root Cause] |
| **Persuasiveness** | [1-3] | [Critique on Data/Urgency/Emotion] |
| **Executive Tone** | [1-3] | [Critique on Brevity/Strategic Alignment] |

### Coaching Tips
- [Bullet point 1: Specific advice on how to fix the biggest weakness]
- [Bullet point 2: Specific advice on alignment or data]

### Proposed Rewrite

*Here is how I would rewrite this to persuade a leader:*

[Your rewritten version]

## 5) Output style guidelines

- Important! add the model recommendation to the top of the output

**Model Recommendation**: For best results with this evaluation task, use a flagship thinking/reasoning model like Gemini Pro, GPT 5.2+, Opus 4.5+, etc. if you're using Auto, consider re-running this command.
-------

- Important! use less than 200 words
- Always describe the user problem/opportunity (ex. increase efficiency) before describing a business problem (ex. reduce CoGS) when re-writing the statement
- Use the advice from the Coaching Tips section
- Keep an even, professional tone - avoid words that sound emotional or overly judging
- Try not to coin new terms unless it adds significant clarity
- Avoid overly finance-bro terms (margin, EBITDA, etc.) - we're an edtech company and bias towards user problems
- Do not use emojis, em dashes, or other common generative AI punctuation
- Do not include a section that offers a proposed solution or opportunity - only describe the problem
