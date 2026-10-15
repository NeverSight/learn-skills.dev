---
name: qa-review-pr
description: Review a pull request as a QA engineer — check whether the change actually solves the stated issue, flag backwards-compatibility breaks and risks, and list the scenarios that must be verified before merge. Use when asked to "review this PR as QA", "what should we test in this PR?", or "is this PR safe to merge?".
---

# QA Review of a Pull Request

Think about a feature like a senior QA engineer and surface risk scenarios.
Gather intent with the `qa-pr-requirements-analyzer` skill first.

## Think

- Does the provided implementation represent the original task or requirement.
- Possible ambiguities in implementation.
- Possible contradictions with existing practices, features.
- Possible duplication of existing features or patterns.
- Unobvious usage: edge cases, repeated actions, boundary values, cancellations.
- Combinations: how this feature interacts with other features.
- Security vulnerabilities.

## Prioritize facts

- Every finding appears in exactly one section. Never restate a finding in another section.
- A defect proven by the code goes to `Is it done` or `Merge Risks`, not both.
- Anything not proven by the code goes to `What must be verified` as a scenario, or is dropped.
- Order every list by impact on end-users, most severe first.
- Limits are maximums, not targets. Fewer points are better than padded ones.
- Whole review: at most 180 words. If over, drop the lowest-severity item.

## Output

- Your output should be readable by a person who doesn't understand or doesn't look into code.
- Use QA language, avoid coding jargon.
- Avoid mentioning internal variable names, syntax, queries, not relevant for QAs.
- Never mention HTTP status codes, test coverage, or unit tests.
- Use high-level business domain specific terms and not low level coding details.
- If needed mention class names, file names, but never get into deeper internal details.
- Explain risks and ambiguities in terms of the persona using the software.
- Try to resolve ambiguities based on your code and requirements understanding.
- State facts directly. No hedging words: "may", "might", "possibly", "should be sanity-checked", "unverified".
- Use bold only for the key point of each item.
- Reply with **only the requested sections, named exactly as provided**. No preface, no conclusions.
- Prefer simple wording and short sentences.

## Requested sections

- Section `Is it done`: does the code meet the original request (PR title, issue description, etc).
  - Verdict is `Yes`, `No`, or `Partially`.
  - If the reported problem still reproduces on any path, verdict is `Partially` — never "Yes, with a caveat".
  - If any `Merge Risks` point says the original problem still happens somewhere, verdict is `Partially`.
  - Issue summary: at most 15 words. Reasoning: at most 30 words.
- Section `Backwards Compatibility`: does the change alter behavior of existing features for existing users.
  - If not, write one sentence and stop.
  - New optional inputs and their new errors are not compatibility issues.
- Section `Merge Risks`: problems merging this PR introduces, proven by the code.
  - At most 3 points. Empty section is allowed: write `No risks found`.
  - Each point: **impact on user, at most 8 words** — who hits it and when, at most 15 words.
- Section `What must be verified`: at most 4 riskiest usage scenarios for end-users.
  - Each scenario: **What if {persona} {action}** — expected result, at most 10 words.
  - Avoid scenarios that are technical and can be unit tested.

## Output Format

```
### 👷‍♀️ Is it done

**<Yes | No | Partially>.** <original issue summary, ≤ 15 words>

<reasoning, ≤ 30 words>

### 🦕 Backwards Compatibility

<'No breaking changes.' + why, ≤ 15 words — OR one line per changed existing behavior>

### 🌋 Merge Risks

1. **<impact on user, ≤ 8 words>** — <who hits it and when, ≤ 15 words>

<0 to 3 points, most severe first>

### 🔬 What must be verified

- **What if <persona> <action>** — <expected result, ≤ 10 words>

<up to 4 scenarios, most risky first>
```
