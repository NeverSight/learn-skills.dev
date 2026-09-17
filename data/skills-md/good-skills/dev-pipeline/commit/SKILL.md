---
name: commit
description: >-
  One git commit, repo-style message. Token-minimal inspect (stat-first, scoped
  diff). /commit or explicit commit ask. No push unless user also asks.
disable-model-invocation: true
version: 1.2.0
---

# Commit

`/commit`, `/commit <hint>`, or explicit commit ask → run **immediately**. One commit; no push unless the user also asks.
When called with `/commit --help` or `-h`, display usage, safety rules, inspect order, and message scope guidance.

**Safety:** Follow user git commit rules when present. Also: no git config changes, no skip hooks, no push, no `-i`, exclude secrets (`.env`, keys, credentials).

## Inspect (strict order — saves tokens)

Do **not** run full-repo `git diff` by default.

1. `git status -sb` — if nothing to commit, stop.
2. **Session reuse** — if this turn or the prior turn already knows scope (task prompt, files you edited, user-listed paths), use that; skip re-reading large diffs.
3. `git diff --stat` and `git diff --cached --stat` — pick paths to include/exclude.
4. **Scoped diff only** — `git diff -- <paths>` / `git diff --cached -- <paths>` for staged/unstaged paths you will commit. Full `git diff` only when ≤15 changed files **and** stat lines look small; otherwise stay scoped.
5. `git log -3 --format='%s'` — style only (prefix, scope, length); not 8+ commits.
6. **Task id** (optional): user hint → conversation handoff path → only then queue/`TASK-QUEUE.md`. Do not open pipeline docs if id already known.

## Decide scope

- Task-scoped when work was a pipeline task; exclude unrelated dirty files.
- No empty commit. Ambiguous mixed concerns → ask before grouping.

## Message

- 1–2 sentences; **why** over file lists.
- Match `git log` style (`feat:`, `fix:`, `docs:`, …).
- Pipeline work: subject scope e.g. `feat(ASK-01): …` or `fix(TASK-ASK-01-01): …`.
- `/commit <hint>` — use hint only if it fits the diff.

## Stage, commit, verify

```bash
git add <paths>
git commit -m "$(cat <<'EOF'
Message here.

EOF
)"
git status -sb
```

Report: hash + subject, ahead of remote?, task id if used, remaining dirty paths (if any).

## Failures

Hook failed → fix, **new** commit (user amend rules). Secrets → unstage, warn, commit safe subset or stop.

**Out of scope:** PR, push, rebase/merge.

## Version

When `--version` or `-v` is detected as the only meaningful flag, emit the skill version (from the frontmatter) verbatim and stop. Do not inspect, reason, or generate.

