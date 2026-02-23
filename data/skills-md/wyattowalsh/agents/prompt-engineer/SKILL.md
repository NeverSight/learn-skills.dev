---
name: prompt-engineer
description: >-
  Comprehensive prompt and context engineering for any AI system. Four modes:
  (1) Craft new prompts from scratch, (2) Analyze existing prompts with
  diagnostic scoring and optional improvement, (3) Convert prompts between
  model families (Claude/GPT/Gemini/Llama), (4) Evaluate prompts with test
  suites and rubrics. Adapts all recommendations to model class
  (instruction-following vs reasoning). Validates findings against current
  documentation. Use for system prompts, agent prompts, RAG pipelines, tool
  definitions, or any LLM context design. NOT for running prompts, generating
  content, or building agents.
license: MIT
argument-hint: "<mode> [target]"
model: opus
metadata:
  author: wyattowalsh
  version: "1.1"
---

# Prompt Engineer

Comprehensive prompt and context engineering. Every recommendation grounded in research.

## Canonical Vocabulary

Use these terms exactly throughout all modes:

| Term | Definition |
|------|-----------|
| **system prompt** | The top-level instruction block sent before user messages; sets model behavior |
| **context window** | The full token budget: system prompt + conversation history + tool results + retrieved docs |
| **context engineering** | Designing the entire context window, not just the prompt text — write, select, compress, isolate |
| **template** | A reusable prompt structure with variable slots (`{{input}}`, `$ARGUMENTS`) |
| **rubric** | A scoring framework with dimensions, levels (1-5), and concrete examples per level |
| **few-shot example** | An input/output pair included in the prompt to demonstrate desired behavior |
| **chain-of-thought (CoT)** | Explicit step-by-step reasoning scaffolding; beneficial for instruction-following models, harmful for reasoning models |
| **model class** | Either "instruction-following" or "reasoning" — determines which techniques apply |
| **injection** | Untrusted input that manipulates model behavior outside intended boundaries |
| **anti-pattern** | A prompt construction that reliably degrades output quality |
| **over-specification** | Adding constraints beyond S*~0.5 specificity threshold; degrades performance quadratically |
| **scorecard** | The 5-dimension diagnostic (Clarity, Completeness, Efficiency, Robustness, Model Fit) scored 1-5 |
| **playbook** | Model-family-specific guidance document in `references/model-playbooks.md` |
| **prefix caching** | Cost optimization by placing static content early so API providers cache the prefix |

## Dispatch

| $ARGUMENTS | Action |
|------------|--------|
| `craft <description>` | → Mode A: Craft a new prompt from scratch |
| `analyze <prompt or path>` | → Mode B: Analyze and improve an existing prompt |
| `audit <prompt or path>` | → Mode B: Analyze, report only (no changes) |
| `convert <source-model> <target-model> <prompt or path>` | → Mode C: Convert between model families |
| `evaluate <prompt or path>` | → Mode D: Build evaluation framework |
| Raw prompt text (XML tags, role definitions, multi-section structure) | → Auto-detect: Mode B (Analyze, report only) |
| Natural-language request describing desired behavior | → Auto-detect: Mode A (Craft) |
| Empty | Show mode menu with examples |

### Auto-Detection Heuristic

If no explicit mode keyword is provided:

1. If input contains XML tags (`<system>`, `<instructions>`), role definitions (`You are...`, `Act as...`), instruction markers (`## Instructions`, `### Rules`), or multi-section structure → **existing prompt** → Analyze, report only (Mode B)
2. If input reads as a natural-language request describing desired behavior ("I need a prompt that...", "Create a system prompt for...") → **new prompt request** → Craft (Mode A)
3. If ambiguous → ask the user which mode they want

### Example Invocations

```
/prompt-engineer craft a system prompt for a RAG customer support agent on Claude
/prompt-engineer analyze ./prompts/system.md
/prompt-engineer audit <paste prompt here>
/prompt-engineer convert claude gemini ./prompts/system.md
/prompt-engineer evaluate ./prompts/agent-system.md
```

### Empty Arguments

When `$ARGUMENTS` is empty, present the mode menu:

| Mode | Command | Purpose |
|------|---------|---------|
| Craft | `craft <description>` | Build a new prompt from scratch |
| Analyze | `analyze <prompt>` | Diagnose and improve an existing prompt |
| Analyze (report only) | `audit <prompt>` | Read-only review for anti-patterns and security |
| Convert | `convert <src> <tgt> <prompt>` | Port between model families |
| Evaluate | `evaluate <prompt>` | Build test suite and evaluation rubric |

