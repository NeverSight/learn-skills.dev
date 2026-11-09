---
name: ship-plan
description: Takes an approved plan from implementation to an open pull request with nobody watching. Picks the depth of the run from the change's size, routes each step to a model, taste tests the build like a user against the repo's committed fixture, reviews it, has a falsifier argue against each finding, fixes what's proven in one round, opens the merge request, and reports back. Never merges. Use after approve-plan hands over a plan to finish unattended, or when the user says "ship this plan".
argument-hint: "<absolute path to .plans/task> [micro|simple|phased]"
---

# Ship plan

You run unattended: nobody answers questions. Never stop to ask. When something needs a decision, take the option closest to the plan's intent and keep going. If that changes something the user approved (what the feature does, its scope, an acceptance criterion, a Record entry), add a divergence note to `plan.md` saying what you did instead and why. Stop early only when an unrecoverable error blocks all progress; then go straight to **Report back**.

**Arguments:** the plan folder as an absolute path, and the loop to run. The loop comes from `tier.md`; the argument only confirms it.

**Never:** merge, force-push, push to the main line, or touch files outside the repo.

## You orchestrate, helpers do the work

Your context is for decisions, not file contents. Run every step below in a fresh subagent and keep only what it reports back. Use subagents in this checkout: helpers must work in the same worktree, and a separate session would get a different checkout.

- **Each helper gets** the plan folder, the step's skill and arguments, the unattended rule above (never ask; note divergences in `plan.md` and risks in `risks.md`), and what to return: at most ten lines on what it did, what it changed, what failed, and what's left open.
- **You read only** those reports, `tasks.md`, `tier.md`, and `git status`. Don't open source files, diffs or test logs yourself. If a report is unclear, send a helper to find out.
- **One helper call per turn.** The harness takes one subagent call per turn; calls issued in a burst are rejected with "a subagent call is already in progress". Never issue two in one turn, and never retry a rejected call with a different model — issue the next helper on the next turn. If the harness offers a fan-out token, you may spend it to run several at once.
- **Run a step once.** A step that reported is done: never run it again because its report was unclear. Read the report again first; if it is still unclear, send one more helper with a sharper question — not the same step again. If a helper fails, retry it once, with the same model and the same task; if it fails again, do the step yourself and say so in the report.
- **After the context pack exists, you do not explore the repository.** No grep, no cat, no file read of the source tree. If the pack lacks something a step needs, send a helper to fetch it. Your own tool use is for the reports, the plan folder and git.
- **One helper at a time,** since they share the worktree. The only exception is the review step's reviewers, which only read.
- **A helper that has reported is done.** If it's still running (in the background, in a pane, in a session you started), stop it.
- **Helpers may start their own helpers** when their skill says so, like interrogate's reviewers or the phased loop's per-phase agents.
- **If you have no subagent tool,** run the step yourself.

## The tier decides the steps

Read `.plans/<task>/tier.md`. If it is missing, run the **pick-tier** skill in measure mode against the merge base of the branch and the default branch, and write the file.

Read `LOOP:` from `tier.md` too.

- If the argument differs from `LOOP:` and the line has no `(user)` mark, run the `tier.md` loop and add a divergence note to `plan.md`.
- If `tier.md` has no `LOOP:` line (an older plan), run `tier.mjs` in measure mode with `--phases` counted from `tasks.md` (`##` headers, leaving out `Verification` and `Manual checks`), plus `--tier <X>` if the `why:` signal says the tier was declared by the user, and write the line.
- If the tier is raised mid-run, the loop already chosen stays: a finished build is not re-run.
- A tier rewrite keeps every `(user)` line in the Steps list.

The tier is a decision, not a suggestion. Run the steps the tier lists, and no others. Never run a step the tier skipped; never add one the tier skipped without the user asking. A step may escalate the tier (see pick-tier); when it does, the new tier replaces the old one for the rest of the run.

