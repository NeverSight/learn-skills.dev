---
name: docs
description: "Project docs system: sync codebase to docs, research what to build next, or work on a roadmap item."
argument-hint: <sync|research|work> [topic or doc path]
---

# Docs

Project memory system. Pick an action:

- **`/docs sync`** — Map codebase to references, update roadmap statuses
- **`/docs research`** — Discover and formalize what to build next into a roadmap doc
- **`/docs work`** — Execute a roadmap item, then update references

Match the first argument to the corresponding section below.

## Core Model

- `.docs/reference/` = **what exists in the codebase**. Sync writes here.
- `.docs/roadmap/` = **what should exist but doesn't yet**. Research writes here. Organized by status.
- `.docs/decisions/` = decision records. Any command can create these.
- `.docs/logs/` = chronological record of all agent work and decisions. Any command writes here after completing substantial work. Exists so every dev in a shared repo can see what agents did and why.

## Rule Levels

- **Required** — Must be followed.
- **Recommended** — Strong default guidance.

## Global Rules (required)

1. **Command contract** — only `sync`, `research`, `work`.
2. **Docs root + folder contract** — this skill manages `.docs/` with only these top-level folders:
   - `.docs/reference/`
   - `.docs/roadmap/`
   - `.docs/decisions/`
   - `.docs/logs/`
   - Inside `.docs/reference/`, use:
     - `features/`
     - `architecture/`
     - `conventions/`
     - `runbooks/`
     - `pitfalls/`
   - Inside `.docs/roadmap/`, use status folders:
     - `proposed/` — ideas formalized, not started
     - `in-progress/` — actively being worked on
     - `completed/` — fully shipped
     - `archived/` — superseded, rejected, or deprioritized
3. **Naming + date rules**
   - `reference/*` → `kebab-case.md`
   - `roadmap/**`, `decisions/` → `YYYY-MM-DD-kebab-case.md`
   - `logs/` → `YYYY-MM-DD-kebab-task-name.md` per-task logs
   - Dates must be zero-padded ISO 8601: `YYYY-MM-DD`.
4. **Append-only history** — for `logs/` and `decisions/`, add new files instead of rewriting history.
5. **Log after every complete piece of work** — whenever an agent finishes substantial work (pushing a PR, completing a sync, finalizing a research recommendation, shipping a feature), create a log entry at `.docs/logs/YYYY-MM-DD-kebab-task-name.md`. The log captures what was done, decisions made, and rationale — so every developer in the repo can reconstruct what agents did and why.
6. **Roadmap status lifecycle** — track status by moving docs between roadmap folders:
   - `proposed/` → `in-progress/` → `completed/`
   - Items that won't be built go to `archived/` with a note explaining why (superseded, rejected, deprioritized)
   - Every roadmap doc must still have a `## Status` line for quick context (e.g., `Proposed`, `In Progress`, `Completed (YYYY-MM-DD)`, `Archived — superseded by [link]`)
7. **Policy files** — if `AGENTS.md` and/or `CLAUDE.md` exist, keep their docs-memory guidance aligned.
8. **Conflict behavior** — if repository conventions conflict with these defaults, do not rewrite conventions silently. Report the mismatch and ask the user before changing direction.

## Global Rules (recommended)

- Prefer focused, single-purpose docs.
- Prefer updating existing docs before creating new ones.
- Keep docs concrete and scannable.
- Treat code as ground truth; avoid full schema dumps in docs.

---

## sync

Fully map the codebase into `.docs/reference/`. Also update roadmap statuses for shipped work.

**Completeness requirement:** Sync must resolve ALL findings before completing. Do not defer undocumented systems, stale docs, or partial docs to "a future sync." Every implemented system must have a corresponding reference doc when sync finishes. If the scope is large, batch the work — but finish it in this run.

### 1. Ensure structure

Runs every sync to keep the folder structure intact. Idempotent — creates what's missing, leaves everything else alone. Never overwrites or removes existing files or folders.

1. Ensure all folders exist (create any that are missing):

```
.docs/
├── README.md
├── reference/
│   ├── features/
│   ├── architecture/
│   ├── conventions/
│   ├── runbooks/
│   └── pitfalls/
├── roadmap/
│   ├── proposed/
│   ├── in-progress/
│   ├── completed/
│   └── archived/
├── decisions/
└── logs/
```

2. If `.docs/README.md` is missing, create it with:
   - A short purpose line for `.docs/`
   - Folder purposes and structure description
   - Naming/date/append-only conventions from Global Rules

3. If `AGENTS.md` and/or `CLAUDE.md` exist but lack docs guidance, add a brief section:
   - `.docs/` is the project memory system. See `.docs/README.md` for conventions.
   - After substantial work (PR, feature, refactor), log what you did and why to `.docs/logs/YYYY-MM-DD-task-name.md`.

### 2. Audit docs vs code

1. Read `.docs/README.md`, then review all files under `.docs/reference/`, `.docs/roadmap/`, `.docs/decisions/`, and `.docs/logs/`.
2. Use repository search to check what exists in code (schema, services, routes, UI, jobs, APIs).
3. Compare every reference doc against current code for accuracy.
4. Identify implemented systems that have no reference doc.
5. Check roadmap items — have any been shipped? Should any move between status folders?

### 3. Classify findings

Use this taxonomy:

- **Stale** — reference doc is materially incorrect vs current code
- **Partial** — reference doc exists but is missing significant implemented behavior
- **Undocumented** — important implemented system has no reference doc
- **Roadmap shipped** — roadmap item has been implemented and should move to `completed/`

### 4. Sync (required — must resolve ALL findings, no deferral)

