---
name: prompt-engineering
description: Use this skill when helping write, improve, debug, or optimize prompts for any LLM — whether for agents, API calls, system prompts, or interactive chat. Trigger whenever the user mentions prompts, prompt engineering, system instructions, agent definitions, prompt templates, few-shot examples, chain-of-thought, or asks to make an LLM behave differently. Also trigger when the user is building agents and needs to define or refine the instructions those agents receive. This skill is a router — it provides the core workflow and dispatches to specialized sub-skills for detailed techniques.
---

# Prompt Engineering — Router Skill

Model-agnostic reference for writing effective LLM prompts. This is the entry point — use it for every prompt task, then load the appropriate sub-skill only when you need detailed techniques.

## Workflow

1. **Gather context autonomously** — Before asking the user anything, collect everything you can: what the prompt should accomplish, which model/provider is in use, whether this is a system prompt, user-turn template, or multi-turn agent, and what failure modes exist. Inspect relevant source files, existing prompts, schemas, and tests.
2. **Surface only blocking unknowns** — If critical info is still missing and cannot be reasonably inferred, ask — but only for the specific missing pieces. If you can make a reasonable assumption, state it and proceed.
3. **Select techniques** — Pick from the reference below. Do not over-engineer. A simple task needs a simple prompt.
4. **Draft the prompt** — Keep it as short as possible while remaining unambiguous.
5. **Review against the checklist** — Run through the checklist below before delivering.
6. **Suggest a testing strategy** — Recommend how to validate. For production prompts, recommend building a reusable eval set of 10–30 representative inputs with expected outputs.

**Default posture: act, don't interview.** Deliver a working prompt as quickly as possible. Surface assumptions so the user can correct them.

---

## Model Selection Guidance

Different models respond differently to prompting techniques. General principles:

**Frontier models (GPT-5.4, Claude Opus/Sonnet 4.6, Gemini 3.1 Pro, GLM-5, MiniMax-M2.7, MiMo-V2-Pro):**
- Handle long, complex system prompts well. Can manage 15-20 tools reliably.
- Structured CoT is usually unnecessary — basic "think step by step" or native reasoning mode suffices.
- Lost-in-the-middle effects are minimal but still worth mitigating for very long contexts (100k+ tokens).
- Can follow nuanced negative constraints more reliably.

**Mid-tier models (Claude Haiku 4.5, GPT-4o-mini, Gemini Flash):**
- Keep system prompts concise. Over ~2000 words, instruction-following degrades.
- Reduce tool count to 10 or fewer. Use classify-then-route to narrow tool selection.
- Structured CoT with explicit tags significantly outperforms basic "think step by step."
- Few-shot examples are more important — these models generalize less from instructions alone.
- Lost-in-the-middle is more pronounced. Place critical content at top and bottom.

**Small/local models (< 20B parameters):**
- Keep prompts short and direct. One task per prompt.
- Few-shot examples are essential, not optional.
- Avoid complex output schemas. Prefer flat JSON over nested structures.
- Chain-of-thought helps significantly but keep reasoning steps simple.
- Tool use is unreliable with more than 3-5 tools. Consider hardcoded routing instead.

**Reasoning models (OpenAI o-series, Claude extended thinking, Gemini thinking mode):**
- Do not add explicit CoT — the model reasons internally.
- Give the task directly with clear success criteria.
- These models are slower and more expensive — use for complex reasoning tasks, not simple extraction or classification.

When building a chained pipeline, you can mix models: use a frontier model for the hardest step and a mid-tier model for straightforward extraction or classification steps. This optimizes cost without sacrificing quality where it matters.

---

## Technique Quick Reference

Use this table to decide which sub-skill to load. If the task is simple and you already know what to do, don't load anything — just apply the technique directly.

| Situation | Key techniques | Load skill |
|-----------|---------------|------------|
| Prompt is vague, format is unspecified, output is inconsistent | Clarity, delimiters, few-shot examples, output format specs, field ordering | `prompt-clarity-and-structure` |
| Task requires multi-step reasoning, or a complex workflow needs decomposition | Chain-of-thought, prompt chaining, inter-step validation | `prompt-reasoning-and-chaining` |
| Model hallucinates, ignores source docs, or you're building a RAG pipeline | Grounding, quote-then-answer, source restriction, long context handling, chunking | `prompt-grounding-and-rag` |
| Building an agent with tools, multi-turn conversations, or multi-agent handoffs | Tool descriptions, tool selection, agent loops, termination, state management, handoffs | `prompt-agents-and-tools` |
| Production deployment: injection risks, provider portability, caching, multimodal, debugging | Security hardening, prompt caching, provider differences, negative constraints, debugging failures | `prompt-security-and-production` |
| Need to measure prompt quality, compare versions, or monitor production performance | Eval set design, metrics, A/B testing, regression testing, monitoring | `prompt-evaluation` |

