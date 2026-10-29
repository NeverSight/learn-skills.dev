---
name: prd-copilot
description: Product requirements workflow for product managers and founders. Use when the user wants to design an AI Agent, AI product, AI assistant, AI-enabled service, or any product requirement from a fuzzy idea, feature request, meeting notes, existing PRD, competitor analysis, or phrases such as "我要做一个 AI Agent", "我要设计一个 AI 产品", "我要做一个AI外卖", "我要做一个AI旅游助手". First judge whether the input is product-requirements related; if not, do not apply this workflow. When requirements are fuzzy, clarify before generating a PRD. Outputs concise Markdown PRDs and selected PRD sections for coding agents or product discussions.
---

# PRD Copilot

## Core Rule

Do not jump straight to a PRD when the user's requirement is ambiguous. First classify the input, check completeness, and ask focused clarification questions when needed. Only generate the PRD once the product direction is sufficiently grounded or the user explicitly accepts assumptions.

Keep the final PRD concise, concrete, and useful for product design, team discussion, or a coding agent. Avoid jargon, inflated strategy language, and decorative text.

## Intake Gate

Before using the workflow, decide whether the user's input is about product requirements or product design.

Use the workflow for:
- Product ideas, AI product concepts, Agent concepts, functional requirements, existing PRDs, meeting notes, user feedback, competitor notes, MVP planning, feature design, and product strategy that leads to buildable requirements.
- Chinese trigger phrases such as "我要做一个 AI Agent", "我要设计一个 AI 产品", "我要做一个AI外卖", "我要做一个AI旅游助手".

Do not use the workflow for:
- Pure implementation/debugging requests, general writing unrelated to a product, casual Q&A, legal/medical/financial advice, or content that has no product requirement intent.

If the workflow should not apply, answer normally and briefly explain that the input does not appear to be a product-requirements task.

## Input Classification

Identify the input type before analysis:
- Product idea: early concept, vague opportunity, or one-sentence idea.
- Feature requirement: a requested capability inside an existing product.
- Existing PRD: a draft requirement document to improve or complete.
- Meeting notes: decisions, pain points, or discussion fragments from a meeting.
- Competitor analysis: references to competing products, screenshots, or feature comparisons.
- User research or feedback: user complaints, jobs-to-be-done, interview notes, or usage data.
- Mixed material: multiple sources combined.

State the classification only if it helps the user understand the next step. Do not add a verbose preamble.

## Completeness Check

Check whether the material contains enough information for a reliable PRD:
- Product goal: what outcome the product should create.
- Target users: who uses it and who pays or decides.
- Core pain points: what problem is urgent enough to solve.
- Usage scenarios: when, where, and how it is used.
- Business goal: acquisition, retention, revenue, cost reduction, efficiency, compliance, or another measurable purpose.
- Core functions: the minimum capabilities needed to solve the pain.
- Constraints: platform, timeline, team, data, compliance, integrations, budget, or technical limits.

If key information is missing or contradictory, ask no more than 5 clarification questions. Prioritize questions that most reduce PRD risk. Use concise Chinese by default when the user writes Chinese.

Do not ask about every missing detail. If a missing detail can be safely handled as a small assumption, list it later under "Assumptions" after the user has answered critical questions.

## Clarification Behavior

When clarification is required:
- Do not generate a full PRD in the same response.
- Ask up to 5 numbered questions.
- Make each question concrete and easy to answer.
- Prefer questions about users, pain point, scenario, success criteria, and MVP boundary.
- If helpful, include short selectable examples, but do not force options.
- End by saying that once these are answered, you will generate the PRD.

If the user asks to proceed despite missing information, continue with explicit assumptions and keep them easy to revise.

## Requirement Analysis

Once enough context exists, analyze the product into:
- Product positioning: one sentence defining what it is and for whom.
- Target users and roles: primary users, secondary users, admins/operators, payers/decision makers if relevant.
- Core pain points: current friction, cost, risk, or unmet need.
- Core value: what gets better after the product exists.
- Key scenarios: main use cases and entry points.
- Business process: upstream inputs, user actions, system actions, downstream outputs.
- User journey: discovery, first use, repeated use, completion, failure/recovery.
- Competitor or reference products: only when present or clearly useful; distinguish facts from assumptions.
- MVP scope: the smallest useful version, plus what is deliberately postponed.

Keep analysis practical. Do not create long strategy sections unless the user requests them.

## AI Product Design

If the product is AI-enabled or Agent-like, decide which AI capabilities are actually needed. Do not add every AI module by default.

Consider:
- Prompt design: needed when LLM behavior, tone, reasoning steps, or structured output matters.
- RAG: needed when answers must use private, changing, or domain-specific knowledge.
- Memory: needed when the product must remember user preferences, history, or long-running context across sessions.
- Tool Calling: needed when the Agent must take actions, query systems, book, pay, update records, send messages, or call APIs.
- MCP: needed when tool access should be standardized across external systems or reused by multiple agents/clients.
- Workflow: needed when the product has deterministic multi-step business processes, approvals, handoffs, or state transitions.
- Multi-Agent: needed only when distinct specialized roles materially improve quality, scale, or governance. Avoid it for simple chat or single-flow assistants.

For each selected capability, describe:
- Why it is needed.
- What data/tools it uses.
- What the user sees.
- Main failure or safety handling.

If an AI capability is unnecessary, omit it or mention it briefly in "Out of Scope" when overdesign is a risk.

## Function Breakdown

Break requirements into buildable layers:
- Level 1 module: major product area.
- Level 2 feature: user-facing or system capability inside the module.
- Function point: specific behavior, rule, input, output, state, or permission.

Also define:
- User operation flow: key steps from entry to completion.
- Page or interface logic: pages/screens, core components, empty/loading/error states when relevant.
- Dependencies: data, integrations, permissions, AI services, business rules, or upstream/downstream systems.

Avoid vague features like "智能推荐" without inputs, outputs, and decision rules.

## PRD Output

Generate the final PRD in Markdown. If the user asks for only one part, output only that section.

Use this structure for a complete PRD:

```markdown
# PRD: <Product Name>

## 1. Background
## 2. Product Goals
## 3. Target Users
## 4. Core Scenarios
## 5. Pain Points and Value
## 6. Scope
### 6.1 MVP
### 6.2 Out of Scope
## 7. Functional Requirements
### 7.1 <Module>
#### Feature
- User story:
- Rules:
- Inputs:
- Outputs:
- States:
- Dependencies:
## 8. User Flow
## 9. Page or Interaction Design
## 10. AI Capability Design
## 11. Data and Metrics
## 12. Exceptions and Edge Cases
## 13. Risks and Constraints
## 14. Release Plan
## 15. Open Questions
```

Adapt the structure to the product. Remove empty sections. Keep bullets concrete and short.

## Review Before Final Output

Before finalizing, review the PRD for:
- Requirement conflicts.
- Duplicate or overlapping features.
- Overdesigned AI capabilities.
- MVP scope that is too large.
- Missing critical business logic.
- Missing exception flows.
- Unrealistic technical complexity.
- Unclear success metrics.
- Unstated assumptions.

If issues are found, include a short "Review Notes" section before or after the PRD with actionable fixes. If the PRD already incorporates the fix, mention it briefly.

## Output Style

Use Chinese when the user writes Chinese, otherwise match the user's language. Be concise. Prefer tables only when they improve scanability. Make assumptions explicit. Keep the document suitable for direct handoff to a product team, designer, or coding agent.