Resolve every finding discovered in steps 2-3. Do not skip, defer, or deprioritize any item:

- **Stale docs** — update to match current code.
- **Partial docs** — fill in the missing sections from code evidence.
- **Undocumented systems** — create new reference docs (`features/`, `architecture/`, `conventions/`, `runbooks/`, or `pitfalls/` as appropriate).
- **Shipped roadmap items** — move the roadmap doc to `completed/` and update its `## Status` line.
- Add or update `conventions/`, `runbooks/`, and `pitfalls/` entries when repository evidence exists.

If a change would alter repository conventions or policy direction, report the mismatch and ask before making that change.

### Output Contract (required)

When `/docs sync` completes, return all of:

1. **Bootstrap status** — `created` or `already present`
2. **Coverage table** with this exact header:

```
| System | Doc | Status | Action taken |
|--------|-----|--------|--------------|
```

3. **Summary** — counts by status (stale fixed, partial filled, undocumented created, roadmap updated)
4. **Docs changes made** — list updated/created/moved paths, or `none`
5. **Log entry** — create `.docs/logs/YYYY-MM-DD-sync.md` capturing what was synced, key findings, and decisions

---

## research

Discover what to build next and formalize it into a roadmap doc.

### 1. Scan for candidates

Work through these lenses. Not all will apply to every product — use what's relevant:

**Usage and behavior** — What are users actually doing?
- If analytics tools are available, check usage patterns, funnels, retention, and drop-off points
- Identify features that are heavily used (double down) vs unused (cut or rethink)

**Demand** — What are users asking for?
- Check issue trackers, feature request backlogs, and support channels for patterns
- Look for frequently requested capabilities or common complaints

**Pain** — What's broken or frustrating?
- Check `.docs/reference/pitfalls/` and `.docs/reference/runbooks/` for recurring operational pain
- Look at bug reports, incident history, and support escalations

**Strategy** — What's the current direction?
- Read `.docs/roadmap/` for existing plans and their statuses
- Read `.docs/reference/features/` for gaps, limitations, and natural next steps
- Consider business goals and priorities the user has communicated

**Landscape** — What's happening externally?
- Research competitors, adjacent tools, and market shifts if relevant
- Identify opportunities others are capitalizing on

**Technical opportunity** — What does the codebase reveal?
- Scan code for `TODO`, `FIXME`, `HACK`, stubs, and dead paths
- Identify tech debt that's actively slowing down development

**Vision** — What's possible that doesn't exist yet?
- What adjacent problems could we solve with what we've already built?
- What emerging capabilities or trends could we leverage?
- What would the product look like if we removed current constraints?
- What would make users say "I didn't know I needed this"?

Narrow to user-specified domain if provided.

### 2. Rank candidates

Rank by:

- impact (user value, pain reduction)
- readiness (how much groundwork already exists)
- size (`small`, `medium`, `large`)

### 3. Propose shortlist

Use this exact header:

```
| # | What | Why now | Size | Readiness | Exists | Missing |
|---|------|---------|------|-----------|--------|---------|
```

### 4. Formalize the chosen item

Once the user picks an item (or accepts the recommendation):

1. Create a roadmap doc at `.docs/roadmap/proposed/YYYY-MM-DD-slug.md`
2. Required sections:
   - Opening line (plain-language summary of the problem)
   - Status (`Proposed`)
   - Why (problem statement, evidence, user impact)
   - What (concrete scope, deliverables)
   - How It Fits In (relation to existing systems, dependencies)
   - Non-Goals (explicit scope boundaries)
   - Open Questions (unresolved decisions)
3. Add cross-links from related reference docs if useful

### Output Contract (required)

When `/docs research` completes, return all of:

1. **Shortlist table** (3-5 rows)
2. **Recommended item** (`#<n>` + one-sentence reason)
3. If formalized: **roadmap doc path**, **open questions**
4. **Next command** suggestion (`/docs work <path>` or another `/docs research` for a different domain)
5. **Log entry** — create `.docs/logs/YYYY-MM-DD-research-<topic>.md` capturing what was investigated, candidates considered, and the recommendation rationale

---

## work

Execute a roadmap item. Build it, then close the loop in docs.

### 1. Understand task

- If user gives a roadmap doc path, read it first
- If user gives a description, find the related roadmap doc in `.docs/roadmap/`
- If no roadmap doc exists, ask: should we create one first (`/docs research`) or proceed directly?
- If ambiguous, clarify scope briefly
- Move the roadmap doc to `in-progress/` if it's still in `proposed/`

### 2. Gather implementation context

- Read the roadmap doc and any related reference docs
- Inspect existing code patterns in touched areas
- Check project rules and conventions

### 3. Build

- Plan first if scope is large (using your environment's planning workflow)
- Implement the change
- Run verification commands

### 4. Close the loop

After implementation is complete:

- **Update reference docs** — create or update `.docs/reference/` docs to reflect the new code (features, architecture, conventions, runbooks, pitfalls as appropriate)
- **Update roadmap doc** — move to `completed/` and update `## Status` to `Completed (YYYY-MM-DD)`, or move to `completed/` with `Partially Completed (YYYY-MM-DD)` and notes on what remains
- **Log entry** — create `.docs/logs/YYYY-MM-DD-kebab-task-name.md` capturing what was done, key decisions made, and why

### Output Contract (required)

When `/docs work` completes, return all of:

1. **Scope delivered**
2. **Code files changed**
3. **Verification** — commands + pass/fail
4. **Docs updated** — list reference/roadmap/log paths, or `none`
5. **Follow-ups** — remaining work or `none`
