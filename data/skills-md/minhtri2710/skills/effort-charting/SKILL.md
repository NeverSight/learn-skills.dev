---
name: effort-charting
description: Chart an effort too large or too foggy for one context as a map of decision tickets with an explicit not-yet-specified section, then, once the way is clear, split the approved spec into tracer-bullet slices with blocking edges. Use when a loose idea arrives that no single session can hold, or when an approved spec needs breaking into agent-sized tickets. Do not use for a task that fits one session, for partitioning a scoped issue among parallel peers, or for deciding module boundaries; that is capability-map.
---

# Effort Charting

A big effort arrives wrapped in fog: the way from here to the destination is not
visible. Charting finds the way; it does not charge at the destination. Two
phases, each with its own artifact: decisions first, then slices to build.

## Phase 1: the map

**Name the destination first.** It is the spec to hand off, the decision to lock,
or the change to make in place. It fixes the scope, so it is settled before any
ticket exists. Then interview breadth-first across the whole space, not deep on
one thread, to surface the open decisions and the first steps takeable now. If
this surfaces no fog, the effort fits one session and needs no map; stop and say
so.

The map is one record in the project's tracker or task manager, and it is an
index, not a store:

```markdown
## Destination
## Notes            <- domain, skills every session should load, standing preferences
## Decisions so far <- one line per closed ticket: name, gist, link to the ticket
## Not yet specified
## Out of scope
```

**Decision tickets** are children of the map. Each holds one question whose
resolution is a decision, sized to one fresh context, typed as research (done
alone), prototype or grilling (done with the human; an agent never answers the
human's side), or task (manual work that unblocks a decision). Blocking uses the
tracker's own dependency relation so the frontier — open, unblocked, unclaimed
tickets — is visible without opening the map. Refer to tickets by name, never by
bare id.

**Fog or ticket?** The test is whether the question can be stated precisely now,
not whether it can be answered now. Sharp but blocked is a ticket; not yet
phrasable goes under *Not yet specified*, coarser than a ticket, and graduates
into tickets as resolutions clear the view. Work ruled beyond the destination is
*Out of scope*, closed, and never graduates; it returns only as a new effort.

Working the map: load the low-resolution map, claim one frontier ticket before
any work, resolve it, record the answer on the ticket and one line in *Decisions
so far*, then add the tickets the answer made specifiable and close any it made
moot. One decision per session, so each starts from a clean primary source; only
research tickets may run in parallel.

## Phase 2: tracer slices

Once nothing remains to decide, split the approved spec into vertical slices:

- each cuts a narrow but complete path through every layer, demoable or
  verifiable on its own; never a horizontal layer;
- each is sized to one fresh context;
- any prefactoring that makes the change easy comes first, as its own slice;
- each declares its blocking edges; a slice with none can start now.

Present the breakdown as a numbered list with title, blocked-by, and the
end-to-end behavior it delivers, and iterate until the user approves granularity
and edges. Publish one ticket per slice in dependency order, describing behavior
in the glossary's terms and naming types and contracts rather than file paths or
line numbers, which go stale. Work the frontier. A wide mechanical refactor whose
blast radius no slice can land green is one ticket done in one cut, updating every
caller; it is not staged behind a parallel old form.
