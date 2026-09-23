---
name: skill-optimizer
author: Crystian
license: MIT
description: "Optimizer that refines and professionalizes AI agent skills through real usage — saves tokens, eliminates redundancy, and tightens instructions so skills cost less to run. Learns from mistakes, reviews quality, and improves over time. Observes skill execution in the current conversation, analyzes up to four sources (conversation friction, file diffs, user feedback, static diagnostic) plus accumulated lessons, and proposes concrete improvements to the target skill's SKILL.md. Works with Claude Code and compatible SKILL.md-based agent frameworks. Use after executing any skill: `/skill-optimizer [name]` or `/skill-optimizer` to auto-detect. `--review` processes accumulated lessons."
metadata:
  version: 2.0.0
  tags: skill-improvement, feedback-loop, retrospective, code-quality, agent-tools, meta-skill, continuous-learning, review, kaizen, efficiency, optimization, improvements
  github: https://github.com/crystian/skills
  linkedin: https://www.linkedin.com/in/crystian
---

# Skill Optimizer

> Born from real-world production usage across multiple projects. Every diagnostic category, every proposal flow, and every guardrail exists because it solved a real problem in a real skill.

Kaizen (改善) for AI agent skills. Observe how a skill performed, find what went wrong or could be better, and propose concrete changes to its SKILL.md.

Diagnoses root causes and proposes improvements — you decide each one. Tracks recurrence in LESSONS.md with automatic importance escalation.

## Execution

### 1. Resolve target

- `/skill-optimizer` (default) — enter listening mode. Output ONLY this single line:
  "skill-optimizer is observing the conversation, waiting for a skill to complete..."
  Nothing else — no explanations, no additional context, no prompts. Be silent.
  Then wait — do not prompt or block. The user will manually invoke
  `/skill-optimizer --review` when ready to analyze.
  This is the ideal scenario — the optimizer observes the skill in real time.

- `/skill-optimizer <name>` — target a specific skill by name
- `/skill-optimizer --diagnose` or `/skill-optimizer <name> --diagnose` — run static
  diagnostic directly on the SKILL.md without prior observation. Skips conversation
  friction and file diffs — uses static diagnostic + user feedback only.
  If no target can be resolved, ask the user: "Which skill do you want to diagnose?
  Provide the name or path."
- `/skill-optimizer --review` — skip to accumulated lessons (no skill execution needed).
  If no target can be resolved (no name, no prior skill in conversation), ask the
  user: "Which skill do you want to review? Provide the name or path."
  If multiple skills were executed in this conversation, ask the user:
  "Multiple skills detected — which one do you want to review?"
  If no `LESSONS.md` exists, inform the user: "No accumulated lessons found —
  static diagnostic and user feedback will still run. Run `/skill-optimizer`
  after a skill execution to start collecting lessons."
- `/skill-optimizer <name> --review` — review accumulated lessons for the named skill.
  Combines target resolution with `--review` mode. If no `LESSONS.md` exists,
  apply the same fallback: inform the user and offer a static diagnostic.

Argument order does not matter — `--review <name>` is equivalent to `<name> --review`.
`--diagnose` and `--review` are mutually exclusive — if both are provided, inform the
user: "Cannot use `--diagnose` and `--review` together. Pick one." and stop.

Once resolved, read the target's `SKILL.md` and `LESSONS.md` (if exists).

**Skill resolution**: Search for `<name>/SKILL.md` in these paths (first match wins):

1. `.claude/skills/`
2. `.agents/skills/`
3. The parent directory of the skill that invoked the optimizer (peer skills are
   expected as sibling folders — e.g., `../other-skill/SKILL.md`)
4. Current working directory

If not found in any path, tell the user: "Could not find `<name>/SKILL.md`.
Check the skill name or provide the full path." Do not guess or search outside
these paths.

**Path input**: If `<name>` contains `/` (e.g., `./my-skill`, `../other-skill`,
or an absolute path), treat it as a direct path — read `<name>/SKILL.md` (or
`<name>` if it already ends in `SKILL.md`). Skip the 4-path search. If the file
does not exist, report: "File not found at `<path>`. Check the path and try again."

**Extra arguments**: Any arguments beyond `<name>`, `--review`, or `--diagnose`
are ignored. Inform the user: "Extra arguments ignored: [args]."

**Self-optimization**: The default mode is observation (conversation friction +
file diffs), but when the target is `skill-optimizer` itself, self-observation is
unreliable — skip conversation friction and file diffs, fall back to static
diagnostic + user feedback instead.

