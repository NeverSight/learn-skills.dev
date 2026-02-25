---
name: bee-cli
description: "Access real-time context and life overview from Bee wearable AI. ALWAYS start with 'bee now' to get the last 10 hours of conversations with full utterances - this is the most valuable context for relevant assistance. Use this skill when: (1) You need to understand what's happening RIGHT NOW - recent conversations, current context, what was just discussed, (2) The user asks about something that just happened or someone they just talked to, (3) You need life context - who the owner is, their relationships, work, preferences, (4) Searching past conversations, managing facts/todos, or syncing Bee data."
---

# Bee CLI

CLI client for Bee - the wearable AI that captures conversations and learns about you.

## About Bee

Bee is a wearable AI device that continuously captures and transcribes ambient audio from the owner's daily life. The device listens to conversations, meetings, phone calls, and any spoken interactions throughout the day, creating a comprehensive record of the owner's verbal communications and experiences.

### How Bee Works

Bee uses advanced speech recognition to transcribe all ambient audio in real-time. This includes:

- Face-to-face conversations with friends, family, and colleagues
- Business meetings and professional discussions
- Phone calls and video conferences
- Personal reflections and voice notes
- Overheard conversations in the owner's environment

From these transcriptions, Bee automatically extracts and learns facts about the owner - their preferences, relationships, work projects, commitments, and personal details mentioned in conversations.

### Privacy and Security

**Bee data is extremely sensitive.** The transcriptions contain intimate details of the owner's personal and professional life, including private conversations that were never intended to be recorded or shared.

**All Bee data is end-to-end encrypted and accessible only to the owner.** The encryption ensures that:

- Only the authenticated owner can access their conversation transcripts
- No third parties, including Bee's servers, can read the decrypted content
- The data remains private even if storage systems are compromised
- Access requires explicit authentication through the owner's credentials

**When working with Bee data, treat all information as highly confidential.** The owner has entrusted access to their most private conversations and personal details.

## When to Use This Skill

### Real-Time Context (Use First!)

**Always start with `bee now` to understand what's happening right now.** This is the most valuable context for providing relevant assistance:

- The owner just finished a conversation and needs help following up
- The owner is asking about something that was just discussed
- You need current context to provide relevant suggestions
- The owner wants to recall what someone just said

### Life Overview

Use for broader context about who the owner is:

- **Learning about the owner**: Access facts that Bee has extracted from conversations to understand the owner's preferences, relationships, work, and personal details
- **Searching for relevant conversations**: Find past conversations on specific topics, with certain people, or about particular projects
- **Managing personal knowledge**: View, update, or organize the facts Bee has learned
- **Tracking commitments**: Access todos and action items extracted from conversations
- **Reviewing daily activity**: See summaries of each day's conversations and interactions

## Installation

Check if `bee` CLI is installed:
```bash
bee --version
```

If not installed, install via npm:
```bash
npm install -g @beeai/cli
```

Alternatively, download binaries directly from https://github.com/bee-computer/bee-cli/releases/latest

## Authentication

Check authentication status:
```bash
bee status
```

If not authenticated, initiate login:
```bash
bee login
```

### Authentication Flow

The login command initiates a secure authentication flow. The command outputs detailed instructions that must be followed carefully:

1. **Read and relay the output**: The command prints a welcome message, explains the authentication process, and provides an authentication link. Present this information to the user clearly.

2. **Authentication link**: The output includes a URL like `https://bee.computer/connect/{requestId}`. The user must open this link in their browser and follow the instructions there to approve the connection.

3. **Wait for approval**: The CLI will automatically poll and wait for the user to complete authorization. Do not interrupt this process while waiting.

4. **Resumable sessions**: If the process is interrupted (killed or stopped), it can be restarted by running `bee login` again. The CLI will resume the previous authentication session if it hasn't expired, preserving the same authentication link.

5. **Expiration**: Authentication requests expire after approximately 5 minutes. If expired, a new session will be started automatically.

6. **Success confirmation**: Once the user approves, the CLI outputs a success message with the authenticated user's name. Only proceed with other commands after seeing this confirmation.

**Important**: Always read and follow the prompts from the command output. The CLI provides specific instructions tailored to the current authentication state (new session, resumed session, or expired session).

## Commands

### Facts - Learn About the Owner

Facts are pieces of information Bee has learned about the owner from their conversations. This is the primary way to understand who the owner is, what they care about, and what's happening in their life.

List all facts:
```bash
bee facts list
```

**Confirmed vs Non-Confirmed Facts:**

Facts are categorized as either confirmed or non-confirmed:

