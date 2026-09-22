---
name: study
description: "Interactive learning tutor with spaced repetition, research helpers, and restart-safe study workspaces. Use when the user wants to learn something new: teach me, I want to study, help me learn, study X, create a course on, tutorial for, walk me through learning. Also use for commands like study init, study start, study status, study review, study break, and book catalog setup/search. Works across Claude Code, Codex, Hermes, Cline, OpenCode, and other Agent Skills-compatible clients for programming, math, physics, science, engineering, and other structured learning."
---

# Study Workspace - Interactive Tutor

A structured learning environment where **you write the code**, and the agent teaches, guides, and supervises. Every lesson has notes and exercises you implement yourself, with spaced repetition for long-term retention.

## Philosophy

- **You do the work** - The agent teaches and supervises, you implement
- **Structured lessons** - each lesson = notes + exercise + review
- **Spaced repetition** - FSRS algorithm resurfaces concepts before you forget
- **Research-backed content** - lessons enriched by live docs, notebooks, web research, and sciagent-skills domain expertise
- **ADHD-aware** - energy gating, capped reviews, no guilt, detailed break state
- **Git-tracked progress** - all attempts saved, safe to experiment

## Agent Compatibility

This skill follows the open Agent Skills folder shape: `SKILL.md` plus optional
`references/`, `templates/`, and `scripts/`. The durable behavior is the study
workspace contract, not any single agent client's slash-command implementation.

Before running a workflow in a new client, read:
- `references/agent-adapters.md` for Claude Code, Codex, Hermes, Cline, OpenCode,
  and generic agent setup.
- `references/workspace-lifecycle.md` for the init/start/break/resume state
  contract shared by all agents.

## Commands

### `study init <topic> [--template=<name>] [--source <path>]`

Initialize a new study workspace.

**Steps:**

0. Read `references/workspace-lifecycle.md` for the shared workspace contract.
1. Sanitize topic to directory name, create workspace, `git init`
2. **Template resolution** — read `references/template-resolution.md`:
   - Auto-detect language from topic → select template + mode (code-as-subject or code-as-tool)
   - Detect scientific domain → attach matching sciagent-skills if plugin is installed
   - Copy template files, create `lessons/`, `practice/`, `notes/`, `.fsrs/`
3. **Ask learning approach**:
   ```
   How would you like to learn?
   1. Project-based — build something real, lesson by lesson (I'll ask what you want to build)
   2. Concept-based — focused lessons with standalone exercises (default)
   3. Challenge-based — progressive difficulty, minimal hand-holding
   ```
   If **project**: ask what to build → store as `end_goal`, create `lessons/plan.md` outline
   If **project** and `sciagent_skills` are attached: use the primary skill's Workflow steps as a lesson plan backbone. Each workflow step maps to a lesson — read `references/research-agents.md` for how to extract skill content.
   - In clients without a dedicated question UI, ask in plain text and wait for
     the user's answer. Do not silently choose the default unless the user asked
     for non-interactive setup.
4. **Source material** — if `--source` provided:
   - Read `references/research-agents.md` for backend selection
   - NotebookLM available → create notebook, add PDF as source
   - Fallback → extract text via pdfplumber, save to `sources/`
   - Store source info in config
5. **Book catalog** — if `~/.config/study/book-catalog.json` exists:
   - Search catalog for topic matches
   - Show the top relevant books with title, format, and path
   - Ask: "Add any of these as source material? Reply with numbers, paths, or skip."
   - Wait for the user's answer. Do not skip this prompt unless there are no
     matches or the user asked for non-interactive setup.
6. Create `.study-config.json` (see Config Schema below), commit, show welcome

### `study start`

Start or resume a learning session.

**Resumption — always check first:**

Read `references/workspace-lifecycle.md` before mutating `.study-config.json`.

1. Read `.study-config.json`
2. If `session_state.phase` is NOT `idle`:
   - Resumed session. Read current lesson file.
   - Tell user: "Resuming — you were [doing X] on Lesson N: [title]"
   - Check `session_state.energy`: "You were at [half] battery. How are you feeling now?"
   - Pick up from saved phase
3. If `idle`: fresh session, increment `session_count`

**Fresh session flow:**

1. **Energy check**: "Before we start — full battery, half, or fumes?"
2. **Energy gating**:
   - Full → new lesson + review warm-up
   - Half → continue existing exercise or review only
   - Fumes → review only (lightweight) or suggest coming back later
