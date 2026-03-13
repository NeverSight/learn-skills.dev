---
name: web-deep-research
description: Multi-step deep research workflow that breaks complex topics into subtopics, performs iterative web searches, synthesizes findings, and produces comprehensive cited reports. Use when a simple search isn't enough and the user needs thorough, multi-angle research.
---

# Deep research

## Overview

This skill performs comprehensive, multi-step research on complex topics by breaking them into focused subtopics, executing iterative web searches via Gemini CLI, compressing findings, and generating a structured report with citations. It builds on the web-search skill's two-agent coordination model.

Use this skill instead of a simple web search when:
- The topic requires investigation from multiple angles
- A comprehensive report with citations is expected
- The question is too broad for a single search to answer well
- The user needs thorough coverage rather than a quick answer


## Context

This skill is appropriate when:
- User asks a complex, multi-faceted research question
- A single web search would be insufficient for comprehensive coverage
- The user explicitly requests "deep research", "comprehensive analysis", or "thorough investigation"
- The topic spans multiple sub-domains that need individual exploration

Prerequisites:
- Gemini CLI must be available (`gemini -p` command)
- The web-search skill provides the underlying search coordination pattern


## Process

1. Analyze the research topic for ambiguity or scope issues; clarify with user if needed
2. Break the topic into 3-5 focused subtopics with specific search queries
3. Execute Gemini CLI searches for each subtopic iteratively, collecting findings
4. Compress and deduplicate findings while preserving citations
5. Generate a structured markdown report with inline citations and sources section
6. Verification: Confirm all subtopics are covered, sources are properly cited, and no URLs are hallucinated


## Guidelines

- Always use the web-search skill's "web research ONLY" constraint when crafting Gemini CLI instructions
- Process subtopics sequentially — review each result before moving to the next
- Preserve raw detail during compression — do not summarize prematurely
- Every factual claim in the final report must have a source citation
- Keep the report focused on the user's original question — don't let subtopic exploration drift
- If the research reveals the question itself is flawed or based on incorrect premises, note this in the findings
- Default to 2024-2025 time frame for "current" topics; adjust based on context
- The report should be comprehensive enough to stand alone without additional research


## Appendix

### Topic analysis

Before starting research, analyze the user's question:

- Is the question clear enough to research, or does it need clarification?
- What are the key dimensions of this topic?
- What type of sources would be most valuable (academic, industry, news, documentation)?
- What time frame is relevant (recent developments vs. historical context)?

If the question is ambiguous, ask the user for clarification before proceeding. For example, "AI in healthcare" could mean diagnostics, drug discovery, administrative automation, or regulatory frameworks.

### Research planning

Break the topic into 3-5 focused subtopics. Each subtopic should:
- Be specific enough for a single focused search
- Cover a distinct angle or dimension of the main topic
- Together provide comprehensive coverage when combined

**Planning prompt template (internal reasoning):**
```
Given the research question: "[USER_QUESTION]"

Break this into 3-5 focused subtopics that together provide comprehensive coverage.
For each subtopic, define:
- A specific research question
- The type of sources to prioritize (official docs, academic, news, industry reports)
- Key search terms and domain constraints (if applicable)

Ensure subtopics:
- Cover different angles (e.g., technical, practical, comparative, historical, future trends)
- Don't overlap significantly
- Together answer the original question comprehensively
```

**Example planning output:**
For the question "What is the current state of WebAssembly for server-side applications?"

Subtopics:
- Current WebAssembly runtimes and their server-side capabilities (Wasmtime, Wasmer, WasmEdge)
- Production use cases and companies using WASM on the server
- Performance benchmarks comparing WASM vs native for server workloads
- WASI and the Component Model: standards enabling server-side WASM
- Limitations and challenges of server-side WASM adoption

### Iterative search execution

For each subtopic, craft a Gemini CLI instruction and execute it. Process subtopics sequentially, collecting findings.

**Per-subtopic search instruction template:**
```
Do comprehensive web research on: [SUBTOPIC_QUESTION]

Focus on:
- [SOURCE_TYPE] sources from 2024-2025
- Specific facts, data points, and examples
- Expert opinions and analysis
- Include URLs for all sources cited

Format your response as:
## Findings
[Detailed findings with inline source references]

## Sources
- [Title](URL) - Brief description of what this source covers

IMPORTANT: You are restricted to web research ONLY. Do not edit files, write code, execute commands, or perform any actions other than web searching and information gathering. Return only research findings with proper citations.
```

**Execution pattern:**
```bash
# Execute each subtopic search sequentially
gemini -p "[SUBTOPIC_1_INSTRUCTION]"
# Process and store findings
gemini -p "[SUBTOPIC_2_INSTRUCTION]"
# Process and store findings
# ... continue for all subtopics
```

