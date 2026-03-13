---
name: agentic-research
description: Shared team playbook for multi-agent deep research operations. Defines communication protocols, source quality tiers, parallel safety rules, output formatting standards, and error handling conventions used by all agents (orchestrator, ExaAI specialist, Firecrawl specialist, NotebookLM specialist) in the agentic research system.
metadata:
  clawdbot:
    emoji: "📋"
    requires:
      skills:
        - exa
        - firecrawl
        - notebooklm
        - agentic-research-orchestration
---

# Agentic Research — Shared Team Playbook

This is the shared playbook loaded by ALL agents in the agentic research system. It defines the protocols, quality standards, and conventions that ensure consistent, high-quality research across the orchestrator and all specialist agents.

**Every agent MUST read and follow this playbook before beginning work.**

## Team Structure

| Agent | Role | Key Tools |
|-------|------|-----------|
| **Orchestrator** | Coordinates workflow, relays URLs, synthesizes report | TeamCreate, SendMessage, Task |
| **ExaAI Specialist** | Semantic web search, source discovery | mcp__exa__web_search_exa |
| **Firecrawl Specialist** | Web scraping, site crawling, vector DB | firecrawl CLI, Qdrant |
| **NotebookLM Specialist** | AI-powered analysis, artifact generation | notebooklm CLI |

## Communication Protocol

### Message Format

All inter-agent messages MUST use this structure:

```
## [Agent Name] [Message Type] (Batch N)

### [Section 1 Header]
- Item 1
- Item 2

### [Section 2 Header]
- Item 1

### Summary
Brief summary of key points.
```

### Message Types

| Type | When | From | To |
|------|------|------|----|
| **URL Report** | Every 3-5 operations | Specialists | Orchestrator |
| **Progress Update** | Every 5-10 operations | Specialists | Orchestrator |
| **Crawl Request** | When docs site discovered | Orchestrator | Firecrawl |
| **Source Relay** | When high-quality URLs received | Orchestrator | NotebookLM |
| **Completion Signal** | When all work done | Specialists | Orchestrator |
| **Error Escalation** | When blocked | Any agent | Orchestrator |

### URL Report Format (Specialists -> Orchestrator)

```
## [Agent] URL Report (Batch N)

### Key URLs Discovered:
- https://url1.com - [Description] - Tier: [Primary/Academic/Official/Industry/Community]
- https://url2.com - [Description] - Tier: [tier]

### Documentation Sites (recommend for Firecrawl):
- https://docs.example.com - Full documentation for X

### Key Findings:
- Finding 1
- Finding 2
```

### Source Relay Format (Orchestrator -> NotebookLM)

```
Add these N sources to the notebook:
- https://url1.com — [Description] — Tier: Primary
- https://url2.com — [Description] — Tier: Academic
```

### Completion Signal Format

```
[Agent] specialist complete. Findings written to findings/[agent]-findings.md.
[Key stats: searches, URLs, pages, etc.]
Key gaps: [list gaps].
```

## Source Quality Tiers

All agents MUST classify discovered sources using these tiers. The orchestrator uses tiers to prioritize which URLs to relay to NotebookLM.

| Tier | Description | Priority | Examples |
|------|-------------|----------|----------|
| **Primary** | Original research, official announcements, creator content | Highest | Blog posts by framework creators, official release notes, original research papers |
| **Academic** | Peer-reviewed papers, university research, conference proceedings | High | arXiv papers, ACM/IEEE publications, NeurIPS/ICML proceedings |
| **Official** | Official documentation, guides, tutorials from project maintainers | High | docs.langchain.com, readthedocs sites, official GitHub READMEs |
| **Industry** | Analysis from recognized industry analysts, reputable tech publications | Medium | Hacker News (top posts), reputable tech blogs, benchmark reports |
| **Community** | Forum discussions, personal blogs, Stack Overflow, Reddit | Lower | Reddit threads, personal dev blogs, community wikis |
| **News** | News articles, press releases, general media coverage | Lowest | TechCrunch, The Verge, general news sites |

### Tier Prioritization Rules

1. **Primary + Academic**: Always relay to NotebookLM
2. **Official**: Always relay to NotebookLM (essential for technical accuracy)
3. **Industry**: Relay if relevant to key questions and not redundant
4. **Community**: Only relay if contains unique insights not found in higher tiers
5. **News**: Rarely relay -- only if contains exclusive information

### Source Limit Management

- **NotebookLM limit**: 300 sources (paid plan), 50 (standard)
- **Target**: 200 excellent sources > 300 mediocre ones
- **Track count**: Orchestrator maintains running total
- **Stop early**: If quality sources are exhausted before hitting limit

