---
name: epistemic-mapper
description: "Build or update a canonical EPISTEMIC-MAP.md sorting a project's knowledge into four states: validated Facts, open Questions, undocumented Assumptions, and inferred Risks. Purpose-built for prototype-to-production handoff, where a signed contract means a new engineering team must take over before the original builder's tacit knowledge walks out the door. Spawns subagents across docs and the codebase to find what's proven, what's asked, what's silently assumed, and what nobody has noticed, then runs a dedicated synthesis pass for systemic risks no single source states. Use whenever a user mentions \"epistemic map\", \"knowledge map\", \"EPISTEMIC-MAP.md\", \"known unknowns\", \"unknown unknowns\", \"what do we actually know vs assume\", \"map our assumptions\", \"handoff risk map\", \"prototype handoff\", or \"onboarding a team onto a prototype\". Always prefer this skill over ad-hoc knowledge-gap documentation."
license: Apache-2.0
metadata:
  author: accelint
  version: "1.0.1"
---

# Epistemic Mapper

Extract a project's knowledge state from its documentation and its code, then
sort every observation into one of four quadrants and write the result into
a canonical `EPISTEMIC-MAP.md`. This is a handoff artifact: it exists because
a prototype builder holds a mass of tacit knowledge that never got written
down, and once a contract is signed and a team takes over, that knowledge
either gets captured now or gets rediscovered the hard way, in production.

```
                    HIGH CERTAINTY (validated)
                              |
          [ ASSUMPTIONS ]    |    [ FACTS ]
          Unknown Known      |    Known Known
          nobody wrote it    |    proven, cited
          down, but the      |    evidence
          code/docs rely     |
          on it              |
    ------------------------ + ------------------------
                              |
          [ RISKS ]           |    [ QUESTIONS ]
          Unknown Unknown     |    Known Unknown
          blind spots, found  |    explicit open
          only by looking     |    gaps, already
          across everything   |    flagged somewhere
                              |
                    LOW CERTAINTY (unvalidated)
```

## Relationship to Other Living Documents

`CONSTRAINTS.md` holds externally-imposed hard limits. `JARGON.md` holds term
definitions. `ARCHITECTURE.md` holds structural decisions. `AGENTS.md` holds
agent behavior and orchestration. `EPISTEMIC-MAP.md` is different in kind
from all four: it isn't a ledger of what's true, it's a map of *how sure we
are* about what's true. Read the other living docs (if present) before
extraction starts, for two reasons:

1. **Don't duplicate.** If a Known Known is already stated in `CONSTRAINTS.md`
   or defined in `JARGON.md`, reference it by file and section instead of
   restating it as a new Fact. `EPISTEMIC-MAP.md` should point at the other
   living docs, not compete with them.
2. **Seed confidence.** A claim backed by an entry in `CONSTRAINTS.md` is
   about as validated as a claim gets — treat it as a Known Known with
   `CONFIRMED` confidence by default, not something to re-litigate.

Unlike the other living documents, which accumulate, **this one is supposed
to shrink.** Every Assumption that gets validated becomes a Fact. Every
Question that gets answered gets marked resolved. Every Risk that gets
investigated either gets fixed (closes) or gets formally accepted (moves to
Known Unknown, now tracked instead of hidden). A re-run with a flat or
growing unresolved count is a signal that the handoff isn't actually
progressing — say so plainly in the executive summary rather than treating
a big file as a sign of thoroughness.

## NEVER Do When Building an Epistemic Map

- **NEVER invent a new category slug.** Pick the closest of the five
  canonical slugs by where the consequence lands, and put the specific
  pattern in the statement/reasoning text instead — `merge_epistemic_map.py`
  refuses anything else and explains the fallback rule in the error itself.
  Worked example: `references/schema.md`.
- **NEVER paraphrase or reconstruct the findings schema from memory when
  writing subagent prompts.** Quote `references/schema.md`'s field names
  and quadrant values verbatim. A renamed field (`observation` for
  `statement`) or a shortened quadrant (`fact` for `known-known`) causes
  every entry from that subagent to fail validation — or worse, be
  silently dropped if the mismatch is at the top-level key instead of a
  field inside it.
