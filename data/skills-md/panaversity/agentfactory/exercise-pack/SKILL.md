---
name: exercise-pack
description: "Design and generate exercise packs for textbook chapters. Supports coding exercises (build/debug, apply/measure) AND business problem-solving exercises (hands-on/design with starter data). Given a chapter number or path, detects audience (beginner/practitioner/developer), analyzes lessons, groups into 5-8 modules, designs exercises (2 per module + 2-3 capstones), generates the exercise repository, lesson file, summary file, and handles quiz renumbering. Use when asked to create exercises for a chapter, e.g., '/exercise-pack ch 4' or '/exercise-pack chapter 6'. Invokes parallel agents for repo generation and lesson writing, then cross-references outputs."
---

# Exercise Pack Factory

Create complete exercise packs for textbook chapters: analyze lessons, design exercises, generate GitHub repo + lesson file + summary, handle quiz renumbering.

## Input

Chapter number or path. Examples:

- `/exercise-pack ch 4`
- `/exercise-pack "chapter 6"`
- `/exercise-pack apps/learn-app/docs/01-General-Agents-Foundations/05-spec-driven-development/`

## Workflow Overview

```
Phase 1: Chapter Analysis .............. team-lead (you)
Phase 2: Exercise Design ............... team-lead (you) → USER APPROVAL
Phase 3: Repository Generation ......... exercise-generator agent
Phase 4: Lesson + Summary Generation ... lesson-writer agent
Phase 5: Cross-Reference Verification .. team-lead (you)
Phase 6: GitHub Push ................... team-lead (you)
Phase 7: Commit to Textbook ............ team-lead (you)
```

---

## Phase 1: Chapter Analysis

### 1A. Resolve the chapter path

```bash
# For "ch 5" → find chapter:
ls -d apps/learn-app/docs/*/05-*/

# Count existing lessons:
ls apps/learn-app/docs/[part]/[chapter]/*.md | wc -l
```

### 1B. Read chapter content

- Read the chapter `README.md` for overview, lesson list, pedagogical layer
- Read ALL lesson files (use Explore agent for efficiency on large chapters)
- For each lesson, note: core concepts, skills taught, hands-on activities

### 1C. Group lessons into modules

Group lessons into **5-8 modules** based on thematic coherence:

- Each module covers 1-3 lessons
- Module titles should name the transferable skill, not just the topic
- Modules progress from foundational to advanced
- Module N (last) is always "Capstone Projects"

### 1D. Determine audience

Check the chapter's pedagogical layer and target reader:

| Signal                                | Audience                | Exercise Language                                      |
| ------------------------------------- | ----------------------- | ------------------------------------------------------ |
| Part 1-2, "no prior coding" in README | **Beginner / Business** | Business scenarios, professional domains, zero code    |
| Part 3-4, tools/methodology chapters  | **Practitioner**        | Tool workflows, configuration, methodology application |
| Part 5-6, advanced engineering        | **Developer**           | Code projects, debugging, architecture                 |

**The audience determines everything**: scenario language, starter file types, rubric criteria, and which exercise pattern to use. Getting this wrong produces exercises students cannot relate to.

### 1E. Choose exercise pattern

Determine exercise type based on chapter content AND audience:

| Chapter Type                                | X.1 Pattern                | X.2 Pattern                              | Examples             |
| ------------------------------------------- | -------------------------- | ---------------------------------------- | -------------------- |
| **Conceptual** (principles, theory)         | Guided (apply principle)   | Discovery (diagnose violation)           | Ch6 Principles       |
| **Technical** (tools, plugins)              | Build (create/configure)   | Debug (fix broken setup)                 | Ch3 Plugins          |
| **Engineering** (methodology, workflow)     | Apply (use methodology)    | Measure (evaluate quality)               | Ch4 Context, Ch5 SDD |
| **Applied/Business** (beginner, non-coding) | Hands-on (solve with tool) | Design (architect workflow on paper, $0) | Ch3 Agent Teams      |

#### Applied/Business Pattern Details

When the audience is beginners or the chapter teaches tool usage for general problem-solving (not coding):

**X.1 = Hands-on**: Student runs a real multi-step workflow with provided business data. Focus on the tool capability, not code.

