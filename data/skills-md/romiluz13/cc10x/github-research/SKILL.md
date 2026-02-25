---
name: github-research
description: "Internal skill. Use cc10x-router for all development tasks."
allowed-tools: WebFetch, WebSearch, AskUserQuestion, mcp__octocode__githubSearchCode, mcp__octocode__githubSearchRepositories, mcp__octocode__githubViewRepoStructure, mcp__octocode__githubGetFileContent, mcp__octocode__githubSearchPullRequests, mcp__octocode__packageSearch, mcp__brightdata__search_engine, mcp__brightdata__scrape_as_markdown, mcp__context7__resolve-library-id, mcp__context7__query-docs, Read, Write, Edit, Bash
---

# External Code Research

## Overview

Research external patterns, documentation, and best practices from GitHub and library docs when AI knowledge is insufficient. Use Octocode MCP for GitHub research, Context7 MCP for library documentation, with WebFetch as final fallback.

**Core principle:** Research BEFORE building, not during. External research enhances planning, not execution.

**This skill is ONLY for external research.** Local codebase search is handled by other cc10x tools (Grep/Glob/Read).

## The Iron Law

```
NO EXTERNAL RESEARCH WITHOUT CLEAR AI KNOWLEDGE GAP OR EXPLICIT USER REQUEST
```

If AI training knowledge covers the technology well, skip external research - UNLESS user explicitly asks. This skill is for NEW technologies, complex integrations, unfamiliar APIs, and explicit user requests.

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "I already know this" | Check if post-2024. API may have changed. |
| "Research takes too long" | 30s research prevents 2hr debugging. |
| "Docs are enough" | GitHub shows real implementations, not ideal cases. |
| "I'll research if stuck" | Research BEFORE is faster than research DURING. |
| "Not worth the tokens" | One good pattern saves 10 bad attempts. |

## When to Use

**ALWAYS invoke when:**
- User explicitly requests research ("research X", "how do others", "best practices", "find on github", "use octocode")
- Technology released after 2024 (AI knowledge cutoff)
- Complex integration patterns (auth, payments, real-time)
- Local debugging failed 3+ times with external service errors

**NEVER invoke when:**
- User says "quick" or "simple"
- Standard patterns AI knows well (CRUD, REST, React basics)
- Code review or refactoring tasks
- Technology released before 2024 (unless user explicitly asks)

**The rule:** Trust octocode for HOW. This skill only decides WHEN.

## User Confirmation Gate (REQUIRED)

**BEFORE any research, ask the user:**

```
AskUserQuestion({
  questions: [{
    question: "Do you want me to research GitHub and web for this task?",
    header: "Research?",
    options: [
      { label: "Yes, research", description: "Search GitHub code + web docs (~30s)" },
      { label: "No, skip", description: "Proceed with AI knowledge only" }
    ],
    multiSelect: false
  }]
})
```

**Gate Logic:**
- User says "Yes" → Proceed to Phase 1 (Parallel Search)
- User says "No" → STOP. Return control to calling agent with: "Research skipped by user."

**Bypass Conditions (Skip gate, auto-research):**
- User already said "research" in original request
- User said "yes" to research in previous turn
- Debug workflow with 3+ failed attempts (urgent)

**Why this gate:** Prevents unwanted research delays. User controls when external calls happen.

## Availability Check (REQUIRED)

**Before using Octocode tools, verify availability:**

```
# Try a simple package lookup to test MCP availability
mcp__octocode__packageSearch(name="express", ecosystem="npm")
```

**If Octocode unavailable → Fall back to Context7 MCP**
**If Context7 unavailable → Fall back to WebFetch**

## Research Process

### Phase 1: Parallel Search Execution

**After user confirms (gate passed), execute parallel search:**

```
# SAME MESSAGE - parallel execution
mcp__octocode__packageSearch(name="{library}", ecosystem="npm")
mcp__brightdata__search_engine(query="{library} best practices tutorial", engine="google")
```

**If one source fails, continue with the other. Only fall to Tier 2 if BOTH fail.**

### Phase 2: Let Octocode Guide the Research

**Trust octocode's embedded guidance.** It will:
- Select the right tools and order
- Optimize queries for token efficiency
- Handle pagination and error recovery

**Your job:** Provide clear research goals in the tool parameters:
- `mainResearchGoal`: The overall question you're trying to answer
- `researchGoal`: What this specific query seeks to find
- `reasoning`: Why this query helps answer the main goal

### Phase 3: Summarize for cc10x Memory

Extract only what's needed for the task at hand:
- Key patterns/approaches found
- Gotchas or warnings discovered
- Specific code snippets (minimal)
- Links for future reference

**DO NOT dump entire files - summarize and cite.**

## Research Chain (3-Tier with Parallel Search)

### Tier 1: Parallel Search (PRIMARY)

**Run Octocode + Bright Data in SAME MESSAGE (parallel execution):**

```
# In same message block - both execute in parallel
mcp__octocode__packageSearch(name="{library}", ecosystem="npm")
mcp__brightdata__search_engine(query="{library} tutorial best practices 2024", engine="google")
```

