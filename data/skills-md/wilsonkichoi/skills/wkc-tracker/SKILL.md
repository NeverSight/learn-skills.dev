---
name: wkc-tracker
description: Read and write ticket state in this project's issue tracker, whether that is GitHub Issues, Linear, or local markdown files. Use it to list, show, create, edit, assign, comment on, move, link, or unlink a ticket, and to ask what to work on next.
argument-hint: "<verb> [args]"
disable-model-invocation: false
---

# wkc-tracker

- **What it does:** reads and writes ticket state against the backend named by `issue_tracker` in
  `docs/dev-agents/config.md`: GitHub Issues, Linear, or local markdown files.
- **When to use it:** any time a skill or a person needs to see or change ticket state. Every other
  skill in this set goes through these verbs instead of touching the backend directly. Callers are
  people, models, and any `wkc-` skill that needs ticket state. A model may read on its own, but
  runs a verb that changes state only when a person, a calling skill, or an agent a person gave
  that permission asked for that change. The caller decides what changes and whether two tickets are
  related; the tracker carries the change out and keeps the dependency graph valid.
- **Dependencies:** `docs/dev-agents/config.md` with `issue_tracker` set, written by `wkc-setup`.
  For GitHub, an authenticated `gh` against a host with native issue dependencies. For Linear, the
  Linear MCP server. For local, nothing.
