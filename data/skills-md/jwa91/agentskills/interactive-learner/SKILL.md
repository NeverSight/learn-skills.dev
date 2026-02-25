---
name: interactive-learner
description: "Personal AI tutoring skill that deeply researches any topic, then creates rich, interactive HTML courses with quizzes, simulators, debug challenges, explain-back exercises, real-world missions, and more. Tracks per-concept mastery across sessions with spaced repetition. Use when: (1) the user wants to learn a new topic, (2) the user says 'teach me X' or 'I want to learn X', (3) the user asks for an interactive lesson or course, (4) the user wants to study or review a subject. Works for any topic: technical, conceptual, creative, math, languages."
metadata:
  version: 0.1.0
---

# Interactive Learner

Create deeply researched, engaging, interactive courses on any topic. Lessons open in the browser with a mix of click-based exercises, open-ended challenges, real-world missions, and AI-evaluated responses. Every course is personalized, evidence-based, and a little adventurous.

## Workflow

### New course: Profile → Research → Curriculum → Session → Build → Debrief

#### 1. Profile the student (first time only)

Keep profiling fast and frictionless. The student wants to learn, not fill out forms.

**Rules:**

- **Prefer multiple-choice questions.** They're faster to answer and give you structured data. Use the agent's question tool with concrete options wherever possible.
- **Max 1 open-ended question at a time.** Never dump multiple open questions in one message.
- **Max 3-4 profiling questions total.** Infer the rest from context and conversation.
- **Start teaching quickly.** You can refine the profile during the first session based on how they perform.

**What to gather (in order of priority):**

1. Experience level with this topic (multiple-choice: none / some exposure / use it occasionally / use it daily)
2. Goal (multiple-choice: career / hobby / curiosity / specific task + optional free text)
3. Time per session (multiple-choice: ~10 min / ~20 min / ~30+ min)
4. Background — only if not obvious from context (one open question max, e.g. "What's your day job or main interest?")

