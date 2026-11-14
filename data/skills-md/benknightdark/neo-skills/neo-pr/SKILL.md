---
name: neo-pr
description: >
  Use this skill when the user asks to create, draft, review, format, or generate a Pull
  Request (PR) title and description, specify target or source branches for a repository,
  or convert git branch diffs into concise, high-impact, non-AI-slop PR content.
license: MIT
compatibility: Requires Python 3.10+ (uv or python3) for git-pr-extractor.py, and Node.js for analyze-slop.js validation.
metadata:
  author: Ben Knight Dark
  version: "1.0.0"
  patterns: generator, reviewer, inversion
---

# Neo PR Generator & Refiner

`neo-pr` is an expert skill engineered to generate precise, concise, and non-AI-slop Pull Request (PR) titles and descriptions for Git repositories. It proactively guides the user to clarify repository and branch targets, extracts change histories, and outputs clear, highly structured PR content.

---

## Gotchas

* **Non-existent or Unaligned Branches**: If the specified source or target branch does not exist locally or on remote, prompt the user to run `git fetch` or provide the correct branch name. Do not invent non-existent base branches.
* **Overly Long Diffs and Token Overhead**: If the branch diff spans dozens of files or thousands of lines, inspect `git diff --stat` and commit logs first to gain high-level context instead of loading full diffs at once.
* **De-slop Does Not Mean Removing Technical Substance**: When stripping AI fluff, eliminate throat-clearing openers (e.g., "It is worth noting that...", "This PR aims to..."), but strictly preserve essential context, key logic shifts, breaking changes, and test instructions.

---

## Workflow Checklist

- [ ] **Step 1 — Perceive (Gather Branch & Repository Context)**: Identify the repository path, source branch (`source branch`), and target branch (`target branch`). If unspecified, prompt the user or detect the current Git state.
- [ ] **Step 2 — Reason & Load References (Load Templates & Guidelines)**: Read [pr-template.md](file:///Users/ben/projects/neo-skills/skills/neo-pr/references/pr-template.md) for structural standards and de-slop conventions.
- [ ] **Step 3 — Act: Extract Diff (Fetch Change Record)**: Execute the helper script `git-pr-extractor.py` to retrieve commit logs, file statistics, and diff snippets.
- [ ] **Step 4 — Act: Generate & De-slop (Produce Concise PR Content)**: Write a Conventional Commits title and bulleted PR description while eliminating all AI tells.
- [ ] **Step 5 — Verify (Quality Check)**: Verify that the generated title and description adhere to de-slop standards (optionally run `analyze-slop.js` to score density).

---

## Detailed Guidelines

### Step 1 — Perceive (Gather Branch & Repository Context)

Determine the following core parameters:
1. **Repository Context**: Current working directory or specified GitHub/GitLab workspace.
2. **Source Branch**: Branch containing the new changes (e.g., `feature/user-auth` or current checked-out branch).
3. **Target Branch**: Base branch to merge into (e.g., `main`, `master`, or `develop`).

If the user has not specified branches, ask with a concise prompt:
> "Please specify your **source branch** (e.g., `feature/xxx`) and **target branch** (e.g., `main` or `develop`). If omitted, I will default to PRing the current branch into `main`."

---

### Step 2 — Reason & Load References

Load relevant design documents based on diff scope:
* **PR Structure & Template**: Read `references/pr-template.md` for standard markdown sections.
* **De-slop Rules**: Apply core `neo-stop-slop` principles (active voice, remove filler phrases, focus on objective facts).

---

### Step 3 — Act: Extract Diff (Fetch Change Record)

Run `git-pr-extractor.py` non-interactively in the target repository directory:
```bash
python3 skills/neo-pr/scripts/git-pr-extractor.py --target-branch <target> --source-branch <source>
```

Alternatively, run native Git commands if script execution is unavailable:
```bash
git log <target>..<source> --oneline
git diff <target>..<source> --stat
```

---

### Step 4 — Act: Generate & De-slop (Produce Concise PR Content)

Construct the PR Title and Description based on extracted commit and diff context.

#### 1. PR Title Standard (Conventional Commits)
* Format: `<type>(<scope>): <short summary>`
* Example: `feat(auth): 新增 JWT 驗證與 Token 自動刷新`
* Rules:
  - Do not begin with filler phrases ("This PR implements...", "A commit to...").
  - Keep under 50 characters, imperative mood, direct and actionable.

#### 2. PR Output Standard Structure
The PR output **must strictly be wrapped in a Markdown code block** (i.e. raw Markdown source code ` ```markdown ... ``` `) so that users can easily copy it directly into GitHub/GitLab PR description fields. The content inside the code block must consist exclusively of the following two sections:

````markdown
```markdown
標題：
<Conventional Commits 格式標題>

內容：
- 列點並重點化的說明重要變更內容（包含主要模組/檔案調整、邏輯變更與重大影響）。
```
````

#### 3. Strict De-slop Rules
* ❌ Never use: "It is worth noting that", "Needless to say", "This PR aims to", "In summary", "Clearly".
* ❌ Avoid hyperbolic fluff: "dramatically improves", "seamlessly integrates", "highly robust".
* ⭕ Use concrete facts & metrics: "reduces response latency by 30ms", "fixes NullReferenceException on null payload".

---

### Step 5 — Verify (Quality Check)

1. Ensure no critical modifications are omitted from the generated title or description.
2. Run de-slop score check if `skills/neo-stop-slop/scripts/analyze-slop.js` is available:
   ```bash
   node skills/neo-stop-slop/scripts/analyze-slop.js --input "<generated PR description>" --format json
   ```
   Confirm `slopDensityScore` is **under 0.5%** (Grade **A+**).
