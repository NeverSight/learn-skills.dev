---
name: constraints-extractor
description: "Extract explicit and implicit constraints (compliance, security, hosting, tooling, stakeholder, scope, and external-dependency boundaries) from a project's documentation, then build or update a canonical CONSTRAINTS.md. Spawns one subagent per source document to flag externally-imposed boundaries with evidence citations and confidence ratings, then correlates, deduplicates, and organizes the results by category before writing them into CONSTRAINTS.md. Use this skill whenever a user mentions \"CONSTRAINTS.md\", \"extract constraints\", \"find our constraints\", \"document constraints\", \"compliance constraints\", \"what limits this project\", \"synthesize constraints\", or wants to capture externally-imposed boundaries (legal, security, compliance, stakeholder, vendor) that shape what a project can build and how. Always prefer this skill over ad-hoc constraint documentation."
license: Apache-2.0
metadata:
  author: accelint
  version: "1.0.1"
---

# Constraints Extractor

Extract explicit and implicit constraints from project documentation and
synthesize them into a canonical `CONSTRAINTS.md` — a living record of the
externally-imposed boundaries (compliance, security, hosting, tooling,
stakeholder, scope, dependency) that shape what a project can build and how.

## Relationship to Other Living Documents

This skill is deliberately narrow. If a piece of content isn't clearly a
constraint, it stays out of this file. Apply the forcing-function test before
writing anything down:

```
Forcing-function test: if this were ignored, would something break OUTSIDE
the codebase — a contract, a law, a security posture, an executive decision,
a vendor relationship? If yes, it's a constraint.

If the honest answer is "the team would just be inconsistent" or "it would
look different," it's a pattern or a procedure, not a constraint — it
belongs in config.yaml or AGENTS.md instead.
```

| Document | Produced by | Captures |
| --- | --- | --- |
| `openspec/config.yaml` | `onboard-openspec` skill | WHAT the team chose (stack, patterns) |
| `AGENTS.md` / `CLAUDE.md` | `onboard-agent` skill | HOW the agent should behave |
| `ARCHITECTURE.md` | `architecture-doc` skill | HOW the system is structured today |
| `CONSTRAINTS.md` | **this skill** | WHY certain choices are non-negotiable |

Full category definitions, the forcing-function test worked through in
detail, and an in-scope/out-of-scope example table per category live in
`references/category-guide.md` — read it before running per-document extraction.

## Output Location

Determine where `CONSTRAINTS.md` belongs before scanning anything, so
Source Discovery knows to treat an existing file as authoritative rather
than as scan fodder.

1. Search the repository for an existing `CONSTRAINTS.md` file before doing
   anything else. Use a repo-wide search (`find`, `rg`, or equivalent), not a
   narrow check of only the root or `docs/`. If exactly one exists, that is the
   target — use it, don't ask.
2. If more than one `CONSTRAINTS.md` exists, stop and show the matches. Ask the
   user which one is authoritative rather than guessing.
3. If nothing exists, default to `CONSTRAINTS.md` at the repo root, alongside
   `ARCHITECTURE.md` and `AGENTS.md`.
4. Announce the chosen path before proceeding: *"No existing
   CONSTRAINTS.md found — I'll write to ./CONSTRAINTS.md."*

## NEVER Do When Extracting Constraints

- **NEVER invent a constraint not supported by evidence in a source
  document.** If a candidate statement doesn't have real evidence behind
  it, it doesn't qualify as `CONFIRMED` — treat it as a near-miss instead
  (see "Preview Before Writing" below), not a low-confidence entry. There
  is no third tier to fall back on for weak evidence.
- **NEVER silently drop a constraint because sources conflict.** Record both
  sides, mark the entry `CONFLICTING`, and cite each source.
- **NEVER write a constraint without at least one evidence citation** (file
  plus section or line reference). An unsourced constraint reads the same
  as a hallucinated one.
- **NEVER treat a confidently-worded team preference as a constraint.** Apply
  the forcing-function test. If no external force is evident, surface it in
  the pre-write preview as a near-miss and leave it out of the file — see
  "Preview Before Writing" below.
- **NEVER write a "Reviewed, Not Included" section, or any section like
  it, into `CONSTRAINTS.md`.** Near-misses are conversation output, not
  file content — see "Preview Before Writing."
- **NEVER add a "Related Documentation" section to `CONSTRAINTS.md`.** The
  linking is one-directional: `AGENTS.md` or `CLAUDE.md` point to this file via the cross-link step, not the other
  way around. A reverse pointer back to files that already reference this
  one is pure noise.
