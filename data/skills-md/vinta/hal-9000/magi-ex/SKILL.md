---
name: magi-ex
description: Use when brainstorming ideas, features, or directions for a project where independent perspectives from different model families (Claude/Codex/Gemini) would surface blind spots and spark creative options the user hasn't considered — especially "what cool things can I add", "what should I build next", "give me ideas for X"
argument-hint: "[question-or-topic]"
compatibility: Designed for Claude Code
user-invocable: true
model: opus
allowed-tools:
  - AskUserQuestion
  - TeamCreate
  - TeamDelete
  - Agent
  - SendMessage
  - WebSearch
  - Read
  - Edit
  - Write
  - Bash(gemini:*)
  - mcp__codex__codex
  - mcp__codex__codex-reply
  - Skill(writing-plans)
---

# MAGI EX

Multi-model brainstorming panel. Three teammates explore a question in parallel, each backed by a different model family, then the lead consolidates their proposals for the user.

- **Scientist** -- reasons directly as Claude Opus (no external dispatch)
- **Mother** -- delegates to OpenAI Codex via `mcp__codex__codex` MCP tool
- **Woman** -- delegates to Google Gemini via `gemini` CLI

## User Question

<user_question>
**$ARGUMENTS**
</user_question>

## Process

### 1. Clarify

If the question is underspecified, use `AskUserQuestion` to nail down purpose, constraints, and success criteria. Skip if already clear and actionable.

- Ask questions one at a time to refine the idea
- Prefer multiple choice questions when possible, but open-ended is fine too
- Only one question per message

### 2. Setup

Read the personality and reference files, then spawn all teammates in parallel.

**Files to read:**
- Personalities: [MAGI-1.md](personalities/MAGI-1.md), [MAGI-2.md](personalities/MAGI-2.md), [MAGI-3.md](personalities/MAGI-3.md)
- References: [codex.md](references/codex.md), [gemini.md](references/gemini.md)

**Create team** with `TeamCreate` using name `magi-{topic}` (e.g., `magi-auth-strategy`).

**Spawn all 3 teammates in a single message** (3 parallel `Agent` calls with `team_name` set):

| Teammate  | `name`      | `subagent_type`   | Prompt includes                                                          |
| --------- | ----------- | ----------------- | ------------------------------------------------------------------------ |
| Scientist | `scientist` | `general-purpose` | MAGI-1.md personality + question (reasons directly as Opus)              |
| Mother    | `mother`    | `general-purpose` | MAGI-2.md personality + codex.md (dispatches to Codex MCP) + question    |
| Woman     | `woman`     | `general-purpose` | MAGI-3.md personality + gemini.md (dispatches to Gemini CLI) + question  |

Include all clarified context in each spawn prompt -- teammates have no conversation history.

### 3. Parallel Exploration

The lead's role is coordination only:

- Wait for teammates to send proposals via `SendMessage`
- Forward any teammate clarifying questions to the user via `AskUserQuestion`, noting which teammate (and model) asked. Never answer on the user's behalf -- only the user answers.

### 4. Consolidate + Present

Collect all proposals, then:

1. Deduplicate similar proposals (attribute to all teammates/models that proposed it)
2. Group by theme if many proposals
3. Present each option with:
   - Which teammate(s) and model(s) proposed it (e.g., "Scientist [Opus]", "Mother [Codex]")
   - Trade-off analysis from each perspective
   - Who tagged it as their top pick and why
4. Ask the user to **select an option** via `AskUserQuestion`
5. Ask via `AskUserQuestion` what to do next:
   - **Write a plan** -- teardown, then handoff to `writing-plans`
   - **Debate** -- another round of critique (see below)
   - **Done** -- teardown, no further action

### 5. Debate (optional, user-triggered)

Only runs if the user requests it. Can be repeated.

1. Broadcast the consolidated option list to all 3 teammates via `SendMessage`
2. Each teammate critiques the proposals through their model (Scientist reasons directly; Mother and Woman follow Debate Mode in their reference files)
3. Collect updated stances and re-present to the user (back to step 4)

### 6. Teardown

Tear down only when the user selects **Write a plan** or **Done**.

1. `shutdown_request` to each teammate
2. Wait for all shutdown approvals
3. `TeamDelete`

### 7. Handoff (write a plan path only)

After teardown, invoke `writing-plans` skill with the chosen option(s) as context.