| Tier | Steps |
|---|---|
| **S** | Build (implement, unit test, lint, commit) → push and merge-request link → CI status |
| **M** | Build (the `tier.md` loop, micro for tier M) → context pack → one correctness review → falsify → fix, once → verify → push and merge-request link → CI status |
| **L** | Build → context pack → review (interrogate, blast radius, the repo's own review skill) → falsify → fix, once → simplify and deslop → spec check → verify → **push and merge-request link** → browser walkthrough → CI status |

The merge-request step comes before the optional checks on purpose: a run that hits a usage limit, a sleep or a crash must still leave a branch and a link behind. Anything an optional check finds afterwards is a new commit on the same branch, and it goes to the user.

## Models

Name the model when you spawn a helper. Each line of `tier.md`'s Steps list reads `<step> — <model>[ (mark)]`; use that model for that step, whatever the mark. `tier.md` is the only source of models: this skill holds no defaults. The orchestrator's own model and effort are the `ORCHESTRATOR:` line.

In Claude Code that is the Agent tool's `model` parameter. In another harness it is whatever the equivalent is — a second session with that model, a CLI invocation with a model flag, a cheap-model profile. If the harness cannot pick a model per agent, use one model for the whole run and say so in the report.

## Steps

The model for each step is its line in `tier.md`'s Steps list. A step missing from that list (or listed under Skipped) is not run: checkpoint it as `status: skipped`.

1.  **Build.** A helper runs the loop from `tier.md`: `/<loop>-loop <plan folder>`. For the phased loop, the helper is that loop's orchestrator, so don't tell it to run solo.
    - **When `.plans/<task>/design.md` exists,** the build helper also builds from its Look line, never a new deal. Find `<taste>` as in design-forge §1. Reprint the tokens with `node <taste>/scripts/start.mjs css` (or `brand`) using the recorded ids, and apply any font swap. Pages: a new site copies `<taste>/assets` into the project and follows taste's run step 5 (build) and step 6 (check and look, at most 3 rounds); an existing app maps the `:root` tokens into its own styling and copies no kit. App screens and native: build per `design-forge/modes/app.md`; native captures with the commands in `design-forge/modes/native.md`. Taste output goes to `.plans/<task>/taste/after`. Add `.taste-skill/` to `"$(git rev-parse --git-path info/exclude)"` so it is never committed.
2.  **Context pack.** A helper runs the context-pack skill on the branch and writes `.plans/<task>/context-pack.md`. Every later helper reads that file instead of re-exploring the repository.
3.  **Review.** One reviewer per turn, **correctness first**, then security, then structure, then tests.
    - **Tier M:** the correctness reviewer only. The others run if it reports a critical finding, or if the user asked for them.
    - **Tier L:** all four angles, one per turn, plus check-impact on the branch's diff, plus the repo's own review skill or agent if it has one. If the harness grants a fan-out token, run them at once and save the turns.
    - Every reviewer reads the context pack first and cites it. It must back every finding with proof: a real run that shows it, or a test that fails now and would pass with the fix. Merge their reports and drop duplicates. The must-fix findings are interrogate's **Act on**, a blast-radius risk it confirmed, and a broken written rule of the repo.
4.  **Falsify.** A helper runs falsify on the must-fix findings, with the plan folder and the branch's diff. No proof, no fix: an unproven finding is left open or dismissed.
5.  **Fix, once.** One helper does what falsify ruled (cut, narrow, fix) and fixes the browser walkthrough's broke lines. Each fix comes with a test that fails without it, where a test can show it. A fix that needs a new rule or special case (a branch for one input, a new setting or flag) isn't made: it goes to **Needs your call**, since it often means the design is wrong. There is no second fix round.
6.  **Simplify.** A helper runs the `simplify` skill if you have it, then deslop, on the branch's changes, then runs `test`. *Tier L only.*
7.  **Spec check.** A helper runs gap-analysis on the plan folder, fixes every gap it lists, then runs `check` and `test` until both pass. *Tier L only.*
8.  **Verify.** A helper runs `check` and `test` **once, at the end**, then lints and formats the files that changed, and fixes until everything passes. Do not run the suite after every phase, and do not run it a second time against another ref to count pre-existing failures — that is a whole extra run for no signal. Type check only when the repo's type-check command actually works: check that it exits cleanly first, and if it is broken, say so and skip it.
    - **When `design.md` exists,** the gate also runs: run the Gate line(s) in `design.md`, with the allowances named there. Exit 1 is a FAIL; WARN does not fail; exit 2 means the check could not run: report it as "could not check" with the reason, never skip it silently. A FAIL is fixed here like any failing check. Judge the app gate from the report's `checks` minus the ignored ids in `design-forge/modes/app.md`, not from the exit code. A page FAIL granted by an allowance in `design.md` does not fail the gate.
9.  **Deliver.** A helper delivers the branch as the `DELIVERY:` line of `tier.md` says (see **The delivery step**), using the repo's own tooling if it has any. It returns the link, or `branch <x>, not pushed` for `local`. Then stop every helper still running. **Tier S, M and L.**
10. **Browser walkthrough.** A helper runs the taste-test skill against the plan folder, using the repo's committed fixture. If there is none, skip it and report "no fixture at `<path>` — run `make-fixture` in this repo". Anything still broken goes to **Needs your call**; don't fix it. *Tier L only.*
11. **CI status.** A helper reports the CI state of the branch.
12. **Report back.** You do this one.

## The delivery step

Read `DELIVERY:` in `tier.md` (the mark is not part of the value). A run always works on a new branch, `local` included.

- `pr` — the default, described below.
- `draft-pr` — as `pr`, but open it as a draft: `gh pr create --draft`, `glab mr create --draft`, and on Gitea a title prefixed `WIP: `. In the link-only fallback, say it was not opened as a draft.
- `push` — push the branch and print its link; do not open a pull request. CI status still runs.
- `local` — commit on the branch only: no push, no link. CI status is skipped (it is under Skipped in `tier.md`). The report says `branch <x>, not pushed`.

**The default is GitHub.** `gh pr create` opens the pull request and `gh pr checks --watch` reports CI. When the remote turns out to be something else, detection overrides the default. The default keeps this skill generic: it works on a GitHub repo with no setup, and on any other forge once the platform is detected.

Detect the platform before running any host-specific command:

```sh
git remote -v
curl -s --max-time 5 https://<host>/api/v1/version   # Gitea and Forgejo answer {"version":"..."}
ls .github/workflows .gitea/workflows .gitlab-ci.yml Jenkinsfile 2>/dev/null
```

- **GitHub** — the default, and the answer whenever nothing else matches: `gh pr create` with the description; CI with `gh pr checks --watch`.
- **Gitea or Forgejo** (the version probe answers): the pull request is a *pull request*, not a merge request, and its link has the shape `<repo-url>/pulls/new/<branch>`.
  - `tea` installed → `tea pr create`.
  - no `tea`, but a token in the environment (`GITEA_TOKEN`, `TEA_TOKEN`, or a `gitea-token` file in the plan folder) → open it through the API: `POST <host>/api/v1/repos/<owner>/<repo>/pulls` with `head` (the branch), `base` (the default branch), `title` and `body` (the description).
  - neither → push the branch and print the link for a human to open:
    ```
    <repo-url>/pulls/new/<branch>
    ```
    Say plainly that the human opens it.
  - CI: Gitea Actions → `GET <host>/api/v1/repos/<owner>/<repo>/commits/<ref>/status` with the same token. Without a token the status is not readable: report "CI unknown".
- **GitLab** (`.gitlab-ci.yml` present, or the host answers GitLab's API): `glab mr create` and `glab ci status` when `glab` is installed and authenticated; otherwise push the branch and print `<repo-url>/-/merge_requests/new?merge_request[source_branch]=<branch>`.
- **Jenkins only** (`Jenkinsfile` at the root and no CI config above): push the branch, print the pull-request link, and report CI as "CI unknown — Jenkins runs on push". If the plan folder holds a `ci-url` file, the helper reads that URL's JSON API (with a token from the environment, if one is there) and reports the build status.

**When the platform is not confirmed.** If detection is inconclusive and `gh` fails, push the branch and print the link for the platform that was detected; if nothing was detected, print the GitHub form:

```
<repo-url>/compare/<base>...<branch>
```

and say plainly that the platform was not confirmed, so the human opens the link by hand.

Never install a tool and never create a credential. When a host cannot be automated, degrade to the link and say so.

## Checkpointing

After every step, append to `.plans/<task>/run-state.md`:

```markdown
## <step name>
status: done | failed | skipped
outcome: <one line>
```

On start, read that file and skip every step already marked `done`. A run that was interrupted — by a usage limit, a sleep, a crash — continues from the checkpoint instead of starting over. This is what makes a run survive the kind of death that left the traced run with no pull request.

## The pull request description

Short, so the user reads all of it. Put these at the top, before the repo's usual template:

- **Summary:** what changed, at most 5 bullets.
- **How it was tried:** what the browser walkthrough did and saw, in a few lines, with the pictures it produced, and the commands to try it yourself.
- **When `design.md` exists,** "How it was tried" also has a before/after table: `consistency.mjs` FAIL and WARN counts (page or app filter), and the rubric score for app screens and native. Name screenshots by path under `.plans/<task>/taste/`; attaching images is left to the human.
- **Needs your call:** at most 5 items, worst first. Anything still broken after the walkthrough, checks it couldn't try, fixes held back because they need a new rule, divergences, and open findings worth a look. If there are more, say how many and that they're in the plan folder.

Everything else stays in the plan folder: every divergence note, open and dismissed finding, and the risk list.

## Report back

One line: `<plan name>: <outcome>. CI <green|red|unknown|skipped>. <N> need your call.` (or what stopped you, if you stopped early). The outcome is `pull request <link>` for `pr`, `draft pull request <link>` for `draft-pr`, `pushed <link>` for `push`, and `branch <x>, not pushed` for `local`.

End your final message with that line. It is the only thing the user needs to read; the findings, the risks and the divergences stay in the plan folder.
