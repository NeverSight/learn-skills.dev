---
name: setup-ci
description: Configures a repository so Accountable Review generates a Review Map automatically in CI — a GitHub Actions workflow that runs when a pull request first becomes reviewable, skips drafts, forks, bots and changes with too little application code to have a reading order, cancels superseded runs, uploads the resulting static HTML as a build artifact the whole team can open, and comments the link on the pull request. Use this when someone wants review maps generated automatically rather than by hand, asks to add Accountable Review to CI or to GitHub Actions, wants the review map shared with their team instead of published from one laptop, or asks how to run this on every PR. Invoke with /accountable-review:setup-ci. It inspects the repository before writing anything, confirms when maps will be generated and what the workflow may do, prefers a dedicated workflow, never modifies unrelated CI, and is safe to run twice. Not for generating a review map — that is review-map — and setup itself posts nothing to GitHub.
---

# Set up CI

Turns "someone runs the review map by hand, sometimes" into "every review-ready pull request has one,
and the whole team can open it."

The result is one workflow file. When a pull request first becomes reviewable, GitHub Actions
generates a Review Map for that exact revision, uploads it as a build artifact, and comments the link
on the pull request so the reviewer finds it where they already are. Drafts cost nothing, and so do
forks and bots, and so does a change with no application code in it or too
little to have a reading order.

**Everything you write here is a file in the repository the user is working in.** This skill posts
nothing itself, enables nothing on GitHub, and creates no secret — the one comment in the picture is
posted by the generated workflow when it runs, not by setup. Where a credential is needed setup says
so and stops short of pretending it is there.

## The one thing not to do

**Do not write a workflow into a repository you have not looked at.** A generic file dropped into
`.github/workflows/` is how this command becomes something a team deletes: it duplicates a job they
already have, ignores a reusable-workflow convention that every other workflow follows, or replaces a
Claude Code integration they set up last month. Step 1 exists because the inspection is the part that
makes the write safe.

The second is smaller and just as damaging: **do not turn this into a wizard.** Running it with no
arguments must produce a good setup. The defaults in § *What it configures* are opinions, and the
user gets them without being asked five questions first.

Step 3's confirmation is not a wizard and must not become one. It shows **one block covering when a
Review Map is generated and what the workflow does to the repository**, and the expected answer is
yes. A user who says nothing has agreed to the defaults; a user who wants one thing different says
which. What turns this into a wizard is asking the questions one at a time, asking about anything
outside that block, or asking again on a re-run that changes nothing.

It exists because those decisions either **spend money on the user's account** or **change what the
job is permitted to do**, and the wrong ones are invisible. A trigger set that regenerates on every
push costs a model run per commit. A bot author list that is wrong spends one on every dependency
bump, or silently skips a contributor whose login looks like a bot's. And the comment step carries
`pull-requests: write`, which is a scope somebody should agree to rather than find. All of that is
worth one block, and none of it is worth a question of its own.

## What is bundled

| File | Read at | For |
|---|---|---|
| `references/workflow.md` | step 3 | What the generated workflow contains, and why each part is the way it is — triggers, the draft guard, concurrency, permissions, checkout depth, the credential |
| `references/config.md` | step 4 | `.accountable-review.yml` — the whole schema, the precedence rule, and when writing one is worth it |
| `references/delivery.md` | step 5, or when asked about anything but artifacts | The delivery abstraction: the contract, the providers that exist, and how a team adds one |
| `scripts/inspect-repo.sh` | step 1 | Reports what the repository already has |
| `scripts/render-workflow.sh` | step 3 | Renders the workflow. Deterministic — same flags, same bytes |
| `scripts/install-workflow.sh` | step 3 | Writes it, idempotently, and refuses to clobber a hand-edited one |
| `scripts/read-config.sh` | step 4 | Reads the config file. Also what the CI scripts use at run time |
| `templates/workflow.yml` | — | The workflow itself. Edit this, not a copy in your head |

Paths are relative to the base directory named at the top of this skill when it loads.
`$CLAUDE_PLUGIN_ROOT` is not set in the shell.

## 1. Look at the repository first

```sh
<skill base directory>/scripts/inspect-repo.sh
```

It prints `key=value` lines and decides nothing. Read them, then **open the files they name** — a
count of workflows is not knowledge of them. What you are looking for:

