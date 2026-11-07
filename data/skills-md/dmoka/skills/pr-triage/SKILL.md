---
name: pr-triage
description: "Triage open PRs: which need attention first, and why. Read every open pull request in a repo, judge how much of a reviewer's attention each one needs (critical, high, medium, low) from what the change actually does, and order the queue most-attention-first — each judgement pointing at the line that drives it, each PR linked to a full reading tour. Renders one self-contained HTML queue plus JSON for agents. Use when the user asks which PR to review first, what needs attention in the PR queue, has too many open PRs, or mentions PR triage, review backlog, or review priority."
---

# PR triage

A review queue sorted by age or size sends people to the wrong PR first. A
900-line rename is harmless; a one-token change to a price is not. This skill
reads every open PR, decides how heavy each change really is, and orders the
queue so the PRs that need real attention come first. Nobody configures
anything.

It points attention; it never approves. The last PR in the queue still gets
read. Every judgement names the line that drives it, and every PR links to a
reading tour built from the same data, so a reviewer can check the judgement
in one click.

Scripts sit in `scripts/` beside this file (Node ≥ 18, zero dependencies,
`gh` logged in). If you fetched this over HTTP, fetch `scripts/*.mjs` and
the files in `references/` as raw text with `curl -sSL`.

## The loop

1. **Check the logins.** `node scripts/preflight.mjs` prints one row per repo,
   with the install link or login command for each row not `ready`. Never ask
   for a token or run a login; pass the command to the user. Done when a row
   is `ready`; otherwise report BLOCKED with the table.
