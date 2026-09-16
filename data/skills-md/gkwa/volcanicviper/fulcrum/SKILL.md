---
name: fulcrum
description: The Fulcrum sourdough starter feed tagging scheme — trigger grammar, monthly feed log resolution, relative time resolution, and routing feed entries into the starter feed log. Use when working with Fulcrum entries, reading Fulcrum voice memo entries to record a starter feeding, or routing feed entries to a starter feed log.
---

## The Fulcrum Scheme

"Fulcrum" is a sentinel word used to tag sourdough starter feeding voice memos.

Each memo recording a feed opens with "For Fulcrum", followed by what was fed.

Fulcrum routes feeds to a starter feed log the way [[zephyr]] routes bake events to a bake log.

Without it a feed memo carries no key, so the voice memo pipeline files it as a one-off research note, which is the wrong home for a recurring maintenance record.

## No Key

Fulcrum takes no number, unlike a Zephyr key.

Starter feeding is continuous maintenance rather than a bounded episode, so there is no bake to identify.

The destination follows from the date of the feed itself, which is why the sentinel stands alone.

Example: "For Fulcrum, we fed the starter 25g of arachnophobia blend along with 25g of water."

## Trigger

Having no numeric key, Fulcrum cannot lean on a number to separate a real entry from incidental speech the way [[zephyr]] does.

Two conditions must both hold:

- "For Fulcrum" opens the sentence
- That same sentence states a feeding

Shapes that do NOT trigger:

- "For Fulcrum to route this correctly, we need..." — a purpose clause, not a feed
- "We should add a rule to Fulcrum" — talk about the scheme itself
- Any sentence where "Fulcrum" appears somewhere other than the opening words

Route only when explicitly asked, never automatically because a document happens to be open.

## Parameters

Resolution precedence follows the Parameters section of the [[zephyr]] skill.

- feed log directory — built-in default `/Users/mtm/Documents/Obsidian Vault/`; machine-local override via the `FULCRUM_FEED_LOG_DIR` environment variable; invocation override by naming a directory in the request

Check `FULCRUM_FEED_LOG_DIR` with Bash at call time, and fall back to the built-in default only when it is unset.

Never assume the current working directory is the feed log directory.

## Feed Log Naming Convention

Naming pattern: `starter feed log M-YYYY.md`

One log per calendar month, because feeding runs about twice daily and a perpetual log would outgrow the file.

M is not zero padded, matching the bake log convention.

Example: `starter feed log 9-2026.md`

The month and year come from the resolved event time of the feed, never from the memo header, since an offset can carry a feed back across midnight into the previous month.

## Time Resolution

Resolution precedence, highest first:

1. An absolute time stated in the body, as in "we fed at 7:15 PM"
2. A quantified relative offset, as in "30m ago", "an hour ago", "two hours ago"
3. The memo header timestamp

An offset subtracts from the header timestamp, so a memo headed 7:45 PM saying "30m ago" resolves to 7:15 PM.

Subtraction can cross midnight, moving the date back a day and with it the target month.

Parse only an offset that states a quantity.

Vague references such as "earlier" or "this morning" carry no quantity, so fall back to the header timestamp rather than inventing an interval.

## Resolve the Offset into the Body

A relative offset means something only at the moment of recording.

Rewrite it as the absolute time it resolves to, so the entry still reads correctly months later.

"We did this 30m ago." becomes "We fed at 7:15 PM."

This matches the [[zephyr]] entry grammar, where the body states an absolute time and the `event_time` tag agrees with it.

## Entry Structure

Entries live at H3 under a `## feed log` section, newest first.

Voice memo exports deliver entries at H2, so demote each one when routing it in.

Sub-headings inside an entry body start at H4, so they stay children of the entry.

Every Fulcrum entry gets an `event_time` tag, because a feed is always a discrete action:

```
`event_time: YYYY-MM-DDTHH:MM:00`
```

Unlike a bake log, there is no category of Fulcrum entry that goes untagged.

## What to Record

Record only what the memo states:

- the flour weight and which blend
- the water weight
- the starter weight carried forward, when stated
- the jar or container, when stated

Never infer an unstated amount from a previous feed.

Never complete a ratio the memo left partial.

## Normalization

Apply the weight notation rules from the [[zephyr]] skill, so `25g` rather than "25 grams".

Speech-to-text renders a blend name as an ordinary noun, so normalize it to its note name followed by the word blend.

"Arachnophobia mix" becomes `[[arachnophobia]] blend`, matching how the bake logs already write it.

## Boundary with Zephyr

Bake logs already record a feed, in the `fed` field of the `## Starter peak duration` block, which the [[zephyr]] skill owns.

The spoken sentinel decides where a feed lands, and nothing else does:

- "For Zephyr N" — a levain or starter build belonging to that bake, filed in the bake log
- "For Fulcrum" — a maintenance feed, filed in the feed log

Never file one entry in both places.

Never infer the other sentinel from context.

A feed that genuinely belongs to both gets two memos.

## Absence of the Sentinel

Follows Absence of the Sentinel in the [[zephyr]] skill without exception.

A pass that finds no Fulcrum entry has succeeded, changes nothing, and says nothing about it.

## Routing

Steps, once the trigger conditions are met:

1. Identify each Fulcrum entry — a timestamp heading plus the body below it, up to the next heading
2. Resolve its event time
3. Resolve the target month from that event time
4. Create the log if it does not exist, scaffolding only frontmatter tagged `sourdough` and a `## feed log` section
5. Normalize, demote to H3, and insert in reverse chronological order
6. Add the `event_time` tag

Entries without the sentinel are never touched, moved, or modified.

Mode is `move` or `copy`, default `move`, as in [[zephyr-routing]].

In move mode, remove each entry from the source document once it lands in the target.

Skip an entry when the target already holds one with the same event time and the same normalized body.

## Commit

Commit each modified feed log, one commit per file.

Commit the source document as its own separate commit.

## Worked Example

Source entry, as the voice memo pipeline delivers it:

```
## Tuesday, September 15, 2026 at 7:45 PM

For Fulcrum, we fed the starter 25g of Arachnophobia mix along with 25g of water.  We did this 30m ago.
```

That resolves to `starter feed log 9-2026.md`, under `## feed log`:

```
### Tuesday, September 15, 2026 at 7:45 PM

For Fulcrum, we fed the starter 25g of [[arachnophobia]] blend along with 25g of water.

We fed at 7:15 PM.

`event_time: 2026-09-15T19:15:00`
```

The heading keeps the recording time, while the body and the tag carry the feed time.

## Shared Rules

Weight notation, the `event_time` tag format, and the silence rule are generic to any sentinel scheme, but they live in the [[zephyr]] skill today, so this skill reads them from there.

That leaves Fulcrum depending on a bake-specific skill for mechanics that are not bake-specific.

Extracting them into a core skill both consume would remove the dependency, and is worth doing if a third sentinel arrives.
