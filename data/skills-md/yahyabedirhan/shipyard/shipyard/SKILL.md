---
name: shipyard
description: "Edit shipyard's config.toml, the macOS menu bar app listing pull requests, issues and workflow runs. Use when asked to change my shipyard or the shipyard app (its layout, projects, notifications, what it shows): watch or group repositories, show or hide issues, runs, drafts or someone's items, switch the menu between a list and tabs, change when it notifies, show pings from my other machines, or fix its configuration file. Also use to ping me through shipyard with the `shipyard ping` command, from my Mac or another machine running Herdr: when a PR is ready, when you need my input, or to bring me back to this pane. Use `shipyard notify` from any of my machines to post a status notice (tests running, done) that needs nothing from me. And use to open, quit, steer or screenshot the shipyard app on my Mac with `shipyard app`, `panel` and `screenshot`, on my data or a demo's. And use for my notes, kept in Notion per shipyard project: to take a note I dictate, find one by its number, or list, tidy or archive them."
---

# shipyard configuration

Shipyard lists the pull requests (and, when turned on, issues and workflow runs) of the **projects** in one TOML file, and sends macOS notifications for the **events** its **notification rules** select. That file is the whole interface for settings: there is no settings window, and no command changes it. The app applies every save live.

Agents also send the user **pings** through shipyard with the `shipyard ping` command: short messages that take the user where the agent means when clicked. See Sending pings, after the configuration. For a status update that needs nothing from the user, they post a **notice** with `shipyard notify` instead: a notification that isn't kept. See Ping or notice?.

On the Mac, agents can also open, steer and screenshot the running app with `shipyard app`, `panel` and `screenshot`, on the user's data or a demo's, one agent at a time. See Driving the app, at the end.

The user's own **notes** live in Notion, one numbered list per project, and the menu lists the open ones. Before you take a note the user dictates, look one up by its number, or list, tidy or archive notes, read [references/notes.md](references/notes.md): it holds where notes live, the rules every agent follows, each operation through the Notion connector or `ntn`, and `shipyard notes check`, which shows whether the app can read them.

A request to change the user's shipyard is a change to this file. When no key below does what's asked, say that shipyard has no such setting.

This skill installs with `npx -y skills add yahyabedirhan/shipyard -g -y`. The app's settings menu (the gear) marks **Set up /shipyard skill** with a check once it's installed, and that view's **Update** runs the same command for its newest version. When the user asks for the newest skill, point them there, or run the command.

## The file

- Path: `$XDG_CONFIG_HOME/shipyard/config.toml` when `XDG_CONFIG_HOME` is set to an absolute path, else `~/.config/shipyard/config.toml`.
- Every key is optional. A missing or empty file means the defaults with no projects (the app then shows its project picker).
- The app writes to the file itself in three ways only: onboarding writes a whole preset (see below), but only into a file that is missing or holds nothing live but `version`; its project picker appends `[[projects]]` blocks; and the layout button in the menu's header sets `layout` under `[menu]` to the next layout in turn (list, then tabs, then list again), keeping every other line. So read the file afresh before each edit.
- Keys are kebab-case. The schema is `https://raw.githubusercontent.com/yahyabedirhan/shipyard/main/schema/config.schema.json`, named by the file's first line, `#:schema <url>`.

## Starting from a preset

Shipyard has three **presets**, ready-made files for its main uses; the app offers them when it's set up, and [presets.md](presets.md) has each one's whole file:

- `my-agents`: the pull requests and issues the user and their agents open, one project per repository.
- `incoming-contributions`: what other people open on the user's repositories, bots hidden, plus the pull requests waiting on their review anywhere.
- `review-queue`: only the pull requests waiting on the user's review, in any repository.

Start from a preset when the user names one, or asks to set shipyard up (or start over) for one of these uses, and the file is missing or holds nothing live but `version`: write the preset's file with the user's repositories, as presets.md says. When the file already has settings or projects, don't replace it: make the change the request needs with the keys below.

## Editing it

1. Read the whole file: the user writes comments in it and edits it by hand. Change or add only the lines the request needs, keeping every comment, blank line and the existing order.
2. Put what you add where TOML reads it:
   - A top-level key (`refresh-interval`, `launch-at-login`, …) goes **above the first `[table]` header**: below one, TOML reads it as a key of that table.
   - Keep `version = 1` at the top. A file that sets keys without it still reads, with a warning; a later version will reject it.
   - A table (`[menu]`, `[menu-bar]`, `[rate-limit]`, `[attention]`, `[defaults.issues]`, …) goes **above the first `[[projects]]` block**, once: when the table already exists, add the key to it. A table header written twice is invalid TOML.
   - A new project is a `[[projects]]` block **appended at the end** of the file.
   - A project's overrides (`pull-requests`, `issues`, `workflow-runs`, `pings`, `notes`, `notifications`) go **inside its own block** as inline tables, so each block stays self-contained.
   - An inline table `{ … }` stays on one line; an array `[ … ]` may span lines.
   - A file the app created starts with a header showing the common settings as commented-out TOML at their defaults: `[defaults.pull-requests] authors`, `[menu] layout`, `[menu-bar] count`, `[defaults] group-by`, `sort-by` and `show-first`, `[defaults.issues]` `show` and `states`, `[defaults.workflow-runs]` `show`, `[defaults.pings]` `show` and `seen-window`, a `[[defaults.notifications]]` rule and `[rate-limit] max-share-percent`. To set one, uncomment its lines (the table line with its keys) and change the value rather than adding a second copy. The header puts top-level keys above its tables, so any of them can be uncommented; in a file edited since, check that no top-level key sits below the table line you uncomment, which would pull that key into the table.
3. The app creates the file with that header whenever it starts, or its Refresh button is clicked, without one. When it still doesn't exist, create it (and its directory) starting with:

   ```toml
   #:schema https://raw.githubusercontent.com/yahyabedirhan/shipyard/main/schema/config.schema.json
   version = 1
   ```

4. Run `shipyard config check` after each edit, then check the rest (see Checking an edit). It is done when `shipyard config check` exits 0, `taplo check` exits 0, and the app's record says `"accepted": true` for your save.

## Keys and defaults

Top level:

| Key | Default | Allowed |
|---|---|---|
| `version` | `1` | only `1` |
| `refresh-interval` | `"2m"` | a window (below), at least `"30s"`: how often the app refreshes; a floor it stretches to stay within its rate-limit share |
| `launch-at-login` | `true` | boolean |

`hide-authors` (a top-level list of logins) is the old way to hide authors. The app still reads it, as a `hide` in each kind's defaults, with a warning; replace it with `authors` (see Whose items).

`refresh-interval-seconds` (a whole number of seconds) is the old form of `refresh-interval`. The app still reads it, with a warning that gives the new key: replace `refresh-interval-seconds = 90` with `refresh-interval = "90s"`. The two together are an error.

Tables:

