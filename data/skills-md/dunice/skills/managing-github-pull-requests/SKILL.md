---
name: managing-github-pull-requests
description: Use when opening, updating, inspecting or re-titling a GitHub pull request from the terminal — running `gh pr create`, `gh pr edit`, `gh pr ready`, adding reviewers, labels or screenshots to an existing PR, or asked to "open a PR", "put this up for review", or "update the PR".
---

# Managing GitHub Pull Requests

## Overview

`gh` is the whole interface — creating, editing, reading, and marking ready all work from the terminal. Two things do not: composing the body, and uploading an image.

**The body is not yours to compose here.** Use `writing-pull-request-descriptions` for the content — its two gates (self-review the diff, check the scope) run *before* any `gh` command. This skill is the mechanics of getting that text onto GitHub.

## Opening a PR

**Every PR is created `--draft` unless the user asked for it ready.** Draft is the default because the author is the last line of review, and a draft does not fire review-request notifications while you are still fixing what you find.

Ready is the *absence* of `--draft` — there is no `--ready` flag on `gh pr create`. To open ready, drop `--draft`; to flip an existing draft, `gh pr ready <n>`.

Ready-for-review requires an explicit ask — "open it ready", "not a draft", "request review from X now". Silence is a draft. An urgent-sounding ticket is not an ask. A CI gate that "only runs on non-draft PRs" is not an ask either — say so and let the user decide.

```bash
# 1. Is there already a PR for this branch? Creating a second one is the common mistake.
gh pr view --json number,state,isDraft,url 2>/dev/null || echo "no PR yet"

# 2. Be current, and read what you are about to ship.
git fetch origin
git diff origin/main...HEAD --stat
git diff origin/main...HEAD          # gate 1 of writing-pull-request-descriptions

# 3. Match the repo's conventions before inventing your own.
cat .github/pull_request_template.md 2>/dev/null
gh pr list --state merged --limit 10 --json number,title --jq '.[] | "\(.number)  \(.title)"'

# 4. Push.
git push -u origin HEAD

# 5. Body to a file, never inline. Then create, as a draft.
gh pr create \
  --draft \
  --base main \
  --title 'BILL-412: rate limit requests per IP' \
  --body-file /tmp/pr-body.md

# 6. Hand back the URL.
gh pr view --json url --jq .url
```

**Body goes in a file.** `--body "..."` runs the markdown through shell quoting: backticks become command substitution, `$` expands, newlines collapse. Write the file (heredoc with a **quoted** delimiter, `<<'EOF'`), then `--body-file`. Same for `gh pr edit`.

Three-dot `origin/main...HEAD` is what the PR will show — the diff against the merge base. Two-dot includes everything that landed on main since you branched.

## Command Reference

Verified against `gh` 2.97.0. `gh pr <cmd> --help` for the rest.

| Task | Command |
|---|---|
| Create as draft | `gh pr create --draft --base main --title '…' --body-file f.md` |
| Fill title/body from commits | `gh pr create --draft --fill` — only when the user asked for it |
| Preview without creating | `gh pr create --dry-run …` |
| Replace the body | `gh pr edit 912 --body-file f.md` |
| Retitle | `gh pr edit 912 --title '…'` |
| Change base | `gh pr edit 912 --base main` |
| Add reviewers | `gh pr edit 912 --add-reviewer amy --add-reviewer raj` |
| Add a team | `gh pr edit 912 --add-reviewer org/frontend` |
| Labels | `gh pr edit 912 --add-label frontend --remove-label wip` |
| Draft → ready | `gh pr ready 912` |
| Ready → draft | `gh pr ready 912 --undo` |
| Read current state | `gh pr view 912 --json number,isDraft,title,body,labels,reviewRequests` |
| Read the existing body | `gh pr view 912 --json body --jq .body > body.md` |
| Review threads | `gh pr view 912 --comments` |
| CI status | `gh pr checks 912` |
| Your open PRs | `gh pr list --author @me --json number,title,isDraft` |
| Open in browser | `gh pr view 912 --web` |

Reviewers are **bare GitHub logins** — `amy`, not `@amy`, which is rejected. Labels must already exist in the repo; `--add-label` fails the whole edit otherwise (`gh label list --search frontend` first, and ask before `gh label create`).

## Editing an Existing PR

```bash
gh pr view 912 --json body --jq .body > /tmp/pr-912-body.bak.md   # keep the old one
git log --oneline origin/redesign-checkout..HEAD                   # must print nothing — else push first
gh pr view 912 --comments                                          # don't contradict the review thread
# rewrite /tmp/pr-912-body.md per writing-pull-request-descriptions
gh pr edit 912 --body-file /tmp/pr-912-body.md
gh pr edit 912 --add-reviewer amy --add-reviewer raj --add-label frontend
gh pr ready 912                                                    # last
```

`gh pr edit --body-file` **replaces** the whole body; it does not append. Read the current body first if any of it survives.

**`gh pr ready` goes last.** It fires the review-request notifications — the body, screenshots and labels should already be in place when they land.

## Screenshots

**`gh` cannot upload an image.** No flag on `gh pr create`, `gh pr edit`, or `gh pr comment` does it, and GitHub's attachment uploader is not in the public REST API. A flag that seems to do it does not exist.

The working path, when the description needs a visual:

```bash
gh pr view 912 --web   # then drag the PNG into the comment box — do NOT submit the comment
```

GitHub replaces the dropped file with `![name](https://github.com/user-attachments/assets/<uuid>)`. Copy those lines out, discard the draft comment, paste them into the body file. Ask the user for the URLs — you cannot read their browser.

Committing PNGs into the repo is the fallback, not the default: it puts binaries in history, and `raw.githubusercontent.com` links render broken for everyone on a private repo.

## Only Claim What You Read

The body describes the diff you actually read in step 2. A header name, a default, a config key, a limitation — if it is not in the diff, it does not go in the PR, however plausible. A reviewer note that turns out to be wrong costs more than no note.

## Rationalizations (verbatim from baseline testing)

| Excuse | Reality |
|---|---|
| "The work is finished, so it's ready for review, not a draft" | Finished is the precondition for opening it at all. Draft vs ready is the user's call, and the default is draft. |
| "The ticket is urgent and the reviewer is waiting" | `gh pr ready` is one command once they say so. Opening ready is not faster, it's just irreversible-ish. |
| "~48 lines across three files strongly implies an in-process Map" | Implication is not reading. Run the diff or leave it out. |
| "I'll write the body in the shape that fits this change" | The shape is already decided by `writing-pull-request-descriptions`. Use it. |
| "`--body` inline is fine, the text is short" | One backtick in a short body is a command substitution. Use `--body-file`. |
| "I'll mark it ready first, then add reviewers and the screenshots" | Ready is the notification. They open a PR with no images and a stale body. |
| "There's a skill for the description but the user just asked for a PR" | Opening a PR includes writing its description. Load it. |

## Red Flags — STOP

- `gh pr create` without `--draft` and the user never said "ready"
- `--body "` followed by markdown
- You are about to run `gh pr create` and have not read `git diff origin/main...HEAD`
- You are writing body sections without having loaded `writing-pull-request-descriptions`
- You are about to claim a flag uploads an image
- `gh pr ready` before the body and reviewers are set
- A statement in the body you cannot point to a diff hunk for

## Not Covered

Body content and structure — `writing-pull-request-descriptions`. Commit messages — `writing-commit-messages`. Merging and branch cleanup are out of scope here.
