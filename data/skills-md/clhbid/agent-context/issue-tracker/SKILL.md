---
name: issue-tracker
description: Read and set work state on the CLHbid Delivery board — the delivery language, issues via gh, the Status field, the board query recipes, cycles, epics, labels, the commit convention and the decomposition rules. Use for any GitHub issue or project-board operation in a clhbid repo, and for what a cycle, epic or slipped issue means.
---

# Issue tracker: GitHub

Issues and specs for this repo live as GitHub issues. **Work state lives on the
[CLHbid Delivery](https://github.com/orgs/clhbid/projects/4) org project**, which spans every
clhbid repo. Use the `gh` CLI for all operations.

## Language

The words the skills plan and report in. Every rule below is written in these terms.

**Cycle**: a fortnight-ish planning period that work is committed to. Committing an issue to a
cycle is a promise to finish it in that cycle. _Avoid_: sprint, milestone.

**Epic**: a top-level issue carrying the `Epic` issue type, too large for one cycle and delivered
through its children. An epic is never committed to a cycle; each child fits in one cycle and is
committed on its own. _Avoid_: initiative, program, tracker issue, parent (every epic is a parent;
few parents are epics).

**Committed unit**: the issue whose `Cycle` is set — a top-level issue, or a child of an epic. Its
descendants inherit the cycle and are never set directly. _Avoid_: planned issue, scheduled issue.

**Slipped**: committed to a cycle and still open when it closed. Always a missed commitment, never
"progressing as expected". _Avoid_: in flight, carried over.

**Progress**: an epic's completed children over its total children. _Avoid_: percent complete,
velocity, burndown.

**Business work**: what the business plans and reads about — a top-level issue, or a child of an
epic. _Avoid_: ticket, story.

## Conventions

- **Create an issue**: `gh issue create --title "..." --body "..."`. Use a heredoc for multi-line
  bodies. This does not apply an issue form — follow
  [Creating an issue from the org form](#creating-an-issue-from-the-org-form).
- **Read, list, comment**: `gh issue view <number> --comments`, `gh issue list`,
  `gh issue comment <number> --body "..."`. `--jq` requires `--json`, so filtering a read means
  dropping `--comments` and naming the fields: `gh issue view <number> --json number,title,labels --jq ...`
- **Refer to an issue** by its full reference — see [References](#references).
- **Set state**: a project field, not a label — see [Status](#status).
- **Close**: an issue closes as `completed`, `not planned` or `duplicate`. The reason is the
  record, so pick the one that matches and say why in a closing comment.

  ```bash
  # Completed — the work is done
  gh issue close <number> --reason completed --comment "Shipped in #<pr>."

  # Not planned — we are not delivering it, abandoned and deferred alike
  gh issue close <number> --reason "not planned" --comment "Deferred to <date>; <owner> holds it."

  # Duplicate — another issue carries the work
  gh issue close <number> --duplicate-of <other-number> --comment "Tracked under #<other-number>."
  ```

  - `completed` is the default when `--reason` is omitted.
  - `not planned` is two words — `not-planned` is rejected. It is the whole record for a deferral
    or an abandonment; nothing else is needed.
  - `--duplicate-of` sets the reason to `duplicate` and links the two issues, so the survivor's
    thread becomes the history. Take the number of the issue that stays open.

- **Fix a close reason**: `gh issue edit` cannot set one, and `gh issue close` no-ops on an
  already-closed issue. For `completed` and `not planned`, PATCH it:
  `gh api --method PATCH repos/{owner}/{repo}/issues/{n} -f state=closed -f state_reason=not_planned`
  To record a duplicate after the fact, reopen and re-close:
  `gh issue reopen <number> && gh issue close <number> --duplicate-of <other-number>`.

## References

**Write every reference in full, as `<org>/<repo>#<number>`**, in prose and in tables alike. GitHub
renders it as a link with a hovercard and shortens it to `#<number>` when it is same-repo, so it
costs nothing to read. A **bare `#<number>` resolves against whichever repo hosts the text it sits
in** — in an org discussion that is `clhbid/clhbid.com`, not the repo you meant — and links silently
to the wrong issue.

**Read short references; write full ones.** People use a bare `#<number>` and the aliases below,
matched regardless of case. Resolve one before acting on it, and say which issue you resolved it to.
When editing a doc or notes that hold short references, propose replacing them with full ones. Ask
when an alias is unknown or could mean two issues, and suggest a short alias for any repository the
table lacks.

| Alias               | Repository                           |
| ------------------- | ------------------------------------ |
| `LA`                | `clhbid/CLHbid-LiveAuction`          |
| `com`               | `clhbid/clhbid.com`                  |
| `AC`                | `clhbid/agent-context`               |
| `infra`             | `clhbid/infrastructure`              |
| `TZ`, `hotpatch`    | `clhbid/canadian-time-zone-hotpatch` |
| `DF`                | `clhbid/devcontainer-features`       |
| `gh`, `.github`     | `clhbid/.github`                     |
| `scripts`           | `clhbid/clhbid-scripts`              |
| `E2I`               | `clhbid/email-to-issue`              |
| `SFET`              | `clhbid/salesforce-email-templates`  |
| `template`          | `clhbid/repository-template`         |

Issues and pull requests share one number space, so resolve a number with `gh pr view <n>`, falling
back to `gh issue view <n>`.

## Status

`Status` on the CLHbid Delivery project is the **single source of truth** for what state an issue
is in.

| Status           | Meaning                                                                                        |
| ---------------- | ---------------------------------------------------------------------------------------------- |
| Backlog          | The inbox — everything not yet routed. New issues land here                                    |
| Waiting on input | We asked the reporter or the business something and cannot proceed until they answer           |
| Ready for Agent  | Fully specified, sliced to one pull request, and carrying an agent brief                       |
| Ready for Human  | Needs a person — judgement, external systems, manual verification, or a pull request to review |
| In progress      | Claimed and being worked                                                                       |
| Done             | Closed, for any reason (`completed`, `not planned` and `duplicate`)                            |

Everything else stays native and is never duplicated onto the board: **assignee** (who holds it),
**linked pull requests** (what is in review), **sub-issues** (decomposition), **issue
dependencies** (blocking), **closed** (finished).

**Triage empties `Backlog`.** Every issue arrives there and leaves by being routed to
`Ready for Agent`, `Ready for Human` or `Waiting on input`, or by being closed. Work considered and
deliberately deferred goes back to `Backlog` and is reconsidered next time — so `Backlog` never
means "already dealt with", and a full inbox is the normal state rather than a backlog of triage
debt.

**An empty `Waiting on input` is a healthy state**, not a query to debug: nothing is blocked on the
business.

**Prefer `Ready for Agent`**, which needs both halves of its row — fully specified _and_ already
sliced. Work that cannot be specified until someone decides something is `Waiting on input`: a
question to answer, not work to schedule. `Ready for Human` is for what no agent can finish. For
what counts as an agent brief, see [`afk-loop` § The agent brief](../afk-loop/SKILL.md#the-agent-brief).

**Ask the business by email.** A business decision is emailed as it comes up rather than saved for
the cycle review, which is for what needs real discussion. The email says what is happening in plain
language, the decision needed, the options each with its consequence, a recommendation and why, and
a link to the issue.

**Claiming is an assignee write.** `gh issue edit <n> --add-assignee @me` is the atomic first
write that stops two agents taking the same issue; setting `Status` to `In progress` follows it.

**An issue that is not on the board has no state** and is invisible to every query below. Auto-add
workflows put newly-opened issues on the board; after creating one, give the workflow a moment and
then confirm it landed, adding anything that was missed.

**Adding one issue adds its whole tree.** Adding a parent pulls in every descendant, across
repository boundaries and including repos nobody had in scope. So planning being set on
[committed units](#business-and-delivery) does not make the board that shallow — most of it is
descendants, and they arrive with `Cycle` unset. Any group-by-`Cycle` view therefore carries a
large **No Cycle** bucket: descendants whose committed ancestor is planned, and epics, which never
carry one.

### Setting Status

`gh project item-edit` needs three IDs. Look them up once per session:

```bash
# project id, Status field id, and the option id for each status
gh api graphql -f query='
  query { organization(login: "clhbid") { projectV2(number: 4) {
    id field(name: "Status") { ... on ProjectV2SingleSelectField { id options { id name } } } } } }'

# the item id for an issue (an issue may sit on several projects — take project 4)
gh api graphql -f query='
  query($owner: String!, $repo: String!, $num: Int!) {
    repository(owner: $owner, name: $repo) { issue(number: $num) {
      projectItems(first: 10) { nodes { id project { number } } } } } }' \
  -f owner="$(gh repo view --json owner --jq .owner.login)" \
  -f repo="$(gh repo view --json name --jq .name)" \
  -F num=<number> \
  --jq '.data.repository.issue.projectItems.nodes[] | select(.project.number == 4) | .id'
```

**Take the repo from the checkout, never a literal.** The board spans every clhbid repo and issue
numbers are per-repo, so a pinned `repo=` resolves the wrong issue somewhere else — usually a
`NOT_FOUND`, but a number that exists in both repos returns a real item id for the wrong issue, and
`item-edit` accepts it.

Then:

```bash
gh project item-edit --project-id <project-id> --id <item-id> \
  --field-id <status-field-id> --single-select-option-id <option-id>
```

Read the value back afterwards — a wrong option id is accepted silently.

## Triage roles

The skills speak in terms of five canonical triage roles. Here a role is a **`Status` value**, not
a label — [Status](#status) has what each one means.

| Role in mattpocock/skills | Status here                         |
| ------------------------- | ----------------------------------- |
| `needs-triage`            | Backlog                             |
| `needs-info`              | Waiting on input                    |
| `ready-for-agent`         | Ready for Agent                     |
| `ready-for-human`         | Ready for Human                     |
| `wontfix`                 | close with `--reason "not planned"` |

When a skill says "apply the AFK-ready triage label", set `Status` to the value in this table.
`In progress` and `Done` have no counterpart in that vocabulary.

## Business and delivery

**Decomposition is a delivery concern.** Work is broken into sub-issues so it can be tracked,
sliced and reviewed one pull request at a time — see
[Decomposing work before Ready for Agent](#decomposing-work-before-ready-for-agent). The business
does not track work at that grain: a **top-level issue is the unit of business work**, and its
children are how that work gets done. The one exception is an [epic](#epics), whose children are
each business work in their own right because each is committed to a cycle on its own.

The board carries both audiences as views — **📋 Delivery board** is everything but epics,
**💼 Business** is `no:parent-issue -type:Epic`, and **🗺️ Epics** is the epics with their progress.

## Querying the board

Issue search cannot read project fields: `status:"In progress"` is not a qualifier and matches
nothing. Every state query therefore runs against the board with
[`board.graphql`](board.graphql) — one query, filtered per use with `--jq`.

**Find `board.graphql` first.** It sits beside this file, with [`snapshot.graphql`](snapshot.graphql),
but where that is depends on how the skill was installed. Resolve them once per session and reuse
them:

```bash
for d in ~/.claude/skills/issue-tracker \
         ~/.agents/skills/issue-tracker \
         .claude/skills/issue-tracker; do
  [ -f "$d/board.graphql" ] && BOARD_QUERY="$d/board.graphql" \
    && SNAPSHOT_QUERY="$d/snapshot.graphql" && break
done
```

If none of them exists, say so rather than guessing — every recipe below needs it.

```bash
# Agent frontier — ready, leaf, unblocked, unclaimed
gh api graphql --paginate -F query=@"$BOARD_QUERY" --jq '
  .data.organization.projectV2.items.nodes[]
  | select(.content.state == "OPEN" and .status.name == "Ready for Agent"
           and .content.assignees.totalCount == 0
           and .content.subIssues.totalCount == 0
           and .content.issueDependenciesSummary.blockedBy == 0)
  | "\(.content.repository.name)#\(.content.number)  \(.content.title)"'

# Needs triage — the inbox
... | select(.content.state == "OPEN" and .status.name == "Backlog")

# Needs business input
... | select(.content.state == "OPEN" and .status.name == "Waiting on input")

# In flight
... | select(.content.state == "OPEN" and .content.assignees.totalCount > 0)

# Business filter — top-level issues and epic children, never an epic itself. Goes at the head of
# the jq program, before `.data`, in any recipe that wants its business view
def business: .content.issueType.name != "Epic"
              and (.content.parent == null or .content.parent.issueType.name == "Epic");

# Planning view — open business work
... | select(.content.state == "OPEN" and business)

# Epics — every open epic with its progress
... | select(.content.state == "OPEN" and .content.issueType.name == "Epic")
    | "\(.content.repository.name)#\(.content.number)  \(.content.subIssuesSummary.completed) of \(.content.subIssuesSummary.total)  \(.content.title)"

# Epics ready to close — open, with every child closed. A person closes them
... | select(.content.state == "OPEN" and .content.issueType.name == "Epic"
             and .content.subIssuesSummary.total > 0
             and .content.subIssuesSummary.completed == .content.subIssuesSummary.total)

# Epic candidates — committed parents that are not epics. Read each one; the recipe only narrows
... | select(.content.state == "OPEN" and .content.issueType.name != "Epic"
             and .content.parent == null and .content.subIssuesSummary.total > 0
             and .cycle != null)
    | "\(.content.repository.name)#\(.content.number)  \(.content.subIssuesSummary.completed) of \(.content.subIssuesSummary.total)  \(.content.title)"

# Status/state mismatch — the Item closed workflow missing one. Healthy result is empty
... | select((.content.state == "CLOSED" and .status.name != "Done")
          or (.content.state == "OPEN"   and .status.name == "Done"))

# Worked off-cycle — work that never got credited to the cycle it happened in
... | select((.content.state == "CLOSED"
              and .content.closedAt >= env.CYCLE_START and .content.closedAt < env.CYCLE_END
              and (.cycle.title // "") != env.CYCLE_TITLE)
          or (.content.state == "OPEN" and .status.name == "In progress" and .cycle == null
              and .content.updatedAt >= env.CYCLE_START))

# ...of which dormant — swap that last clause for uncycled In progress work nobody touched
              and .content.updatedAt < env.CYCLE_START))

# Stale closed items — closed but never archived. Healthy result is empty
... | select(.content.state == "CLOSED"
             and (.content.closedAt | fromdateiso8601) < (now - 4838400))

# Stale issues — business work untouched for eight weeks
... | select(.content.state == "OPEN" and business
             and (.status.name | IN("Backlog", "Ready for Agent", "Ready for Human"))
             and (.content.updatedAt | fromdateiso8601) < (now - 4838400))

# ...of which newly stale — add this clause to keep the ones not yet stale when the cycle began
             and (.content.updatedAt | fromdateiso8601)
                 >= ((env.CYCLE_START | strptime("%Y-%m-%d") | mktime) - 4838400)
```

`...` stands in for the full command above. `--paginate` applies `--jq` per page, so filtering and
listing work as written; counting needs a pipe (`| wc -l`).

**Archived items are invisible here.** `ProjectV2.items` defaults to
`archivedStates: [NOT_ARCHIVED]`, so every recipe reads the live board only. That is what makes the
stale-closed recipe re-runnable — it cannot see what it just archived — and it is why
[`snapshot.graphql`](snapshot.graphql) passes `archivedStates: [ARCHIVED, NOT_ARCHIVED]` explicitly.

**Eight weeks is 4838400 seconds**, and it is the definition of _stale_ — an item is stale on the
board, not in someone's judgement, and staleness is measured on business work. The cycle recipes
read `CYCLE_TITLE`, `CYCLE_START` and
`CYCLE_END` from the environment; set them from the iteration's `title`, `startDate` and
`startDate + duration`. `CYCLE_END` is **exclusive** — an iteration ends the day before the meeting
that closes it, so a cycle titled `14 Aug → 28 Aug` has `CYCLE_START=2026-08-14` and
`CYCLE_END=2026-08-28`.

**Newly stale is derived, never stored.** It compares one `updatedAt` against two thresholds: stale
against today, and not-yet-stale against `CYCLE_START`. There is no baseline to snapshot at the end
of a cycle. Anchoring it to `CYCLE_END` instead would ask which items went stale between today and
today, and return nothing.

**Pull requests are not board items**, so the recipe below runs per repository against
`gh pr list` instead, taking the issue from the `NNNN:` title prefix or the `NNNN-` branch prefix
(see [Commit convention](#commit-convention)):

```bash
# Merged pull request, open issue — a closing reference that never fired, or none. Healthy result is empty
for repo in $(gh repo list clhbid --no-archived --json name,hasIssuesEnabled --jq '.[] | select(.hasIssuesEnabled) | .name'); do
  open=$(gh issue list --repo "clhbid/$repo" --state open --limit 500 --json number --jq '.[].number')
  gh pr list --repo "clhbid/$repo" --state merged --limit 200 --json number,title,headRefName,closingIssuesReferences \
    --jq '.[] | ((.title | capture("^#?(?<n>[0-9]+)[: ]")?) // (.headRefName | capture("(^|/)(?<n>[0-9]+)-")?) // empty) as $m
          | "\($m.n)\t\(.number)\t\(.closingIssuesReferences | length)\t\(.title)"' \
  | while IFS=$'\t' read -r n pr refs title; do
      grep -qx "$n" <<<"$open" && echo "$repo#$n open — merged in $repo#$pr, $refs closing reference(s)  $title"
    done
done
```

**A closing reference fires only on a merge into the default branch.** A row with a closing
reference and an open issue is a pull request that merged somewhere else — a stacked slice merged
into its parent before GitHub retargeted it, or anything merged into `scale-up` or `development`.
A row with none had no `Closes` line, or a deliberate `Refs`/`Part of`. Either way the issue closes
by hand — as `completed`, naming the pull request, per [Conventions](#conventions) — unless the pull
request was a partial and the issue is still live.

**These recipes are canonical**, and no API returns a view's contents — so a view can never be
queried directly, only mirrored:

| #   | View              | Filter                                             | Purpose                                   |
| --- | ----------------- | -------------------------------------------------- | ----------------------------------------- |
| 1   | 📋 Delivery board | `-type:Epic`                                       | everything but epics, grouped by `Status` |
| 2   | 🎯 This cycle     | `cycle:@current`                                   | the running cycle                         |
| 3   | ⏭️ Next cycle     | `cycle:@next`                                      | what is planned next                      |
| 4   | 💼 Business       | `no:parent-issue -type:Epic`                       | top-level work, delivered and outstanding |
| 5   | 🤖 Frontier       | `status:"Ready for Agent" no:assignee -is:blocked` | mirrors the frontier recipe               |
| 6   | ⏳ Waiting        | `status:"Waiting on input"`                        | mirrors the needs-business-input recipe   |
| 8   | 📥 Triage         | `status:Backlog no:parent-issue`                   | the inbox, top-level only                 |
| 9   | 🗺️ Epics          | `type:Epic`                                        | mirrors the epics recipe                  |

View **numbers** are stable and never reused after a delete, which is why 7 is missing. Only the
filter is worth asserting against this table: a view's name, columns and tab position belong to
whoever uses it, so a change there is intent rather than drift. The one column worth naming is
**Sub-issues progress** on 🗺️ Epics — a built-in field, and the progress bar the view exists for.

**A filter is writable.** `updateProjectV2View` takes `name`, `layout`, `filter` and
`configuration`, so a drifted filter can be **repaired**, not only reported. Grouping and sorting
are **readable** — `ProjectV2View` exposes `groupByFields`, `verticalGroupByFields` and
`sortByFields` — but not writable: `ProjectV2ViewConfigurationInput` takes only `visibleFieldIds`.

Both board views group by `Cycle` as swimlanes with `Status` as the columns, and **an iteration with
no items renders no swimlane** — so a completed cycle leaves the board once its items are archived,
and no filter is needed to hide one.

## Cycles

A cycle is an iteration of the `Cycle` field. An iteration **ends the day before the meeting that
closes it**.

Read them from the field's `configuration`. `completedIterations` holds the closed ones; the
running cycle is the entry in `iterations` whose `startDate` is on or before today and whose
`startDate + duration` is after it, and the future cycles are the ones starting after it. Select by
date rather than by index — nothing guarantees the array's order.

`Cycle` is set on the **committed unit** — a top-level issue, or a child of an [epic](#epics) —
and its descendants inherit it, so a sub-issue with no `Cycle` is planned, not missed. An epic's
own `Cycle` is never set.

**Three iterations are live at all times** — the running cycle and two future ones — so planning
always has somewhere to put work deferred two meetings out.

**The title carries the theme**, and until one is agreed it is the date range as a placeholder
(`Sep 29 - Oct 12`). Dates live in the iteration's own `startDate` and `duration`. **Titles must be
unique**: the cycle recipes match on `CYCLE_TITLE` and the swimlanes are labelled by title, so two
cycles sharing one read as one.

### Writing the configuration clears the whole board

`updateProjectV2Field` is the only mutation that touches `iterationConfiguration`, and **every write
is a full replacement that regenerates every iteration id and clears every item's `Cycle`**. Even an
identical configuration written back does it, so appending an iteration costs exactly what renaming
one does. The input also has **no `completedIterations`**, so any completed cycle not passed back
inside `iterations` is deleted outright.

**Make one configuration write per cycle**, folding every pending change into it — the new
iteration, the agreed end date, any theme titles — and wrap it:

1. **Snapshot** every item's `Cycle`, archived items included, with
   [`snapshot.graphql`](snapshot.graphql) — [`board.graphql`](board.graphql) is live-only and
   would silently skip them:

   ```bash
   gh api graphql --paginate -F query=@"$SNAPSHOT_QUERY" \
     --jq '.data.organization.projectV2.items.nodes[] | select(.cycle.startDate)' \
     > /tmp/cycle-snapshot.jsonl
   ```

2. **Write once**, passing **all** iterations, completed ones past-dated so GitHub re-sorts them
   back into `completedIterations`. The configuration's own `startDate` cannot be read back — only
   `startDay` is exposed — so pass the earliest iteration's `startDate`.
3. **Restore** every snapshot value, resolving iterations **by `startDate`** — every id changed, and
   a title may have moved to another date. An archived item cannot be edited, so unarchive it
   (`unarchiveProjectV2Item`), set its `Cycle`, and archive it again (`archiveProjectV2Item`).
4. **Read back** `completedIterations` and the restored count. An empty `completedIterations` is the
   failure signature; a count short of the snapshot means items were missed.

## Epics

An epic is work too large for one cycle — see [Language](#language). The hierarchy is
**epic → issue → sub-issues**, the first and last optional, and the epic layer is one deep: an
epic sits under nothing, and its children are the committed units. Work that turns out to span
cycles becomes an epic by being split into children that each fit one.

- **The `Epic` issue type is the marker**, and the only issue type the skills key off. Set it with
  `gh api --method PATCH repos/{owner}/{repo}/issues/{n} -f type=Epic`; `gh issue create` cannot,
  so create the issue and PATCH it. Find them with `gh issue list --search type:Epic`, or the
  **Epics** recipe. If the org has no `Epic` type, creating one is `createIssueType` on the org
  node, and it needs the `admin:org` scope that the default `gh` login lacks.
- **Status walks the ordinary ladder**, and so does each child, triaged like anything else.
  `Backlog` while the epic still needs decomposing, `Ready for Human` once its children exist,
  `In progress` from the first child committed to a cycle, `Done` when a person closes it.
- **`Cycle` is never set on the epic.** Each child is a committed unit and carries its own — so a
  child left open at cycle close slipped, and the epic is neither done nor slipped, only
  progressing.
- **Decompose before the first child is committed.** Progress counts direct children only, so it
  reads truthfully only when every child is a one-cycle piece. A child that will not fit a cycle
  is split into two children of the epic, keeping the layer one deep.
- **Closing is a judgement**, so a person does it. The **Epics ready to close** recipe finds
  candidates.

## Deferring work

Deferring is a decision to record. Its form follows when the work comes back:

- **A future cycle** — set `Cycle` to one of the two ahead. The issue stays open and the board
  carries it.
- **A later date** — comment with the decision, the owner, and when it returns, then close with
  `--reason "not planned"`. The owner sets the calendar reminder; nothing in GitHub will raise it
  for them.
- **Unknown** — leave it in [`Backlog`](#status) for triage to reconsider.

**Reopen rather than refile** when it comes back, so the thread stays the history.

## Labels

Labels never carry state. Two matter:

- **`bug`** — something is broken.
- **`enhancement`** — everything else: new features, and the tooling, config and refactor work we
  used to call chores.

Issue templates apply exactly one of them, and `/wayfinder` adds its own — see
[Wayfinding operations](#wayfinding-operations).

Any other label is decoration — read it if you like, but nothing keys off it.

## Creating an issue from the org form

Issue forms in `clhbid/.github/.github/ISSUE_TEMPLATE/` are the source of truth for what an issue
body contains.

Before `gh issue create`, fetch the form you need:

```bash
gh api repos/clhbid/.github/contents/.github/ISSUE_TEMPLATE/<bug|enhancement>.yml \
  --jq .content | base64 -d
```

Use each field's `label` as a `### ` heading in the issue body, in the same order as the form. Fill
every required field, written with `writing-lean`. Omit optional fields when they do not apply.
This rule applies to any agent-authored body, including later edits.

Anything beyond the form's fields — acceptance criteria, interface notes, verification steps, or
scope boundaries outside the form itself — belongs in the issue's agent-brief comment (or a
triage-notes comment), not as extra body headings. See [`afk-loop` § The agent brief](../afk-loop/SKILL.md#the-agent-brief).

Creating this way still means one category label (`bug` or `enhancement`), no state label, and then
confirming the issue landed on `Backlog` — see [Status](#status).

## Templates apply a category, never a state

Issue forms come from the org defaults in `clhbid/.github` under `.github/ISSUE_TEMPLATE/`. **A
person filing an issue should use one** — they collect fields a triager otherwise has to ask for.

A form applies exactly one **category** label (`bug` or `enhancement`) and **no state**. Category
says what kind of thing an issue is; `Status` says where it has got to — nothing about the category
implies a state.
When an agent creates an issue without the browser form, use
[Creating an issue from the org form](#creating-an-issue-from-the-org-form).

## Commit convention

Commit subjects carry the issue number as a bare prefix — `2217: <subject>`. A trailing `(#NNNN)`
is the **pull request**, added by squash-merge, and is never the issue. When resolving the spec for
a diff, read the leading `NNNN:` and ignore the trailing `(#NNNN)`.

## Decomposing work before Ready for Agent

Keep `1 issue = 1 branch = 1 PR`. If work is too large, split the **issue**, not the pull request.
Size is a precondition of `Ready for Agent`. Work too large for a **cycle** is an [epic](#epics),
split one level higher.

**Smaller is better.** ~1000 changed lines is the ceiling — excluding lockfiles, snapshots and
generated files — but it is a limit, not a target: a changeset that splits cleanly should be split
well below it, because a reviewer reads a small diff and skims a large one. If a plan crosses the
ceiling, simplify first, cutting documentation that fails the `writing-lean` deletion test before
anything else, then split. There is no CI gate for this.

- A valid slice is **independently mergeable and green**. Behaviour-neutral slices (rename,
  extraction, refactor) count when they stand alone.
- **Stack the pull requests when slices depend on each other.** A pull request can target a branch
  other than `main`, and GitHub retargets it automatically when its base merges — so a dependent
  slice can be opened and reviewed straight away instead of waiting for its parent to land.
- **If an agent finds mid-flight that work is too large**, it simplifies, creates sub-issues, links
  them as children, sets the leaves to `Ready for Agent`, opens a pull request for the work it has
  finished — stacked on the previous slice where they depend on each other — and comments on the
  original issue explaining the cut.

## Pull requests as a triage surface

**PRs as a request surface: no.** _(Set to `yes` if this repo treats external PRs as feature requests; `/triage` reads this flag.)_ While it is `no`, external PRs are not triaged and no `gh pr` state handling applies.

## When a skill says…

- **"publish to the issue tracker"** — create a GitHub issue via
  [Creating an issue from the org form](#creating-an-issue-from-the-org-form).
- **"fetch the relevant ticket"** — `gh issue view <number> --comments`.

## Wayfinding operations

Used by `/wayfinder`. The **map** is a single issue with **child** issues as tickets.

- **Map**: a single issue labelled `wayfinder:map`, holding the Notes / Decisions-so-far / Fog body. `gh issue create --label wayfinder:map`.
- **Child ticket**: an issue linked to the map as a GitHub sub-issue (`gh api` on the sub-issues endpoint). Labels: `wayfinder:<type>` (`research`/`prototype`/`grilling`/`task`). Once claimed, the ticket is assigned to the driving dev.
- **Blocking**: GitHub's **native issue dependencies**. Add an edge with `gh api --method POST repos/<owner>/<repo>/issues/<child>/dependencies/blocked_by -F issue_id=<blocker-db-id>`, where `<blocker-db-id>` is the blocker's numeric **database id** (`gh api repos/<owner>/<repo>/issues/<n> --jq .id`, _not_ the `#number` or `node_id`). GitHub reports `issue_dependencies_summary.blocked_by` (open blockers only — the live gate). A ticket is unblocked when every blocker is closed.
- **Frontier query**: list the map's open children, drop any with an open blocker or an assignee; first in map order wins.
- **Claim**: `gh issue edit <n> --add-assignee @me` — the session's first write.
- **Resolve**: `gh issue comment <n> --body "<answer>"`, then `gh issue close <n>`, then append a context pointer (gist + link) to the map's Decisions-so-far.

## Traps

**A wrong filter looks correct.** GitHub ignores an unknown qualifier rather than erroring. It can
fail in either direction — a typo may return everything, while `status:"In progress"` in issue
search returns nothing — so a result count proves nothing on its own. Check a new filter against a
query whose answer you already know.

**REST lies about parentage.** `gh issue view --json parent` errors outright, and
`gh api repos/{owner}/{repo}/issues/{n} --jq .parent.number` returns `null` for a child exactly as
for a top-level issue. GraphQL's `Issue.parent` answers truthfully, which is what
[`board.graphql`](board.graphql) selects. Checking issue by issue costs a request each and gets
skipped under pressure, so **put `no:parent-issue` (or `.content.parent == null`) in the query
itself**.

**Adding an item unarchives it.** `addProjectV2ItemById` on an already-archived item silently
returns it to the live board. Archived items are invisible to a live-only read, so a **reopened**
issue looks absent, gets re-added, and comes back out of the archive as a side effect.

**A read-back can be stale.** The project API is eventually consistent. Verify every write by
read-back, but treat a mismatch straight after a write as unconfirmed rather than failed — re-check
after a delay, and never re-issue the write on the strength of one disagreeing read.
`issueDependenciesSummary.blockedBy` lags the same way — it read `0` immediately after a blocker was
linked and `1` shortly after — so the **Agent frontier** recipe run straight after a write can hand
out an issue that is already blocked.
