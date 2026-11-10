---
name: init-project-light
description: "Bootstrap a lightweight project with minimal guidance, context, and repository structure. Use when a small non-research project needs durable AI collaboration without the full research or course scaffold. Not for formal research projects; use $init-project-research."
allowed-tools: Bash(mkdir*), Bash(ls*), Bash(touch*), Read, Write, Edit, Glob, Grep, AskUserQuestion
argument-hint: "[no arguments — runs in current directory]"
---

# Init Project Light

> Lightweight project bootstrapper for small projects that do not need a full research-project scaffold.

## When to Use

- Small document collections (proposals, applications, meeting notes)
- One-off or short-lived projects
- Projects without a code pipeline or Overleaf link
- When the user says "set up something light", "quick init", "organise this folder"
- Any project that does not warrant the installation's full research-project initializer

## When NOT to Use — Escalate to a full research-project initializer

- Research papers targeting a journal or conference
- Projects with code, data, or computational pipelines
- Anything that needs Overleaf, git, or a vault atlas entry

---

## Phase 1: Scan

Read everything already in the directory before asking questions.

1. List all files and folders (excluding `.claude/`, `.DS_Store`)
2. Read text files (`.md`, `.tex`, `.bib`, `.txt`) to understand content — respect file size (skip files > 500 lines, note them)
3. Build a mental model: what is this project, what's the main output, who's involved?

**Goal:** Minimise interview questions by inferring answers from existing files.

---

## Phase 2: Interview (2-3 questions max)

Use `the available structured-question mechanism`. Only ask what you couldn't infer from Phase 1.

Pick from these (skip any you can already answer):

1. **What is this project?** — one sentence (e.g., "PhD research proposal for [University]")
2. **What's the main output?** — document, application, collection of notes, etc.
3. **Anyone else involved?** — names and roles if relevant

If Phase 1 gave you enough, confirm your understanding instead of asking:
> "From the files, this looks like [X]. The main output is [Y]. Correct?"

---

## Phase 3: Create CLAUDE.md

Follow the `lean-guidance-files` rule. Include only:

1. **Project overview** — 2-3 sentences from interview/scan
2. **People** — if collaborators/supervisors exist
3. **Directory structure** — compact tree of what exists
4. **Conventions** — only if detectable (e.g., LaTeX compilation, bibliography style)
5. **Key context** — anything a future session needs to know immediately

**Do NOT include:**
- Detailed literature notes or reference lists
- Action items or timelines (those go to vault)
- Anything that duplicates global rules

---

## Phase 4: Organise (suggest, don't force)

Based on what's in the directory, **suggest** lightweight organisation. Present options and wait for approval.

### Standard suggestions

| Folder | When to suggest |
|--------|----------------|
| `to-sort/` | Multiple unsorted documents exist |
| `docs/` | Reference materials, guidelines, or background reading present |
| `archive/` | Old versions or abandoned drafts detected |

### Rules

- Never create more than 2-3 folders — this is a light project
- Never move files without explicit approval
- If the existing structure already makes sense, say so and skip this phase
- If there's a `.claude/settings.local.json`, leave it. If not, create one with standard permissions.

### Standard permissions (`.claude/settings.local.json`)

```json
{
  "permissions": {
    "allow": [
      "Bash(latexmk *)",
      "Bash(ls:*)",
      "Bash(mkdir:*)",
      "Bash(tree:*)",
      "Edit",
      "Glob",
      "Grep",
      "Read",
      "Write"
    ],
    "deny": []
  }
}
```

Only create if missing. Never overwrite existing permissions.

---

## Phase 5: Confirmation

Short report:

```
Set up lightweight project: <name>

Created:
  - CLAUDE.md
  - [any folders created]
  - [.claude/settings.local.json if created]

Skipped (use an installed full research-project initializer if needed later):
  - Git, Overleaf, vault atlas, code scaffold
```

---

## Cross-References

| Skill | Relationship |
|-------|-------------|
| Installed full research-project initializer | Escalate to this for full research projects |
| `update-project-doc` | Run later to refresh CLAUDE.md if the project grows |
