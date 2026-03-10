---
name: deep-research
description: Researches a topic using parallel web search agents, then creates or updates a structured markdown playbook with sourced practitioner insights. Auto-invoke when user says "deep research", "research playbook", "create a playbook about", "update playbook", or asks to deeply research a topic and write findings into a document. Do NOT invoke for simple web searches, quick questions, or general research that does not produce a persistent playbook file.
user-invocable: true
argument-hint: "<topic> [--file path.md]"
allowed-tools: Agent, WebSearch, WebFetch, Read, Edit, Write, Glob, Grep, AskUserQuestion
license: MIT
---

# Deep Research Skill

Research the latest practitioner insights, official docs, and community discussion on a topic, then create or update a playbook.

## Step 0: Parse Arguments

The user's input is: `$ARGUMENTS`

**If no arguments**: Display this help and stop:
```
Usage:
  /deep-research swift concurrency
  /deep-research kubernetes cost optimization --file infra-playbook.md
  /deep-research --file existing-playbook.md   (updates all sections)
Playbook is created in your current working directory by default.
```

**Parsing rules** — MUST follow this order:

1. If `$ARGUMENTS` contains `--file <path>`, extract that as the file path. Everything else is the topic.
2. Else if a token ends in `.md` or contains `/`, treat it as the file path. Everything else is the topic.
3. Else treat ALL of `$ARGUMENTS` as the topic. Auto-generate the file path: `<topic-slug>.md` in the current working directory (e.g., "swift concurrency" → `swift-concurrency.md`).

Examples:
- `/deep-research swift concurrency` → topic: "swift concurrency", file: `swift-concurrency.md`
- `/deep-research kubernetes cost optimization --file infra-playbook.md` → topic: "kubernetes cost optimization", file: `infra-playbook.md`
- `/deep-research --file docs/playbook.md` → topic: inferred from existing file, file: `docs/playbook.md`
- `/deep-research docs/react-hooks.md state management` → topic: "state management", file: `docs/react-hooks.md`

## Step 0.5: Clarify Assumptions

Before proceeding, use **AskUserQuestion** if any of these apply:

- **Ambiguous topic**: The topic has multiple common meanings (e.g., "swift", "python", "spring", "agent", "mercury"). Ask which one.
- **Overly broad topic**: The topic is too wide to research well without focus (e.g., "machine learning", "AI safety"). Ask what aspect or audience matters.
- **Missing context that changes results**: The topic implies a specific context the user hasn't stated (e.g., cloud provider, programming language, audience level).
- **Update mode without topic**: If inferring the research focus from an existing file, confirm the inferred focus before launching agents.

Skip this step if the topic is specific and unambiguous.

## Step 1: Read or Create Playbook

**If the target file exists**:
- Read it. Check if it looks like a playbook (has a Sources section or `*Captured:*` date).
- If yes: note all section headings, Sources list, and voice/style. Set `mode = update`.
- If no: warn user — "This file exists but doesn't look like a playbook. Update it anyway, or create a new file?"

**If the target file does not exist**:
- If no topic was given, stop: "New playbook needs a topic. Usage: `/deep-research <topic>`"
- If the parent directory does not exist, create it.
- Set `mode = create`. The research agents will discover the structure.

Tell the user: "Creating playbook at `<absolute path>`" or "Updating playbook at `<absolute path>`".

## Step 2: Determine Research Scope

### `mode = update` (existing playbook):

Identify the playbook's **subject** from its title and section headings.

**With topic**: Launch 2-3 agents researching the topic within the playbook's subject domain. Each agent MUST search from a different angle:
1. Official docs and authoritative sources
2. Community discussion and practitioner blogs
3. (Optional) Social media and recent reports

**Without topic**: Group the existing section headings into 3-5 research themes. Launch one agent per theme, looking for updates since the playbook's `*Captured:*` date.

### `mode = create` (new playbook):

The topic IS the subject. Launch 3-5 agents, each covering a different facet:
1. Core concepts and official documentation
2. Best practices and common patterns
3. Gotchas, pitfalls, and troubleshooting
4. Tools, libraries, and ecosystem
5. (Optional) Advanced techniques and emerging trends

Adapt facets to fit the topic — not every topic needs all five.

## Step 3: Launch Research Agents

Before launching, tell the user:
```
Launching [N] research agents in parallel:
  1. [Agent 1 angle]
  2. [Agent 2 angle]
  ...
```