**Fallback without prior run**: If the target skill was not executed in this
conversation (e.g., `/skill-optimizer <name>` without prior run), fall back to
static diagnostic + user feedback. State this to the user before proceeding.

### 2. Gather

Collect findings from the appropriate source:

**Sources**: conversation friction, file diffs, user feedback, static diagnostic

- **Default** — enters listening mode; analysis deferred to `--review`
- **`<name>` without prior run** — static diagnostic, user feedback
- **`<name>` with prior run** — conversation, diffs, static diagnostic, user feedback
- **`--diagnose`** — static diagnostic, user feedback
- **`--review`** — conversation, diffs, existing LESSONS.md entries, static diagnostic, user feedback

**Conversation friction**:

- Errors or exceptions during skill execution
- User corrections ("no, not that", "I meant...", "undo that")
- Retries or repeated attempts at the same step
- Manual interventions the user had to make
- Confusion about what the skill was supposed to do
- Steps the skill skipped or did in the wrong order

**File diffs**:
Use `git diff` (or `git diff --cached`) to inspect changes made during the
skill's execution. If not in a git repo, compare file contents against the
SKILL.md's expected output. Look for:

- Files the skill created or modified — do they match what was expected?
- Changes the user had to make after the skill ran (post-corrections)
- Incomplete implementations (TODOs, placeholders, missing pieces)
- Patterns that deviate from what the SKILL.md prescribed

**User feedback**:
After gathering findings, ask the user:
"Want to add anything, or should we review the findings?"

**Static diagnostic** (used in `--review`, `--diagnose`, and `<name>` without prior run):
Validate against baseline rules:

- Frontmatter must have `name` and `description` (required)
- Description max 1024 characters, third person, with specific trigger phrases
- Body should be under 500 lines and under 5k tokens — use `references/` for overflow.
  Token count is the primary constraint; line count is a quick heuristic.
- Name: lowercase, hyphens only, 1-64 characters
- Progressive disclosure: metadata (~100 tokens) → body → resources (as needed)
- Check for: dead content (unreferenced sections, commented-out blocks, instructions
  that no longer match the skill's actual behavior), scope creep (sections that belong
  in a different skill or exceed the stated purpose), trigger quality (description
  contains specific verbs and contexts that help the harness match user intent — not
  just generic terms), token efficiency (redundant paragraphs, verbose phrasing that
  could be tightened without losing meaning), completeness (all stated flows have
  matching instructions — no "TODO" or undocumented branches), task trackability
  (skill defines sequential steps or phases but does not instruct the agent to
  track progress via harness task tools)
