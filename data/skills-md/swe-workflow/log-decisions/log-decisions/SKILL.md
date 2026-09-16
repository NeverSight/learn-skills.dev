---
name: log-decisions
description: Append-only DECISIONS.md journal at the project root for consequential calls the spec didn't settle. Use when you (or the user) make a non-trivial call worth a durable record — an ambiguity you interpreted, a tradeoff, a deviation, or a hard-to-undo action.
---

# log-decisions

`DECISIONS.md` (project root) is an append-only **decision journal** for any work (code, research, writing, ops): the durable answer to *"what was decided here, and why?"*, and the reader's running list of what to confirm or revise. Throughout, the **spec** is whatever you're working from: instructions, requirements, a prompt, an ask.

## When to log, and how to decide

Significance is the gate: *if the spec already authorized the call, it's not journal-worthy; if you had to invent the authorization, it is* — put differently, from the reader's side: *would the person who gave you the spec want to know before accepting the work?* **When in doubt, log.** Log **as you work**, at the moment of the call while the reasoning is fresh — a running journal, never a reconstruction at handoff.

**Look before you ask.** Most "open" questions are already answered — search the spec, project files and docs, existing conventions, history, and earlier journal entries before treating one as needing a human. Premature escalation is the most common failure.

Then classify on two axes — **determinable** (did research settle it?) and **reversible** (cheap to undo?) — and act:

| | Reversible | Irreversible |
|---|---|---|
| **Determinable** (project / docs / convention) | decide and proceed; log + cite the artifact if it crosses the bar | decide + cite, **log, then verify** the result did what the artifact intended |
| **Needs human context** | **assume** — safe default, log, proceed | **escalate** — stop and ask |

**Hard floor:** the *catastrophic* irreversible subset — data loss, deleting or overwriting work that isn't yours, irreversible spend, sending or publishing what can't be recalled, breaking something others depend on — **escalates even when determinable.** Nothing unrecoverable happens unattended.

- **Assume** — write `Outcome: assumed`, `Chosen:` your default, `Justification:` the default rule you applied (match the existing pattern · prefer the standard, least-surprising option · prefer the choice cheapest to reverse), and **proceed**. A settled entry flagged for async review, not a blocker. When several open questions pile up, **batch them into one ask**.
- **Escalate** — write `Outcome: escalated`, `Chosen: —`, `Justification:` *why only a human can decide*, and **pause to ask a human**. It stays open until a human resolves it.

Categories (a descriptive label on each entry): `gate-resolution` (answered an open question) · `irreversible-action` (a hard-to-undo step) · `deviation` (changed existing behavior/plan) · `tradeoff` (chose X over Y at a cost).

## The entry

One append-only `##` block in `DECISIONS.md` at the project root. Create the file with an `<!-- AI-maintained, append-only -->` header if absent. **Never edit, reorder, or delete existing entries.**

```
## Q<n> — <context> — <category>

**Question:** <the decision point, paraphrased>
**Options considered:** <opt / opt>
**Chosen:** <the answer; the default you took if assumed; "—" if escalated>
**Decided-by:** agent | human            (human if a person chose, even if you surfaced the options)
**Justification:** <artifact cited by reference — or, for an assumption / tradeoff / deviation, your rationale>
**Outcome:** applied | assumed | escalated
**Ref:** <commit / PR / issue / doc, or "(pending)">
**Supersedes:** <prior Q-number> — <why>   (only on a revision)
```

`Q<n>` = the entry's sequential number (`Q1`, `Q12`, `Q13`): one more than the previous entry's, counting from the top of the file. `context` = a task ref (`auth/02`, `#57`) or a session tag (`interactive/<topic>`, `research/<topic>`, `writing/<topic>`).

**The numbering is an invariant, not just a convention:** every `Q<n>` must equal its own 1-based position among *all* entries in the file — so the sequence is monotonically increasing and continuous, with no gaps, duplicates, or out-of-order entries. "All entries" matters in a journal that predates Q-numbering: a file whose first three entries are timestamps and whose fourth is `## Q4` is correct, not broken, because the count spans both forms. **Read the file to get the next number** — never carry it from memory or an earlier read, since a concurrent session may have appended since.

Verify after appending:

```bash
awk '/^## / { i++
        if ($2 ~ /^Q[0-9]+$/) { n = substr($2,2)+0
          if (n != i) { printf "  line %d: %s is entry #%d — expected Q%d\n", NR, $2, i, i; bad++ } } }
      END { printf "  %d entries, %d break(s) — %s\n", i, bad+0, (bad?"BROKEN":"OK") }' DECISIONS.md
```

**Repairing a break.** If the check reports one, renumber the offending entry and every entry after it so the sequence is continuous again. This is the one sanctioned exception to *never edit existing entries* — the numbers are addresses, not content, and a broken sequence makes every later citation ambiguous. Two rules keep the repair safe:

- **Renumber forward only.** Close the gap by pulling later entries down; never write a number that is already in use, even transiently.
- **Update citations in lockstep.** `Supersedes:` lines — and any prose citing `Q<n>` — address entries *by number*. Renumbering a header without rewriting what points at it silently redirects the citation to a different decision, which is worse than the gap you set out to fix. Search for every mention of each number you move, not just the `##` headers, and remember a `Supersedes:` may cite a timestamp from before the migration.

Leave entry *content* untouched: change only the header number and the citations naming it. When two sessions appended at once, the later entry is the one that moves.

**Dedup / revise / reuse.** Before appending, search the journal for an existing entry with the same `(context, Question)`: same `Chosen` → do nothing (retries don't duplicate); changed `Chosen` → append a new entry with `Supersedes:` (never edit the original). A prior entry for the same question is itself a valid citation — reuse it rather than re-deciding; never bulk-load the journal.

## At handoff

When you hand the work back — end of turn, summary, PR description — list the `assumed` and `escalated` entries you appended: what to confirm or revise, what's blocked on an answer. The reader gets the review queue without opening the journal.

## Content discipline

`DECISIONS.md` persists with the project and may be read back, so keep every entry safe: **paraphrase** (your own words); **cite by reference, not payload** (name the source and section — `spec §Security` — never paste message bodies, web content, or untrusted text); **never log secrets** (tokens, credentials, PII).

## Example

A determinable call — cite the artifact that settled it:

```
## Q12 — report/q2 — gate-resolution

**Question:** Which currency should the revenue figures use?
**Options considered:** USD (audience convention) / EUR (source data) / both (cluttered tables)
**Chosen:** USD, converted at the period-average rate.
**Decided-by:** agent
**Justification:** Spec `notes/q2-spec.md §Audience` says "for the US board" without naming a currency; took the audience's convention.
**Outcome:** applied
**Ref:** (pending)
```