- **NEVER write a scratch or findings JSON file anywhere inside the
  repository being scanned, and never with a relative filename.** Every
  intermediate file — each subagent's scratch output and the single
  correlated findings file — lives under an absolute
  `/tmp/constraints-extractor.XXXXXX/` path. A relative filename resolves
  against the agent's working directory, which is the repo being scanned,
  not `/tmp`.
- **NEVER hand-write or hand-format an entry in `CONSTRAINTS.md`.** Every
  write — including a single new entry — goes through
  `scripts/merge_constraints.py`. Hand-formatting is how inconsistent
  structure (ad hoc symbols, extra fields, uneven spacing) ends up in the
  file, and it breaks the script's ability to parse the file back in on
  the next run.
- **NEVER crawl `openspec/changes/archive/` automatically** — it grows too
  large for a full-corpus scan and drowns real signal in resolved-change
  noise. Only read specific archive files if the user names them explicitly.
- **NEVER run subagent extraction serially when subagents are available** —
  dispatch in parallel, capped at 5 concurrent subagents. More than 5
  source documents means multiple waves, not unlimited concurrency.
- **NEVER overwrite an existing `CONSTRAINTS.md` without reading it first**
  — a human may have hand-corrected a confidence rating or resolved an
  ambiguity that a fresh scan can't recover.

---

## Source Discovery

Before spawning any subagents, assemble the set of source documents to scan.
Announce the final list to the user before dispatching subagents.

**Step 1 — Auto-discover conventional locations.** Check for, and if
present, include:

- `docs/`, `documents/`, `doc/` (recursively — markdown and plain text)
- `README.md`, `CONTRIBUTING.md`, `SECURITY.md`, `COMPLIANCE.md`, `LICENSE*`
- `ARCHITECTURE.md`, `AGENTS.md` / `CLAUDE.md`, `openspec/config.yaml` —
  these are decision *outputs*, but their prose sometimes carries buried
  rationale that never got promoted to a first-class constraint
- Decision-record style folders, if present: `adr/`, `decisions/`, `rfd/`,
  `rfcs/`, `notes/`, `spikes/` — any folder holding NOTE/SPIKE/RFC-style
  documents is high-signal, since rationale for a resolved decision is
  exactly where a forcing function tends to get written down explicitly
- An existing `CONSTRAINTS.md` at the location determined in "Output
  Location" above, if one exists (read it fully — see "Locate or Create
  CONSTRAINTS.md" below, do not treat it as just another scan target)

Run every check above as **one consolidated bash command**, not a
separate tool call per path — these are all fast existence checks with no
reasoning involved, so batching them costs one round trip instead of a
dozen:

```bash
for p in docs documents doc README.md CONTRIBUTING.md SECURITY.md \
         COMPLIANCE.md ARCHITECTURE.md AGENTS.md CLAUDE.md \
         openspec/config.yaml adr decisions rfd rfcs notes spikes; do
  [ -e "$p" ] && echo "FOUND: $p"
done
ls LICENSE* 2>/dev/null
```

**Step 2 — Accept an explicit user-provided list.** If the user names
specific files or paths — including files inside
`openspec/changes/archive/` — add them to the set. This is additive to
Step 1, never a replacement for it.

**Step 3 — Deduplicate and announce.**

```
Merge (Step 1 ∪ Step 2) by resolved path, then tell the user:

"Scanning N documents across ceil(N/5) waves of up to 5 subagents each:
[list]. This excludes openspec/changes/archive/ by default since it's
typically too large for a full pass — name specific files there if you
want them included."
```

If the merged set is empty, stop and ask the user where their documentation
lives rather than guessing at paths.

---

## Per-Document Extraction (parallel subagents)

Spawn one subagent per source document — parallel, never serial, capped at
**5 concurrent subagents**. With more than 5 documents in the discovered
set, dispatch in waves of up to 5: wait for a wave to finish before
starting the next.

Waves are a dispatch-batching concern only. They do **not** change the
Single Correlation Pass below — that still runs exactly once, after every
wave has finished, never once per wave.

Each subagent:

1. Reads its assigned file in full.
2. Applies the forcing-function test to every rule, limit, or boundary
   statement it finds.
