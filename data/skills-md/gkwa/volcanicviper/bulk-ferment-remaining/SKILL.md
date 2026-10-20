---
name: bulk-ferment-remaining
description: "Report the bulk fermentation status of a Zephyr bake as one terse line, by reading the bake log and running chargingcheetah and ferment.py. The line carries elapsed time, expected total time, time remaining and the expected finish time, the initial and target dough volume, the estimated and target rise, and the average dough temperature. Use when asked about any one of those for a Zephyr key, such as how long is left on bulk, when the bulk will be done, how long it has been, what volume or rise to expect, how far along the rise is, what the dough temperature is, or how the bulk ferment is going."
---

## Bulk ferment remaining

This skill answers one question: how long until the bulk ferment is expected to finish.

It reads the start time and the initial dough volume from the Zephyr bake log, rebuilds the temperature parquet with chargingcheetah, and runs ferment.py.

It prints one line on success and says nothing else.

The line is the same whichever field the user asked about, whether time remaining, expected volume, rise or temperature, so a question about one field is answered by the whole line and never by a reworded subset.

Read the zephyr skill first for the key scheme, the bake log filenames, and the event_time tags.

## Inputs

`zephyr` is required and has no default.

It accepts only the Zephyr key form, such as `2` or `3-2`.

Anything else, including a bake log date, is an error, so say what was accepted and ask again.

`probe` defaults to `2`.

The user can override it with `1`, or with `1 2`.

The bulk start time and the initial dough volume are never typed by default.

Both are read from the bake log, as described below.

If a required input is missing, state exactly which one and ask for it, then continue once the user answers.

## Usage examples

Every example below runs the same skill and prints the same one line, whichever field the question names.

Slash command with the key:

- `/bulk-ferment-remaining 2`
- `/bulk-ferment-remaining zephyr 2`
- `/bulk-ferment-remaining Zephyr 3-2`
- `/bulk-ferment-remaining 2 probe 1`
- `/bulk-ferment-remaining 2 probes 1 2`

Slash command with no key asks which Zephyr key to use:

- `/bulk-ferment-remaining`

Time remaining and finish time:

- "What's the time left on zephyr 2"
- "How much time left on zephyr 2"
- "How long is left on bulk for zephyr 2"
- "When will zephyr 2 bulk be done"
- "What time does zephyr 3-2 finish bulk"

Elapsed time:

- "How long has zephyr 2 been in bulk"
- "How far into bulk is zephyr 2"

Volume:

- "What volume should zephyr 2 reach"
- "What's the target volume for zephyr 2"
- "What was the initial volume on zephyr 2"

Rise:

- "How far along is the rise on zephyr 2"
- "What's the expected rise for zephyr 2"
- "Has zephyr 2 hit its target rise"

Temperature:

- "What's the dough temperature on zephyr 2"
- "What's the average temp for zephyr 2 bulk"

General status:

- "How's the bulk ferment going on zephyr 2"
- "Bulk status for zephyr 2"
- "Check zephyr 2"

Probe override in a sentence:

- "Time left on zephyr 2 using probe 1"
- "Time left on zephyr 2 using probes 1 and 2"

Prompts a run can end in:

- A question with no key, such as "How long is left on bulk", asks which Zephyr key.
- A key more than 3 days from today, such as "zephyr 28", asks whether to run anyway.
- A last probe reading older than 5 minutes asks whether to run anyway.
- A log with no bulk start entry, or no measured volume, asks for the missing value.
- A log with several bulk start entries, or several measured volumes, lists them and asks which.

## Resolving the key to a bake log

Bake logs are named `bake log M-D-YYYY-N.md` and live in /Users/mtm/Documents/Obsidian Vault.

N is the bake number, taken from the key suffix, and is 1 when the key has none.

Consider every bake log whose start day equals the key day, across all months and years.

Pick the one whose start date has the smallest absolute difference in days from today, whether that date is ahead or behind.