---

## Design Checklist

Before delivering any prompt, verify:

- [ ] A person with no context could follow the instructions unambiguously
- [ ] Output format is explicitly specified (not left to the model's discretion)
- [ ] All variable inputs are clearly delimited from instructions
- [ ] The prompt is as short as possible — every sentence earns its place
- [ ] Examples are included if format consistency matters
- [ ] Business/domain context is explicit enough that the model won't substitute its own assumptions
- [ ] Hallucination safeguards are present if factual accuracy matters
- [ ] For production: untrusted input is separated and the model is told to ignore embedded instructions
- [ ] For agents: termination conditions and tool-use boundaries are defined
- [ ] For chained calls: shared concepts are defined identically across all prompts
- [ ] The prompt's language and register match the desired output style
- [ ] Structured output fields are ordered so upstream fields precede dependent values
- [ ] max_tokens is set high enough that structured output won't truncate; parsed output is validated
- [ ] Data processed by the model (RAG chunks, emails, scraped content) is wrapped in labeled tags and treated as untrusted
- [ ] If the task involves classifying sensitive/harmful content, the role framing makes the legitimate purpose explicit
- [ ] An eval set of representative inputs exists for prompts that will be iterated on
- [ ] The prompt degrades gracefully if the model is swapped (no provider-specific tricks without fallbacks)
- [ ] For production at scale: static content is placed before dynamic content to maximize cache hits
- [ ] Multimodal inputs are placed before the text query, with specific instructions on what to extract
- [ ] Negative constraints are reframed positively only when they demonstrably backfire

---

## Debugging Table

| Symptom | Likely cause | Fix |
|---------|-------------|-----|
| Wrong format | Format spec is ambiguous or missing | Add explicit schema + 2-3 examples |
| Hallucinated facts | No grounding constraints | Add source restriction + quote-first + "say I don't know" |
| Skipped steps | Too many instructions in one prompt | Break into a chain |
| Inconsistent tone | No role or role is too vague | Add a specific persona in the system message |
| Calls wrong tool | Tool descriptions vague or overlapping | Sharpen descriptions, reduce tool count, add negative constraints |
| Agent won't stop | No termination condition | Add explicit completion criteria |
| Works sometimes | Ambiguity resolved differently each run | Add examples + tighten wording |
| Ignores constraints | Constraints buried in middle of long prompt | Move constraints to end, near the query, or repeat |
| Injection / jailbreak | No input separation | Apply security techniques → load `prompt-security-and-production` |
| Drifts over many turns | System prompt diluted by long context | Reiterate key rules, summarize history, test at turn 50 |
| CoT hurts reasoning model | Explicit CoT on a model that reasons internally | Remove CoT instructions, let model think natively |
| Output uses wrong domain meaning | Business context missing or vague | Add operational definitions for key terms |
| Chained steps contradict | Shared concepts defined differently per step | Extract common definitions into shared preamble |
| Tone doesn't match intent | Prompt language misaligned with desired register | Rewrite prompt in same style as expected output |
| JSON fields seem incoherent | Type generated after the content it governs | Reorder: types/categories precede dependent values |
| Truncated / broken JSON | Response hit max_tokens mid-output | Increase max_tokens, request compact output, validate schema |
| Model refuses legitimate task | Content looks harmful out of context | Add role framing clarifying legitimate purpose |
| Injection via processed data | RAG/emails contain embedded instructions | Wrap data in labeled tags, treat as data only |
| Prompt changes break unpredictably | No eval set — testing by vibes | Build reusable set of 10-30 inputs, run before every change |
| "Do not X" causes X | Negative constraint triggers attention on prohibited concept | Reframe positively: tell the model what to do instead |
| Prompt breaks after model upgrade | Phrasing calibrated to old model's tendencies | Re-evaluate against eval set after any model version change |
| High API costs on repeated calls | Static prompt re-processed every call | Restructure for cacheability: static prefix, dynamic suffix |
| Model misinterprets image | Image placed after query, or no visual instructions | Place images before text, add specific visual instructions |
| Chained step produces garbage | No validation between steps | Add schema validation, design downstream to be resilient |