| Key | Default | Allowed |
|---|---|---|
| `[menu-bar] count` | `"total"` | `"total"`, `"per-kind"` (PRs, issues, runs, pings apart), `"none"` |
| `[menu] layout` | `"list"` | `"list"` (every project in one scrolling list, one line per item), `"tabs"` (one project at a time) |
| `[menu] header-counts` | all five | a list of `"pull-requests"`, `"issues"`, `"workflow-runs"`, `"pings"`, `"notes"`, each once: the kinds with a count in each project header of the list layout. A project's header shows a count for each listed kind it has items of, always in that order, whatever order the list has. Global only: a project can't set it |
| `[rate-limit] show` | `"always"` | `"always"`, `"when-low"` (below 25%), `"never"` |
| `[rate-limit] max-share-percent` | `10` | `1`–`50`: the share of each hourly GitHub limit shipyard may spend (it's shared with the user's agents) |
| `[attention] unseen` | `true` | an item not clicked yet needs attention |
| `[attention] changed` | `true` | an item that changed since it was clicked needs attention |
| `[attention] review-requested` | `true` | a PR requesting the user's review (or a team's they're in) needs attention |
| `[attention] checks-failed` | `true` | a PR (or run) whose checks failed needs attention |
| `[herdr] terminal` | unset | the terminal app Herdr runs in, by name (`"Ghostty"`) or bundle id (`"com.mitchellh.ghostty"`): clicking a ping sent with `--herdr` focuses its Herdr tab, then brings this app forward. Unset, it brings forward the terminal the ping was sent from, when that was known; otherwise only the tab is focused |
| `[remote] machines` | `[]` | your other machines, by the labels your Herdr knows them by as saved machines (`["netcup-vps"]`), never a host or an address: shipyard asks each one for its agents' pings through Herdr and lists them in a section named after the machine, after the projects. A label can't start with `-` or be a project's slug or title |
| `[notices] listen` | `false` | whether the app takes notices (`shipyard notify`) from agents on your other machines straight over your tailnet. Nothing listens unless it's `true`; then the app listens on 127.0.0.1 only, and takes only notices sent from this Mac's own Tailscale login. Setting it up: [references/notices.md](references/notices.md) |
| `[notices] port` | `47420` | the port on 127.0.0.1 it listens on, which `tailscale serve` exposes to your tailnet |
| `[banners] snooze-duration` | `"1h"` | a window (below), more than `0`: how long a banner above the projects stays hidden after its ✕ is clicked. After it, the banner shows again if its condition still holds; a condition that stops and starts again shows its banner at once. A short one, such as `"10s"`, makes it quick to check that banners come back. `[banners] snooze` is its old name: the app still reads it, with a warning; rename it to `snooze-duration` |

What every project shows, set in `[defaults.pull-requests]`, `[defaults.issues]`, `[defaults.workflow-runs]`, `[defaults.pings]` and `[defaults.notes]` (and `[[defaults.notifications]]`), and what a project may override in its own block:

