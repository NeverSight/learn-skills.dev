---
name: ticket-creator
description: Create structured project tickets from user intent. Use when the user wants to create a ticket, formalize a feature request, document a bug or task, or turn a conversation into a structured ticket. Handles project prefix detection, ticket numbering, and context gathering automatically.
metadata:
  version: "1.0.0"
---

# Ticket Creator

Create well-structured project tickets from user intent, with automatic context detection and intelligent defaults.

## When to Use

- User says "create a ticket", "write a ticket", "make a ticket"
- User describes a feature/bug/task and wants it formalized
- User says "turn this into a ticket" or similar
- User wants to document work in a structured format

## Workflow

### 1. Understand the Intent

Start by understanding what tickets need to be created. The user might request:
- A single ticket with full context provided
- Multiple tickets in one request (e.g., "create tickets for X, Y, and Z")
- A list of features/bugs to formalize

Extract what you can from the user's message. If the request is ambiguous or needs clarification, ask:

- What is/are the ticket(s) about? (brief descriptions)
- What type of work is this? (Epic, Task, Enhancement)
- What's the priority? (High, Medium, Low)
- Any dependencies between tickets or on other work?

Keep this conversational — don't make the user fill out a form.

### 2. Spawn Sub-Agents for Each Ticket

For each ticket to be created, fan out sub-agents to handle research and generation in parallel:

```
Create a project ticket with the following details:

Ticket Intent: <what the user wants - extracted from their request>
Type: <Epic | Task | Enhancement - inferred or specified>
Priority: <High | Medium | Low - inferred or specified>
Dependencies: <any mentioned dependencies>

Follow this workflow:

1. **Gather Project Context** - understand the codebase:
   - Check for existing tickets (`.tickets/`, `docs/tickets/`, `tickets/`, `.md` files with ticket patterns)
   - Read `README.md`, `CLAUDE.md`, `AGENTS.md` for project context
   - Check tech stack indicators (`package.json`, `Cargo.toml`, `go.mod`, etc.)
   - Sample relevant source files if the ticket mentions specific components

   Depth of research should match ticket complexity (simple bug fix needs less than an epic).

2. **Detect Project Metadata:**
   - **Project Prefix**: Check existing tickets for patterns like `[FOO-123]` or `FOO-123:` in filenames/content, try git remote URL (extract repo name, uppercase it), check `package.json` name field, or use `[PROJECT-NNN]` as placeholder
   - **Ticket Number**: If existing tickets found, extract numbers and suggest next sequential number, otherwise use `NNN` as placeholder

3. **Fill the Template** using the structure provided below.

4. **Output**: Return the completed ticket in a markdown code block, followed by a brief note about what was detected (project prefix, ticket number, context sources).

<paste the template structure from section 4 below>
```

**Important**: Spawn all sub-agents in the same turn using parallel Agent calls. This allows them to research and generate tickets concurrently.

**Sub-agent prompt template:**

```
Create a project ticket with the following intent:

<extracted description of what the user wants for this specific ticket>

Ticket metadata:
- Type: <Epic | Task | Enhancement - inferred or "Medium" if unclear>
- Priority: <High | Medium | Low - inferred or "Medium" if unclear>
- Dependencies: <any mentioned dependencies, or "None">

Follow this workflow:

1. **Gather Project Context** - Research the codebase to write meaningful acceptance criteria:

   **If opsx:explore skill is available:**
   - Invoke `/opsx:explore` with a focused prompt about what this ticket touches
   - Use the exploration results to inform the ticket description and acceptance criteria

   **Otherwise, use manual research:**
   - Check for existing tickets in: .tickets/, docs/tickets/, tickets/, or .md files with ticket patterns
   - Read README.md, CLAUDE.md, AGENTS.md for project context
   - Check tech stack indicators (package.json, Cargo.toml, go.mod, etc.)
   - Sample relevant source files if the ticket mentions specific components
   - Use Glob/Grep to find relevant code patterns

   Match research depth to ticket complexity (simple bug fix needs less than an epic).

2. **Detect Project Metadata:**
   - **Project Prefix**: Look for patterns like [FOO-123] or FOO-123: in existing tickets/filenames, try git remote URL (extract repo name, uppercase), check package.json name field, or use [PROJECT-NNN] as placeholder
   - **Ticket Number**: If existing tickets found, extract highest number and suggest next sequential, otherwise use NNN as placeholder

3. **Fill the Template** - Use this structure:

<paste the template from section 4>

4. **Output** - Return:
   a) The completed ticket in a markdown code block
   b) A brief note about what was detected (project prefix source, ticket number rationale, where context came from)
```

### 3. Aggregate and Display Results

