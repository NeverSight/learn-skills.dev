---
name: context-compressor
description: Compress long conversation histories, large code files, research results, and documents by 70% without losing critical information. Triggers when context window fills up, when summarizing previous steps in multi-step tasks, before loading large files into context, or on "summarize", "compress", "reduce context", "save tokens".
---

# Context Compressor Protocol

Reduce content by 70% — preserve critical information, discard repetition and noise. Target: compressed output should be ~30% of original size with preserved information density.

---

## Workflow

```
1. Detect content type
2. Mark critical elements (these are never discarded)
3. Apply type-specific compression
4. Verify 70% target
5. Present compressed output
```

---

## Step 1: Detect Content Type

| Content Type | Detection Criteria |
|---|---|
| Conversation history | User/assistant message pairs |
| Code file | Function/class structures, syntax |
| Research results | URLs, source references, data points |
| Meeting notes / document | Headers, bullet lists, decisions |

---

## Step 2: Mark Critical Elements

These elements are **never discarded**:
- **Decisions & conclusions**: "We decided to use X", "Y was chosen"
- **Errors & fixes**: Discovered bugs, applied solutions
- **Numerical data**: Dates, version numbers, metrics, amounts
- **Dependencies**: "A must finish before B" constraints
- **Action items**: Who does what, when
- **Current state**: Latest version, current config, last decision

---

## Step 3: Type-Specific Compression

### Conversation History

**Discard:** Greetings, acknowledgments ("OK", "Got it", "Thanks"), repeated explanations, intermediate reasoning that contradicts the final conclusion.

**Keep:** User's clear requests, decisions and rationale, error messages and fixes, current task status.

**Format:**
```
[CONVERSATION SUMMARY — N messages -> M lines]
Context: [what the task is, 1 sentence]
Decisions: [bullet list]
Current status: [where things stand]
Pending: [open questions if any]
```

### Code File

**Discard:** Comments (except docstrings), excessive blank lines, long import lists (consolidate), temporary debug prints.

**Keep:** All function/class signatures (with parameters), return types and critical type annotations, exception handling, configuration constants. Summarize function bodies as single-line pseudocode.

**Format:**
```python
# [COMPRESSED — original: ~N lines -> now: ~M lines]
class ClassName:
    """[Original docstring]"""
    def method_name(self, param: Type) -> ReturnType:
        # [What it does — 1 line summary]
        ...
```

### Research / Web Results

**Discard:** Duplicate information, generic background, verbose URLs (use domain name), out-of-scope quotes.

**Keep:** Concrete data points, primary source findings, contradictory findings (keep both), directly relevant findings.

**Format:**
```
[RESEARCH SUMMARY — N sources -> M items]
Topic: [what was researched]

Key findings:
- [Finding 1] (Source: domain.com)
- [Finding 2] (Source: domain.com)

Contradictions:
- [Source A says X, Source B says Y]

Missing / unverified:
- [Information not found]
```

### Documents / Meeting Notes

**Discard:** Intro/closing paragraphs (if no content), repetitive statements, generic commentary.

**Keep:** Decisions made, action items (who, what, when), alternatives discussed and why rejected, next steps.

---

## Step 4: Verify 70% Target

```
Original size   : ~N words / lines / tokens
Compressed size : ~M words / lines / tokens
Compression     : ~X% reduction

Target: 70% [Achieved / Below target]
```

If below target (< 50% reduction): re-scan for repetition, compress background more aggressively, convert long examples to single-line references.

---

## Output Header

Every compression starts with:

```
CONTEXT COMPRESSOR
Type    : [content type]
Before  : ~N [words/lines]
After   : ~M [words/lines]
Saving  : ~X% reduction
```

---

## When to Skip

- Content is already short (< 200 words / 50 lines)
- User said "all details matter"
- Legal, medical, or financial documents (information loss risk too high)

---

## Guardrails

- **Never discard decisions or error resolutions** — these are the most valuable context.
- **Preserve contradictions** — if two sources disagree, keep both.
- **Show compression ratio** — the user must see how much was removed.
- **Cross-skill**: works with `memory-ledger` (can compress ledger entries) and `agent-reviewer` (provides compressed history for retrospective).