A bake ahead of today is a valid match, because the user may refer to a bake not yet started.

If two logs are equally close, one ahead and one behind, stop, list both, and ask which.

If no log matches, stop and say which key and which filenames were looked for.

If the closest match is more than 3 days from today, ask whether to run anyway and state the date and distance, such as "Zephyr 28 resolves to September 28, 5 days back. Run anyway?"

## Bulk start time

Find the entry in the log that records the bulk ferment start, the one the zephyr skill lists as "Bulk ferment start (flour added)".

Use its `event_time` tag as the start.

If that entry has no `event_time`, use the time in the entry header.

If no entry records the bulk start, stop and ask the user for the time.

If several entries do, stop, list them with their times, and ask which.

## Initial dough volume

Find the entry in the log that records a measured initial dough volume.

If exactly one entry is found, use its value without asking, because the output line shows the volume and a wrong value is visible there.

If no entry records one, stop and ask the user for the volume in mL.

If several do, stop, list them with their values, and ask which.

Do not use the flour weight prediction unless the user supplies it.

## Running the tools

Run each command as its own Bash call.

START is the bulk start as `YYYY-MM-DDTHH:MM:SS`.

```sh
uv run --no-active --directory /Users/mtm/pdev/taylormonacelli/chargingcheetah main.py parquet --start START --probe 2 --output /Users/mtm/pdev/taylormonacelli/chargingcheetah/merged_data.parquet
```

```sh
uv run --no-active --project /Users/mtm/pdev/taylormonacelli/dreamydragonfly /Users/mtm/pdev/taylormonacelli/dreamydragonfly/ferment.py --parquet-path /Users/mtm/pdev/taylormonacelli/chargingcheetah/merged_data.parquet --meta --start START --json
```

For probes `1 2`, pass `--probe 1 2` to the first command.

The JSON carries `elapsed_minutes`, `estimated_rise_pct`, `target_rise_pct`, `avg_temp_f`, `last_temp_age_minutes`, and under `meta`, `reference_duration_minutes`, `reference_offset_minutes`, and `reference_offset_direction`.

## Run history

Every successful run appends one line to a JSONL file, so repeated runs on the same bake can be compared.

The directory comes from the environment variable `BULK_FERMENT_HISTORY_DIR`, defaulting to `/Users/mtm/Library/Logs/bulk-ferment`.

Read the variable in its own Bash call with `printenv BULK_FERMENT_HISTORY_DIR`, and use the default when it prints nothing.

The file is `zephyr-KEY.jsonl` in that directory, where KEY is the Zephyr key, such as `zephyr-5.jsonl` or `zephyr-3-2.jsonl`.

Create the directory with `mkdir --parents` before the first write.

Append with a single `printf '%s\n' 'LINE' >> FILE` call, with the absolute path to the file.

The line is one compact JSON object with these keys:

- `run_at`, the local time of the run as `YYYY-MM-DDTHH:MM:SS`
- `zephyr`, the key as given
- `start`, the bulk start as START
- `initial_volume_ml`, the confirmed initial volume
- everything the `ferment.py` JSON returned, copied verbatim

The history is written silently, and nothing about it is printed on success.

Do not append when the run stopped on an error, a missing input, or a declined stale-reading prompt.

Do append a run the user approved with "run anyway".

Nothing prunes the directory, and at roughly 300 bytes a run it stays small.

### Drift in the total

The expected total shifts from run to run as the average dough temperature changes, and the output line reports how far it has moved since the first call on that bake.

Read the history file for the key before appending the current run, so the current run is never its own baseline.

Take the earliest line whose `start` equals the current START, and call its `reference_duration_minutes` the first total.

The drift is the current `reference_duration_minutes` minus the first total.

Write it as a span in the same form as the elapsed span, followed by `shorter` when negative and `longer` when positive, then `than the first estimate of`, the first total as a span in the same form, `at`, and the 12-hour clock time of that earliest line's `run_at`.