**X.2 = Design**: Student architects the workflow on paper — team structures, dependency graphs, communication protocols. **Zero API cost.** This builds strategic thinking before spending tokens.

**Budget-friendly path**: Design exercises (X.2) always come free. Document this path explicitly:

> Complete all design exercises first (1.2, 2.2, 3.2, 4.2), then selectively run hands-on exercises.

**Domain rotation**: Rotate exercises across professional domains so students see breadth:

| Domain                    | Scenario Examples                                        | Starter File Types                                                  |
| ------------------------- | -------------------------------------------------------- | ------------------------------------------------------------------- |
| **Knowledge Work**        | Market research, competitive analysis, literature review | CSVs (50-100 rows), competitor profiles (.md), analysis briefs      |
| **Corporate**             | Event planning, QBR prep, hiring pipelines, compliance   | Budget CSVs, venue/vendor lists, guest lists, requirements docs     |
| **Entrepreneurship**      | Feature prioritization, pitch decks, go-to-market        | Survey CSVs (100+ responses), revenue projections, effort estimates |
| **Freelancer/Consultant** | Proposal writing, deliverable review, client management  | RFPs, capability docs, reference proposals, approval checklists     |

Each module should use a **different domain**. The capstones can mix domains or let students choose their own.

**Rubric criteria for Applied/Business** (replaces technical accuracy criteria):

| Criteria          | What It Measures                                             |
| ----------------- | ------------------------------------------------------------ |
| Comprehensiveness | Did the analysis cover all required angles?                  |
| Actionability     | Could someone act on these recommendations?                  |
| Evidence Quality  | Are conclusions backed by data from starter files?           |
| Team Coordination | Did agents effectively share and build on each other's work? |

### 1F. Determine lesson placement

- Where in the lesson order does the exercise lesson go?
- Typically: after the last lesson whose concepts are exercised, before the quiz
- Count existing lessons to know the current numbering

### Output: Exercise Plan

```
Chapter: [N] [Name]
Path: apps/learn-app/docs/[part]/[chapter]/
Audience: [Beginner/Business | Practitioner | Developer]
Exercise type: [Conceptual | Technical | Engineering | Applied/Business]
X.1 pattern: [Guided | Build | Apply | Hands-on]
X.2 pattern: [Discovery | Debug | Measure | Design ($0)]
Domain rotation: [if Applied/Business: list domain per module]
Repo name: claude-code-[topic]-exercises
ZIP name: [topic]-exercises
Lesson position: L[NN] (before quiz)
Modules: [list of 5-8 module titles with lesson coverage]
Quiz file: [current quiz filename] → [new quiz filename after renumber]
```

---

## Phase 2: Exercise Design

### 2A. Design exercises (2 per module)

For each module (except capstones):

**Exercise X.1** (the X.1 pattern from above):

- Title, scenario description, learning objective
- Starter files needed (data, templates, broken configs)
- What the student does

**Exercise X.2** (the X.2 pattern from above):

- Title, scenario description, learning objective
- Starter files needed
- What the student investigates/measures/discovers

### 2B. Design capstones (2-3)

Capstones synthesize multiple modules:

| Capstone | Pattern              | Description                                        |
| -------- | -------------------- | -------------------------------------------------- |
| **A**    | Integration          | Combine 3+ module skills in one project            |
| **B**    | Real-world           | Apply to a realistic professional scenario         |
| **C**    | Forensics / Personal | Diagnose a complex failure OR apply to own project |

### 2C. Present design to user for approval

**STOP HERE.** Present the complete exercise design as a table:

```markdown
## Exercise Design: [Chapter Name]

### Modules and Exercises

| Module | Title   | Covers Lessons | Exercise X.1         | Exercise X.2         |
| ------ | ------- | -------------- | -------------------- | -------------------- |
| 1      | [title] | L01-L02        | [title + 1 sentence] | [title + 1 sentence] |
| 2      | [title] | L03            | [title + 1 sentence] | [title + 1 sentence] |
| ...    | ...     | ...            | ...                  | ...                  |

### Capstones

| Capstone | Title   | Pattern            | Description     |
| -------- | ------- | ------------------ | --------------- |
| A        | [title] | Integration        | [1-2 sentences] |
| B        | [title] | Real-world         | [1-2 sentences] |
| C        | [title] | Forensics/Personal | [1-2 sentences] |

### Exercise Metrics

- Modules: [N]
- Exercises: [N] (N modules x 2 + N capstones)
- Estimated lesson length: ~550-600 lines
- Estimated EXERCISE-GUIDE length: ~500 lines

**Does this design look right? Any modules to merge, split, or rename?**
```