2. **Compute.** `node scripts/triage.mjs` (add `--repo owner/name` outside
   the repo). For every open PR it writes `.pr-review/tour-<n>.json` — files,
   noise, FACT items, reading order, the author's words — and it writes
   `.pr-review/triage.json` listing them, fetches every PR head once into
   `origin/<head>` for the judges, and renders the unjudged page. No
   model is involved. A repo list gives one queue ([Many repos](#many-repos)).
   Rerunning replaces the reports and pages, judgements included, and removes
   those of PRs that closed — judge after the last run.
   More than 20 open PRs: say how many, and ask before judging them all.
3. **Judge each PR on its own.** For each `tour-<n>.json`, read that PR —
   `gh pr diff <n>`, noise skimmed, surrounding code at the PR head
   (`git fetch origin <head>` then `git show "origin/<head>:<path>"` — never
   `FETCH_HEAD`, which parallel judges overwrite) — and write
   `.pr-review/tour-<n>.notes.json` in the format of
   [references/notes.md](references/notes.md), **with the `attention` block**.
   Then `node scripts/annotate.mjs .pr-review/tour-<n>.json
   .pr-review/tour-<n>.notes.json` — it writes the checked notes into
   `tour-<n>.json` — and fix the notes until it passes.
   **Use one fresh sub-agent per PR when you can**, in parallel, each given
   only the judge brief below. A judge that has read the other PRs grades on
   a curve. Without sub-agents, judge them one by one and judge each on its
   own merits.
4. **Order the queue.** Read every PR's `attention`. Write
   `.pr-review/triage.notes.json`: `{ "summary": "...", "order": [7, 6, ...] }`
   — the `key` of each PR in `triage.json` (many repos: `"dmoka-ticket-bay-7"`),
   most attention first, by level, across all repos. Within a level, apply these in order
   and stop at the first that separates two PRs: irreversible before
   reversible; live code before code nothing calls yet; a PR that conflicts
   with others (`overlaps`) before one that does not; older before newer. The summary is two or three
   sentences on the queue as a whole; use `overlaps` in `triage.json` (files
   two or more PRs change) for conflicts between PRs.
   `node scripts/annotate.mjs .pr-review/triage.json .pr-review/triage.notes.json`
   checks every PR is placed once, judged, and never below a lower level.
5. **Render.** `node scripts/render.mjs .pr-review/triage.json` writes
   `.pr-review/review.html`: one file holding the queue and every tour, with
   a sidebar per tour and instant switching (`#/pr/7`). No server, safe to
   publish as a CI artifact. Look at the queue before you
   report — in a browser if you have one (`python3 -m http.server -d
   .pr-review` when `file://` is blocked; with no browser, open the file with
   headless Chrome `--dump-dom` and check the same). Check: no PR shows "not judged",
   the order matches your notes, and each evidence link opens its tour at
   the right line.
6. **Report** in chat: the path to `review.html`, then the queue — level,
   PR, what happened, why — critical and high in full, the rest as one line
   each.

## Judge brief

Fill in the absolute paths and HEAD_BRANCH (`pr.head` in `tour-N.json`), and
hand this, and nothing else, to each judge:

> Judge pull request #N in the git repo at REPO (run commands there). Read
> SKILL_DIR/references/notes.md and follow it. Read the PR with `gh pr diff N`
> and `gh pr view N`; read surrounding code at the PR head with
> `git show "origin/HEAD_BRANCH:<path>"` — it is already fetched; do not run
> `git fetch`. Never check out a branch — others share this checkout. Skim noise; when
> the author claims something about it ("formatting only"), check the claim
> with any tool you like. Write REPO/.pr-review/tour-N.notes.json, including
> the `attention` block, then run `node SKILL_DIR/scripts/annotate.mjs
> REPO/.pr-review/tour-N.json REPO/.pr-review/tour-N.notes.json`; it copies
> your checked notes into tour-N.json. Fix your notes until it passes. Do not
> touch GitHub or any other file. Reply with your attention block.

Many repos: N is the PR key. The judge reads with the tour's `read.diff`,
`read.show` and `read.grep` (not `gh`, not `origin/...`) and its `intent`.

## Many repos

- **Config:** `~/.config/pr-triage/repos.jsonc` (Windows:
  `%USERPROFILE%\.config\pr-triage\repos.jsonc`), JSON with comments:
  `{ "repos": ["github:<owner>/<repo>", ...] }`. No file: the current repo;
  `--repo` ignores it. `gitlab:`/`azure:` entries: "not supported yet", skipped.
- **Login check** (step 1), per repo: `git` and `gh` installed, logged in, can
  read the repo. Only `ready` repos are triaged; the page lists the rest first.
- **Cache:** `~/.cache/pr-triage/github/<owner>/<repo>`, a partial clone
  (`--filter=blob:none`), no working tree. Each run fetches every open PR head
  into `refs/pr-triage/pr/<n>`, updates the default branch and deletes the
  refs of closed PRs. It never touches your checkouts; a broken one is cloned
  again. Delete it: `node scripts/triage.mjs --clean-cache [github:<owner>/<repo>]`.
- **Keys:** a PR is `<owner>-<repo>-<n>` (`dmoka-ticket-bay-33`) in file
  names, links and the queue order; each card shows its repo.

## Hard rules

- **Judge the change, not its size, title, or author.** Read the diff before
  you judge. A title can hide a change; that is a reason for more attention.
- **No verdicts.** Attention is an order to read in. Never call a PR "safe",
  "LGTM", "fine", "ready to merge", or "nothing to review". The gate refuses
  the common phrasings; the rule covers the rest.
- **Every level above low points at a line**, with a verbatim code fragment
  the gate checks. No line, no judgement.
- **Read-only on GitHub.** Never comment, label, approve, request changes,
  assign, or merge. Outputs live in `.pr-review/`; if neither `.gitignore`
  nor `.git/info/exclude` covers it, suggest adding it.

## What the ranking cannot see

- **Whether the code works.** Nobody ran it. A judge reads; tests run.
- **Everything a reader misses.** Models catch a minority of the issues a
  careful human finds. A low level means "nothing stood out to a reader",
  never "checked".
- **Context outside the repo:** deadlines, who is waiting, what the business
  cares about this week. Say so when it would change the order.
- **Stability.** Two runs can place PRs within a level differently. The
  levels themselves should not move; if they do, the evidence line says why.

## Done means

- `triage.json` passed `annotate.mjs`, and so did every tour's notes.
- `review.html` exists and opens every PR's tour from the queue.
- The chat report gives the queue with levels and reasons, most attention
  first.
- Nothing on GitHub changed.

## Gotchas

- Never `git fetch` into the cache: `triage.mjs` already fetched every head,
  and parallel fetches collide on refs.

The intent map inside each tour, its search order for the author's intent,
and the fresh-session rule are adapted from Matt Pocock's
[`code-review`](https://github.com/mattpocock/skills) skill (MIT).

Last verified: 2026-09-28 with Hermes v0.21.5 (the morning cron job on dmoka/ticket-bay)