Put the day name before that clock time only when the first run was on a different day than today.

When the drift is zero, write `same as the first estimate of`, the first total as a span, `at`, and that clock time.

When no earlier line has the current START, leave the drift out, because this run is the first call.

### Showing the history

Print the history table only when the user asks for it, such as "show the history", "table of runs", "how has the estimate changed", or "is it linear".

Print the normal line first, then the table under it.

Read the file for that key, keep the runs with the same `start`, and print one row per run in run order.

Columns, in order: run time, remaining, elapsed, rise, temperature, and the pace since the previous row.

The pace is the drop in `reference_offset_minutes` divided by the wall-clock minutes between the two `run_at` values, such as 0.97.

A pace near 1.00 means the remaining estimate is shrinking in step with real time, above it means the dough is running warm and the finish is being pulled in, and below it means the dough is running cool.

The first row has no pace and leaves that cell blank.

The table ends with a total row, plain text, leaving a cell blank when a column has no meaningful sum.

If the file has no earlier run for this start, say so in one line instead of printing a one-row table.

## Stale readings

If `last_temp_age_minutes` is more than 5, ask whether to run anyway and state the age, such as "The last probe reading is 7m old. Run anyway?"

At 5 or under, continue without asking.

## Output

On success print exactly one plain line, with no code fence so it wraps, and the Zephyr key followed by a colon, because the fields describe the state of that bake. The fields after the colon are separated by a semicolon and a space.

```
Zephyr 2: 6h09m remaining at 8:51 PM; 5h04m elapsed; 11h13m total, 40m shorter than the first estimate of 11h53m at 1:31 PM; 1,000mL → 1,711mL; 32% of 72% rise; 71°F avg
```

The fields, in order:

- the Zephyr key as given, followed by a colon
- `reference_offset_minutes` as the remaining span, then the target clock time, which is the start plus `reference_duration_minutes`
- `elapsed_minutes` as a span, such as 5h04m, or 42m under an hour
- `reference_duration_minutes` as the expected total span, in the same form as the elapsed span, followed by the word total, then a comma and the drift from Drift in the total when there is one
- the confirmed initial volume, an arrow, and the target volume, which is `(1 + target_rise_pct / 100)` times the initial volume rounded to whole mL
- `estimated_rise_pct` of `target_rise_pct`, each rounded up to a whole percent, followed by the word rise
- `avg_temp_f` rounded up to a whole degree, followed by avg

Round the rise percentages and the temperature up with the ceiling function, and never show a decimal for them.

```
⌈67.2%⌉ = 68%
⌈71.6°F⌉ = 72°F
```

The rounding is for display only.

Compute the target volume from the unrounded `target_rise_pct`, not from the rounded figure shown in the line.

Clock times are 12-hour with AM or PM.

Put the day name before the target clock time only when the target falls on a different day than today.

Numbers at 1,000 and above carry a comma, and units are squashed against the number, as in 1,711mL and 71°F.

Print nothing else on success, no preamble and no summary, except the history table when the user asks for it, as described under Run history.

## Asking with a provisional line

When the skill must ask a question and the result line can already be computed on the assumed answer, print the line first and the question under it.

Prefix the line with `Provisional:` so it is clear the line is not final until the user answers.

Provisional: Zephyr 2: 4h49m remaining at 8:44 PM; 6h17m elapsed; 11h06m total; 1,000mL → 1,705mL; 40% of 71% rise; 71°F avg

Run anyway? The last probe reading is 7m old.

When the question cannot be answered without the user, such as a missing input, print only the question.

## Errors

Any error or missing input stops the run.

Be verbose about errors, because a terse success line only works when failures are impossible to miss.

State what failed, what was tried, what is needed, and the exact command and its output when a tool failed.

If `reference_offset_direction` is `over`, the reference duration has already passed.

That case has no defined output yet, so stop and report the JSON values instead of inventing a format.
