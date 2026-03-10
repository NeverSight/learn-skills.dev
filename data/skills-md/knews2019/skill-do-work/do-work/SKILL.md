---
name: do-work
description: Task queue - add requests or process pending work
argument-hint: (describe a task) | run | verify requests | review work | present work | clarify | cleanup | version
upstream: https://raw.githubusercontent.com/knews2019/skill-do-work/main/SKILL.md
---

# Do-Work Skill

A unified entry point for task capture and processing.

**Actions:**

- **capture requests**: Capture new tasks/requests → creates UR folder (verbatim input) + REQ files (queue items), always paired
- **verify requests**: Evaluate captured REQs against original input → quality check
- **work**: Process pending requests → executes the queue
- **clarify questions**: Batch-review Open Questions from completed work → user answers, confirms, or skips
- **review work**: Post-work review → requirements check, code review, acceptance testing, and testing suggestions
- **present work**: Client-facing deliverables → briefs, architecture diagrams, value propositions, Remotion videos
- **cleanup**: Consolidate archive → moves loose REQs into UR folders, closes completed URs
- **commit**: Commit uncommitted files → analyzes, groups atomically, traces to REQs

> **Core concept:** The capture requests action always produces both a UR folder (preserving the original input) and REQ files (the queue items). Each REQ links back to its UR via `user_request` frontmatter. This pairing is mandatory for all requests — simple or complex.

> **Capture ≠ Execute.** The capture requests action captures requests. The work action executes them. These are strictly separate operations. After capture finishes writing files and reporting back, **STOP**. Do not start processing the queue, do not begin implementation, do not "helpfully" transition into the work action. The user decides when to execute — always. The only exception is if the user explicitly says something like "add this and then run it" or "capture this and start working" in the same invocation.

> **Human time has two optimal windows.** The system is designed to maximize the value of human attention:
>
> 1. **Capture phase** (capture requests action) — The user is present, actively thinking about the request. This is the best time for back-and-forth: clarifying ambiguities, resolving contradictions, making scope decisions. Use `AskUserQuestion` with concrete choices here. Every question must present options — never open-ended "what do you mean?" prompts.
>
> 2. **Batch question review** (clarify questions action) — After the build phase completes everything it can without feedback, any remaining `pending-answers` REQs are surfaced as a batch. The user reviews all builder-decided questions together, confirms or adjusts, and resolved REQs re-enter the queue.
>
> Between these windows, the build phase runs autonomously. Builders never block on Open Questions — they mark them `- [~]` with best-judgment reasoning and create `pending-answers` follow-ups when they return via `do work clarify`.

## Routing Decision

### Step 1: Parse the Input

Examine what follows "do work":


Check these patterns **in order** — first match wins:

| Priority | Pattern                  | Example                                                                                                                            | Route                         |
| -------- | ------------------------ | ---------------------------------------------------------------------------------------------------------------------------------- | ----------------------------- |
| 1        | Empty or bare invocation | `do work`                                                                                                                          | → help menu                   |
| 2        | Action verbs only        | `do work run`, `do work go`, `do work start`                                                                                       | → work                        |
| 3        | Verify keywords          | `do work verify`, `do work verify requests`, `do work check`, `do work evaluate`                                                   | → verify requests              |
| 4        | Clarify keywords         | `do work clarify`, `do work questions`, `do work pending`                                                                          | → clarify questions            |
| 5        | Review keywords          | `do work review`, `do work review work`, `do work review code`, `do work code review`, `do work audit code`                        | → review work                  |
| 6        | Present keywords         | `do work present`, `do work present work`, `do work showcase`, `do work deliver`                                                   | → present work                 |
| 7        | Cleanup keywords         | `do work cleanup`, `do work tidy`, `do work consolidate`                                                                           | → cleanup                     |
| 8        | Commit keywords          | `do work commit`, `do work commit changes`, `do work save work`                                                                    | → commit                      |
| 9        | Version keywords         | `do work version`, `do work update`, `do work check for updates`                                                                   | → version                     |
| 10       | Changelog keywords       | `do work changelog`, `do work release notes`, `do work what's new`, `do work what's changed`, `do work updates`, `do work history` | → version                     |
| 11       | Descriptive content      | `do work add dark mode`, `do work [meeting notes]`, `do work capture request [the request]`                                        | → capture requests              |


### Step 2: Preserve Payload

**Critical rule**: Never lose the user's content.

**Single-word rule**: A single word is either a known keyword or ambiguous — it is never "descriptive content."

- **Matches a keyword** in the routing table (e.g., "version", "verify", "cleanup") → route to that action directly.
- **Doesn't match any keyword** (e.g., "refactor", "optimize") → ambiguous. Ask: "Do you want to add '`{word}`' as a new request, or did you mean something else?"

