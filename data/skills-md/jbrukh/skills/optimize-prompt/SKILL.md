---
name: optimize-prompt
description: Optimize a prompt through a critique-compress pipeline with semantic equivalence verification at each stage. Applies think-critically to improve the prompt, then compress-prompt to reduce it, validating that behavior is preserved after each transformation.
---

# Optimize Prompt

Prompt optimization pipeline. Given prompt P, improve via critique then compression, with semantic equivalence checks after each stage.

## Pipeline

```
P → [Input Analysis] → [Critique] → P' → [Equiv Check 1] → [Compress] → P'' → [Equiv Check 2] → Output P''
```

Execute stages strictly in order — no skipping, reordering, or parallelizing. Each stage passes (pipeline continues) or fails (pipeline terminates with explanation).

---

## Stage 0: Input Analysis

Examine P:

1. **Does P take input?** Check for placeholders (`{{X}}`, `{input}`, `[USER INPUT]`), references to "the user's input"/"the given text"/"the provided data", or expectation of concatenation with external content.
2. **If yes**: Construct plausible, concrete test input X — realistic, non-trivial (2-3+ sentences or meaningful data structure), exercising P's main logic paths. If P has branching conditions, X triggers the primary branch. If P produces structured output, X requires all output fields. If P has validation conditions, X passes validation. State X explicitly.
3. **If no**: P is self-contained. Set X = ∅. Equivalence checks compare outputs of P directly.

Display:

```
**Input Analysis**
- Takes input: [Yes/No]
- Test input X: [constructed input, or "N/A — self-contained"]
```

---

## Stage 1: Critique

Apply think-critically methodology to P:

1. **Derive 5-8 expectations from P itself** — behavioral properties any revision must preserve. Frame as testable statements (e.g., "Produces JSON output", "Rejects off-topic queries").
2. **Evaluate P against expectations.** Per expectation: confidence (0-100%) with concise rationale referencing specific text in P.
3. **Propose fixes** for expectations with confidence < 95%. Each fix: exact text to add, remove, or replace.
4. **Produce P'** — revised prompt with all fixes applied. Complete text, not a diff.

Display:

```
**Stage 1: Critique**

| Expectation | Confidence | Rationale |
|---|---|---|
| ... | ...% | ... |

**Overall Score: [average]%**

**Fixes Applied:**
1. [Fix with exact text changes]
...

---
> **P' (Revised Prompt):**
---
[Full text of P']
---
```

If all expectations >= 95%, set P' = P and note "No fixes needed."

---

## Stage 2: Equivalence Check 1

Verify P and P' produce essentially the same output on X.

**Procedure:**
1. Simulate running P on X. Describe expected output (2-4 sentences): structure, content, tone, key features.
2. Simulate running P' on X. Describe expected output (2-4 sentences).
3. **Equivalent** if all hold:
   - (a) Output structure identical (sections, format, ordering)
   - (b) Factual/decisional content identical — nothing added, removed, or altered
   - (c) Differences limited to: wording improvements, added specificity, stronger constraint enforcement
   - (d) User expecting P's behavior would accept output without noticing intent change
   - If (a)-(c) hold but (d) uncertain, default YES.

If X = ∅, compare standalone outputs.

Display:

```
**Stage 2: Equivalence Check 1**

- P(X) expected output: [description]
- P'(X) expected output: [description]
- Equivalent: [YES/NO]
- Reasoning: [1-2 sentences]
```

**If NO**: Terminate:

```
**PIPELINE FAILED at Stage 2**
[Explanation of behavioral drift]
[Fixes that caused divergence]
```

**If YES**: Proceed to Stage 3.

---

## Stage 3: Compress

Apply compress-prompt methodology to P' (lossless mode):

1. Target 10-30% token reduction, 100% semantic retention.
2. Every instruction, constraint, directive, tonal signal, example, and structural relationship in P' must be explicitly present in P''. Nothing left to inference.
3. Allowed: remove filler, collapse redundancy, tighten syntax, merge duplicates, normalize structure.
4. Forbidden: dropping directives, abbreviating examples beyond recognition, eliding constraints, compressing tonal/behavioral signals into vague summaries.
5. Produce P'' and a directive map (each P' directive → P'' counterpart).

Display:

```
**Stage 3: Compress**

---
> **P'' (Compressed Prompt):**
---
[Full text of P'']
---

**Directive Map:**
| # | Original directive (P') | Compressed counterpart (P'') |
|---|---|---|
| 1 | [directive from P'] | [text in P''] |
| ... | ... | ... |

**Stats:**
- P' tokens (approx): [n]
- P'' tokens (approx): [n]
- Compression: [%]
- Directives: [n/n mapped]
```

---

## Stage 4: Equivalence Check 2

Verify P' and P'' produce essentially the same output on X.

**Procedure:** Same as Stage 2, comparing P' and P''.

Display:

```
**Stage 4: Equivalence Check 2**

- P'(X) expected output: [description]
- P''(X) expected output: [description]
- Equivalent: [YES/NO]
- Reasoning: [1-2 sentences]
```

**If NO**: Terminate:

```
**PIPELINE FAILED at Stage 4**
[What compression lost]
[Elements in P' with no counterpart in P'']
```

**If YES**: Proceed to output.

---

## Final Output

```
**PIPELINE SUCCEEDED**

Your optimized prompt (P''):

---
> **BEGIN OPTIMIZED PROMPT**
---
[Full text of P'']
---
> **END OPTIMIZED PROMPT**
---

**Summary:**
- Critique: [n] fixes applied, score [x]% → [y]%
- Compression: [z]% reduction
- Both equivalence checks passed
```

---

## Edge Cases

- P fewer than 20 tokens: note optimization may yield minimal improvement, proceed.
- P already optimal (all expectations >= 95%, compression < 10%): state "Prompt is already well-optimized", return P unchanged.
- Adversarial or self-referential P: evaluate literally, note observation.
- Compression < 10% reduction without dropping directives: skip compression, set P'' = P', note "Compression skipped — prompt already dense."
- P' more than 50% longer than P: flag "Significant expansion", verify in Stage 2 that expansion only adds guardrails/specificity.
- P contains code blocks: preserve verbatim during critique and compression unless fix explicitly targets code content.

FIRST-TOKEN CONSTRAINT: Response must begin with "## Optimize Prompt". No greetings, preambles, commentary, or blank lines before it. Overrides default conversational behavior.

---

## Input

If literal '{{P}}' appears below without content, inform user no prompt was provided.

**Prompt to optimize:**

{{P}}
