---
name: deep-research
description: Use when the user asks to 'research trends', 'analyze a topic', 'fact-check this', 'verify claims', 'what's the state of X', or hands you a document to vet. A disk-first, checkpointed research workflow with three modes — trend research, topic analysis, and fact-checking.
license: Apache-2.0
compatibility: Requires tavily_search/extract tools; Context7 (resolve-library-id, query-docs) optional for technical topics
metadata:
  authors:
    - Artem Rozumenko <artem_rozumenko@epam.com>
  version: "0.1.0"
---

# Deep Research

One workflow, three modes. Pick the mode from the user's intent:

| Mode | Use when |
|---|---|
| **trends** | "what's happening in X", "emerging patterns", "who are the players" |
| **analyze** | "go deep on X", "tradeoffs of X", "SWOT", "compare perspectives" |
| **factcheck** | document or list of claims handed in for verification |

All three share the same workspace + checkpoint discipline below. **Read this section once, then jump to your mode.**

## Workspace & Checkpointing (all modes)

Workspace: `.research/<YYYY-MM-DD>/<mode>_<session>/`

```
00_plan.md         # written before any research
notes.md           # rolling findings, source URLs
checkpoint_NNN.md  # batch results (factcheck) or section drafts (trends/analyze)
report.md          # final output, assembled from disk — never from memory
```

Rules that apply to every mode:

1. **Plan first.** Write `00_plan.md` before searching anything. Include the question, sub-questions, and the sources you intend to hit.
2. **Disk is truth, memory is scratch.** Append findings to `notes.md` as you go with source URLs. If the session dies, you resume from disk.
3. **Checkpoint on a budget.** Every ~10 research steps OR when context approaches ~150K tokens, write a checkpoint and drop detailed research from working memory — keep only 2–3 line summaries.
4. **Assemble the final report from disk.** Use `cat` / `Read` over checkpoints. Never reconstruct from memory.
5. **Resume, don't restart.** On error, `ls` the workspace, read the last checkpoint, continue from the next unprocessed item.

## Mode: trends

Goal: identify the current state and trajectory of a space.

1. Plan sub-questions: who are the players, what's new in the last 6–12 months, what are adoption signals, what are the contrarian takes.
2. `tavily_search` for each sub-question. For technical topics, also `resolve-library-id` + `query-docs` (Context7) to ground claims in current docs.
3. Note publication dates aggressively — anything older than 12 months gets flagged as "background, not signal."
4. Final `report.md`:
   - **State of the space** (2–3 paragraphs)
   - **Key players** (table: name, focus, signal)
   - **Emerging patterns** (bullets, each with a dated source)
   - **Contrarian / risk signals**
   - **Where this is heading** (1 paragraph, clearly labeled as opinion)

Prioritize actionable insight over exhaustive coverage.

## Mode: analyze

Goal: deep, balanced decomposition of a single topic.

1. Plan: break the topic into core components, stakeholder perspectives, and decision axes.
2. Research each component with `tavily_search` / `tavily_extract`. For each, capture both the strongest case for and the strongest case against.
3. Final `report.md`:
   - **Executive summary** (3–5 sentences, no hedging)
   - **Components** (one section each)
   - **Perspectives & counterarguments**
   - **SWOT** (or equivalent: tradeoffs, risks, opportunities)
   - **Recommendation** with reasoning, clearly separated from facts

Depth over breadth. Nuance over coverage.

## Mode: factcheck

Goal: extract every factual claim from a document and label each one with evidence.

### Setup
- `Read` the document.
- Extract **every** factual claim (statements presented as objective truth — stats, dates, quotes, attributions, causal claims). Write all of them, numbered, to `00_claims_extracted.md` **before any verification**.
- Skip opinions, predictions, value judgments. Mark them in a separate `opinions.md` if useful for the final summary.
- Categorize: statistical / historical / scientific / attributional. Order by significance.

### Verification (batches of 8–10)
For each batch:
- `tavily_search` for current/breaking and synthesis-heavy claims, `tavily_extract` for primary-source verification.
- Aim for ≥2 independent sources per claim. Note publication dates and source authority.
- Watch for **context manipulation** (accurate quote, misleading framing) and **outdated facts presented as current**.
- Write `checkpoint_NNN.md` with full findings for the batch, then **drop the details from memory** — keep only `claim# | verdict | confidence` lines.

Checkpoint format:
```markdown
# Checkpoint NNN — Claims X–Y

## Claim #X: <verbatim claim>
**Status**: VERIFIED | FALSE | MISLEADING | UNVERIFIABLE | OUTDATED
**Evidence**: <urls>
**Analysis**: <what the sources say vs. the claim>
**Confidence**: HIGH | MEDIUM | LOW
```

### Final report
Read all checkpoints from disk and assemble `report.md`:

```markdown
## FACT-CHECK REPORT: <doc title>

### Summary
<N claims checked: V verified, F false, M misleading, U unverifiable, O outdated>

### Detailed Findings
<one block per claim, same format as checkpoint>

### Overall Assessment
<one paragraph on the document's factual reliability>
```

Be impartial. Distinguish **FALSE** (contradicted by evidence) from **UNVERIFIABLE** (insufficient evidence either way). Cite sources for every verdict.

## Cross-mode rules

- Never fabricate sources. If you can't find evidence, say so.
- Never include raw page dumps in the final report — summarize and link.
- Flag conflicting evidence rather than picking a winner silently.
- Mask any PII / credentials encountered during searches.
