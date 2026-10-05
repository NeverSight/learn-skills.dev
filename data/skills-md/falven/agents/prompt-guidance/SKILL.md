---
name: prompt-guidance
description: Review, rewrite, and design prompts using bundled model-specific guidance. Use for prompt migration, prompt reviews, system/developer prompt tuning, outcome-first instructions, retrieval and citation budgets, creative drafting guardrails, frontend or coding prompt guidance, validation loops, Responses API phase handling, and prompt behavior around reasoning effort or text.verbosity. Current bundled documentation covers GPT-5.5 only. Do not use for broad OpenAI API support, pricing, or model availability unless the request is about prompt behavior.
---

# Prompt Guidance

Use this skill to adapt prompts from model-specific guidance. Keep `SKILL.md` as the workflow router; read the relevant bundled reference before rewriting or reviewing prompts.

The only bundled reference today is GPT-5.5 guidance. If the user requests another model and no matching reference exists, use official OpenAI docs before making model-specific claims, or state that the skill currently only includes GPT-5.5 documentation.

## Workflow

1. Classify the prompt surface: customer assistant, grounded Q&A, creative drafting, frontend/coding agent, long-running tool workflow, or general product prompt.
2. Identify the target model. If none is specified, use the bundled GPT-5.5 reference as the default baseline and say so when it matters.
3. Read [references/gpt-5-5-prompt-guidance.md](references/gpt-5-5-prompt-guidance.md) before giving the final rewrite or review.
4. Preserve the user's product contract first: audience, required behavior, source limits, side-effect limits, output shape, and any true safety or business invariants.
5. Convert legacy process-heavy instructions into outcome-first guidance: role, goal, success criteria, constraints, output, and stop rules.
6. Keep absolute words such as `always`, `never`, `must`, and `only` only for true invariants. For judgment calls, write decision rules.
7. Add concise personality and collaboration style only when the prompt powers a user-facing or collaborative experience.
8. For grounded answers, add citation requirements, missing-evidence behavior, and a retrieval budget that says when to stop searching.
9. For tool-heavy or coding agents, add preamble guidance, concrete validation expectations, and Responses API `phase` handling notes when assistant items are manually replayed.
10. Return the revised prompt or review in the structure the user requested. If unspecified, return the revised prompt plus short change notes and any assumptions.

## Boundaries

- Do not invent OpenAI model availability, pricing, API limits, or feature support. Use official OpenAI docs for those questions.
- Do not broaden the task into automated migration, prompt optimizer integration, eval design, or API rewiring unless the user asks.
- Do not preserve obsolete prompt scaffolding just because it exists. Keep only instructions that change model behavior or protect the product contract.
- Do not claim bundled references are current when the user asks for latest guidance; refresh the official Markdown source in that case.

## Output

For rewrites, provide:

- the revised prompt, ready to paste
- the important changes made, kept short
- assumptions or fields the user should fill in

For reviews, provide:

- findings ordered by impact
- exact prompt sections or lines when available
- concrete replacement text for the highest-impact fixes

## Reference Map

- [references/gpt-5-5-prompt-guidance.md](references/gpt-5-5-prompt-guidance.md) -> Current bundled GPT-5.5 prompt guidance derived from OpenAI's LLM-friendly Markdown docs.
