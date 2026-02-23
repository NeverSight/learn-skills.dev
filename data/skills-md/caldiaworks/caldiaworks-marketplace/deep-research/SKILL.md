---
name: deep-research
description: "Conduct deep research on any topic through structured investigation design. Use when the user needs comprehensive, multi-source analysis -- not a quick lookup. Triggers: deep research, comprehensive analysis, research report, compare X vs Y, analyze trends, investigate, or any request requiring synthesis across multiple perspectives. Do NOT use for simple questions answerable with 1-2 searches or for debugging."
---

# Deep Research

A research skill that thinks before it searches.

The core principle: no search happens until you understand what questions the research must answer and why. This separates genuine research from "search and summarize."

You are the **LeadResearcher** — the orchestrator. Your job is to plan, delegate, synthesize, and verify. Delegate search tasks to **subagents** (worker agents via the Task tool) that operate in parallel, compress their findings, and return them to you. If the Task tool is unavailable in your environment, execute searches directly but still follow the same structured approach — evaluate sources, compress findings, and track evidence criteria satisfaction for each question.

## Process

Four phases, executed in strict order.

### Phase 1: Decompose the Research Question

Receive the user's theme. Before touching any search tool, reason about what this research needs to answer.

Produce a **Research Question Map** and present it as visible output. Every field below is required — do not summarize or omit any.

1. **Core Questions** (3-7 questions)
   For each question, write out all five fields explicitly:
   - **Question**: stated precisely, not a rephrasing of the user's theme
   - **Category**: factual / comparative / causal / evaluative
   - **Commonly known**: what is already well-established about this (not worth researching)
   - **Knowledge gap**: what is genuinely unknown, contested, or where common assumptions may be wrong. For at least one question, frame it as testing a common assumption (e.g., "It is widely assumed that X, but the evidence for this is unclear")
   - **Evidence criteria**: what specific evidence would constitute an adequate answer (e.g., "peer-reviewed meta-analysis", "benchmark data from 2024+", "practitioner survey with N>500")

2. **Question Dependencies**
   State which questions must be answered before others, and explain **why** each dependency exists. Not just "Q1 → Q3" but "Q1 (what is the current adoption rate) must precede Q3 (whether adoption is accelerating) because Q3 requires a baseline from Q1."

**Why this matters:** Without this step, you default to searching the user's theme verbatim, which produces the same shallow results they could get themselves. The decomposition forces you to identify what is actually worth investigating — the gaps between what is commonly known and what the user needs to know.

**How to do this well:** Don't just rephrase the theme as questions. Interrogate it. If the user asks about "YouTube video planning," don't just ask "How do you plan YouTube videos?" — ask what specific aspects of planning are non-obvious, what practitioners disagree about, what has changed recently, what the evidence says about what actually works versus what is merely conventional wisdom.

### Phase 2: Present the Research Plan

Transform the question map into an investigation plan and present it to the user.

The plan must show, **organized per question** (not grouped by wave or batch):

1. **Research Questions** — the questions from Phase 1, ordered by dependency
2. **Investigation Angles** — listed under each question individually, at least 2 distinct angles per question, each specifying:
   - What to look for
   - Why this angle is expected to yield useful information
   - What source domains to prioritize (e.g., "academic papers in peer-reviewed journals", "official government statistics", "practitioner accounts from industry blogs", "developer surveys like State of JS")
3. **Investigation Order** — the sequence of investigation, with reasoning for why this order makes sense (e.g., "Question 3 depends on findings from Question 1")

Present the plan to the user and wait for approval. Do not execute any searches until the user approves.

If the user rejects or modifies the plan, revise it and re-present.

**What makes a good investigation angle:** It's not a search query — it's a line of reasoning about where to find information. "Search for YouTube planning tips" is a search query. "Examine what professional creators with 100K+ subscribers describe as their actual planning process, since practitioner accounts often differ from marketing advice" is an investigation angle.

### Phase 3: Parallel Multi-Agent Exploration

After approval, execute the plan using subagent delegation. This is the orchestrator-worker phase.

**Delegation Protocol:**
For each investigation angle, delegate to a subagent (using the Task tool) with these instructions:
- The specific research question being investigated
- The investigation angle details (what to look for, why, which sources)
- The evidence criteria to satisfy
- Instructions to return compressed findings (see "Subagent Return Format" below)

**Parallel vs. Sequential:**
- Launch subagents in parallel when their research questions have no dependencies
- Execute sequentially when one question's findings inform another's search strategy
- Use multiple Task tool calls in a single response for parallelism