- **Is this a git repository with a GitHub remote?** `git_repo=no` stops the run: say so plainly and
  offer nothing else. `remote_github=no` is worth naming — the workflow will be written but nothing
  will run it until the repo is on GitHub.
- **Is GitHub Actions already in use, and how?** A repository whose every workflow is three lines
  calling a reusable one from a platform repo has a convention, and a standalone workflow ignoring it
  is the wrong shape even though it works.
- **Is Accountable Review already set up?** `accountable_workflow` names it. That is the idempotent
  path — step 3 handles it, and the answer is often "nothing to do".
- **Is Claude Code already running in CI?** `claude_workflows` and `anthropic_secret_used` together
  tell you whether the credential question is already answered. A repository that already runs
  `claude-code-action` has the secret; say which one you found rather than asking for a new one.
- **Conventions worth preserving.** Workflow naming, whether jobs pin actions by sha, a shared
  `runs-on` label, a `CONTRIBUTING.md` that says how CI is organised. Match them where you can.

## 2. Decide where it goes

**Prefer a dedicated workflow.** `.github/workflows/accountable-review.yml`, doing one thing, easy to
read, easy to delete. It is a separate concern from the test suite: it takes minutes, it costs model
tokens, and it must not become a reason a required check is red.

Integrate into an existing workflow **only when it is obviously cleaner** — and the bar is genuinely
high, because integration means editing a file that other people's work depends on. The case where it
is right: the repository has exactly one pull-request workflow, every job in it is added there by
convention, and adding a file would be the odd one out. Even then, add a **job**, never a step inside
someone else's job, and change nothing else in the file.

Two things settle it against integration on their own: the existing workflow has `permissions:` wider
than `contents: read` (this job must not inherit them), or it has no `concurrency` (a Review Map job
without one wastes tokens on superseded runs, and adding one to a shared workflow changes how their
tests behave).

If you integrate, everything in `references/workflow.md` still applies to the job you add — the same
guard, the same permissions block on the job, the same steps.

## 3. Confirm what the workflow will do

Read `references/workflow.md` now. It explains every part of the file, and you will be asked about
the triggers by the next person who reads it.

Then show the user this, filled in from the defaults, **before writing anything**:

```
Review Maps will be generated when a pull request first becomes reviewable:

  opened ready for review, marked ready, or reopened  ->  a Review Map
  a push to a ready pull request                      ->  nothing; the map is not regenerated

Skipped: drafts, pull requests from forks, dependabot, and trivial changes
         — 2 or fewer application files and 20 or fewer application lines, both.
         Tests, docs, tooling and lockfiles are not counted as application code.
         Both thresholds are yours, in .accountable-review.yml.

When one is generated, the workflow comments the link on the pull request —
one comment, updated in place, naming the revision the map describes.
That is what `pull-requests: write` is for, and it is the only write the
job can do: it cannot push, approve, or set a check.

One thing this costs you, and it is quiet:
  - the map describes the revision that made the PR reviewable, so on a branch
    that keeps moving it goes stale without saying so

A pull request that changes no application code, or too little of it, gets no
map — the run still happens and its summary says which rule skipped it and
what it counted. The thresholds are yours, in .accountable-review.yml.

Use these, or change something?
```

**Name the write scope in the block, every time.** It is the one decision here that changes what the
job is permitted to do rather than how often it runs, and a team that discovers `pull-requests: write`
in a file they did not read is entitled to be annoyed. Do not soften it into "posts a link" — say the
permission, and say what it cannot do, which is most of what they want to know.

**Say the costs in the same breath as the decisions.** Both are the kind that is invisible when it
bites: a stale map reads exactly like a current one, and a skipped pull request looks identical to a
broken workflow. A user who has heard both once can live with either; a user who discovers one in
three weeks concludes the tool is unreliable.

If the repository has a dependency bot — `inspect-repo.sh` reports `bot_prs` — name the file you
found, because the guard is otherwise an abstraction. If it has none, the guard still ships; say it
is there for when one is added rather than pretending it is doing something today.

Take their answer as flags rather than as an edit to the file:

| They say | Pass |
|---|---|
| regenerate on every push | `--regenerate-on-push` |
| map the bot's pull requests too | `--no-skip-authors` |
| skip another bot as well | `--skip-authors 'dependabot[bot],renovate[bot]'` |
| don't comment on the pull request | `--no-pr-comment` — drops the write scope with it |

