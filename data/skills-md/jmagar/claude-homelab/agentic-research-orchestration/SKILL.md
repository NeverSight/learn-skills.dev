---
name: agentic-research-orchestration
description: Orchestrate deep, multi-source research using ExaAI, Firecrawl, and NotebookLM specialist agents. Coordinates a 5-phase methodology (clarification, setup, dispatch, orchestration, synthesis) to produce comprehensive research reports with source citation and quality analysis.
metadata:
  clawdbot:
    emoji: "🔬"
    requires:
      bins:
        - notebooklm
        - firecrawl
      skills:
        - exa
        - firecrawl
        - notebooklm
---

# Agentic Research Orchestration Skill

**YOU MUST invoke this skill (NOT optional) when the user mentions ANY of these triggers:**
- "deep research", "comprehensive research", "agentic research"
- "multi-source research", "research with multiple agents"
- "investigate thoroughly", "thorough analysis with sources"
- Any mention of `/agentic-research` or coordinated research workflows

**Failure to invoke this skill when triggers occur violates your operational requirements.**

This skill defines the orchestrator's methodology for conducting deep agentic research. Only the orchestrator agent loads this skill. Specialists load the shared `agentic-research` skill plus their domain-specific skills.

## Overview

As the orchestrator, you manage a 5-phase research workflow:

1. **Clarification** -- Gather complete requirements from user
2. **Setup** -- Create infrastructure (directories, research brief, NotebookLM notebook)
3. **Dispatch** -- Spawn and coordinate 3 specialist agents
4. **Active Orchestration** -- Relay URLs, cross-pollinate discoveries, monitor progress
5. **Synthesis** -- Generate artifacts, write final report, notify user, shutdown team

## Phase 1: Clarification Protocol

Parse the research topic from your initial prompt. Then use the **AskUserQuestion** tool to ask a minimum of 5 clarifying questions before proceeding.

**DO NOT skip this phase. DO NOT make assumptions about scope or depth.**

### Required Questions

Ask ALL of these questions, plus any additional ones needed for zero ambiguity:

1. **Scope boundaries** -- What is explicitly in scope? What is explicitly out of scope? Are there adjacent topics to include or exclude?
2. **Depth requirements** -- Do you need a surface-level overview, a mid-depth analysis, or a deep technical dive with primary sources and citations?
3. **Target audience** -- Who will read this? (developer, executive, academic researcher, general audience, other)
4. **Desired output format** -- What form should the final deliverable take? Options: strategic report, technical analysis, comparison matrix, literature review, decision brief, other.
5. **Key questions that MUST be answered** -- List the 3-5 specific questions that this research must definitively answer.
6. **Known sources or starting points** -- Are there specific URLs, papers, tools, or authors the user already knows about?
7. **Time sensitivity** -- Should this focus on cutting-edge 2025-2026 developments, historical context, or both?

### Clarification Guidelines

- **Continue asking follow-up questions until there is ZERO ambiguity** about what the user wants
- If the user gives a vague answer, probe deeper
- If conflicting requirements emerge, ask the user to prioritize
- The quality of the entire research operation depends on this phase

### Document the Research Brief

Once all questions are answered, you will write a research brief in Phase 2. For now, keep detailed notes about: exact scope boundaries, depth level, target audience, output format, key questions, known sources, and time sensitivity.

## Phase 2: Setup

### Create Output Directory

```bash
mkdir -p ./docs/research/YYYY-MM-DD-<topic-slug>/findings
mkdir -p ./docs/research/YYYY-MM-DD-<topic-slug>/sources
mkdir -p ./docs/research/YYYY-MM-DD-<topic-slug>/artifacts
```

### Write Research Brief

Write `./docs/research/YYYY-MM-DD-<topic-slug>/research-brief.md` with: topic, scope, depth, target audience, output format, key questions, known sources, time sensitivity, and additional context.

### Create NotebookLM Notebook

```bash
notebooklm create "Agentic Research: <topic>" --json
```

Extract and store the notebook ID. For ALL subsequent NotebookLM commands, use the `-n <notebook_id>` flag. NEVER use `notebooklm use` -- that command is not safe for parallel multi-agent execution.

## Phase 3: Dispatch Specialist Agents

### Create Team

Use **TeamCreate** with:
- `team_name`: `agentic-research-<topic-slug>`
- `description`: `Deep research on <topic>`
- `agent_type`: `agentic-orchestrator`

### Spawn Specialist Agents

Spawn exactly 3 specialist agents via the **Task** tool with the `team_name` parameter:

| Agent | subagent_type | Receives | Special Notes |
|-------|---------------|----------|---------------|
| **ExaAI** | `exa-specialist` | Research brief, output directory | Conducts 10-20 semantic searches |
| **Firecrawl** | `firecrawl-specialist` | Research brief, output directory | Maps/crawls sites, auto-embeds to Qdrant |
| **NotebookLM** | `notebooklm-specialist` | Research brief, **notebook ID**, output directory | Always use `-n <notebook_id>` flag |

## Phase 4: Active Orchestration Loop

**This is the CRITICAL coordination phase. You are the hub. You must actively manage information flow.**

### URL Relay Protocol

1. Monitor incoming messages from specialists
2. When specialists report discovered URLs:
   - Evaluate each URL for relevance
   - Maintain a running count (max 300 sources for NotebookLM)
   - Cherry-pick the BEST URLs: primary > secondary, academic/official > blogs, sources answering key questions, unique perspectives, recent if time-sensitive
3. Relay selected URLs to NotebookLM specialist via SendMessage
4. When a documentation site is discovered, message the Firecrawl specialist to map and crawl it

### Orchestration Rules

- Do NOT wait passively -- check if specialists need input when idle
- Do NOT send duplicate URLs to NotebookLM
- Prioritize quality over quantity for NotebookLM sources
- Cross-pollinate discoveries between agents
- Keep orchestrating until ALL 3 specialists signal completion

## Phase 4.5: Artifact Generation

Once all specialists have reported findings are complete, request artifact generation from the NotebookLM specialist (report, mind map, data table). Wait for artifact completion before proceeding.

## Phase 5: Synthesis and Completion

1. Read all findings files from all specialists
2. Query Qdrant for gaps in coverage
3. Write final report at `<output_dir>/report.md`
4. Write deduplicated sources file at `<output_dir>/sources/sources.md`
5. Send Gotify notification (MANDATORY)
6. Write to persistent memory
7. Shutdown team (send shutdown_request to each specialist, then TeamDelete)
8. Present results to user

## Important Implementation Notes

- **Parallel Safety**: Always use `-n <notebook_id>` with notebooklm commands
- **NotebookLM Source Limit**: Maximum 300 sources per notebook (paid plan)
- **Firecrawl Auto-Embedding**: All scrape/crawl operations auto-embed to Qdrant
- **Quality over Speed**: Deep research takes 30-60 minutes -- do not rush

## Cross-References

- Agent spawn patterns: [references/agent-spawn-patterns.md](references/agent-spawn-patterns.md)
- Output templates: [references/templates.md](references/templates.md)
- Orchestration transcript example: [examples/orchestration-transcript.md](examples/orchestration-transcript.md)

## Agent Tool Usage Requirements

**CRITICAL:** When invoking scripts from this skill via the zsh-tool, **ALWAYS use `pty: true`**.