**Wait for user approval before proceeding to Phase 3.**

---

## Phase 3: Repository Generation

Dispatch an **exercise-generator** agent with Task tool. The prompt must include:

### Agent prompt structure

```
Create the complete exercise repository for [chapter] exercises.

## Repository: claude-code-[topic]-exercises

### Directory Structure
[Complete tree showing every module folder, every exercise folder, every file]

### .github/workflows/release.yml
[Exact YAML — use template from references/github-setup.md]

### EXERCISE-GUIDE.md
[Full outline with every module, every exercise description, framework, rubric]

### README.md
[Package structure, getting started, recommended order]

### Per-exercise INSTRUCTIONS.md
[For EACH exercise: exact filename, title, sections, starter file descriptions]

### Starter Files
[For EACH exercise that needs them: exact filenames, realistic content descriptions]

## Constraints
- Use FAKE-xxx-for-exercise for any tokens/keys (NEVER real patterns like xoxb-, sk-proj-, ghp_, gho_)
- Every INSTRUCTIONS.md follows the exercise-standard template
- Exercises completable in 15-45 minutes each (capstones 2-4 hours)
- No solutions embedded — students discover outcomes

Execute autonomously without confirmation.
Output path: /absolute/path/to/claude-code-[topic]-exercises/
```

### Key structural rules for the repo

```
claude-code-[topic]-exercises/
+-- .github/workflows/release.yml
+-- EXERCISE-GUIDE.md            (~500 lines)
+-- README.md
+-- module-1[-optional-slug]/
|   +-- exercise-1.1-slug/
|   |   +-- INSTRUCTIONS.md
|   |   +-- [starter files]
|   +-- exercise-1.2-slug/
|       +-- INSTRUCTIONS.md
|       +-- [starter files]
+-- module-2[-optional-slug]/ ...
+-- module-N[-optional-slug]/    (last module = capstones)
    +-- capstone-A-slug/
    +-- capstone-B-slug/
    +-- capstone-C-slug/
```

### Module naming decision

- Pedagogical progression (skills grow across modules) -> slugged names: `module-1-understanding-specs/`
- Topic categories (modules are independent topics) -> bare numbers: `module-1/`

### INSTRUCTIONS.md template

```markdown
# Exercise X.Y -- Title

**[Chapter-specific layer]: [technique]** -- [one-line description]

## Goal

[What students will accomplish]

## What You Have

[Files provided in this exercise folder]

## Your Tasks

### Step 1

[Clear, actionable step]

### Step 2

[Clear, actionable step]
...

## Scoring

[Reference the assessment rubric — list 4-5 criteria and target score]

## Expected Results

[What "done" looks like — concrete deliverables]

## Reflection

1. [Question about what they learned]
2. [Question about process quality]
3. [Question about generalization]
```

#### Applied/Business INSTRUCTIONS.md additions

For Applied/Business exercises, INSTRUCTIONS.md must also include:

