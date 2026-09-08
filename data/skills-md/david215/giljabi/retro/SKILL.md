---
name: retro
description: Turn the friction lines in retro/inbox.md into skill diffs — one proposal per item with file:line evidence, applied on approval, the routed lines deleted. Run in the giljabi repo whenever the inbox has entries.
disable-model-invocation: true
---

# Retro

Skills never edit themselves; this is the one place they change. Each `[friction]` line in
`retro/inbox.md` names a moment a skill fought its user. The run turns each into **one proposed
diff**, applies it on approval, and deletes the line — so the inbox is empty when the run ends and
the skills carry every lesson that survived scrutiny.

Load `/writing-for-agents` before touching any skill text. Every diff it produces is judged by that
skill's rules — positive phrasing, no-op test, single source of truth, leading words over
restatement — and a diff that fails them is redrafted, not applied.

## 1. Read the inbox, then the skills it names

Read `retro/inbox.md` whole. For each item, open the skill(s) it names and find the **exact lines**
the item is about — the step that was skipped, the rule that misfired, the sentence that was read
two ways. Quote them as `skills/<name>/SKILL.md:<line>`. An item that names no skill is traced to
the skill whose step was running when the friction happened.

Then read `docs/design.md`: a fix that contradicts one of its entries is not a wording fix but a
reversed decision, and is handled as one (step 3).

## 2. Classify every item

Take the first that fits:

| Class | Test | Action |
| --- | --- | --- |
| **landed** | the current skill text already says what the item asks for (a previous run or commit fixed it) | cite the line; delete the item |
| **repo fact** | the fix could differ per repo (a DB URL, a template path, a merge strategy) | no skill diff; state which `docs/agents/` file in the *target* repo should carry it, and whether `/setup` should ask for it — that last part is a skill diff |
| **reversed decision** | the fix contradicts a `docs/design.md` entry, or two items pull one skill in opposite directions | step 3 |
| **skill diff** | the skill said the wrong thing, said it ambiguously, or left a step unnamed | step 4 |
| **drop** | a one-off with no rule behind it, or the fix would be a no-op the agent already does | say why; delete the item |

Two items with one root cause are one diff; say which items it closes.

## 3. Reversed decisions go through a grill round

A reversed decision is the user's call, and the argument for the old shape is written down. Run it
as one `/grill` frontier round: the `docs/design.md` entry's reasoning, the friction that contradicts
it, the options with what each costs, your recommendation first — on both surfaces, prose and the
harness's structured question. The outcome rewrites the `design.md` entry (or deletes it) **in the
same diff** as the skill change; a skill whose design note argues for the shape it no longer has is
two homes disagreeing.

## 4. Draft the diff

For each skill-diff item, the proposal is:

- the item, verbatim;
- the current text at `file:line`;
- the replacement text, complete — a reader approves what will land, not a description of it;
- one line on why this wording and where else the same meaning lives (it must not).

Placement follows the three tests in `README.md`: method identical in every repo → the skill; could
differ per repo → the target repo's docs, via `/setup`; governs sessions that never invoke a skill →
the user's rules file, which this repo does not own — name it and stop. A line that fits nowhere is
dropped, not homed.

Where an item says a decision was asked "in prose", the fix names the **structured-question
capability** (`/giljabi`'s harness map), not one harness's tool.

## 5. Approve, apply, verify

Present every proposal, grouped by skill, before applying any. Approval is per item through the
structured question — recommendation first; "apply all" is an option only when every item in the
batch is a skill diff with no reversed decision behind it. A declined item is deleted from the inbox
with its reason appended to the proposal record in this conversation; it is not carried forward.

Apply the approved diffs, then:

```bash
./check.sh                       # names, metadata, plugin.json, skill references
git diff --stat
```

Delete every routed line from `retro/inbox.md`, leaving the header. One `/commit` per skill touched
when the diffs are independent; one commit when a reversed decision spans skill and `design.md`.

## Report

One list, one line per item: class, the diff applied or the reason declined, the commit. Nothing
about items that landed cleanly beyond the line.
