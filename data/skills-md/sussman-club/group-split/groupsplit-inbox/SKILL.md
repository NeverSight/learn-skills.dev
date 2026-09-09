---
name: groupsplit-inbox
description: >-
  Turn imported bank rows into GroupSplit expenses without recording the same money twice.
  USE FOR: the GroupSplit inbox, imported or synced bank rows, filing a bank row as an
  expense, reconciling a card statement against what a group already recorded, a
  POSSIBLE_DUPLICATE_EXPENSE refusal, `groupsplit inbox`, `groupsplit bank`, or
  `groupsplit transactions bank-matches`.
  DO NOT USE FOR: recording an expense somebody typed (that is `transactions create`),
  balances, settling up, or anything else in the CLI -- use the groupsplit skill.
  REQUIRES: the groupsplit skill for the JSON contract, exit codes and the confirmation
  protocol. Read it first.
license: MIT
metadata:
  author: Sussman Club
  version: "0.1.0"
---

# Filing bank rows

Two paths put an expense in the ledger: somebody types one, and somebody files a row the
bank sent. The failure this skill exists to prevent is both happening for the same money.

It goes wrong quietly. Somebody records the dinner at the table so nobody forgets it. The
card charge lands two days later, gets filed from the inbox, and the group now holds the
same dinner twice -- counted twice in every balance, twice in every total, with nothing
anywhere saying so. Whoever paid appears to be owed twice what they are, and the only way to
notice is to read the history line by line.

**Nothing here merges, hides, files or ignores anything on its own.** Every step waits for a
person. Your job is to put the choice in front of them with enough information to make it,
not to make it for them.

Read the **groupsplit** skill first: the JSON contract, the exit codes and the confirmation
protocol all apply here unchanged.

## The loop

```bash
groupsplit inbox summary --json                    # how many are waiting, and how many look filed already
groupsplit inbox list --json                       # what they are
groupsplit inbox matches <row-id> --json           # what each could already be
```

`inbox summary` answers `newCount` and `possibleDuplicates` -- how many of those waiting
look like an expense somebody has already recorded. It is worth leading with: a backlog
where none of them are duplicates is a different job from one where a third of them are.
Pass `--duplicates false` to skip that count, which is the cheaper read; the count itself
means running the matcher over every waiting row.

For each row, in order:

1. **`inbox matches <row-id>`** first, always -- before filing anything. It is a read: it
   changes nothing, and it answers the only question that matters. At most three candidates
   come back, each with `transactionId`, `name`, `amount`, `daysApart` and
   `amountDifference`, so a person can see *why* it was offered rather than take it on
   trust.
2. **Nothing came back** → file it. `groupsplit inbox file <row-id> [--group <id>]
   [--category-id <id>]`.
3. **Something came back** → show the candidates to the user with their amounts and how far
   apart they are, and ask. There are exactly three answers, and each has its own command:

| The user says | Command | What it does |
| --- | --- | --- |
| "That's the same payment" | `groupsplit inbox link <row-id> <transaction-id>` | Attaches the row to the expense that is already there. No second expense. |
| "I really did pay twice" | `groupsplit inbox file <row-id> --file-anyway` | Records it anyway. |
| "That's not it" | `groupsplit inbox dismiss-match <row-id> <transaction-id>` | Never suggests that pair again. The row stays waiting. |

Do not pick for them. The three are not interchangeable and the wrong one is not obviously
wrong afterwards.

## The refusal

Filing a row that looks like an expense already recorded fails with exit code 1 and

```json
{ "code": "POSSIBLE_DUPLICATE_EXPENSE", "error": "..." }
```

**before** a second expense exists, and the refusal names what it matched. Treat it as the
question it is: go back to `inbox matches`, show the candidates, and take one of the three
answers above.

`--file-anyway` is **not** a `--yes`. `--yes` skips a confirmation prompt; `--file-anyway`
asserts a fact about the world -- that the same amount really was paid twice to the same
merchant within days. Never add it to get past a refusal. Add it only when a user has told
you, in this conversation, that they paid twice.

## What linking does and does not do

Linking leaves one expense with the bank's row attached to it -- the same field filing would
have written -- and **no change to the amount, the date or the division**. What somebody
wrote down stays what they wrote down. A card that settled for six more than the typed
figure is not a correction anybody asked for; if the user wants it corrected, that is
`groupsplit transactions update <transaction-id> --amount <new>` afterwards, as a separate
decision they made.

## What filing copies

`inbox file` copies what the bank already said: the date, the amount, the currency. Those
have no flags here. Correcting the bank is `transactions update` afterwards.

What you may set while filing:

| Flag | |
| --- | --- |
| `--group <group-id>` | Which group. **Omit and it is personal** -- on the user's own ledger, shared with nobody. |
| `--category-id <category-id>` | Its rule is what divides the expense. |
| `--paid-by <user-id>` | Who paid, if not the user. |
| `--split <user-id>=<amount>` | Exact shares, repeatable. Omit and the category's rule divides it. |
| `--name`, `--description` | A readable name in place of `SQ *TRATTORIA 4421`. |
| `--file-anyway` | See above. |

A row filed into no group is a decision, not a default to fall back on when you are unsure
which group it belongs to. Ask.

## The other direction

An expense typed *after* the bank row arrived is the same problem the other way round:

```bash
groupsplit transactions bank-matches <transaction-id> --json
```

Answers with the rows still waiting that could be the expense just recorded. Ask it after
creating an expense in a group whose bank account is linked, and take the same three
answers.

The two directions deliberately ask about different rows. Filing is checked against any row
that can still be filed, **including an ignored one** -- filing refuses only a row that is
already an expense. Suggestions in this direction offer only rows that are still **waiting**,
because a row somebody put away is not waiting for anything.

## Putting a row away

`groupsplit inbox ignore <row-id>` takes a row out of the waiting list;
`groupsplit inbox restore <row-id>` puts it back. Neither is destructive and neither is
confirmation-gated. Ignoring is for a row that is not a group expense at all -- a personal
purchase, a bank fee -- not for a row you could not work out.

`groupsplit inbox list --status filed|ignored|new` reads back each pile.

## When the matcher fires

Worth knowing so you can explain a suggestion, or explain its absence. Two conditions have
to hold before anything is compared:

- **The payer is the same person.** A bank row is one person's card charge, so the only
  expenses it can be are ones they are down as having paid.
- **The expense has no bank row already.**

Then: within **5 days**, and within **25%** or **1.00** of the amount, whichever is more
generous -- a card charge posts days after the meal, and a tip added after the receipt was
written is the usual reason two amounts differ. At most **3** candidates are offered.

Money in another currency is not the same money, and money coming *in* -- a refund, a
deposit -- has no expense to be a duplicate of. **The bank's merchant text is deliberately
not a condition**: "Dinner" against `SQ *TRATTORIA 4421` is the ordinary case, so a name test
would refuse most real duplicates. It is a tiebreak between two otherwise equal candidates
and nothing more.

None of this catches duplicates within one side: two typed expenses for the same dinner, or
two bank rows for it. It watches the seam between the two paths.

## Getting rows in

```bash
groupsplit bank list --json                 # linked accounts and their state
groupsplit bank sync <connection-id>        # pull new rows
```

`BANK_CONNECTION_NEEDS_ATTENTION` means the user has to re-authorise with their bank; there
is nothing to retry. `bank link` and `bank unlink` are the user's to run --
`bank unlink` is confirmation-gated.
