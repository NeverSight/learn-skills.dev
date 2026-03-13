---
name: speak-memory
description: >-
  PRIMARY cross-session memory. Use INSTEAD of auto-memory for multi-step work,
  plans, or tasks spanning conversations. Tracks stories in .speak-memory/ with
  objectives, checklists, and context. ALWAYS check .speak-memory/index.md
  before starting work — resume matching stories or create new ones.
  Activates on: implement, fix, build, refactor, debug, test, feature, bug,
  task, plan, design, review, deploy, create, change, optimize, migrate,
  configure, install, develop, ship, investigate, explore, document, story,
  memory, resume, continue, status, progress, checklist.
allowed-tools: Read Write Edit Glob Grep Bash
metadata:
  version: 1.0.1
---

# Speak, Memory

Persistent story-based memory for tracking work across sessions. Each story has
an objective, checklist, current context, and activity log stored as markdown
files in `.speak-memory/` at the project root (the directory containing `.git/`,
or the current working directory if no `.git/` is found).

## Activation Protocol

On every activation, **before responding to the user**:

1. Check if `.speak-memory/index.md` exists at the project root.
2. If it exists, read it to get active stories (small table, low context cost).
3. Match the user's request against active story descriptions (see heuristics below).
4. If a match is found, read that story's `story.md` and resume silently.
   If the matched story's directory does not exist, remove that row from
   `index.md` and continue matching.
5. If no match and the request is non-trivial multi-step work, read
   `references/lifecycle.md` and create a new story.
6. If `.speak-memory/` does not exist but the request warrants tracking, read
   `references/lifecycle.md` to initialize the directory and create the first story.
7. If `index.md` is missing but `.speak-memory/stories/` exists, read
   `references/lifecycle.md` for index recovery before continuing.

Do NOT announce "loading speak-memory" or similar. Activation is invisible.
First-time initialization (creating `.speak-memory/`, modifying `.gitignore`)
should be communicated to the user since it changes their project.

## Match Heuristics

When comparing the user's request to active stories:

- Check if the request references files, features, or concepts in a story's
  objective, checklist, or current context.
- Prefer stories with status `active` over `paused`.
- Among matching stories, prefer the most recently updated one.
- If multiple stories match ambiguously, ask: "Are you continuing work on
  [story name], or starting something new?"
- One active story per interaction. Do not load or update multiple stories.

## Post-Interaction Update

After every interaction where you did **meaningful work related to the active
story**, update the story. This is not optional — it is the core persistence
mechanism. Do it silently at the end of your response.

**What to update:**

1. **Checklist**: Mark completed items `[x]`, add newly discovered items.
2. **Current Context**: Replace entirely with what was just done + what's next
   (max ~5 sentences). See `references/story-format.md` for format.
3. **Key Decisions**: Append any significant decisions made this interaction.
4. **Recent Activity**: Append one entry: `- [YYYY-MM-DD] Brief description`
5. **Frontmatter `updated`**: Set to today's date (YYYY-MM-DD).
6. **index.md**: Update the `Updated` column to today's date. Update the
   `Summary` column if the story's direction changed.

**When NOT to update**: Do not update if the interaction was unrelated to any
story (one-off question, greeting, unrelated topic). Only update when relevant
work was done on the matched story.

**Compaction**: If Recent Activity exceeds 30 entries after updating, read
`references/compaction-rules.md` and compact immediately.

## When NOT to Create a Story

- One-off questions ("what does this function do?")
- Simple single-file edits completable in one interaction
- Informational requests with no implementation component
- Greetings or non-coding requests

Stories are for work spanning multiple steps or sessions.

## Commands

Users may explicitly manage stories with these phrases:

| User says | Action |
|-----------|--------|
| "new story" / "start a story for..." | Read `references/lifecycle.md`, create a new story |
| "show stories" / "list stories" | Read and display `index.md` |
| "story status" | Show the active story's checklist and current context |
| "pause story" | Read `references/lifecycle.md`, pause the current story |
| "resume [name]" | Resume a specific story by name |
| "complete story" | Read `references/lifecycle.md`, mark story completed |
| "compact story" | Read `references/compaction-rules.md`, force compaction |
| "what was I working on?" | Read `index.md`, show active/recent stories |
| "archive story [name]" | Run `scripts/manage-stories.py --archive <name> --root <project-root>` |
| "clean up stories" | Run `scripts/manage-stories.py --prune --root <project-root>` |

## Cross-Session Pickup

Automatic story resumption is best-effort — it depends on this skill being
activated by the agent runtime. If auto-pickup does not trigger, the user can
use explicit commands above ("resume", "what was I working on?", "show stories")
as reliable fallbacks.

## Index Hygiene

Keep the index manageable. If it exceeds ~20 active+paused stories, suggest
the user archive or complete older stories. Run `scripts/manage-stories.py --prune`
to auto-archive completed stories older than 30 days.

## Reference Files

Load these only when needed — do not read them on every activation:

- `references/lifecycle.md` — Creating, resuming, pausing, completing stories;
  directory init; naming rules; index recovery
- `references/story-format.md` — Full story.md schema and section guidelines
- `references/compaction-rules.md` — When and how to compact activity logs
- `assets/index-template.md` — Template for initializing index.md
- `assets/story-template.md` — Template for new story files
- `scripts/manage-stories.py` — Archive, delete, prune, and rebuild operations
