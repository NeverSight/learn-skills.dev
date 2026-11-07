---
name: inbox-to-memory
description: Process raw inputs (transcripts, meeting notes, PDFs, slide decks, scratch braindumps) from a `_inbox/` queue into one groomed markdown note per input, and propose memory records across three scope tiers — project, client, and a cross-client journal. Use whenever the user wants to process the inbox, groom notes, drain the inbox, crystallize a memory candidate, promote something to memory or to a journal — even if they don't say "skill" or name a file type. Also use to set up the substrate for a new project, client, or the journal — scaffold a new project here, set up notes substrate, spin up a client, set up the journal, create a memory bank here. Client and project scaffolds default to a lightweight 3-type memory schema (Decision/Context/Rule) with a canonical 4-type opt; they also produce a README, `_personal.md`, `working-state.md` (project scope), and a `patterns-journal/`. Only operates on opted-in directories (holding `_memory/` or `entries/`, plus an `_inbox/` at that level or under `notes/`).
---

# inbox-to-memory

Three modes:

- **Process** (default): pulls raw inputs from a `_inbox/` queue, produces one groomed markdown note per input, and proposes memory records or journal entries for the user to approve.
- **Scaffold**: stands up the directory structure and CLAUDE.md for a new scope — a project, a client, or the cross-client journal.
- **Migrate**: rewrites an existing scope's v1 frontmatter onto the v2 contract, leaving every body untouched.

Decide the mode from the user's phrasing. When ambiguous, ask.

| Phrasing                                                                                                                             | Mode     |
| ------------------------------------------------------------------------------------------------------------------------------------ | -------- |
| "process the inbox", "groom these notes", "drain the inbox", "crystallize this candidate", "promote to memory", "promote to journal" | process  |
| "scaffold a new project here", "set up notes substrate", "spin up a client", "set up the journal", "create a memory bank here"       | scaffold |
| "migrate this scope", "bring these notes onto v2", "upgrade the frontmatter", "migrate to schema 2", "get this scope onto the contract" | migrate  |

---

## Process Mode

Six phases, plus a 2.5 that slots in ahead of grooming. The user reviews and approves between phase 4 and phase 5; never auto-promote. The one write into `_memory/` that skips that review lands in the same gap — a `last_confirmed` date stamped onto a record this run's inputs confirmed, under Stamp Confirmations below.

### Phase 1 — Detect Scope

Walk up from the user's cwd to find the nearest opted-in directory. A directory is opted in when it carries a queue and one of these markers:

- `_memory/` → project or client scope.
- `entries/` → journal scope.

The marker sits at the directory itself. The queue sits either there or one level down at `notes/_inbox/`, which is where the client and project scaffolds put it; only the journal scaffold puts it at the root. Look in exactly those two places. A queue found at any greater depth belongs to a scope nested below this one, and a client root that claimed it would start acting on its own projects' inputs.

Distinguish project from client scope by path: a project sits under `pursuits/<name>/` or `projects/<name>/`; a client root is the directory that _contains_ those (and is itself opted in). Journal scope is set by the `entries/` marker.

State the detected scope and root path back to the user before doing anything destructive. If nothing is opted in, stop and ask whether to scaffold — do not create directories silently.

### Phase 2 — Extract Content From Each Inbox File

For each file in `_inbox/`, dispatch by extension:

| Extension             | Tool                    |
| --------------------- | ----------------------- |
| `.md`, `.txt`, `.vtt` | Read directly           |
| `.pdf`                | invoke the `pdf` skill  |
| `.docx`               | invoke the `docx` skill |
| `.pptx`               | invoke the `pptx` skill |
| anything else         | ask the user            |

While reading, apply the extraction heuristics in [references/extraction-heuristics.md](references/extraction-heuristics.md). The short version: pull 6-12 surprising or contradictory quotes; flag tensions; split stated and unstated assumptions; capture action items with owner + priority; tag cross-note relationships as `confirms | contradicts | extends | introduces`.

### Phase 2.5 — Check Against Accepted Memory

Nothing else in the skill reads memory before writing to it, which is how a working session quietly contradicts an `accepted` record and the groomed note cheerfully writes down both. The conflict then surfaces months later, usually when someone acts on the stale half.

This phase carries a half number on purpose. Phases 3 through 6 keep the numbers they have had since v1, and every scaffold, note, and CLAUDE.md that refers to "phase 5 sign-off" keeps pointing at sign-off.

For each inbox file, in order:

1. **Extract the named entities.** People, systems, vendors, regions, anything a record might be about.
2. **Normalize them through the scope's alias table** before any lookup. Grep matching happens on canonical forms only. Skip this and "Shachi" and "Saatchi" search as two people, which produces a clean no-conflict report on a scope that has the conflict.
3. **Glob `_memory/`** and grep the entity list against frontmatter and titles.
4. **Read the headers of the hits.** Frontmatter, and no further. That's stage 3 of [references/retrieval-funnel.md](references/retrieval-funnel.md).
5. **Body-read only the records whose headers suggest overlap** with something this input actually claims.

That read answers two questions rather than one: does this input contradict what the record claims, or does it restate it? A restatement is a **confirmation** — the claim is still true, and somebody said so on the date this input carries, which is the whole of what `last_confirmed` is for. Deciding an input doesn't contradict a record means you have already read everything the second question needs, so the confirmation costs nothing past the read that was happening anyway. Keep the pairing of note to records; the stamping call below takes one group per note.

