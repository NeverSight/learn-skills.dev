---
name: qa-thinking
description: Analyze a feature a developer is building from a QA perspective — edge cases, negative flows, abuses, unobvious scenarios. Use when asked "what could go wrong?", "what am I missing?", or "review this as QA".
---

# QA Thinking

Think about a feature like a senior QA engineer and surface risk scenarios.
Explain these risks to a developer who implements this feature
You are provided either with a feature specification or implementation
You must provide a critical review of it from QA perspective and ask clarifying questions
The user can explain the idea, or take it from the current branch or PR.
For a PR, gather intent with the `qa-pr-requirements-analyzer` skill first.
When the feature's current behavior is unclear, establish it with the `qa-explain-behavior` skill first.

## Think as QA

- What is this feature is about
- How does it align with exiting features, common project patterns, business intends
- Is there already implemented a similar pattern in codebase (aren't we duplicating existing behavior)
- Negative scenarios: possible misuse and failures.
- Unobvious usage: edge cases, boundary values, cancellations during executions.
- Combinations: how this feature interacts with other features.
- Security vulnerabilities.

## Output

Only requested section named exactly the way we provide
Information in section written as numbered lists

Requested sections:


- Section `👷 Must be aknowledged`: brief summary in bullet points. Potential correlation with other areas. Potential risks
- Section `👓 Must be clarified`: up to 5 questions to resolve important ambiguities. Start each with "What if".
- Section `🔬 Must be verified`: up to 5 most important risk scenarios, no more.
- Prefer simple wording and short sentences.

## Next actions

Offer after the analysis:

- Draft missing or unclear user stories → `write-user-story` skill.
- Split the scenarios across testing levels → `qa-split-testing-levels-pyramid` skill.
- Turn scenarios into test cases or a checklist → `qa-write-test-cases` skill.
- Ambiguities point to requirement defects → `qa-requirement-reviewer` skill.
