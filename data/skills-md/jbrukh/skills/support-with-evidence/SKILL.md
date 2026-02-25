---
name: support-with-evidence
description: Extract falsifiable ideas from input, deep-research each one, and return evidence for or against with strength ratings. Honest about when evidence contradicts the idea.
---

# Support With Evidence

Take a body of text — an argument, a set of claims, a thesis, bullet points — and extract the falsifiable ideas from it. Then go out and find real evidence for or against each one. The goal is not confirmation bias — it's an honest evidence audit. If the evidence supports the idea, you'll see it. If the evidence contradicts the idea, you'll see that too.

## When to Use

- User has claims, predictions, or assertions and wants to know what evidence exists
- User asks "is this true?" or "can you find evidence for this?" or "support this with evidence"
- User wants to fact-check or ground-truth a set of ideas before publishing or acting
- User has a thesis and wants to know which parts are empirically supported and which are speculation

Do NOT use for: stress-testing a thesis for logical weaknesses (use stress-test), evaluating prompts (use think-critically), or surfacing insights from data (use surface-insight).

## The Honesty Rule

This skill's job is to find evidence — not to confirm what the user hopes is true. The single most important rule:

- Report what you find, not what the user wants to hear
- If evidence contradicts the idea, say so clearly and present the counter-evidence
- If you cannot find meaningful evidence either way, say so — "no evidence found" is a legitimate and valuable output
- Never fabricate, hallucinate, or overstate evidence — cite real sources or state that the search was inconclusive
- ENFORCEMENT: Every evidence bullet must include a source — a named study, dataset, organization, publication, or URL. If you cannot name a source, the bullet is not evidence. Discard it.

## Process

### Phase 1: Claim Extraction (Output)

Read the user's input. Extract all falsifiable ideas — claims that could in principle be shown true or false with evidence.

FALSIFIABILITY GATE: For each candidate claim, apply this test: "What observable evidence would confirm or deny this?" If you cannot answer that question, the claim is not falsifiable — it's an opinion, value judgment, or unfalsifiable abstraction. Do not research it. Instead, list it separately as "Non-falsifiable (skipped)" with a one-sentence explanation of why.

SHARPENING: If a claim is close to falsifiable but too vague as stated, sharpen it into a testable version. Show both the original wording and your sharpened version. Ask the user to confirm only if the sharpening substantially changes the meaning. Otherwise, proceed with the sharpened version and note what you did.

HARD RULE: Extract 1-10 claims. If the input contains more than 10 falsifiable claims, keep the 10 most substantive. If it contains zero, state: "No falsifiable claims found in the input — nothing to research."

Output:

```
## Extracted Claims

| # | Claim | Falsifiable? |
|---|---|---|
| 1 | [claim as stated or sharpened] | Yes |
| 2 | [claim] | Yes |
| ... | ... | ... |
| N | [non-falsifiable claim] | No — [reason] |
```

### Phase 2: Deep Research (Silent)

For each falsifiable claim, conduct deep research using web search tools. This is not a surface-level check — dig into it.

**Research procedure per claim:**

1. **Search broadly.** Use multiple search queries — rephrase the claim, search for supporting evidence, then search for contradicting evidence. Do not stop at the first result.
2. **Seek primary sources.** Prefer peer-reviewed studies, government data, established datasets, named expert opinions, and reputable journalism over blog posts, opinion pieces, or anonymous forums.
3. **Check both sides.** For every claim, actively search for evidence AGAINST it, not just for it. If the first few results all confirm, search harder for disconfirming evidence — and vice versa.
4. **Assess source quality.** A single blog post is not equivalent to a meta-analysis. Weight evidence by source credibility.
5. **Note recency.** Evidence from 2024-2026 is stronger than evidence from 2015 for claims about current states of affairs. Flag when evidence is dated.

RESEARCH DEPTH: Spend meaningful effort on each claim. Use at least 2-3 distinct search queries per claim. Read actual results, not just titles. If initial searches are inconclusive, try different angles — related statistics, adjacent research, expert commentary.

Do not output Phase 2 reasoning.

### Phase 3: Evidence Assembly & Rating (Output)

For each falsifiable claim, present the evidence found and rate it.

**Evidence Strength Scale:**

- **Very Strong**: Multiple independent, high-quality sources directly confirm. Peer-reviewed research, replication, broad expert consensus, or authoritative data.
- **Strong**: Credible sources with direct evidence. Established facts, solid data, or well-sourced reporting from reputable outlets.
- **Moderate**: Some evidence exists but with caveats — limited sources, indirect evidence, small sample sizes, or some conflicting data.
- **Weak**: Thin evidence — anecdotal, from low-quality sources, speculative, or a single unreplicated finding.