**Five body reads per input, and the budget binds.** It is not a suggestion to stay near. When detection would need a sixth read to be useful, say so in the phase 6 report and leave the read undone. A budget quietly exceeded on every input is one nobody notices has stopped bounding anything. A scope where five is routinely too few is telling you its records are too granular, which is a finding worth having. Confirmations come out of that same budget rather than drawing one of their own. There is no second pass over the records, and no sixth read on the grounds that an input might also be confirming something.

Only `status: accepted` records produce flags, and only they can be confirmed. A `proposed` record hasn't been agreed to yet, so disagreeing with it is just discussion and agreeing with it asserts nothing; a `superseded` one is already known to be wrong.

Flag a conflict inline, where the triggering passage lives:

```
[contradicts accepted: [[<record-filename>|<short-label>]]] <what this input says> | claims: <what the record says>
```

Both halves are required. The record's own claim written down beside the new statement is what lets a reader settle the disagreement without opening the record, and what makes it obvious when the two never actually disagreed.

A contradiction is a first-class candidate, resolved at phase 5 sign-off like any other. Its three outcomes are in that phase.

A confirmation is not a candidate and gets no flag. The record already exists and already makes the claim; the only thing that changes is the date saying when it was last seen to be true, so there is nothing for the user to sign off on and the stamp never passes through phase 5. Its trace is the date on the record itself and the phase 6 report, which names every record the run stamped and every one the stamper declined to write.

### Phase 3 — Groom Into a Single Note

Emit one note per input at `<scope-root>/notes/YYYY-MM-DD-<slug>-<nanoid>.md`. The template is at [assets/note.template.md](assets/note.template.md).

Three zones, always in this order:

1. **Frontmatter** — `id`, `date`, `type`, `attendees`, `tags`, `topics`, optional `source_file` (binary sources only), `raw_file: raw/<id>.md` (whenever the note has raw text, which then lives in the sidecar), optional `related`.
2. **Extracted sections** — `## Notable Quotes`, `## Tensions`, `## Stated Assumptions`, `## Unstated Assumptions`, `## Open Questions`, `## Action Items / Memory Candidates`.
3. **Raw Content** — `## Raw Content`, a blank line, and the pointer line `In [raw/<id>.md](raw/<id>.md). Open it only to verify a quote.` Always last.

The raw text itself, the verbatim original (text sources) or extracted text (binary sources), goes in the sidecar `<scope-root>/notes/raw/<id>.md`, where `<id>` is the note's `id`. The sidecar has no frontmatter and holds every line that would otherwise follow the `## Raw Content` heading, so note and sidecar together reproduce the raw text byte for byte. Keeping it out of the note lets an embedding index exclude `notes/raw/`, so a transcript's chunks never outnumber the reviewed sections above it. `L<n>` in a quote anchor counts lines in the sidecar. The full rule is in [references/machine-contracts.md](references/machine-contracts.md), under "The Raw Sidecar".

Write the sidecar first, creating `notes/raw/` if it is missing, then the note with `raw_file` set. A run that stops between the two leaves an orphan sidecar, which nothing reads. The other order leaves a note pointing at nothing, which the lint fails as `raw-file`. A note with no raw text at all, such as a directly authored one, keeps an empty `## Raw Content` section and no `raw_file`.

Inside the extracted sections, flag candidates **inline** using the taxonomy below. Don't hide candidates in a separate file or section — keep them where the triggering passage lives, so the user can read both together.

### Candidate Flag Taxonomy

```
[memory candidate: project] <claim>
[memory candidate: client] <claim>
[memory candidate: update existing [[<filename>|<short-name>]]] <amended claim>
[journal candidate: <generalized pattern>]
[contradicts accepted: [[<filename>|<short-name>]]] <statement> | claims: <what the record says>
```

- The scope token (`project` or `client`) is the skill's _proposal_, not a decision. The user confirms or overrides at phase 5.
- The contradiction flag comes out of phase 2.5 rather than out of reading the input alone. It's the one candidate type that needs memory read first.
- The "update existing" variant signals an amendment to an already-crystallized record. Its scope is inherited from the target.
- Journal candidates take no scope token — their destination is always the cross-client journal.

Every token the skill emits is registered in the grammar table in [references/machine-contracts.md](references/machine-contracts.md) with the grep that finds it. Register a new shape there before using it; a token invented at the point of use is one nothing can retrieve later.

#### Open Question Slugs

Before writing the Open Questions section, grep the scope's prior notes for slugs already in play:

```bash
grep -rhoE '\[open question( resolved)?: [^]]*\]' <scope-root>/notes/ | sort | uniq -c | sort -rn
```

Reuse an existing slug for the same question rather than minting a new one. Then, in the note you're writing:

- Report each recurring open question with the number of notes it has stayed open across. That count is what you bring to the person who can close it.
- Rewrite this note's own entries to the resolved form for anything this session answered.
- Flag a slug open across three or more notes as `[tension: unacknowledged]`, unless the transcript shows someone naming it out loud. Chronic non-answers should be escalated by arithmetic rather than by whoever happens to notice.

