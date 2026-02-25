---
name: down-skilling
description: >-
  Distill Opus-level reasoning into optimized instructions for Haiku 4.5
  (and Sonnet). Generates explicit, procedural prompts with n-shot examples
  that maximize smaller model performance on a given task. Use when user says
  "down-skill", "distill for Haiku", "optimize for Haiku", "make this work
  on Haiku", "generate Haiku instructions", or needs to delegate a task to
  a smaller model with high reliability.
metadata:
  author: Oskar Austegard and Opus
  version: 1.0.0
---

# Down-Skilling: Opus → Haiku Distillation

Translate your reasoning capabilities into explicit, structured instructions
that Haiku 4.5 can execute reliably. You are a compiler: your input is
context, intent, and domain knowledge; your output is a Haiku-ready prompt
with decision procedures and diverse examples.

## Core Principle

Opus infers from WHY. Haiku executes from WHAT and HOW.

Your job: convert implicit reasoning, contextual judgment, and domain
expertise into explicit procedures, concrete decision trees, and
demonstrative examples. Every inference you would make silently, Haiku
needs stated explicitly.

## Activation

When triggered, perform these steps:

1. **Extract task context** from the conversation: what is the user trying
   to accomplish? What domain knowledge applies? What quality criteria
   matter?

2. **Identify the reasoning gaps** — what would Opus infer automatically
   that Haiku needs spelled out? Common gaps:
   - Ambiguity resolution (Opus picks the sensible interpretation; Haiku
     needs a decision rule)
   - Quality judgment (Opus knows "good enough"; Haiku needs explicit
     criteria)
   - Edge case handling (Opus reasons through novel situations; Haiku
     needs enumerated cases)
   - Output calibration (Opus matches tone/length intuitively; Haiku
     needs explicit constraints)

