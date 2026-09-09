---
name: groupsplit
description: >-
  Drive the GroupSplit CLI (`groupsplit`) to read and change shared expenses: groups,
  members, expenses, balances, settlements, split rules, categories, invitations, linked
  bank accounts and imported bank rows.
  USE FOR: splitting an expense with a group, who owes whom, settling up with one person
  across every group at once, recording what somebody paid, a group's ledger or totals, what
  you have paid and what it cost you month by month, inviting or removing members, join
  links, filing an imported bank row; or whenever a `groupsplit` binary or a
  `~/.config/groupsplit/config.json` is present.
  DO NOT USE FOR: working on the GroupSplit codebase itself -- builds, tests, Aspire, EF
  migrations -- which is ordinary repository work; or other expense trackers.
  COVERS: the JSON contract, the exit-code table, the exit-4 confirmation protocol that
  gates every destructive change, and token auth with no browser.
  ROUTES TO: groupsplit-inbox, for turning imported bank rows into expenses.
license: MIT
metadata:
  author: Sussman Club
  version: "0.2.0"
---

# GroupSplit from the command line

`groupsplit` is the terminal client for GroupSplit. It was built to be driven by a program
as much as by a person: JSON is the default whenever stdout is not a terminal, the exit
codes are a contract, and destructive commands describe themselves rather than blocking on
a prompt nobody can answer.

Everything below is the protocol around the CLI. The CLI's own surface comes from the
CLI, not from here.

## Start by reading the schema

```bash
groupsplit schema --json
```

One call returns the whole command tree -- every command, argument, flag, type, arity and
the exit-code table. It is generated from the same tree that parses the arguments, so it
cannot describe a CLI that does not exist, and it is right for the version that is actually
installed.

**Read it once per session and plan from it.** Do not shell out to `--help` per subcommand,
and do not pass a flag it does not list: this skill was written against one version and the
schema is the one that is in front of you.

If `groupsplit` is not on `PATH`, or no server is configured, see
[references/setup.md](references/setup.md) before going further.

## The loop

1. `groupsplit schema --json` once.
2. Run each command with `--json`. It is the default when stdout is redirected, but say it
   anyway -- you are not always the thing holding the pipe.
3. Branch on the **exit code** first, then on the envelope's `code`.
4. On exit code 4, stop and show the user what would change. Do not decide for them.

```bash
groupsplit groups list --json
groupsplit transactions list --group <group-id> --json --fields id,name,amount,date
```

`--fields` keeps only the named top-level fields, of an object or of every element of an
array. Use it: a full expense list is mostly fields you did not ask about.

## Exit codes

| Code | Meaning | What to do |
| --- | --- | --- |
| `0` | Success. stdout is trustworthy. | Parse stdout. |
| `1` | A general failure. | Read `code`; retrying may help. |
| `2` | Not signed in, expired, or refused. | See [setup.md](references/setup.md). Do not retry the same call. |
| `3` | The invocation was wrong, or no server is configured. | **Retrying will not help.** Fix the arguments. |
| `4` | A mutation needs confirming. | Surface it. See below. |

stdout carries the result and nothing else. Progress, warnings and errors are on stderr, so
capture the two separately -- a warning folded into stdout will break your JSON parse.

## Confirming a destructive change

Fourteen actions stop unless confirmed: `groups.remove-member`, `groups.settle`,
`groups.settle-up`, `settle.pay`, `groups.leave`, `groups.link.create` (when a link already
exists), `groups.link.revoke`, `transactions.delete`, `categories.delete`,
`split-rules.delete`, `merchants.update` (only when it renames -- a merchant is shared by
every group that has spent there, so the prompt carries the count), `merchants.delete`,
`bank.unlink` and `users.delete`.

With no terminal you get exit code 4 and this on stdout:

```json
{
  "confirmationRequired": true,
  "action": "groups.leave",
  "summary": "Leave the group 'Trip to Lisbon'?",
  "changes": ["You are removed from 'Trip to Lisbon' (4 members)."],
  "confirmCommand": "groupsplit groups leave 3f25... --yes"
}
```

**Show `summary` and every line of `changes` to the user, and wait for them to agree.** Then
run `confirmCommand` verbatim -- it is the exact invocation, so you never have to
reconstruct one from your own history.

Do not put `--yes` on a command yourself. The flag exists for a caller who has already been
told what it does; reaching for it to avoid a round trip performs a deletion nobody asked
for. The one exception is a user who has said, in this conversation, to go ahead with that
specific action.

## Errors

Failures print an envelope on stderr:

```json
{
  "error": "No group with that id.",
  "code": "GROUP_NOT_FOUND",
  "remediation": "Check the id. List what you can see with: groupsplit groups list",
  "traceId": "00-a1b2c3-d4e5f6-01"
}
```

Branch on `code`, never on `error` -- the prose may be reworded. A `CLI_` prefix means the
CLI refused before any request was sent; anything else came from the server and means the
request was understood and refused. `remediation` is written to be acted on. Pass `traceId`
along when reporting a problem.

## Rules

- **Never invent an id.** Every id in this system is a uuid that came from a listing. List
  first, then act on what you were given.
- **Amounts have two decimal places** and the currency is the group's. Do not round a
  user's figure to make a split come out even -- `--preview` instead, below.
- **Preview a split before creating it** when the division matters:
  `groupsplit transactions create "Dinner" 84.20 --group <id> --preview` shows the split the
  server would apply and creates nothing.
- **Do not print the output of `groupsplit auth token`.** It is a bearer token. It is for
  piping into another tool, not for a transcript.
- **Settle with a person, not a group.** `groupsplit settle plan` is the answer to "how do
  I clear this?": it adds every group's balance up per person, so one payment clears a
  friend you owe in two places. `groups settle` is still right when the user means one
  group specifically.
- **`groupsplit config list`** answers what the *next* command will talk to, and says which
  source each value came from. Run it before wondering why a request went somewhere
  unexpected.
- Set `GROUPSPLIT_DEBUG=1` to attach a stack trace to an unexpected error. An envelope with
  code `CLI_INTERNAL_ERROR` is a defect in the CLI, not a usage mistake -- report it rather
  than working around it.

## Where to look next

| You need | Read |
| --- | --- |
| The full command surface, and the flag formats that are not obvious | [references/commands.md](references/commands.md) |
| Installing, pointing at a server, signing in, profiles, the local stack | [references/setup.md](references/setup.md) |
| The machine contract in full: output, envelopes, the error-code catalog | [references/protocol.md](references/protocol.md) |
| Turning imported bank rows into expenses without recording anything twice | the **groupsplit-inbox** skill |