3. For each candidate constraint, extracts:
   - `statement` — the constraint in plain English, self-contained (must
     read correctly without the source file open)
   - `impact` — one to three sentences on practical impact: what this
     constrains, what decisions it should shape, what breaks if ignored.
     Required whenever a constraint is included. If a subagent can't
     articulate this, that's usually a sign the candidate is a near-miss,
     not a real constraint.
   - `category` — the exact slug, verbatim: `compliance-governance`,
     `security-privacy-ip-cui`, `hosting-infrastructure`,
     `tooling-approved-path`, `workflow-sequencing`,
     `stakeholder-executive`, `scope-prioritization-delivery`, or
     `external-dependencies`. Full definitions in
     `references/category-guide.md`. Use the slug itself, not a
     shortened or display form of it — `merge_constraints.py` will
     auto-correct a few common variants but hard-fails on anything it
     can't confidently resolve, and a mismatch here is how a category's
     findings silently go missing.
   - `confidence` — always `CONFIRMED` at this stage. There is no
     "weak evidence" tier — if the statement isn't backed by a real
     citation, it's a near-miss, not a lower-confidence constraint.
     `CONFLICTING` only gets assigned during the Single Correlation Pass
     below, when two extracted findings disagree; a single-document
     subagent can't see that on its own.
   - `evidence` — a list of citations, each with `file` (relative path
     from the project root, not an absolute path), `location` (a line
     number or range where the source has real line numbers, a short
     section anchor otherwise), and `note` (one required sentence on
     what that specific citation shows — this becomes the entry's
     `Evidence notes` bullet for that citation, so it needs to earn its
     own line, not just restate the statement).
   - `affects` — optional list of bare tokens (rule IDs, other
     constraint IDs, system names) this constraint's enforcement touches.
     Omit or leave empty rather than guessing at a token that isn't
     actually named in the source.
   - `enforced_by` — optional list of bare tokens naming a specific
     downstream rule (in `AGENTS.md`, `ARCHITECTURE.md`, `config.yaml`,
     or elsewhere) that this constraint drives. Omit rather than
     guessing.
4. Also flags near-miss candidates — statements that read like constraints
   but fail the forcing-function test — with a one-line reason. These are
   surfaced only in the pre-write preview (see "Preview Before Writing")
   and are never written into `CONSTRAINTS.md` itself.
5. Writes full findings as JSON to a scratch file at an **absolute path**
   under `mktemp -d "/tmp/constraints-extractor.XXXXXX"` (one file per
   subagent — never a relative filename, never anywhere inside the
   repository being scanned) and returns only a one-line confirmation to
   the orchestrator, e.g. `Extracted 4 constraints, 2 near-misses from
   docs/SECURITY.md`. Keep bulk findings out of the orchestrator's context
   — the orchestrator reads scratch files directly during the single
   correlation pass; it does not receive findings inline.

Never assign an entry's `CONSTR-<CATEGORY>-<NNN>` ID at this stage, or at
correlation — ID assignment happens once, inside `merge_constraints.py`,
scoped per category. Extraction and correlation only ever produce
findings; the script is the sole owner of identity.

---

## Single Correlation Pass

After all subagents complete, run exactly **one** reduce pass — never one
per wave.

1. Read every scratch file in one call — `cat
   /tmp/constraints-extractor.XXXXXX/*.json` — rather than opening each
   one with a separate tool call.
2. Group candidates by category.
3. **Correlate duplicates.** If two or more sources support the same
   underlying constraint, merge into a single finding, combining their
   evidence citations (deduped by file+location, not summed) into one
   `evidence` list. Every citation keeps its own `note` — merging findings
   doesn't merge notes into one another.
4. **Surface conflicts.** If two sources make incompatible claims about the
   same boundary, do not pick a winner. Build a `claims` list — one entry
   per side, each with its own `statement`, `file`, and `location` — set
   `confidence` to `CONFLICTING`, and drop the `evidence`/`impact` fields
   for that finding entirely (a `CONFLICTING` finding carries `claims`
   instead, never both).
5. **Route near-misses.** Anything flagged as a near-miss during
   per-document extraction is carried into the correlated findings file
   for the preview step to display — it does not get a section in
   `CONSTRAINTS.md`.

Write the correlated result to `<scratch-dir>/correlated-findings.json` —
an absolute path in the same `/tmp` directory as the scratch files, never
a bare relative filename. The top-level shape is a flat list, not a
grouping by category:

```json
{"constraints": [ {"category": "workflow-sequencing", "title": "...", ...}, ... ], "near_misses": [...]}
```

