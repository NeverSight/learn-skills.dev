---
name: setup-skills
description: "Configure this repo for the Gharib89/skills engineering skills: draft its ship profile, local gate, PR template, coding-standards doc and reviewer scaffolding, and check the host tooling. Run once after /setup-matt-pocock-skills, before the first /ship."
disable-model-invocation: true
metadata:
  version: 0.13.0
  composes: mattpocock/skills#d81f3a183412e71a5b1e84ca21bc1a35eea03a60:triage
---

# Setup skills

Draft the per-repo documents the `ship` skill reads, confirming with the human before every write. Same shape as `setup-matt-pocock-skills`: explore once, present, walk what exploration could not settle, confirm the full draft, write, prove. This skill does only what that parent leaves undone and ship needs: it takes the parent's answers on tracker, triage vocabulary and domain-doc layout as given, and asks only about what the parent left open.

Every document you write here is read by an agent: apply `writing-for-agents` to its prose.

## Process

### 1. Preconditions: instruct and stop

Check all three before exploring. On any failure print the exact command, then "then rerun `/setup-skills`", and stop.

1. **Parent docs.** `docs/agents/issue-tracker.md`, `docs/agents/triage-labels.md` and `docs/agents/domain.md` exist. Else: `/setup-matt-pocock-skills`. One exception: when the host (step 2) is Azure DevOps and `issue-tracker.md` is missing or is the parent's freeform "Other" page, offer to write the vendored [issue-tracker-ado.md](./issue-tracker-ado.md) in its place (confirm first), then continue. The parent ships GitHub, GitLab and local templates only.
2. **Composed skills as derived copies.** `.claude/skills/` holds `code-review`, `tdd`, `writing-for-agents`, `triage`, `find-docs` and `show-me`, each recorded in the repo's `skills-lock.json` (the skills CLI writes it at install) with the `ref` its line below pins, the upstream commit the source repo tested. A copy the lock records at another `ref`, or none, is off its pin: print its line. A copy present but absent from the lock is hand-maintained: report it as "will be replaced by the derived copy", confirm, then refresh it with the same line. A global copy under `~/.claude/skills` leaves this check unmet: a personal skill silently shadows a repo's, so ship's composed skills must live in the repo. Else print:

   ```sh
   npx skills add mattpocock/skills#c55ee46073ed923f86ce59a5eb3b6d895095d1b7 --skill code-review --skill writing-for-agents --agent claude-code -y
   npx skills add mattpocock/skills#d81f3a183412e71a5b1e84ca21bc1a35eea03a60 --skill tdd --skill triage --agent claude-code -y
   npx skills add upstash/context7#e275a848a420e0d11c2822f61201ee005bfd1133 --skill find-docs --agent claude-code -y
   npx skills add humanlayer/skills#ca7c8088db69e315a8b2deea43820270457f8f3c --skill show-me --agent claude-code -y
   ```

3. **`ship`, `cloud-ship` and `setup-skills`.** `.claude/skills/ship`, `.claude/skills/cloud-ship` and `.claude/skills/setup-skills` exist and are in the lock. A `ship` folder with no `metadata.version` in its frontmatter is a hand-maintained copy from before the generic skill: report "will be replaced by the derived copy", confirm, refresh. `setup-skills` gets step 1.2's treatment; the copy running this check is not evidence, so read `skills-lock.json`. It belongs in the repo because the `### Ship` block below and ship's three profile stops both end "run `/setup-skills`", which only a repo carrying it can follow. Else print:

   ```sh
   npx skills add Gharib89/skills --skill ship --skill cloud-ship --skill setup-skills --skill update-skills --agent claude-code -y
   ```

   `update-skills` is no precondition: nothing refuses without it. When it is absent from the lock, report that, print the same line, which installs it, and go on.

   Project scope always, which is the install line without `-g`. The agent id is `claude-code`; the CLI rejects `'Claude Code'`.

### 2. Host

From `git remote get-url origin`: `github.com` is `github`; `dev.azure.com` or `visualstudio.com` is `ado`; anything else stops as out of scope. Cross-check against `docs/agents/issue-tracker.md`'s title line; a mismatch stops and names both.

Then prove the host tooling with ship's own preflight, the one host check that exists. Call it issueless, so the verdict is about the host and the profile alone:

