---
name: ai-customer-analysis
description: >-
  Analyze customer data (transcripts, surveys, interviews) with AI while
  preventing the 4 failure modes that silently break qualitative research.
  Use when analyzing customer interviews, processing transcripts, making
  sense of survey data, getting insights from customer calls, or working
  with any qualitative or mixed data.
---

# AI Customer Analysis — Verified Insight Protocol

Most AI-assisted customer analysis produces confident-sounding outputs that are wrong. The model doesn't analyze your data — it generates the most statistically likely answer, which is almost always what you already believe, formatted as insight.

This skill enforces a verification protocol that prevents the 4 failure modes before they reach your decisions.

---

## The 4 Failure Modes

**1. Invented Evidence**
The model fabricates or misattributes quotes. It sounds specific but the source doesn't exist or says something different.

**2. False or Generic Insights**
Surface-level patterns that are technically true but don't distinguish your customers from any other product's customers. Useless for decisions.

**3. Signal Without Direction**
Observations that don't tell you what to build, change, or stop doing. Insight that doesn't guide a decision is noise.

**4. Contradictory Insights**
The model averages conflicting customer perspectives into a single coherent-sounding narrative. Real tensions in your data disappear.

---

## How It Works

1. **Anchor to exact words** — force the model to quote the customer verbatim before drawing conclusions
2. **Demand source timestamps** — every insight must cite a specific participant and timestamp that can be verified
3. **Segment before summarizing** — group customers by actual behavior or need, not by what they said they want
4. **Challenge the literal request** — if customers ask for "a screen", ask what problem the screen solves
5. **Surface contradictions explicitly** — require the model to identify customers who disagree with the main finding
6. **Run the verification pass** — after the first output, re-run with a second prompt that audits the first for failure modes

---

## Usage

Tell your agent:
> "Analyze these customer transcripts using the ai-customer-analysis skill"

Or trigger naturally:
> "I have 12 customer interview transcripts — help me find real insights"
> "What are customers actually asking for in these survey responses?"

---

## Rules

→ Load `rules/anchor-to-exact-words.md`
→ Load `rules/demand-timestamps.md`
→ Load `rules/segment-before-summarizing.md`
→ Load `rules/surface-contradictions.md`
→ Load `rules/verification-pass.md`

---

## Output Format

For each insight, produce:

```
INSIGHT: [one sentence — specific, directional, actionable]
EVIDENCE: [exact quote] — [participant ID, timestamp]
SEGMENT: [which customer type this applies to, not all customers]
CONTRADICTIONS: [quote from a customer who disagrees] — [participant ID, timestamp]
DECISION: [what this means for the product — specific action or explicit non-action]
```

Do not produce an insight without all 5 fields. If you cannot fill a field, the insight is not ready.

---

## Verification Pass

After producing initial insights, run this audit:

1. Can every quote be traced to a specific participant + timestamp?
2. Does each insight tell you something you couldn't have known without this data?
3. Are there customers in the dataset who contradict the main finding?
4. Does each insight suggest a specific action — not just "consider" or "explore"?
5. Does any insight recommend something that would apply to any product in your category?

If any check fails: remove or rewrite the insight before presenting to stakeholders.

---

## Troubleshooting

**Model gives confident output with no citations**
→ Re-prompt: "Show me the exact quote and timestamp from the transcript that supports each insight."

**All insights are positive / no contradictions found**
→ Re-prompt: "Find me the customer in this dataset who would disagree with your main finding."

**Insights are generic ("customers want simplicity")**
→ Re-prompt: "What specifically about simplicity? Name the exact workflow step they found complex."

**Model says "participants mentioned X" without attribution**
→ Reject the output. Re-prompt: "Name which participant and at what point in the interview."