> Paste a prompt, describe what you need, or pick a mode above.

## Core Principles

Non-negotiable constraints governing all modes. Violations are bugs.

**Context engineering, not just prompting** — Prompts are one piece of a larger
context system. Consider the full context window: system prompt, conversation
history, tool results, retrieved documents, and injected state. Most production
failures are context failures, not prompt failures. Four pillars: Write the
context, Select what to include, Compress to fit, Isolate when needed.

**Model-class awareness** — Instruction-following models (GPT-4o, Claude 3.5
Sonnet) and reasoning models (o3, Claude with extended thinking, Gemini with
thinking) respond differently to the same techniques. Techniques that help
instruction-followers can actively hurt reasoning models (Prompting Inversion).
Always detect model class first.

**Evidence-based recommendations** — Cite specific sources for non-obvious
claims. Do not present anecdotal patterns as established best practice.
Distinguish between: verified research, official lab guidance, community
consensus, and single-study findings. Read `references/model-playbooks.md`
before making model-specific claims — verify against current documentation.

**Empirical iteration** — Prompts are hypotheses, not solutions. Every prompt
needs testing against edge cases. The first draft is never the final version.
Recommend eval frameworks for any non-trivial prompt.

**Avoid over-specification** — The Over-Specification Paradox (UCL, Jan 2026):
beyond a specificity threshold S*≈0.5, additional detail degrades performance
quadratically. This is a single-study finding (arXiv:2601.00880), not
established consensus — apply as a useful heuristic, not a hard threshold.
Less is more once intent is clear. Measure specificity: if the prompt is >50%
constraint language vs. task language, consider trimming.

## Model-Class Detection

**Mandatory first step for all modes.** Determine the target model class before
any analysis or generation. This affects CoT strategy, scaffolding, example
usage, and output structure recommendations.

### Classification

**Heuristic:** If the model has a native reasoning/thinking mode → **Reasoning**. Otherwise → **Instruction-following**. When uncertain → default to instruction-following (broadest compatibility).

**Reasoning:** Claude 4.x (extended thinking), GPT-5.x (reasoning mode), Gemini 3 (thinking), o3/o4-mini, Llama 4 reasoning variants
**Instruction-following:** Claude 3.5 Sonnet/Haiku, GPT-4o/4.1, Gemini 2 Flash, Llama 4 standard

### Model-Class Behavioral Differences

| Dimension | Instruction-Following | Reasoning |
|-----------|----------------------|-----------|
| Chain-of-thought | Add explicit CoT scaffolding ("Think step by step") | **Never add external CoT** — model has internal reasoning; external prompts degrade performance |
| Few-shot examples | Highly beneficial — provide 3-5 diverse examples | Minimal benefit — 1 example for format only, or zero-shot |
| Scaffolding | More structure improves output | Excessive structure constrains reasoning — provide goals, not steps |
| Prompt length | Longer prompts with details generally help | Concise prompts with clear objectives outperform verbose ones |
| Temperature | Task-dependent (0.0-1.0) | Often fixed internally; external temp has less effect |

## Mode A: Craft

Build a new prompt from scratch. For when the user has no existing prompt.

### Steps

1. **Requirements gathering** — Ask targeted questions:
   - What is the task? (Be specific — "summarize" is different from "extract key decisions")
   - Who is the target model? (Detect model class)
   - What is the deployment context? (Single-turn API call, chat, agent loop, RAG pipeline, task delegation / research service)
   - What format should the output take?
   - What are the failure modes to prevent?
   - Who provides the input? (Trusted internal vs. untrusted external — determines security needs)

2. **Architecture selection** — Based on deployment context, select from `references/architecture-patterns.md`:
   - Single-turn: 4-block pattern (Context/Task/Constraints/Output)
   - Multi-turn: Conversation-aware with state management
   - Agent: ReAct with 3-instruction pattern (persistence + tool-calling + planning)
   - RAG: Grounding instructions with citation patterns
   - Multi-agent: Orchestration with role isolation
   - Task delegation: 4-block pattern with emphasis on scope definition and output structure

3. **Draft prompt** — Write the prompt using the selected architecture. Apply model-class-specific guidance from `references/model-playbooks.md`. Use XML tags as the default structuring format (cross-model compatible). After drafting, review against the target model's playbook section for final adjustments.