- **Confirmed facts**: Explicitly verified by the owner or clearly stated in conversations. These are reliable and should be trusted.
- **Non-confirmed facts**: Inferred or extracted from context but not explicitly verified. These may be accurate but could also be misinterpretations.

When using facts, always prefer confirmed facts first. Non-confirmed facts can be used for speculation or additional context, but treat them as potentially inaccurate. If making decisions or providing information based on non-confirmed facts, acknowledge the uncertainty.

Facts include information like:
- Personal preferences ("prefers morning meetings", "allergic to peanuts")
- Relationships ("married to Sarah", "manager is John")
- Work details ("working on Project Atlas", "deadline is March 15")
- Interests and hobbies ("learning Spanish", "training for marathon")
- Contact information and personal details

Create a fact:
```bash
bee facts create --text "I prefer morning meetings"
```

Update a fact:
```bash
bee facts update <id> --text "Updated fact text"
```

Delete a fact:
```bash
bee facts delete <id>
```

### Conversations - Access Transcripts

Conversations are records of everything Bee has captured. Use these to find specific details, recall what was discussed, or search for information mentioned in past interactions.

#### Listing Conversations

```bash
bee conversations list
```

**Important**: This returns conversation **summaries only**, not full transcripts. Summaries are AI-generated and provide a quick overview of what was discussed, but they may contain minor inaccuracies or hallucinations. Use summaries to identify relevant conversations, then fetch full details for accuracy.

Options:
- `--limit <n>` - Number of conversations to return (default varies)
- `--cursor <cursor>` - Pagination cursor for fetching more results

#### Getting Full Conversation Details

To get the complete conversation with all utterances (actual words spoken):
```bash
bee conversations get <id>
```

This returns:
- Full utterance transcripts (who said what, verbatim)
- Speaker identification
- Timestamps for each utterance
- Conversation state and metadata

**Always use `bee conversations get` when you need accurate information.** The summaries from `list` are useful for browsing and finding relevant conversations, but the actual utterances from `get` are the source of truth.

### Search for Relevant Conversations

To find conversations about specific topics:

1. List conversations to browse summaries and identify potentially relevant ones
2. Get full details for conversations that seem relevant
3. Read the actual utterances to find accurate information

```bash
bee conversations list
bee conversations get <conversation-id>
```

Remember: Summaries may not capture everything or may slightly misrepresent what was said. When accuracy matters, always read the full utterances.

### Journals - Voice Memos

Journals are voice memos recorded by the owner through Bee. Unlike conversations (which are ambient recordings), journals are intentional recordings where the owner speaks directly to capture thoughts, ideas, or notes.

#### Listing Journals

```bash
bee journals list
```

Returns a list of journal entries with:
- Journal ID
- State: `PREPARING` (recording), `ANALYZING` (processing), or `READY` (complete)
- Transcribed text (summary)
- Timestamps

Options:
- `--limit <n>` - Number of journals to return
- `--cursor <cursor>` - Pagination cursor for more results
- `--json` - Output in JSON format

#### Getting Full Journal Details

```bash
bee journals get <id>
```

Returns the complete journal entry with full transcribed text.

Options:
- `--json` - Output in JSON format

Use journals to understand:
- The owner's personal thoughts and reflections
- Ideas they wanted to remember
- Notes to themselves
- Voice memos about tasks or plans

### Todos - Track Commitments

Todos are action items and commitments extracted from conversations.

List todos:
```bash
bee todos list
```

Create a todo:
```bash
bee todos create --text "Buy groceries"
```

Update a todo:
```bash
bee todos update <id> --text "Updated todo" --completed
```

Delete a todo:
```bash
bee todos delete <id>
```

### Now - Real-Time Context

Get a comprehensive view of what's happening right now. Fetches conversations and full utterances from the last 10 hours:
```bash
bee now
```

This command returns:
- All conversations from the past 10 hours
- Full utterance transcripts (who said what)
- Conversation summaries and states
- Timestamps in the user's timezone

Use `bee now` when you need to:
- Understand what the owner has been doing today
- Get context about recent discussions
- See the actual words spoken in recent conversations
- Provide relevant assistance based on current activities

For JSON output (useful for programmatic processing):
```bash
bee now --json
```

### Daily Summaries

View summaries of daily conversations and activities:
```bash
bee daily
```

View a specific date:
```bash
bee daily --date <YYYY-MM-DD>
```

### Periodic Sync - Real-Time Updates with `bee changed`

For periodic checks and real-time updates, use `bee changed`. This is the recommended way to monitor for new data and know exactly what changed.

