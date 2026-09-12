---
name: jargon-extractor
description: "Extract internal terminology, acronyms, shorthand, and jargon from a set of documents, then build or update a project glossary in JARGON.md. Reuse an existing JARGON.md anywhere in the repo if one already exists; otherwise default to the repo root. Spawns one subagent per input file to flag terms with plain English definitions, then a single reduce subagent correlates, deduplicates, and alphabetizes the combined results, intelligently merging any overlapping definitions before writing them into the glossary. Use this skill whenever the user asks to extract jargon, build or update a glossary, catalog acronyms, document internal terminology, flag undefined terms, or mentions a JARGON.md file by name, even if phrased casually, for example 'go through these design docs and pull out anything a new hire wouldn't know' or 'scan this repo's markdown files and build a term list.' Also trigger when the user hands over several documents and asks what specialized vocabulary or shorthand appears across them."
license: Apache-2.0
metadata:
  author: accelint
  version: "1.0.0"
---

# Jargon extractor

Reads a set of documents, flags the internal terminology, acronyms, and jargon a new reader would not know, and maintains a single alphabetized `JARGON.md` glossary across runs.

The work splits into three phases with different failure modes and different homes. Extraction is judgment-heavy: deciding whether a word counts as jargon depends on reading the document. Correlating and merging is also judgment-heavy: deciding whether two definitions describe the same concept. Filing is mechanical: sorting, deduplicating, and writing the file correctly every time. Extraction and merging happen in disposable subagent contexts that report back only a short summary; filing is a deterministic script that reads and writes files directly on disk without needing their contents echoed into any model's context at all. The orchestrator's own context only ever holds file paths and small counts, never the bulk of the extracted terms.

Both extraction and merging run as subagents, but only once each per run, not once per wave.

## Execution flow

```
wave 1 (up to 5 files)        wave 2 (up to 5 files)      ...
+---------+  +-----------+    +---------+  +-----------+
| file A  |->| extractor |    | file F  |->| extractor |
+---------+  +-----------+    +---------+  +-----------+
     ...          ...              ...          ...

each extractor writes its findings to a file and returns only a
one-line confirmation; waves run one after another, capped at 5
concurrent extractors at a time, purely to bound concurrency

once every wave has finished:

  all extraction file paths            +---------+     +--------------------+
  + the glossary path        ------->  | reducer | ---> | merge_jargon.py    |
                                        | (whole  |      | upserts into        |
                                        |  run)   |      | chosen JARGON.md    |
                                        +---------+      +--------------------+

  the reducer reads every extraction file and the current glossary
  itself, correlates and merges once across the whole run, and
  writes one entries file plus a short summary
```

1. Collect the input files and group them into waves of up to five, purely to bound concurrency.
2. Locate (or plan) the target glossary path once, up front.
3. Extract: run every wave, each extractor writing its findings to a file and returning only a short confirmation.
4. Reduce: once, after all extraction is done, one subagent correlates and merges everything against the current glossary.
5. File: one `merge_jargon.py` call folds the reducer's output into the glossary.
6. Link: if `AGENTS.md` or `CLAUDE.md` exists, add a reference to the glossary if one isn't already there.
7. Report a summary to the user.

## Step 1: Collect input files

Take the file paths the user gave you. If they pointed at a directory instead of a list of files, expand it (respect their intent: a request like "extract jargon from the docs folder" means every readable text or markdown file under it, not the whole repo including `node_modules`, `dist`, `.git`, lockfiles, or binary assets).

**Auto-discover conventional locations.** Check for, and if
present, include:

- `docs/`, `documents/`, `doc/` (recursively — markdown and plain text)
- `README.md`, `CONTRIBUTING.md`, `SECURITY.md`, `COMPLIANCE.md`, `LICENSE*`
- `ARCHITECTURE.md`, `AGENTS.md` / `CLAUDE.md`, `CONSTRAINTS.md`
- Decision-record style folders, if present: `adr/`, `decisions/`, `rfd/`,
  `rfcs/`, `notes/`, `spikes/` — any folder holding NOTE/SPIKE/RFC-style
  documents is high-signal