- **NEVER create a separate state or cache file** (`.epistemic-map-state.json`
  or similar). All state lives in `EPISTEMIC-MAP.md`'s own rendered text,
  parsed back in by `merge_epistemic_map.py` on every run — see
  `references/schema.md` if a run seems to need somewhere else to persist
  state.
- **NEVER truncate, summarize, or write a placeholder in
  `EPISTEMIC-MAP.md`** in place of full content — no "N total, see X for
  the complete list," no "showing top K of N," no pointer to a
  `consolidated.json`, a `backlog.md`, or any other file that isn't
  `EPISTEMIC-MAP.md` itself. The file is self-contained; every entry the
  merge script produced belongs in it, however long that makes the file. A
  large entry count is never a reason to summarize — see "Correlating and
  Deduplicating" above for why volume doesn't require the agent to hold or
  author entries by hand in the first place.
- **NEVER create an intermediate "consolidated" or "merged" findings
  file.** Pass every subagent's scratch file directly to a single
  `merge_epistemic_map.py` invocation via multiple `--findings` arguments.
  The script does the correlation; there is nothing to pre-merge.
- **NEVER hand-draft or restructure `EPISTEMIC-MAP.md`.** Every write goes
  through `merge_epistemic_map.py` — a hand-edit won't just look
  inconsistent, it will fail to parse on the next run.
- **NEVER add a "Related Documentation" section to `EPISTEMIC-MAP.md`
  itself.** Linking is one-directional: `AGENTS.md`/`CLAUDE.md` point to
  this file, not the reverse.
- **NEVER write scratch or findings JSON with a relative path, or inside
  the repository being scanned.** Absolute `/tmp/...` paths only —
  `merge_epistemic_map.py` refuses relative paths outright.
- **NEVER invent an entry not supported by evidence** (Facts, Questions,
  Assumptions) **or a reasoning trail** (Risks). Mark it `INFERRED` rather
  than asserting certainty, and never silently upgrade confidence to make a
  finding look more solid than it is.
- **NEVER crawl `openspec/changes/archive/` automatically** — only read
  specific archive files if the user names them explicitly.
- **NEVER run subagent extraction serially when subagents are available** —
  dispatch one per source simultaneously, capped at 5 per wave.

## The Quadrant Test

Every candidate observation goes through this triage, in order. Stop at the
first `YES`.

```
CANDIDATE OBSERVATION
        |
        v
Q1: Backed by evidence (data, contract, test result,
    executed code path, explicit recorded decision)?
        |
   YES -+----------------------------> KNOWN KNOWN (Fact)
        | NO
        v
Q2: Is the gap explicitly raised somewhere (a TODO,
    an open question in a doc, a ticket, an unresolved
    thread)?
        |
   YES -+----------------------------> KNOWN UNKNOWN (Question)
        | NO
        v
Q3: Does the code or docs silently rely on this without
    anyone stating it outright?
        |
   YES -+----------------------------> UNKNOWN KNOWN (Assumption)
        | NO
        v
             (handled separately, see Synthesizing Risks below)
                                    -> UNKNOWN UNKNOWN (Risk)
```

`references/quadrant-test.md` has the full version with worked examples per
quadrant and a redirect table for things that look epistemic but aren't
(team preferences, decided facts that already live in `CONSTRAINTS.md`,
glossary terms). Read it before the first extraction wave.

Note what this test structurally implies: Facts, Questions, and Assumptions
can all be found by a subagent reading one source closely. Risks cannot — if
a single source stated the risk, it would already be a Question or an
Assumption. Risks only emerge from looking at the whole picture at once,
which is why they get their own pass below instead of coming out of the
same extraction wave.

## Discovering Sources

Two source types, both in scope:

