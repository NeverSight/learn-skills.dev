---
name: transcribe-voice-memos
description: "Run the full valorousverdin voice memo pipeline — transcribe the recordings waiting in the ASR queue, route the Zephyr and Fulcrum entries into the vault, file whatever no router took in the aggregate note, and leave the cleaned transcripts on the clipboard. Use when asked to transcribe voice memos, process or drain the memo queue, run the voice memo pipeline, or check how many memos are waiting. The short phrases drain memos and run memos also invoke this skill and mean transcribe and then triage."
allowed-tools: Bash
---

## Short phrases

The phrases "drain memos" and "run memos" are each a complete request, so nothing else needs to be said.

Either one means transcribe the queue and then triage what it added, in one go.

Run the pipeline as described below, and when it finishes, invoke the voice-memo-triage skill with a run scope, using the run directory this run created.

Do not ask whether to triage, because the phrase already asked for it.

The phrases "transcribe memos" and "process memos" mean the pipeline only, with no triage.

A question such as "how many memos" is a count only and starts nothing.

If the run's audit has no `leftover` lines, there is nothing to triage, so say so in one line and do not invoke voice-memo-triage.

## One script runs the whole thing

The pipeline is a shell script, and this skill runs it rather than reproducing any part of it.

```sh
/Users/mtm/pdev/taylormonacelli/valorousverdin/scripts/voice-memos.sh
```

It counts the queue, transcribes what is waiting, drives the vault routing, commits the aggregate note, and puts the cleaned transcripts on the clipboard.

What each stage does and which flags exist is documented in /Users/mtm/pdev/taylormonacelli/valorousverdin/README.md, so read that when a question goes past running it.

Never assemble the stages by hand out of `valorousverdin-pipeline` and `valorousverdin-reconcile` calls.

The script is the only place the ordering, the run directory and the router list are written down, and a hand-assembled run silently skips the reconciliation that proves no entry was lost.

## Count before running

A question about how many memos are waiting is answered without starting anything:

```sh
uv run --no-active --project /Users/mtm/pdev/taylormonacelli/valorousverdin valorousverdin-pipeline --output-dir /Users/mtm/pdev/taylormonacelli/valorousverdin/output --count
```

That prints a bare number and touches nothing.

Run it first even when the request was to transcribe, because a zero means no run is needed.

The count leaves out any recording the pipeline skipped for being over the size limit, so a zero does not mean the inbox is empty.

Check for skipped recordings after every count and every run, as described under the section on recordings skipped for size, before deciding that nothing is waiting.

The script makes the same check itself and exits zero without a word, so a run against an empty queue is harmless rather than wrong.

## Run it in the background

A run spans transcription plus three nested Claude sessions, and observed runs have taken anywhere from two to thirteen minutes.

That exceeds the foreground command timeout, so start it in the background and let the completion notification arrive:

```sh
/Users/mtm/pdev/taylormonacelli/valorousverdin/scripts/voice-memos.sh
```

Do not poll it with a shell loop while it runs, and do not start a second run to see how the first is doing.

The queue is consumed as it goes, so a second run transcribes nothing and produces an empty run directory that confounds the reporting below.

## The run directory is the record

Each run writes to a timestamped directory under /Users/mtm/.local/share/valorousverdin/runs.

Find the one the run just created by taking the newest:

```sh
ls -dt /Users/mtm/.local/share/valorousverdin/runs/*/ | head -1
```

Take that path before starting the run as well, so the two can be compared and a run that created no directory is recognised as such rather than reported from a stale one.

Inside it, `original.md` holds the cleaned transcripts, `zephyr.log` and `fulcrum.log` hold each router's own account of what it took, skipped as a duplicate, or replaced, `bake-logs.log` holds the bake log pass, and `audit.jsonl` holds the reconciliation.

Read the logs to report the run rather than inferring the outcome from the script exiting zero.

The routers are the only record of what they deduplicated, which is why their transcripts are kept.

## A run that dies partway

The script runs under `set -euo pipefail`, so a failed stage stops it where it stands and the run directory survives.