**Why parallel:** Different strengths complement each other:
| Source | Strength | Best For |
|--------|----------|----------|
| Octocode | Real code, PRs, implementations | "How do others implement X?" |
| Bright Data | Official docs, tutorials, blogs | "What are the gotchas?" |

**Merge Strategy:** Use Octocode for code patterns, Bright Data for context/warnings.

### Tier 1.5: Context7 Library Docs

**When to use:** Octocode unavailable, or need quick library API reference.

```
# Step 1: Resolve the library ID
mcp__context7__resolve-library-id(libraryName="{library}")

# Step 2: Query docs with specific topic
mcp__context7__query-docs(context7CompatibleLibraryID="{resolved_id}", topic="{specific API or feature}")
```

**Best for:**
- Library API reference and usage examples
- Framework-specific patterns and configuration
- Quick answers without full GitHub exploration

**Falls to Tier 2 when:** Context7 MCP unavailable or library not indexed.

### Tier 2: Native Claude Code (FALLBACK)

**If Tier 1 AND Tier 1.5 fail (MCPs unavailable):**

```
# Native Claude Code tools - always available
WebSearch(query="{library} best practices")
WebFetch(url="https://docs.{library}.com/getting-started", prompt="Extract key setup steps")
```

**When to use:**
- Octocode MCP unavailable
- Bright Data MCP unavailable
- Both Tier 1 sources return empty results

### Tier 3: Ask User for Context (FINAL FALLBACK)

**If Tier 1 AND Tier 2 fail:**

```
AskUserQuestion({
  questions: [{
    question: "Research sources unavailable. Can you provide documentation or context?",
    header: "Need help",
    options: [
      { label: "I'll paste docs", description: "I have documentation to share" },
      { label: "Try specific URL", description: "I have a URL you can fetch" },
      { label: "Skip research", description: "Proceed without external context" }
    ],
    multiSelect: false
  }]
})
```

**Why this fallback:** Graceful degradation. Never fail silently - always give user options.

### Tier Progression Logic

```
START
  │
  ├─→ Tier 1: Parallel (Octocode + Bright Data)
  │     ├─ Both succeed → Merge results, DONE
  │     ├─ One succeeds → Use that result, DONE
  │     └─ Both fail → Fall to Tier 1.5
  │
  ├─→ Tier 1.5: Context7 Library Docs
  │     ├─ Success → Use result, DONE
  │     └─ Fail → Fall to Tier 2
  │
  ├─→ Tier 2: Native (WebSearch + WebFetch)
  │     ├─ Success → Use result, DONE
  │     └─ Fail → Fall to Tier 3
  │
  └─→ Tier 3: Ask User
        ├─ User provides context → Use that, DONE
        └─ User says skip → Return "No research available"
```

**NO LOCAL SEARCH** - This skill is for external research only. Local codebase search uses Grep/Glob/Read directly.

## Incremental Checkpoints (During Research)

**Trigger:** If research involves 5+ octocode tool calls, checkpoint progress incrementally.

**Why:** Long research can fill context before reaching "Save Research" section. Incremental saves prevent total loss.

### Checkpoint Triggers (ANY of these)

| Trigger | Action |
|---------|--------|
| 5+ tool calls completed | Save current findings |
| Significant discovery | Save immediately |
| Switching research direction | Save before pivoting |
| 10+ minutes of research | Save progress |

### Checkpoint Format (Quick Save)

```
# In docs/research/YYYY-MM-DD-<topic>-research.md (append mode)

## Checkpoint [N] - [timestamp]
**Tools used so far:** [count]
**Findings:**
- [Finding 1]
- [Finding 2]
---
```

### Checkpoint Operations (Permission-Free)

**First checkpoint (creates file):**
```
Bash(command="mkdir -p docs/research")
Write(file_path="docs/research/YYYY-MM-DD-<topic>-research.md", content="# Research: <topic>\n\n## Checkpoint 1 - [timestamp]\n**Findings:**\n- [findings so far]\n---")
```

**Subsequent checkpoints (append):**
```
Read(file_path="docs/research/YYYY-MM-DD-<topic>-research.md")
Edit(file_path="docs/research/YYYY-MM-DD-<topic>-research.md",
     old_string="---",
     new_string="---\n\n## Checkpoint [N] - [timestamp]\n**Findings:**\n- [new findings]\n---")
```

### Memory Link (First Checkpoint Only)

**After first checkpoint, immediately update memory:**
```
Read(file_path=".claude/cc10x/activeContext.md")
Edit(file_path=".claude/cc10x/activeContext.md",
     old_string="## References",
     new_string="## References\n- Research (in progress): `docs/research/YYYY-MM-DD-<topic>-research.md`")
```

**Why first checkpoint links memory:** Even partial research is recoverable if memory points to the file.

### Final Save (Still Required)

Incremental checkpoints do NOT replace "Save Research (MANDATORY)".

