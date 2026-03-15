---
name: project-sync
description: Sync experiment results from the code repo into the paper's daily experiments log (daily_experiments.tex). Use when you have new experiment results to record, want to update the paper with latest numbers, or log experimental findings from an ML research project.
allowed-tools: Read, Write, Edit, Bash, Glob
---

# Project Sync Workflow

Use this workflow when you have new experiment results in the code repo and want to record them in the paper's `daily_experiments.tex`.

This is a **manual, human-triggered** workflow — run it whenever you want to checkpoint results into the paper.

---

## Step 1 — Locate the Project

// turbo
Auto-detect the project structure. Run:

```bash
# Find the git root of the current repo
git rev-parse --show-toplevel 2>/dev/null

# Check if we're in code/ or paper/ and find sibling
ls "$(git rev-parse --show-toplevel)/../"
```

Determine:
- `$CODE_ROOT` — the code repo root
- `$PAPER_ROOT` — the paper repo root (sibling directory)

If both `paper/` and `code/` are not siblings under a common parent, ask the user:
> "Where is the paper repo? Please provide its path."

---

## Step 2 — Gather New Results

Ask the user **in a single message**:

1. **Date**: What date are these experiments? (default: today's date, YYYY-MM-DD)
2. **Short title**: A brief label for this experiment batch (e.g. "Baseline on CIFAR-10", "Ablation: remove attention layer")
3. **Setup**: What method variant / config / dataset was used?
4. **Results**: What are the key numbers? (paste metrics, accuracy, loss, etc.)
5. **Observation**: What do the results mean? What worked, what didn't?
6. **Next**: What follow-up experiment is planned?

Optionally, also check if there are existing result files to pull from:

```bash
# Recent files in experiments/ or outputs/
ls -lt "$CODE_ROOT/experiments/" 2>/dev/null | head -10
ls -lt "$CODE_ROOT/outputs/logs/" 2>/dev/null | head -10
```

If relevant log files exist, read them and pre-fill the answers for the user to confirm.

---

## Step 3 — Preview the Entry

Compose and display the LaTeX entry for the user to review:

```latex
\subsection*{<DATE> — <SHORT TITLE>}
\textbf{Setup:} <setup>\\
\textbf{Result:} <results>\\
\textbf{Observation:} <observation>\\
\textbf{Next:} <next>
```

Ask: **"Does this look correct? Should I add it to the paper?"**

Wait for confirmation.

---

## Step 4 — Insert into daily_experiments.tex

// turbo
Read the current contents of `$PAPER_ROOT/sections/daily_experiments.tex`.

Insert the new entry **at the top** (below the comment header), so the log is in reverse chronological order (newest first).

After inserting, show the user the updated top of the file to confirm it looks right.

---

## Step 5 — Commit to Paper Repo (optional)

Ask: **"要把这条实验记录提交到 paper repo 的 Git 吗？(Y/n)"**

If yes:

```bash
git -C "$PAPER_ROOT" add sections/daily_experiments.tex
git -C "$PAPER_ROOT" commit -m "exp: add <DATE> — <SHORT TITLE>"
```

If no, inform the user the file is saved and can be committed later.

---

## Step 6 — Confirm

Report:

```
Experiment logged:
  Date:   <DATE>
  Title:  <SHORT TITLE>
  File:   <PAPER_ROOT>/sections/daily_experiments.tex

To view all logged experiments:
  cat <PAPER_ROOT>/sections/daily_experiments.tex
```