```sh
<skill base directory>/scripts/install-workflow.sh --repo-dir . --print-diff [-- <flags>]
```

It renders and writes, and prints one status line:

| `status=` | What happened | What to do |
|---|---|---|
| `created` | The file did not exist | Report it in step 6 |
| `unchanged` | It was already exactly this | Say so. **This is a success, not a no-op to apologise for** |
| `drift` | It exists and differs | Below |
| `updated` | It was rewritten because you passed `--update` | Say what changed |

It also prints a `when=` line: the decisions the written file actually makes, in the same flags. When
a workflow was already there, those came from **its** `# Decisions:` line rather than from what
you passed — the script recovers a team's confirmed decisions so that moving the version pin does not
revert them. **Report from `when=`, not from what you asked for.** They differ exactly when it
matters, and a setup message describing decisions the file does not make is worse than one that says
nothing.

That recovery is also why a re-run should not re-ask. A workflow already carrying its decisions has
been confirmed once; confirm again only if the user is changing something or the line is missing.

**Drift is the interesting case and it is not an error.** Someone edited the workflow — tightened a
timeout, pinned an action by sha, changed the runner. The script prints the diff and writes nothing.
Show the user what would change, in a sentence or two rather than a wall of YAML, and let them choose;
re-run with `--update` only if they say so. Silently reverting a team's edit is the worst thing this
command can do, which is why the script cannot do it by accident.

The rendered file is deterministic — no date, no run id, nothing random — which is what makes running
this twice safe: the second run compares bytes and finds nothing to do. Do not add a timestamp
comment to the workflow for any reason.

**Do not hand-write the YAML**, and do not paste an edited copy of the template. `templates/workflow.yml`
is the source; a run that types its own version produces a file that no longer matches what
`install-workflow.sh` renders, so the next run reports drift against setup's own output.

## 4. Write a config file only if it would say something

Read `references/config.md`. `.accountable-review.yml` is optional and usually unnecessary:

```yaml
review_map:
  delivery:
    retention_days: 14
```

**Write one only when a value differs from the default.** A file whose entire content restates the
defaults is a file the team has to maintain that carries no information, and worse, it reads as
configuration someone chose. If the user asked for nothing unusual, write nothing, and say that the
defaults are in effect rather than leaving them wondering where the settings live.

**This is where a size answer lands.** A user who says *map everything, however small* or *don't
bother under about fifty lines* is asking for `trivial_lines: 0` or `trivial_lines: 50`, not a flag —
how big a change has to be is run-time configuration, not one of step 3's when-decisions, and
`references/config.md` says why. Write the key, and only the one they moved.

The config is read **at run time**, by the CI scripts, from the repository — so changing it later
does not mean regenerating the workflow. That is worth telling the user in step 6.

## 5. Delivery is already decided, unless they ask

The default provider is `github-artifact` and it is what the workflow ships with. It needs no
hosting, no credential and no extra service, and it is shared with everyone who can see the
repository the moment the run finishes. The cost is that a Review Map has to be downloaded and
extracted before it can be read.

If the user asks for anything else — a static host, an S3 bucket, a URL people can click — read
`references/delivery.md`. The short version: generation writes a portable static directory, delivery
is one script, and adding a provider changes nothing about how the page is produced. Do not build one
unless they asked for it.

## 6. Say exactly what happened, and what has not

Report in this shape:

```
Accountable Review CI configured.

Created:
  .github/workflows/accountable-review.yml

Review Maps will be generated when:
  - a pull request is opened ready for review
  - a draft is marked ready for review
  - a pull request is reopened

Not generated for:
  drafts, forks, dependabot, and trivial changes — 2 or fewer
  application files and 20 or fewer application lines, both

Delivery:
  GitHub Actions artifact, retained 30 days
  linked in one comment on the pull request (pull-requests: write)

A push to a ready pull request does not regenerate the map; check the revision
the page names before trusting it. Superseded runs are cancelled automatically.

Still to do:
  Add a model credential as a repository secret
  (Settings → Secrets and variables → Actions → New repository secret) — either:
    ANTHROPIC_API_KEY        an API key from the Anthropic Console, billed to
                             that API account; or
    CLAUDE_CODE_OAUTH_TOKEN  run `claude setup-token` on a machine already
                             signed in to Claude Code and paste what it prints,
                             to bill the runs to that Claude subscription.
  Until then the workflow will run and fail at the generation step.
```

