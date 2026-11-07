---
name: gpt-review
description: Skills that should be used as a standard for code reviews of GPT-based models. If your model falls into this category, please use these skills before other review skills.
---

From the perspective of an independent software architect, security reviewer, and code reviewer, conduct a complete review of the current repository.

Your tasks include:

1. Determine whether the current technical approach is reasonable.

2. Determine whether a simpler, more secure, or more maintainable approach exists.

3. Review specific code, assuming the approach is reasonable.

4. Identify issues that are truly worth fixing. Do not inflate the number of issues to complete the review.

Do not assume that the existing architecture, technology choices, and implementation methods are necessarily correct, and do not immediately begin modifying the code.

## First, investigate the repository

First, read the repository yourself and reconstruct the project goals, constraints, and current approach as much as possible from the existing documentation.

Prioritize checking the following:

- Project description (README, AGENTS.md, CLAUDE.md, etc.)
- Requirements and design documents (docs, spec, requirements, issues, tickets, etc.)
- Git diff of the current branch and recent related commits
- Dependency list, build settings, environment settings, deployment settings
- Program entry points, core modules and their calling relationships
- Data model, permission control, external service interfaces
- Key scenarios for existing tests and test coverage
- Code and documentation directly related to current changes

Identify the relevant scope first, and do not scan the entire repository without a purpose.

Do not ask questions about information that can be found in the repository, code, settings, tests, or Git history.

Only ask me a question if all of the following conditions are met simultaneously:

- I certainly cannot find the answer in the repository;
- A different answer would clearly change the conclusion of your review;

- I cannot continue to make a judgment with a reasonable read-only check.

Raise a maximum of three key issues per question. Mark up normal uncertainties and do not let them interrupt the entire review.

## II. Reconstruct the Goals and Current State

Based on your findings, explain the following in concise terms:

- What problem is this project or change trying to solve?
- What approach is currently being taken?
- Which files or code led to this decision?
- What are the key assumptions on which the current approach depends?
- What information remains uncertain?

If there are discrepancies between the documentation and the code, clearly point out the differences and explain which one you adopted as the basis for your decision.

## III. Conduct an Approach Review First

Temporarily set aside your local coding style and return to the project goals to check if the current route is appropriate.

Key considerations:

- Does the current solution truly meet the requirements?

- Is it complicating a simple problem?

- Has the early decision resulted in a large number of subsequent patches?

- Are permission, security, or state issues stemming from the architecture itself?

- Can the current problem be resolved with a local fix?

- Are there other solutions that can eliminate this type of problem at its root?

- Is the cost of migrating to an alternative solution worthwhile?

Don't be constrained by the amount of existing code or development investment. Just because a lot of code has been written doesn't mean the current solution should be continued.

If a meaningful alternative solution exists, compare it to:

- Requirements coverage
- Security risks
- Implementation complexity
- Maintenance costs
- Performance and resource costs
- Impact after an error occurs
- Difficulty of migration and rollback

Don't force alternative solutions just to meet formatting requirements. If the current solution is already reasonable, directly explain why it's worth retaining.

Finally, please come to one of the following conclusions:

- Keep the current plan
- Adjust the current plan
- Change the plan
- Missing key information makes a decision impossible at this time

Please do not provide code patches before reaching a root conclusion.

## IV. Next, conduct an implementation review

If the current plan is still worth keeping, please check the specific implementation. Includes the following:

- Functional and logic errors
- Permissions, authentication, and data leakage risks
- Input validation and exception handling
- Concurrency, state consistency, and resource release
- Performance issues
- Test gaps
- Implementations that do not match requirements or design
- Structural issues that increase subsequent maintenance costs

For each issue, include the following:

- Severity: Critical / High / Medium / Low
- Confidence: High / Medium / Low
- Evidence of corresponding files, code, or configuration
- Specific scenarios causing the problem
- Possible consequences
- Proposed course of action
- Is this a root cause or a surface symptom?

If multiple issues stem from the same root cause, explain them in a unified manner and prioritize the root cause's handling solution.

## V. Controlling Review Quality

Adhere to the following rules:

- Do not raise issues simply to meet the number.
- State directly if no new significant issues are found.
- Distinguish between confirmed defects, reasonable risks, and speculations awaiting verification.

- Do not write theoretical possibilities as existing bugs if there is no evidence in the code or documentation.
- Do not treat personal style preferences as defects.
- Do not repeat issues that have already been fixed.
- Do not check only local patches; check the caller, data flow, and scope of impact.
- For low-probability, low-impact issues, explain whether they are worth addressing.
- Do not modify the code unless I explicitly request implementation later.
- If continuing the review will reduce revenue, explicitly suggest stopping.

## VI. Output Format

Please output in the following order:

1. Repository Investigation Scope
2. Project Goals and Current Plan
3. Key Information Still Unconfirmed
4. Key Assumptions of the Current Plan
5. Plan-Level Issues
6. Alternative Plans and Selections
7. Root Conclusion
8. Implementation-Level Issues
9. Three Top Priorities
10. Temporarily Acceptable Residual Risks
11. Is it Worth Continuing the Next Review?

Please complete the review first and await my decision. Please do not modify the code directly.