Group the resulting file list into waves of up to five, for extraction concurrency only. Five is a starting point, not a hard ceiling: it keeps the one-subagent-per-file design intact (which is what keeps each extraction focused and its JSON output clean) while capping how many run at once. Adjust it down if a wave is clearly straining the environment, or up if the environment handles more concurrency comfortably and the files are small.

Also create a scratch directory for this run's intermediate files, and keep track of its path. Every extraction and reduce output in the steps below is written under it, never returned inline.

Pin this explicitly under `/tmp`, rather than a bare `mktemp -d` (whose default location varies by platform and, on macOS, resolves somewhere hard to find again later):

```bash
mktemp -d "/tmp/jargon-extractor.XXXXXX"
```

## Step 2: Locate the target glossary

Search the repository for an existing `JARGON.md` before doing anything else. Use a repo-wide search (`find`, `rg`, `grep`, or equivalent), not a narrow check of only the root or `docs/`.

1. If exactly one `JARGON.md` exists anywhere in the repo, that is the glossary path for the rest of this run.
2. If more than one `JARGON.md` exists, stop and show the matches. Ask the user which one is authoritative rather than guessing.
3. If none exists, default to a new `./JARGON.md` at the repo root.
4. Announce the chosen path before proceeding.

The file does not need to exist yet when you choose it; `merge_jargon.py` creates it on first write. Either way, you only need the path here, not the file's contents: the reduce subagent in Step 4 reads the current contents itself, directly from disk, in its own disposable context. The orchestrator never needs to hold the glossary's content in its own context.

## Step 3: Extract (subagent phase, one wave at a time)

For each wave, spawn one subagent per file in that wave, all in the same turn so they run in parallel, then wait for the wave to finish before starting the next one. If the current environment has no subagent or Task tool available, skip spawning entirely and instead process each file yourself, one at a time, applying the same extraction instructions below before moving to Step 4. Note that without subagents there is no way to keep this work off the main context; if that matters for a large file set in such an environment, consider processing a handful of files per turn across multiple turns instead of all at once.

**Extraction subagent task template:**

```
Read exactly one file: <path>

Flag every term in this file that a competent outside reader would not
already know: internal terminology, shorthand, abbreviations, acronyms,
and project- or domain-specific words. This includes terms that are
central to how the system works even if they are not abbreviations.

The test: would someone new to this specific project or domain need
this explained? That includes acronyms and initialisms (expanded and
defined, not just expanded), internal tool/system/process names,
shorthand the document uses without defining, and domain terms from a
specialized field the document assumes familiarity with. It excludes
plain vocabulary and terms already standard enough that defining them
would insult the reader (e.g. "function," "database," "HTTP" used in
their standard sense). When in doubt, flag it; over-flagging is cheap
to fix later, under-flagging loses information silently.

For each flagged term, give a plain English definition. Use the file's
own explanation if it states one; otherwise infer the meaning from
context. Flag any definition you are genuinely unsure about by noting
the uncertainty inline rather than presenting a guess as settled fact.
Keep each definition to one or two sentences; if a term needs more than
that to explain, give the short version anyway rather than writing an
exhaustive one.

Write your findings as strict JSON, nothing else, no markdown fences,
to this exact path: <output-path>
[
  {"term": "sidecar", "definition": "A helper process deployed
   alongside the main service to handle a supporting concern, such as
   logging or metrics, without living in the main service's codebase."},
  ...
]
If there is no jargon worth flagging, write an empty array: []

Then reply with ONLY a one-line confirmation, for example:
Wrote 6 terms to <output-path>
Do not repeat the extracted terms in your reply; they are already on
disk at <output-path>, and repeating them here only spends context
budget that the next step does not need.
```