Say which stage failed, naming the last file the run directory contains, and leave the queue alone.

Do not rerun the script to clear a failure, because the recordings whose transcripts already landed have been deleted, and the half-finished run directory is the only thing that explains what happened.

## A recording skipped for size

The pipeline refuses any recording larger than the limit, which defaults to 25MB and is set by the `MAX_FILE_SIZE_MB` environment variable.

It refuses silently.

The only trace is a warning line in /Users/mtm/.local/share/valorousverdin/valorousverdin.log, while the count, the script output, `audit.jsonl` and the exit code all look like a clean run.

The recording stays in the S3 inbox, is skipped again on every later invocation, and is never transcribed.

After every count and every run, read the warnings that invocation wrote:

```sh
grep -o -E "^[0-9-]+ [0-9:]+ WARNING valorousverdin\.s3_source: Skipping [^ ]+: file too large \([^)]*\)" /Users/mtm/.local/share/valorousverdin/valorousverdin.log
```

The log repeats each warning on every invocation, so keep only the lines stamped at or after the moment this invocation started, and list each recording once.

A recording is skipped when its warning appears in this invocation, whatever the count said.

The reply must say so before anything else, ahead of the count and ahead of the outcome of the run.

For each skipped recording, name its inbox key, its size and the limit, and say that it was not transcribed.

Say that it will be skipped again on every run until it is dealt with.

Do not word this as a footnote or fold it into a sentence about the run finishing.

A run that finished with a skipped recording did not drain the queue, and the reply says that too.

Never answer nothing waiting while a skipped recording exists.

Offer the way forward without taking it:

```sh
MAX_FILE_SIZE_MB=37 /Users/mtm/pdev/taylormonacelli/valorousverdin/scripts/voice-memos.sh
```

Set the number above the recording's size in MB, and raise it for that one run only, never in a config or a profile.

The limit applies to every recording in the run, so a larger value also admits any other oversized recording waiting in the inbox.

Run it only after the user has agreed to the new limit.

A recording's duration is not in the log, only its size, so say what is known and do not guess a length.

## Reporting

The reply says whether the pipeline finished and what it did with the entries, and nothing about what the entries said.

Someone who dictated the memos already knows their contents, and the cleaned text is on the clipboard and in `original.md`, so a summary of it returns them something they already have while leaving the one thing they asked about unanswered.

Never summarise, paraphrase, quote or characterise a memo, and never list the subjects the memos covered.

A memo's own date-time heading is state rather than content, so naming one is correct where it identifies which entry went where.

## Build the report from audit.jsonl

`audit.jsonl` in the run directory holds one object per memo, carrying its heading, its outcome, the router that took it, and the absolute paths it was written to.

That file is the report, already reduced to state, and it carries no memo bodies at all:

```sh
cat /Users/mtm/.local/share/valorousverdin/runs/2026-09-18T11-36-49/audit.jsonl
```

It is also the handoff to `voice-memo-triage`, whose run scope is the `leftover` headings in this run, so a request that transcribes and then triages needs nothing carried between the two beyond this directory.

Read the router logs only when `audit.jsonl` shows an outcome that needs explaining, because those logs quote memo bodies back and reading one puts the content in front of you at the moment you are trying not to repeat it.

Even then, report what the router decided and why, never the body it decided about.

## The shape of a finished run

State the outcome as counts by disposition, then one line per entry only where an entry went somewhere a count does not identify:

```
Pipeline finished. 1 recording transcribed, 0 entries routed, 1 entry to the aggregate note.
```

Say plainly that it finished, since that is the question being asked.

Name each destination file by absolute path where a router took something, because which bake log or feed log received an entry is the part that cannot be checked at a glance.

Report duplicates skipped and existing entries replaced as counts, since those are the outcomes that silently lose work.

Do not restate the run directory path unless something in it needs reading, and do not narrate the stages while they run.

Nothing waiting and nothing skipped is a one-line reply, and nothing else.

A skipped recording is never nothing, so the reply then leads with the skipped recording, as described above.
