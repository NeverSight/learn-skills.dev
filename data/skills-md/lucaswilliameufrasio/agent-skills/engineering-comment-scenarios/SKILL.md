---
name: engineering-comment-scenarios
description: "Turn technical analysis, bug investigations, review findings, audit responses, and blockers into short, direct, human issue-tracker or pull-request comments. Use when drafting an engineering comment for Jira, GitHub, Bitbucket, or similar, and the scenario is a decision response, bug triage, code-review finding, or blocker."
---

# Engineering comment scenarios

Act as a pragmatic tech lead. Convert raw analysis into a comment with the highest signal-to-noise ratio: the least text that still gives the reader the technical and business facts. Use `comment-writing` for general principles; this skill adds scenario structures.

## Style rules

- No greeting or empty introduction ("Hi team", "Based on the analysis...", "I'd like to update...").
- No ceremonial closing ("Let me know if you have questions", "Best regards").
- No inflated corporate or passive-aggressive phrasing ("as previously aligned", "kindly").
- At most 2–3 short blocks. Use simple lists; bold only operational terms.
- Reference issues by key (e.g. `PROJ-123`) and mention people naturally with their role (e.g. `@Name (Product)`, `@Name (QA)`), only when the person is identified and the channel supports real mentions.
- Write in the language of the thread or the user's request.
- Never state a fix, test, or deploy as done without evidence; separate "proposed", "in progress", and "verified". Do not invent keys, names, numbers, or deadlines.

## Workflow

1. Identify the matching scenario below; if none fits, apply the style rules with the closest structure.
2. Extract only the critical facts: root cause, impact, decision, next step.
3. Output only the final comment, ready to paste, with no meta-commentary. If a fact that changes the ask is missing, ask first.
4. Do not post unless publication was explicitly authorized.

## Scenarios

### 1. Response to an audit, security finding, or business decision

Structure:
- Context of the original decision, with referenced stories/tickets.
- What is technically valid and needs adjustment.
- Next step, and who decides if a rule changes.

Example:

> Not requiring special characters and uppercase letters was a product/UX decision to reduce signup friction (PROJ-101, validated in PROJ-102 and PROJ-103). The only agreed blocker in the app is a minimum of 8 characters (PROJ-104).
>
> That said, the finding is valid in two places:
> 1. **Backend mismatch:** the API (PROJ-105) still accepts 4+ characters. We'll ship a fix enforcing 8 characters server-side.
> 2. **Weak/common passwords:** worth adding a basic check against sequential or obvious values (e.g. `12345678`).
>
> If the audit considers uppercase and symbols mandatory, we need `@Name (Product)` to weigh the funnel impact and decide whether to change the rule or accept the risk.

### 2. Bug triage or investigation

Structure:
- Root cause in one or two sentences (where it breaks and why).
- Current vs expected behavior.
- Proposed fix and affected scope.

Example:

> The 500 on checkout comes from a type mismatch in the payload the payment gateway returns when the status is `PENDING_REVIEW`; it throws a null-pointer error in the transaction parser (`payment-service`).
>
> - **Current:** the webhook fails and the transaction stays stuck with no retry.
> - **Proposed fix:** handle the null payload with a fallback for the intermediate state and reprocess the pending dead-letter messages.
>
> Opening a hotfix branch today for QA validation with `@Name (QA)`.

### 3. Code review or critical PR finding

Structure:
- The specific technical problem (concurrency, performance, contract break).
- Practical impact in production.
- A direct suggestion or alternative.

Example:

> Purging in a single batch query with no pagination limit will lock the table at peak hours; this entity grows by more than 500k rows per day.
>
> Either delete in chunks of 5,000 with a short pause between iterations, or run it asynchronously in a dedicated worker outside the API transaction.
>
> Marking the PR as blocked until we settle the strategy, to avoid loading the database.

### 4. Deadline or blocker

Structure:
- What blocked the item (external dependency, infrastructure drift, contract break).
- Direct impact on the sprint/delivery.
- Options to unblock, or the decision needed.

Example:

> PROJ-200 is blocked: the staging gateway route diverged from the repository declaration and lost its link to the authorizer function.
>
> - **Impact:** the integrated flow can't be tested in the app until the route is restored.
> - **Action:** pushing a declarative fix to remove the drift. This delays the card by about half a day but doesn't endanger the sprint goal if it reaches QA by end of day.

The examples are illustrative; replace every key, name, and number with real, verified values.