**Process mode never edits a prior note.** Each note is a faithful record of what was known that day, and rewriting an old one to reflect a later answer destroys the only thing it was good for. A question resolved today gets its resolution in today's note.

Use the heuristics in [references/scope-decisions.md](references/scope-decisions.md) to pick a scope. The short version: project is the floor (cheapest to be wrong); client requires recurrence across projects or stakeholder-level facts; journal requires generalization beyond this client.

### Phase 4 — Dispose Source

Text sources (`.md`, `.txt`, `.vtt`) get deleted from `_inbox/`. Their words survive in the note's raw sidecar, so confirm `notes/raw/<id>.md` exists and is non-empty before deleting.

Binary sources (`.pdf`, `.docx`, `.pptx`) move to `<scope-root>/notes/attachments/<original-filename>`. Set `source_file: attachments/<filename>` in the note's frontmatter so the original is referenceable. Their extracted text goes to the sidecar like any other raw text.

Never leave a file in `_inbox/` after grooming. The inbox is a queue, not a library.

### Stamp Confirmations

Phase 2.5 worked out which records this run's inputs confirm. Writing the dates is mechanical, so a script does it:

```bash
bash <skill-path>/scripts/stamp-confirmed.sh <scope-root> \
  --note <note-path> <record-path>... \
  [--note <note-path> <record-path>...]...
```

Each `--note` group is one groomed note and the records that note confirms. The script reads the note's own `date:` and stamps it onto them. It refuses to move a date backwards, to touch a v1 file, to stamp anything that isn't `accepted`, and to insert the key where doing so would push the frontmatter past its 20-line budget; each refusal comes back as a `skipped:` line naming the reason. Paths are absolute or relative to the scope root.

**One call for the whole queue, never one per input.** Hand it every group at once. Two inputs in one run can confirm the same record, and the script only gets to write that record once — taking the later of the two dates — if it sees both groups in the same invocation. A loop calling it per input has already written the first date before it hears about the second, so the same inbox writes that record once or twice and reports it differently depending on which file got read first.

**A run that found no confirmations makes no call at all**, and most runs are that run. An invocation with no `--note` group is a usage error rather than a quiet no-op, so there is nothing to hand it and nothing to run.

Putting the call here, after phase 4 and before phase 5, is a convention rather than something the script forces. The close of phase 3 would serve as well, since phase 4 only disposes sources and opens no gate. Fixing it in one spot is what makes two agents draining the same inbox produce the same trace, and it keeps the phase 6 report reading in phase order; the batch rule above is the part that carries real weight. It gets no phase number of its own because it is a call, not a phase of work.

The script writes without stopping to ask, which is the exception spelled out in Operating Rules. Keep its output: phase 6 reports both the stamps and the skips off those lines. `--dry-run` prints the same lines and writes nothing, if you want to look first.

### Phase 5 — Propose and Crystallize (gated)

Stop here. Show the user every groomed note and every flagged candidate, organized by candidate type and proposed scope. Wait for explicit per-candidate sign-off.

For each candidate the user approves:

1. **Generate a nanoid**: `nanoid -s 10` (globally-installed CLI). Never random-generate or use Python's random module.
2. **Create the record file** using the matching template in [assets/records/](assets/records/):
   - Memory record (project or client scope): `<scope-root>/_memory/<type-folder>/<slug>-<nanoid>.md`. The folder set depends on the scope's memory mode (declared at the top of its `CLAUDE.md`):
     - Lightweight: `decisions/`, `context/`, `rules/`.
     - Canonical: `decisions/`, `context/`, `policy-rules/`, `exceptions/`.
     The folder must match `memory_type` in the frontmatter (`Rule` in lightweight = `PolicyRule` in canonical; see [references/memory-bank-schema.md](references/memory-bank-schema.md)).
   - Journal entry: `11 Clients/11.99 Journal/entries/YYYY-MM-DD-<slug>-<nanoid>.md`.
3. **Rewrite the candidate line** in the source note to a wiki link:
   - `[memory candidate: <scope>] <claim>` → `[[<record-filename-without-ext>|memory]] <claim>`
   - `[memory candidate: update existing [[<target>|<name>]]] <claim>` → `[[<target>|memory — updated]] <claim>`
   - `[journal candidate: <pattern>]` → `[[<relative-path-to-journal-entry>|journal]] <pattern>`
4. **For "update existing" promotions** (this is how a record grows over time rather than spawning duplicates):
   - Append the source note's `id` to the target record's `source_refs`.
   - Amend the target record's body. Mark new content inline with `(added YYYY-MM-DD, <note-id>)` so the next reader can trace which source contributed which passage.
   - Keep the original `date` field. Only bump it if the core claim has materially changed — at which point consider whether the old record should be `status: superseded` and a new record created instead.

#### Resolving a Contradiction

A `[contradicts accepted: ...]` flag has three outcomes, and the user picks one per flag:

- **Amend.** The record was right but incomplete. Take the update-existing path above against the flagged record, and rewrite the line to `[[<target>|memory — updated]]`.
- **Supersede.** The record is now wrong. Create the replacement, set the old record's `status: superseded` and its `superseded_by`, set the new record's `supersedes`, and rewrite the line to `[[<new-record>|memory — supersedes <old-label>]]`.
- **Dismiss.** They don't actually conflict, or the new statement is the mistaken one. Append `| dismissed: <reason, and who decided>` and leave everything else where it is.