- **Documentation.** Auto-scan conventional folders — `docs/`, `documents/`,
  `README.md`, and similar — the same discovery behavior as
  `constraints-extractor`. Accept explicit paths the user adds. Exclude
  `openspec/changes/archive/` by default; it's historical record, not
  current knowledge. **Also exclude `CONSTRAINTS.md`, `JARGON.md`,
  `ARCHITECTURE.md`, `AGENTS.md`/`CLAUDE.md`, and `EPISTEMIC-MAP.md` itself
  from this scan** — they're read separately below for cross-referencing,
  not re-extracted as sources. A broad doc glob that sweeps these up too
  produces circular or duplicate entries (re-"discovering" a fact that's
  already a validated `CONSTRAINTS.md` entry) and wastes a subagent's pass
  on content that's already known.
- **The codebase.** Prototypes carry more tacit knowledge in code than in
  prose — a hardcoded region, a `// TODO: handle retries`, a try/catch that
  silently swallows an error, a config value nobody explains. Identify the
  main source directories (`src/`, `lib/`, `app/`, or whatever the repo
  actually uses) and treat each top-level module or package as its own
  source for extraction purposes.

Read any existing `CONSTRAINTS.md`, `JARGON.md`, `ARCHITECTURE.md`, and
`AGENTS.md` up front, per the section above — these seed Known Knowns and
tell you what not to restate. **This read and the source-discovery glob
above are independent of each other — issue them as parallel/batched tool
calls in the same turn, not one after another.** Neither depends on the
other's result, and serializing two cheap, independent operations only adds
latency for no benefit.

**Optional interview pass.** Pass `--interview` to enable a short, targeted
question phase after correlation (below), for when the original builder is
still reachable. Off by default — don't require an interview session to
produce a useful map, since the builder may already be gone by the time this
runs.

## Extracting Facts, Questions, and Assumptions

**Read `references/schema.md` in full before writing a single subagent
prompt.** Every subagent's task instructions must include the exact JSON
shape from that file, quoted directly — the `entries` top-level key, field
names (`statement`, `evidence`, `impact`, `confidence` — never `observation`
or another synonym), and quadrant values written exactly as the hyphenated
`known-known` / `known-unknown` / `unknown-known` strings, never a short
form like `fact` or `question`. Do not reconstruct the schema from memory or
from this file's summary of it — paraphrasing here is exactly how a field
gets renamed or a quadrant gets shortened in a subagent's output, and
`merge_epistemic_map.py` validates strictly against the schema as written,
not against a close approximation of it.

Spawn one subagent per source — one per doc, one per top-level code module —
capped at 5 concurrent per wave, matching the rest of this skill family.
Each subagent applies the Q1/Q2/Q3 test to everything in its source and
reports back a flat list of candidates in the Q1-through-Q3 quadrants only.
Risk is out of scope for this wave; a subagent looking at one file has no
way to tell a real systemic risk from an isolated oddity.

Every Fact, Question, and Assumption needs at least one evidence pointer —
a file (relative path from the project root, not an absolute path), a line
range or section, and a short quote or paraphrase of what's there. No
evidence, no entry. This mirrors `constraints-extractor`: ambiguity is fine,
an unsupported claim is not.

Subagents write scratch findings to **absolute paths only** (e.g.
`/tmp/epistemic-mapper/<source-id>.json`) — never a relative path, which
resolves against the repo's working directory and leaves stray JSON files
in the root. Refuse and re-request if a relative path is about to be used.

## Correlating and Deduplicating

Merge the wave's findings with `scripts/merge_epistemic_map.py`, which
handles the mechanical parts: ID assignment, category slug canonicalization
against the alias table in `references/schema.md`, duplicate collapsing
across sources, and ordering. This is not judgment work — don't hand-roll
it, and don't pre-merge it either.

**One invocation, every scratch file passed directly.** Every subagent's
scratch file (from every wave) plus the risk-synthesis file goes to a
*single* run of the script, as multiple `--findings` arguments:

```bash
python3 scripts/merge_epistemic_map.py \
  --findings /tmp/epistemic-mapper/doc-1.json /tmp/epistemic-mapper/doc-2.json ... /tmp/epistemic-mapper/risks.json \
  --output-dir /absolute/path/to/repo/root
```