Substitute a real path under the run's scratch directory for `<output-path>`, for example `<scratch-dir>/architecture.json`, and the real file path for `<path>`. Keep a running list of every extraction output path as waves complete; that list is all Step 4 needs, and it costs almost nothing to hold since it is just file paths.

## Step 4: Reduce (subagent phase, once for the whole run)

Once every wave has finished, spawn a single reduce subagent for the entire run. Give it every extraction output path collected in Step 3 and the glossary path from Step 2.

**Reduce subagent task template:**

```
You are the merge step for a jargon extraction run.

Read these extraction result files, each a JSON array of
{"term", "definition"}:
  <path-1>
  <path-2>
  ...

Also read the current glossary, if it exists, at:
  <glossary-path>
Treat every term already there as part of the same pool you are
correlating against, not just the newly extracted terms. If the file
does not exist yet, there is nothing existing to correlate against.

CORRELATE: group entries that refer to the same term, case-insensitively.
Two entries are the same term if they are the same word or phrase modulo
case (API / api) and trivial punctuation or spacing differences
(sub-agent / subagent) that clearly mean the same thing. Do not merge
two different concepts just because they share a substring. Do not
merge an acronym with its own expansion unless the source treats them
as one entry (CDC and "Change Data Capture" are the same entry only if
used interchangeably; keep them separate if the expansion is a
description rather than the term itself).

MERGE: for any term with more than one definition in the pool, write
one definition at least as informative as any single source, never one
that drops information, and still no more than a couple of sentences
unless a genuine multi-sense split requires it:
- If two definitions say the same thing differently, combine them into
  the clearer, more complete phrasing.
- If two definitions describe genuinely different senses of the same
  term, keep both, numbered inside one definition: "(1) ... (2) ...".
  Do not split into separate term (context) entries; the term must
  stay one stable lookup key so future runs can find and update it.
- If you are not confident two entries describe the same underlying
  concept, do not force a merge. Keep them separate and say so in your
  summary. A wrong merge is worse than a duplicate: a duplicate is easy
  to spot later, a wrong merge quietly loses information.

OUTPUT: write a JSON array containing ONLY the terms that are new, or
whose definition changed as a result of this run, to this exact path:
  <output-path>
[{"term": "...", "definition": "..."}, ...]
Leave out any term whose meaning is unchanged from what is already in
the glossary. Do not reproduce the untouched glossary into this file;
list only what is new or different.

Then reply with ONLY a short plain-text summary: how many terms you are
adding, how many you are updating (and one short clause why, per term),
how many you saw but left unchanged, and any cases where you
deliberately kept entries separate instead of merging them. Do not
include the full entries list in your reply; it is already written to
<output-path>.
```

Substitute the full list of extraction file paths, the real glossary path, and a real output path under the scratch directory, for example `<scratch-dir>/merged.json`.

## Step 5: File the results

Run the merge script against the reduce subagent's output. This is a plain bash call, not a subagent: the script reads and writes the files directly, so its content never has to pass through any model's context, only its small summary does.

`scripts/merge_jargon.py` is bundled with this skill, at a path relative to this SKILL.md file, not relative to the project you are working in. The bash tool runs from the project's working directory, so a bare `scripts/merge_jargon.py` will only resolve if that directory happens to be the skill's own folder, which it will not be in normal use. Resolve the absolute path to this skill's own directory first (the same directory this SKILL.md was loaded from), and invoke the script using that path:

```bash
python3 "$SKILL_DIR/scripts/merge_jargon.py" <glossary-path> <scratch-dir>/merged.json
```

`$SKILL_DIR` stands for this skill's own absolute directory; substitute the actual path. The glossary path argument is the one from Step 2, relative to (or an absolute path within) the project, not the skill directory.

The script reports counts of terms added, updated, and unchanged, and errors out (rather than guessing) if the entries file contains a duplicate term or if the existing glossary has a line in the entry region it cannot parse. Read `"$SKILL_DIR/scripts/merge_jargon.py" --help` if you need the exact flags; the script is intentionally strict, so treat its refusal to write as a signal to fix the input rather than working around it. Add `--dry-run` first if you want to preview the change before committing it.

