---
name: zephyr
description: The Zephyr sourdough bake tagging scheme — key syntax, bake log filename resolution, event_time tags, weight notation, and the Starter peak duration block. Use when working with Zephyr bake logs, finding which bake log corresponds to a Zephyr key, reading Zephyr voice memo entries to extract bake events, or adding event_time tags. Also read this skill as the shared core whenever a Zephyr verb skill needs those rules.
---

## The Zephyr Scheme

"Zephyr" is a sentinel word used to tag sourdough bake voice memos.

Each voice memo related to a bake begins with "Zephyr N", where N is the day of the month the bake started.

Example: a bake started on May 28th uses the key "Zephyr 28" for all memos across the full bake cycle.

The sentinel word "Zephyr" was chosen because it is rare in baking speech, two syllables, and phonetically distinctive — speech-to-text will not confuse it with a date, number, or common word.

## Multiple Bakes on the Same Day

When multiple bakes start on the same day, a numeric suffix after a hyphen distinguishes them.

"Zephyr 3" means the first bake on the 3rd of the current month — the -1 suffix is implied and may be omitted.

"Zephyr 3-2" means the second bake on the 3rd of the current month.

"Zephyr 5-5" said in May means the fifth bake started on May 5th.

The suffix maps directly to the trailing bake number in the bake log filename.

## Absence of the Sentinel

The sentinel is a filter, not a requirement.

Most text carries no Zephyr key, and text without one is simply not addressed to this scheme.

A pass that finds no sentinel has succeeded — it did exactly what it was asked to do.

Finding nothing to act on is not a failure.

The instruction is conditional: if the text holds Zephyr entries, act on them, and if it holds none, the condition simply did not fire.

A false condition is not an error, so never report the run as failed, and never exit non-zero on account of a miss.

Say nothing about it.

Do not explain that no key was found, do not enumerate the entries that lacked one, do not restate the rule that entries without a key are never modified, and do not present the absence as a finding, a deviation, or an anomaly.

Report only what changed.

When a run changes nothing, emit nothing — no summary, no confirmation, no line announcing that there was nothing to do.

This holds for every verb skill in the scheme.

A skill that runs and finds nothing to do is in its normal state, not an exceptional one.

## Parameters

The skill accepts named parameters with defaults, like Python keyword arguments.

Resolution precedence, highest first:

1. An explicit value stated in the invocation or request
2. Machine-local configuration
3. The built-in default

Parameters:

- bake log directory — built-in default `/Users/mtm/Documents/Obsidian Vault/`; machine-local override via the `ZEPHYR_BAKE_LOG_DIR` environment variable; invocation override by naming a directory in the request

Verb skills declare their own additional parameters and resolve them by this same precedence.

Check `ZEPHYR_BAKE_LOG_DIR` with Bash at call time; fall back to the built-in default only when it is unset.

Never assume the current working directory is the bake log directory.

## Bake Log Naming Convention

This section is the single owner of bake log filename resolution.

All other components, including routing, resolve filenames through these rules rather than restating them.

Bake logs live in the bake log directory (see Parameters).

Naming pattern: `bake log M-D-YYYY-N.md`

N is the bake number for that day, starting at 1.

The suffix is not always `-1`: a second bake started the same day is `-2`, a third is `-3`, and so on.

N maps directly to the Zephyr key suffix — "Zephyr 3-2" resolves to bake number 2.

Examples:
- `bake log 5-28-2026-1.md` — first bake started May 28, 2026
- `bake log 5-21-2026-1.md` — first bake started May 21, 2026
- `bake log 6-3-2026-2.md` — second bake started June 3, 2026

## Mapping a Zephyr Key to a Bake Log

"Zephyr 28" with current date in May 2026 → `bake log 5-28-2026-1.md`.

"Zephyr 3-2" with current date in June 2026 → `bake log 6-3-2026-2.md`.

The Zephyr day number is the day of the month the bake started. Combine with the current month and year to resolve the full date. The optional suffix is the bake number; when absent, assume 1.