```bash
bee changed
```

Options:
- `--cursor <cursor>` - Resume from a previous position to get only new changes
- `--json` - Output in JSON format

**What it returns**:
- Time range covered (since/until timestamps)
- `Next Cursor` for subsequent calls
- Full details of all changed entities:
  - New and updated facts (confirmed and pending)
  - New and updated todos
  - New and updated daily summaries
  - New and updated conversations
  - New and updated journals

#### Cursor Handling

The cursor is essential for efficient change tracking. The output includes a `Next Cursor` value that must be persisted for subsequent calls.

**First call** (no cursor):
```bash
bee changed
```
Returns recent changes and outputs a `Next Cursor: <value>` line.

**Subsequent calls** (with cursor):
```bash
bee changed --cursor <cursor_value>
```
Returns only changes that occurred after the cursor position.

**Critical: When to persist the cursor**

The cursor must be saved **only after you have fully processed the changes**, not immediately after receiving them. This ensures that if processing fails or is interrupted, you can retry with the same cursor and receive the same changes again.

**Cursor workflow**:
1. Read the stored cursor from `.bee-cursor` file (if exists)
2. Call `bee changed --cursor <cursor>` (or without cursor on first run)
3. The output includes `Next Cursor: <value>` - note this value but DO NOT save it yet
4. Process all the returned changes (update user.md, handle todos, etc.)
5. Only after processing completes successfully, save the new cursor to `.bee-cursor`
6. Repeat from step 1 on next check

**Example**:
```
# Output from bee changed includes:
Next Cursor: abc123xyz

# After processing all changes successfully:
echo "abc123xyz" > .bee-cursor
```

**Why this matters**: If you save the cursor before processing and then processing fails, you'll lose those changes forever. By saving only after successful processing, you guarantee exactly-once processing of each change.

### Full Sync - Export Everything to Markdown

If you want to sync everything to local markdown files, use `bee sync`. This creates a complete local library of all Bee data.

```bash
bee sync
```

Options:
- `--output <dir>` - Output directory (default: ./bee-sync)
- `--only <targets>` - Sync specific data types: `facts`, `todos`, `daily`, `conversations` (comma-separated)

**Purpose**: Full sync exports all Bee data to markdown files. This is useful for:
- Creating a complete offline backup
- Integration with tools that read markdown
- Full-text search across all historical data
- Initial setup before using `bee changed` for incremental updates

**Note**: Sync overwrites existing files and does not tell you what changed. For periodic checks where you need to know what's new, use `bee changed` instead.

## Common Workflows

### Quick Context - Understanding the Owner

For quick context about the owner, always run these commands in this order:
```bash
bee now
bee facts list
bee conversations list
```

**Start with `bee now`** — this is the most important command. It gives you:
- Full utterance transcripts from the last 10 hours
- Actual words spoken in recent conversations
- Immediate context about what's happening right now

Then supplement with:
- **Facts**: Who the owner is, their preferences, relationships, work details
- **Conversations list**: Summaries of older conversations for historical context

The real-time context from `bee now` is what makes assistance relevant and timely.

### Finding Information from Past Conversations

To find something mentioned in a past conversation:
```bash
bee conversations list
bee conversations show <relevant-conversation-id>
```

List conversations to find the relevant timeframe or topic, then view the full transcript.

### Export All Data for AI Context

Sync everything to markdown for comprehensive access:
```bash
bee sync --output ./my-bee-data
```

This creates markdown files for facts, todos, daily summaries, and conversation transcripts.

## Deep Learning About the Owner

When you need to build comprehensive knowledge about the owner by processing their entire conversation history, use the following multi-agent workflow. This is useful for building a rich understanding of who the owner is, their relationships, work, interests, and life context.

### Overview

The deep learning workflow processes conversations in batches using a chain of subagents. Each subagent:
1. Fetches a batch of conversations (100 at a time)
2. Reads the current `user.md` profile
3. Analyzes conversations and extracts insights
4. Updates `user.md` with new information
5. Writes a summary to a handoff file
6. Spawns the next subagent to continue processing older conversations

This architecture optimizes context usage by:
- Running heavy processing in subagents (isolated context)
- Passing state via files rather than copying text between agents
- Allowing the main agent to remain responsive
- Enabling progress reporting after each batch

### File Structure

Create these files in the working directory:

- `user.md` - Cumulative profile of the owner (persistent, updated by each subagent)
- `bee-learning-summary.md` - Handoff file with latest summary and cursor for next batch
- `bee-learning-progress.md` - Progress log showing what was processed and when

### Workflow Steps