- **Input:** one verb and its arguments, as documented in [section 4](#4-verbs), plus the configured
  backend. The verb table explains ticket ids, text, statuses, milestones, holders, and dependency edges.
  Optional arguments keep their existing behaviour: `list` without filters returns open tickets;
  bare `assign <id>` takes the ticket. `next` needs no arguments.
- **Output:** the tickets asked for, or the changed ticket state plus its URL or file path.

## 1. Resolve the backend

Read `issue_tracker` from `docs/dev-agents/config.md`, then read exactly one backend file, all the
way through, before running anything:

- `github` → [github.md](./github.md)
- `linear` → [linear.md](./linear.md)
- `local` → [local.md](./local.md)
- `other` → no backend file. Follow the workflow the user wrote into the config body.

Stop when the config cannot name a backend: the file does not exist, it has no `issue_tracker`
field, or the value is not one of the four above. Write nothing, create no file or directory, and
read no backend file. Say so, and ask the user to run `wkc-setup` first. Never use another tool's config or ticket
format instead, even when one is in the repository. No verb here can see a ticket written there.

## 2. Statuses

| Status | Meaning |
|---|---|
| `backlog` | Captured, not committed to. |
| `ready` | Committed to and groomed. Safe to pick up. |
| `in-progress` | One session is implementing it. |
| `in-review` | The work is up and waiting on review. |
| `done` | Merged and verified. Never "merged soon". |
| `cancel` | Deliberately not doing it. |
| `duplicate` | Another ticket already covers it. |

A ticket can move between the four open statuses in any direction. Do not refuse a move because it
skips a status.

The three terminal statuses are final. No verb moves a ticket out of one or reopens it; that is a
person's decision.

A ticket with no recorded status is `backlog`.

A ticket recorded in two statuses at once is **inconsistent** and has no status. `list` and `next`
never return it as a normal ticket and never drop it silently: they name it separately, and
`move <id> <status>` repairs it.

There is no `blocked` status. Anything that blocks a ticket, other work or a decision only a person
can make, becomes its own ticket, joined with `link`. A decision ticket sits in `backlog`,
unassigned, with the question in its body. The blocked ticket keeps its status and leaves the
frontier because it has an unmet blocker. The **frontier** is the set of tickets that could be
started right now, and `next` returns it.

**A blocker is met only when it is `done`.** A `duplicate` blocker stands for its original: follow
the original, and its original when that is a duplicate too, and the blocker is met when the ticket
at the end of the chain is `done`. Every other blocker is unmet and keeps the ticket off the frontier:

- an open or inconsistent one, or one the read could not see;
- a `cancel` one, because the work was dropped, not delivered. Whether the blocked ticket still
  needs it is the caller's decision: `unlink` the edge, or `link` a ticket that will deliver the
  work. No verb reopens a ticket or deletes one;
- a duplicate whose chain cannot be followed: the original is missing or unreadable, or the chain
  comes back to a ticket already in it.

The backend file says how to read each case. Where it cannot, the blocker is unmet.

## 3. Read, write, verify

`create`, `edit`, `assign`, `comment`, `move`, `link`, `unlink`, and `milestone <name>` change state. Each runs read, write, and verify:

1. **Read.** Fetch the current state and check this verb's precondition. If it fails, write nothing
   and say why.
2. **Write.** One command where possible, so nothing is half applied.
3. **Verify.** A separate read, checked against what the backend now says. Never trust the write's
   exit code, printed URL, or response: several backend commands return success and change nothing.

When verification fails, report the verb, the ticket, what you expected, what the backend says, and
what you did about it. A verb that cannot confirm its own write has failed.

| Verb | Precondition | Verification |
|---|---|---|
| `create` | the ticket text is given. A milestone, when given, matches exactly one open milestone; otherwise write nothing and name the ones that exist. Local markdown has no milestone objects; its backend file says what it checks | the ticket exists by id, at `backlog`, with every section it was given, and in exactly the milestone it was given, or in none. The backend file says how to compare the body |
| `edit` | the ticket exists, in any status. A milestone, when given, matches as for `create`. Every added edge passes the `link` checks | everything given reads back as given, and each added edge verifies as for `link`. The title, sections, milestone, and edges not given, the status, and the assignees are unchanged |
| `link` | both tickets exist, they differ, and the edge would not close a cycle | the edge is on the blocked ticket, and the blocker's own blockers are unchanged |
| `unlink` | both tickets exist, in any status, and the edge is on the blocked ticket. Otherwise write nothing and say the edge does not exist | the edge is gone, and every other blocker of the ticket is unchanged |
| `assign` | not terminal. The bare form also needs `ready` with no assignee. Any other holder must be named | the assignee is exactly the one asked for, or nobody for `none`. The bare form also shows `in-progress` |
| `comment` | the ticket exists | the comment body is on the ticket |
| `move` | the user's words mean one of the seven statuses: its name, misspelled or in another form, or a word with the same meaning. A real word with its own unrelated meaning that shares letters with a status name means none: change nothing and ask, listing the seven. The current status is not terminal. Other people act on a status, and no verb reverses a terminal move | the backend reports the new status |
| `milestone <name>` | a name is given, and no milestone has exactly that name. An open one needs no write: report it. A closed one is a stop, because reopening it is a person's decision | the backend lists an open milestone with exactly that name |

## 4. Verbs

| Verb | Semantics |
|---|---|
| `list [status] [milestone]` | Tickets with id, title, status, assignee, and blockers. Both filters are optional. An argument that names a milestone is that milestone; otherwise it is a status. With no status, open tickets only |
| `show <id>` | One ticket in full: body, comments, labels, blockers, assignee, milestone, and a duplicate's original |
| `next` | The frontier |
| `create <ticket>` | One ticket at `backlog`, in the shape from section 5, plus its dependency edges. Everything given to `create` is the ticket. A word in it that names a status or another verb is ticket text, not a request |
| `edit <id> <changes>` | Change the title, named body sections, `## Blocked by`, or milestone. Only what is given changes |
| `assign <id> [who] [from <holder>]` | Set who holds the ticket |
| `comment <id> <body>` | Append a comment. Never edit or delete an existing one |
| `move <id> <status> [original]` | Change status, including a terminal close |
| `link <id> blocked-by <id>` | Record that the first ticket is blocked by the second |
| `unlink <id> blocked-by <id>` | Remove that one edge |
| `milestone <name>` | Create an open milestone with that name when none exists. Never rename, close, or reopen one |
| `milestone list` | Every milestone the backend holds, closed ones included. Read only |
| `milestone show <name>` | One milestone and its ticket counts by status. Read only |

**`milestone`** has three forms, chosen by the first word. `list` alone is the listing; `show`
followed by a name is the inspection; anything else is a name to ensure, and a name may contain
spaces, such as `M2: Reply handling`. To ensure a milestone named exactly `list`, or one whose name
starts with `show `, quote the whole name: `milestone "list"`.

- `milestone list` reports each milestone's name, plus its id or URL and its state where the
  backend has them. No milestones is an explicit empty result, never an error or a ticket list.
- `milestone show <name>` matches the name exactly, never a similar one. It reports the name, id or
  URL, and state where the backend has them, the total tickets, and a count for each of the seven
  statuses. `done`, `cancel`, and `duplicate` are different outcomes: never add them up as
  "completed". Tickets with no clean status are counted on their own line. An empty milestone shows
  zero tickets. For the tickets themselves, use `list <status> <milestone>`.
- Neither read writes anything. No verb closes a milestone, including when all its tickets are done.

A milestone that `show` cannot find is a stop that names the milestones that exist, like `list`.

In `list`, a milestone that matches none is a stop that names the milestones that exist, never an empty or
unscoped list.

**`next`** returns every ticket that is `ready`, has no assignee, and has every blocker met, lowest id
first. Never report an empty frontier from a read that could not see dependency edges, that came
back truncated, or that lags behind recent writes. If the backend cannot report blockers at all,
stop with an error that says so.

**An empty frontier says why.** Say the frontier is empty, then name every `ready` ticket left off
and the reason:

- its assignee, when the ticket is reserved;
- each unmet blocker, with that blocker's status and assignee. For a `cancel` blocker, say the
  caller decides whether the work is still needed. For a duplicate, give the chain and where it ends;
- a blocker list the backend truncated.

Walk each held ticket's unmet blockers through their own, a duplicate through its original, and name
any cycle as its path, such as `#12 → #14 → #15 → #12`. With no `ready` ticket at all, say so and
count the open tickets in each other status. "Nothing to do" and "everything is stuck" must never
give the same answer.

**`create`** writes the ticket at `backlog`, then one `link` per `## Blocked by` entry, or the edges
together with the ticket where the backend can. If a step fails, report the id and which edges
landed. A ticket that lands in another milestone, or in none, is a partial write: report it, and
never create a milestone or move the ticket to repair it.

**`link`** refuses a self-link. Before writing `link <A> blocked-by <B>`, start at B and follow its
blockers, then theirs, and so on. A `done` or `cancel` ticket ends that branch of the walk; a
`duplicate` one continues at its original. If the walk reaches A, refuse, write nothing, and name
the path. Run the check yourself: no backend refuses every cycle. `create` skips the walk.

**`edit`** changes only what it is given, never status, assignees, or comments. A section runs from
its `## ` heading to the next `# ` or `## ` heading, or the end of the body. Its `###` subsections
belong to it, and a line inside a fenced code block is never a heading. A given section replaces
that whole span, and a section the ticket lacks is added. A given `## Blocked by` is the new edge
set: `unlink` each current edge it no longer lists and `link` each one it adds, walking every added
edge over the edges as they will stand. A cycle refuses the whole edit, and nothing is written.
`milestone none` clears the milestone. Check every part before writing any; a part the backend
cannot write is a stop. If a step fails, report what landed.

**`unlink`** removes exactly the named edge and needs no cycle walk. Backends report success for
removing an edge that is not there, so only the read can tell. A backend with no way to remove an
edge stops with an error that says so; it never reports success.

**`assign`** has four forms. Only the bare form changes status:

| Form | What it does |
|---|---|
| `assign <id>`, `assign <id> me` | Take the ticket: requires `ready` with no assignee, and sets you and `in-progress` in one write |
| `assign <id> <who>` | Give the ticket to someone. Status unchanged |
| `assign <id> <who> from <holder>` | Take the ticket from `<holder>`. Status unchanged, also when `<who>` is `me` |
| `assign <id> none [from <holder>]` | Unassign. Needs `from <holder>` unless the holder is you |

**A `ready` ticket with an assignee is reserved.** `assign <id> <who>` on a `ready` ticket keeps it
off the frontier for that person, and `show` and `list` name the holder.

**A holder who is not you must be named.** Any form that would replace an existing assignee refuses
unless `from <holder>` names them. The write removes every holder the read found except the new one.

**The bare form's tie-break.** Check the verification read in this order:

1. A status other than `in-progress` means a person moved the ticket while you were writing. Take
   back exactly what you wrote and report. The backend file gives the command.
2. More than one assignee means another session wrote at the same time. The assignee whose login
   sorts first, compared case-insensitively, keeps the ticket. If that is not you, remove your own
   assignment, leave the status, and report.

**`move`** reads the current status first and refuses any move out of `done`, `cancel`, or
`duplicate`. `move <id> duplicate <original>` needs the id of the original ticket.

| Target | Assignees |
|---|---|
| `backlog`, `ready` | Cleared, every one of them, not only yours |
| `in-progress`, `in-review` | Unchanged. Say who holds it when that is not you, and say when nobody does |
| `done`, `cancel`, `duplicate` | Unchanged. They record who did the work |


## 5. Ticket shape

The body `create` writes and `show` expects:

```markdown
## What to build
One to three sentences on what exists when this is done.

## Acceptance criteria
- [ ] Checkable, one per line.

## Blocked by
- #12
- #14

## Related
- #31

## Notes
Spec references, with the key excerpt copied in so nobody has to fetch it.
```

`create` turns every `## Blocked by` entry into a real dependency edge, and `edit` keeps the edges equal to a `## Blocked by` it is given. `## Related` is only for readers: no verb parses it, queries it, or turns it into an edge. Write the
ids plainly and let the backend render them.

A ticket carries its title, its body sections, its `## Blocked by` edges, and a milestone. `create`
writes them and `edit` changes them. The backend records who created it. Status and assignee are
not part of a ticket: `move` and `assign` set them.

The shape is loose. Other skills may add sections, no verb rejects a ticket over formatting, and a
one-line ticket a person wrote is valid.

## 6. Rules

- The tracker owns ticket state. Never keep a parallel status file, such as `PLAN.md` checkboxes or a
  `PROGRESS.md`.
- The product docs (`prd_file`, `spec_file`, `roadmap_file`) own intent.

## 7. Report

Say what you read or changed, with the ticket URL for `github` and `linear` or the file path for
`local`. When a write only half landed, say which half and what state the ticket is in now. When a
read came back truncated or inconsistent, say that instead of reporting a result.