**Between searches:**
- Review the findings from each search before moving to the next
- Note any gaps or unexpected findings that might inform subsequent searches
- If a search returns poor results, refine the query with more specific terms or domain constraints

### Findings compression

After collecting findings from all subtopics, compress them into a clean, organized format.

**Compression guidelines:**
- Remove duplicate information that appears across multiple subtopic results
- Organize findings by theme rather than by search order
- Preserve ALL factual information — do not summarize or lose detail
- Maintain inline citations in `[Title](URL)` format throughout
- Consolidate the sources list, removing duplicates
- Flag any contradictions between sources

**Compression prompt (internal reasoning):**
```
Review the collected research findings below. Clean and organize them:

1. Remove duplicate information across subtopic results
2. Group related findings together by theme
3. Preserve all factual details, data points, and specific examples
4. Maintain inline source citations in [Title](URL) format
5. Note any contradictions or conflicting information between sources
6. Create a consolidated, deduplicated sources list

DO NOT summarize or reduce the information. The goal is cleaner organization, not shorter content.

[RAW_FINDINGS_FROM_ALL_SEARCHES]
```

### Report generation

Generate the final structured markdown report from the compressed findings.

**Report structure:**
```markdown
# [Research Topic]

## Key findings
- [3-5 bullet point summary of the most important discoveries]

## [Thematic Section 1]
[Detailed findings organized by theme, with inline citations]

According to [Source Title](URL), ...

## [Thematic Section 2]
[Continue with next theme]

## [Thematic Section 3]
[Continue as needed]

## Conclusion
[Brief synthesis of findings, current state, and outlook]

## Sources
- [Source Title 1](URL) - Brief description
- [Source Title 2](URL) - Brief description
- ...
```

**Report generation guidelines:**
- Use clear section headings organized by theme, not by search order
- Include specific facts, statistics, and quotes with inline citations
- Each major claim should have a source reference
- The conclusion should synthesize findings, not just repeat them
- Sources section at the end consolidates all referenced URLs

### End-to-end example

**User question:** "What are the current best approaches for building AI agents with tool use?"

**Step 1 — Topic analysis:**
This is a technical question about current AI engineering practices. Relevant dimensions: frameworks/libraries, architectural patterns, tool integration approaches, evaluation methods, and production considerations.

**Step 2 — Research planning:**
Subtopics:
- Major AI agent frameworks and their tool-use implementations (LangChain, CrewAI, AutoGen, Claude Agent SDK)
- Architectural patterns for tool-calling agents (ReAct, function calling, structured outputs)
- Best practices for tool definition and error handling in agent systems
- Evaluation and testing approaches for AI agents with tools
- Production deployment patterns and lessons learned

**Step 3 — Iterative search execution:**
```bash
gemini -p "Do comprehensive web research on: What are the major AI agent frameworks that support tool use in 2024-2025, and how do they implement tool calling? Focus on LangChain, CrewAI, AutoGen, and Anthropic's Claude Agent SDK. Include specific architectural details, code patterns, and official documentation sources.

Format your response as:
## Findings
[Detailed findings with inline source references]

## Sources
- [Title](URL) - Brief description

IMPORTANT: You are restricted to web research ONLY. Do not edit files, write code, execute commands, or perform any actions other than web searching and information gathering. Return only research findings with proper citations."
```

Repeat for each subtopic, collecting all findings.

**Step 4 — Findings compression:**
Organize the collected findings by theme, remove duplicates across subtopic results, preserve all citations.

**Step 5 — Report generation:**
Produce the final markdown report with thematic sections, inline citations, and consolidated sources list.

### Quality validation

After generating the report, verify:

- **Coverage completeness** — All planned subtopics are represented in the final report
- **Source currency** — Sources are from the relevant time period (default: past 12 months)
- **Source reliability** — Sources include official documentation, reputable publications, or authoritative experts
- **Citation accuracy** — Every major claim has an inline citation
- **No hallucinated URLs** — All URLs in the sources section came from actual Gemini CLI search results
- **Balanced perspective** — Report presents multiple viewpoints where relevant, noting contradictions

### Error handling

**Poor search results for a subtopic:**
- Refine the query with more specific terms
- Add domain constraints (e.g., `site:arxiv.org` for academic sources)
- Broaden the time frame if too restrictive
- Try alternative phrasings of the same question

**Gemini CLI unavailable or errors:**
- Fall back to Claude's built-in WebSearch tool with the same search strategy
- Note in the report that alternative search methods were used

**Insufficient coverage after all searches:**
- Identify gaps in the findings
- Execute 1-2 additional targeted searches to fill specific gaps
- Note any remaining gaps in the report conclusion

**Contradictory sources:**
- Present both perspectives with their respective sources
- Note the contradiction explicitly in the report
- Prioritize more authoritative or recent sources