**After research completes:**
1. Finalize the research file (remove checkpoint markers, structure properly)
2. Update memory reference from "in progress" to final
3. Extract patterns to patterns.md

### Red Flag - Research Without Checkpoints

If research uses 5+ tool calls and NO checkpoint was saved:
- You are at risk of total context loss
- STOP and save current progress before continuing

## Output Format

```markdown
## External Research Summary

**Knowledge Gap**: [What we didn't know]

**Research Conducted**:
- Source: [repo/docs URL]
- Query: [what we searched]

**Key Findings**:
1. [Pattern/approach found]
2. [Gotcha or warning]
3. [Relevant code snippet - minimal]

**Application to Task**:
[How this applies to current work]

**References Saved**:
- [URL for future debugging]
```

## Integration Points

**Two-Phase Execution (via cc10x-router):**

The router executes research BEFORE invoking agents. This is NOT a hint - it's a prerequisite.

```
1. Router detects github-research trigger (explicit request OR knowledge gap)
2. Router executes octocode tools directly (this skill's guidance)
3. Router passes research results to agent in prompt
```

**Research results passed to:**
- `planner` agent - For informed planning decisions
- `bug-investigator` agent - For external error patterns

**Never used during:**
- `code-reviewer` - Review focuses on code itself
- `silent-failure-hunter` - Speed is priority
- `integration-verifier` - Verification, not research

## Save Research (MANDATORY)

**Research insights are LOST after context compaction unless saved.** This section is NON-NEGOTIABLE.

### Step 1: Save Research File

```
# Create directory (permission-free)
Bash(command="mkdir -p docs/research")

# Save research using Write tool (permission-free for new files)
Write(file_path="docs/research/YYYY-MM-DD-<topic>-research.md", content="[full research from Output Format above]")
```

**File naming convention:** `YYYY-MM-DD-<topic>-research.md`
- Use today's date
- Use kebab-case for topic (e.g., `claude-code-tasks-system`, `react-server-components`)

### ATOMIC CHECKPOINT (DO NOT PROCEED UNTIL BOTH COMPLETE)

**The next two operations MUST complete in sequence with NO agent invocations between them:**
- ✓ Research file saved to docs/research/
- ⏸️ IMMEDIATELY proceed to Step 2 (do not invoke agents, do not pass go)

**Why this is critical:** If context compaction occurs between Step 1 and Step 2, the research file becomes orphaned (exists but not indexed in memory). These two operations must be atomic.

### Step 2: Update Memory (Links Research to Memory)

**CRITICAL: This must happen in the same execution block as Step 1**

**Use Edit tool with stable anchor (permission-free):**

```
# Step 1: READ
Read(file_path=".claude/cc10x/activeContext.md")

# Step 2: VERIFY "## References" exists (if not, use fallback below)

# Step 3: EDIT using stable anchor
Edit(file_path=".claude/cc10x/activeContext.md",
     old_string="## References",
     new_string="## References\n- Research: `docs/research/YYYY-MM-DD-topic-research.md` → [Key insight]")

# Step 4: VERIFY (do not skip)
Read(file_path=".claude/cc10x/activeContext.md")
```

**If References section doesn't exist (fallback):**
```
Edit(file_path=".claude/cc10x/activeContext.md",
     old_string="## Last Updated",
     new_string="## References\n- Research: `docs/research/YYYY-MM-DD-topic-research.md` → [Key insight]\n\n## Last Updated")

# VERIFY (do not skip)
Read(file_path=".claude/cc10x/activeContext.md")
```

### Step 3: Extract Patterns (Auto-Promote Learnings)

**If research found gotchas or reusable patterns, add to patterns.md:**

```
Read(file_path=".claude/cc10x/patterns.md")

Edit(file_path=".claude/cc10x/patterns.md",
     old_string="## Common Gotchas",
     new_string="## Common Gotchas
- [Gotcha from research]: [Solution] (Source: docs/research/YYYY-MM-DD-topic-research.md)")

# VERIFY (do not skip)
Read(file_path=".claude/cc10x/patterns.md")
```

**What to extract:**
- Error patterns and their solutions
- API quirks and workarounds
- Integration gotchas
- Best practices discovered

**What NOT to extract:**
- Task-specific implementation details
- One-time findings not applicable to future work
- Raw code snippets without context

### Step 4: Commit Research (User-Directed Only)

Do NOT auto-commit. If the user requests a commit, they will handle it.

## Red Flags - Research NOT Complete

If you finish research WITHOUT:
- [ ] Saving to `docs/research/YYYY-MM-DD-topic-research.md`
- [ ] Updating `activeContext.md` with research reference
- [ ] Extracting patterns to `patterns.md` (if applicable)

**STOP. Research is NOT complete. Go back and save.**

## Why This Matters

```
WITHOUT SAVE:
Research → Context compaction → LOST FOREVER

WITH SAVE:
Research → docs/research/ → Memory reference → PERSISTS ACROSS SESSIONS
         → patterns.md → LEARNINGS COMPOUND
```

**Research without documentation is wasted effort.**
