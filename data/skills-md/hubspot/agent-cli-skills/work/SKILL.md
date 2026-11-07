---
name: work
description: HubSpot Work, the project and work-management product inside HubSpot — workspaces, projects, tables of items and subitems, project documents, record comments, and the AI agents that automate a table. Use this skill whenever someone wants to look at, report on, or change work their team tracks in HubSpot Work — find a tracker or board, see what's overdue, blocked or assigned to someone, add tasks, update or bulk-update statuses, mark things done, comment on or @mention someone about an item, read a project's documents, or explain what a project's agents do — even when they only say "my tracker", "the launch board", "our onboarding table" or "my tasks in Work". Not for CRM records (contacts, companies, deals, tickets, CRM tasks), CRM workflows, or HubSpot developer projects, which have their own skills.
triggers:
  - "hubspot work"
  - "work management"
  - "work table"
  - "work project"
  - "work tracker"
  - "work board"
  - "work items"
  - "mark work items done"
  - "work comments"
  - "work docs"
  - "work agents"
---

# HubSpot Work

`hubspot work --help` and each command's `--help` document the flags, input lines and output
shapes, and they are kept current. When a command rejects its arguments, its `--help` shows the
exact form; many take the id itself as an argument (`tables get 7-123`) rather than a flag. This
skill is about what you are touching and why it matters, so you can turn a request like "close out
everything Pat finished on the launch board" into the right reads, the right writes, and the right
thing to tell the person.

| To learn or change | Command (positional ids in caps) |
|---|---|
| where things live | `projects list`, `projects get PROJECT_ID` (its tables and agents), `workspaces list` |
| which table someone means | `tables search --query WORDS`, `tables list --project ID` |
| what a table's columns, options and groups are | `tables get TABLE_ID`; `tables options TABLE_ID --column NAME` for long option lists |
| what is in it | `records search --table ID` (`--filter`, `--group`, `--parent`; its `--help` has the filter grammar), `records get --table ID RECORD_ID` |
| the conversation on a record | `comments list --table ID --record ID` |
| the plan and decisions | `docs list --project ID`, `docs get DOCUMENT_ID` |
| what runs on its own | `agents list --project ID`, `agents get AGENT_ID` |
| who someone is | `users search --query NAME --table ID`, `hubspot whoami` for "me" |
| change records | `records create` / `records update --table ID` (JSONL), `records complete --table ID RECORD_ID...`, `comments create --table ID --record ID --message TEXT` |

## What Work is

Work is HubSpot's project management product: a team's plans, trackers and the automation around
them, living next to its CRM. It is in public beta, so an account may not have it yet.

```
Workspace                  a team's area ("Marketing Ops") and its sharing
└── Project                one initiative ("Q3 launch"): its tables, documents and agents
    ├── Table (7-123)      a typed tracker; each row is a record
    │   ├── Item           a row, in one group
    │   │   └── Subitem    a child row of one item, with its own columns
    │   └── Group          a bucket of items: a phase, a week, a board column
    ├── Document           the project's written context: briefs, plans, notes
    └── Agent              automation for the project: a goal plus the workflows that pursue it
```

- **Workspaces and projects are how people organize, not just folders.** A project is where a
  team keeps one initiative's tracker, its written plan and its automation together. When someone
  asks "what's going on with the launch?", the answer is spread across the project's tables
  (status), documents (intent and decisions) and agents (what runs on its own). Read all three
  before summarizing.
- **A table is a tracker the team designed.** Its columns, options and groups mean whatever that
  team decided. "Done" might be an option called "Shipped" or "Closed", "blocked" might be a status
  option or a group, and "owner" might be an assignee column or a person-type column with a custom
  label. Read the table's schema (`tables get`) before you interpret, filter or write; never guess
  internal names from labels.
- **Which option means done is the table's setting.** A team might count "Published" as done and
  "Draft done" as not. `tables get` says which: a status column's options carry `isDone`, and its
  `doneValue` is the value `records complete` writes. Count, filter and report "done" by that, not
  by what a label sounds like.
- **Groups and statuses are different things.** A group is where an item sits (a phase, a sprint,
  a board column); a status is a column value. Some teams move items between groups to show
  progress, others only change status. Look at how this table is actually used, from its groups
  and a few records, before deciding which one the person means.
- **Subitems are a second schema.** A table's subitems have their own columns (`subitemColumns`),
  separate from the items' columns. A subitem belongs to exactly one item and has no group of its
  own.
- **Agents are a project's automation.** An agent has a goal and instructions, and runs through
  workflows that fire on table events: an item created, a column changed, an item moved to a group,
  a date reached, or a schedule. `agents get` shows what triggers each workflow and what it does,
  whether it is enabled, and `pausedBecause` when HubSpot (not a person) paused it. Work's
  automation lives on Work agents, not in CRM workflows.

## Values, labels and ids

Every read gives you two views of a record. `values` are what Work stores (option values, user
ids, dates as epoch milliseconds), exactly what a write accepts back. `labels` are what a person
sees on screen. Reason and write with `values`; speak to the person in `labels`. Writing a label
where a value belongs fails, or worse, stores text nobody's filter matches.

The same split applies everywhere: column `name` (`work_col_3`) versus its label ("Due date"), an
option's `value` versus its label, a group's `name` (`group_1`) versus its label. Ids such as
`7-123` (a table) are stable handles; names are not unique and can change.

