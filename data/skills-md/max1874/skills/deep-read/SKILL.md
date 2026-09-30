---
name: deep-read
description: Reads a long source (course or podcast transcript, SRT/VTT subtitles, long article, meeting notes, long PDF) line by line to the end, without skimming, sampling, or summarizing from impressions, and leaves a coverage record proving every line was read. Use when the user says "read it all", "don't skip anything", "go through it properly", or hands over tens of thousands of words to distill, take notes on, or answer detailed questions about.
---

# Deep read

## Why this exists

When an agent reads a long source, it often misses content without noticing, then writes a summary that looks complete:

| How content gets missed | What actually happens |
|---|---|
| A read is too big and errors | Read fails once a single call returns more than ~25k tokens; the agent falls back to grep or the first screen, and the rest is never read |
| A line too long to split | offset/limit split by line. Transcripts often put a whole paragraph on one line, and a file with no line breaks is a single line; if one line exceeds the limit, there is no way to chunk it |
| Line cap | Read returns the first 2000 lines by default; everything after is silently dropped |
| Sampling passed off as reading | Head, tail, and a few grep hits, then straight to the summary |
| Delegating to a subagent | The subagent returns its own summary; the main agent never saw the source |
| Writing from memory | Reading everything first and recalling later loses early details, and context compaction erases even the impressions |

Real case: a 3-hour YouTube course transcript (~41k words, ~54k tokens, too big for one read). Read in 4 chunks with this workflow, it surfaced things a sampled read would not: the same community size stated two different ways, `$6.41` transcribed as `$641`, a topic promised in the intro and never covered, and an explanation promised mid-course and never given.

## Rules

- **Read it yourself; never delegate the reading.** Subagents may look up outside facts (who the author is, the publish date), but reading and distilling the source is the main agent's job.
- **No conclusions until every line is read.** grep, head/tail, or "picking the key paragraphs" never substitute for reading.
- **Write notes after every chunk.** Write that chunk's notes to a file before reading the next one, so progress survives context compaction.
- **Every chunk must be readable.** Keep lines short in the reading copy, so the source can always be split into chunks under the limit.

## Workflow

### Step 1: Prepare a reading copy

Run the script in this skill's directory (path relative to the skill directory; Python 3 standard library only):

```bash
python3 scripts/prepare.py <file> --out <scratch dir>
```

- `.srt` / `.vtt`: strips cue numbers and timestamps, merges the repeated lines of rolling captions, writes `transcript.txt` as paragraphs each starting with `[HH:MM:SS]`, then builds `read.txt` from it.
- Other plain text: builds `read.txt` directly, keeping existing blank lines.
- The script prints the longest original line, line count, estimated tokens, and the Read parameters for each chunk.
- The two defaults:
  - **Lines of at most 200 characters**: any source can then be split by line, and one line holds only a sentence or two, so notes can cite the source by line number precisely.
  - **Chunks of about 15k tokens**: Read errors above ~25k tokens. Chunking by characters failed in practice: 60k Chinese characters came to ~64k tokens. The script estimates about 4 English characters per token and 1 CJK character per token, with margin. If Read still reports the limit, lower `--chunk-tokens` and rerun.
- PDF: if it has a text layer, convert with `pdftotext -layout` first, then run the script. `pdftotext` ships with poppler (`brew install poppler` on macOS, `apt install poppler-utils` on Debian/Ubuntu). For scanned PDFs, or without poppler, use Read's `pages` parameter, up to 20 pages per call, in page order.
- Web pages / HTML: extract plain text first, then run the script.

Keep the reading copy in a scratch directory, not in the repo.

### Step 2: Read chunk by chunk

- Follow the script's offset/limit plan in order. Each chunk starts at the previous chunk's last line + 1, with no gaps.
- If the source is too big for one session (roughly 150k+ tokens), spread it over several sessions. Record "read up to line N" at the top of the notes file and resume from there.

### Step 3: Write notes after each chunk

Organize notes in source order, marking each section with its timestamps or line range so the source can be checked. For each chunk, record at least:

- **Content**: claims, steps, examples, settings, numbers. Record numbers as stated, marked "as stated by the author, unverified".
- **Recognition errors**: speech-to-text or OCR mistakes, collected in a "as written → actually means" table, e.g. `claw` → Claude. Never edit the source; map it in the notes.
- **Contradictions**: the same thing stated two different ways. Mark with ⚠️ and note where each occurs.
- **Unkept promises**: "I'll cover this later" / "I'll explain why" with no follow-through. Log each promise when you meet it, then check them all once the whole source is read; mark unkept ones with ⚠️.

### Step 4: Wrap up

- Put a **coverage statement** at the top of the notes: which file, how many lines after wrapping, how many chunks, and each chunk's line range. This is the evidence that everything was read.
- **Keep the source and your judgment apart**: what the author said goes in the body; your own views go in a separate "my take" section.
- In the reply, give the coverage statement first, then conclusions, then the ⚠️ items.

## Don't

- Don't hand in a "roughly, it covers…" summary without a coverage statement.
- Don't skip Step 1 and read the original file directly. Even if it fits in one read, you get no chunk plan and no line numbers, so the coverage statement has nothing to stand on.
- Don't clean up the source to make it look tidy; map recognition errors in the notes only.
- Don't present your own inferences as the author's words.