## Reading Zephyr Entries

Each Zephyr entry in the bake log follows this pattern:

```
For Zephyr N, [event description] at [time] on [date].
```

The header timestamp (the timestamp heading above the entry) is when the memo was recorded.

The event timestamp is the time mentioned inside the body text — this is the actual time the bake action occurred.

Always use the event timestamp, not the header timestamp, when extracting bake events.

## Entry Heading Level

Inside a bake log, entries are H3 headings nested under the `## bake log` section.

Voice memo exports deliver entries at H2, so demote each one to H3 when routing it into a bake log.

Sub-headings inside an entry body start at H4, so they stay children of the entry instead of becoming its peers.

Older bake logs whose entries predate the `## bake log` section keep those entries at H2, because there is no section in those files to nest under.

## Weight Notation

Voice memos are transcribed by speech-to-text, which spells out units as words or leaves a space between the number and the unit abbreviation.

When writing or editing Zephyr entries, normalize all weight values to compact form:

- No space between number and unit
- Use `g` not `grams`
- Use `mL` not `milliliters` or `ml`

Examples:

- "18 grams" → `18g`
- "562 grams" → `562g`
- "20 g" → `20g`
- "2190 milliliters" → `2190mL`

This applies to all weights and volumes anywhere in the entry body — ingredient amounts, dough weights, container tares, and measurements.

## Writing References to Zephyr Bakes

Never write a bare Zephyr number (e.g. "Zephyr 13") into any note or table.

A bare number is ambiguous across months — "Zephyr 13" could mean June 13 or July 13 depending on when the reader encounters it.

Always resolve the Zephyr key to a bake log wikilink before writing it into a note:

- Good: `[[bake log 5-13-2026-1]]`
- Bad: `Zephyr 13`

This applies to table cells, prose references, and any other written context.

## event_time Tags

Each Zephyr entry that records a specific bake action gets an inline event_time tag on its own line after the body text:

```
`event_time: YYYY-MM-DDTHH:MM:00`
```

Actions that get event_time:
- Feeding the starter
- Starter peaked
- Removing starter from bowl
- Mixing water with starter
- Adding tangzhong to dough
- Bulk ferment start (flour added)
- Adding salt / dimpling salt
- Stretch and fold sets
- Lamination folds
- Preshape
- Shape
- Cold retard start
- Bake start / bake done
- Inserting temperature probes

Entries that do NOT get event_time:
- General notes, reminders, or lessons learned
- Pure measurements or weight observations with no action
- Speculative or retrospective commentary

Time resolution:
- Use the time stated in the entry body when one is given
- Fall back to the header timestamp only when the body states no time
- Convert to ISO 8601: `YYYY-MM-DDTHH:MM:00`

Example entry with tag:

```
### Friday, June 5, 2026 at 9:57 AM

For Zephyr 4-2, the starter peaked at 9:57 AM on June 5th.

`event_time: 2026-06-05T09:57:00`
```

Example entry without tag (measurement only):

```
### Friday, June 5, 2026 at 10:59 AM

For Zephyr 4-2, the initial dough volume is 2100 ml.
```

## Starter Peak Duration

Each bake log contains a `## Starter peak duration` section with a YAML block:

```yaml
fed: "[TBD]"
peaked: "[TBD]"
duration_to_peak: "[TBD]"
starter_remaining: "[TBD]"
```

Fill in each field only when the bake log contains enough information to derive it.

Never guess or carry over values from a previous bake log.

| field | source | fill when |
| ----- | ------ | --------- |
| `fed` | event_time of the feed_starter entry | a feeding entry with a known time exists |
| `peaked` | event_time of the starter peaked entry | a starter peaked entry with a known time exists |
| `duration_to_peak` | elapsed time from `fed` to `peaked` | both `fed` and `peaked` are known |
| `starter_remaining` | measurement entry recording leftover starter after use | such a measurement exists in the bake log |