**The last part is not optional and never gets rounded up.** If the credential is not configured, say
it is not configured. You cannot check a repository's secrets from here, so unless step 1 found a
workflow already reading `ANTHROPIC_API_KEY` or `CLAUDE_CODE_OAUTH_TOKEN`, list it as outstanding and
say plainly that you could not verify it. A setup message claiming everything is ready, followed by a
red run on someone's first pull request, spends the trust this command needs.

**Name both, and name where each comes from.** The workflow file reads two variables and says nothing
about their source, so a team that has never created one assumes an API key is the only way to pay
for this. `claude setup-token` is the other way and usually the one they want, since it uses a Claude
subscription they already have. Add, for the OAuth token only, that it is personal — every Review Map
in the repository is generated as whoever ran the command — and that it expires, so re-running the
command and replacing the secret's value is the fix for a workflow that starts failing on
authentication with nothing else having changed. `references/workflow.md` § *The credential* has both
sources in full.

Name the other limits in the same breath, briefly, where they apply:

- **Pull requests from forks are skipped.** They get no secrets, so the job could not authenticate.
  Say so for a repository that takes outside contributions — it is the difference between a
  documented boundary and a feature that mysteriously never fires.
- **The map is generated once and never regenerated**, so on a branch that keeps moving it describes
  an older revision while looking current. Nothing on the page says the code changed under it; the
  revision it names is the only way to tell, which is why that is in the masthead. Say this to any
  team whose branches keep moving after review starts, and tell them `--regenerate-on-push` is the
  answer. `references/workflow.md` § *Triggers* has the trade both ways.
- **Two kinds of pull request get no Review Map**, and the first time either happens it reads as the
  setup having quietly broken — so say both. One that changes **no application code**: only
  documentation, only tests, only a lockfile, only CI config. And one whose application change is
  **trivial**: 2 files or fewer *and* 20 lines or fewer, both, so a change that is large by either
  measurement still earns a map. The run stops after the checkout and writes a job summary naming
  which rule fired and the numbers behind it. Say that the thresholds are theirs —
  `review_map.trivial_files` and `review_map.trivial_lines` in `.accountable-review.yml`, read at run
  time, either at `0` to turn the trivial rule off — and that the defaults are a starting point
  rather than a measurement. `references/workflow.md` § *The application-code gate* has the trade.
  The run itself is not silent about either: it happens, and its summary names the rule and the
  counts, so a skip is never mistaken for a broken workflow.
- **The workflow pins a plugin version**, and setup cannot check that the tag exists — it has no
  network. Review Maps stay attributable to a version of this plugin, and re-running this command
  after an upgrade moves the pin. If you are running from a development checkout rather than an
  installed release, say that the pinned tag may not be published yet: the failure otherwise lands on
  someone's pull request as a clone error.

Then stop. Do not offer to open a pull request, do not commit, and do not push — the files are in the
working tree and the user decides what happens to them. If they ask you to commit, commit only the
files this command created.

## What it configures

Defaults, chosen so that running this with no arguments is the right answer. Every one of them is
explained in `references/workflow.md`.

The first block is **when** a Review Map is generated. Those are the ones step 3 confirms, and the
ones a flag can change.

| | | |
|---|---|---|
| Triggers | `opened`, `ready_for_review`, `reopened` | `--regenerate-on-push` adds `synchronize` |
| Draft pull requests | Skipped | — |
| Fork pull requests | Skipped — no secrets are available to them | — |
| Bot pull requests | `dependabot[bot]` skipped | `--skip-authors`, `--no-skip-authors` |

How big a change has to be is deliberately **not** in that table. It decides the same thing — whether
a model run happens — but the counts that settle it are over application paths, which the event
payload cannot express, so it is decided after the checkout and configured in
`.accountable-review.yml` rather than rendered here:

| | | |
|---|---|---|
| No application code changed | Skipped | — |
| Trivial application change | Skipped at 2 files **and** 20 lines or fewer, both | `review_map.trivial_files`, `review_map.trivial_lines`; either at `0` turns it off |

And one decision about **what the workflow may do**, which is the only one that changes the job's
permissions:

| | | |
|---|---|---|
| Link on the pull request | One comment, upserted, naming the revision | `--no-pr-comment` |
| Permissions | `contents: read`, plus `pull-requests: write` **only** for that comment | — |

