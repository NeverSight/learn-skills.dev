---
name: codex-review-cc
description: "Run code review or codebase analysis using OpenAI Codex CLI to get a second-opinion from a different AI model. Use this skill whenever the user wants code reviewed, a second opinion on their changes, codebase analysis, or quality checks — even if they don't mention 'codex' explicitly. Triggers include: code review, review my code, 代码审核, 代码审查, 检查代码, 帮我看看代码, 让 codex 看看, codex 分析, second opinion, 有没有 bug, 看看有没有问题, review PR, review changes, 审查一下."
---

# Codex Code Review Skill (CC Edition)

> Battle-tested edition with CLI pitfall avoidance, network fallback strategy, and real-world case patterns.

This skill delegates analysis to the **Codex CLI**, which is powered by OpenAI's models. The whole point is to get a **second opinion from a different AI** — if you (Claude) do the analysis yourself, the user gets zero additional value.

## Two Modes: Change Review vs Focused Analysis

This skill has two distinct modes. **Determine the mode FIRST before doing anything else.**

| Mode | When to use | Pre-flight (git diff) needed? | Codex command |
|------|-------------|-------------------------------|---------------|
| **变更审查** (Change Review) | User wants to review uncommitted changes, a commit, or a PR | YES — need diff stats | `codex review --uncommitted` |
| **定向审查** (Focused Analysis) | User wants codebase analysis with a specific angle (test quality, architecture, security, feature mapping, etc.) | NO — skip entirely | `codex exec --full-auto "prompt"` |

### How to determine mode

- If user's request is about **changes/diff** (e.g. "review 我的改动", "审一下代码", "看看有没有 bug") → **变更审查**
- If user's request has a **specific analysis focus** unrelated to changes (e.g. "梳理核心功能", "review 测试代码找冗余", "分析架构", "看看安全性") → **定向审查**
- If unclear, use AskUserQuestion:

```
AskUserQuestion:
  question: "选择审查模式："
  header: "Review mode"
  options:
    - label: "变更审查"
      description: "审查当前未提交的代码变更，找 bug、回归、代码质量问题 (codex review)"
    - label: "定向审查"
      description: "针对特定角度分析代码库，比如测试质量、架构梳理、安全性 (codex exec)"
```

If the user's original request already clearly indicates one mode, **skip the question and go directly to the corresponding path.**

---

## CLI Pitfall Guide (Must Read)

| Trap | Wrong | Correct |
|------|-------|---------|
| `-p` flag | `codex -p "review"` (`-p` = `--profile`, NOT prompt) | `codex review --uncommitted` |
| Non-interactive exec | `codex "prompt"` (opens interactive) | `codex exec --full-auto "prompt"` |
| Redundant exec | `codex exec review --uncommitted` | `codex review --uncommitted` (review is already a subcommand) |

**Key rule**: `codex review` is a direct subcommand — no need for `exec` wrapper.

---

## Path A: 变更审查 (Change Review)

For reviewing uncommitted changes, specific commits, or PRs.

### A1. Pre-flight checks

Run in parallel:

```bash
git diff --name-only && git status --short
```

```bash
git diff --stat | tail -1
```

- If there are untracked files (`??` in status), stage them first:
  ```bash
  git ls-files --others --exclude-standard -z | while IFS= read -r -d '' f; do git add -- "$f"; done
  ```
- **Clean working directory** → use `codex review --commit HEAD` instead

### A2. Optionally update CHANGELOG

If the project has a CHANGELOG.md **and** the user's changes are significant, check if it's already in the diff:

```bash
git diff --name-only | grep -iE "changelog"
```

If not updated, suggest adding an entry under `## [Unreleased]`. Skip this step if the project doesn't use a CHANGELOG or the changes are minor.

### A3. Assess difficulty & run

**Difficulty rules (ANY triggers xhigh):**