## Step 6: Link the glossary from the agent behavior file

The glossary is only useful to future agent runs if something points them at it. `JARGON.md` itself should stay a pure term list, it should not reference agent behavior files, but the reverse should hold: `AGENTS.md` or `CLAUDE.md`, if either exists, should reference the glossary so a later agent working in this project picks it up as context.

Check, in order, whether `./AGENTS.md` or `./CLAUDE.md` exists at the project root. If `./CLAUDE.md` exists but its entire content is just an import pointer to `AGENTS.md` (for example, the file's content is essentially just `@AGENTS.md`), and `./AGENTS.md` exists too, treat `AGENTS.md` as the real target instead of editing the pointer file. If neither file exists, skip this step; do not create one from scratch, that is out of scope for this skill.

If a target file was found, read it fully first, then:

- If it already has a `## Related Documentation` section, check whether the glossary is already listed there (search for its path, or `JARGON.md`). If it is, leave the file alone. If not, add one entry to that section, preserving every existing entry exactly as it was.
- If no such section exists, add one at the end of the file.

Either way, the entry looks like this, with the glossary's actual path from Step 2 in place of `JARGON.md`:

```markdown
- **JARGON.md**: Internal terminology, acronyms, and shorthand used in this project, with plain English definitions
  _(Reference this when a term, acronym, or piece of shorthand in this project isn't self-explanatory)_
```

This is a small, one-entry, once-per-run edit, not the high-volume sorting and merging `merge_jargon.py` exists to protect, so doing it directly is fine here.

## Step 7: Report to the user

Summarize using the reduce subagent's short summary and `merge_jargon.py`'s small JSON output: total terms added, total updated, any ambiguous merges the reducer flagged instead of forcing, and whether `AGENTS.md` or `CLAUDE.md` was updated (or already referenced the glossary, or neither file was present). If the user wants to see the file itself, that is a normal file read at that point, not something that needs to happen mid-run.

## Entry format

`merge_jargon.py` owns the rendered shape (`- **Term**: Definition`, sorting, acronym casing). The one content rule that matters upstream, keeping numbered senses inside one entry rather than splitting into separate `term (context)` entries, is already stated in the reduce template above, since that is the only place it is actually applied.

## Edge cases

- **Binary or unreadable files**: skip and note which files were skipped and why, rather than failing the whole run.

## Example

Given `docs/architecture.md` and `docs/onboarding.md`, two extractors run in parallel in a single wave. Each writes its own file and returns only a confirmation to the orchestrator, for example `Wrote 1 term to <scratch-dir>/architecture.json`. The orchestrator never sees the definitions themselves at this point.

The reduce subagent then reads both files itself:

```json
// architecture.json
[{"term": "sidecar", "definition": "A helper process deployed alongside the main service to handle logging and metrics without living in the main service's codebase."}]
```

```json
// onboarding.json
[{"term": "sidecar", "definition": "Used loosely by the team for any auxiliary process that runs next to a primary one and shares its lifecycle, not just the logging/metrics helper."}]
```

Both describe the same term, but genuinely different senses, a specific technical meaning and a looser everyday one, not just different phrasings of the same idea. The reducer keeps both rather than picking one, writes the merged entry to `<scratch-dir>/merged.json`, and replies to the orchestrator with only a short summary such as "1 term added (sidecar, two senses merged)":

```json
[{"term": "sidecar", "definition": "(1) A helper process deployed alongside the main service to handle logging and metrics without living in the main service's codebase. (2) More loosely, any auxiliary process that runs next to a primary one and shares its lifecycle."}]
```

The orchestrator then runs `merge_jargon.py` against that file, which inserts the entry into the chosen `JARGON.md` path in alphabetical order. Across this whole example, the orchestrator's own context held two short confirmations, one short reduce summary, and one small script summary, never the definitions themselves.