**Subagent Return Format:**
Each subagent must return:
- Key factual claims with quantitative data where available
- Source attribution for each claim (URL, title, retrieval date)
- Assessment of whether the evidence criteria are met
- Any contradictions found between sources
- Unexpected findings that suggest new investigation directions

**Source Evaluation:**
Subagents must filter and compress their findings:
- Assess whether each retrieved source actually addresses the research question; discard irrelevant sources
- Extract substantive content, stripping HTML boilerplate, navigation, advertisements, and cookie notices
- Compress findings to preserve factual claims, quantitative data, and source metadata while minimizing noise

**Follow-Up Exploration:**
After receiving subagent results, evaluate what was found:
- Are the evidence criteria from Phase 1 met?
- Do sources contradict each other? If so, **this must trigger a targeted follow-up search** to investigate the contradiction — do not simply acknowledge it and move on. For example, if Source A claims remote work increases productivity by 13% and Source B claims it decreases by 20%, search specifically for studies that explain the discrepancy (different measurement methods, different populations, different time periods).
- Did you find unexpected information that opens a new line of inquiry?
- Are there gaps where the evidence criteria are not yet satisfied?

For each gap, contradiction, or promising lead: formulate a specific follow-up question and delegate a new subagent to investigate it.

**When to stop:** Cease exploration for a question when either:
- The evidence criteria defined in Phase 1 are satisfied, or
- Two consecutive follow-up searches yield no new relevant information

### Phase 4: Synthesize and Report

Integrate findings into a Markdown report. The report answers the research questions — it does not summarize sources.

**Cross-Reference Verification:**
Before writing the report, verify key claims:
- When a factual claim central to the findings comes from a single source, attempt to verify it against at least one additional independent source
- If verification fails, flag the claim directly in the report text where it appears — for example: "According to [3] (single source; independent verification not found), the latency decreased by 90%." Do not bury single-source warnings in appendices or separate notes; the reader must see the caveat in context

**Contradiction Resolution:**
Compare factual claims across all sources for each research question. Flag instances where sources present conflicting data, conclusions, or recommendations. When contradictions exist, present both sides with the evidence supporting each, and note any explanation for the discrepancy found during follow-up searches.

**Report Structure:**
The report follows the research questions, not the sources. Each major section corresponds to a research question from Phase 1.

```markdown
# [Research Theme]

## Executive Summary
[2-3 paragraphs: key findings and their implications]

## [Research Question 1]
[Synthesized answer drawing from multiple sources]
[Where sources agree, disagree, or complement each other]

## [Research Question 2]
...

## [Research Question N]
...

## Synthesis
[Insights that emerge from connecting findings across questions —
things no single source states but that become apparent when
evidence is considered together]

## Limitations
[What could not be determined and why, what evidence was lacking,
what methodological concerns exist (data staleness, selection bias,
confounding factors), what assumptions were made]

## Bibliography
[1] Source Name. "Title". URL (Retrieved: YYYY-MM-DD)
[2] ...
```

**Writing standards:**
- Every factual claim must cite a specific source: [1], [2], etc. No factual statement may appear without a citation — if you cannot attribute it, either find the source or state it as your interpretation using the phrasing below
- When presenting your own analysis or interpretation (not directly from a source), use explicit phrasing: "This suggests...", "Taken together, these findings indicate...", "Based on the available evidence..."
- Write in prose. Use bullets only for distinct lists (product names, enumerated steps). Default to paragraphs.
- Be precise: "reduced mortality by 23%" not "significantly improved outcomes"
- Each section must integrate information from 2+ sources, not summarize one source at a time

**Bibliography:** Every source cited in the report must appear in the bibliography with: source name, title, URL, and retrieval date. No placeholders, no truncation.

**Output:** Save the report to the `.docs/` directory following project conventions: `.docs/research-YYYY-MM-DD-<topic-slug>.md`. If no project CLAUDE.md specifies an output directory, save to the current working directory.

## Handling Edge Cases

**Ambiguous theme:** If the user's theme is vague, interpret it in Phase 1 and let the user correct in Phase 2 (when they see the plan). Don't ask for clarification before starting — the plan presentation is the clarification mechanism.

**No useful results:** If searches for a question yield nothing useful, state this explicitly in the report rather than padding with tangentially related information.

**Theme too broad:** If decomposition yields more than 7 questions, narrow the scope to the most substantive questions and note what was excluded in the Limitations section.