**A dismissed flag stays in the note permanently.** It is the record that someone looked at this and decided it was nothing, which is what stops the next four notes from re-flagging the same non-conflict. Deleting it throws away the only evidence the question was ever asked.

Never auto-promote. Every record creation requires explicit user approval per candidate. Unpromoted candidates keep their `[memory candidate: ...]` or `[journal candidate: ...]` prefix — the prefix signals "considered, not crystallized," which is itself useful provenance.

### Phase 6 — Verify

Run the lint over the scope first:

```bash
bash <skill-path>/scripts/lint-scope.sh <scope-root>
```

It reports how many files in the scope are v1 and how many are v2, and exits nonzero if any check fails.

Then check by hand what the lint can't:

- Every candidate flag in every groomed note has either been resolved to a wiki link OR retains its original prefix. No half-rewrites, no orphans.
- Every record file has a valid `id`, a `memory_type` matching its folder, and at least one entry in `source_refs`.
- Every wiki-link path resolves (the target file exists at the expected location).
- The `_inbox/` is empty.
- Any input where the phase 2.5 read budget bound is named, along with what went unread. A budget that silently truncates detection reports the same "no conflicts" as a scope that genuinely has none.
- Every record whose `last_confirmed` the run stamped is named, with the date it now carries. Read them off the stamper's `stamped:` lines. This report is the only durable trace of a write the user was never asked to approve.
- Every record the stamper declined to write is named, with its reason: a v1 file, a `status` other than `accepted`, a date already at or past the note's, or an insertion that would overrun the 20-line frontmatter budget. Read them off its `skipped:` lines, which is also the scope of this list: what the stamper turned down, not everything phase 2.5 opened. The skipped v1 records are the ones nobody would otherwise learn were left behind, and a silent skip reads exactly like a record nobody confirmed.

Report failures. Don't silently retry or auto-fix — those bugs hide.

---

## Scaffold Mode

Stand up the directory structure and CLAUDE.md set for a new scope. Ask at most four questions:

1. **Scope** — project, client, or journal. (Suggest a default based on cwd: inside a client root, suggest client; inside `pursuits/` or `projects/`, suggest project; matches `*/11.99 Journal*`, suggest journal.)
2. **Target path** — where to scaffold. Default: cwd. Exception: journal scope defaults to `11 Clients/11.99 Journal/` relative to the nearest vault root.
3. **For project scope only** — pursuit (pre-sale, RFP work) or delivery (post-sale, working sessions)? This drives the `type:` enum baked into the generated CLAUDE.md.
4. **For client and project scope** — memory mode: **lightweight** (default, 3 types: Decision/Context/Rule) or **canonical** (4 types: Decision/PolicyRule/Exception/Context). The user can answer simply "lightweight" / "canonical" or "use the full schema". See [references/memory-bank-schema.md](references/memory-bank-schema.md) for the trade-off. Default is lightweight — Exception folds into Decision.

The chosen memory mode gets recorded in the scope's `CLAUDE.md` (top frontmatter blockquote) so later `process inbox` runs flag candidates against the right type set.

### Outputs per Scope

**Client scope (lightweight default):**

```
<target>/
├── CLAUDE.md                       # from assets/claude-md/client.template.md
├── README.md                       # from assets/readme/client.template.md
├── _personal.md                    # from assets/personal.template.md
├── notes/
│   ├── CLAUDE.md                   # from assets/claude-md/notes.template.md
│   ├── README.md                   # from assets/readme/notes.template.md
│   ├── _inbox/.gitkeep
│   └── attachments/.gitkeep
├── _memory/
│   ├── CLAUDE.md                   # from assets/claude-md/_memory.template.md
│   ├── README.md                   # from assets/readme/_memory.template.md
│   ├── decisions/.gitkeep
│   ├── context/.gitkeep
│   └── rules/.gitkeep              # canonical mode: policy-rules/ + exceptions/ instead
└── patterns-journal/
    ├── CLAUDE.md                   # from assets/claude-md/patterns-journal.template.md
    └── journal.md                  # from assets/patterns-journal/journal.template.md
```

`projects/` and `pursuits/` subdirectories are not pre-created — they're added by hand or via subsequent scaffold-mode runs when projects/pursuits open.

**Project scope (lightweight default):**

```
<target>/
├── CLAUDE.md                       # from assets/claude-md/project.template.md
├── README.md                       # from assets/readme/project.template.md
├── working-state.md                # from assets/working-state.template.md
├── _personal.md                    # from assets/personal.template.md
├── notes/
│   ├── CLAUDE.md
│   ├── README.md
│   ├── _inbox/.gitkeep
│   └── attachments/.gitkeep
├── _memory/
│   ├── CLAUDE.md
│   ├── README.md
│   ├── decisions/.gitkeep
│   ├── context/.gitkeep
│   └── rules/.gitkeep              # canonical mode: policy-rules/ + exceptions/ instead
└── patterns-journal/
    ├── CLAUDE.md
    └── journal.md
```

The differences from client scope: project scope gains `working-state.md` (the narrative decisions layer) and does not create `projects/` or `pursuits/` subdirectories.