See [references/source-quality-tiers.md](references/source-quality-tiers.md) for detailed tier classification examples.

## Parallel Safety Rules

### NotebookLM Commands

**CRITICAL: ALL agents MUST follow these rules.**

- **ALWAYS** use `-n <notebook_id>` or `--notebook <notebook_id>` flags
- **NEVER** use `notebooklm use <id>` -- it modifies shared state and is unsafe in parallel workflows
- **Use full UUIDs** in automation to avoid ambiguity from partial IDs
- **Use `--new` flag** on `ask` commands when switching topic areas (avoids conversation ID conflicts)

### File System Safety

- Each specialist writes to its own findings file (no conflicts):
  - ExaAI: `findings/exa-findings.md`
  - Firecrawl: `findings/firecrawl-findings.md`
  - NotebookLM: `findings/notebooklm-findings.md`
- Only the orchestrator writes to `report.md` and `sources/sources.md`
- Artifacts are downloaded to `artifacts/` (NotebookLM specialist only)

### Team Communication Safety

- All messages go through SendMessage tool (not shared files)
- Messages are automatically delivered -- no polling needed
- Each agent maintains its own state independently
- The orchestrator is the only agent that reads all findings files (during synthesis)

## Output Formatting Standards

### Findings Files

All specialist findings files MUST include:

1. **Research Topic** -- exact topic from brief
2. **Methodology Summary** -- what was done, key stats
3. **Key Findings** -- organized by topic area, with inline source URLs
4. **Contradictions** -- where sources disagree (do NOT smooth over)
5. **Gaps** -- what couldn't be found or needs more investigation

### Source Citation Format

Inline citations use markdown links:

```markdown
According to the official documentation [Source Title](https://url), the framework supports...
```

When citing multiple sources:

```markdown
Multiple sources confirm this approach [Source A](url1), [Source B](url2), though [Source C](url3) disagrees.
```

### URL Reporting Format

When reporting URLs, always include:
- Full URL (no shortlinks)
- Brief description (what the page contains)
- Quality tier classification

```
- https://docs.example.com/guide - Comprehensive setup guide - Tier: Official
```

## Error Handling Protocol

### Severity Levels

| Level | Action | Examples |
|-------|--------|----------|
| **Warning** | Log and continue | Rate limit on one site, single source fails to load |
| **Error** | Report to orchestrator, attempt workaround | Auth failure, major site blocked, tool crash |
| **Critical** | Report to orchestrator immediately, stop work | All tools failing, auth completely broken |

### Error Reporting Format

```
## Error Report

**Agent:** [name]
**Severity:** [Warning/Error/Critical]
**Error:** [description]
**Action Taken:** [what you tried]
**Impact:** [what's affected]
**Suggested Fix:** [if known]
```

### Recovery Strategies

1. **Rate limits**: Exponential backoff (30s -> 2min -> skip)
2. **Auth failures**: Run diagnostic commands, report to orchestrator
3. **Tool crashes**: Retry once, then report
4. **Network issues**: Wait 1 minute, retry, then report
5. **Source not found**: Log, skip, continue with other sources

## Persistent Memory Conventions

All agents write session learnings to `~/.claude/memory/`:

| Agent | Memory File |
|-------|-------------|
| Orchestrator | `~/.claude/memory/agentic-orchestrator.md` |
| ExaAI | `~/.claude/memory/exa-specialist.md` |
| Firecrawl | `~/.claude/memory/firecrawl-specialist.md` |
| NotebookLM | `~/.claude/memory/notebooklm-specialist.md` |

### Memory Entry Format

```markdown
## Session: YYYY-MM-DD -- <topic-slug>

**What worked:**
- [insight 1]
- [insight 2]

**What didn't work:**
- [issue 1]

**Lessons learned:**
- [lesson 1]
```

### Memory Usage

- **Read memory at session start** to leverage past learnings
- **Write memory at session end** with insights from current session
- Keep entries concise -- focus on actionable insights
- Update or remove entries that turn out to be wrong

## Cross-References

This playbook is used by:
- **Orchestrator agent**: `agents/agentic-orchestrator.md`
- **ExaAI specialist agent**: `agents/exa-specialist.md`
- **Firecrawl specialist agent**: `agents/firecrawl-specialist.md`
- **NotebookLM specialist agent**: `agents/notebooklm-specialist.md`

Related skills:
- **Orchestration methodology**: `skills/agentic-research-orchestration/SKILL.md`
- **ExaAI search**: `skills/exa/SKILL.md`
- **Firecrawl web scraping**: `skills/firecrawl/SKILL.md`
- **NotebookLM automation**: `skills/notebooklm/SKILL.md`