Only route to **capture requests** when the input is clearly descriptive — multiple words, a sentence, a feature request, etc.

If routing is genuinely unclear AND multi-word content was provided:

- Default to **capture requests** (adding a task)
- Hold onto $ARGUMENTS
- If truly ambiguous, ask: "Add this as a request, or start the work loop?"
- User replies with just "add" or "work" → proceed with original content

### Action Verbs (→ Work)

These signal "process the queue":
run, go, start, begin, work, process, execute, build, continue, resume

### Clarify Verbs (→ Clarify Questions)

These signal "review pending questions":
clarify, answers, questions, pending, pending answers, blocked, what's blocked, what needs answers

Note: This routes to the work action with `mode: clarify` — see work.md "Clarify Questions" section.

### Verify Verbs (→ Verify Requests)

These signal "check request quality":
verify, verify requests, check, evaluate, review requests, review reqs, audit

Note: "check" routes to verify requests ONLY when used alone or with a target (e.g., "do work check UR-003"). When followed by descriptive content it routes to capture requests (e.g., "do work check if the button works" → capture requests).

Note: "audit" alone routes to verify requests. "audit code" and "audit implementation" route to review work (see Review Verbs below).

### Review Verbs (→ Review Work)

These signal "review the completed work":
review, review work, review code, code review, audit code, audit implementation, review REQ-NNN, review UR-NNN

Note: "review requests" and "review reqs" route to **verify requests** (priority 4), not review work. "review" alone or followed by a target/code-related word routes to review work (priority 5). The review work action also runs automatically as part of the work pipeline — see `work.md` Step 7.

### Present Verbs (→ Present Work)

These signal "generate client-facing deliverables":
present, present work, showcase, deliver, pitch, client brief

Note: `do work present` (no target) presents the most recent completed UR. `do work present all` or `do work present portfolio` enters portfolio mode. `do work present UR-003` or `do work present REQ-005` targets specific work.

### Cleanup Verbs (→ Cleanup)

These signal "consolidate the archive":
cleanup, clean up, tidy, consolidate, organize archive, fix archive

### Commit Verbs (→ Commit)

These signal "commit uncommitted files atomically":
commit, commit changes, commit files, save changes, save work

### Changelog Verbs (→ Version)

These signal "show release notes":
changelog, release notes, what's new, what's changed, updates, history

Note: "updates" (plural) routes to changelog display. "update" (singular) routes to update check. Both are handled by the version action.

### Content Signals (→ Capture Requests)

These signal "add a new task":

- Descriptive text beyond a single verb
- Feature requests, bug reports, ideas
- Screenshots or context
- "add", "create", "I need", "we should"

## Examples

### Help Menu (bare invocation)

When invoked with no arguments (`do work`), show a help menu with available actions and example prompts:

```
do-work — task queue for agentic coding tools

  Capture requests:
    do work add dark mode to settings
    do work the search is slow and the header is misaligned
    do work [paste meeting notes, specs, or a screenshot]

  Process the queue:
    do work run

  Verify & review:
    do work verify requests     Check capture quality against original input
    do work review work         Review completed work (requirements + code + acceptance)

  Present to client:
    do work present work        Generate client brief, architecture, value prop
    do work present all         Portfolio summary of all completed work

  Other actions:
    do work clarify             Answer pending questions from completed work
    do work cleanup             Consolidate the archive
    do work commit              Analyze and commit uncommitted files atomically
    do work version             Check version / updates
    do work changelog           Show release notes
```

Do not ask "Start the work loop?" — just print the help menu and wait.

### Routes to Work

- `do work run` → Starts work action immediately
- `do work go` → Starts work action immediately

### Routes to Clarify Questions

- `do work clarify` → Presents all pending-answers REQs for batch review
- `do work questions` → Same as clarify
- `do work answers` → Same as clarify
- `do work pending` → Same as clarify
- `do work what's blocked` → Same as clarify

### Routes to Verify Requests

- `do work verify requests` → Evaluates most recent UR's REQs
- `do work verify` → Evaluates most recent UR's REQs
- `do work verify UR-003` → Evaluates specific UR
- `do work check REQ-018` → Evaluates the UR that REQ-018 belongs to
- `do work evaluate` → Evaluates most recent UR's REQs
- `do work review requests` → Evaluates most recent UR's REQs

### Routes to Review Work

- `do work review work` → Reviews the most recently completed REQ
- `do work review` → Reviews the most recently completed REQ
- `do work review REQ-005` → Reviews a specific completed REQ
- `do work review UR-003` → Reviews all completed REQs under that UR
- `do work code review` → Reviews the most recently completed REQ
- `do work review code` → Reviews the most recently completed REQ

### Routes to Present Work