- Files >= 10
- Total changes (insertions + deletions) >= 500
- Insertions alone >= 300 OR deletions alone >= 300

| Difficulty | Config | Timeout |
|-----------|--------|---------|
| Hard | `model_reasoning_effort=xhigh` | 30 min |
| Normal | `model_reasoning_effort=high` | 10 min |

```bash
codex review --uncommitted --config model_reasoning_effort=high
```

For clean working directories: `codex review --commit HEAD --config ...`

---

## Path B: 定向审查 (Focused Analysis)

For codebase analysis with a specific focus. **NO pre-flight checks needed** — go directly to composing and running the prompt.

### B1. Compose prompt

Build the prompt from three parts:

1. **Objective** — what the user wants analyzed, in their words
2. **Scope** — which files to focus on (derive from user's request)
3. **Output format** — structured findings (P1/P2/P3 for reviews, or custom structure for analysis)

**Prompt template for code quality review:**

```
Review the codebase with this specific focus:

OBJECTIVE: {user's concern}
SCOPE: {file pattern}

INSTRUCTIONS:
- Read the relevant source files to understand the implementation
- Evaluate against the objective
- Be thorough and specific

Report findings as:
- P1 (Critical): ...
- P2 (Important): ...
- P3 (Minor): ...

For each finding: file path, what's wrong, and suggested fix.
```

**Prompt template for architecture/feature analysis:**

```
Analyze the codebase with this focus:

OBJECTIVE: {user's concern, e.g. "Map out all core features and end-to-end user flows"}
SCOPE: {key files to read}

INSTRUCTIONS:
- Read each file listed in scope
- {specific analysis instructions}

Output in {language}. Use structured format with clear headings.
```

Adapt the template to fit the user's actual request.

### B2. Choose effort level

For focused analysis, effort level is based on **scope size** (not diff size):

| Scope | Effort | Timeout |
|-------|--------|---------|
| > 10 files or complex multi-file analysis | `model_reasoning_effort=xhigh` | 30 min |
| <= 10 files or focused single-aspect review | `model_reasoning_effort=high` | 10 min |

### B3. Run

```bash
codex exec --full-auto "YOUR_COMPOSED_PROMPT" --config model_reasoning_effort=high
```

---

## Interpret Output & Act

**Priority levels (for review-type output):**

| Level | Meaning | Action |
|-------|---------|--------|
| **P1** | Bugs, misleading code, data loss risk | Fix immediately |
| **P2** | Quality issues, redundancy, resource leaks | Fix if reasonable, explain if skipping |
| **P3** | Nits, style | Optional |

**Do NOT blindly follow all suggestions.** Evaluate each:

- Is this a real bug or a false positive?
- Does the suggested fix introduce new complexity?
- Is this relevant to the current scope?

**After fixing P1/P2 items:** re-run tests to confirm fixes don't break anything.

---

## Network Stability & Fallback

Codex CLI can fail with `Transport error: network error` during long sessions.

```
IF codex hangs or returns network error:
  1. DO NOT retry more than once
  2. Tell the user codex failed and you're falling back to manual analysis
  3. Read the relevant files yourself and perform the analysis inline
  4. Report findings in the same format
```

Always inform the user which path was taken.

---

## Codex CLI Reference

### Review Mode

```bash
codex review [OPTIONS]
```

| Option | Description |
|--------|-------------|
| `--uncommitted` | Review all uncommitted changes |
| `--base <BRANCH>` | Review changes relative to a base branch |
| `--commit <SHA>` | Review a specific commit |
| `--title <TITLE>` | Optional title for review summary |
| `-c, --config <key=value>` | Override config (e.g., `model_reasoning_effort=xhigh`) |

### Exec Mode (for focused analysis)

```bash
codex exec --full-auto "your prompt here" --config model_reasoning_effort=high
```

**Constraints:**

- `--uncommitted`, `--base`, `--commit` are mutually exclusive
- Must run inside a git repository