There is no manual pre-merge step, no intermediate "consolidated" file, and
no reason for one — the script reads every findings file straight off disk
and does the dedup itself. This means entry volume is never something the
orchestrating agent needs to hold in its own context or author by hand: 13
source documents producing 106 total candidates is the script reading 14
small files and writing one output file, the same amount of orchestration
work as 2 sources producing 4 candidates. If a run feels like it's
generating "too much" to write out, that's a sign the script isn't being
invoked directly on the raw scratch files — stop and call it that way
instead of summarizing.

While merging, assign a confidence tier to each entry:

- **CONFIRMED** — two or more independent sources agree.
- **INFERRED** — a single source, reasonably read.
- **CONFLICTING** — sources disagree. Don't average them into a false
  middle; keep both readings visible and flag it. A CONFLICTING entry in
  the Facts quadrant is a contradiction worth escalating on its own — two
  docs stating different rate limits for the same API is itself a finding.

## Synthesizing Risks

After correlation, run one dedicated pass over the full merged picture —
not per-source, across everything at once. Look for the patterns that only
show up in aggregate:

- A dependency that three separate modules assume works a certain way, that
  nothing in the codebase or docs ever confirms.
- A single vendor, region, or credential with no fallback mentioned
  anywhere, especially where multiple Assumptions already cluster around it.
- A structural pattern common to failed handoffs — no error handling on an
  external call, no documented rollback path, a "temporary" decision with
  no owner or expiry — that this specific project also exhibits, whether or
  not anyone here has said so.

Because no source states a Risk outright, evidence citations don't apply.
Instead, write a **reasoning trail**: which observations, taken together,
point at the risk, and why the combination matters more than any one of
them alone. This is the one quadrant where the burden is on synthesis and
judgment rather than citation — say so plainly rather than manufacturing a
citation that doesn't exist.

**Risks still need one of the five canonical category slugs — never a new
one.** A synthesized risk is cross-cutting by nature (that's what makes it
a Risk rather than a Fact filed under one source), so it will often feel
like it deserves a more precise label than any of the five categories in
`references/schema.md` offers. Resist that. The category field answers
"where does the consequence land," not "what kind of risk pattern is
this" — a cascading schedule dependency across three deliverables isn't a
new `schedule-cascade-risk` category, it's `business-scope` if the missed
commitment is externally facing, or `team-process` if it's an internal
bottleneck. Pick the closest existing slug based on where the impact
actually lands, and put the specific mechanism in the `statement` and
`reasoning` text, where the precision belongs. `merge_epistemic_map.py`
will refuse to guess at an invented category — see the worked example in
`references/schema.md` for exactly this situation.

## Assembling the Backlog

`merge_epistemic_map.py` generates the Epistemic Backlog automatically —
3-5 action items, ranked by quadrant and severity (Risks and Assumptions
generally outrank Questions, since an unexamined blind spot is more
dangerous to a new team than a known open question). It always lands as
the `## Epistemic Backlog` section inside `EPISTEMIC-MAP.md` itself.

**There is no separate `backlog.md` file, and there never should be.** Do
not create one, do not reference one, do not write "see backlog.md" instead
of the actual checklist. If the backlog needs turning into real tickets
rather than a checklist, offer to hand the top items off to a ticket-creator
skill if one is available — but that produces tickets, not a markdown file,
and it's an offer, never automatic. The checklist inside `EPISTEMIC-MAP.md`
always stands on its own even if the offer is declined.

## Previewing and Writing EPISTEMIC-MAP.md

`EPISTEMIC-MAP.md` is one self-contained file, and it's plain markdown —
no frontmatter, no hidden block, no companion state file. Every field the
merge needs to round-trip (id, category, confidence, evidence, impact,
history, severity, first-seen date) is folded directly into each entry's
own rendered lines — see `references/schema.md` for the exact per-entry
format. `merge_epistemic_map.py` parses that same text back in as state on
the next run, the same approach `constraints-extractor` already uses. Two
files (or a visible block plus a hidden one) is how a handoff artifact
gets copied, moved, or reviewed with half of it left behind, or ends up
carrying the same content twice for no reason — earlier drafts of this
skill did exactly that with a YAML frontmatter block, and it roughly
doubled the file's size for zero added information. Don't reintroduce it.