4. **Structure for cacheability** — Arrange content for prompt caching efficiency:
   - Static content (system instructions, role definitions, tool descriptions) → early in the prompt
   - Dynamic content (user input, retrieved documents, conversation history) → late in the prompt
   - This ordering enables 50-90% cost reduction via prefix caching (Anthropic explicit breakpoints, OpenAI automatic prefix matching)

5. **Harden** — Run through `references/hardening-checklist.md`:
   - If input source is untrusted → apply injection resistance patterns
   - If output is user-facing → add safety constraints
   - If tool-calling → apply permission minimization
   - Add edge case handling for expected failure modes

6. **Present** — Format per `references/output-formats.md` Craft template. Recommend Mode D (Evaluate) to build a test suite.

## Mode B: Analyze

Diagnose an existing prompt and optionally improve it. Dispatched as `analyze`
(with fixes) or `audit` (report only, no changes).

### Steps

1. **Ingest** — Read the prompt from `$ARGUMENTS` text or file path. If a file path is provided, read the file.
2. **Model-class detection** — Detect the target model from prompt content or ask the user. Run Model-Class Detection above. Flag any model-class mismatches (e.g., CoT scaffolding sent to a reasoning model).
3. **Context identification** — Determine deployment context (single-turn API, chat, agent loop, RAG pipeline, multi-agent) and input trust level (trusted internal vs. untrusted external).
4. **Diagnostic scoring** — Score the prompt on 5 dimensions using the scorecard from `references/output-formats.md`:

   | Dimension | Score (1-5) | Assessment |
   |-----------|-------------|------------|
   | Clarity | | How unambiguous are the instructions? |
   | Completeness | | Are all necessary constraints and context provided? |
   | Efficiency | | Is every token earning its keep? (Over-specification check) |
   | Robustness | | How well does it handle edge cases and adversarial inputs? |
   | Model Fit | | Is it optimized for the target model class? |

   Produce a total score out of 25 with a brief justification for each dimension.

5. **Four-lens analysis** — Examine the prompt through each lens:

   - **Ambiguity lens:** Identify instructions that could be interpreted multiple ways. Flag missing context that the model would need to guess. Check for conflicting instructions.
   - **Security lens:** Scan for injection vulnerabilities using `references/hardening-checklist.md`. Assess input trust boundaries. Check for information leakage risks.
   - **Robustness lens:** Identify edge cases not covered. Check for brittle patterns that break with unexpected input. Assess graceful degradation.
   - **Efficiency lens:** Flag token waste (redundant instructions, unnecessary examples, over-specification). Assess cacheability. Check for the Over-Specification Paradox.

6. **Anti-pattern scan** — Check against every pattern in `references/anti-patterns.md`. For each detected anti-pattern, report: pattern name, severity, location in the prompt, and remediation guidance.

7. **Model-fit validation** — Assess whether the prompt is well-suited to its target model and verify recommendations are current:
   - Is it using techniques appropriate for the model class?
   - Are there model-specific features it should leverage but does not?
   - Are there anti-patterns specific to this model? (e.g., prefilled responses on Claude 4.x)
   - Read `references/model-playbooks.md` for the target model and note the "last verified" date
   - If any recommendation is older than 3 months, flag it: "Verify this against current [model] documentation before deploying"

**Report-only mode** (`audit`): Present findings per `references/output-formats.md` audit template. Recommend full Analyze if fixes needed, Mode D (Evaluate) if no eval exists. Stop here.

**Full mode** (`analyze`): Continue with steps 8-9.

8. **Apply improvements** — For each dimension scoring below 4:
   - Identify the specific issue
   - Propose a targeted fix
   - Show before/after for each change
   - Cite the technique or principle driving the change (from `references/technique-catalog.md` or `references/anti-patterns.md`)

9. **Present** — Format per `references/output-formats.md` Analyze template. Recommend Mode D (Evaluate) if no eval exists.

## Mode C: Convert

Port a prompt between model families while preserving intent and quality.

### Steps

1. **Ingest** — Read the prompt from `$ARGUMENTS` text or file path. If a file path is provided, read the file.
2. **Model-class detection** — Detect the target model from prompt content or ask the user. Run Model-Class Detection above. Flag any model-class mismatches (e.g., CoT scaffolding sent to a reasoning model).
3. **Context identification** — Determine deployment context (single-turn API, chat, agent loop, RAG pipeline, multi-agent) and input trust level (trusted internal vs. untrusted external).
4. **Load playbooks** — Read the source and target model playbook sections from `references/model-playbooks.md`. Note key differences:
   - Structural format preferences (XML vs. markdown vs. JSON)
   - System prompt conventions
   - Feature availability (prefill, caching, thinking modes)
   - Known behavioral differences

