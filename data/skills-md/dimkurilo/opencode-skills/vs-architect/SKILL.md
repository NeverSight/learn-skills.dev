---
name: vs-architect
description: "Generate diverse solution variants with probability estimates using Verbalized Sampling (arXiv 2510.01171). Use when choosing between multiple approaches, debugging with unknown root cause, generating hypotheses or synthetic data, or when direct prompts produce repetitive mode-collapsed responses. Do NOT use for trivial scripts, factual queries, or stable production code."
---

# VS Architect — Agent Instructions

## Two-Phase Workflow

```
PHASE 1: VS Analysis
  Distribution prompt → k variants with probabilities → user selects

PHASE 2: Execution Prompt
  Selected variant → detailed implementation prompt (no VS)
```

---

## Step 0: Input Validation

- **Task context present** (3+ facts: task/constraints/what was tried/files/prompt) → proceed. Any format is valid.
- **No input or < 15 words** → ask: "Describe the task in detail: what needs to be done, constraints, what you've already tried."

---

## PHASE 1: VS Analysis

### Step 1: Classification

Classify the input along 4 axes (see `references/vs-theory.md`, Classification Axes section). Set UNKNOWN for missing axes.

Present classification to user and request confirmation before proceeding to Step 2:

```
TASK CLASSIFICATION:
- Complexity: [TRIVIAL | MODERATE | UNCERTAIN]
- Type: [CODE | STRATEGY | DIAGNOSTIC | CREATIVE | DATA]
- Variants: [FEW | MANY | SINGLE]
- Constraints: [YES | NO]

Confirm? If not — specify what to adjust.
```

### Step 2: Pattern Selection

Apply Decision Tree from `references/vs-theory.md`. Check rules strictly top-to-bottom; first match wins.

### Step 3: Execution Mode Selection

Apply Mode Mapping from `references/vs-theory.md`.

Additional rules:
- Complex mode → first tool call must be read-only (Assumption Checkpoint)
- 25+ tool calls → Business Outcome Verification pause
- ≥2 external systems with unverified API contracts → Pro
- Subagent task() calls → append 【思维模式要求】 injection

### Step 4: VS Prompt Construction

Use the template from `references/vs-theory.md` (Prompt Templates section) for the selected pattern.

Parameters:
- k (variant count): default 5. D → 5 (many rounds). B → 5. C → 3–5
- Probability threshold: B → p < 0.10 (diversity) or p > 0.5 (stability)
- Output format: headers + sections (human-readable), JSON (subagent)
- Language: preserve user's input language
- Do not use XML tags — headers are equally readable

---

## PHASE 2: Execution Prompt

### Step 5: Construction

After user selects a variant — build an execution prompt without VS:

```
Task: [selected variant from VS analysis]
Context: [what is already known, constraints]

What to do:
- [concrete steps]
- [which files/systems]
- [constraints]

Output format: [what is expected]

Agent1st: Mode: [mode], injection for subagent calls.
```

---

## Step 6: Output Format

```
## VS-ARCHITECT RESULT

### ANALYSIS
- Complexity: [...]
- Type: [...]
- Variants: [...]
- Constraints: [...]

### PHASE 1: VS ANALYSIS
Pattern: [A/B/C/D/E/F/G/none]
Mode: [...]

VS ANALYSIS PROMPT:
[generated prompt]

ACTION: Select the best variant and say "selecting variant N" — I will build the execution prompt.

### PHASE 2: EXECUTION PROMPT (after selection)
[to be built]

### EXECUTION
1. New DeepSeek V4 session: copy the VS prompt, get hypotheses, select
2. Current session: run VS prompt via subagent or direct dialogue
3. After selection: return — I will build the execution prompt
```

---

## Agent1st Integration

- **Assumption Checkpoint:** Complex Mode → diagnostic command before execution
- **Failure Packet:** 2+ identical errors → 3-field packet. Generate root cause hypotheses using pattern A or C
- **Verification:** VS analysis — user selected a relevant variant. Execution — test command (curl, test, run)
- **Act Immediately:** TRIVIAL → skip VS, recommend direct prompt
- **Pro Mode:** ≥2 unverified external systems → Pro
- **Subagent Injection:** task() → append 【思维模式要求】 at end of prompt

---

## Patterns Overview

| Pattern | When | What it does |
|---------|------|-------------|
| **A** VS-Standard | Moderate complexity, 3-5 variants | Single call → k variants with probabilities |
| **B** Diversity Tuning | Uniform responses from direct prompt | Filters by probability threshold (p < 0.10 or p > 0.5) |
| **C** VS-CoT | Uncertainty, diagnostics, strategy | Step-by-step reasoning first, then variant distribution |
| **D** VS-Multi | Need 10+ variants | Multiple rounds, each round excluding previous ideas |
| **E** External Collapse | External constraints LLM doesn't know about | User weights variants by own criteria (budget, time) |
| **F** VS-Refine | Interesting ideas need elaboration | First pass → variants, second pass refines top picks |
| **G** VS-Ensemble | Critical decision needs cross-validation | Two independent VS prompts, results compared |

See `references/vs-theory.md` for complete decision tree, classification axes, and templates.
See `references/examples.md` for real-world usage examples.