Format rules:
- `fed` and `peaked`: ISO 8601, `YYYY-MM-DDTHH:MM:00`
- `duration_to_peak`: `XhYm` (e.g. `11h52m`)
- `starter_remaining`: compact weight notation (e.g. `1g`)

Leave a field as `"[TBD]"` when the required information is not yet in the bake log.

## Workflow

To work with a Zephyr bake log:

1. Identify the Zephyr key (e.g. "Zephyr 28" or "Zephyr 3-2")
2. Resolve it to a bake log filename using the day number, optional bake-number suffix, and current date
3. Read the bake log and extract all "For Zephyr N" entries
4. Use event timestamps (body text), not header timestamps (the timestamp headings)
5. When writing any output that references the bake, use `[[bake log M-D-YYYY-N]]` — never the bare Zephyr number

To add event_time tags to a bake log:

1. Read the target bake log
2. For each Zephyr entry, decide if it records a specific action (see list above)
3. If yes, append the event_time tag after the last line of the body
4. Use the body time when stated; use the header time otherwise
5. Commit after all tags are added

To update the Starter peak duration block:

1. Read the bake log and locate the `## Starter peak duration` section
2. For each field, check whether the required information exists in the bake log entries
3. Fill in only the fields that can be derived — leave the rest as `"[TBD]"`
4. Commit after updating

## Components

This skill is the shared core: the scheme itself, filename resolution, weight notation, event_time tags, the Starter peak duration block, and parameter precedence.

The verbs that act on a bake log are separate skills, each independently invocable and each swappable without changing the core scheme.

| skill | handles |
| ----- | ------- |
| [[zephyr-routing]] | delivering Zephyr entries from any document to their proper bake logs |
| [[zephyr-grafana-links]] | the two dashboard links at the top of the `## grafana` section |
| [[grafana-bake-annotation]] | the `annotate-grafana.py` command blocks in the `## grafana` section |

Each verb skill consumes the rules above and does not restate them.

Read the matching verb skill when a request calls for that verb, rather than acting from this skill alone.

The `## grafana` section is shared by the last two — links at the top, annotation command blocks below.

Read whichever of those two you are invoking before touching that section, to see which part it owns.

## Applying Zephyr to a Bake Log

"Apply zephyr", or "apply the zephyr skill to this bake log", is a compound request.

It covers the bake log's whole standard state, not only the rules this skill owns.

Run these in order:

1. event_time tags on every entry that records a discrete bake action — this skill
2. the `## Starter peak duration` block — this skill
3. the two links at the top of the `## grafana` section — the [[zephyr-grafana-links]] skill

Step 3 runs even though the request never names the links.

That is what makes the request compound: naming the core skill is enough to reach the link component.

Two verbs are never included, and each stays a separate ask:

- [[grafana-bake-annotation]] — the `annotate-grafana.py` command blocks in the `## grafana` section
- [[zephyr-routing]] — delivering entries from one document to another

This is the only request that fans out across skills.

Every other request names its own verb and follows the Components table above.

## Where Measurements Go

Anything measured during a bake — tangzhong weights, dough volumes, temperatures, yields — belongs in the dated entries under the `## bake log` section, newest first.

The scaffold sections above it, such as the prophylactic buffer check, tangzhong adaptation, baker's math, and steps, describe the recipe and its formulas.

The scaffold is the plan and gets carried forward into the next bake log, while the dated entries are the observations from this one bake. Mixing measurements into the scaffold makes the plan unusable as a template.

When asked to tabulate or record numbers observed during a bake, add a new dated entry at the top of the entry list with the current timestamp, and leave the scaffold alone.

A scaffold section may cite a previous bake's outcome in prose to justify a formula choice, but never accumulates this bake's raw measurements.

## Levain Rounding

Always round up when a levain calculation produces a fractional gram. Never leave 46.5g; write 47g.

Scales cannot measure fractions of a gram, so a fractional value is meaningless in practice.

Show the rounding explicitly with ceiling notation in the math, as in `x = ⌈(278 − 19) / 2⌉ = ⌈129.5⌉ = 130g`, and use the rounded value in prose build amounts too.