People are user ids. Owner, assignee and other person columns, and `comments create --mention`,
take a HubSpot user id from `users search`. A person is only useful on a record they can open, so
when assigning someone, scope the search to that table: an assignee who can't see the table is
still saved, with a warning, but they can't open the record until someone shares the table with
them. A person column that holds one person replaces whoever is there, so say who you'd be taking
off the record, not just who you'd be adding.
`hasWorkAccess: false` means the person has no Work access in this account at all.

## Access and absence

Every `work` command runs as the person who ran `hubspot auth login`, with their Work access: what
they can see is what you can see, and what you write is attributed to them, through the HubSpot
Agent CLI. Before calling a record "yours" or "assigned to you", check who that is (`hubspot
whoami`) rather than assuming. Service keys are refused on purpose: every Work read and write is checked against one
person's access.

- **Not finding something is not proof it doesn't exist.** Tables, projects and records the person
  can't see are left out, and table search is fuzzy. Say "I couldn't find a table called X that you
  can see" rather than "there is no table X", and offer to search by another word or browse a
  project. Notes on stderr say when a list is incomplete.
- **Read the error, it tells you what to do.** A refusal names its cause: the account doesn't have
  HubSpot Work yet (it links to the beta in Product Updates, so pass that link on), the login lacks
  Work's read or write permission (`hubspot auth login --force` and grant it), or the person can't
  access that workspace, project or table (only its owner can share it). Pass the remedy on; don't
  retry or work around it.
- **Comments run a second permission check.** Reading or editing a record works as soon as the
  person can see the table, but commenting goes through HubSpot's commenting service, which can
  take a minute or two to recognize a table that was only just created. A comment refused on a
  table the person clearly has access to is usually that delay: wait a minute and try again before
  calling it a permissions problem.

## Writes land in front of people

A Work table is shared, live team data. Changes appear immediately to everyone who can see the
table, show up in the record's activity, and can set other things in motion:

- **Writes can trigger automation.** Creating an item, changing a column, or moving an item to a
  group can fire an agent's workflow: a notification, a new subitem, an update to another record, a
  CRM write. Before a bulk change, check the project's agents to see what that change will kick off,
  and tell the person.
- **Mentions and assignments reach people.** A comment with `--mention` notifies that person, and
  an item assigned to someone lands on their My work list across every project. Write comments as
  the person would want them read, and don't mention or assign anyone they didn't ask you to.
- **Comments are permanent from the CLI.** There is no edit or delete for comments or records
  here. To remove something, send the person the record's `url` to do it in HubSpot.

That is why `records update` and `records complete` make you preview first. `--dry-run` shows each
record's current and new values and gives a digest; applying with that digest re-checks every
record, so if a teammate edited one in between, the apply refuses and you preview again. Use the
preview the way it is meant: show the person what will change (in labels, with counts), confirm it
matches what they asked for, and only then apply. When a request is broad ("mark everything done",
"move all of Pat's items"), make sure the filter matches the intent before anything changes, for
example by checking a sample of the matching records.

## Finding and reading

- **Start from what the person named.** `tables search` finds a table by words in its name across
  every project they can see; `projects list` and `projects get` let you browse when they name a
  project or don't know the table's name. `projects get` returns the project's tables and agents
  in one read; `docs list` gives its documents.
- **Learn the table before searching it.** `tables get` tells you which column holds the status,
  the due date or the owner, each option's value, and which groups exist. Then filter on stored
  values (`--filter`), not on what the labels say.
- **Some columns can't be written, and some option lists are partial.** A column marked `readOnly`
  (system fields, calculations, rollups, references that don't allow editing) rejects writes, so
  don't plan an edit to it; change its source instead, or tell the person. When a column's
  `optionsSource` is `PAGED` or `EXTERNAL` (owners, users, people, pipeline stages), `tables get`
  lists only some of its options or none: `tables options` pages and searches the full list and
  gives you each option's `value` to write and `label` to say.
- **Read all of it before you summarize.** Lists, searches and documents return a page at a time,
  and the default jsonl output prints only the rows, so a cut-off page looks complete. When the
  answer needs everything (a count, a "nothing is overdue", a summary of a plan), read with
  `--format json` and follow `meta.next` with `--after` until it is null.
- **Say what you read, and mark what you infer.** "Launch email is Blocked" is in the data; "so
  the launch will slip" is your reading of it. Keep the two apart, so the person can trust the
  facts and judge the inferences.
- **Link back.** Records, tables, documents and agents come with a `url`. Give the person links
  to what you found or changed so they can see it in HubSpot.

## Writing

- **Edit only what was asked.** Build each update line from a record's `id` and `recordType` plus
  only the `values` you mean to change; fields you leave out keep their values. Sending back a
  whole record row rewrites fields you never meant to touch.
- **Creating needs a place.** A new item needs a group (pick the one the person meant, or the
  table's first group if they didn't say); a new subitem needs its parent item.
- **Marking done is the table's notion of done.** `records complete` sets each table's own done
  status, so prefer it over writing a status value yourself.
- **One call takes up to 100 records.** Split larger changes into batches, preview each, and report
  progress in plain terms.
- **Read the write's report.** A write returns the records as they now are, plus `skipped` (already
  in that state, nothing changed) and `warnings` (such as an assignee who can't see the table).
  Tell the person about both.

## Not Work

Contacts, companies, deals, tickets and CRM tasks are CRM records, with their own skills, even
though a Work table can link to them through association columns. CRM workflows are a different
product from Work agents. HubSpot developer projects (`hs project`) are unrelated to Work projects.