3. **Optional time budget**: "How long do you have? (or skip for open-ended)"
4. **FSRS review warm-up** — read `references/fsrs-spaced-repetition.md`:
   - Resolve `<skill-dir>` to the directory containing this `SKILL.md`
   - Run: `FSRS_STORE=.fsrs/cards.json <skill-dir>/scripts/fsrs/fsrs schedule`
   - If items due: present max 3 as recall exercises (cap at 5 minutes)
   - If nothing due: skip to lesson
5. **Main lesson loop** (see below)

**Main Loop:**

```
LOOP:
  1. Agent's Turn: Teach
     - Create lesson notes (with proactive research — read references/research-agents.md)
     - Assign exercise
     - Commit notes: [agent] lesson N: topic
     - Update session_state.phase = "teaching"

  2. User's Turn: Implement
     - User works in practice/lesson-NN/
     - User can ask questions, request hints, or say "done"
     - Update session_state.phase = "practicing"

  3. Review & Feedback
     - Check git diff to see user's work
     - If sciagent skill attached: read references/difficulty-adaptation.md for verification protocol
     - Provide specific feedback (quote their code, explain why)
     - Track metrics: review_rounds, hints_requested
     - Update session_state.phase = "reviewing"

  4. Completion
     - When exercise passes review:
       - Add FSRS card: FSRS_STORE=.fsrs/cards.json <skill-dir>/scripts/fsrs/fsrs add "lesson-NN" "topic" N
       - Update lesson status to "completed"
       - Check difficulty adaptation (read references/difficulty-adaptation.md)
       - Ask: next lesson, review, or break?

  REPEAT
```

### `study status`

Show progress overview. Read `.study-config.json` and use
`references/workspace-lifecycle.md` to interpret `session_state`. If
visual-explainer is available, generate an HTML dashboard. Otherwise text:

```
Study: [topic] ([approach])
Difficulty: [level]
Progress: [N] lessons completed, [M] in review queue

Lessons:
  1. [title] ✓
  2. [title] ✓
  3. [title] ← current
  4. [title] (planned)

Review: [N] items due | Next review: [date]
Sources: [N] books attached
```

### `study review`

Standalone review session. Read `references/fsrs-spaced-repetition.md` for the full protocol. No lesson, just recall exercises for all due items.

### `study add-source <path>`

Add a PDF/ebook to the current workspace. Read `references/research-agents.md` for backend selection and ingestion.

### `study catalog build <library-path>`

Build book catalog:
```bash
cd <skill-dir>/scripts/catalog && uv run study-catalog build <library-path>
```

### `study catalog search <query>`

Search the catalog:
```bash
cd <skill-dir>/scripts/catalog && uv run study-catalog search "<query>"
```

### `study break`

Save session state and exit cleanly:
Read `references/workspace-lifecycle.md` first.
1. Commit any uncommitted changes
2. Update `.study-config.json`:
   - `session_state.phase` = current phase (NOT `idle` — that loses context)
   - `session_state.pending_action` = specific next step
   - `session_state.context` = brief note about where things stand
   - `session_state.energy` = current energy level
3. Write session summary to `notes/session-YYYY-MM-DD.md`
4. Commit: `[session] end session N`

## Lesson Structure

Each lesson file in `lessons/NN-topic.md`:

```markdown
# Lesson N: Topic

## Concept
[Clear explanation — enriched by research agent findings]

## Key Points
- Point 1
- Point 2

## Reference Example (Don't Copy!)
[Small example illustrating the concept, if helpful]

## Common Pitfalls
- Pitfall and how to avoid it

## Exercise

### What to Build
[Clear description]

### Requirements
1. Requirement 1
2. Requirement 2

### Success Criteria
- [ ] Criterion 1
- [ ] Criterion 2

### Where to Work
Create your implementation in: `practice/lesson-NN/`
```

## Teaching Rules

1. **NEVER write implementation code for the user.** Small reference examples in notes (2-5 lines) are OK. Exercises must be implemented by the user entirely.
2. **Guide, don't solve.** Hints not answers. Point to concepts, not code. Ask questions to guide thinking.
3. **Feedback is specific.** Quote their code. Explain why something is wrong/good. Suggest approach, not exact fix.
4. **Encourage experimentation.** Breaking things is learning. Git keeps everything safe.

## User Interaction

**After presenting a new lesson:**
```
What would you like to do?
1. Read the lesson and start the exercise
2. I have questions about the concept first
3. Take a break
```