| Key | Default | Allowed |
|---|---|---|
| `pull-requests.show` | `true` | boolean |
| `pull-requests.states` | `["open", "merged", "closed"]` | which PRs are listed: any of `"open"` (drafts too), `"merged"`, `"closed"` (closed without merging) |
| `pull-requests.closed-window` | `"7d"` | a window (below): how long closed and merged PRs stay listed; `"0"` hides them |
| `pull-requests.drafts` | `true` | boolean; list draft PRs |
| `pull-requests.authors` | `{ show = [], hide = [] }` | whose PRs are listed: `authors.show` minus `authors.hide`, each a list of author selectors (see Whose items) |
| `pull-requests.review-requested` | `false` | boolean; `true` lists only open PRs waiting on the user's review, requested from them or from one of their teams |
| `issues.show` | `false` | boolean |
| `issues.states` | `["open", "closed"]` | which issues are listed: any of `"open"`, `"closed"` |
| `issues.closed-window` | `"7d"` | a window: how long closed issues stay listed |
| `issues.authors` | `{ show = [], hide = [] }` | whose issues are listed, as for pull requests |
| `workflow-runs.show` | `false` | boolean |
| `workflow-runs.states` | `["in-progress", "failed", "succeeded"]` | which runs are listed: any of `"in-progress"` (queued or running), `"failed"` (timed out and failed to start too), `"succeeded"` |
| `workflow-runs.finished-window` | `"3h"` | a window: how long finished runs stay listed (running ones always are) |
| `workflow-runs.branches` | `"default-and-pull-requests"` | or `"all"` |
| `workflow-runs.authors` | `{ show = [], hide = [] }` | whose runs are listed (a run's author is the account that started it) |
| `pings.show` | `true` | boolean; list the pings agents send with `shipyard ping`, each under the projects that watch its repository, or the one project it names. Pings take no `states`, `authors`, `drafts` or `review-requested`: setting one is an error |
| `pings.seen-window` | `"24h"` | a window: how long a seen ping stays listed, counted from when it was seen; an unseen ping stays until it's seen. A seen ping leaves within one refresh of its window passing, and is deleted |
| `notes.show` | `true` | boolean; list the user's open notes from Notion, newest first, in a "Notes" group: the notes in the project's database under the "Shipyard Notes" page's "Projects" page, matched by the project's exact title. Each row shows its number with its prefix (`SHOP-7`), its title (or its body's first line) and its labels; clicking it opens it in Notion, and the header's notes count opens the project's database. The project's header has a new-note icon that creates an empty note in its database (creating the database first, and the Projects page, when there is none) and opens it in Notion. Notes never need attention, so they add nothing to any count. A project without a database lists none. The app reads and writes them through `ntn`, Notion's CLI, with ntn's own login, every minute and when the menu opens; it keeps no Notion token of its own. Nothing lists, and no `ntn` runs, until the user presses **Connect with ntn** in the settings menu's **Set up Notion** view. Once connected, while `ntn` isn't installed or isn't logged in, or ntn's default workspace has no Shipyard Notes page, no notes list and a banner says what to do, and the new-note icon hides until `ntn` is installed and logged in (see the notes reference's Setting up ntn). Notes take only `show`: `states`, `authors`, `drafts`, `review-requested` or `seen-window` is an error |
| `notifications` | five rules: `pr.opened`, `ping.sent`, `agent.notice`, `control.started` and `control.ended`, each `authors = []` | a list of rules (below) |

A **window** is a string: a whole number and one unit, `s`, `m`, `h` or `d`, such as `"45s"`, `"30m"`, `"12h"` or `"7d"`; `"0"` hides closed (or finished) items at once. No fractions, negatives, spaces or two units: write `"90m"`, not `"1.5h"` or `"1h30m"`. A bad one is rejected with its line and the nearest spelling: "`closed-window` must be a whole number and one unit, `s`, `m`, `h` or `d`, such as "30m" (got "30min"; did you mean "30m"?)". An item leaves within one refresh of its window passing, without a click.

`pull-requests.closed-window-days`, `issues.closed-window-days` and `workflow-runs.finished-window-hours` (a whole number of days or hours) are the old forms. The app still reads them, with a warning; replace each with the new key (`closed-window-days = 3` is `closed-window = "3d"`, `finished-window-hours = 4` is `finished-window = "4h"`). Setting the old and the new key in one table is an error.

How every project's items are grouped and sorted in the menu, set straight under `[defaults]` (not in a sub-table), and what a project may override in its own block:

| Key | Default | Allowed |
|---|---|---|
| `[defaults] group-by` | `"kind"` | `"kind"` (pull requests, then pings, then issues, then runs, then notes), `"repository"` (A to Z), `"date"` (Today, Yesterday, This week, This month, Older), `"author"` (A to Z; pings by who sent them, then those that don't say, as "Pings"), `"none"` (one list); one level only |
| `[defaults] subsections` | unset | boolean: `true` draws each group under a subheader (its name and count), `false` after a divider line; unset keeps each layout's own look (dividers in the list, subheaders in tabs) |
| `[defaults] sort-by` | `"updated"` | `"updated"` (newest first), `"created"` (newest first), `"title"` (A to Z); open or running items always come first. `"date"` groups by this date (`"updated"` when sorting by title) |
| `[defaults] show-first` | `0` | a whole number, 0 or more: each group shows its first N rows and a "Show N more" row, which reveals the rest and then reads "Show less"; `0` shows every row. With `group-by = "none"` it caps the whole project. A group's count includes the rows it hides, and every cap comes back when the menu closes |

The All tab of the tabs layout always groups by kind, newest first.

What repository groups and `owner/*` bring in (see Which repositories), set in `[defaults]` and in a project's block:

| Key | Default | Allowed |
|---|---|---|
| `[defaults] archived` | `false` | boolean; `true` brings in archived repositories too |
| `[defaults] forks` | `true` | boolean; `false` leaves forks out |

A project, one `[[projects]]` block each, shown as sections in file order:

| Key | Required | Allowed |
|---|---|---|
| `slug` | yes | the project's ID, unique across projects: lowercase letters and digits joined by single hyphens, such as `"e-commerce"`. `--project`, `panel fold` and `panel tab` take it |
| `title` | no | the text the menu shows for the project, its section's and its tab's title, such as `"E-commerce"`; unset, the slug |
| `repositories` | yes | at least one repository selector: `owner/name`, `owner/*`, `owned`, `organizations`, `collaborator` or `anywhere` (see Which repositories); no URLs |
| `pull-requests`, `issues`, `workflow-runs`, `pings`, `notes` | no | inline tables with the keys above |
| `group-by`, `subsections`, `sort-by`, `show-first` | no | as under `[defaults]` above |
| `archived`, `forks` | no | booleans, overriding `[defaults]` for this project |
| `notifications` | no | a list of rules |

A `[[projects]]` block's `name` is the old form of `slug` and `title`. The app still reads it, with a warning that gives both: the title is the name, and the slug is the name in lowercase, with each run of other characters changed to one hyphen (`name = "Review queue"` reads as `slug = "review-queue"` and `title = "Review queue"`). Replace `name` with the two keys; `name` beside `slug` or `title` is an error.

## Overrides

- A project's `pull-requests`, `issues`, `workflow-runs`, `pings` and `notes` tables merge **key by key** onto `[defaults.*]`: `issues = { show = true }` shows issues and keeps the default `closed-window`. A list such as `states` is one key: the project's list replaces the default's. `authors` merges key by key too: a project's `authors = { hide = [...] }` replaces the default `hide` and keeps the default `show`.
- A project's `notifications` **replaces** the default list for that project; it doesn't add to it. Repeat any default rule the project should keep. `notifications = []` means no notifications for that project.
- `[[defaults.notifications]]` blocks likewise replace the built-in defaults (`pr.opened` from everyone, `ping.sent`, `agent.notice`, `control.started` and `control.ended`): once the file has one, write those rules too if they should stay. A file that lists its own rules without `ping.sent` gets no notification for pings; add `{ event = "ping.sent" }` to hear of them. A project whose rules leave out `agent.notice` refuses agents' notices, so `shipyard notify` exits 1 there; add `{ event = "agent.notice" }` to see them. Likewise, without `control.started` and `control.ended` it gets none when an agent starts or stops using the app.

## Which repositories: repository selectors

A project's `repositories` lists **repository selectors**, in any mix. The syntax is the author selectors' (below): a bare word is a group, and `/` marks a repository.

| Selector | Watches |
|---|---|
| `owner/name` | one repository: the owner is letters, digits and `-`; the name adds `_` and `.` |
| `owner/*` | every repository a user or organization owns, e.g. `my-org/*` |
| `owned` | every repository the signed-in account owns |
| `organizations` | every repository the account reaches through an organization it's a member of, directly or through a team |
| `collaborator` | someone else's repositories that added the account as a collaborator |
| `anywhere` | open pull requests waiting on the user's review in any repository, even one the user has never committed to |

- `owned`, `organizations` and `collaborator` are GitHub's own affiliations: they don't overlap, and together they are every repository the account can reach. There's no `me/*`: write `owned`.
- Groups and wildcards are looked up when the app starts, after each edit, on ⌘R and otherwise about once an hour, so a repository created later shows up without editing the file. Its existing items are listed quietly; only what happens after notifies.
- They leave out archived repositories and keep forks, unless `archived = true` or `forks = false` says otherwise. A repository named as `owner/name` is always listed, archived or not.
- A repository that two selectors bring in is listed once.
- An `owner/*` whose owner doesn't exist, or that the account can't see, shows an error row in the project; a group with no repositories shows "Nothing open".
- An author group (`me`, `others`, `bots`) or an `@login` in `repositories` is rejected with a hint: to watch someone's repositories, write `owner/*`.
- `anywhere` comes from one GitHub search, not from repositories, so it works only in a project that lists pull requests with `review-requested = true` and shows no issues or runs (in its block or its defaults). Anything else is rejected: "`anywhere` needs `pull-requests = { review-requested = true }`, and lists no issues or runs". The project's other filters (`authors`, `states`, `drafts`) apply as usual. The search returns at most 100 pull requests; when more are waiting, the project says so.

## Which items: states

Each kind's `states` picks its items by where they stand; what it leaves out isn't shown, counted or notified. The closed windows still apply: `states` says which items, `closed-window` (or `finished-window`) how long a closed, merged or finished one stays. So `pull-requests = { states = ["open"] }` lists no merged or closed PRs at all, and `states = ["merged"]` lists PRs merged within `closed-window`. A state the kind doesn't take is rejected with the nearest one it does: "unknown pull request state `merge` (did you mean `merged`?)". `states = []` lists none of the kind's items; to hide a kind, `show = false` says so more plainly.

## Whose items: author selectors

Each kind's `authors = { show = [...], hide = [...] }` decides whose items a project lists. An item is listed when its author matches `show` (an empty `show` is everyone) and doesn't match `hide`; `hide` wins when both match. Set it for every project in `[defaults.pull-requests]`, `[defaults.issues]` or `[defaults.workflow-runs]`, or for one project inside its block. Pull requests, issues and runs each have their own; hiding someone everywhere means hiding them in each kind the projects show.

What a project's filters leave out is gone from shipyard: it isn't shown, counted in the menu bar, the project's header or a tab, nor notified. Every fetched item is still remembered, so when a later edit brings an item into view it isn't notified as new.

The entries of `show` and `hide`, and of a notification rule's `authors`, are **author selectors**. The syntax is small: **a bare word is a group, `@` marks a person, `/` marks a repository.**

| Selector | Covers |
|---|---|
| `me` | the signed-in user, which includes agents working as them |
| `others` | anyone but the user and bots |
| `bots` | a GitHub Bot account or a login ending in `[bot]` |
| `@login` | one account, e.g. `@octocat` or `@dependabot[bot]` (keep the `[bot]` suffix); matched ignoring case |

`me`, `others` and `bots` together cover every author once. Always write a login with `@`: a bare word that isn't a group is rejected with a hint: "unknown author `bots2` (did you mean `bots` or `@bots2`?)". A repository (`owner/name`) or a repository group is rejected in `authors` too: repositories belong in a project's `repositories`.

## Notification rules

A rule, one element of a `notifications` list, is `{ event = "…", authors = [...] }`; `authors` is a list of author selectors and defaults to `[]`, everyone. An event is notified when a rule in the project's list names it and one of its `authors` matches the item's author. A rule only narrows what the project lists: an item the project's filters leave out (its `states`, `authors`, `drafts`, or a closed window of `0`) is never notified, whatever the rule says; so `pr.merged` needs `merged` in `states` and `closed-window-days` above `0`, and `run.failed` needs `failed` in `states` and `finished-window-hours` above `0`. Each event is notified once, and a project's existing items never notify when it's added.

| Event | When |
|---|---|
| `pr.opened` | a new pull request is listed open (drafts too) |
| `pr.merged` | an open pull request was merged |
| `pr.closed` | an open pull request was closed without merging |
| `pr.reopened` | a closed pull request was reopened |
| `pr.review_requested` | an open pull request newly requests the user's review, or a team's they're in |
| `pr.checks_failed` | an open pull request's checks newly failed |
| `pr.commented` | a pull request got comments or reviews |
| `issue.opened` | a new issue is listed open |
| `issue.closed` | an open issue was closed |
| `issue.commented` | an issue got comments |
| `run.failed` | a workflow run finished failed (also timed out or failed to start) |
| `run.succeeded` | a workflow run finished successfully |
| `control.started` | an agent started using the shipyard app (`shipyard app`, `panel` or `screenshot`): "Claude Code is using shipyard", over where it runs. Decided by `[[defaults.notifications]]` (or the built-in defaults) only: a project's own list and a rule's `authors` don't apply to it, and the app warns about either. Clicking it opens the panel, whose banner names the agent |
| `control.ended` | that agent is done with the app: "Claude Code is done with shipyard", over why (released, its lease ran out, you stopped it). Decided as `control.started` is |
| `ping.sent` | an agent sent a new ping: titled with the project and the ping's title, over its body and sender. A ping is notified once, and clicking the notification does what clicking the ping does: runs its action (opens its link or app, or focuses its Herdr tab) and marks it seen. Pings have no author, so a rule with `authors` never selects one |
| `agent.notice` | an agent posted a notice with `shipyard notify`: titled with the project and the notice's title, over its body and sender. Each notice is its own notification unless an `--id` replaces one, never listed or kept. A project whose rules leave it out refuses the notice, and the agent is told. Notices have no author, so a rule with `authors` never selects one |

Issue events need the project to show issues, and run events to show workflow runs.

Older files write a rule's `authors` as one string: `"any"`, `"me"`, `"others"` or `"bots"`. The app still reads them, with a warning; when you touch such a rule, write the list instead (`authors = ["others"]`; `"any"` is `[]`, or leave `authors` out).

## Checking an edit

**The command.** Run `shipyard config check` after each edit. It reads the file as the app reads it, without the app, and also reads the command's own `cli.toml` when there is one:

```sh
shipyard config check; echo "config check exit status: $?"
```

```text
/Users/me/.config/shipyard/config.toml: rejected
  problem: config.toml line 14: unknown event `pr.openned` (did you mean `pr.opened`?)
/Users/me/.config/shipyard/cli.toml: accepted (no file: the defaults)
```

Exit status 0 means every file is accepted: fix each `warning` line anyway, usually a misspelled key. Exit status 1 means a file has a `problem`: fix each one at its line and run the command again. `shipyard config check --json` prints each file's result under its name (`config.toml`, `cli.toml`) in the same fields as the app's record below, so you can compare them. It checks the files on disk, not what the app runs on: the app's record says whether the app took your save.

**The schema.** Run [Taplo](https://taplo.tamasfe.dev) on the file and print its exit status; it finds the schema through the `#:schema` line:

```sh
taplo check ~/.config/shipyard/config.toml; echo "taplo exit status: $?"
```

Exit status 0 is a pass; anything else is a fail, and the lines above it say why. Don't pipe the output through `tail`, `grep` or `head`: on success Taplo prints only an INFO line, and a pipe hides the exit status. Without Taplo installed, run `npx -y @taplo/cli check <file>` the same way, or `brew install taplo`. When the file has no `#:schema` line, or its schema URL can't be fetched, pass `--schema <url>` with the schema URL above (a local copy works as `file://<absolute path>`). The schema is stricter than the app about unknown keys: it rejects what the app would only warn about and ignore, so fix those too.

The schema can't check three rules; `shipyard config check` and the app's record catch them, or check them by reading the file:

- Every project `slug` is used once.
- A project lists each repository, wildcard and group once, ignoring case (`owner/name` and `Owner/Name` are the same repository).
- Top-level keys sit above the first `[table]` header.

**The app.** Shipyard rereads the file within a moment of each save and writes its verdict to `~/Library/Application Support/Shipyard/config-status.json`. After saving, wait a second, then read the record and the modification time of the file you edited (under `$XDG_CONFIG_HOME` when it is set):

```sh
cat ~/Library/Application\ Support/Shipyard/config-status.json
date -u -r ~/.config/shipyard/config.toml +%Y-%m-%dT%H:%M:%SZ
```

```json
{
  "accepted" : false,
  "checked" : "2026-09-25T12:05:01Z",
  "config" : "/Users/me/.config/shipyard/config.toml",
  "configModified" : "2026-09-25T12:05:00Z",
  "problems" : [
    {
      "banner" : "config.toml line 14: unknown event `pr.openned` (did you mean `pr.opened`?)",
      "line" : 14,
      "message" : "unknown event `pr.openned` (did you mean `pr.opened`?)"
    }
  ],
  "version" : 1,
  "warnings" : []
}
```

- **Is it about your save?** Only when `configModified` equals the `date` output (both UTC, whole seconds) and `config` is the file you edited. When it's older, the app hasn't reread yet: wait a moment and read it again. When it never catches up, shipyard isn't running; say so rather than claiming the app took the edit.
- **`"accepted": true`**: the app took the edit. `warnings` lists settings it ignored, each with its `line`: usually a misspelled key, so fix it.
- **`"accepted": false`**: the app rejected the file and keeps running on the last valid configuration. Fix every entry in `problems` at its `line` (`null` when it can't be placed), save, and read the record again. `banner` is the same line the user sees in the panel's banner, which ends in "Using the last valid configuration.".

The record also catches what only the app checks, including the three rules above.

## Worked requests

**"Watch this repo in shipyard."** Take the `owner/name` slug from the repository's `origin` remote. If a project already lists it, say so and stop. Otherwise append a block. Its `slug` comes from the repository's name, the part after `/`: in lowercase, each run of other characters one hyphen (`My_Shop` → `my-shop`). When another project already has that slug, make it from the whole `owner/name` the same way (`yahyabedirhan-shipyard`). When the user gives the project a name of their own, make the slug from their name instead, and add their name as the `title` unless it's already the slug (`"My Shop"` → `slug = "my-shop"`, `title = "My Shop"`):

```toml
[[projects]]
slug = "shipyard"
repositories = ["yahyabedirhan/shipyard"]
```

**"Group these repos into one project."** One block lists them all. When some of them are already projects, move their repositories (and any overrides that should apply to the group) into one block and delete the blocks they leave empty; keep the comments that still apply.

```toml
[[projects]]
slug = "e-commerce"
repositories = ["yahyabedirhan/e-commerce-frontend", "yahyabedirhan/e-commerce-backend"]
```

**"Watch all my repositories."** One project with the `owned` group; add `organizations` when the user means their organizations' repositories too:

```toml
[[projects]]
slug = "mine"
repositories = ["owned"]
```

**"Watch everything in my-org, and my own shipyard."** A wildcard beside a single repository; `archived = true` would bring in the organization's archived repositories as well:

```toml
[[projects]]
slug = "my-org"
repositories = ["my-org/*", "yahyabedirhan/shipyard"]
```

**"Notify me when others open PRs here."** Give that project its own list (it replaces the defaults; see Overrides):

```toml
[[projects]]
slug = "shipyard"
repositories = ["yahyabedirhan/shipyard"]
notifications = [
  { event = "pr.opened", authors = ["others"] },
]
```

For every project instead, write `[[defaults.notifications]]` blocks.

**"Hide dependabot."** A `hide` in the pull requests' defaults (add to the list when it exists; add the same to `[defaults.issues]` when projects show issues). Write the login with `@`, as GitHub shows it, `[bot]` suffix included. To hide every bot, write `bots` instead.

```toml
[defaults.pull-requests]
authors = { hide = ["@dependabot[bot]"] }
```

When the file still has an old `hide-authors` list, move its logins into these `hide` lists (each with `@`) and delete the `hide-authors` line.

**"Keep merged and closed items for 30 minutes."** Set `closed-window` in each kind's defaults (`finished-window` for runs), or inside one project's block for that project alone. Replace an old `closed-window-days` line rather than adding beside it.

```toml
[defaults.pull-requests]
closed-window = "30m"

[defaults.issues]
closed-window = "30m"
```

**"Only show what other people open in this project."** Hide `me` and `bots` in each kind the project shows, inside its block:

```toml
[[projects]]
slug = "shipyard"
repositories = ["yahyabedirhan/shipyard"]
pull-requests = { authors = { hide = ["me", "bots"] } }
issues = { show = true, authors = { hide = ["me", "bots"] } }
```

For only one account's items (say a project for dependency updates), use `show` instead: `pull-requests = { authors = { show = ["@dependabot[bot]"] } }`.

**"Only show the PRs waiting on my review in this project."** Set `review-requested` in the project's pull requests. A request to one of the user's teams counts too. It leaves the project's issues and runs as they are; turn them off too for a pure review queue:

```toml
[[projects]]
slug = "shipyard-reviews"
title = "shipyard reviews"
repositories = ["yahyabedirhan/shipyard"]
pull-requests = { review-requested = true }
```

**"Show every PR waiting on my review, wherever it is."** A project with the `anywhere` group; it must list only PRs waiting on the user's review. Grouping by repository keeps many repositories readable, and `pr.review_requested` notifies each new request:

```toml
[[projects]]
slug = "review-queue"
title = "Review queue"
repositories = ["anywhere"]
pull-requests = { review-requested = true }
group-by = "repository"
subsections = true
notifications = [
  { event = "pr.review_requested" },
]
```

**"Group this project by repository, with a header for each."** Set `group-by` and `subsections` in the project's block (in `[defaults]` for every project):

```toml
[[projects]]
slug = "contributions"
repositories = ["yahyabedirhan/shipyard", "yahyabedirhan/skills"]
group-by = "repository"
subsections = true
```

For the most recently opened first, add `sort-by = "created"`; for what changed today at the top, `group-by = "date"`.

**"Keep this project short: show a few of each and let me expand."** Set `show-first` in the project's block (in `[defaults]` for every project). Each group shows that many rows and a "Show N more" row that reveals the rest until the menu closes:

```toml
[[projects]]
slug = "contributions"
repositories = ["yahyabedirhan/shipyard", "yahyabedirhan/skills"]
show-first = 5
```

**"Only show open PRs and issues here."** `states` in each kind, inside the project's block:

```toml
[[projects]]
slug = "shipyard"
repositories = ["yahyabedirhan/shipyard"]
pull-requests = { states = ["open"] }
issues = { show = true, states = ["open"] }
```

Runs work the same way: `workflow-runs = { show = true, states = ["failed", "in-progress"] }` leaves out the ones that succeeded. For every project, set `states` in `[defaults.pull-requests]` (or `[defaults.issues]`, `[defaults.workflow-runs]`) instead.

**"Switch the menu to tabs."** One key in the `[menu]` table; uncomment the header's `# [menu]` lines where the placement rule allows it. The layout button in the menu's header makes the same edit with one click.

```toml
[menu]
layout = "tabs"
```

**"Show issues for this project."** Add an `issues` override inside the project's block:

```toml
[[projects]]
slug = "e-commerce"
repositories = ["yahyabedirhan/e-commerce-frontend", "yahyabedirhan/e-commerce-backend"]
issues = { show = true }
```

To show issues in every project instead, set it once in the defaults:

```toml
[defaults.issues]
show = true
```

**"Show CI runs for this project and tell me when they fail."** A `workflow-runs` override, and a notification list that keeps the defaults `pr.opened`, `ping.sent` and `agent.notice` beside `run.failed`:

```toml
[[projects]]
slug = "shipyard"
repositories = ["yahyabedirhan/shipyard"]
workflow-runs = { show = true }
notifications = [
  { event = "pr.opened" },
  { event = "ping.sent" },
  { event = "agent.notice" },
  { event = "run.failed" },
]
```

**"Shipyard doesn't notify me about pings."** The file lists its own rules without `ping.sent` (see Overrides). Add the rule beside the ones already there, in `[[defaults.notifications]]` or in each project's `notifications` that lists its own:

```toml
[[defaults.notifications]]
event = "pr.opened"
authors = ["others"]

[[defaults.notifications]]
event = "ping.sent"
```

To keep a project's pings out of its menu, `pings = { show = false }` in its block; to keep seen pings for a week, `seen-window = "7d"` in `[defaults.pings]`. Notes work the same way: `notes = { show = false }` in a project's block keeps its notes out of the menu, and `show = false` in `[defaults.notes]` keeps every project's out unless its block says `notes = { show = true }`.

**"Show pings from my VPS."** Shipyard reaches another machine only through Herdr, so the machine must already be one of the user's Herdr saved machines; ask for its label when you don't know it, and never write a host or an address. List the label in `[remote] machines` (add to the list when it exists):

```toml
[remote]
machines = ["hetzner-vps"]
```

Then, on that machine, the user (or you, when you run there) installs the herdr-shipyard plugin, once per machine. It puts the `shipyard` command on that machine and pings for its blocked agents (see Sending pings):

```sh
herdr plugin install yahyabedirhan/herdr-shipyard
```

The plugin's page is <https://github.com/yahyabedirhan/herdr-shipyard>. Shipyard asks each machine for its pings about every 30 seconds. A machine it can't reach shows a quiet line in the menu and keeps its last pings until it answers again.

Tell the user one known limit of Herdr 0.9.3: clicking a machine's ping focuses its pane on that machine, but the Mac's Herdr window moves there only when it's already showing that machine. When it shows the Mac or another machine, the click looks like it did nothing (the ping is still marked seen); they switch Herdr to that machine themselves to see the pane. Herdr has no command yet that switches an open window to a saved machine, so no setting changes this.

**"Let my VPS's notices reach me."** Notices from another machine travel over the user's tailnet, so the Mac and the machine must both be on it, logged in as the user. Turn the listener on in `config.toml`:

```toml
[notices]
listen = true
```

The rest happens outside `config.toml`, on the Mac (`tailscale serve`) and in the machine's own `cli.toml` (`app-machine`): [references/notices.md](references/notices.md), "Receive notices from another machine", has each step and a test notice.

## Ping or notice?

Shipyard carries two kinds of message from you to the user. Pick by what the user has to do:

| | Ping (`shipyard ping`) | Notice (`shipyard notify`) |
|---|---|---|
| For | something the user should act on or would want to know now: a pull request ready for review, a question you're blocked on, a long task finished or failed | a status update that needs nothing from them: "orchestration started", "tests running", "deployed to staging" |
| What the user sees | a row in the menu that needs attention until clicked, and a notification (`ping.sent`) | a notification only (`agent.notice`): never listed, counted or kept |
| What you learn | its id; it waits for the user | exit 0 when the app showed it, or when it was queued for the Mac's poll (it says `queued`); exit 1 with why when it wasn't shown |

When in doubt, a notice: it costs the user nothing to ignore. Never both for one thing. A notice follows the user's notification rules and tells you whether it was shown, which a notification you post yourself doesn't. It works on the Mac and on the user's other machines running Herdr, and from those straight over the user's tailnet once they've set that up. [references/notices.md](references/notices.md) has the command, its flags, its routes, the exit codes and worked examples.

## Sending pings

A **ping** is a short message you send the user through shipyard: a title, an optional body and sender, and at most one action that clicking it runs (open a URL, bring an app forward, or focus a Herdr tab). It's listed under the projects that watch the repository you're working in, needs attention until the user clicks it, and posts a notification (the `ping.sent` event). Nothing reaches GitHub.

The same command works on the user's Mac and on their other machines that run Herdr with the herdr-shipyard plugin. Where you run decides how the ping reaches the user:

| | On the Mac | On another machine (a VPS) |
|---|---|---|
| How it reaches the menu | the app reads it from the Mac | the Mac asks the machine through Herdr about every 30 seconds, once `[remote] machines` names it (see Worked requests) |
| Where it's filed | under the projects that watch its repository, checked as you send; none, and it's refused (see The command) | on the Mac, under the projects that watch its repository; none, and it lists under the machine's own section (see On another machine) |
| Clicking it with no action | marks it seen | focuses your pane on that machine |
| When it leaves | after it's seen, once `seen-window` passes | 24 hours after you sent or last replaced it, seen or not |
| When you're blocked on the user | ping yourself | the plugin pings for you |

Ping when the user should act or would want to know now: a pull request is ready for review, you're blocked waiting on their answer, something they asked for is published, a long task finished or failed. Don't ping for progress along the way, or when the user is talking to you right now. Prefer one ping you replace (same `--id`) over a pile of them, and withdraw a ping once it's no longer true.

**On another machine with the plugin, waiting for input is pinged for you.** On a Linux machine where the herdr-shipyard plugin is installed (`herdr plugin list` shows `yahyabedirhan.herdr-shipyard`), the plugin pings the user by itself as soon as Herdr marks you blocked ("Claude is waiting in <tab>"), and withdraws that ping when you go on or your pane, tab or workspace closes. Don't send a ping there just to say you're waiting for input: it would be a second ping for the same thing. Ping for everything else as usual. On the Mac the plugin does nothing, so there, as on a machine without the plugin, ping yourself when you're waiting.

### The command

The app links its command at `~/.local/bin/shipyard` (onboarding, or **Set up shipyard CLI** in the panel's settings menu, the gear). When `shipyard` isn't found, run `~/.local/bin/shipyard`; when that isn't there either, ask the user to link it from **Set up shipyard CLI**, which also says what is in the way when the link can't be made. The app needn't be running: a ping sent meanwhile shows when it starts.

```sh
shipyard ping "<title>" [--body <text>] [--from <label>] [--id <id>]
                        [--open <url> | --app <bundle id or name> | --herdr [<tab or pane id>]]
                        [--repo <owner/name> | --project <name>]
shipyard ping withdraw <id>
```

| Flag | What it does |
|---|---|
| `"<title>"` | the one line the menu and the notification show; quote it, it's one argument |
| `--body <text>` | more than the title fits, shown under it and in the notification |
| `--from <label>` | who sent it, such as your name and the task (`"claude · checkout"`); `group-by = "author"` groups pings by it. Start it with your agent's name, in any case and with words after it, so the row shows its logo: `claude`, `codex`, `opencode`, `cursor`, `pi`, `gemini`, `copilot`, `amp` or `droid` (also `Claude Code`, `Codex CLI`, `OpenAI Codex`, `Cursor Agent`, `Cursor CLI`, `Pi Agent`, `Pi Coding Agent`, `Gemini CLI`, `Copilot CLI`, `GitHub Copilot`, `Ampcode`, `Factory Droid`) |
| `--id <id>` | names the ping, so you can replace or withdraw it: 1 to 64 lowercase letters, digits, `-` and `_`, starting with a letter or digit. Without it, one is made up |
| `--open <url>` | clicking it opens the URL: a page, a pull request, an artifact, or an app's deep link; the URL needs its scheme (`https://…`) |
| `--app <bundle id or name>` | clicking it brings the app forward, by name (`"Claude"`) or bundle id (`com.anthropic.claudefordesktop`) |
| `--herdr [<id>]` | clicking it focuses a Herdr tab. Alone, your own pane's tab (from `HERDR_PANE_ID`, so only inside Herdr); or a tab or pane id as Herdr prints them, such as `w1:t2` or `w1:p3`. The argument after `--herdr` is its id only when it has that shape |
| `--repo <owner/name>` | file the ping by this repository instead of the working folder's |
| `--project <name>` | file it under this one project, by its `slug` in `config.toml`, or else its `title` |
| `--` | ends the flags: everything after it is the title, even `withdraw`, `list` or a word starting with `--` |

- **One action at most.** With none, clicking the ping only marks it seen. When an action fails (the pane closed, no such app), the ping stays unseen and its row says why.
- **Where it's filed.** Without `--repo` or `--project`, the repository is the working folder's git remote `origin`, as `owner/name`, and the ping is filed under every project that watches it: one whose `repositories` names it, or brings it in through a group or `owner/*` (as the app last looked them up, so a project just added needs the app to have refreshed once). `--repo` and `--project` don't go together.
- **Output.** On success it prints the ping's id, such as `k7qm2x`, and exits 0: the id is what `--id` and `withdraw` take. The Mac numbers the ping in each project it's listed in (`#3` on its row), in the order pings arrive; a replace keeps the number. Otherwise it prints one line on standard error: exit 1 when it's refused (no project watches the repository or has that name, every project it would go under hides pings with `pings.show = false`, or `config.toml` doesn't read, which only the Mac checks; the id to withdraw is unknown), exit 2 when the arguments don't read (a missing title, two actions, a bad id, `--herdr` alone outside Herdr). The refusals list the user's projects: pick one with `--project`, or, when the repository should have its own, offer the user to watch it (see Worked requests) rather than editing the file unasked. A ping refused because its projects hide pings names them and the projects that show pings: send it with `--project` under one of those, or tell the user it couldn't reach them; the user hid pings there on purpose, so don't turn `show` back on unasked.
- **Replacing.** Sending an id that's already there replaces that ping: the new title, body, sender, action and projects, its age starting again from the replace, unseen again, with no second notification.
- **Withdrawing.** `shipyard ping withdraw <id>` takes the ping back: it leaves the menu and its notification leaves Notification Center. An id no ping has exits 1; the user may have dismissed it, or it left after being seen, so there's nothing left to do.
- **Listing.** `shipyard ping list` with `--json` prints the computer's pings as JSON, for shipyard on the user's Mac to read; you don't need it to ping.
- **Herdr's terminal.** A `--herdr` click focuses the tab in Herdr; the click also brings forward the terminal app the ping was sent from, which the CLI notes by itself. The user can name another with `[herdr] terminal` (see Keys and defaults), which wins.

### On another machine

On a Linux machine (a VPS, say) with the herdr-shipyard plugin installed, `shipyard` is at `~/.local/bin/shipyard` and takes the same flags. The user's Mac asks that machine for its pings through Herdr, when `[remote] machines` names it (see Worked requests). What differs:

- **Filing happens on the Mac.** The machine has no projects, so `shipyard ping` doesn't refuse a repository no project watches: it keeps the ping with its repository (from `origin`, or `--repo`) or its `--project` name, and the Mac files it under the projects that watch it. When the working folder has no `origin`, pass `--repo <owner/name>` or `--project <name>`; with neither, or when no project takes it, the ping lists under the machine's own section in the menu.
- **Your pane comes with it.** Sent from a Herdr pane with no action, clicking the ping focuses your pane on that machine, so you don't need `--herdr` to be found again.
- **`--open` and `--app` run on the Mac.** The URL opens in the Mac's browser, and the app is a Mac app; a `localhost` URL on the machine won't open there.
- **Pings leave after a day.** A ping leaves its machine 24 hours after you sent or last replaced it, seen or not. Replace it (same `--id`) to keep it, or withdraw it once it's no longer true.

### Worked pings

**"Ping me when the PR is ready."** Once the pull request is open and its checks pass, a ping that opens it:

```sh
shipyard ping "PR #57 is ready for review" --body "Adds the order export" --from "claude · orders" \
  --open https://github.com/my-org/shop/pull/57
```

**"Bring me back to this pane when you need me."** On another machine with the herdr-shipyard plugin, the plugin already does this when you're blocked; ping there only for what it can't see, such as a choice you want made while you keep working. On the Mac, from inside Herdr, `--herdr` alone points at your own pane. Give it an id so you can update or withdraw it later:

```sh
shipyard ping "Waiting for your input" --body "Postgres or SQLite for the cache?" --from "claude · cache" \
  --herdr --id cache-question
```

Still waiting after a while, send the same id again: the ping is updated and needs attention again, without a second notification.

```sh
shipyard ping "Still waiting for your input (10 min)" --body "Postgres or SQLite for the cache?" --from "claude · cache" \
  --herdr --id cache-question
```

**"Withdraw it when I've answered."** When the user answers (in the pane, or anywhere), take the ping back so nothing stale is left:

```sh
shipyard ping withdraw cache-question
```

**"Tell me when Claude needs me."** An action that brings an app forward, filed under a named project when the working folder isn't one of the user's repositories:

```sh
shipyard ping "Claude is asking for permission" --app Claude --project shop
```

## Driving the app

On the user's Mac, three more commands open, steer and photograph the running app, so you can see what shipyard shows, check a change, or attach a screenshot: `shipyard app`, `shipyard panel` and `shipyard screenshot`. They talk to the app directly; they need no Accessibility or Screen Recording permission, and they never change `config.toml`. One agent at a time holds them, and `shipyard control` holds shipyard for a run: see Taking turns. The command is found as in Sending pings (`~/.local/bin/shipyard`).

```sh
shipyard app open [--demo <folder>] | quit | status [--json]
shipyard panel open | close | fold <project> | unfold <project> | show-more <project> <kind> | tab <name> | view <name>
shipyard screenshot <file.png> [--appearance light|dark] [--menu-bar-icon] [--with-indicator]
shipyard control take [--wait <seconds>] [--for <purpose>] [--key <k>] | release [--key <k>]
```

| Command | What it does | Prints on success |
|---|---|---|
| `app open` | launches shipyard in the background unless it runs, and waits until it answers (about 10 seconds at most) | the status, as `app status` does |
| `app open --demo <folder>` | quits shipyard and runs it on demo data (see Demo runs) | the status, with a `demo:` line |
| `app quit` | quits shipyard and waits until it's gone | `shipyard quit` |
| `app status` | whether shipyard runs, and what its panel shows | the status (below) |
| `app status --json` | the same, as one JSON object on one line | the status as JSON |
| `panel open`, `panel close` | opens or closes the menu bar icon's panel, waiting until it has. For 30 seconds after the user closes the panel (by clicking elsewhere too), `panel open` is refused with the time it can open it again; wait for that time and don't retry sooner | `panel open`, `panel closed` |
| `panel fold <project>`, `panel unfold <project>` | collapses or expands a project's section, by its `slug` in `config.toml`, or else its `title` | `folded <project>`, `unfolded <project>` |
| `panel show-more <project> <kind>` | shows every row of the project's group of one kind past its `show-first` cap, until the panel closes; `<kind>` is `pull-requests`, `issues`, `workflow-runs`, `pings` or `notes` | `showing all <kind> in <project>` |
| `panel tab <name>` | selects a tab of the tabs layout: a project's slug or title, or `All` | `showing <title>` |
| `panel view <name>` | shows a status view in place of the projects, as the settings menu's items do: `github`, `notion`, `skill` or `cli`. `github` shows the signed-in account (`@login`) and how it connected (the GitHub CLI `gh` or Sign in with GitHub), or the sign-in steps when signed out, so a screenshot of it may show the user's login. `projects` shows the projects again, as **‹ Back** does. Closing the panel shows the projects again too | `showing <title>` (`Shipyard CLI`), or `showing projects` |
| `screenshot <file.png>` | saves the panel as it looks; a closed panel is rendered off screen without opening it (said on standard error), so `panel open` first for the panel as drawn on screen; a relative path is taken from the folder you run in | the file's absolute path |
| `--appearance light` or `dark` | draws the panel in that appearance for the screenshot, then goes back to the Mac's | |
| `--menu-bar-icon` | saves the menu bar icon alone instead of the panel, without opening it | |
| `--with-indicator` | keeps the yellow dot and the banner that show an agent is using shipyard; a screenshot leaves them out otherwise | |
| `control take` | holds shipyard for a run, until 5 minutes after you took it (see Taking turns) | `you hold shipyard until <HH:mm:ss>` |
| `control take --for <purpose>` | the same, and shows the user why on the panel's banner, in a few words (`--for "checking the header icons"`); one line, 80 characters at most. Always say why: the banner also shows each command you run as you run it ("Taking a screenshot…", then "Took a screenshot · 12s ago"), so the user can tell whether to leave the panel open | the same |
| `control take --wait <seconds>` | while another agent holds shipyard, waits in line up to that long (3600 at most), first come, first served | the same, once you hold it |
| `control release` | gives shipyard up for the next agent; does nothing when you don't hold it | `released shipyard` |

`app status` prints lines; `demo:` appears only in a demo run, `tab:` only in the tabs layout:

```text
shipyard 0.2.0 is running
lease: free
panel: closed
view: projects
layout: tabs
tab: All
projects: shop, blog
folded: none
showing all: pull-requests in shop
```

With `--json`, the keys are `running` (always `true`), `version`, `panelOpen`, `view` (`projects`, or the status view shown: `github`, `notion`, `skill`, `cli`), `layout` (`list` or `tabs`), `tab` (`null` in the list layout), `projects` (the projects, then the remote machines listing pings: the names `panel fold` and `panel tab` accept), `folded`, `showingAll` (`[{"kind":"pull-requests","project":"shop"}]`), `demo` (the demo folder, `null` otherwise) and `lease` (`null` when free, else `{"holder", "place", "secondsLeft", "waiting"}`: the agent using shipyard, as the `lease:` line names it); read it rather than the lines when you act on it.

What a command changes, it changes as the user's own click would. A fold is remembered after the panel closes, so unfold what you folded in the user's app; Show more and the panel's appearance come back by themselves. Close the panel when you're done. Never run these commands in a loop to wait for something, such as data loading: check `app status` once, and take one screenshot.

### Taking turns

Shipyard answers one agent at a time: the one holding its **lease**. Every `app`, `panel` and `screenshot` command needs it, except `app status`, which reports it. You never name yourself: `shipyard` knows you by your Claude Code session (`CLAUDE_CODE_SESSION_ID`), else by the agent process that runs it, so every command you run counts as you. Sub-agents of one Claude Code session share its session id, so they share one lease: it never makes one wait for another, so take turns between them yourself. The user sees your name and your folder (or Herdr pane) as a yellow dot on the menu bar icon and a banner on the panel, and gets a notification when you start and when you're done.

- **A quick check needs nothing more.** Your first command takes the lease and each one after renews it. It ends a minute after your last command, and 5 minutes after you took it at most; then your next command takes a new one, unless another agent was waiting.
- **Hold it for a run.** Before steps with work between them (a build, then several screenshots), `shipyard control take` holds it until 5 minutes after you took it, whatever the gaps. Taking it again doesn't move that end; a run past it takes a new lease, as above.
- **Release it at the end of every run**, after a demo's closing `app open` too: `shipyard control release`, so the next agent and the user needn't wait for it to run out.
- **A relaunch keeps it.** `app open --demo <folder>`, and the plain `app open` that ends a demo, launch the next app with your lease, until the same end. A separate `app quit` and `app open` leave shipyard free between them.
- **Look first** with `app status`: `lease: free`, or `lease: <name> in <place>, <n>s left, <k> waiting` (`lease` in the JSON).
- **Screenshots leave the dot and the banner out**, so they show shipyard as the user normally sees it; `--with-indicator` keeps them, for a picture of the lease itself.
- **When shipyard can't tell your commands are yours** (each runs as a separate process that isn't a Claude Code session, so your own commands refuse each other as "in use"), export `SHIPYARD_CONTROL_KEY=<k>` for the run, a name of your own: every `app`, `panel`, `screenshot` and `control` command then goes as `<k>`. `--key <k>` does the same for one `control take` or `release` only.

A command shipyard won't run for you exits 1 with one of these lines:

| Refusal | What to do |
|---|---|
| ``shipyard is in use by <name> in <place> until <HH:mm:ss> (<n>s left); `shipyard control take --wait <seconds>` to queue`` | Another agent holds it. Queue with `shipyard control take --wait <seconds>`, a wait long enough for its time left: it returns as soon as you hold it. Give the command a timeout longer than the wait plus 15 seconds; cut off sooner, it loses your turn. When your task can't wait that long, tell the user who holds shipyard and go on with what doesn't need it. |
| `waited <n>s; shipyard is still in use by <name> in <place> until <HH:mm:ss> (<n>s left)` | Your wait ran out. Tell the user who holds shipyard, and queue again only when they say so. |
| `the user took shipyard back; ask them before using it again` | The user pressed Stop on your banner. Stop your app control there and ask them what they want; use shipyard again only once they say so. They can allow you back at once; otherwise it refuses you for 5 minutes, `control take` included, and waiting that out, retrying or another key goes against their Stop. |

### Exit codes

- **0**: done. A screenshot is still exit 0 when the app couldn't capture its window and drew the panel itself instead: it writes that picture, prints the path, and says so on standard error, `captured by rendering: <why>`. Look at such a picture before you rely on it.
- **1**: refused, with one line on standard error saying why. Another agent holds shipyard, or the user took it back (see Taking turns). Shipyard isn't running (``shipyard isn't running; `shipyard app open` ``), or didn't answer within 10 seconds of launching. No project, kind or tab has that name; the line lists the ones that exist, such as ``no project is named `shopp`; the projects are `shop`, `blog` ``, so try again with one of them. `tab` in the list layout (``the menu uses the list layout; tabs need `[menu] layout = "tabs"` ``). `show-more` on a project not grouped by kind. `panel open` within 30 seconds of the user closing the panel (the line gives the time it can open again). A screenshot nothing could be written for, such as one into a folder that doesn't exist.
- **2**: the arguments don't read (a missing name, an unknown subcommand or option, a path that isn't `.png`, a `--demo` folder that doesn't exist); the line comes with the usage. On a machine other than the Mac, every one of these commands is exit 2 too: ``shipyard: `shipyard app` runs on the Mac, where the app is``.

### Demo runs

`shipyard app open --demo <folder>` shows shipyard with example data, for a screenshot or a check, without touching the user's setup. The folder holds a configuration at `<folder>/shipyard/config.toml`, written like the user's (everything above applies); the run keeps its own state in `<folder>/support`. It quits the user's app, launches shipyard on the folder, and every later `shipyard app`, `panel` and `screenshot` reaches the demo, with nothing more to pass. `app status` says `demo: <folder>` while it runs.

- **The user's files stay as they were.** Their `config.toml`, their state and their login item are left alone; the run writes only a small pointer file in shipyard's support folder, which the next plain `app open` removes.
- **Plain `shipyard app open` brings the user's app back**: it quits the demo and launches the user's own. Always end a demo with it, so the user is left with their shipyard running.
- **It reads GitHub as the signed-in user**, so name public repositories in a demo's configuration: what it shows ends up in screenshots. Signing out from a demo's panel would sign the user out too.
- **Pings you send meanwhile go to the user's app**, not the demo, and show there once it's back.
- **Put the folder in the user's home**, such as `~/shipyard-demo`, never in a shared folder like `/tmp`: another account on the Mac could create that folder first and answer your `panel` and `screenshot` commands in the demo's place.
- **Keep the folder's path short**: the run refuses one whose path is too long for its socket, saying `use a folder with a shorter path`.

### What it can't do

- **Click.** Rows, buttons, links and the gear menu can't be clicked, and nothing is typed into the panel: steer it only with the `panel` commands, and ask the user for anything else.
- **Hover.** Hover cards and tooltips never show in a screenshot.
- **The real menu bar.** A screenshot shows the panel, or the icon drawn on its own with `--menu-bar-icon`; the menu bar strip itself, with its count and the other apps' icons, can't be captured.
- **Another machine's app.** The commands reach the app on the Mac you run on. From another machine there's no app to drive: ask the user, or run on their Mac.

### Worked app control

**"Is shipyard running?"** Ask, and launch it when it isn't:

```sh
shipyard app status --json || shipyard app open
```

**"Restart shipyard."** Quit it, then open it again; `open` returns once it answers. Shipyard is free between the two, so another agent may take it there:

```sh
shipyard app quit
shipyard app open
```

**"Show me the panel."** Open it, and close it when you've looked:

```sh
shipyard panel open
shipyard panel close
```

**"Collapse the blog project."** By its `slug`; unfold it the same way:

```sh
shipyard panel fold blog
shipyard panel unfold blog
```

**"Show me every pull request in shop."** The group of that kind opens past its `show-first` cap until the panel closes:

```sh
shipyard panel show-more shop pull-requests
```

**"Screenshot the shop tab in dark mode."** In the tabs layout, select the tab, then capture; the path printed is the file:

```sh
shipyard panel tab shop
shipyard screenshot shop-dark.png --appearance dark
```

**"Screenshot the Shipyard CLI view."** Open the panel, show the view, capture it, then go back to the projects:

```sh
shipyard panel open
shipyard panel view cli
shipyard screenshot cli-view.png
shipyard panel view projects
```

**"Screenshot the menu bar icon."**

```sh
shipyard screenshot icon.png --menu-bar-icon --appearance light
```

**"Screenshot the panel in both appearances."** A run of steps: hold shipyard for it, waiting up to a minute for an agent that holds it, and release it at the end:

```sh
shipyard control take --wait 60 --for "screenshots in both appearances"
shipyard screenshot panel-light.png --appearance light
shipyard screenshot panel-dark.png --appearance dark
shipyard panel close
shipyard control release
```

**"Show what the user sees while you work."** The banner and the dot are yours while you hold shipyard; keep them in the picture:

```sh
shipyard screenshot lease.png --with-indicator
```

**"Screenshot shipyard with example data."** Write a demo configuration naming public repositories, run the demo, capture it, then bring the user's app back:

```sh
mkdir -p ~/shipyard-demo/shipyard
cat > ~/shipyard-demo/shipyard/config.toml <<'TOML'
version = 1

[[projects]]
slug = "swift"
repositories = ["swiftlang/swift"]
TOML
shipyard app open --demo ~/shipyard-demo
shipyard screenshot ~/shipyard-demo/panel.png
shipyard app open
shipyard control release
```