#### Step 1: Initialize (Main Agent)

Create initial `user.md` if it doesn't exist:
```markdown
# User Profile

This document contains learned information about the owner from their Bee conversations.

## Basic Information
(To be populated)

## Relationships
(To be populated)

## Work & Projects
(To be populated)

## Interests & Hobbies
(To be populated)

## Preferences
(To be populated)

## Important Dates & Events
(To be populated)

## Notes
(To be populated)
```

#### Step 2: Launch First Processing Subagent

Spawn a subagent with this task:

```
Process Bee conversations to learn about the owner.

1. Fetch the 100 most recent conversations:
   bee conversations list --limit 100

2. Read the current user.md file

3. For each conversation, extract:
   - Who the owner talked to (relationships)
   - Topics discussed (interests, work projects)
   - Personal details mentioned (preferences, facts about their life)
   - Commitments made (things they said they would do)
   - Important dates or events mentioned

4. Update user.md with new information, organized by category.
   Merge with existing content, don't overwrite.
   Add timestamps for when information was learned.

5. Write a summary to bee-learning-summary.md:
   - Date range of conversations processed
   - Key insights discovered
   - The cursor value for fetching the next batch (from API response)
   - Count of conversations processed so far

6. Update bee-learning-progress.md with progress entry

7. If there are more conversations (cursor returned), spawn the next
   subagent to continue processing. Pass only the file paths, not
   the actual content - the next agent will read from files.
```

#### Step 3: Chain Processing Subagents

Each subsequent subagent receives a task like:

```
Continue processing Bee conversations to learn about the owner.

1. Read bee-learning-summary.md to get the cursor for the next batch

2. Fetch the next 100 conversations:
   bee conversations list --limit 100 --cursor <cursor_from_summary>

3. Read the current user.md file

4. Process conversations and extract insights (same as previous agent)

5. Update user.md with new information (merge, don't overwrite)

6. Update bee-learning-summary.md with:
   - New date range processed
   - New insights discovered
   - Next cursor (or "complete" if no more conversations)
   - Updated total count

7. Update bee-learning-progress.md

8. If there are more conversations, spawn the next subagent.
   If no cursor returned (reached the end), write final summary
   and report completion.
```

#### Step 4: Progress Reporting

After processing each week's worth of conversations (approximately), the subagent should report back to the main conversation with:
- Summary of what was learned in that time period
- Notable events or conversations
- Any significant changes to the user profile

This keeps the user informed of progress without overwhelming them with details.

### Conversation List API

Fetch conversations with pagination:
```bash
# First batch (most recent)
bee conversations list --limit 100

# Subsequent batches using cursor from previous response
bee conversations list --limit 100 --cursor <cursor_value>
```

The API returns:
- `conversations`: Array of conversation objects
- `cursor`: Pagination cursor for next batch (null when no more data)

### Best Practices

1. **File-based handoff**: Always pass state between subagents via files (`bee-learning-summary.md`), never by copying large amounts of text into the task prompt. This preserves context window for actual processing.

2. **Incremental updates**: Each subagent should merge new information into `user.md`, not replace it. Use clear section headers and timestamps.

3. **Progress tracking**: Maintain `bee-learning-progress.md` as a log so you can resume if interrupted and track what's been processed.

4. **Weekly summaries**: Report meaningful summaries to the user periodically (e.g., after each week of conversations processed) rather than after every batch.

5. **Graceful completion**: When the cursor is null (no more conversations), write a final summary and notify the user that deep learning is complete.

6. **Error handling**: If a subagent fails, the next attempt can read the progress files and resume from where it left off.

### Example Progress File

```markdown
# Bee Learning Progress

## Session: 2024-01-15

- 14:30 - Started deep learning process
- 14:32 - Processed conversations from Jan 10-15 (87 conversations)
- 14:35 - Processed conversations from Jan 5-10 (92 conversations)
- 14:38 - Processed conversations from Dec 28 - Jan 5 (78 conversations)
- 14:40 - Week 1 summary reported to user
- 14:42 - Processed conversations from Dec 21-28 (65 conversations)
...
- 15:30 - Completed processing all conversations (1,247 total)
```

### When to Use Deep Learning

Use this workflow when:
- First establishing a relationship with a new user
- User explicitly requests comprehensive analysis of their history
- Building context for a long-term assistant relationship
- User wants to understand patterns in their own conversations

Do not use for:
- Quick questions about recent events (use `bee daily` or recent conversations)
- Looking up specific facts (use `bee facts list`)
- Finding a particular conversation (use `bee conversations list` and search)