```sh
.claude/skills/ship/scripts/preflight.sh none
```

Exit 2 with a `host-unreachable` reason (CLI missing, extension missing, not signed in, no push permission) stops here with that reason: setup is the one moment a human is present to fix auth. Exit 1 with `profile missing` is the expected answer at this point; continue.

Preflight cannot prove the git remote itself, so also run `git ls-remote --heads origin`. A failure here surfaces later only as `existing branch: remote unreadable`, and every push in a run would fail. On Azure DevOps with an Entra `az login` and no PAT, offer the repo-local credential helper from the tracker doc's Auth line, which mints the git password from the same token.

### 3. Explore

Read the repo once, every section, before saying anything. The right-hand column says whether exploration settles the section or the walk (step 4) must.

**The harness first**, because it decides the Local gate and Cloud lane rows. Its profile, `docs/agents/harness.md`, is the one signal: a bare `scripts/check.sh` or a harness `CLAUDE.md` block is not. Present: read two of its lines, `Location:` under `## Check entry point` and `Setup:` under `## Cloud`, and run `<Location> full` once from the repo root, where `<Location>` is that harness line, not the ship profile's. The entry point conforms when that one run exits 0 or 1 with one JSON line on stdout carrying `rung`, `verdict` and a `checks` object; a red check is still a conforming answer. Anything else is reported as `harness present, check entry point non-conforming: re-run /setup-harness`, and **Local gate over the harness** stops there: no gate is written or rewritten, since a gate over that entry point would map nothing. An existing gate is still run once in step 5, and the ship profile's `Location:` records it; with none, `Location:` records `scripts/local-gate.sh`, the path a setup-skills re-run writes once `/setup-harness` has fixed the entry point, and step 7 tells the user that no local gate exists until then. Every other item goes on, **Cloud bootstrap** included, which never calls `check.sh`. Absent: step 4 opens with the no-harness question.

