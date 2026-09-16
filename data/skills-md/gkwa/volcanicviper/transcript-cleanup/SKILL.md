---
name: transcript-cleanup
description: Clean up raw transcripts from output/ and write to a timestamped file in cleaned/. Use when the user wants to process, clean, or tidy transcript files from the output/ directory.
allowed-tools: Read, Write, Glob, Bash
---

Process all transcript files in the `output/` directory of the current project. Follow these steps carefully:

## Step 1: Find input files

Use Glob to find all `.txt` files in `output/`. If there are no files, report that there is nothing to process and stop.

## Step 2: Parse each file

For each file, extract only the content under `=== TRANSCRIPTION ===`. Ignore the `=== SUMMARY ===` and `=== METADATA ===` sections.

## Step 3: Derive the date-time header from the filename

Each filename is formatted as `YYYY_MM_DD_HH_MM_SS.txt`. Convert this to a human-readable date-time string including the day of the week, in the format:

`## Thursday, February 26, 2026 at 2:20 PM`

Use 12-hour AM/PM time. Derive the day of the week correctly from the date.

## Step 4: Clean up each transcript

Apply the following rules to the transcription text:

- Correct all spelling errors
- Fix grammatical mistakes (subject-verb agreement, tense consistency, etc.)
- Add proper punctuation (periods, commas, apostrophes, contractions)
- Capitalize proper nouns and sentence beginnings
- Place each complete sentence on its own line
- Separate each sentence with a blank line
- Combine fragmented phrases into complete, coherent sentences
- Remove filler words (um, uh, like)
- Remove false starts and repeated words

## Step 5: Write output

Get the current date and time by running `date '+%Y_%m_%d_%H_%M_%S'` in Bash. Write all cleaned transcripts to:

`cleaned/transcripts_YYYY_MM_DD_HH_MM_SS.md`

where the timestamp comes from that Bash command. Create the `cleaned/` directory if it does not exist.

The file should contain all transcripts in reverse chronological order (newest filename first), each under its `##` date-time header, separated only by the headers (no horizontal rules).

Provide only the cleaned transcripts in the output file — no introductions, explanations, or additional commentary.

## Step 6: Verify

After writing the output file:

- Confirm the file exists and is non-empty
- Confirm the number of `##` headers in the output matches the number of input files processed

If verification fails, report the error clearly and do NOT delete any files from `output/`.

## Step 7: Delete source files

Only if verification passes, delete all the `.txt` files that were processed from `output/` using Bash.

## Step 8: Leave the source recordings alone

Do not move, delete, or otherwise touch any `.mp3` file.

The transcriber deletes each recording itself, in Python, the moment it has verified that recording's transcript is on disk.

That step used to live here, and it silently failed for months because matching a recording back to its transcript by filename is guesswork, and guesswork is the wrong thing to put in charge of deleting someone's voice memos.

Report how many files were processed and the path to the output file.
