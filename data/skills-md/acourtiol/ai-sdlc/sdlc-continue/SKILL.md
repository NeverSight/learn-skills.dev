---
name: sdlc-continue
description: >-
  Resume an existing intent at its next gate, or work through all open intents
  when the user explicitly asks for an autonomous run. Use for "continue",
  "what is in flight", or "work the queue".
license: MIT
metadata:
  author: acourtiol
  version: "3.0"
---

# sdlc-continue

Find where work stands and take the next step.

## Steps

1. Run `sh <this-skill-dir>/scripts/status.sh` from the product repo root (`<this-skill-dir>` is this skill's installed directory, not the repo). It lists each open intent with tier, status, steps ticked, spec and report state, and the next gate. If `sh` or the script is unavailable, read `intent/*/` yourself.
2. Pick the slug the user named, or the only open one. If several are open and none was named, show the list and ask which.
3. Check the repo agrees with the artifacts (`git status`, the code a ticked step claims to have changed) and resume at the reported next gate by loading that skill: `sdlc-plan`, `sdlc-apply` or `sdlc-verify`.

## Autonomous run

Only when the user asks to work the queue. You orchestrate: you decide order and parallelism, workers build. The user accepts intents (what) and results; you own how and when.

1. **Preflight.** Confirm you can start a fresh worker and a fresh verifier. If not, run the intents one after another in this session, mark tier `critical` ones blocked before building, and say tier `change` results are "not independently reviewed".
2. **Select.** Run `status.sh`. Work `accepted` intents; list `draft` ones and skip them.
3. **Schedule once, cheaply.** From each `## Approach` and its Acceptance find overlap: shared files, contracts, migrations. Overlapping intents, and any two that add migrations, run in sequence, and the later worktree is created only after the earlier one has landed. Independent ones run in parallel, each in `<repo-root>/.worktrees/<slug>` (see `sdlc-apply`); a single intent uses the current checkout. At most 3 at once. Show the schedule in 10 lines or fewer and start.
4. **One worker per intent.** Brief: repo, worktree path, slug, "run `sdlc-apply` through its step 5, then stop. Do not run verify or close and never ask the user: if blocked on a decision return `needs-decision: <question>`." It reads `intent.md`, not a summary from you.
5. **One fresh verifier per finished intent**: repo, worktree path, slug, `reviewed_head`, "run `sdlc-verify`". Do not re-read its diff. Repairs go to a worker holding the findings; the re-review is a delta.
6. **Hard decisions.** At a fork with confidence not high (see `sdlc-plan`: outcome explicit, source supports it, failure modes evidenced, no open assumption), spawn at most 2 read-only research workers, one specific question each, 15-line answers. Decide, record it in `## Approach`. Ask the user only for product direction, authority or an acceptance change.
7. **Land**, one intent at a time. Rebase onto the main branch and fast-forward. If the patch changed, re-verify narrowly; a migration intent reruns its upgrade proof. Copy the worktree's `report.md` into the main checkout's `intent/<slug>/`, then `git worktree remove` and `git branch -d`. Resolve mechanical conflicts; semantic ones go back to a worker. No integration branches.
8. **Bounded.** One repair round per intent; a second failure of the same kind blocks it with the narrow repro. A worker that returns nothing and shows no new commit at your next check is stuck: block that intent and move on. Never loop on wait or status calls; act on completion notices or end the turn. One status line per transition: `slug | phase | verdict`.
9. **Finish** with one table: slug, verdict, landed or not, anything for the user. The user accepts; then close (`sdlc-apply`), all passing intents at once if they say so.

Never push, deploy or take external actions without separate authorization.
