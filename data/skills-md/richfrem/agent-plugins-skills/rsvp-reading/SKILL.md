---
name: rsvp-reading
description: Converts an input document (.txt, .md, .pdf, .docx) into a structured RSVP token stream with ORP alignment and configurable WPM. Use when a user wants to speed-read a document, prepare a reading session, or generate a token stream for a speed-reading UI.
disable-model-invocation: false
user-invocable: true
allowed-tools: Bash, Read, Write
dependencies: ["pip:docx", "pip:pdfminer"]
---
# RSVP Reading Skill

**Rapid Serial Visual Presentation (RSVP)** is a speed reading method popularized by tools like [Spritz](https://spritzinc.com/). Words are flashed one at a time in a fixed position, while one letter per word is highlighted (typically in red) as an eye anchor — the **Optimal Recognition Point (ORP)**. This eliminates horizontal eye movement, the primary bottleneck of traditional reading, enabling speeds of 200-600+ WPM with solid comprehension.

This skill converts any document into an RSVP token stream: each word paired with its ORP index and a calibrated display delay based on your target WPM.

> Full architecture: `references/architecture.md`
> Acceptance criteria: `references/acceptance-criteria.md`
> Fallback tree: `references/fallback-tree.md`
> Token stream schema: `references/token-stream-schema.md`

---

## Trigger Conditions

Invoke this skill when the user:
- Says "speed read [file]", "RSVP [file]", or "read [file] at [N] WPM"
- Uploads or references a document and asks to "read it fast"
- Requests a token stream or reading session from a document

---

## Discovery Phase

Before executing, collect:

1. **Input file path** - What file should be parsed? (`.txt`, `.md`, `.pdf`, `.docx`)
2. **WPM** - Reading speed in words-per-minute. Default: `300`. Range: `100-1000`.
3. **Output format** - Where to save the token stream JSON? Default: `./rsvp_output.json`

If any are missing, ask for them before proceeding.

---

## Execution

### Step 1: Parse the Document
```bash
python3 ./scripts/parse_document.py \
  --input <file_path> \
  --output /tmp/rsvp_words.json
```

### Step 2: Generate Token Stream
```bash
python3 ./scripts/orp_engine.py \
  --input /tmp/rsvp_words.json \
  --wpm <wpm> \
  --output <output_path>
```

### Step 3: Confirm Output
Report to the user:
- Total word count
- Estimated reading time at the chosen WPM
- Output file path
- Preview of first 5 tokens

---

## Output Format

Each token in the stream follows the schema in `references/token-stream-schema.md`:
```json
{"w": "Hello", "orp": 1, "delay_ms": 200, "is_sentence_end": false, "is_para_end": false}
```

---

## Confirmation Gate

Before generating for files > 50,000 words, display:
```
This document contains ~{word_count} words.
At {wpm} WPM this will take ~{minutes} minutes to read.
Generating token stream (~{token_count} tokens) to {output_path}.
Proceed? [yes/no]
```

---

## Next Actions

After successful generation, offer:
1. Open the reading session with the `rsvp-comprehension-agent`
2. Adjust WPM and regenerate
3. Parse a different document
