---
name: asciinema-record
description: 'Record a terminal session to a named .cast file using asciinema, trim the recording to marked content, and optionally convert it to a GIF using agg.'
---

# Asciinema Record

Record a focused terminal session using [asciinema](https://asciinema.org/), trim the raw `.cast` file to the content between `start here` / `end here` markers, and optionally render an animated GIF with [agg](https://github.com/asciinema/agg).

## Role

You are an expert in terminal recording, asciinema workflows, and developer experience tooling.

- Derive a short, descriptive filename from the task being demonstrated (e.g. a file-listing demo → `ls.cast`)
- Produce clean recordings by stripping shell preamble and teardown, keeping only the content the viewer needs to see
- Handle the full pipeline: record → trim → (optionally) render GIF
- Never overwrite an existing `.cast` file without confirmation

## Workflow

1. **Derive the cast filename** — From the task description, choose a concise snake_case name that identifies what is being demonstrated (e.g. "show directory listing" → `ls`, "install dependencies" → `npm_install`, "run tests" → `test_run`). The output file will be `./tmp/<name>.cast`.

2. **Ensure the output directory exists** — Run:
   ```bash
   mkdir -p ./tmp
   ```

3. **Start the recording** — Launch an asciinema session targeting the output file:
   ```bash
   asciinema rec ./tmp/<name>.cast
   ```
   This opens an interactive shell inside the recording session.

4. **Emit the start marker** — As the very first command inside the recorded session, run:
   ```bash
   echo "start here"
   ```

5. **Perform the demonstration** — Run the commands that illustrate the task. Keep the session focused; avoid long pauses or unrelated commands.

6. **Emit the end marker** — When the demonstration is complete, run:
   ```bash
   echo "end here"
   ```

7. **End the recording session** — Exit the recorded shell:
   ```bash
   exit
   ```
   asciinema writes and closes `./tmp/<name>.cast`.

8. **Trim the cast file** — Use the Python script in `references/trim_cast.py` to strip everything outside the markers, always preserving the header (line 1):
   ```bash
   python3 skills/asciinema-record/references/trim_cast.py ./tmp/<name>.cast
   ```
   The script rewrites the file in-place: header line + only the events between (exclusive of) the `start here` and `end here` marker lines.

9. **Render a GIF (optional)** — If the task calls for a GIF or the `agg` utility is available, convert the cast:
   ```bash
   agg ./tmp/<name>.cast ./tmp/<name>.gif
   ```
   The GIF shares the same base name as the cast file.

## Notes

- The `start here` and `end here` strings must appear as plain `echo` output in the cast; the trim script searches for them as substrings in the event data.
- If `agg` is not installed, skip step 9 and note the cast file location for the user to convert manually.
- The `./tmp/` directory should be added to `.gitignore` if recordings are not meant to be committed; add the specific files explicitly if they should be.
- See `_assets/asciinema/` for example `.cast` and `.gif` reference files.
