---
name: paper-rebuttal-helper
description: Use this skill when the user has received peer review comments and needs to write a rebuttal or author response. Triggers include "write my rebuttal", "respond to reviewers", "how do I address this comment", "reviewer says X, how do I respond", "help me triage these reviews", or pasting review text into the conversation. Handles triage of major vs. minor concerns, response strategy, draft writing, and prioritisation of additional experiments. Do not use for writing the original paper — use research-paper-writing instead; do not use for writing a new paper from scratch after rejection.
license: MIT
metadata:
  category: "Writing"
  version: "0.1.0"
  author: "VIOS Lab, University of Edinburgh"
---

# Paper Rebuttal Helper

A skill for writing effective author responses and rebuttals. The goal is not to win an argument — it is to help reviewers understand what you actually did and to resolve their legitimate concerns.

## When to invoke this skill

- You received reviews and have a rebuttal period (NeurIPS, ICLR, ICML, CVPR, MICCAI all have one)
- You are submitting a revision to a journal and need to write a response letter
- You are not sure which comments require new experiments vs. clarifications vs. pushback
- You need to coordinate responses across co-authors

## Workflow

### 1. Triage all comments

For each reviewer, categorise every concern into:

| Type | Description | Response strategy |
|------|-------------|------------------|
| **Misunderstanding** | Reviewer misread or missed something already in the paper | Clarify with page/line reference; offer to add a clearer sentence |
| **Legitimate gap** | Something is genuinely missing that you can address | Provide the result / experiment / reference |
| **Out of scope** | Request for work beyond the paper's stated contribution | Acknowledge and explain the scope decision |
| **Matters of taste** | Style, phrasing, or framing preference | Politely accommodate where possible |
| **Wrong** | Factual error by the reviewer | Correct with evidence; be respectful |

Never dismiss a comment as "wrong" without evidence. Reviewers who feel dismissed become hostile meta-reviewers.

### 2. Identify must-do experiments

List any concern that, if unaddressed, would justify rejection. For each:
- Can it be run in the rebuttal window? (Usually 72 hours for conference, 2–8 weeks for journal)
- What is the minimal experiment that addresses it?
- What is the expected result, and what if it goes the other way?

If a must-do experiment cannot be run in time, you must address it conceptually and promise it in the camera-ready — but be honest about the limitation.

### 3. Draft the response

**Format:**
```
We thank all reviewers for their careful reading and constructive feedback.

--- Reviewer 1 ---

**R1.1** [Quote or paraphrase the concern]

[Your response — 2–5 sentences. If you have new results, state them clearly with numbers.]

**R1.2** ...

--- Reviewer 2 ---
...
```

**Tone principles:**
- Open by thanking reviewers genuinely.
- Never be defensive or dismissive.
- Quote the exact concern before responding — this prevents misalignment.
- When you agree with a concern, say "The reviewer is correct that..." before explaining the fix.
- When you disagree, explain why with evidence, not opinion.
- Use bold headings for each comment so reviewers can find their points easily.
- Keep responses concise — reviewers re-read rebuttals quickly.

### 4. Handling common difficult situations

**"The method is not novel enough."**
State the specific technical contribution in one sentence, then compare it to the closest prior work with a concrete difference. If the novelty is primarily empirical (new application, new scale), say so explicitly and argue why that is a valid contribution for the venue.

**"The baselines are not fair / missing X."**
If you can run X in the rebuttal window, do it. If not, explain the computational or data-access constraint and offer a proxy experiment. Cite any prior work that also omitted X under the same constraint.

**"The results are only on one dataset."**
If you have a second dataset available, run it. If not, explain what the first dataset covers and why generalisation is likely (or honestly state it as a limitation).

**"The ablation is incomplete."**
Run the missing ablation. If it cannot be done in time, explain why the omitted component is unlikely to be the driver using theoretical or intuitive argument, and promise a full ablation in camera-ready.

**"I do not understand [key concept]."**
This is a writing problem, not a reviewer problem. Rewrite the relevant paragraph and include it verbatim in the response: "We propose the following revised text for Section 3.2: ..."

**Conflicting reviewer comments:**
State the conflict explicitly: "Reviewer 1 suggests adding X while Reviewer 3 suggests removing it. We [chose X / chose against X] because [reason], and we are happy to discuss this with the Area Chair."

### 5. Rebuttal checklist

Before submitting:
- [ ] Every numbered comment from every reviewer has a numbered response.
- [ ] New experimental results are clearly labelled (e.g., "NEW RESULT").
- [ ] You have not introduced new claims not in the original paper.
- [ ] Promises for camera-ready are realistic and stated clearly ("we will add...").
- [ ] The response fits within the word/character limit.
- [ ] At least one co-author has read the rebuttal cold (without looking at the reviews first) to check it makes sense.

## Anti-patterns

- **Do not** write a rebuttal that is longer than the paper — brevity signals confidence.
- **Do not** promise experiments you cannot deliver in the camera-ready.
- **Do not** address comments in a different order than the reviewer listed them — it looks evasive.
- **Do not** copy-paste the same generic response to multiple reviewers who raised the same concern — personalise each.
- **Do not** use the rebuttal to attack the reviewer's expertise or competence.
- **Do not** ignore a comment because you think it is wrong — address it and show why it is wrong.

## See also

- `pre-submission-review` for catching these issues before reviewers do.
- `venue-reviewer` for understanding what reviewers at a specific venue typically care about.
- `research-paper-writing` for improving sections that reviewers flagged as unclear.