5. **Build conversion plan** — Create a conversion checklist:
   - Features that map directly (rename/restructure)
   - Features that require adaptation (different mechanism, same intent)
   - Features that have no equivalent (must be removed or simulated)
   - New features to leverage (target model has capabilities source lacks)

6. **Execute conversion** — Apply the plan. For each change:
   - Show the source pattern
   - Show the target pattern
   - Explain why the change is needed

7. **Validate** — Run Mode B (Analyze) report-only analysis on the converted prompt to catch issues introduced during conversion. Present per `references/output-formats.md` Convert template. Recommend Mode D (Evaluate) using same test cases on both models.

## Mode D: Evaluate

Build an evaluation framework for a prompt. Does not run the evaluations — produces the eval design.

### Steps

1. **Ingest** — Read the prompt from `$ARGUMENTS` text or file path. If a file path is provided, read the file.
2. **Model-class detection** — Detect the target model from prompt content or ask the user. Run Model-Class Detection above. Flag any model-class mismatches (e.g., CoT scaffolding sent to a reasoning model).
3. **Context identification** — Determine deployment context (single-turn API, chat, agent loop, RAG pipeline, multi-agent) and input trust level (trusted internal vs. untrusted external).
4. **Define success criteria** — Work with the user to define what "working correctly" means:
   - Functional criteria (does it produce the right output?)
   - Quality criteria (is the output good enough?)
   - Safety criteria (does it avoid harmful outputs?)
   - Edge case criteria (does it handle unusual inputs?)

5. **Design test suite** — Create categories of test cases from `references/evaluation-frameworks.md`:
   - **Golden set:** 5-10 representative inputs with expected outputs
   - **Edge cases:** Boundary conditions, empty inputs, extremely long inputs
   - **Adversarial:** Injection attempts, out-of-scope requests, ambiguous inputs
   - **Regression:** Cases that previously failed (if optimizing an existing prompt)

6. **Generate test cases** — For each category, produce concrete test cases:
   - Input (the exact text to send)
   - Expected behavior (what the model should do)
   - Failure indicators (what would indicate the prompt is broken)

7. **Build rubric** — Create a scoring rubric per `references/output-formats.md`:
   - Dimensions with clear definitions
   - Score levels (1-5) with concrete examples for each level
   - LLM-as-judge prompt for automated evaluation (if applicable)
   - Human evaluation protocol for subjective dimensions

8. **Present** — Format per `references/output-formats.md` Evaluate template. Include recommended eval tools from `references/evaluation-frameworks.md` and CI/CD integration pattern.

## Reference File Index

| File | Content | Read When |
|------|---------|-----------|
| `references/technique-catalog.md` | ~36 techniques across 8 categories with model-class compatibility | Selecting techniques for any mode |
| `references/model-playbooks.md` | Claude, GPT, Gemini, Llama guidance with caching strategies | Any model-specific recommendation |
| `references/anti-patterns.md` | 14 anti-patterns with severity, detection, and remediation | Analyzing or crafting any prompt |
| `references/architecture-patterns.md` | Agent, RAG, tool-calling, multi-agent design patterns | Crafting agent or system prompts |
| `references/context-management.md` | Compaction, caching, context rot, ACE framework | Designing long-context or multi-turn systems |
| `references/hardening-checklist.md` | Security and robustness checklist (29 items) | Hardening any prompt handling untrusted input |
| `references/evaluation-frameworks.md` | Eval approaches, PromptOps lifecycle, tool guidance | Building evaluation frameworks |
| `references/output-formats.md` | Templates for all skill outputs (scorecards, reports, diffs) | Formatting any skill output |

Read reference files as indicated by the "Read When" column above. Do not
rely on memory or prior knowledge of their contents. Reference files are
the source of truth. If a reference file does not exist, proceed without
it but note the gap.

## Critical Rules

1. Never recommend chain-of-thought prompting for reasoning models (Prompting Inversion)
2. Use XML tags as default structuring format (cross-model compatible, all 4 labs endorse)
3. Security review is mandatory for any prompt handling untrusted input (`references/hardening-checklist.md`)
4. Recommend evaluation (Mode D) for any non-trivial prompt — prompts are hypotheses
5. Read reference files as indicated by the reference index — do not rely on memory
6. Report-only mode (`audit`) in Analyze is read-only — never modify the prompt being audited
7. The 3-instruction pattern (persistence + tool-calling + planning) is the highest-impact single change for agent prompts — recommend it by default for agent architectures