**`merge_epistemic_map.py` is the only legitimate way this file gets
written or changed.** Never hand-draft or restructure `EPISTEMIC-MAP.md`
directly — not a heading, not a single line inside an entry. Write
findings to scratch JSON per `references/schema.md` and run the script.
The file is regenerated in full on every run from what the script parses
back in; a hand-edit doesn't just fail to survive a re-run, it will make
the next run fail to parse the file at all, on purpose — see "NEVER Do"
above. The file's structure is exactly what the script produces — Facts,
Questions, Assumptions, Risks, Epistemic Backlog, nothing else. If a task
seems to call for a different section (a cross-link note, a summary file,
anything not in that list), that's a signal to say so in the conversation
rather than add it to the file.

Always preview before writing, including small updates to an existing
file — same convention as the rest of this skill family. On a re-run, the
script reads prior state directly out of the existing file's own rendered
entries (there is nothing else to read it from) and marks:

- **Promotions** — an Assumption or Question that now has evidence moves
  quadrants, and the entry gains a `History (DATE): was -> became — reason`
  line. All of an entry's history lines are kept, not just the latest.
- **Resolutions** — a Question that's been answered or a Risk that's been
  fixed gets marked `resolved` with a short note, not silently deleted.
  Institutional memory of what used to be uncertain has value.
- **Dismissals** — a Risk investigated and found not to apply gets marked
  `dismissed` with the reasoning kept, for the same reason.

Never overwrite state silently. If a run finds zero new or changed entries,
say so plainly in the executive summary rather than padding the file to
look productive. If `EPISTEMIC-MAP.md` exists but doesn't match what
`merge_epistemic_map.py` itself would render — a hand-edit, a heading
missing a field, an old frontmatter-based file from a previous version of
this skill — the script refuses to run rather than guessing at prior state
and silently losing promotion history. Surface that error to the user
instead of working around it.

## Cross-Linking Into AGENTS.md / CLAUDE.md

This is the one exception to "the script owns the file" — a separate,
one-time prose edit to a *different* file, done after `EPISTEMIC-MAP.md`
has already been written and previewed. It never touches
`EPISTEMIC-MAP.md`'s own generation.

If `AGENTS.md` or `CLAUDE.md` exists at the target location, check whether
it already has a "Related Documentation" section (or equivalent)
referencing `EPISTEMIC-MAP.md`. If not, offer to append a one-line
reference in the same style the file already uses — matching how
`jargon-extractor` links `JARGON.md` and `constraints-extractor` links
`CONSTRAINTS.md`. This is a plain prose edit, not a companion script: a
single presence check, not high-volume sorting or dedup, so there's no
ongoing mechanical work here that would justify one.

`AGENTS.md`/`CLAUDE.md` is read on every agent interaction, so a pointer
placed there is not a passive footnote — it surfaces every time the file
loads, regardless of whether the agent goes on to open `EPISTEMIC-MAP.md`
itself. Word it to push toward "actually consulted," not just
discoverable:

```markdown
- **EPISTEMIC-MAP.md**: What's proven, what's assumed, and what's still unknown about this project; most relevant during handoff.
  _(Check this before making changes in an area flagged as an open Question or Assumption — treat an entry there as something to verify, not something to rely on)_
```

**The linking is one-directional** — see the NEVER-list rule above.
`AGENTS.md`/`CLAUDE.md` points to `EPISTEMIC-MAP.md` via this step, never
the reverse.

## Reference Files

- `references/quadrant-test.md` — worked examples per quadrant and a
  redirect table for near-misses (the triage test itself is the flowchart
  above). Read before extraction.
- `references/template.md` — the full `EPISTEMIC-MAP.md` skeleton used for
  new-file creation.
- `references/schema.md` — the JSON shape subagents write to scratch files,
  the category alias table, and the shape `merge_epistemic_map.py` expects.
  **Mandatory reading before dispatching subagents** — quote its exact
  field names and quadrant values into subagent prompts rather than
  paraphrasing; see "Extracting Facts, Questions, and Assumptions" above.