Once all sub-agents complete:

1. Collect the generated tickets from each sub-agent's response
2. Present all tickets to the user in sequence with clear separators
3. Provide a summary:
   - How many tickets were created
   - What project prefix/numbering was detected (or if placeholders were used)
   - Any patterns noticed across tickets (e.g., all marked High priority, dependencies between them)

### 4. Fill the Template (for sub-agents)

Use this exact structure:

```markdown
### [PROJECT-NNN]: [Title]

Status: [Complete | Not Started | Closed | In Progress]
Type: [Epic | Task | Enhancement]
Priority: [High | Medium | Low]
Dependencies: [None | TICKET-ID (description)]

Description:

[1-3 paragraph context explaining the problem/goal]

Acceptance Criteria:

- [Specific, testable criteria]
- [Implementation requirements]
- [Validation/testing requirements]
- [Documentation requirements]
- [Integration/deployment requirements]
- [Edge cases covered]
- [Performance requirements if applicable]

[Optional: Additional context, architecture decisions, or approach]

**[Optional subsection heading]:**
[Bulleted details, tables, or code examples]
```

**Filling guidelines:**

- **Title**: Clear, actionable, 5-10 words
- **Status**: Default to "Not Started" unless user specifies
- **Type**: Infer from intent (new feature = Enhancement/Epic, fix = Task, large initiative = Epic)
- **Priority**: Ask if unclear, default to Medium
- **Dependencies**: "None" if no dependencies mentioned
- **Description**: 1-3 paragraphs with:
  - What problem this solves or what goal it achieves
  - Why it matters (user impact, technical debt, etc.)
  - Relevant context from the codebase
- **Acceptance Criteria**: Specific, testable bullets covering:
  - What needs to be implemented
  - How to validate it works
  - What documentation is needed
  - Integration/deployment considerations
  - Edge cases to handle
  - Performance requirements (if applicable)
- **Optional sections**: Add subsections if helpful (e.g., "Technical Approach", "Security Considerations", "Migration Plan")

### 5. Output the Ticket

Output the filled template directly to chat in a markdown code block. The user can copy it and save it wherever they manage tickets.

After outputting, briefly mention:
- What project prefix/number was detected (or that placeholder was used)
- Where you gathered context from (if you used opsx:explore, existing tickets, docs, etc.)

## Quality Guidelines

**Make tickets actionable**: Acceptance criteria should be clear enough that someone else could implement the ticket without asking questions.

**Balance detail with brevity**: Epics need more context than simple tasks. Don't over-specify trivial changes.

**Be specific about verification**: "Tests pass" is weak. "Unit tests cover X, Y, Z edge cases; integration test validates end-to-end flow" is strong.

**Capture the why**: The description should explain motivation, not just what to do. Future readers need to understand why this work mattered.

**Use domain language**: Mirror terminology from the codebase (e.g., if the code calls them "rules" not "checks", use "rules").

## Examples

**Example 1: Single Feature Request**

Input: "We need to add a --json flag to the scan command so users can pipe output to jq"

Process:
1. Parse intent: single ticket, Enhancement, Medium priority
2. Spawn one sub-agent with the ticket details
3. Sub-agent researches codebase, detects project metadata, fills template
4. Display result to user

Output to user:
```markdown
### [AUDITKIT-015]: Add JSON output format to scan command

Status: Not Started
Type: Enhancement
Priority: Medium
Dependencies: None

Description:

Users frequently need to post-process scan results programmatically. Currently, the scan command outputs human-readable text only, requiring users to write fragile parsers. Adding a `--json` flag enables structured output that can be piped to tools like `jq`, integrated into CI systems, or consumed by other automation.

This aligns with the CLI's goal of being automation-friendly while maintaining excellent human UX by default.

Acceptance Criteria:

- `auditkit scan --json <path>` outputs valid JSON to stdout
- JSON structure includes: findings array (each with rule ID, severity, location, message), summary stats, scan metadata (timestamp, version, config used)
- Human-readable output remains default (no breaking changes)
- JSON schema is documented in README.md
- Unit tests validate JSON structure matches schema
- Integration test pipes output to `jq` and extracts fields successfully
- Error messages are written to stderr (not mixed with JSON stdout)
- Exit codes remain consistent (0 = clean, 1 = findings, 2 = error)

**JSON Schema:**
```json
{
  "version": "1.0.0",
  "timestamp": "ISO-8601",
  "findings": [
    {
      "ruleId": "string",
      "severity": "critical|high|medium|low",
      "location": {"file": "string", "line": number, "column": number},
      "message": "string",
      "snippet": "string (optional)"
    }
  ],
  "summary": {"critical": 0, "high": 1, "medium": 3, "low": 5}
}
```
```

