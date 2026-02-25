---
name: commit
description: Detect the repo's commit convention (Conventional Commits, Gitmoji, or a custom template) and create commits. Use when asked to commit, write a commit message, stage and commit changes, or commit and push work.
---

# Commit

Follow the repo's existing convention, create the commit, verify, and push when requested.
Use the reference docs for detailed rules.

## Workflow

1. Identify the convention
   - Read agent guidance first: `AGENTS.md`, `CLAUDE.md`, etc.
   - Check repo guidance or templates if present: `CONTRIBUTING.md`, `README.md`, commit templates, etc.
   - Scan history: `git log -n 50 --pretty=%s`
   - Choose exactly one: Conventional Commits, Gitmoji, or Custom.
   - If ambiguous, pause and ask using the user input guidance below.
   - Never invent new commit types or emoji codes.

2. Pull if requested
   - If `--pull` is set, run `git pull` before reviewing changes.
   - If conflicts occur, try to resolve them. If you cannot, pause and ask using the user input guidance below.

3. Review changes
   - `git status -sb`
   - `git diff --stat`
   - `git diff` (or `git diff --staged`)
   - Split unrelated changes into separate commits.

4. Stage intentionally
   - Prefer `git add -p` or `git add <files>`
   - Do not stage secrets or large generated artifacts unless explicitly requested.

5. Run verify steps
   - If the repo has tests, lint, or format checks, run them before committing.
   - Only proceed if they pass, unless the user requests `--no-verify`.
   - If checks fail, try to resolve them. If you cannot, pause and ask using the user input guidance below.

6. Compose the message
   - If a convention is identified, you MUST open the matching reference and follow its rules before composing the message.
   - Conventional Commits: follow `references/conventional-commits.md`.
   - Gitmoji: follow `references/gitmoji.md`.
   - Custom template: follow the exact pattern from history or the template file.
   - Use a body and trailers when needed (blank line before body, wrap at 72 chars).

7. Commit, inspect, and push
   - ALWAYS run the commit through the guard script (do not use `git commit` directly):
     - Resolve `{baseDir}` (the installed skill root) before running:
       - Check project-scoped installs first: `./.claude/skills/commit`, `./.codex/skills/commit`, `./.opencode/skills/commit`
       - Then check user-scoped installs: `~/.claude/skills/commit`, `~/.codex/skills/commit`, `~/.opencode/skills/commit`
     - Use `{baseDir}/scripts/commit-guard.py`:
       - `python {baseDir}/scripts/commit-guard.py --convention <conventional|gitmoji|custom> --message "subject"`
       - `python {baseDir}/scripts/commit-guard.py --convention <conventional|gitmoji|custom> --file <path>`
     - If `{baseDir}` cannot be found, pause and ask the user for the exact skill install path.
   - `git log -1 --format="%h %s"`
   - `git show --stat`
   - If `--push` is set, push to the current branch after commit.
   - If push fails, pause and ask using the user input guidance below.

## Commit guard script

Use the guard script to validate and create commits.
Run `python {baseDir}/scripts/commit-guard.py --help` for full usage (after resolving `{baseDir}`).

- `--convention` (required): `conventional`, `gitmoji`, or `custom`
- `--message` (required unless `--file`): commit message string
- `--file` (required unless `--message`): path to commit message file
- `--dry-run` (optional): validate only; do not run git commit

## User input guidance

If you cannot proceed, pause and ask. Examples include: ambiguous convention, unresolved conflicts, failed checks, or a failed push.

- Summarize the current state and what you attempted.
- Offer a recommended option and why.
- List alternative options the user can choose.

## Options

These options can be expressed in natural language, not just the flag form.
Honor the user's explicit request even if it does not use `--flag` syntax.

- `--dry-run`: analyze changes and recommend a commit message, but do not commit or push
- `--no-verify`: skip tests, lint, and format checks even if they exist
- `--pull`: run `git pull` before reviewing changes; attempt conflict resolution
- `--push`: push to the current branch after commit

## Important Rules

- **ALWAYS** identify the repo convention and follow it over defaults.
- **ALWAYS** open the matching reference and follow its rules before composing the message.
- **ALWAYS** run verify steps if they exist, unless the user requests `--no-verify`.
- **ALWAYS** use `scripts/commit-guard.py` to create commits.
- **ALWAYS** summarize state and propose options when you need user input.
- **NEVER** invent new commit types or emoji codes.
- **NEVER** stage secrets or large generated artifacts unless explicitly requested.
- **NEVER** run `git commit` directly.
- **NEVER** push unless the user explicitly requests a push (via `--push` or natural language).
- **NEVER** compose a commit message without checking the matching reference.

## References

- `references/conventional-commits.md`
- `references/gitmoji.md`
