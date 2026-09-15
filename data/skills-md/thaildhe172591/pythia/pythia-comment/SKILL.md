---
name: pythia-comment
description: Use when you are about to write or edit a comment in PL/SQL you are changing, or in a .sql deliverable headed for the database. One line, one fixed shape, and anything longer goes where it belongs instead. It fires on the act of commenting rather than on a request - catching yourself opening a second comment line above one statement is the trigger.
---

# Comments - one line, or somewhere else

**Announce at start:** "Using pythia-comment — one line, date - author - what changed."

**Phase:** Do — it applies while writing, before `pythia apply` sees the file

A comment is the only part of a change no compiler checks and no test covers,
so it is the part that rots. One line survives the next rewrite. A paragraph
becomes a claim the next reader has to disprove before they can work.

## The shape

```sql
-- 11/09/2026 - jdoe - source flag reads the mapping table, not the join
```

`date - author - what changed`, with the date as `DD/MM/YYYY`. The author is
the developer's handle, never the agent's: the agent did not decide this, and
a blame trail that names a tool is a dead end.

`--` for PL/SQL and SQL. That is the whole surface this skill covers — what
pythia applies.

**ASCII only.** Parts of the chain around a .sql file still read it as ANSI,
and a diacritic there becomes mojibake in something the database keeps
forever. Vietnamese without diacritics is a house style for exactly this
reason, and it is a fine one.

## One line

If it needs a second line, the comment is the wrong container. Move it:

| What you were about to write | Where it goes |
|---|---|
| why this shape, and what breaks without it | the header block of the .sql deliverable |
| a rule that must not regress | a test or verifier, as an assertion with a message |
| the decision, and the alternatives you rejected | the spec, or the ticket |
| what changed and why, for a reader of history | the commit message |
| what the statement does | nowhere — the statement already says it |

Comment only what the code cannot show: a trap, a decision, a why.

## Do not

- Multi-line explanatory blocks above one statement.
- Banners, box drawing, `-- ==== section ====`.
- Bullet lists, quoted error codes, revision archaeology inline.
- Commented-out code kept as documentation. Delete it — the journal and the
  VCS both remember, and neither of them lies about what is live.
- Touching comments on code you are not changing. That is a different diff,
  and it buries yours.

## Before you finish

Count the comment lines you added. More than one per statement is a rewrite,
not a trim.

Then confirm the comment actually reached the database. A comment is exactly
the kind of line a second writer drops without noticing, and it costs nothing
to check:

```sql
select count(*) from all_source
 where owner = :owner and name = :name and text like :marker
```

The preview's *changed outside pythia* warning is the other half of that
check — it fires when the object moved since pythia last wrote it.