**After providing feedback:**
```
What's next?
1. I'll revise my implementation
2. Questions about the feedback
3. I think it's done — final review?
4. Move to next lesson
5. Take a break
```

**When user is stuck:**
- Ask what specifically is confusing
- Provide hints, not solutions
- Spawn on-demand research agent if needed (read `references/research-agents.md`)
- Point to relevant section of lesson notes or source material

## Visual Enrichment

When teaching concepts that benefit from visual representation, read `references/visual-libraries.md` to select the right rendering approach:

- **Equations** → KaTeX (web-native, CDN)
- **Function plots, phase portraits** → JSXGraph (web-native, CDN)
- **3D surfaces** → Plotly.js (web-native, CDN)
- **Physics simulations** → p5.js + Matter.js (web-native, CDN)
- **Circuit diagrams** → SchemDraw (Python SVG generation)
- **Molecular structures** → Kekule.js (web-native) or RDKit (SVG generation)
- **Star charts** → Starplot (Python SVG generation)
- **Music notation** → LilyPond (CLI SVG generation)

If subagents or background tasks are available, ask visual-explainer with the
library choice in the prompt:

```
Agent(subagent_type="general-purpose", prompt="
  Using the visual-explainer skill, create an HTML page showing [concept].
  Use KaTeX for equations and JSXGraph for the function plot.
  Save to practice/lesson-NN/diagrams/
")
```

For SVG generation (circuits, molecules, etc.), generate a Python script, run it via Bash, and embed the SVG in the HTML.

For scientific topics with sciagent-skills attached, the plugin's visualization skills (`matplotlib-scientific-plotting`, `plotly-interactive-visualization`, `seaborn-statistical-visualization`) provide domain-appropriate plotting patterns (volcano plots, UMAP embeddings, heatmaps, survival curves). Pass the relevant sciagent visualization skill name to the visual-explainer agent for domain-specific output.

If visual-explainer is unavailable, use ASCII diagrams in the lesson notes. Visuals are enrichment, never a dependency.

## Config Schema (v3)

`.study-config.json`:

```json
{
  "version": 3,
  "topic": "Go Concurrency",
  "template": "go-idiomatic",
  "template_mode": "code-as-subject",
  "approach": "concept",
  "end_goal": null,
  "difficulty": "beginner",
  "difficulty_override": null,
  "next_calibration_at_lesson": 4,
  "mode": "tutorial",
  "created": "2026-04-04T10:00:00Z",
  "sciagent_skills": [],
  "sciagent_primary": null,
  "progress": {
    "current_lesson": 0,
    "lessons_completed": 0,
    "session_count": 0,
    "last_session": null
  },
  "lessons": [],
  "session_state": {
    "phase": "idle",
    "pending_action": null,
    "context": null,
    "energy": null,
    "time_budget_minutes": null
  },
  "sources": [],
  "review": {
    "fsrs_data_path": ".fsrs/cards.json",
    "items_due": 0,
    "last_review": null
  },
  "catalog_path": "~/.config/study/book-catalog.json"
}
```

## Git Conventions

- `[agent]` - lesson notes, feedback, guidance written by the active agent
- `[user]` - user's implementation work
- `[session]` - session start/end markers

Always commit before switching turns between the agent and user. This keeps the
git history clean and makes `git diff HEAD` reliable for reviewing user work.

## Workspace Layout

```
workspace/
├── .study-config.json
├── .fsrs/cards.json
├── lessons/
│   ├── plan.md              (project approach only)
│   ├── 01-intro.md
│   └── 02-next-topic.md
├── practice/
│   ├── lesson-01/
│   └── lesson-02/
├── notes/
│   ├── feedback-2026-04-04.md
│   └── session-2026-04-04.md
├── sources/                  (chunked text from PDFs, if no NLM)
└── [template files]          (go.mod, Makefile, etc.)
```

## Learning Approaches

- **concept** (default) — focused lessons with standalone exercises, no overarching project
- **project** — build toward a working end product; each lesson advances the build
- **challenge** — progressive difficulty, minimal notes, maximum practice

Store in `.study-config.json` → `approach`. Shapes how exercises are generated.

## Modes

Per-session modes that can change within an approach:

- **tutorial** (default) — structured lessons with concepts + exercises
- **practice** — work on exercises without new concepts
- **exploration** — user-driven, the agent assists and answers questions
- **review** — revisit previous lessons via FSRS, fill gaps