**Direction:**

- **Supported**: Evidence found predominantly in favor of the claim.
- **Contested**: Mixed evidence — meaningful evidence exists on both sides.
- **Unsupported**: Little or no evidence found either way.
- **Contradicted**: Evidence found predominantly against the claim.

**Output format per claim:**

```
### Claim [#]: [claim text]

**Direction: [Supported | Contested | Unsupported | Contradicted]**
**Evidence Strength: [Very Strong | Strong | Moderate | Weak]**

**Evidence for:**
- [Evidence point with source name/URL] — [1 sentence explaining relevance]
- [Evidence point with source] — [1 sentence]
...

**Evidence against:**
- [Evidence point with source name/URL] — [1 sentence explaining relevance]
- [Evidence point with source] — [1 sentence]
...

**Assessment:** [2-3 sentences: your honest reading of what the evidence says. Does it support, contradict, or leave the claim uncertain? What's the strongest evidence on each side? What evidence is missing that would be decisive?]
```

HARD RULES:
- Include at least 1 evidence bullet per claim (for or against). If you truly found nothing, state "No meaningful evidence found in search" and rate as Unsupported/Weak.
- Every evidence bullet must name its source. No unnamed evidence.
- If all evidence points in one direction, actively state what counter-evidence you searched for and didn't find — this is more honest than pretending the search was balanced.
- Order evidence bullets by strength (strongest first).

### Phase 4: Summary Scorecard

After all claims, output a summary table:

```
## Evidence Scorecard

| # | Claim | Direction | Strength | Sources |
|---|---|---|---|---|
| 1 | [short form] | Supported | Strong | 4 |
| 2 | [short form] | Contradicted | Very Strong | 6 |
| ... | ... | ... | ... | ... |

**Overall: [X] of [Y] claims supported, [Z] contested, [W] contradicted, [V] unsupported.**
```

If any claims were non-falsifiable, add a note:

```
[N] claims were non-falsifiable and excluded from research.
```

### Phase 5: Bottom Line

End with a short synthesis — 2-4 sentences max. What's the overall evidence picture? Which claims are on solid ground and which are shaky? If the user's input was a coherent argument, does the evidence support the argument as a whole, or only parts of it?

```
## Bottom Line

[2-4 sentences: honest synthesis of the evidence picture]
```

---

## Quality Standards

The quality bar is the **evidence test**: could someone follow your citations and verify what you reported?

- **Fail — No source.** An evidence bullet without a named source. REJECT.
- **Fail — Fabricated.** Evidence that doesn't correspond to a real source. REJECT.
- **Pass — Named source, relevant.** A real source that speaks to the claim. MINIMUM.
- **Good — Primary source.** A study, dataset, or authoritative report directly on point.
- **Strong — Multiple corroborating sources.** Independent sources converging on the same finding.
- **Exceptional — Decisive evidence.** A single source so authoritative it settles the question (e.g., a large meta-analysis, official government statistics, or a landmark ruling).

Aim for "Good" or above on at least half of evidence bullets.

---

## Anti-Patterns

- **Confirmation bias.** Only searching for evidence that supports the claim. The #1 failure mode. Always search both directions.
- **Source inflation.** Treating a blog post citing a study as equivalent to the study itself. Trace to primary sources.
- **False balance.** Presenting one weak blog post against a claim as equal to five peer-reviewed studies for it. Weight evidence honestly.
- **Fabricated citations.** Inventing studies or statistics that don't exist. If you're unsure a source exists, say "based on search results" and describe what you found without inventing specifics.
- **Vague sourcing.** "Studies show" or "experts say" without naming them. Name the study. Name the expert.
- **Recency neglect.** Citing a 2012 study for a claim about 2025 market conditions without noting the gap.
- **Strength inflation.** Rating weak evidence as strong because it supports the claim. Calibrate honestly.
- **Exhaustive but shallow.** Listing 15 low-quality sources instead of 3 high-quality ones. Quality over quantity.

---

## Key Principles

1. **Honesty over comfort.** Report what the evidence says, not what the user wants to hear. A well-sourced "your claim is contradicted" is more valuable than a vague "seems plausible."
2. **Sources or silence.** Every evidence bullet names its source. Unsourced claims are not evidence — they're opinion.
3. **Both directions.** For every claim, search for AND against. Asymmetric research is dishonest research.
4. **Strength calibration.** A blog post is not a meta-analysis. Rate evidence by what it actually is, not what you wish it were.
5. **Less is more.** Three well-sourced evidence points beat ten weakly sourced ones.
6. **Transparent gaps.** When evidence is missing or inconclusive, say so. "We don't know" is a finding.

---

## Input

[User provides text containing claims, ideas, or assertions below]