Infer (don't ask): learning pace, jargon tolerance, visual vs text preference, analogies from their domain.

See [student-profiling.md](references/student-profiling.md) for the full profiling framework.

Initialize progress:

> All scripts use `uv run`. If `uv` is not available, use `python3` instead.
>
> **Path note:** `.agents/skills/` and `.claude/skills/` are symlinked — both paths reference the same location. Examples below use `.agents/`.

```bash
uv run .agents/skills/interactive-learner/scripts/progress.py init <course> <name>
```

#### 2. Research the topic thoroughly

**This is critical. Do not skip or rush this step.** Before designing any curriculum, become an expert on the subject.

**Deep research protocol:**

1. **Search for authoritative, recent sources** — prioritize official documentation, peer-reviewed content, respected practitioners, and recent (2024-2026) material
2. **Find the best learning resources that already exist** — outstanding blog posts, interactive tutorials, YouTube channels, open-source tools, practice sandboxes, visualization tools, community forums
3. **Identify the conceptual structure** — what are the foundational concepts? What depends on what? What are the common misconceptions? What's the optimal learning order?
4. **Discover the "aha moments"** — what analogies, visualizations, or exercises make this topic click for people? What do the best teachers do differently?
5. **Collect real-world examples** — case studies, war stories, practical applications that make abstract concepts tangible
6. **Find hands-on resources** — playgrounds, sandboxes, tools the student can actually use during the course

**Save research notes** to a file the student can reference later:

```bash
# Write research to a markdown file alongside the course
# Include: key sources, recommended deep-dives, practice resources, community links
```

**Source priorities** (in order):

1. Official documentation and specs
2. Peer-reviewed research / reputable educational content
3. Respected practitioners and educators (conference talks, well-known blogs)
4. Community-vetted resources (highly-rated tutorials, curated awesome-lists)
5. Interactive tools and sandboxes

**Connecting research to lessons:**
- Reference 1-2 sources inline in story-cards where relevant (e.g., "According to the Bash Reference Manual...")
- End every explainer with a `recommended-deep-dive` section linking 2-4 of your best research sources

#### 3. Design the curriculum

Based on research, plan the full course:

- 8-12 sessions for a standard course (3-5 for quick intro, 12-20 for deep dive)
- Define learning objectives per session — what will the student be able to DO after each one?
- Map concept dependencies — what must come before what?
- Plan review touchpoints — which earlier concepts get revisited where?
- Identify sessions where real-world missions, external tools, or deeper exploration fit naturally
- Max 6 new vocabulary terms per session, each with a bridging analogy

Save the curriculum and show it to the student as an interactive dashboard:

1. Write a curriculum JSON file (array of session objects):
   ```json
   [
     {
       "session_number": 1,
       "title": "How Bash Actually Works",
       "description": "The mental model that changes everything",
       "objectives": ["Explain what a shell does", "Break down command syntax"],
       "concepts": ["shell-mental-model", "commands-and-arguments"],
       "estimated_minutes": 20
     }
   ]
   ```
2. Save it to the course progress:
   ```bash
   uv run .agents/skills/interactive-learner/scripts/progress.py set-curriculum <course> <curriculum.json>
   ```
3. Build and open the dashboard so the student can see the full plan:
   ```bash
   uv run .agents/skills/interactive-learner/scripts/build-dashboard.py --open
   ```

**STOP here.** Ask the student to review the curriculum in the dashboard. Let them react, reprioritize, or skip sessions they already know. Do not proceed to step 4 until the student confirms the plan.

See [course-design-guide.md](references/course-design-guide.md) for topic-type → component mapping and session patterns.

#### 4. Build the explainer

Build a lesson config using **only content components** (no scored exercises):

- **MANDATORY: Before generating JSON for ANY component, read its schema in [component-catalog.md](references/component-catalog.md). Do NOT guess field names. Every component has different required fields — using wrong field names produces empty/broken output that silently fails.**
- **MANDATORY: Search for videos before building the explainer:**
  ```bash
  uv run .agents/skills/interactive-learner/scripts/find-videos.py "topic for beginners"
  ```
  Embed 1-2 if good results exist. If nothing suitable, note this and move on. The search is required; embedding is not.
- See [sharp-edges.md](references/sharp-edges.md) for anti-patterns to avoid
- Design the explanation first, then pick the best component for each piece
- Include at least one moment of surprise, delight, or creative challenge per session
- Keep JSON concise but rich: ~60-100 lines

```bash
uv run .agents/skills/interactive-learner/scripts/build-lesson.py <explainer.json> --mode explainer --course <course-id> --open
```

Tell the student what the explainer covers (1-2 sentences about concepts and ideas), invite questions, and let them know you're available to explain anything in more detail. Do NOT list component types in your message — describe what they'll *learn*, not what components you used.

#### 5. Conversational checkpoint

When the student comes back after reading:

1. **Ask "Was everything clear?"** — discuss any confusion, clarify using your research sources. If the student has questions, answer them thoroughly and refer to the research notes.
2. **Ask 1 teach-back question in chat** — "Let me quickly check if you're ready for the test: [question about a key concept from the explainer]"
3. If the student struggles, explain further before proceeding. If they nail it, move to the test.

Open-ended assessment (explain-back, roleplay, open-reflection) happens here in conversation, not in HTML. The agent evaluates responses in real-time.

#### 6. Build the test

Build a test config using **only scored components** + `score-summary`:

- Include `quiz`, `matching`, `fill-blanks`, `sorting-game`, and/or `custom` components
- Always end with `score-summary`
- Keep JSON concise: ~40-80 lines

```bash
uv run .agents/skills/interactive-learner/scripts/build-lesson.py <test.json> --mode test --course <course-id> --open
```

Tell the student to complete the test and click "Get my result code" when done.

#### 7. Debrief after the session

After the student completes the test:

1. Student clicks "Get my result code" — a compact code appears on screen (e.g. `BASH-7A3E-9C51-...`)
2. Student copies the code and pastes it back in chat
3. Agent decodes the result code:
   ```bash
   uv run .agents/skills/interactive-learner/scripts/progress.py decode <code>
   ```
4. Update progress with decoded scores AND concept mastery:
   ```bash
   uv run .agents/skills/interactive-learner/scripts/progress.py update <course> --session N --score S --max M --concepts '{"pod-basics": 0.9, "deployments": 0.6}'
   ```
   Assign concept scores based on your knowledge of which test questions tested which concepts.
5. Rebuild the dashboard:
   ```bash
   uv run .agents/skills/interactive-learner/scripts/build-dashboard.py --open
   ```
6. Discuss what they found hard or interesting
7. If they had a real-world mission: ask how it went, what they discovered
8. Prepare notes for the next session — adjust based on everything you learned

### Returning student: Review → Adapt → Build next session

```bash
uv run .agents/skills/interactive-learner/scripts/progress.py show
```

Check:

- Concept mastery levels — which concepts need review? (below 0.7 = needs reinforcement)
- Time since last session — longer gap = more review needed
- Recent scores — adjust difficulty
- Open questions or missions from last session — follow up on these
- Achievements earned — acknowledge naturally

Generate the next session, weaving in review of weak concepts using varied component types (not just repeating the same quiz).

### Generate review session (when needed)

When concepts are fading or it's been a while:

```bash
uv run .agents/skills/interactive-learner/scripts/progress.py review <course>
```

This outputs concepts due for review. Build a review session that mixes these concepts into fresh contexts and varied exercise types.

### View student dashboard

```bash
uv run .agents/skills/interactive-learner/scripts/build-dashboard.py --open
```

Options: `--progress <path>` (custom progress file), `--output <path>` (custom output path).

## Lesson JSON Structure

Each session produces two JSON files: an **explainer** (content-only) and a **test** (scored exercises). Open-answer questions (explain-back, roleplay, open-reflection) are asked by the agent in conversation between the two phases.

### Explainer JSON (`--mode explainer`)

```json
{
  "course_name": "Kubernetes",
  "title": "Why Does Kubernetes Exist?",
  "subtitle": "The problem before the solution",
  "session": 1,
  "estimated_minutes": 12,
  "xp_start": 0,
  "concepts": ["container-orchestration", "scaling-problem", "self-healing"],
  "sections": [
    {
      "type": "story-card",
      "variant": "blue",
      "label": "The Problem",
      "content": "<p>Imagine you're running 50 containers...</p>"
    },
    { "type": "vocab-cards", "terms": [{ "term": "Pod", "icon": "🫛", "definition": "...", "analogy": "..." }] },
    { "type": "video-embed", "youtube_id": "dQw4w9WgXcQ", "title": "Watch This", "intro": "Quick overview." },
    {
      "type": "side-by-side",
      "title": "Docker Alone vs With Kubernetes",
      "left": { "header": "Docker Alone", "icon": "🐳", "items": ["You manage everything", "Manual restarts"] },
      "right": { "header": "With Kubernetes", "icon": "☸️", "items": ["Automated management", "Self-healing"] }
    },
    {
      "type": "real-world-mission",
      "mission": "Open play-with-k8s.com and run: kubectl get nodes. How many nodes do you see?",
      "url": "https://labs.play-with-k8s.com/",
      "context": "This is a free Kubernetes playground — no install needed.",
      "followup": "We'll discuss what you found at the start of next session."
    }
  ]
}
```

### Test JSON (`--mode test`)

```json
{
  "course_name": "Kubernetes",
  "title": "Session 1 Test",
  "subtitle": "Container orchestration basics",
  "session": 1,
  "xp_start": 0,
  "sections": [
    {
      "type": "quiz",
      "questions": [
        {
          "question": "What happens when a container crashes in plain Docker?",
          "options": ["It auto-restarts", "Nothing — it stays dead", "Docker alerts Kubernetes", "The host reboots"],
          "correct": 1,
          "feedback_correct": "Exactly — without orchestration, crashed containers stay down.",
          "feedback_wrong": "Not quite. Without an orchestrator, Docker won't auto-restart crashed containers."
        }
      ]
    },
    {
      "type": "matching",
      "title": "Match Terms",
      "pairs": [
        { "term": "Pod", "definition": "Smallest deployable unit in Kubernetes" },
        { "term": "Node", "definition": "A machine in the cluster" }
      ],
      "right_order": [1, 0]
    },
    {
      "type": "score-summary",
      "learned": ["Why container orchestration exists", "Pod and Node basics"],
      "next_preview": "Next: what Kubernetes actually does about these problems."
    }
  ]
}
```

## Available Components

### Explainer phase (content-only, `--mode explainer`)

`story-card` `vocab-cards` `side-by-side` `video-embed` `timeline` `concept-map` `mind-map` `kanban-board` `radar-profile` `recommended-deep-dive` *(include at end of every explainer)* `debug-challenge` `simulator` `real-world-mission` `community-challenge` `custom`

### Test phase (scored, `--mode test`)

`quiz` `matching` `fill-blanks` `sorting-game` `score-summary` `custom`

### Conversational (asked by agent in chat, not in HTML)

`explain-back` `roleplay` `open-reflection` — these are handled in the conversational checkpoint (Step 5), not rendered into HTML.

### Escape hatch

`custom` — allowed in both phases. When no template fits, invent something new.

Full JSON schemas and usage guidance: [component-catalog.md](references/component-catalog.md)

## Finding Videos

```bash
uv run .agents/skills/interactive-learner/scripts/find-videos.py "topic for beginners"
```

> The video search script scrapes YouTube HTML and may break when YouTube changes their page structure. If it fails, ask the user to search YouTube manually and paste the URL.

Max 2 embedded videos per lesson. But you CAN recommend additional videos/resources via `recommended-deep-dive` components — these are optional extras, not required viewing.

## Core Rules

1. **Research first.** Never teach from assumptions. Find authoritative, recent sources.
2. **Bridge from known knowledge.** Read the student profile. Connect every new concept to something they already understand.
3. **Explain, then discuss, then test.** The explainer HTML teaches. The conversation checks understanding and fills gaps. The test HTML assesses. This flow is structurally enforced by `--mode explainer` and `--mode test`.
4. **Mostly click-based tests.** Test exercises should be click/drag/select. Open-ended assessment happens in conversation (Step 5), not in HTML.
5. **Conversational teach-back is powerful.** Use the checkpoint between explainer and test to ask 1 teach-back question, discuss confusion, and verify readiness. This replaces the old in-HTML open-answer textareas.
6. **Max 6 new terms per session.** Each needs an analogy bridging to what the student knows.
7. **50% practice, 30% content, 20% assessment** — but treat this as a guideline, not a straitjacket. Some sessions are exploration-heavy, some are drill-heavy.
8. **Design content first, then choose components.** Outline what you want to teach and how you'd explain it conversationally. Then map each piece to the best component. If three story-cards in a row is the clearest way to teach something, that's fine. Vary components when it serves comprehension, not for variety's sake.
9. **Always end tests with score-summary.**
10. **Be adventurous.** Send students to real websites, sandboxes, and tools. Recommend books, talks, and articles. Ask them to draw something and share it. Suggest they explain a concept to a friend. The lesson HTML is the core, but learning extends beyond it.
11. **Achievements are dynamic.** Don't use a fixed list. Generate achievements that match the specific course, topic, and student milestones. See [gamification.md](references/gamification.md).
12. **Every interaction earns data.** Track concept mastery, not just session scores. Feed this into future sessions.

## Anti-patterns

See [sharp-edges.md](references/sharp-edges.md) — updated with guidance on when open answers help vs hurt, and new anti-patterns around research shortcuts and stale content.

## Gamification

See [gamification.md](references/gamification.md) — dynamic achievements, XP, streaks, and the memory garden concept.