Not `{"workflow-sequencing": [...], "compliance-governance": [...]}`. The
merge script reads the `constraints` array and reads each item's own
`category` field — it does not know how to interpret category names used
as top-level JSON keys. It checks for the `constraints` key explicitly
and refuses to run if it's missing, naming the keys it actually found, so
this shows up as a clear error rather than a silent zero-result write.
See `references/troubleshooting.md` for the full shape the merge script
expects (only needed if you're troubleshooting the merge step; day-to-day
use doesn't require reading it).

---

## Locate or Create CONSTRAINTS.md

Use the path determined in "Output Location" above.

- **If it exists:** read it fully first. Treat any hand-edited entry as
  authoritative over a fresh scan's version of the same constraint, unless
  new evidence directly contradicts it — in that case, flag the conflict
  in the preview step rather than overwriting silently. Merge new
  findings into the correct category sections in place.
- **If it doesn't exist:** create it fresh from `references/template.md`.

All mechanical file operations — ID assignment, category insertion,
dedup merge, ordering
— are handled by `scripts/merge_constraints.py`. Never hand-edit the file's
structure with ad hoc string appends; naive end-of-file appending
corrupts category grouping. The script is the single source of truth for
how entries get inserted:

```bash
python3 scripts/merge_constraints.py \
  --target <absolute path to CONSTRAINTS.md> \
  --findings <absolute path to correlated-findings.json under /tmp>
```

Both arguments must be absolute paths. The script refuses to run with a
relative `--findings` path, precisely because a relative path resolves
against the repo being scanned rather than `/tmp`.

The script is idempotent — re-running it with the same findings file
produces no diff.

A finding that fails validation (bad category, missing evidence, an
unrecognized shape it can't coerce) is skipped individually — it does not
block the rest of the batch from being written. Check the script's stdout
after every run: it reports both what was written and what was skipped,
with the specific reason for each skip. Relay skipped findings back to
the person rather than treating a successful exit as "everything from
this run made it in" — a partial write is still a successful run.

---

## Preview Before Writing

Show the user a summary before touching the filesystem:

- New constraints found, grouped by category
- Constraints whose evidence ref count grew via corroboration from
  multiple sources
- Any `CONFLICTING` entries, with every claim shown side by side
- Near-misses found, with their one-line reasons — shown here only; they
  are never written into `CONSTRAINTS.md`

Ask: *"Does this look right? Anything to reclassify, merge, or drop before
I write it?"*

A wrong compliance boundary is worse than a wrong reference doc entry
elsewhere — do not skip this step even for small diffs. If a run produces
zero new constraints, say so plainly rather than padding the file to look
productive.

---

## Cross-Link From the Agent Behavior File

If `AGENTS.md` or `CLAUDE.md` exist at the project root, check whether the
target already has a "Related Documentation" section referencing
`CONSTRAINTS.md`. If not, offer to append a reference.

The constraints are only useful to future agent runs if something points them at it. `CONSTRAINTS.md` itself should stay a pure list, it should not reference agent behavior files, but the reverse should hold: `AGENTS.md` or `CLAUDE.md`, if either exists, should reference the constraints file so a later agent working in this project picks it up as context.

Check, in order, whether `./AGENTS.md` or `./CLAUDE.md` exists at the project root. If `./CLAUDE.md` exists but its content is just an import pointer to `AGENTS.md` (for example, the file's content is essentially just `@AGENTS.md`), and `./AGENTS.md` exists too, treat `AGENTS.md` as the real target instead of editing the pointer file. If neither file exists, skip this step; do not create one from scratch, that is out of scope for this skill.

If a target file was found, read it fully first, then:

- If it already has a `## Related Documentation` section, check whether the constraints file is already listed there (search for its path, or `CONSTRAINTS.md`). If it is, leave the file alone. If not, add one entry to that section, preserving every existing entry exactly as it was.
- If no such section exists, add one at the end of the file.

Either way, the entry looks like this, with the constraints's actual path in place of `CONSTRAINTS.md`:

```markdown
- **CONSTRAINTS.md** — Externally-imposed boundaries (compliance,
  security, hosting, stakeholder) that shape what this project can build
  and how.
  _(Check this before scoping any change with compliance,
  security, hosting, or stakeholder-priority implications — it is not
  optional background reading)_
```

Do this with plain prose edits, not a companion script. This is a single
one-time presence check per file, not high-volume sorting or
deduplication — there's no ongoing mechanical work here that justifies a
script.

---

## Reference Files

- `references/category-guide.md` — the eight constraint categories, the
  forcing-function test worked through with examples, and an in-scope vs.
  out-of-scope table per category. Read before per-document extraction.
- `references/template.md` — the bare `CONSTRAINTS.md` skeleton used for
  new-file creation. Nothing but the eight category headings — no example
  content, so it can never be mistaken for real entries on first parse.
- `references/entry-format.md` — the `CONSTRAINTS.md` entry grammar that
  `merge_constraints.py` renders and parses. Read once per run.
- `references/troubleshooting.md` — the JSON shapes extraction and
  correlation produce, the shape-tolerance layer, and the merge script's
  exact behavior. Only needed if a run actually fails.
