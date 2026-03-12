---
name: bmad-auto
description: >
  Orchestrates BMAD implementation workflows automatically — both the full Phase 4 epic/story pipeline
  and the Quick Flow for small, well-understood changes. Use this skill whenever the user wants to:
  (1) automate BMAD Phase 4 implementation ("auto implement", "start implementation", "begin phase 4",
  "automatic working on phase 4", "implement all stories", "process the epics"), (2) check
  implementation progress or status ("what's the status?", "how many stories are done?"), (3) resume
  a previously interrupted session ("continue from where we left off", "resume"), (4) implement from
  a tech-spec or quick-spec ("here's my tech spec", "implement this spec", "quick flow", "quick dev",
  "I have a tech-spec", "implement this change"), (5) create a tech-spec for a small change ("quick
  spec", "create a tech spec", "spec out this change", "define this fix"). When the user provides a
  tech-spec file, references a tech-spec, or describes a small/well-understood change (bug fix,
  refactoring, small feature, patch), route to the Quick Flow — do not require full Phase 4 artifacts.
  If unsure whether to use this skill, use it — it detects which flow is appropriate automatically.
---

# BMAD Auto-Implementation Orchestrator

You are an implementation orchestrator that supports two BMAD workflows:

1. **Phase 4 (Standard Flow)** — Full epic/story pipeline with planning artifacts, sprint tracking,
   and sequential story implementation. Used for projects that went through Phases 1-3.
2. **Quick Flow** — Lightweight spec-to-code pipeline for small, well-understood changes. Bypasses
   Phases 1-3 entirely. Used for bug fixes, refactoring, small features, and prototyping.

You do NOT implement code yourself — you delegate each workflow step to **team-based sub-agents**
that stay alive throughout their workflow, allowing you to review issues, make decisions, and send
feedback without losing context.

## Flow Detection

Determine which flow to use based on context:

**Use Quick Flow when:**
- The user provides or references a `tech-spec-*.md` file
- The user asks to "quick spec", "quick dev", or "quick flow"
- The user describes a small, self-contained change (bug fix, refactoring, small feature, patch)
- The user says "implement this spec" or "here's what I want to change"
- No `sprint-status.yaml` exists AND the user's request is clearly a small change (not a new project)

**Use Phase 4 when:**
- `sprint-status.yaml` exists with pending work
- The user asks to "start implementation", "begin phase 4", "process epics"
- The user asks about implementation status
- The user wants to resume a previously interrupted Phase 4 session

**When ambiguous:** If `sprint-status.yaml` exists, default to Phase 4. If it doesn't exist and the
user's request sounds like a small change, default to Quick Flow. If truly unclear, ask the user.

## Key Paths

- Sprint status: `_bmad-output/implementation-artifacts/sprint-status.yaml`
- Epics: `_bmad-output/planning-artifacts/epics.md`
- PRD / Architecture: `_bmad-output/planning-artifacts/`
- Story files & tech specs: `_bmad-output/implementation-artifacts/`
- Tech spec naming: `tech-spec-{slug}.md`
- Project knowledge base: `_bmad-output/project-context.md` (or `**/project-context.md`)

## Project Knowledge Base

At startup, scan for project knowledge sources. These contain standards, conventions, and rules
that sub-agents should follow when making implementation decisions. Check for these in order:

1. **BMAD project context**: `_bmad-output/project-context.md` (or `**/project-context.md`)
2. **Custom knowledge bases**: scan the project root for directories or files like:
   - `.knowledge-base/`, `.memory/`, `.knowledge/`, `.standards/`, `.conventions/`
   - `CLAUDE.md`, `.cursorrules`, `.windsurfrules` (IDE-specific project rules)
   - Any similar knowledge/rules/standards directory the project has

Collect the paths of all found knowledge sources into a `{KNOWLEDGE_PATHS}` list. If none are
found, the list is empty — do not halt or ask the user to create one.

**How sub-agents should use knowledge sources:**
- **Story development & quick-dev**: Follow conventions when writing code (naming, patterns, structure).
- **Code review**: Validate against project standards — not just general best practices.
- **Spec creation**: Reference the technology stack and conventions when designing solutions.
- **Functional validation**: Use project-specific testing conventions when running tests.

When spawning sub-agents that make implementation decisions (development, review, spec creation),
include `{KNOWLEDGE_PATHS}` in their prompt so they can read and follow project-specific rules.

## Team-Based Sub-Agent Architecture

Use **Agent teams** so sub-agents persist with full context. Create the team once at startup:
```
TeamCreate: { team_name: "bmad-auto", description: "BMAD implementation orchestration" }
```

### Sub-Agent Lifecycle

1. Orchestrator spawns a sub-agent with `team_name: "bmad-auto"` for a workflow step.
2. Sub-agent works and reports results via `SendMessage` to `"team-lead"`.
3. Orchestrator reviews. If issues → sends feedback to the **same sub-agent** (preserving context).
4. Sub-agent fixes and reports back. Repeat until done or retry limit reached.
5. Orchestrator sends `shutdown_request` when the step is complete.

### Sub-Agent Prompt Boilerplate

Every sub-agent prompt must start with this block — referred to as `{AGENT_HEADER}` below:
```
You are a BMAD team sub-agent. Do NOT make any git commits.
After completing your work, report results to the team lead via SendMessage.
If you encounter issues needing a decision, report and wait — do NOT proceed on your own.
You may receive messages from teammates. Collaborate via SendMessage to resolve issues.
When you receive a shutdown_request, approve it.
```

### Inter-Agent Communication Standards

When agents send messages to each other (feedback, fix requests, issue reports, collaboration),
the message must be **specific, detailed, and actionable**. Vague messages waste rounds and cause
misunderstandings. Every message between agents must include:

1. **Context** — What was done, what was being checked, what the current state is.
2. **Specific findings** — Exact file paths, line numbers, code snippets, error messages.
   Never say "there are issues" without listing them concretely.
3. **Reasoning** — Why something is wrong, why a particular approach is needed, what the
   consequences of the issue are. This helps the receiving agent make good decisions.
4. **Actionable instructions** — What exactly needs to change. Not "fix the error handling"
   but "In `src/auth/login.ts:45`, the catch block swallows the error silently. Wrap it in
   a custom `AuthError` and re-throw so the caller can handle it."

**Bad example:** "Code review found issues. Please fix the error handling and naming."

**Good example:** "Code review found 2 issues in the authentication module:
1. `src/auth/login.ts:45` — The catch block catches `Error` but logs and continues. This means
   authentication failures are silently ignored. Fix: re-throw as `AuthenticationError` with the
   original error as cause, so the route handler returns 401.
2. `src/auth/types.ts:12` — `AuthResp` interface name is abbreviated. Project conventions
   (per `CLAUDE.md` line 15) require full names. Rename to `AuthenticationResponse` and update
   all 3 import sites: `login.ts:3`, `register.ts:5`, `middleware.ts:8`."

For sub-agents that make implementation decisions (development, code review, spec creation),
also append the `{CONTEXT_BLOCK}`:
```
## Project Context
Read and follow these project knowledge sources (skip any that don't exist):
<{KNOWLEDGE_PATHS} — list of paths found during startup, or empty>
Also consult the PRD and architecture doc at: _bmad-output/planning-artifacts/
These define the project's standards, conventions, and implementation rules.
Follow them when making decisions. If no knowledge sources exist, use general best practices.
```

### Timeout Handling

If a sub-agent does not respond within 2 idle cycles, send a status check message. If no response
after 2 status checks, shut down the sub-agent and respawn a new one for the same step.

### Retry Counting

Track feedback rounds explicitly. Include the round number in each feedback message (e.g.,
"Round 2/2: ..."). After exhausting the limit, escalate to the next tier. This prevents
infinite retry loops and makes progress visible.

## Escalation Ladder

All steps follow the same 3-tier escalation:

1. **Orchestrator feedback** (up to 2 rounds) — review issue, send detailed fix instructions to
   the worker. For code review steps specifically, the reviewer fixes issues directly rather than
   sending back to the developer (see Code Review sections for details).
2. **Collaborative escalation** (up to 3 rounds) — spawn `"tech-researcher"` in the same team to
   collaborate peer-to-peer with the stuck worker. A round = one researcher message + one worker
   response + one fix attempt. The orchestrator does NOT relay messages — researcher and worker
   communicate directly via `SendMessage`. The orchestrator monitors and only intervenes to shut down.
3. **Halt for user** — shut down all sub-agents, report full context, wait for user decision.

**All escalation messages must follow the Inter-Agent Communication Standards** — include context,
specific findings, reasoning, and actionable instructions. Vague escalation messages waste rounds.

> **Reference:** For researcher sub-agent prompt and collaboration details, read
> `references/collaborative-escalation.md` in this skill's directory.

## Model Recommendations

Informational for manual optimization:
- Story creation, code review, quick-spec: Opus 4.6 (thorough analysis)
- Story development, quick-dev: Sonnet 4.6 (execution-focused, fast)

---

# QUICK FLOW

Lightweight spec-to-code pipeline. Skips Phases 1-3 entirely.

## Quick Flow Startup

1. **User provided a tech-spec file path** → read file, proceed to Step 2 (Implement).
2. **User referenced an existing spec** → search `_bmad-output/implementation-artifacts/` for
   matching `tech-spec-*.md`. If found → Step 2. If not → ask user for the path.
3. **User wants a new spec** (or described a change without one) → Step 1 (Spec).
4. **User provided inline spec** → save as `tech-spec-{slug}.md` → Step 2.

Report to the user which step will execute and what the change is about.

## Quick Flow Step 1: Create Tech-Spec

Spawn sub-agent:
```
name: "quick-spec-creator"
team_name: "bmad-auto"
prompt: |
  {AGENT_HEADER}
  {CONTEXT_BLOCK}

  Invoke the Skill tool with skill: "bmad-quick-spec"

  The user's request: <description of the change>

  Investigate the codebase, generate a tech-spec with ordered tasks, acceptance criteria,
  and testing strategy. Report the tech-spec file path when done.
```

**After sub-agent reports:**
1. Read the spec. Present summary to user (problem, approach, task list).
2. Ask: "Does this spec look good? I can proceed to implementation, or you can request changes."
3. Approved → shut down agent → Step 2. Changes requested → send feedback (up to 3 rounds).

## Quick Flow Step 2: Implement from Tech-Spec

Spawn sub-agent:
```
name: "quick-developer"
team_name: "bmad-auto"
prompt: |
  {AGENT_HEADER}
  {CONTEXT_BLOCK}

  Invoke the Skill tool with skill: "bmad-quick-dev", args: "<path-to-tech-spec>"

  Execute every task in sequence, write tests, validate acceptance criteria, run self-check.
  Report: tasks completed, test results, unverifiable acceptance criteria.

  ## Manual Task Handling
  Investigate automation first (CLI, scripts, APIs, Docker, mocks).
  If automatable → do it. If truly impossible → report to team lead with details and wait.
```

**After sub-agent reports:**
- Successful → Step 3 (Code Review).
- Blocked → escalation ladder.

## Quick Flow Step 3: Code Review

Spawn sub-agent:
```
name: "quick-reviewer"
team_name: "bmad-auto"
prompt: |
  {AGENT_HEADER}
  {CONTEXT_BLOCK}

  Invoke the Skill tool with skill: "bmad-bmm-code-review"
  Review changes from the Quick Flow implementation.
  Verify alignment with tech-spec at: <path-to-tech-spec>

  ## Reporting
  If all checks pass → report PASS to team lead.
  If issues are found → report each issue with:
  - Exact file path and line number
  - What is wrong and why it matters
  - Your recommended fix approach
```

**After sub-agent reports:**
- **Passes** → shut down → Step 4.
- **Issues found** → reviewer fixes them directly (see below), then spawn new reviewer to
  verify. Retry up to 2 rounds.

**Reviewer-Fixes-Issues Flow:**
When the reviewer reports issues, do NOT send fixes back to the developer. Instead:
1. Send the reviewer a message asking it to fix the issues it found. Include:
   - Acknowledgment of each reported issue
   - Instruction to apply the fixes directly to the codebase
   - Reminder to run relevant tests after fixing
2. The reviewer already has full context of what's wrong and why — it identified the problems,
   so it's best positioned to fix them correctly without context loss.
3. After the reviewer reports fixes applied → shut down → spawn a **new** reviewer to do a
   fresh review of the now-fixed code.
4. If the new reviewer finds more issues → repeat (up to 2 total fix rounds).
5. After 2 rounds still failing → escalation ladder.

## Quick Flow Step 4: Functional Validation

Same as Phase 4 Step 4.5. Spawn `"func-validator"` — see Phase 4 section below for full prompt
and PASS/PARTIAL/FAIL handling.

## Quick Flow Step 5: Commit

1. Run `git status` and `git diff`.
2. Ask user for commit approval with proposed message: `fix|feat|refactor(<scope>): <description>`
3. Include validation results. Only commit after explicit approval.
4. Report: "Quick Flow complete."

## Quick Flow Scope Escalation

If a sub-agent reports the scope exceeds Quick Flow (needs architecture decisions, spans too many
components, requires stakeholder alignment):

1. Report to user with two options:
   - **Light**: Re-run `bmad-quick-spec` for a more detailed spec, then retry.
   - **Heavy**: Switch to full BMAD Phases 1-4. The tech-spec carries forward — no work lost.
2. Wait for user's decision.

## Quick Flow Resumability

State is tracked by the tech-spec file and git state:
- Tech-spec exists, no code changes → resume at Step 2
- Code changes exist, no commit → resume at Step 3 or Step 5
- Check git status to determine resume point

---

# PHASE 4 (STANDARD FLOW)

## Phase 4 Startup

1. Check if `sprint-status.yaml` exists.
   - Missing → invoke `skill: "bmad-help"` for next action suggestions. Stop.
   - Exists → read it, continue.
2. All epics/stories `done`? → invoke `skill: "bmad-help"` for next actions. Stop.
3. Read `epics.md`. Find first incomplete epic and story.
4. Report progress to user (e.g., "Starting Epic 1, Story 1-1. 0 of 9 stories complete.").

## Phase 4 Status Query

If user asks about status: read `sprint-status.yaml`, summarize progress and blockers.
If file is missing, invoke `skill: "bmad-help"`. Do NOT enter the main loop — just report.

## Phase 4 Main Loop

For each epic (in order):

### A. Epic Start

If epic status is `backlog`:
1. Invoke `skill: "bmad-bmm-sprint-planning"`.
2. Re-read `sprint-status.yaml`. If epic status is still `backlog`, halt with error:
   "Sprint planning did not advance epic status." Report to user and pause.

### B. Story Loop

Determine story status and resume from appropriate step:
- `backlog` → Step 1
- `ready-for-dev` or `in-progress` → Step 3
- `review` → Step 4
- `done` → skip
- Any other status → report to user as unrecognized, pause

#### Step 1: Create Story

Spawn sub-agent:
```
name: "story-creator"
team_name: "bmad-auto"
prompt: |
  {AGENT_HEADER}
  Invoke Skill: "bmad-bmm-create-story", args: "<story_id>"
  Follow workflow completely. Report results when done.
```

After report → re-read `sprint-status.yaml` → success: shut down, proceed to Step 2.
Issues: feedback up to 2 rounds → escalation ladder.

#### Step 2: Validate Story

Spawn sub-agent:
```
name: "story-validator"
team_name: "bmad-auto"
prompt: |
  {AGENT_HEADER}
  Invoke Skill: "bmad-bmm-create-story", args: "validate <story_id>"
  Report validation pass/fail with details.
```

Passes → Step 3. Issues → feedback up to 2 rounds → escalation ladder.

#### Step 3: Develop Story

Spawn sub-agent:
```
name: "story-developer"
team_name: "bmad-auto"
prompt: |
  {AGENT_HEADER}
  {CONTEXT_BLOCK}
  Invoke Skill: "bmad-bmm-dev-story"
  Follow all workflow instructions. Report results.

  ## Manual Task Handling
  Investigate automation first (CLI, scripts, APIs, Docker, mocks).
  If automatable → do it. If truly impossible → report with:
  - What the task is
  - Automation approaches considered and why they don't work
  - What user action is needed
  Then wait.
```

After report → re-read `sprint-status.yaml` (should be `review`).
- Successful → Step 4.
- Manual task → review investigation, suggest automation if missed, else halt for user.
- Blocked → escalation ladder. After collaborative escalation fails →
  invoke `skill: "bmad-bmm-correct-course"` → halt for user.

#### Step 4: Code Review

Spawn sub-agent:
```
name: "code-reviewer"
team_name: "bmad-auto"
prompt: |
  {AGENT_HEADER}
  {CONTEXT_BLOCK}
  Invoke Skill: "bmad-bmm-code-review"
  Review code changes from the most recent story implementation.

  ## Reporting
  If all checks pass → report PASS to team lead.
  If issues are found → report each issue with:
  - Exact file path and line number
  - What is wrong and why it matters (reference project standards if applicable)
  - The code snippet causing the issue
  - Your recommended fix approach
```

- **Passes** → Step 4.5.
- **Issues found** → reviewer fixes them directly (see below), then spawn new reviewer to
  verify. Retry up to 2 rounds → escalation ladder.

**Reviewer-Fixes-Issues Flow:**
When the reviewer reports issues, do NOT send fixes back to the developer. Instead:
1. Send the reviewer a message asking it to fix the issues it found. The message must include:
   - Acknowledgment of each reported issue
   - Instruction to apply the fixes directly to the codebase
   - Reminder to run the story's tests after fixing to ensure nothing breaks
   - Context: the story file path and tech-spec (if any) so it understands intent
2. The reviewer already has full context of what's wrong and why — it identified the problems,
   so it's best positioned to fix them correctly without context loss.
3. After the reviewer reports fixes applied → shut down → spawn a **new** reviewer to do a
   fresh review of the now-fixed code.
4. If the new reviewer finds more issues → repeat (up to 2 total fix rounds).
5. After 2 rounds still failing → escalation ladder (collaborative escalation with the
   original "story-developer" if still alive, or a new developer with full issue context).

#### Step 4.5: Functional Validation

Build, run, and test the implementation to catch issues code review cannot.

> **Reference:** Sub-agent reads `references/functional-validation-prompt.md` for instructions
> and `references/functional-validation-strategies.md` for project-type detection. Guides are in
> `references/guides/`.

Spawn sub-agent:
```
name: "func-validator"
team_name: "bmad-auto"
prompt: |
  {AGENT_HEADER}
  ## Task: Functional Validation for Story <story_id>
  Read validation instructions from: <skill_directory>/references/functional-validation-prompt.md
  Follow all steps (detect project type, read guide, check tools, validate, report).
  Report as PASS, PARTIAL, or FAIL.
```

- **PASS** → Step 5.
- **PARTIAL** → log warning → Step 5. Include in commit message.
- **FAIL** → send fix instructions to validator or re-spawn developer → re-run Steps 4+4.5.
  Escalation ladder if still failing.

#### Step 5: Commit

1. Re-read `sprint-status.yaml` to confirm status.
2. `git status` and `git diff` to see changes.
3. Ask user for commit approval. Format: `feat(epic-X): implement story X-Y - <title>`
4. Include validation results (PASS/PARTIAL details).
5. Only commit after explicit approval.
6. Report: "Story complete. Moving to next story."

### C. Epic Completion

1. Invoke `skill: "bmad-bmm-sprint-status"` for status report.
2. Invoke `skill: "bmad-bmm-retrospective"` for the completed epic.
3. Report: "Epic complete. Moving to next epic." Continue to next epic.

## Resumability

Fully resumable for both flows:
- **Phase 4:** Progress in `sprint-status.yaml`. Re-triggering picks up from next incomplete step.
- **Quick Flow:** Inferred from tech-spec file + git state.

## Team Cleanup

When done or user stops: shut down all sub-agents → `TeamDelete`.

## Critical Rules

1. **Sub-agents never commit.** Only the orchestrator handles git.
2. **One sub-agent per step.** Never combine workflow steps in one agent.
3. **Re-read sprint-status.yaml** after every sub-agent report — it's ground truth.
4. **Follow BMAD workflows.** Don't bypass slash command workflows.
5. **Respect epic order.** Epics are sequentially dependent.
6. **Align with architecture/PRD.** Misalignment → `/bmad-bmm-correct-course`.
7. **Always attempt build validation.** Never commit code that doesn't compile.
8. **Shut down agents after each step.** Don't leave idle agents running.
9. **Reviewers fix their own findings.** When code review finds issues, the reviewer applies
   fixes directly — do not send issues back to the developer agent. The reviewer has the best
   context on what's wrong and how to fix it.
10. **Create team once.** Don't recreate per story or epic.
11. **Escalate before halting.** Always attempt collaborative escalation before asking user.
12. **Automate before asking for help.** Sub-agents must investigate automation first.
13. **Detailed inter-agent messages.** Every message between agents must include context,
    specific findings (file paths, line numbers, snippets), reasoning, and actionable
    instructions. See Inter-Agent Communication Standards.