✅ **1 ticket created**

Context detected: AUDITKIT prefix from git repo, ticket 015 from existing `.tickets/` directory, CLI architecture from `src/cli/commands/scan.ts`.

---

**Example 2: Multiple Tickets**

Input: "Create tickets for: (1) fix the crash when scanning empty directories, (2) add rate limiting to the API client, (3) improve error messages in the parser"

Process:
1. Parse intent: 3 tickets needed
2. Extract details for each:
   - Ticket 1: Bug fix, High priority
   - Ticket 2: Enhancement, Medium priority
   - Ticket 3: Enhancement, Low priority
3. Spawn 3 sub-agents in parallel (one Agent call with 3 sub-agents)
4. Aggregate results and display to user

Output to user:
```markdown
### [PROJECT-016]: Fix crash when scanning empty directories

Status: Not Started
Type: Task
Priority: High
Dependencies: None

Description:

The scanner currently crashes with a null pointer exception when run on empty directories. This happens because the file discovery module assumes at least one file exists and doesn't handle the empty array case.

Users encounter this when running the scanner on newly initialized projects or filtered directories, leading to a poor experience and confusion about whether the tool is broken.

Acceptance Criteria:

- Scanner gracefully handles empty directories without crashing
- Output message clearly indicates "No files found in <path>" when appropriate
- Exit code is 0 (success) for empty directories (not an error condition)
- Unit test verifies behavior with empty directory
- Integration test runs scanner on `fixtures/empty-dir/` and validates output
- Edge case covered: directory exists but all files are ignored by config

**Technical Approach:**
- Add null check in `src/utils/file-discovery.ts` before iterating files
- Return early with informational message instead of proceeding to scan phase
```

---

```markdown
### [PROJECT-017]: Add rate limiting to API client

Status: Not Started
Type: Enhancement
Priority: Medium
Dependencies: None

Description:

The API client currently makes unlimited requests, which can lead to 429 errors from external services and potentially cause service disruption. Implementing rate limiting ensures respectful API usage and prevents hitting service quotas unexpectedly.

This is particularly important for the external rule repository sync feature, which may need to fetch many rule definitions in quick succession.

Acceptance Criteria:

- API client respects configurable rate limits (requests per second/minute)
- Configuration allows per-endpoint rate limits if needed
- Client automatically retries with exponential backoff on 429 responses
- Rate limit state persists across client instances (shared token bucket)
- Unit tests verify rate limiting logic
- Integration test confirms requests are throttled appropriately
- Documentation updated with configuration examples
- Default rate limits are conservative (avoid hitting common API limits)
```

---

```markdown
### [PROJECT-018]: Improve error messages in parser

Status: Not Started
Type: Enhancement
Priority: Low
Dependencies: None

Description:

Current parser error messages are cryptic and unhelpful for users debugging rule syntax issues. Messages like "parse error at line 42" don't indicate what went wrong or how to fix it. Improving error messages reduces support burden and improves developer experience.

Acceptance Criteria:

- Error messages include context: what was expected vs. what was found
- Line/column numbers are accurate and included in all parse errors
- Common mistakes have helpful suggestions (e.g., "Did you mean X?")
- Multi-line context shown around error location (±2 lines)
- Error messages tested for clarity with non-expert users
- Documentation includes common parse errors and solutions
- Parser maintains same performance characteristics
```

---

✅ **3 tickets created**

Summary:
- Project prefix: PROJECT (from placeholder, no existing tickets found)
- Ticket numbers: 016-018 (sequential numbering started)
- Priorities: 1 High, 2 Medium, 1 Low
- All tickets are independent (no dependencies between them)

---

## Edge Cases

- **No git repo**: Sub-agents can't detect project prefix from remote URL → will use placeholder
- **Ambiguous intent**: Ask clarifying questions before spawning sub-agents (not after)
- **User provides partial info**: Fill in what you can before spawning sub-agents, pass defaults to them
- **Very large epic**: Consider suggesting the user break it into multiple tickets before spawning
- **Sub-agent failures**: If a sub-agent fails or times out, report the error to the user and offer to retry that specific ticket
- **Sequential numbering**: When multiple tickets are created in parallel, sub-agents may suggest the same ticket number. After aggregating results, renumber tickets sequentially if needed and note this to the user.
- **Claude.ai or environments without subagents**: Fall back to serial processing — handle each ticket one at a time following the research/detection/generation workflow inline

## Output Format

Always output the ticket in a markdown code block so the user can easily copy it:

````markdown
```markdown
### [PROJECT-001]: Ticket Title
...
```
````

Then add a brief note about what was detected/inferred.
