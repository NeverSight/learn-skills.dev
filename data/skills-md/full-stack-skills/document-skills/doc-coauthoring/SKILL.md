---
slug: doc-coauthoring-partme-ai
displayName: 协作编写高质量文档：提案、RFC、技术方案、战略与跨团队计划
version: 1.0.0
summary: 通过关键问题访谈、证据梳理、结构设计和读者测试，与你共同写出真正能推动评审、决策和执行的提案、RFC、技术规格、战略及跨团队计划。
license: Apache-2.0
name: doc-coauthoring
description: Collaboratively draft, revise, and reader-test substantial documentation such as proposals, RFCs, decision records, technical specifications, strategy documents, and cross-team plans. Use when the user needs help transferring context, shaping an argument, resolving gaps, iterating on an existing document, or validating whether a document works for readers. Use a more specialized document skill when the requested artifact is a product-doc suite, technical tutorial, or API reference.
---

# Document Co-Authoring

Act as an active writing partner. Adapt the depth of the workflow to the request instead of forcing the user through a fixed interview.

## Route specialized artifacts

- Product documentation suites and PRD hierarchies: hand off to the **`full-stack-doc`** skill. Install with: `npx skills add full-stack-skills/document-skills --skill full-stack-doc`.
- Technical tutorials and integration articles: hand off to the **`technical-blog-doc`** skill. Install with: `npx skills add full-stack-skills/document-skills --skill technical-blog-doc`.
- API reference generation: hand off to the **`api-doc-generator`** skill. Install with: `npx skills add full-stack-skills/document-skills --skill api-doc-generator`.

Use this skill alongside a specialized skill when stakeholder context, argument structure, or reader testing is the main challenge.

## Stage 1: Establish the writing contract

Determine from the request and available materials:

- document type and decision it should enable;
- primary and secondary readers;
- desired reader action or understanding;
- required format, length, deadline, and approval constraints;
- source material and authority level;
- target file or shared document, if any.

Ask only questions whose answers materially change the document. Accept shorthand and unstructured context dumps.

## Stage 2: Build an evidence map

Separate the input into:

| Category | Treatment |
|---|---|
| Verified fact | State directly and cite or link when useful |
| Decision | Record owner, rationale, and consequences |
| Constraint | Explain its impact on alternatives |
| Assumption | Label explicitly and identify validation needed |
| Open question | Track owner or next action |
| Opinion | Attribute it or turn it into a reasoned recommendation |

Read referenced files or connected sources when available. Do not claim access to integrations or tools that are not present. Never invent absent stakeholder positions.

## Stage 3: Propose the structure

Offer an outline appropriate to the document's purpose. Explain only non-obvious ordering choices. For an existing document, preserve its useful structure and propose focused changes rather than replacing it wholesale.

Typical decision-document flow:

1. Executive summary
2. Context and problem
3. Goals and non-goals
4. Constraints and evidence
5. Options considered
6. Recommendation and rationale
7. Risks and mitigations
8. Rollout, validation, and ownership
9. Open questions

## Stage 4: Draft and refine

- Draft the highest-value sections first.
- Keep terminology consistent and define ambiguous terms once.
- Prefer concrete claims, examples, and decision criteria over generic prose.
- Preserve the user's voice and requested language.
- Flag evidence gaps inline with `待确认` or an equivalent marker.
- Track major unresolved decisions separately so they are not buried in prose.
- When editing files, show or summarize material structural changes and never overwrite unrelated content.

## Stage 5: Reader testing

Test the document against the actual reader contract:

1. Predict questions a new reader will ask.
2. Check whether the document answers each question without conversation context.
3. Identify ambiguous pronouns, undefined terms, hidden assumptions, unsupported claims, and missing transitions.
4. Verify that the requested decision or action is obvious.
5. Revise and repeat until no material reader gap remains.

When independent agents are available and the test is safe, give a fresh agent the document and reader questions without leaking the intended answers. Otherwise perform a cold-read pass using only the document text.

## Completion contract

Deliver or update the requested artifact, then report:

- the final structure and major decisions;
- unresolved questions and their owners when known;
- evidence that still needs verification;
- reader-test issues found and corrected;
- the exact output location if a file was created.
