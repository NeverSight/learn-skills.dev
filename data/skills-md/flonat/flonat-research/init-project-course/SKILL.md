---
name: init-project-course
description: "Bootstrap a university course or module folder with the canonical teaching structure, guidance, and starter files. Use when creating or migrating a course workspace. Not for checking an existing course without modifying it; use $audit-project-course."
allowed-tools: Bash(mkdir*), Bash(mv*), Bash(ls*), Bash(tree*), Bash(find*), Bash(rm*), Bash(cp*), Read, Write, Edit, Glob, Grep, AskUserQuestion
argument-hint: "[no arguments — runs in current directory]"
---

# Init Project Course

> Bootstrap a university course or module folder into a clean, navigable structure. Designed for taught modules with lectures, workshops, assessments, and optionally recordings.

## When to Use

- University modules with lectures + workshops + assessments
- Course folders that have accumulated files over a term
- When the user says "organise this module", "init course", "set up this module folder"
- Any taught course with recurring weekly components

## When NOT to Use — Escalate

- To `init-project-light` if it's a one-off document collection (no lectures/workshops structure)
- To `init-project-research` if it's a research project that happens to be for a course

---

## Phase 1: Scan

Read everything already in the directory before asking questions.

1. List all files and folders (excluding `.claude/`, `.DS_Store`)
2. Identify content types:
   - **Lecture PDFs** — files matching `Lecture*` or containing "lecture" in name
   - **Seminar materials** — files matching `Seminar*`, `Session*`, or containing "seminar" in name (discussion-based modules use seminars instead of lectures)
   - **Lecture recordings** — video files (`.mp4`, `.mov`, `.mkv`, `.webm`, `.avi`) or folders named `recordings`
   - **Workshop folders** — folders matching `Workshop*`, `Lab*`, `Week*`, or numbered folders with exercise content
   - **Assessment folders** — folders containing "group", "individual", "exam", "coursework", "assignment", "portfolio"
   - **Workshop PDFs** — PDFs inside workshop folders that are NOT lectures (exercise sheets, briefs)
   - **Code projects** — `node_modules/`, `package.json`, `.py`, `.js`, `.ts` files inside workshop folders
   - **Notes** — personal notes, reading lists, exercise solutions (common in student modules)
3. Detect duplicates: lecture PDFs that appear in multiple locations
4. Note workshop numbering gaps (normal — not every week has a workshop)
5. Check for existing organisation (already has `lectures/`, `workshops/`, etc.)

**Goal:** Build a complete inventory so the interview is short.

---

## Phase 2: Interview (4-5 questions max)

Use `the available structured-question mechanism`. Only ask what you couldn't infer from Phase 1.

Pick from these (skip any you can already answer):

1. **What module is this?** — code + name (e.g., "IB9PK Advances in Behavioural Science")
2. **Are you a student or instructor?** — determines template variant (see Phase 3)
3. **Who teaches it?** — name(s) and role(s) (for student modules: instructor name; for instructor modules: module leader if different)
4. **What components exist?** — lectures/seminars, workshops, group work, individual work, exams, recordings
5. **Status?** — still in progress (more content coming) or archived/complete

If Phase 1 gave you enough, confirm your understanding instead of asking:
> "This looks like [module code + name]. You're [student/instructor]. It has [N] workshops, [N] lecture PDFs, and [assessment types]. Still in progress. Correct?"

**Always interview** — even if scan is comprehensive. Course folders affect a full term of work; assumptions are expensive.

---

## Phase 3: Organise

Present the proposed structure and **wait for explicit approval** before moving anything.

Full templates (student + instructor directory structures), workshop naming, lecture/recording/assessment handling rules: [references/organise-templates.md](references/organise-templates.md)

---

## Phase 4: Create CLAUDE.md

Follow the `lean-guidance-files` rule. Include only:

1. **Module overview** — code, name, institution, programme, credits, 1-2 sentence description
2. **People** — instructor(s) and/or student, role
3. **Assessment** — type(s), format, word count/page limit, deadline(s) if known
4. **Directory structure** — compact tree of the organised layout
5. **Conventions** — detectable patterns (LaTeX compilation, GitHub repo naming, submission format)
6. **Status note** — "in progress" or "complete/archived", with note on what's still to come

**Do NOT include:**
- Lecture-by-lecture notes
- Workshop solution details
- Full assessment criteria (those live in `docs/` or `assessments/`)
- Anything that duplicates global rules

---

## Phase 5: Seed MEMORY.md

Create `MEMORY.md` using the appropriate template (student or instructor). Templates, settings.local.json, and vault entry details: [references/memory-and-settings.md](references/memory-and-settings.md)

---

## Phase 6: Settings

Create `.claude/settings.local.json` if missing. Full details: [references/memory-and-settings.md](references/memory-and-settings.md)

---

## Phase 7: Vault Sync

Offer to create entries in the vault tracking for this module (Student or Instructor). Database IDs and field mappings: [references/memory-and-settings.md](references/memory-and-settings.md)

---

## Phase 8: Confirmation

Short report:

```
Set up course project: <module code + name>
Role: Student / Instructor

Created:
  - CLAUDE.md
  - MEMORY.md (seeded with [student/instructor] template)
  - lectures/ or seminars/ (N PDFs, deduplicated from M locations)
  - notes/ (student only, if applicable)
  - recordings/ (if applicable)
  - workshops/ (N workshops, renamed from original folders)
  - assessments/{types}/ (moved from original folders)
  - docs/ (module specification, guidelines)
  - [.claude/settings.local.json if created]
  - [vault entry created in Modules Pipeline (Student/Instructor)]

Workshop naming:
  "Workshop 1 - JavaScript Bootcamp" → workshops/01-javascript-bootcamp
  "Workshop 6" → workshops/06-cwe-vulnerability-analysis
  ...
```

---

## Cross-References

| Skill | Relationship |
|-------|-------------|
| `init-project-light` | For non-course document collections |
| `init-project-research` | For research projects within a course |
| `audit-project-course` | Run later to check the structure is still clean |
| `update-project-doc` | Run later to refresh CLAUDE.md if the module grows |