Use the **Agent tool** to launch agents in parallel. Each agent MUST use `subagent_type: general-purpose` and `run_in_background: false`.

**Constructing the prompt for each agent** — MUST include:

1. **The subject and specific angle** this agent covers (e.g., "best practices for Swift async/await" or "Claude Code opus 4.7 official docs")
2. **Context from the playbook**:
   - `mode = update`: list existing section headings so the agent skips what's already covered
   - `mode = create`: tell the agent this is a new playbook — return all findings
3. **Search instructions**: Tell the agent to use WebSearch with queries derived from the subject and topic. Pattern:
   - `"[subject] [topic] [current year]"` (general web)
   - `"[subject] [topic]"` on authoritative domains for that subject
   - `"[subject] [topic] blog [current year]"` (practitioner blogs)
   - Then WebFetch promising URLs to extract details
4. **Output format**: For each finding, return:
   - **Insight**: The specific, actionable finding (1-2 sentences)
   - **Source URL**: Direct link
   - **Suggested section**: Which section this belongs in (exact name for update mode, proposed name for create mode)
   - **Confidence**: High (official docs/multiple sources) or Medium (single practitioner report)
5. **Rules**: MUST only return findings with real source URLs. NEVER return findings without sources. Focus on practitioner insights (what people actually do), not marketing. Prefer concrete techniques, numbers, and gotchas over general advice.

If an agent returns no results, try broader search terms without the year qualifier before giving up.

## Step 4: Integrate Findings

### If `mode = update` (existing playbook):

For each research agent's results:

1. **Filter**: Drop anything without a source URL or that duplicates existing content
2. **Locate**: Find the exact section in the playbook where each finding belongs
3. **Edit**: Use the Edit tool to merge the finding into the existing section
   - MUST match the playbook's existing voice — read a few paragraphs to internalize the style before writing. Tone contrast:
     - BAD: "It is generally recommended to consider implementing caching for improved performance."
     - GOOD: "Cache aggressively. Redis for shared state, in-memory for hot paths. Profile first."
   - Format: `[Insight text]. — [Source Name](URL)` (space-emdash-space before source)
   - Add to existing paragraphs, tables, or bullet lists — NEVER create a new subsection unless the content covers a topic not addressed anywhere in the existing section AND requires more than 3 bullet points
4. **Source list**: Add any new source URLs to the Sources list at the bottom

**Integration rules**:
- NEVER create a separate "New Findings" or "Updates" section — merge into existing structure
- NEVER add a claim without a source URL
- NEVER change the voice — match whatever style the playbook already uses
- If a finding contradicts existing content and has High confidence, update the existing content — keep the old source alongside the new one so the reader can see the evolution
- If a finding contradicts existing content but only has Medium confidence, add it as an alternative perspective rather than replacing
- ALWAYS preserve existing content unless explicitly superseded by a High-confidence source

### If `mode = create` (new playbook):

1. **Filter**: Drop anything without a source URL
2. **Group**: Cluster findings by theme into logical sections (aim for 5-10 sections)
3. **Write**: Use the Write tool to create the file. Structure:
   ```markdown
   # [Title derived from topic]

   [Sections — group related insights under clear headings]

   ---
   ## Sources

   [All source URLs from research]

   ---
   *Captured: YYYY-MM-DD*
   ```
   For each section:
   - Write a tight summary paragraph synthesizing the findings, then bullet the key insights
   - Every claim MUST have a source: `[Insight]. — [Source Name](URL)`
   - Voice: direct, concise, practitioner-focused — no filler, no hedging
4. **Source list**: Collect all source URLs into the Sources section at the bottom

If all findings were filtered out, tell the user: "No sourced findings were found for this topic. Try a broader or more specific topic."

## Step 5: Verify and Report

After all edits:

1. Read the playbook to verify:
   - Every new claim has a source URL
   - No duplicate entries
   - Sections read cohesively (new content doesn't feel bolted on)
   - The Sources list includes all URLs

2. Report to the user:
   ```
   ## Playbook [Created | Updated]

   **File**: [absolute file path]
   **Mode**: [create | update]
   **Topic**: [what was researched]
   **Agents launched**: [N]

   ### Sections [created | modified]:
   - **Section Name** — [brief description of content]
   - ...

   ### Sources: [count]
   ### Findings integrated: [count]
   ### Findings dropped (no source / duplicate): [count]
   ```