| Section | Read | Settled by exploration? |
|---|---|---|
| Host | step 2 | yes |
| Worktree | `Carry:` from `git status --ignored --short`, kept to small dotfiles (`.env*`, `*.local`); `Bootstrap:` `None.` unless a setup script exists that the local gate cannot own | yes, confirm the list |
| Local gate | with a harness, the gate step 5 writes over the harness profile's `Location:`; otherwise `scripts/local-gate.sh`, else `.claude/skills/ship/scripts/local-gate.sh`, else `scripts/ship/local-gate.sh`; the lockfile fixes the runner (`package-lock.json` npm, `pnpm-lock.yaml` pnpm, `uv.lock` `uv run pytest`, `pyproject.toml` alone `pytest`); `Small node:` syntax follows the runner, and a docs-class line giving the path of the changed document | location yes; node syntax walked |
| CI | `Legs:` every job of every workflow with a `pull_request` trigger (`.github/workflows/*.yml`; on ADO the pipelines named by build-validation policies); other workflows named in prose as non-PR; `No-checks legal: yes` iff any PR workflow carries a `paths:` filter, or there is no PR workflow at all, which with `Legs: None.` is the pair that drops `ci-wait`'s no-checks grace to zero; `Push policy:` | legs yes; push policy walked |
| Reviewers | one list per reviewer kind, [### Reviewers](#reviewers) below | walked |
| Coding standards | a path CLAUDE.md names, `CODING_STANDARDS.md`, `CONTRIBUTING.md`, `docs/contributing/*` | yes, or stub |
| Verification | not discoverable; seed from test markers (`e2e`, `integration`), Docker use, browser-test scripts | walked |
| Versioning and changelog | semantic-release config, changesets, `version-gate` or bump scripts, `CHANGELOG.md`; `In-PR requirement:` | walked |
| PR | `.github/pull_request_template.md` or `.azuredevops/pull_request_template.md`: presence, headings, and where any closing reference sits relative to the first `## ` heading | yes |
| Public surface | `Default.` proposed | walked |
| Triage | copied from the `needs-triage` row's right-hand column in `triage-labels.md` | yes |
| Docs sync | `README.md`, `docs/`, `GLOSSARY.md`, skills the repo ships; `Agent-facing:` `docs/agents/`, `.claude/skills/` | yes, confirm |
| Current docs | context7 always; Microsoft Learn when a Microsoft stack shows (D365, Azure, Power BI, .NET); `Pinned:` | walked |
| Cloud lane | `PR cap: 3`; `Bootstrap:` `scripts/cloud-ship-bootstrap.sh` with a harness, which step 5's **Cloud bootstrap** writes; without one, that path when the file exists, else `None.` | yes |

Also record, for step 5, three things:

- The per-repo ship scripts the generic mechanics supersede: `claim`, `isolate`, `preflight`, `poll-pr`, `ci-wait`, `merge-and-verify`, `merge`, `reflect`, `release`, `_lib` under `scripts/ship/`, and `claim`, `merge-and-verify` and `release` under `.claude/skills/ship/scripts/`, whose other files are the derived copy's own mechanics.
- Which of `triage-labels.md`'s five role labels and [dimension-labels.md](./dimension-labels.md)'s fourteen dimension labels the host already carries, from `gh api --paginate "repos/{owner}/{repo}/labels" --jq '.[].name'`. Read it paginated rather than through `gh label list`, which fetches 30 by default and silently truncates: a label the host carries but the read missed is reported as a gap, and step 5 then asks the host to create a label that is already there. Match **case-insensitively**, because GitHub label names are: a label in another casing is recorded as a rename and not as a gap. On ADO a tag exists once it is used, so there is nothing to read.
- Whether `docs/agents/triage-labels.md` already carries a `## Dimension labels` heading.

### Reviewers

Detect per kind, propose each with the trigger the evidence implies, and confirm every one:

- **CodeRabbit.** `.coderabbit.yaml` in the repo: `Trigger: on-push`.
- **Copilot.** `.github/copilot-instructions.md`, plus the `copilot_code_review` rule read from `gh api repos/{owner}/{repo}/rules/branches/{default_branch}` with the branch percent-encoded into that one segment, since a default branch may carry a slash and an unencoded one addresses a different route. That endpoint returns the rules the host has already resolved for that branch, so a rule scoped to another branch stays out of the answer, and it is the endpoint ship's own preflight reads: propose from the repo-wide ruleset list instead and setup writes a profile ship then refuses. The rule's `review_on_push` fixes the trigger: `true` is on-push; `false` or absent is auto-once where the PR's opening round is the only one wanted, or on-request where that same opening round is the loop's round 1 and the cap buys the rest, which is the shape to propose wherever the repo wants a bound it controls. Preflight reads the rule and refuses a `Trigger:` that disagrees with it, so a value confirmed against the evidence here is the one that runs.
- **A reviewer with request history.** `review_requested` events on the last ten merged PRs: `on-request`.
- **Claude Code.** `claude-code-action` in a workflow, where the trigger the workflow declares is the trigger the profile takes: a `pull_request` trigger is on-push, an `issue_comment` trigger is on-request, the phrase its `if:` matches is the `Request: comment <phrase>` value, and the workflow file itself is the `Workflow:` value. A Claude review pipeline on Azure DevOps is on-push.

Then, for each reviewer the draft names: `Resolve:` is walked where the proposed trigger is on-push or on-request and the reviewer's findings arrive as inline review comments, and it takes the mechanism that reviewer offers on that host. `resolve-thread` covers the GitHub reviewers that open review threads, Copilot and `claude-code-action`. A Claude review pipeline on Azure DevOps takes the line [its scaffold](reviewers/ado-claude-review.md) writes instead, the PR thread's status set to `fixed` once a finding is dispositioned. A reviewer that posts its own resolve comment takes that, as CodeRabbit does. It reads `None.` otherwise, which is what auto-once always takes because its one round ends with every thread dispositioned and none resolved. `Workflow:` is taken from the evidence rather than asked: the path of the workflow file detection already read, on the one reviewer whose `Request:` is a comment transport, and `None.` on every other. `Cap:` is asked of every reviewer, always.

### 4. Present, then walk

Present the whole exploration once: what each section will read, one line each. Then walk **only the walked rows**, one section, one answer, each led by the recommended answer so the user can accept in a word. A one-line explainer only where the choice genuinely branches. Sections exploration settled are shown in the draft; the walk skips them.

Walk order and the recommendation to lead with:

- **No harness**, asked first and only where step 3 found no harness profile: "no harness found: run `/setup-harness` first (recommended), or continue without". The first ends the run with nothing written, printing "run `/setup-harness`, then rerun `/setup-skills`". Continuing takes the **Self-contained local gate** item and skips **Cloud bootstrap**, so the bootstrap stays as step 3 found it. The answer is recorded nowhere, so every run asks it again.
- **Local gate, small node**: the runner's own node syntax with one example from the repo's tests, and the docs-class value, the path of the changed document, with one example.
- **CI, push policy**: `one push per review round` on metered minutes (private repos, ADO parallel jobs); `Default.` otherwise.
- **Reviewers**: each detected reviewer with its inferred trigger; then "any reviewer not detected?". Then **one question for Claude Code**, asked only where exploration found no Claude workflow already. With another reviewer in the draft, lead with the on-request fallback shape, naming that reviewer as the primary it stands in for. With the draft naming none, ask about both shapes in one question with the trade-off, leading with on-request for a repo where ship opens most PRs, on-push otherwise: on-request (comment transport, `Fallback-for: None.`, `Cap: 2`) gives a small-lane run one round and a cap that binds, and any commenter can trigger it; on-push reviews every push, human ones included, and its cap is advisory. That one answer picks the shape step 5 scaffolds; there is no second question. Ask every reviewer its cap: recommend 2 on-request, 3 on-push, `None.` for auto-once.
- **Verification**: one block per seed, or `None.` when nothing in the repo talks to a real system.
- **Versioning**: what exploration found, then `In-PR requirement:`, the one line that changes what ship does.
- **Public surface**: `Default.` unless the repo publishes more than an API (gate rules, palettes, bundle inputs).
- **Current docs, pinned**: the libraries whose major version the repo's manifest pins and whose API moved recently.

### 5. Confirm and edit

Show the full draft of everything below, then let the user edit before writing. Field-level validation happens here, the one moment a human is present to fix it. Every reviewer block carries every `Label:` line the template lists, `Cap:` included, and the draft is clear of the eight reviewer shapes ship's preflight refuses:

- an on-request reviewer with no `Cap:`
- a `Cap:` that is neither a number nor `None.`
- a `Fallback-for:` on a reviewer whose `Trigger:` is not `on-request`
- a `Fallback-for:` naming a reviewer the draft does not list
- a `Request: comment` with no phrase for the transport to post
- a `Request: comment <phrase>` with no `Workflow:` naming the file its round comes from
- a `Workflow:` on a block whose `Request:` is not a comment transport
- a `Workflow:` naming a file the checkout does not carry, a path climbing out of it with `..` included

Then: every `Also proven by CI:` names a leg defined in `## CI`; `defer-to-ci` appears only with such a leg; `Host:` matches step 2; fourteen headings in order; the `Schema:` line equals ship's `metadata.profile-schema`.

**`docs/agents/ship.md`** from [ship-profile.md](./ship-profile.md): all fourteen headings, `None.` or `Default.` where an axis is defaulted, template comments removed.

**The `### Ship` sub-block**, from [ship-block.md](./ship-block.md) with its template comment removed, inside the existing `## Agent skills` block of whichever of `CLAUDE.md` / `AGENTS.md` the parent chose (the file that has the block). Updated in place when present, so the file ends with exactly one.

**Local gate over the harness**, when step 3's probe conformed. `check.sh full` supplies every gate it runs, one per check under the check's own name; the local gate adds only what Ship needs.

- Absent: write `scripts/local-gate.sh` from [local-gate-harness.sh](./local-gate-harness.sh): `__CHECK__` the harness profile's `Location:` path, `__DEPS__` and `__RUNNER__` from step 3's Local gate row, `secrets` wired as the self-contained item below wires it, and the marked slot holding the Ship-only gates: the checks relative to the base, and a `mark <leg> deferred-to-ci` for each CI leg only CI can prove. Gates here carry check names rather than leg names, so the self-contained item's one-gate-per-leg rule does not apply; each `deferred-to-ci` mark still names its leg as `## CI` names it.
- Present: propose a rewrite onto that template. Drop each gate `check.sh full` already runs, matched by the command it runs rather than by its name; the template's own `secrets`, `deps` and small-lane `tests` replace the old gate's. Keep each gate that needs Ship (one relative to the base, a `deferred-to-ci` mark) in the Ship-only slot, and list for the human each one that neither matches a check nor needs Ship, and keep or drop each on their answer. Show the diff, write on confirm.

**Self-contained local gate**, without a harness:

- Absent: write `scripts/local-gate.sh` from [local-gate.sh](./local-gate.sh), one gate per CI leg named as the leg is named in `## CI`, run locally where the runner is obvious and `deferred-to-ci` where it is not; `secrets` wired to a detected scanner (`gitleaks`, `ggshield`, `detect-secrets`, `trufflehog`), else left `unavailable` with a comment naming what to add. That is honest: the first attended run stops and names exactly what is missing.
- Present and conforming (JSON verdict with `verdict`, `gates`, a `secrets` gate, `--small` and `--base` flags): keep it; `Location:` records where it is.
- Present but non-conforming (prints text, positional `--small`, no `unavailable` status): propose a rewrite to the contract that keeps every check the old gate ran, show the diff, write on confirm. `Location:` moves to `scripts/local-gate.sh` only if the human agrees.

Whichever local gate item ran, or the existing gate a non-conforming probe left in place, **run the gate it wrote or kept once** (`--small` with the example node) and check the verdict shape: a JSON object with `verdict`, `base`, `lane`, `gates.secrets`.

**Cloud bootstrap**, with a harness; skipped without one. Write `scripts/cloud-ship-bootstrap.sh` from [cloud-ship-bootstrap.sh](./cloud-ship-bootstrap.sh). It reads `Setup:` from `docs/agents/harness.md` at run time and runs that cloud setup, so nothing is filled for it. Fill `SCANNER` with the executable name of the scanner the local gate's `secrets` gate runs (`gitleaks`), which it looks up with `command -v`, and `SCANNER_INSTALL` with its install: `apt_install gitleaks`, or a registry's own, `pipx install detect-secrets`. Never fill it with a GitHub release-asset download, which a cloud session's network blocks, so an existing bootstrap's pinned download is replaced rather than kept. Fill the marked slot with the repo's Ship-only steps. A step belongs to the harness cloud setup unless it needs something only Ship has, such as live-e2e credentials or profiles. An existing bootstrap is proposed as a rewrite onto the template: drop each step the cloud setup covers, matched by what it installs, keep the rest as Ship-only steps, list each ambiguous one for the human and keep or drop each on their answer, show the diff, write on confirm.

**PR template.** None: create it from [pull_request_template.md](./pull_request_template.md) at `.github/pull_request_template.md` (GitHub) or `.azuredevops/pull_request_template.md` (ADO). Exists: propose these edits and nothing else.

- A **legacy-heading migration**, when the template carries `## Summary` or `## Deviations from plan`. Propose renaming `## Summary` to `## Change outline` with a `## Why the change` heading above it, its one-sentence why split out of whatever prose the old section's comment asked for, and renaming `## Deviations from plan` to `## Special things to note`. Renaming rather than adding, because a template that keeps both carries nine sections of which two are dead: Ship writes into the new names, and the old pair sits under them collecting nothing while a human fills them in by hand. The instruction comment under each renamed heading is replaced too, with the one [pull_request_template.md](./pull_request_template.md) carries for that section: a `## Change outline` still carrying the old Summary comment asks for prose where the new section wants a fence, and a `## Special things to note` still carrying the old Deviations comment asks for the verbatim log the fold rule retired. Only content the repo's own people wrote is preserved.
- A **Door-line refresh**, when the template's `## Special things to note` comment does not ask for the Door line. Propose replacing that comment with the one [pull_request_template.md](./pull_request_template.md) carries for that section. The section acquired a required first bullet after this comment was written, and the legacy-heading migration above reaches a comment only where it renames the heading, so a template whose heading is already correct keeps prompting for warnings alone: the one line a reviewer reads before the diff is then the line no template asks anyone for. The comment text only; the heading and anything the repo's own people wrote under it stay.
- Each section the template still lacks after that migration, placed in this order and no other: `## Why the change`, `## Change outline`, `## Special things to note`, `## Needs attention`, `## Verification`, `## Review`, then `## Attribution` last. Placement is the whole point, not presentation: Ship reaches four of these with a `--section` write after PR open, `## Change outline` among them when a reviewer's objection to the outline is accepted, and a `--section` write on a body that lacks the heading **creates it at the end**. A heading missing from the template therefore lands below the attribution footer, which is the one thing the footer's placement rule forbids. `## Attribution` stays last for the same reason.
- A **closing-reference move**, when a closing reference sits below the first `## ` heading: propose moving that line, unchanged, above the first heading. A closing reference is any inflection of `close`, `fix` or `resolve` followed by `#`, case-insensitive, with or without an issue number: `ship_body_closes` needs the number to read a filled-in body as a claim, and a template carries the bare `Closes #` placeholder a run fills in. A section rewrite drops whichever one sits inside a section, and nothing else migrates a template written before the reference moved into the preamble.

**Coding standards.** None found: write `docs/contributing/coding-standards.md` from [coding-standards.md](./coding-standards.md), recording only what exists and is enforced today (config-enforced tools, links to CLAUDE.md sections carrying inline standards). Link to CLAUDE.md prose rather than moving it in.

**Triage labels on the host** (GitHub only). Any of the five role labels from `triage-labels.md` missing on the repo: create them, because ship's hand-back exits 1 without `ready-for-human`. Then the fourteen dimension labels of [dimension-labels.md](./dimension-labels.md), each created with that file's own color and description: only the ones step 3 recorded as missing, so a repo already carrying the set sees no label call. A label of **either** set that step 3 recorded in another casing is **renamed** rather than created a second time, which the host refuses anyway: `gh label edit <variant> --name <the spelling its own file gives>`, `triage-labels.md`'s right-hand column for a role label and the template's Label column for a dimension one. A dimension label's rename carries `--color <Color> --description <Description>` as well, the template owning both and casing drift usually bringing the rest with it; a role label's color is the repo's own, so its rename moves the name alone. On Azure DevOps a tag exists once it is used, so nothing is created there and only the section below is written.

**The `## Dimension labels` section** of `docs/agents/triage-labels.md`, from the same [dimension-labels.md](./dimension-labels.md), appended at the end of the file, below the role table and the two prose lines that explain it, with the template comment removed. Below those lines and not directly under the table: they speak about the role table, and a heading inserted above them puts them under the Kind table instead, where "from this table" and "the right-hand column" both resolve to the wrong thing. A file that already carries the heading is left alone: the section is the repo's once it is written. `triage-labels.md` is the label mapping a repo hands the vendored `triage` skill, through the `### Triage labels` block of its CLAUDE.md, so this write is how triage learns the three dimensions; its own prose carries the one-per-dimension and derived-order rules, and this step adds nothing to them.

**Reviewer scaffolding**, for each reviewer the user named that is not installed: write the files the host needs and hand the human an inline checklist of the steps only they can do (secrets, app installs, branch policies). Claude Code as reviewer: [reviewers/github-claude-review.md](./reviewers/github-claude-review.md), in the shape step 4's one question settled, or [reviewers/ado-claude-review.md](./reviewers/ado-claude-review.md) on Azure DevOps. Point the scaffold's `__INSTRUCTIONS__` at the profile's `Instructions:` path, which is the repo's reviewer brief where it has one and the coding-standards path where it has none, pointing at that file rather than a copy of it. Other bots (CodeRabbit, Copilot) are configured in their own UIs; the checklist names the setting. In a setup section re-run that names `reviewer-scaffolding`, an installed Claude workflow, the GitHub Actions file or the Azure DevOps pipeline, is compared against the whole current scaffold and each part the repo lacks is proposed, on the re-run rule below, and where none is installed the write above applies; a plain profile re-run does not run it, and the compare is done when every part of the scaffold is matched, proposed or reported kept. Read the fills, never ask: the shape (on-push or on-request) from the installed trigger, and `__INSTRUCTIONS__`, `__PHRASE__` and `__PRIMARY__` from the reviewer's profile block (`Instructions:`, `Request: comment <phrase>`, `Fallback-for:`). A value that cannot be read leaves that part kept and reported, never guessed. Keep the repo's deliberate departures, a dropped `issues: read` among them. In the GitHub file, propose a pin move only where a `uses:` ref is not a SHA or a checkout lacks `persist-credentials: false`; an existing SHA pin stays even where it differs from the scaffold's, so a refresh never downgrades.

**Superseded ship scripts** (migrating repos): list what step 3 recorded, propose deletion, delete on confirm. Leave `local-gate.sh`, `live-e2e`, `copilot-pr-review-loop` and `cloud-ship-bootstrap.sh` (which is `## Cloud lane`'s `Bootstrap:`) in place.

### 6. Write, then prove

Write every confirmed file. Then run ship's preflight against the new profile:

```sh
.claude/skills/ship/scripts/preflight.sh none
```

Report its `reasons`. The issueless call raises none of its own, so the list should be empty; any `profile missing`, `profile invalid`, `skill missing`, `skill off pin`, `skills lock unreadable` or `composes pin invalid` reason is yours to fix before finishing, the last by re-running the refresh line, since it means the installed `ship` copy is malformed. A `skill missing` or `skill off pin` reason names a composed skill step 1 left uninstalled or off its pin and carries the line that installs it: run that line. A `skills lock unreadable` reason comes before any install line: the skills CLI rewrites a lock it cannot parse holding only the new entry, so repair its JSON first.

### 7. Done

Tell the user: the profile is at `docs/agents/ship.md`, the first `/ship <issue>` can run, and `cloud-ship` is installed: a cloud routine on this repo fires it with the one-line prompt `Run the cloud-ship skill.` (it selects its own issue; the prompt names no repo). The routine itself is one operator's schedule and not written here. They can edit `docs/agents/ship.md` directly later.

## Re-run

Profile exists: run steps 1 to 3. Then compare the profile's `Schema:` line to ship's `metadata.profile-schema` in `.claude/skills/ship/SKILL.md`. Trailing: apply each `## Schema N` entry of [profile-schema.md](./profile-schema.md) between the two numbers in order, walking only the rows an entry adds or whose vocabulary it moves, leaving the prose under existing headings alone, and rewrite the `Schema:` line last. Ahead of ship: stop and print the refresh line; the profile is not what needs fixing. Then diff each section of the fresh exploration against the existing profile, propose only the updates, and ask whether anything else should change. Prose under the headings is the human's; update the `Label:` lines and leave the prose alone unless a fact it explains changed. Then propose step 5's closing-reference move against the existing PR template, and step 5's two dimension-label writes, the labels step 3 recorded as missing or miscased and the `## Dimension labels` section where `triage-labels.md` has none, each confirmed like every other write: a re-run reaches all three no other way. With a harness present, run step 5's **Cloud bootstrap** item, and **Local gate over the harness** where the probe conformed: each writes its file where the repo has none and proposes a rewrite of the copy it finds, since a harness installed after setup reaches them no other way. End with step 6.

**A setup section re-run**, when a refresh names setup sections whose templates moved (update-skills' step 6 maps each to the item it feeds): run steps 1 to 3, whose reads the items use (step 3's host labels among them), then only those items, then step 6. For each, compare the repo's whole current copy of what the item writes (the file, the `### Ship` sub-block, the labels on the host) against the whole current template, not only the template's change since the version the repo last installed. A repo that missed one paragraph releases ago misses it still after a delta-only re-run. Compare by what each part says rather than byte for byte, the template's own `setup-skills:` comment excepted. Propose each part of the template the repo lacks, and keep the repo's deliberate departures: its own wording, framing (a `### Ship` block worded around the repo's own derived copies, say) and any checks it added. For every named item, this compare replaces what the item otherwise does with a copy that already exists: updating it in place from the template (**The `### Ship` sub-block**), keeping it (**Self-contained local gate**), leaving it alone (**The `## Dimension labels` section**), proposing only listed edits (**PR template**), proposing the parts an installed Claude workflow lacks and writing one where none is installed (**Reviewer scaffolding**), or writing only where none is found (**Coding standards**, step 1.1's Azure DevOps tracker doc). **Triage labels on the host** already works on the whole label set, creating only what step 3 recorded missing, and **Local gate over the harness** and **Cloud bootstrap** already propose a rewrite of the copy they find; all three keep their rule. Write on confirm, like every other write. A section the refresh did not name is not audited.
