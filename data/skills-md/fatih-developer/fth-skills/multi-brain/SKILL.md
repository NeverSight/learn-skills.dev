---
name: multi-brain
description: Evaluate complex requests from 3 independent perspectives (Creative, Pragmatic, Comprehensive), reach consensus, then produce complete outputs. Use for architecture decisions, creative content, analysis, and any task where multiple valid approaches exist.
---

# Multi-Brain Consensus Protocol

Evaluate incoming requests from 3 independent perspectives, synthesize a consensus, then produce a **complete and final output** in the appropriate format. This is not just "decide" — it is "decide and deliver."

---

## Workflow

```
1. Understand the request
2. 3 Perspectives → Consensus
3. Determine output format
4. Produce full output
```

---

## Step 1: Understand the Request

If the request is ambiguous or missing critical context, ask **one** clarifying question — never more than one. If the request is clear, proceed directly to Step 2.

---

## Step 2: Three Perspectives

Each instance works independently — none sees the other's reasoning. Each summarizes its approach and rationale in 2–3 sentences.

**Instance A — Creative & Unconventional**
Go beyond conventional solutions. Seek the least expected but potentially most impactful approach. Take calculated risks, but justify them clearly.

**Instance B — Pragmatic & Fast**
Find the most practical, fastest-to-implement solution within existing constraints. Minimize complexity, propose concrete steps, and state trade-offs explicitly.

**Instance C — Comprehensive & Safe**
Consider long-term consequences and risks. Identify edge cases, side effects, and missing information. Prioritize sustainability and resilience.

---

## Step 3: Consensus

Synthesize the three perspectives:
- **Agreement points**: If two or three instances converge, this is likely the right path.
- **Complementary elements**: Combine the strengths of different perspectives.
- **Conflicts**: Which argument is stronger? Why?

---

## Step 4: Determine Output Format

**Mandatory:** The final response must **always** include all 3 perspectives and the consensus decision **before** the main output. Never skip or collapse them — the user must see the reasoning trail.

If the request or context already implies a format, use it. If not, ask the user:

> "Based on the consensus, how should I proceed — a detailed report, working code, or a brief summary?"

### Format Options

**Report / Analysis Document**
When the request involves research, decision-making, or strategy:
- Produce as a Markdown document (offer to save).
- Include sections: Summary, Approaches & Trade-offs, Recommendation, Next Steps.
- Write thoroughly — as if the user will share it with stakeholders.

**Code**
When the request involves implementation:
- Apply the architecture/approach from the consensus.
- Write working, testable code.
- Save files and present them to the user.
- Explain "why this approach" in code comments.

**Brief Summary**
When the user wants a quick answer or it is a simple decision:
- Single paragraph: chosen approach + rationale + next step.

---

## Output Template

Use `references/OUTPUT_TEMPLATE.md` for the standard response structure.

---

## When to Skip

Do **not** start the brainstorm process — respond directly when:
- The question has a single factual answer ("How do I iterate a list in Python?").
- The user explicitly asks for a quick/short answer.
- The task is a simple transformation (translation, reformatting, spell-check).
- The user has already decided and only wants execution.

See `references/SKIP_CONDITIONS.md` for the full decision matrix.

---

## Examples

See `references/EXAMPLES.md` for 3 worked examples covering report, code, and brief summary outputs.

---

## Guardrails

- **Always show all 3 perspectives and the consensus in the response** — they are not internal reasoning, they are part of the deliverable.
- Each instance must reason **independently** — no cross-contamination.
- Keep individual perspectives to **2–3 sentences** — concise reasoning, not essays.
- Consensus must explicitly address **conflicts**, not just average opinions.
- The final output must be **complete and ready to use** — not a stub or outline.
- Prefer the **pragmatic** path when perspectives are equally strong.

---

## Templates

- Use `templates/brainstorm-report.md.tmpl` for report/analysis outputs.
- Use `templates/brainstorm-brief.md.tmpl` for quick decision responses.