3. **Generate the distilled prompt** following the structure in
   [Prompt Architecture](#prompt-architecture)

4. **Generate 3-5 diverse examples** following the principles in
   [Example Design](#example-design)

5. **Deliver** the complete Haiku-ready prompt as a copyable artifact or
   file, including system prompt and user prompt components as appropriate

## Prompt Architecture

Structure every distilled prompt with these components in this order.
Haiku responds best to this specific sequencing:

```
<role>
[Single sentence: who Haiku is and what it does]
</role>

<task>
[2-3 sentences: the specific task, its purpose, and the deliverable]
</task>

<rules>
[Numbered list of explicit constraints. Be precise about:]
- Output format (JSON schema, markdown structure, etc.)
- Length bounds (word/token counts, not vague "brief"/"detailed")
- Required elements (must-include fields or sections)
- Prohibited behaviors (specific failure modes to avoid)
- Decision rules for ambiguous cases
</rules>

<process>
[Numbered steps. Maximum 7 steps. Each step is one action.]
[Include validation checkpoints: "Before proceeding, verify X"]
[Include decision points: "If X, do Y. If Z, do W."]
</process>

<examples>
[3-5 diverse examples showing input → output pairs]
[See Example Design section]
</examples>

<context>
[Task-specific data, reference material, or domain knowledge]
[Use labels: [Context], [Policy], [Reference]]
</context>
```

## Haiku Optimization Rules

Apply these when generating any Haiku-targeted prompt:

### Structure & Syntax
- Use XML tags to delimit every section — Haiku respects labeled boundaries
- Keep sentences under 25 words where possible
- One instruction per sentence; split compound instructions
- Use numbered steps, not prose paragraphs, for procedures
- Specify token/word budgets explicitly: "respond in 80-120 words"

### Reasoning Support
- Replace open-ended judgment with decision rubrics:
  BAD: "Assess whether the code is production-ready"
  GOOD: "Check: (a) no TODO comments, (b) all functions have error
  handling, (c) no hardcoded secrets. Score pass/fail per item."
- Bound reasoning depth: "Think in 3-5 steps, then give your answer"
- Provide a fallback for uncertainty: "If you cannot determine X,
  respond with: 'UNCERTAIN: [brief reason]'"

### Context Management
- Front-load critical instructions (Haiku attends strongly to position)
- Keep total prompt under 2,000 tokens when possible (excluding examples)
- Pass only the 1-3 most relevant context snippets, not full documents
- Use explicit delimiters between context and instructions

### Output Control
- Require structured output (JSON, labeled sections) for extractable results
- Provide an output template Haiku can fill in
- Specify what comes first in the response: "Begin your response with..."
- For classification tasks, enumerate all valid categories

### Failure Prevention
- Anticipate Haiku's common failure modes and add guardrails:
  - **Hallucination**: "Use ONLY information from the provided context.
    If the answer is not in the context, say 'Not found in sources.'"
  - **Verbosity**: "Maximum 150 words. Do not add preamble or caveats."
  - **Format drift**: Include the output schema in both rules and examples
  - **Instruction skipping**: Number all constraints; reference them in
    the process steps: "Apply rules 2-4 from <rules>"

## Example Design

Examples are the highest-leverage element for Haiku performance. Follow
these principles:

### Diversity Requirements
Each example set must cover:
- **Typical case**: The most common input pattern
- **Edge case**: Unusual but valid input (empty fields, very long text,
  special characters, boundary conditions)
- **Negative case**: Input that should be rejected or handled differently
  (if applicable to the task)

### Example Format
```xml
<example>
<input>
[Realistic input data]
</input>
<output>
[Exact format Haiku should produce — not a description, the actual output]
</output>
<reasoning>
[Optional: 1-2 sentences explaining WHY this output is correct.
 Helps Haiku generalize the pattern.]
</reasoning>
</example>
```

### Example Quality Criteria
- Examples must be realistic, not toy data
- Output format must be identical across all examples
- Include the hardest case you expect Haiku to handle
- Vary input characteristics: length, complexity, domain
- Never include an example that contradicts your rules

## Delivery Format

Present the distilled prompt in a code block or artifact with clear
section markers. Include:

1. **System prompt** (if applicable): role + persistent rules
2. **User prompt template**: with {{placeholders}} for variable content
3. **Examples**: embedded in the prompt or as a separate few-shot section
4. **Usage notes**: any caveats about when this prompt may fail and what
   to watch for

When generating for API use, include the model parameter and recommended
settings:
```
model: claude-haiku-4-5-20251001
max_tokens: [appropriate for task]
temperature: 0 (for deterministic tasks) or 0.3 (for creative tasks)
```

## Agentic Resource Selection

The skill includes two directories of granular reference files. Do NOT
read them all. Scan the index below, then read only the files relevant
to the current task.

### gaps/

Each file documents one reasoning pattern where Haiku diverges from Opus,
with a tested mitigation strategy. Read 2-4 per task.

| File | Use when the task involves... |
|------|------|
| `ambiguity-resolution.md` | Input that has multiple valid interpretations; vague user requests |
| `code-generation.md` | Generating code, scripts, or queries; style matching to existing code |
| `comparative-analysis.md` | Comparing options, pros/cons, tradeoff analysis |
| `conditional-logic.md` | Decision trees, branching rules, nested if/then logic |
| `context-utilization.md` | Long context windows, documents >2K tokens, position-sensitive info |
| `counting-enumeration.md` | "Generate exactly N items", counting occurrences, list lengths |
| `creative-generation.md` | Writing, tone adaptation, persona consistency, style matching |
| `implicit-constraints.md` | Tasks where tone, audience, or format norms are assumed not stated |
| `instruction-density.md` | Tasks requiring 8+ simultaneous constraints; complex rule sets |
| `multi-hop-reasoning.md` | 3+ step inference chains; cause-effect-consequence analysis |
| `multi-turn-consistency.md` | Chatbot behavior, stateful conversations, persona maintenance |
| `negation-handling.md` | Constraints phrased as "don't", "never", "avoid"; prohibitions |
| `nuanced-classification.md` | Borderline cases, multi-label classification, overlapping categories |
| `output-calibration.md` | Length control, format precision, verbosity management (ALWAYS read) |
| `parallel-consistency.md` | Generating multiple similar items; lists where format must be uniform |
| `partial-information.md` | Missing fields, incomplete input, optional data, error states |
| `schema-adherence.md` | Structured output (JSON, tables) that must survive edge-case inputs |
| `self-correction.md` | Tasks needing verification; quality checks before output |
| `summarization-fidelity.md` | Summarizing documents without distortion, position bias, or fabrication |
| `tool-use-planning.md` | Multi-tool workflows, API orchestration, dependency ordering |

### examples/

Complete before/after distillations. Each shows an Opus-level task →
Haiku-optimized prompt with annotated examples. Read 1-2 closest to
the current task domain.

| File | Use when distilling... |
|------|------|
| `api-orchestration.md` | Multi-step tool/API workflows with dependencies and branching |
| `code-review-triage.md` | Analysis tasks with severity classification and structured JSON output |
| `content-moderation.md` | Safety-critical classification with "when uncertain" defaults |
| `creative-rewriting.md` | Tone adaptation, audience-aware rewriting, style transfer |
| `data-extraction.md` | Schema-bound extraction from unstructured text to JSON |
| `document-qa.md` | RAG / retrieval-grounded QA with citation and "not found" handling |
| `email-summarization.md` | Information extraction from conversations/threads into sections |
| `meeting-notes.md` | Transcript processing into decisions, actions, and next steps |
| `resume-screening.md` | Multi-criteria evaluation with parallel scoring structure |
| `sql-generation.md` | Natural language to code with schema constraints and error handling |
| `step-by-step-analysis.md` | Multi-step analytical reasoning with explicit decision rubrics |
| `text-classification.md` | Multi-label classification with confidence and ambiguity handling |

## Self-Check

Before delivering, verify the distilled prompt against these criteria:
- [ ] Every Opus inference is made explicit
- [ ] All constraints are numbered and cross-referenced
- [ ] 3+ diverse examples with consistent output format
- [ ] Total prompt fits within 4,000 tokens (excluding dynamic context)
- [ ] No instruction assumes Haiku will "figure it out"
- [ ] Decision points have explicit branches, not open-ended judgment
- [ ] Output format is demonstrated, not just described