- When recommending `references/`: this is a subdirectory alongside SKILL.md
  that holds supporting material (tables, examples, templates) the agent loads
  on demand. Files should be markdown, named descriptively (e.g.,
  `references/diagnostic-tables.md`), and referenced from the body with
  explicit load instructions (e.g., "Read `references/diagnostic-tables.md`
  for the full list").
- If the target SKILL.md is missing frontmatter or required fields (`name`,
  `description`), report it as a `high` finding and propose adding the
  missing structure — infer values from the body content.
- **Task discovery**: Scan the skill's execution flow for numbered steps, phases,
  or sequential tasks (e.g., `### 1.`, `Step N:`, `Phase N`, ordered markdown
  lists within execution sections). If found, enumerate them in the diagnostic
  output:
  ```
  Tasks detected (N):
    1. [step title or summary]
    2. [step title or summary]
    ...
  ```
  Then check: does the skill instruct the agent to report progress per step?
  If not, and the harness provides task management tools (e.g., `TaskCreate`/
  `TaskUpdate` in Claude Code, `todo` in OMO — or skip if none exists), propose adding an instruction like:
  "Create a task per step at the start of execution and update each task's
  status as it completes, so the user can track progress."
  Importance: `medium`. Diagnostic: `missing instruction`.

Cross-reference against the SKILL.md. Read `references/diagnostic-tables.md`
(relative to this skill's own directory, NOT the project CWD) for the category
and root-cause lookup tables.

**Static diagnostic output**: Present results as a single unified checklist before proposals:

- One line per baseline rule: ✅ for pass, ❌ for findings (include importance + short description)
- Cross-reference findings go in the same list with ❌ — no separate section, no numbering
- End with finding count: "Found N findings." or "No issues found."

**Importance**: `high` (breaks output, errors) · `medium` (suboptimal, friction) · `low` (style, preferences)

**Recurrence**: Same pattern in LESSONS.md? Increment `Hits` instead of duplicating.
Hits >= 3 escalates: `low` → `medium`, `medium` → `high`.

**context7 (optional)**: If the target skill references a specific
library or framework (e.g., Angular, NestJS, React), use context7
to verify that code patterns, API calls, or config examples in the
SKILL.md match current docs. Report mismatches as findings with
diagnostic `outdated content`. If the skill does not reference any
library, skip — the baseline rules are sufficient. If context7 is not
available in the environment, skip this step — the baseline rules are
sufficient.

### 3. Propose

If no findings were identified, report: "No issues found. The skill looks solid."
If user feedback was not yet collected (e.g., `--review` mode), ask for it
now. If the user has none, end with no proposals.

Before the first proposal, show the sources legend listing only the
sources actually used in the current run (e.g.,
`Sources: static diagnostic, user feedback`).

Present findings one at a time, ordered by importance.
For `--review` findings from LESSONS.md, verify the root cause still exists
in the current SKILL.md before proposing. If resolved, mark as
`(resolved)` and recommend rejecting to clean up the entry.
If there are more than 15 findings, present the top 15 (by importance) and
offer to log the rest to LESSONS.md: "There are [N] more remaining
findings — want me to log them to LESSONS.md for later review?"
If the user declines, discard the remaining findings.

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  PROPOSAL [N/total] — [importance]
  Source: [conversation | diff | user | lessons | diagnostic]

  Finding: [what was observed]
  Root cause: [diagnostic] — [which line/section and why]
  Hits: [N — omit if first occurrence]

  Proposed change: [what to add/modify/remove]
  Preview:
  - [old line]
  + [new line]
  For additions, show only `+` lines with surrounding context.
  For removals, show only `-` lines.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

Use the harness's question tool if one exists (e.g., `AskUserQuestion` in Claude Code), otherwise ask in plain text:

**Default mode:**
- question: "Proposal [N/total] — [importance]: [one-line finding summary]"
- header: "Proposal [N/total]"
- options:
  - label: "Accept", description: "Apply the edit to the SKILL.md"
  - label: "Postpone", description: "Save to LESSONS.md for later"
  - label: "Reject", description: "Discard this finding"
  - label: "Don't", description: "Add a permanent negative rule to SKILL.md"

**`--review` mode:**
- Same as above but replace "Postpone" with:
  - label: "Keep", description: "Leave in LESSONS.md for later review"

**Actions:**

- **Accept** → apply the edit
- **Postpone** → save to LESSONS.md
- **Reject** → discard (in review: remove from LESSONS.md)
- **Keep** (only in `--review`):
  - Existing LESSONS.md entry → leave it for later
  - New finding (from diagnostic or user feedback) → add to LESSONS.md
- **Don't** → ask "This will add a permanent negative rule. Confirm? (y/n)",
  then on `y`, append a negative rule at the end of the target's SKILL.md Guardrails
  section (create one if absent — place it as the last section before
  any footer like `---`) using the format:
  `- **Never [action].** [reason from the finding]`

If the user selects "Other" and types "skip all", write current and all
remaining findings to LESSONS.md and end.

Summary: `Done. [N] accepted, [N] postponed, [N] rejected, [N] don'ts.`

## LESSONS.md Format

Lives alongside the target's SKILL.md.
Read `references/lessons-format.md` (relative to this skill's own directory,
NOT the project CWD) for the full format and rules.

## Guardrails

- **Never edit without confirmation.** Show the diff, wait for explicit approval. No
  exceptions. The user owns the skill.
- **Never expose secrets.** Redact API keys, tokens, passwords, credentials (`sk-...`,
  `ghp_...`, `Bearer ...`) with `[REDACTED]` in all output and LESSONS.md.
- **Read before proposing.** Read SKILL.md + LESSONS.md first to avoid duplicates.
- **Never invent.** Zero findings is a valid outcome. Never fabricate findings or fill gaps with guesses — if you don't know, say "I don't know".
- **One at a time.** Present, decide, move on.
- **Respect structure.** Match existing style when inserting content.
- **Don'ts need double confirmation.** Negative rules are impactful — always confirm.
- **Never bump versions.** Version management is the user's responsibility — do not
  modify version fields in frontmatter.

---

Made with <3 by [Crystian](https://github.com/crystian)