- **Scoring section**: Reference the 4-criteria rubric (Comprehensiveness, Actionability, Evidence Quality, Team Coordination) with target score
- **Expected Results section**: Concrete deliverable description ("a prioritized feature list with data-backed justifications")
- **Tool note**: "Works in Claude Code" (and "and Cowork" only if the exercise doesn't require terminal-only features like Agent Teams)
- **Starter Prompt + Better Prompt**: For early modules only (1-2), show progression from vague to specific prompts. Later modules omit starter prompts.

### EXERCISE-GUIDE.md template (~500 lines)

```markdown
# [Title] -- Practice Exercises

**[Subtitle/tagline]**

_By Panaversity -- [Mission phrase]_

---

## How This Guide Works

[3-4 paragraphs: exercise pattern, core skills, tool guide]

---

## [Framework Name]

[5-7 step framework appropriate to chapter domain]

---

## Module 1: [Title]

> **Core Skill:** [One sentence]

### Exercise 1.1 -- [Title]

**The Problem:** [2-3 sentences]
**Your Task:** [numbered list]
**What You'll Learn:**

- [transferable insight 1]
- [transferable insight 2]
- [transferable insight 3]

**Reflection Questions:**

1. [question]
2. [question]
3. [question]

---

[Repeat for all exercises...]

---

## Module N: Capstone Projects

> **Choose one (or more). This is where everything comes together.**

### Capstone A -- [Title]

[Full description]

---

## Assessment Rubric

| Criteria      | Beginner (1) | Developing (2) | Proficient (3) | Advanced (4) |
| ------------- | :----------: | :------------: | :------------: | :----------: |
| [criterion 1] |     ...      |      ...       |      ...       |     ...      |
| [criterion 2] |     ...      |      ...       |      ...       |     ...      |
| [criterion 3] |     ...      |      ...       |      ...       |     ...      |
| [criterion 4] |     ...      |      ...       |      ...       |     ...      |
| [criterion 5] |     ...      |      ...       |      ...       |     ...      |

---

_Built for Panaversity's AI-Native Development Curriculum._
```

### release.yml template

```yaml
name: Release Exercise Pack
on:
  push:
    branches: [main]
jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Create ZIP
        run: zip -r [topic]-exercises.zip . -x '.github/*' '.git/*'
      - name: Create Release
        uses: softprops/action-gh-release@v2
        with:
          tag_name: latest
          files: [topic]-exercises.zip
          make_latest: true
```

---

## Phase 4: Lesson + Summary Generation

Dispatch a **lesson-writer** agent with Task tool. Run in parallel with Phase 3.

### Agent prompt structure

````
Create the exercise lesson file and summary for [chapter] exercises.

## Lesson File: [NN]-[topic]-exercises.md

### YAML Frontmatter
[Complete frontmatter using lesson-template.md pattern — include all fields:
sidebar_position, chapter, lesson, duration_minutes, primary_layer,
layer_progression, skills (3), learning_objectives (3),
cognitive_load, differentiation]

### Skills (3)
1. [skill matching X.1 pattern]: proficiency [A2|B1], bloom [Apply|Analyze]
2. [skill matching X.2 pattern]: proficiency [A2|B1], bloom [Analyze|Evaluate]
3. [skill matching capstone pattern]: proficiency [B1], bloom [Create|Evaluate]

### Learning Objectives (3)
1. Maps to skill 1 — assessed by X.1 exercises
2. Maps to skill 2 — assessed by X.2 exercises
3. Maps to skill 3 — assessed by capstone projects

### Opening Narrative (2-3 paragraphs)
Paragraph 1: Acknowledge what students know from prior lessons. "You understand X..."
Paragraph 2: What these exercises do. Name 3 core skills in bold.
Paragraph 3 (optional): The Big Idea if chapter has a unifying concept.

### Download Section
:::info Download Exercise Files
**[Download [Topic] Exercises (ZIP)](https://github.com/panaversity/claude-code-[topic]-exercises/releases/latest/download/[topic]-exercises.zip)**
After downloading, unzip the file. Each exercise has its own folder with an INSTRUCTIONS.md and any starter files you need.
If the download link doesn't work, visit the [repository releases page](https://github.com/panaversity/claude-code-[topic]-exercises/releases) directly.
:::

### How to Use These Exercises
[5-6 step workflow]

### [Framework Name]
[5-7 steps matching chapter domain — same framework as EXERCISE-GUIDE.md]

### Assessment Rubric
[5 criteria x 4 levels — same rubric as EXERCISE-GUIDE.md]

### Module Walkthroughs (ALL modules, 2 exercises each)

**ExerciseCard Integration:** Each exercise walkthrough MUST include an `<ExerciseCard>` marker
that connects the lesson to the practice environment. Add at the top of the lesson file:

```mdx
import ExerciseCard from '@site/src/components/ExerciseCard';
````

Then for EACH exercise, place the marker immediately before the exercise heading:

```mdx
<ExerciseCard id="X.Y" title="Exercise X.Y -- [Title]" />
```

The `id` must match the exercise numbering (e.g., "1.1", "2.2", "capstone-A").

For EACH exercise include:

- `<ExerciseCard id="X.Y" title="Exercise X.Y -- [Title]" />` (practice marker)
- Title: ### Exercise X.Y -- [Title]
- **The Problem:** [2-4 sentences referencing exercise files]
- **Your Task:** [what to do]
- **What You'll Learn:** [3 bullets — transferable insights]
- Early modules: **Starter Prompt (Intentionally Vague)** + **Better Prompt (Build Toward This)**
- Later modules: fewer/no prompts
- **Reflection Questions:** [3 questions]
- Optional: one of The Twist / The Extension / The Challenge (0-1 per exercise)
- Separator: ---

### Capstones Section

- Module N heading with "Choose one (or more)" blockquote
- 3 capstones (A, B, C) — no starter prompts, broader scope
- Each has: description, What You'll Learn (3 bullets)

### What's Next

[1 paragraph: summarize skills practiced, preview next lesson(s)]

## Summary File: [NN]-[topic]-exercises.summary.md

3 paragraphs, no headings, no frontmatter:

- P1: What the lesson provides (exercise count, module count, core skills in bold, framework name)
- P2: Module progression (list all modules by name)
- P3: Self-assessment method + what's next

## Quiz Renumber

Read the existing quiz file: [current-quiz-filename].md
Copy it EXACTLY. Only change:

- sidebar_position: [old + 1]
  Write to: [new-quiz-filename].md

Execute autonomously without confirmation.
Output paths:

- Lesson: /absolute/path/to/[NN]-[topic]-exercises.md
- Summary: /absolute/path/to/[NN]-[topic]-exercises.summary.md
- New quiz: /absolute/path/to/[NN+1]-chapter-quiz.md (copy of old quiz with incremented sidebar_position)

````

### Lesson sizing targets

| Component                | Target                                  |
| ------------------------ | --------------------------------------- |
| Total lesson lines       | ~550-600 (up to 860 for large chapters) |
| Opening narrative        | 2-3 paragraphs                          |
| Framework                | 5-7 steps                               |
| Rubric                   | 5 criteria x 4 levels                   |
| Per-exercise walkthrough | ~20-30 lines                            |
| Summary file             | 3 paragraphs, ~5-9 lines                |

---

## Phase 5: Cross-Reference Verification

**This phase is critical.** In 100% of past runs, the lesson-writer and exercise-generator produced mismatched folder names.

### 5A. Extract folder names from both outputs

```bash
# From repo: list actual exercise folder names
ls -d claude-code-[topic]-exercises/module-*/exercise-* claude-code-[topic]-exercises/module-*/capstone-*

# From lesson: extract referenced folder names
grep -oP 'exercise-\d+\.\d+-[\w-]+|capstone-[A-C]-[\w-]+' [NN]-[topic]-exercises.md
````

### 5B. Compare and fix mismatches

For each mismatch:

1. Decide which name is better (usually the repo name, since that is what students see)
2. Update the lesson file to match the repo folder names
3. Verify the fix

### 5C. Verify exercise count

```bash
# Count INSTRUCTIONS.md files in repo
find claude-code-[topic]-exercises/ -name "INSTRUCTIONS.md" | wc -l

# Count exercise headings in lesson
grep -c "^### Exercise\|^### Capstone" [NN]-[topic]-exercises.md
```

These numbers must match.

---

## Phase 6: GitHub Push

### 6A. Initialize and push repo

```bash
cd claude-code-[topic]-exercises/
git init
git add -A
git commit -m "feat: initial exercise pack for Chapter [N]"
gh repo create panaversity/claude-code-[topic]-exercises --public --source=. --push
```

### 6B. Verify

- [ ] Actions tab: workflow ran successfully (green check)
- [ ] Releases tab: `latest` release exists with ZIP attached
- [ ] Download URL works:
  ```
  https://github.com/panaversity/claude-code-[topic]-exercises/releases/latest/download/[topic]-exercises.zip
  ```
- [ ] ZIP extracts correctly, contains all exercise folders
- [ ] ZIP does NOT contain `.github/` or `.git/`
- [ ] INSTRUCTIONS.md count matches expected total

---

## Phase 7: Commit to Textbook

### 7A. Stage files

```bash
# New files
git add [NN]-[topic]-exercises.md
git add [NN]-[topic]-exercises.summary.md
git add [NN+1]-chapter-quiz.md      # new quiz (renumbered)

# Delete old quiz
git rm [old-quiz-filename].md
```

### 7B. Commit

```bash
git commit -m "feat: add [topic] exercises for Chapter [N] with ZIP downloads"
```

---

## Proven Metrics

Reference data from 5 successful runs:

| Pack       | Chapter | Type            | Modules   | Exercises | Repo Files | Lesson Lines | Guide Lines |
| ---------- | ------- | --------------- | --------- | --------- | ---------- | ------------ | ----------- |
| SDD        | Ch5     | Engineering     | 5+cap     | 17        | ~50        | 863          | ~500        |
| Principles | Ch6     | Conceptual      | 7+cap     | 17        | 354        | 566          | 518         |
| Plugins    | Ch3     | Technical       | 7+cap     | 17        | 67         | 580          | 522         |
| Context    | Ch4     | Engineering     | 7+cap     | 17        | ~60        | ~580         | ~500        |
| **Teams**  | **Ch3** | **Applied/Biz** | **4+cap** | **11**    | **~40**    | **402**      | **~400**    |

Typical output: 4-8 modules, 11-17 exercises + 2-3 capstones, ~400-860 line lesson.

**Applied/Business packs tend to be smaller** (fewer modules, shorter lessons) because each exercise requires more substantial starter files (CSVs, briefs, profiles) that take up repo space instead of lesson prose.

---

## Known Issues

1. **Cross-reference mismatches** (100% occurrence rate): Lesson-writer and exercise-generator work independently and produce different folder names. Phase 5 exists specifically to catch and fix this.

2. **GitHub push protection**: Never use real-pattern tokens in exercise files. Always use `FAKE-xxx-for-exercise` format. Patterns that trigger GitHub push protection: `xoxb-`, `sk-proj-`, `ghp_`, `gho_`, `AKIA`, `AIza`.

3. **Quiz renumbering**: Read existing quiz file, copy content exactly, only change `sidebar_position` value (increment by 1). Delete the old quiz file. Do NOT modify quiz questions or structure.

4. **Module naming consistency**: Choose bare numbers OR slugged names at the start and be consistent. Do not mix styles within a single repo.

5. **Token safety in starter files**: If exercises involve API configurations, use obviously fake values:

   ```
   FAKE-api-key-for-exercise
   FAKE-token-for-exercise
   sk-FAKE-not-a-real-key-for-exercise
   ```

6. **Audience mismatch** (Agent Teams incident, 2026-02-11): First run produced coding-focused exercises (Node.js bugs, code review, UUID migrations) for a chapter targeting beginners doing business problem-solving. Root cause: skipped audience detection (Phase 1D). The entire repo had to be regenerated. **Always determine audience before choosing exercise pattern.**

7. **Applied/Business starter file quality**: Business exercises live or die on realistic data. CSVs with 5 rows feel fake. Minimums: market data 50+ rows, survey data 100+ rows, customer reviews 200+ rows, guest lists 80+ rows. Competitor profiles and RFPs should be 1-2 pages each, not stubs.

---

## Reference Documents

These spec documents contain detailed templates and checklists. Load as needed:

- **Exercise folder standard**: `specs/041-consolidated-exercises/exercise-standard.md` -- INSTRUCTIONS.md templates, folder naming, exercise types
- **Lesson template**: `specs/041-consolidated-exercises/lesson-template.md` -- YAML frontmatter, section-by-section template with placeholders
- **GitHub setup**: `specs/041-consolidated-exercises/github-setup.md` -- Workflow YAML, repo creation steps, download URL format
- **Review rubric**: `specs/041-consolidated-exercises/review-rubric.md` -- 69-check quality rubric for final review
- **Master checklist**: `specs/041-consolidated-exercises/chapter-exercise-checklist.md` -- End-to-end phase checklist