- `do work present work` → Generates deliverables for most recently completed UR
- `do work present` → Same as present work
- `do work present UR-003` → Generates deliverables for specific UR
- `do work present REQ-005` → Generates deliverables for specific REQ
- `do work present all` → Portfolio summary of all completed work
- `do work present portfolio` → Same as present all
- `do work showcase` → Same as present work

### Routes to Cleanup

- `do work cleanup` → Consolidates archive, closes completed URs
- `do work tidy` → Same as cleanup
- `do work consolidate` → Same as cleanup

### Routes to Commit

- `do work commit` → Analyzes and commits all uncommitted files atomically
- `do work commit changes` → Same as commit
- `do work save work` → Same as commit

### Routes to Changelog (via Version)

- `do work changelog` → Displays changelog (newest at bottom)
- `do work release notes` → Same as changelog
- `do work what's new` → Same as changelog
- `do work updates` → Same as changelog
- `do work history` → Same as changelog

### Routes to Capture Requests

- `do work add dark mode` → Creates REQ file + UR folder
- `do work the button is broken` → Creates REQ file + UR folder
- `do work [400 words]` → Creates REQ files + UR folder with full verbatim input

## Payload Preservation Rules

When clarification is needed but content was provided:

1. **Do not lose $ARGUMENTS** - keep the full payload in context
2. **Ask a simple question**: "Add this as a request, or start the work loop?"
3. **Accept minimal replies**: User says just "add" or "work"
4. **Proceed with original content**: Apply the chosen action to the stored arguments
5. **Never ask the user to re-paste content**

This enables a two-phase commit pattern:

1. Capture intent payload
2. Confirm action

## Action Dispatch

Each action has an action file with full instructions. How you execute it depends on your environment's capabilities.

| Action             | Action file                     | Context to pass                |
|--------------------|---------------------------------|--------------------------------|
| capture requests   | `./actions/capture.md`          | Full user input text           |
| work               | `./actions/work.md`             | (none needed)                  |
| clarify questions  | `./actions/work.md`             | `mode: clarify`                |
| verify requests    | `./actions/verify-requests.md`  | Target UR/REQ or "most recent" |
| review work        | `./actions/review-work.md`      | Target REQ/UR or "most recent" |
| present work       | `./actions/present-work.md`     | Target REQ/UR, "most recent", or "all" |
| cleanup            | `./actions/cleanup.md`          | (none needed)                  |
| commit             | `./actions/commit.md`           | (none needed)                  |
| version            | `./actions/version.md`          | `$ARGUMENTS`                   |

### If subagents are available

Dispatch each action to a subagent. The subagent reads the action file and executes it — the main thread only sees the routing decision and the returned summary.

- **`work` and `cleanup`**: Run in the background if your environment supports it. Print a status line (e.g., "Work queue processing in background...") and return control to the user immediately.
- **`capture requests`, `clarify questions`, `verify requests`, `review work`, `present work`, `version`**: Run in the foreground (blocking). These need user interaction or produce small immediate output.
- **Screenshots (`capture requests` only):** Subagents can't see images from the main conversation. Before dispatching, save screenshots to `do-work/user-requests/.pending-assets/screenshot-{n}.png`, write a text description of each, and include the paths + descriptions in the subagent prompt.

### If subagents are not available

Read the action file directly and follow its instructions in the current session. The action files are designed to work as standalone prompts — no subagent infrastructure required.

### On failure

Report the error to the user. Do not retry automatically.

## Suggest Next Steps

After every action completes, suggest the next logical prompts the user might want to run. Use fully qualified action names so the user can copy-paste directly.

**After capture requests:**
```
Next steps:
  do work verify requests     Check capture quality before building
  do work run                 Start processing the queue
```

**After work (queue processing):**
```
Next steps:
  do work review work         Review the completed work
  do work present work        Generate client-facing deliverables
  do work clarify             Answer any pending questions
```

**After verify requests:**
```
Next steps:
  do work run                 Start processing the queue
  do work [describe changes]  Capture additional requests
```

**After review work:**
```
Next steps:
  do work present work        Generate client-facing deliverables
  do work run                 Process follow-up REQs (if any were created)
  do work [describe changes]  Capture new requests
```

**After present work:**
```
Next steps:
  do work present all         Generate portfolio summary (if multiple URs completed)
  do work [describe changes]  Capture new requests
```

**After commit:**
```
Next steps:
  do work review work         Review the committed changes
  do work [describe changes]  Capture new requests
```

**After clarify questions:**
```
Next steps:
  do work run                 Process answered questions
  do work clarify             Continue answering (if skipped any)
```

**Rules:**
- Only suggest prompts that provide value given the current state (e.g., don't suggest `do work run` if the queue is empty)
- Use the full action name (`verify requests`, not just `verify`; `review work`, not just `review`)
- Keep it to 2-3 suggestions max — don't overwhelm
- Format as a simple list the user can scan and copy