The rest is not confirmed and has no flag, because none of it decides what gets spent, what gets
skipped, or what the job is allowed to do:

| | |
|---|---|
| CI platform | GitHub Actions |
| Effort | `high` |
| Delivery | `github-artifact` |
| Retention | 30 days |
| Concurrency | One run per pull request; superseded runs cancelled |
| Timeout | 30 minutes |

## Hard rules

- **Never modify a workflow this command did not create**, except for the one deliberate integration
  case in step 2 — and there, add a job and change nothing else. Do not rename files, do not
  reorganise jobs, do not "tidy" YAML, do not touch test configuration, and do not change
  repository-wide permissions.
- **Never overwrite a hand-edited Accountable Review workflow without being asked.** `drift` is
  reported and shown, never resolved silently.
- **Never write the workflow without having shown the user when it will run.** Step 3's block is one
  message and the expected answer is yes, but it is not optional and it does not get summarised into
  a clause after the fact. Two of those decisions — a trigger set that costs a model run per push,
  and a gate whose skips are invisible — spend or withhold money on someone else's account.
- **Never move a when-decision into `.accountable-review.yml`.** That file is read at run time and
  changing it must never mean regenerating the workflow; the triggers and the guard are the workflow.
  The request will arrive as "can we tune the thresholds without re-running setup", and the answer is
  that they edit the file, or re-run setup, and either way the file keeps saying what it does.
- **Never claim a credential is configured.** You cannot see repository secrets. Say what you found
  and what you could not check.
- **Never request permissions the job does not use.** `contents: read` always; `pull-requests: write`
  only when the comment step is rendered, and never a scope beyond those two. The rule did not
  loosen — it is the same rule, and the comment is now a thing the job does. A workflow carrying a
  write scope for a step that is not there is the failure, which is why `--no-pr-comment` removes
  both together and `tests/run.sh` checks that it does.

  `pull_request_target`, which would hand this job the repository's secrets on a branch a stranger
  controls, is still not an option to weigh.
- **Never measure the size of anything but application code, and never join the two thresholds with
  `or`.** The counts that decide a skip are over application paths only — a lockfile's lines are not
  the change's lines — and both have to be small for a pull request to be called trivial, so a
  change that is large by either measurement earns a map. Putting a count on the job's own `if:`
  breaks both rules at once, because the `pull_request` payload measures the whole diff and has no
  file list. `references/workflow.md` § *The application-code gate* owns all of it.
- **Never bake a size threshold into the generated workflow.** The when-decisions are rendered
  because they are the triggers and the guard; how big a change has to be is not one of them. Those
  numbers are a team's to own and change without regenerating anything, so they live in
  `.accountable-review.yml` and are read at run time.
- **Never make the generated workflow run the application under review.** No `bundle exec`, no
  migrations, no database service, no `docker compose`. The Review Map is built by reading source and
  tests; that is a property of the product, not an optimisation. `review-map` proposes validation
  commands for a human to run and never runs them, and CI must not quietly become the place that
  does.
- **One comment, and nothing else on GitHub.** The generated workflow may post exactly one comment
  per pull request — a link to the Review Map and the revision it describes — upserted against a
  hidden marker so a reopen updates it rather than adding a second. No checks, no statuses, no
  reviews, no labels, no approvals, no second comment, and nothing in the comment that grades the
  change.

  **The line is between discoverability and verdict, and it is narrower than it looks.** A link is
  where a reviewer already is; a check run named "Review Map" with a green tick is the product
  principle undone, because a passing check is a verdict whatever it is named. The next request will
  be for the check, and it will arrive as "so the map is visible in the status list". The answer is
  no: the comment is the visibility, and it was the whole reason to spend a write scope.

  **This reversed an earlier rule**, which was that the workflow posts nothing at all, and the reason
  it reversed is worth keeping. The run summary said where the map went, and nobody opens a workflow
  run to find out whether there is something worth opening — so the map was generated, uploaded and
  unread. A boundary that makes the product undiscoverable is not protecting the product.
- **`review-map` itself still posts nothing**, and that has not changed. The skill writes a page; the
  workflow's own final step is what comments. Threading a "post the link" step into generation would
  put a write token in the process that reads a pull request's code, and would make the delivery seam
  a lie — see § *Generation does not know where the page goes* in the repository's own notes.
- Never write the plugin's own files into the repository being set up. The workflow clones the plugin
  at a pinned tag; it does not vendor it.
