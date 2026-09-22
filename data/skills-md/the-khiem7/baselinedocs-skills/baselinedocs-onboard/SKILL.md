---
name: baselinedocs-onboard
description: Load, ingest, or absorb an existing adaptive baseline pack or initiative into working context completely, reading every document in full before any planning or implementation discussion. Use when the user asks for a doc pack to be loaded before work starts, and wants the agent to hold the pack's entire state rather than a forward-looking summary.
---

# Baseline Docs Onboard

Load a pack into working context and report the state it records. The deliverable is a loaded agent, not a new document. Nothing is written.

Read `references/pack-contract.md` in full before reporting the pack state, every time. It is the only definition of which document owns which content, the entry-index shape, and what a phase or an open question records; do not infer any of it from a filename, from an earlier session, or from memory.

Read `references/report-style.md` in full before reporting to the user, every time. It governs how a pack element is named in conversation; an identifier stated without its meaning is a question the user has to ask.

## Inputs

Determine or confirm:

- the pack root or the initiative index path
- the scope. For an initiative the default is one domain pack, not the whole set
- whether linked wiki articles are in scope
- whether retained source material is in scope

## Workflow

1. Classify the target: a single pack, an initiative with an index, or an initiative whose sub-packs have no index.
2. Route before loading. A single pack needs no routing: go to step 4. For an initiative, read the index, stop, and read no sub-pack content yet. With no index, build the same view from each sub-pack's frontmatter and next action, report the missing index, and name `baselinedocs-maintain-split`. Never write the index: a reader can only record links it inferred, not the edges an author supplies.
3. Select the scope. When the routing evidence names exactly one sub-pack in progress, load it and state what named it. Otherwise present the routing table and ask. Bypass the question only on stated evidence, never on which pack looks more important.
4. Enumerate the selected scope. Report the file list with line counts before reading anything, and name what the scope excludes.
5. Apply the size gate. When you cannot say with confidence that the scope fits in remaining context, stop, present the total, propose a narrower scope, and wait. Uncertainty resolves toward asking, not toward starting.
6. Read every file in the agreed scope in full. Do not truncate, skim headings, sample sections, or substitute a search for a read.
7. Record provenance per document: `status`, `updated`, `code_ref`. `uncommitted` and `unknown` are provenance, not commits. A newer commit than a document's `code_ref` is the drift signal the contract describes, not a verdict to investigate here.
8. Follow links out of the pack. Read a wiki article when it is in scope; otherwise leave it unread and do not treat it as loaded.
9. Collect unresolved references: every point where a loaded document leans on something outside the scope, said in your own words and then quoted with its location. A decision cited without its content, a term used undefined, a link into another pack.
10. Report the sections `Output` defines, in that order. Render every section every time except `Cross-pack checkpoint`, which follows its own stated condition; when a section has nothing to report, say so rather than dropping its heading.
11. Stop. Do not propose, plan, or begin work unless asked.

## Reading Rules

- Complete means complete for the selected scope, not for everything reachable. Narrow openly before reading starts; never read part of what was then selected. An agent that believes it is loaded and is not is worse than one that knows it read nothing.
- Report the line counts read. Never summarize a document from its headings.
- Report state as the documents record it. Onboard describes; it does not assess progress, revise a status, or invent a next action.
- A dependency edge is status, not reading order. Report edges as stated; do not reorder reads around them, and do not pull in an excluded upstream pack.
- Collect references from the text, not from the edges: an edge can be purely operational, and a pack can lean on one it has no edge to.
- An unresolved reference is a stated gap. Report it, say that an answer touching it is unbacked, and offer to load what it names. Do not load unasked, and do not answer around the gap as though it were closed.
- Dependency edges and the cross-pack checkpoint live only in the index. Without one they are missing, not derivable: do not infer them from directory names, alphabetical order, or the import graph.
- Do not resolve a contradiction found while reading; report it. `baselinedocs-sync-reconcile` owns the repair. Index status disagreeing with a pack's own `status` is one of these: do not treat the index as authoritative and do not prefer the newer `updated`.
- Retained source material is out of scope unless the user includes it: a `sources/` directory, or any file in the pack without baseline frontmatter. `baselinedocs-adopt` already distributed its information into the documents, so reading both loads the same content twice, and the source is usually the largest file present.
- Do not update frontmatter, dates, or status. Onboard writes nothing, including the index it just reported missing.

## Output

Five named sections, each its own heading, in this order: `Doc pack introduction`, `Roadmap and Opens`, `Next actions`, `Cross-pack checkpoint`, `Unresolved references`. Render every section as headings and nested bullets, never as a paragraph; a paragraph is for an argument that must be followed in order, and a report is not one.

`Doc pack introduction`: one sub-heading per pack in scope, named for the pack. Under it, one bullet for scope and one bullet for target, as `introduction` records them. Report what it records; do not reproduce it, and do not fold scope and target into one paragraph.

`Roadmap and Opens`: one sub-heading per pack in scope, holding that pack's table. One row per phase, four columns: the phase identifier, a short phrase of what the phase did, its status in the pack's own word for it, and the identifiers of any open question recorded against that phase, or a dash. This is the contract's entry-index shape, identifier and about and status and related, applied to a phase instead of a decision; `report-style.md`'s stated exception is what lets this table run to four columns. When a phase needs more than the phrase column holds, add a bullet below the table naming the phase identifier; never widen a cell into a sentence. Under the table, a bulleted list titled `Not tied to a phase` for any open question the pack records without a phase link; omit that list when the pack has none.

`Next actions`: one sub-heading per pack in scope. Under it, one bullet per action item, ordered from easiest and least urgent to hardest and most urgent. An item is the pack's recorded `Next action`, its instructions split one per nested bullet, or an open question the pack's own next action names as something it cannot proceed past. Head each item with what it is and close with its identity tag as inline code; nest its instructions under it, restructured under the report-style next-action rule so what they tell the user to do survives unchanged, none added, none softened. Rank on two recorded signals, never on unstated judgment: whether the pack already records a recommendation for the item, which ranks easier than one with none, since approving a recorded answer is easier than originating one; and how many other recorded items are blocked on it or waiting on it, which ranks more urgent the higher that count. State the signal beside the item, so the ranking is checkable against the pack rather than taken on trust.

`Cross-pack checkpoint`: only when the scope sits inside a multi-pack initiative. Omit the heading when the index records no dependency edge and no coupling note touching an in-scope pack; an empty heading is the filler the contract's own omission rule exists to prevent. When it records one, report the index's own checkpoint narrative restructured as bullets, and pair the specific coupled entries or phases it names, for example "`family-design` FD-D30 amended one clause of `skill-consolidation` SC-Q6," rather than merging both packs' phase tables into one timeline. Phases in different packs run on independent per-pack counters with no shared date at phase granularity, only a document-level `updated` date each, so pairing the named entries is the fusion this section offers, not a unified chronology.

`Unresolved references`: one bullet per reference. Say in your own words what is missing, before quoting it, with its location.

## Non-Goals

- not a quick brief; onboard loads the pack in full, `baselinedocs-brief` reports position without loading
- not a drift audit; `baselinedocs-audit-drift` does that
- does not create the missing index; `baselinedocs-maintain-split` does that
- writes no files