**Canonical mode replaces** the `_memory/rules/` folder with `_memory/policy-rules/` and `_memory/exceptions/`, and the generated CLAUDE.md templates substitute `Decision/PolicyRule/Exception/Context` for `Decision/Context/Rule` throughout.

**Journal scope:**

```
<target>/
├── CLAUDE.md                       # from assets/claude-md/journal.template.md
├── _inbox/.gitkeep
├── entries/.gitkeep
└── attachments/.gitkeep
```

Journal scope stays lightweight by design — single-tier substrate, no working-state, no patterns-journal (that's what the journal itself is), no `_personal.md`.

### Template Substitution

The CLAUDE.md and README templates use double-curly placeholders. Substitute these at scaffold time:

| Placeholder | Replacement |
| ----------- | ----------- |
| `{{ClientName}}` / `{{ProjectName}}` / `{{ScopeName}}` | Human-readable name supplied by the user. |
| `{{pursuit\|delivery project}}` / `{{pursuit\|project}}` / `{{pursuits\|projects}}` / `{{Pursuit\|Project}}` | Pick one side of the pipe based on question 3. Use the title-cased `{{Pursuit\|Project}}` form when the substitution lands inside a heading. |
| `{{MEMORY_MODE}}` | `lightweight` or `canonical`. |
| `{{MEMORY_TYPES}}` | `Decision, Context, Rule` (lightweight) or `Decision, PolicyRule, Exception, Context` (canonical). |
| `{{MEMORY_TYPE_ENUM}}` | `Decision \| Context \| Rule` or `Decision \| PolicyRule \| Exception \| Context`. |
| `{{MEMORY_TYPE_FOLDERS}}` | `decisions/, context/, rules/` or `decisions/, policy-rules/, exceptions/, context/`. |
| `{{MEMORY_TYPE_LIST}}` | Markdown bullet list of types with one-line descriptions (pull from `references/memory-bank-schema.md`). |
| `{{MEMORY_TYPE_SUMMARY}}` | Short table or bullet list summarizing types for the human-facing `_memory/README.md`. |
| `{{RULES_FOLDER}}` | `rules` (lightweight) or `policy-rules` (canonical). |
| `{{NOTE_TYPE_ENUM}}` | Pipe-separated baseline note types: `scoping-call \| working-session \| stakeholder-call \| internal \| reading \| braindump \| transcript \| status`. The generated project CLAUDE.md will override this in its Deltas section if the user provides project-specific values. |
| `{{date}}` | Today's date in ISO format. |
| `{{engagement-list}}`, `{{stakeholder-list}}`, `{{tag-list}}`, `{{type-enum-values}}`, `{{one-sentence-project-description}}` | User-supplied during scaffold; left as HTML-commented placeholders if the user defers. |

Leave placeholders that the user defers as `<!-- Fill in: ... -->` comments rather than blanks — that way they're easy to grep for later.

### Stamping the Scaffold

Every markdown file this mode generates carries a `scaffold_digest` in its frontmatter: a hash of the body it was written with. Stamp them by running the script, rather than computing the hash inline:

```bash
python3 <skill-path>/scripts/scaffold_digest.py --stamp <every generated .md>
```

`jd-file` stamps the Overviews it mints and `jd-audit` re-hashes every scaffolded file to decide what counts as furniture. All three skills carry byte-identical copies of that script, because a boundary drawn one byte differently in any copy marks every stamped file as edited. Frontmatter stays out of the hash because Obsidian rewrites it unprompted—adding tags, touching timestamps—and none of that is a person writing content.

`README.md` and `CLAUDE.md` are furniture in a scaffold and real content everywhere else, so their names can never answer whether anyone has written here. A file whose digest still matches is one nobody has touched, and an ID holding only such files is empty no matter how many files it holds.

Stamp last, once every body is final—substitutions resolved and the Deltas section filled or left as `<!-- Fill in -->` comments. Stamp before that and the next check reads this skill's own writing as a human edit. Skip files that carry no frontmatter. They need no digest: `.gitkeep` is furniture by its name alone, which is how `jd-audit` already reads it.

### The Deltas Convention

Each generated CLAUDE.md (client and project) carries a `## Deltas` section with a fixed structural shape, not free-form. The shape:

**Client-level Deltas:**
- `### Active engagements` — short list of in-flight projects and pursuits.
- `### Cross-engagement stakeholders` — roster of people who appear across multiple projects at this client. Format: `Name — Role/Title. Additional facts.`
- `### Alias table` — every name that arrives under more than one spelling, canonical form first.
- `### Client-wide tag namespace` — controlled vocabulary for memory record `tags:`.

**Project-level Deltas:**
- `### Note type: values` — controlled vocabulary for note frontmatter `type:`.
- `### Active stakeholders` — project-specific roster.
- `### Alias table` — project-specific aliases, optionally pointing to client-level Context records.
- `### Tag namespace (suggested)` — project-specific tags.
- `### applies_to facets` — optional per-scope dimension prefixes for memory-record `applies_to` values.
- `### Pre-existing content` — optional, only when a project subdirectory predates the substrate.

The alias table is load-bearing for grooming accuracy. It covers everything that reaches a note under more than one spelling: transcript mishears, nicknames, abbreviations, and OCR variants off slides and PDFs. The form is `canonical <- [variant, variant]`.

During process mode, read it and normalize while grooming, then record what was applied in the groomed note's frontmatter as `transcript_corrections: [Saatchi→Shachi, Lince→Lancey]`. The key keeps its old name so greps written against v1 notes keep working.

Two rules govern how far normalization reaches:

- **Extracted sections only.** Never rewrite raw content. It is the source of truth, and a normalized transcript stops being a record of what was actually said.
- **Read either heading.** Scopes scaffolded before the rename say `### Transcription-error mapping`. Both resolve to the same table, so an existing setup keeps working without being touched.

The `entities` frontmatter key holds canonical forms only, never the variants they came from. The point of the key is that one grep finds every note touching a person or system, and that fails the moment the same person appears under three spellings.

During scaffold mode, prompt the user for known stakeholders and tag namespace seeds. Offer to populate the roster inline. If the user defers, leave the structure with `<!-- Fill in -->` comments.

### What Never Lands in `_memory/`

No `MEMORY.md` or `INDEX.md` summary file in any `_memory/` directory. Filenames already carry slug + id; subfolders carry type. An index would duplicate information that globbing already surfaces, drift the moment a record is renamed or superseded, and teach a retrieval path that doesn't exist in Copilot Spaces or MCP queries. If you need "what's currently in memory," generate it on demand: `Grep "^title:" _memory/`.

### Idempotency

If the target directory already contains an opted-in structure (matching markers), do **not** clobber. Report "already scaffolded at <path>" and offer to regenerate just the CLAUDE.md set. If the user agrees, write regenerated content to `CLAUDE.md.new` (and `README.md.new`, etc.) rather than overwriting — they may have customizations to merge by hand. Stamp the `.new` files the same way and leave the originals untouched. If the user has written into one, its digest stops matching, and that mismatch is the signal `jd-audit` reads.

### Existing-directory Regeneration

When invoked at a pre-existing project (e.g., `pursuits/atlas/`) that already has notes and `_memory/`:

1. Detect existing structure; do not overwrite content.
2. Add any missing subdirectories per the chosen memory mode (e.g., `_memory/rules/` for lightweight, `_memory/policy-rules/` and `_memory/exceptions/` for canonical) with `.gitkeep`.
3. Add any missing top-level files (`README.md`, `_personal.md`, `working-state.md` for projects, `patterns-journal/{CLAUDE.md,journal.md}`) without clobbering existing content.
4. Regenerate `CLAUDE.md` from the project template (write to `CLAUDE.md.new` if the existing file has been edited beyond template substitution).
5. Ask the user for **deltas** — active stakeholders, custom tag namespace, custom `type:` enum values, transcription-error mappings. Append them under the regenerated `## Deltas` section.
6. Stamp every file this run wrote—the regenerated `CLAUDE.md` or `CLAUDE.md.new`, plus anything added in step 3. The Deltas append in step 5 changes the body, so stamping before that records a digest the file already no longer matches.
7. If the pre-existing `_memory/` uses a different mode than the user requests (e.g., existing canonical 4-type vs. requested lightweight), report the mismatch and ask before changing anything. Do not auto-migrate.

---

## Migrate Mode

Bring one opted-in scope's v1 files onto the v2 frontmatter contract. Full spec in [references/migration.md](references/migration.md).

```bash
bash <skill-path>/scripts/migrate-scope.sh <scope-root>            # dry run, writes nothing
bash <skill-path>/scripts/migrate-scope.sh <scope-root> --apply    # writes
```

One scope per run. Files already carrying `schema: 2` are skipped, so a second run over the same scope reports everything as already migrated and changes nothing.

**Show the user the dry run and get approval before `--apply`.** Tier 1 is mechanical, so it's approvable as one batch rather than per file. Every transformation in it has a single correct answer; nothing in Tier 1 is the skill's opinion.

What it changes, all above the fence:

- Adds `schema: 2` and `body_schema: 1`.
- Converts block-style lists to inline arrays and reorders keys to the contract.
- Flattens `related` mappings to `<relation>::<id>` and journal `source_refs` to `<scope-path>::<note-id>`.
- Computes the four derived counts from body tokens. A v1 note with no tokens gets zeros, because they were counted and not assumed.
- Sets `last_confirmed` on a record to the record's own date.

**The body is copied byte for byte**, which is why a migrated file carries `body_schema: 1`. Its frontmatter is v2 and its body is still v1, that combination is legal indefinitely, and the lint's body-grammar checks skip it. Old anchors, old phrasing, and old section names all stay exactly as written.

The migrator refuses to guess. A `related` entry with an id but no relation keeps its bare id and gets reported; so does any frontmatter it can't parse, any rewrite that would overrun the 20-line budget, and any sub-field the compound form has no room for. Read the "needs a human" list at the end of the run.

**Requires a clean working tree** unless run with `--allow-dirty`. Every safety claim here rests on `git diff` being readable afterward, and starting dirty makes a mistake indistinguishable from whatever was already uncommitted.

### Tier 2: Summary and Entities

Most v1 notes carry neither key, and filling them in is the skill's reading of a note rather than a fact about it. So Tier 2 runs through a sidecar the migrator writes and then holds you to: it emits the text you're allowed to read, you fill in a proposals file, and the apply writes back only what it can source.

```bash
# 1. write the sidecar: one extract per v1 note, plus a proposals skeleton
bash <skill-path>/scripts/migrate-scope.sh <scope-root> --tier2-extract <dir>

# 2. fill in summary and entities for each note id in <dir>/proposals.yaml

# 3. dry run the merge, show it to the user, then write
bash <skill-path>/scripts/migrate-scope.sh <scope-root> --tier2 <dir>/proposals.yaml
bash <skill-path>/scripts/migrate-scope.sh <scope-root> --tier2 <dir>/proposals.yaml --apply
```

Step 1 writes nothing to the scope. For every note it would migrate, it drops `<note-id>.extract.md` into `<dir>` holding that note's sections down to `## Raw Content` and no further, and appends an entry to `<dir>/proposals.yaml` keyed by note id, with the file it came from and `summary: ''` / `entities: []` waiting. Records get no extract; Tier 2 is a note concept.

**Generate `summary` and `entities` from the emitted extract and from nothing else.** Not the note on disk, and never raw content. The extract is the reviewed layer, it is the only text the script can hold a proposal against, and a name that appears only below the fence came out of a transcript nobody checked. Each summary is one line that asserts nothing the extract doesn't support: no date, name, decision, or outcome that isn't already up there. Each entity is a canonical name appearing in the extract verbatim.

The apply enforces the half it can. An entity missing from that note's extract gets `tier2-entity-unsourced` and the note is left exactly as it was, never written halfway. A summary spanning lines gets `tier2-summary-multiline`, since it would fail `frontmatter-single-line` the moment the lint ran. Both land in the "needs a human" list with everything else.

Tier 2 rides along with the Tier 1 apply rather than following it. Once a note carries `schema: 2` the migrator skips it whole, so there is no adding summaries to a scope that already migrated. Run the extract before you apply anything.

**Tier 2 is approved separately from Tier 1.** A plain `--apply` writes no `summary` or `entities` key anywhere, so approving the tier you can check never ships the one you can't. Tier 2's own approval is per file or one batch, whichever the user wants: the dry run prints each proposal inside the diff for the file it belongs to, so a reviewer reads a proposed summary against the note that would get it, and can rewrite one without touching the rest.

Rejecting a proposal is an absence, not a rollback. Leave a note out of the proposals file and it still migrates, because Tier 1 never waits on Tier 2, and it comes out byte-identical to what a Tier-1-only apply would have written. There is nothing to undo, because nothing was written.

### Verifying a Migration

```bash
bash <skill-path>/scripts/verify-migration.sh <scope-root> --since <pre-migration-ref>
```

The closing sweep, and it stands apart from the migrator on purpose: it reads git history rather than the working tree, so it works just as well on a migration someone applied and committed last week. It lints the scope, confirms every wiki-link target the scope carried at `<ref>` still resolves (by filename first, then by the trailing ten-character id, and it says how many needed that fallback), and reads `git diff --name-status -M <ref>` for anything renamed or deleted. Failures carry `verify-lint`, `verify-link`, or `verify-rename`, so the report names what broke.

Verification reports and never repairs. It prints every failure it found rather than the first, changes nothing on disk, and exits nonzero.

A passing run ends by printing one paragraph carrying the scope, the date, and the run's counts, for the user to paste into the scope's patterns journal. Offer it; don't write it. Nothing under the scope is touched, `patterns-journal/` included. A failing run prints no paragraph, because a migration that didn't verify has nothing paste-ready to say.

---

## Frontmatter Quick Reference

Full shapes live in the templates, and the rules behind them in [references/machine-contracts.md](references/machine-contracts.md). Values stay on one line, lists are inline arrays, and the block closes inside the first 20 lines. Omit any key you don't need; the order below is fixed among the keys you keep.

**Groomed note**, in order:

```
schema, body_schema, id, date, type, summary, attendees, tags, topics, entities, source_file, raw_file, transcript_corrections, open_questions, resolved_questions, deferred_tensions, unpromoted_candidates, related
```

**Memory record** (memory-bank-aligned), in order:

```
schema, body_schema, id, memory_type, title, status, date, effective_from, effective_to, last_confirmed, source_refs, applies_to, owners, tags, themes, related, exception_to, supersedes, superseded_by
```

`status` is `proposed|accepted|superseded|deprecated|rejected`. Type-specific body fields are in [references/memory-bank-schema.md](references/memory-bank-schema.md).

Files with no `schema` key are v1. They stay legal forever, and a scope holding both generations is a supported state rather than an unfinished migration. The lint checks one thing on them, whether their wiki links resolve, because a link resolving to no file is broken whichever generation wrote it.

`memory_type` values depend on the scope's chosen memory mode:
- **Lightweight** (default): `Decision | Context | Rule`. Exception is folded into Decision.
- **Canonical**: `Decision | PolicyRule | Exception | Context`. Matches the upstream reference architecture exactly.

The scope's `CLAUDE.md` declares the mode in its top frontmatter blockquote. Read it before flagging candidates so the suggested type uses the right vocabulary.

**Journal entry** follows the record order, using `themes` in place of `tags` and `status` values of `current|superseded|archived`. Its `source_refs` are compound strings of the form `<scope-path>::<note-id>`, so a moved note doesn't break the reference. Body is free prose.

---

## Filename and ID Conventions

- All IDs come from the globally-installed `nanoid -s 10` CLI. Never generate manually or via Python's random module.
- Notes: `YYYY-MM-DD-<slug>-<nanoid>.md`.
- Memory records: `<slug>-<nanoid>.md` inside the type folder.
- Journal entries: `YYYY-MM-DD-<slug>-<nanoid>.md` inside `entries/`.
- Slugs: lowercase, kebab-case, 3-6 words, descriptive of the primary subject.

---

## Operating Rules

- **Stage, never auto-commit.** Outputs are proposals. Never run `git commit` unless the user asks.
- **Preserve raw content as the source of truth.** Memory records cite notes; they don't replace them.
- **One groomed note per input.** No four-file fragmentation. Sections, not separate files. The raw sidecar under `notes/raw/` is not a second note: it holds the unreviewed raw text and nothing from the reviewed layer.
- **Never auto-promote across scopes.** Scope is decided at flagging time, confirmed at sign-off, sticky after crystallization. If a record needs to move, the user moves it by hand. (This trades convenience for audit safety — at high enough volume, v2 may add a guarded `promote` mode.)
- **`last_confirmed` is written without sign-off.** The gate on `_memory/` — no file written until the user approves that item — has one exception, and this is it. When an input confirms a claim an `accepted` record already makes, the run stamps the confirming note's date onto the record and names it in the phase 6 report instead of asking. Everything else stays gated: creating a record, amending one, superseding one, changing a word of what one claims. What the stamp touches is metadata rather than content — a date recording when the claim was last seen to hold, never the claim itself — which is what makes it safe to leave ungated. It stays that narrow on purpose. A prompt whose answer is always yes, in front of every input, teaches the user to approve without reading, and the gate is then worth nothing on the writes it exists for.
- **Cross-scope references are fine.** A project note can wiki-link to a client-scope record. A client record can list project note ids in its `source_refs`. The record's _home_ (which `_memory/` it lives in) defines its scope, not its references.
- **Don't open `raw_file` unless verifying a quote.** When reading a note to answer a question, read its extracted sections and leave the sidecar closed. Those sections are the reviewed layer and are what you came for. The raw text is for a human reading back, and for verifying a quote you have specific reason to doubt. Opening it by default pulls a whole transcript into context to answer something the sections already answered. A note with no `raw_file` still holds its raw text inline, so read it down to `## Raw Content` and no further.
- **Never rename, resolve by id.** Files keep the name they were created with and ids never regenerate. Resolve a wiki link as a path from the linking note's directory first, which is how a cross-scope link resolves, then, where the target holds no `/`, by filename within the scope. When both miss, resolve by id. A `<slug>-<nanoid>` name carries its id as the ten characters that end the basename, with a hyphen right before them. The nanoid alphabet includes `-`, so the id can hold a hyphen of its own: `atlas-dry-run-prep-zFpm-hfD5u` carries `zFpm-hfD5u`, not the `hfD5u` after its last hyphen. The id search stays within the linking note's scope. A target whose basename lacks that suffix carries no id and has no id step. Report a link broken only after every step fails.
- **VTT raw content is collapsed, not verbatim.** Cues get merged into speaker turns with timestamps kept at turn boundaries, via `scripts/collapse-vtt.sh`. This is the one sanctioned exception to preserving raw content exactly as captured. A wall of two-second cues is unreadable to the human the zone exists for, and the words themselves are unchanged. A blank line separates the turns, because markdown runs consecutive non-blank lines together as one paragraph; `scripts/reflow-raw.sh` repairs notes groomed before that separator existed ([references/migration.md](references/migration.md)). Captions carrying no speaker label collapse one turn per cue under `@unknown`, the same token an open question uses for a resolver nobody named. Attribute unlabelled speech to `@unknown` even when a neighbouring turn makes a name look obvious. When the collapser exits nonzero it has refused the file and written no usable output: report the line it names, leave the source in `_inbox/`, and groom nothing from it.

---

## When NOT to Use This Skill

- The user has a single ad-hoc note they want to write directly. The skill is for queue-driven processing, not freeform composition.
- The cwd is not inside an opted-in directory and the user hasn't asked to scaffold one. Do not silently create memory infrastructure where none was intended.
- The user is asking about memory records for an existing skill or code repo. This skill targets consulting notes in an Obsidian vault. Code-repo memory wants the memory-bank reference architecture this skill borrows from, not this skill.

---

## Further Reading

- [references/extraction-heuristics.md](references/extraction-heuristics.md) — quote selection, tension surfacing, assumption mining.
- [references/scope-decisions.md](references/scope-decisions.md) — full heuristics for proposing project vs client vs journal scope.
- [references/memory-bank-schema.md](references/memory-bank-schema.md) — vendored summary of the substrate schema. Inspired by, not bound to.
- [references/retrieval-funnel.md](references/retrieval-funnel.md) — token-efficient four-stage retrieval at scale.
- [references/machine-contracts.md](references/machine-contracts.md) — the frontmatter contract and the closed token grammar, both enforced by the lint.
- [references/migration.md](references/migration.md) — what Tier 1 migration changes, what it refuses to guess, and the safety properties behind both.
