---
name: critique-manuscript
user_invocable: true
description: Critique an academic manuscript for novelty, methodological rigor, causal claims, data quality, generalizability, mechanism, and presentation. Use for pre-submission review or anticipating reviewer concerns.
---

# Critique an academic manuscript

Review only manuscripts the user is authorized to share. If authorization is unclear, ask before reading. Do not run an external literature search unless the user requests it.

## Scope

Use a user-provided manuscript path when available. Otherwise, identify the entrypoint from the project configuration and document structure, then follow included files. Read the complete argument, including figures and tables needed to evaluate its claims.

Before evaluating, establish the research question, approach, key findings, and claimed contribution. Use that understanding to test whether the manuscript's framing and evidence agree.

## Review criteria

### Literature and novelty

Check whether the paper engages the relevant prior work, distinguishes its contribution, and supports claims of novelty. Ask whether a reviewer could consider the result incremental or already known and whether recent or foundational references are missing.

Do not infer a confirmed literature gap from the manuscript alone. Without a search, describe the suspected gap and give concrete topics, authors, or query terms that could test it. If the user requests a search, use targeted OpenAlex queries based on the title, key claims, suspected gaps, and relevant authors or groups. Present results as papers to review, not proof that a citation is missing.

### Methodological rigor

Check whether measurements and proxies capture their stated constructs; methods fit the question; baselines and null models are appropriate and up-to-date; robustness and sensitivity checks cover consequential assumptions; uncertainty is quantified; and sample size supports the analysis.

### Causal claims and confounders

Identify causal language that outruns correlational evidence. Check plausible confounders, selection effects, alternative explanations, and whether hedging accurately distinguishes association from causation.

### Data quality and limitations

Check representativeness, selection bias, measurement error, systematic data or method biases, temporal artifacts, reproducibility, and availability. Assess whether the limitations are discussed honestly and prominently and whether any limitation could explain the reported result.

### Generalizability

Identify the populations, datasets, periods, and contexts to which the evidence applies. Check boundary conditions and whether a narrow result should be framed as a case study rather than a general claim.

### Mechanism

Ask whether the paper explains how and why the result arises, not only what happened. Check whether theory or additional analysis supports the proposed mechanism and whether a simpler mechanism fits the evidence.

### Clarity and presentation

Check whether the paper is clear and self-contained, the title and abstract match the actual contribution, notation is consistent, and figures and tables are informative, well-labeled, and referenced in the text. Check that the narrative has a clear question. Compare introduction claims with the results, assess whether the discussion adds interpretation rather than repetition, and judge whether length matches content.

## Evidence and calibration

Anchor every finding to a section, paragraph, figure, table, or short quoted claim. Distinguish demonstrated problems from plausible alternative explanations and questions a reviewer may raise. Do not fabricate references or present suspected literature gaps as established facts.

Keep the critique proportional to the manuscript and venue. Be candid about weaknesses, preserve strengths that should survive revision, and give a concrete next step for each material issue.

## Report

Return the critique in the conversation unless the user asks for a file. Organize it around:

- A neutral 1–3 sentence summary.
- The three most important risks.
- Strengths to preserve.
- Anticipated reviewer questions.
- Detailed findings under only the criteria that produced useful observations.
