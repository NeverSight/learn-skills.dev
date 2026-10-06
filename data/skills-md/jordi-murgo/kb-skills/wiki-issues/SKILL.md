---
name: wiki-issues
description: Own the wiki/meta/OPEN-ISSUES.md issue stack end-to-end — push (synthesize session todos/insights into new stack entries with fresh IDs) and pop (verify and work exactly one top-of-stack issue). Triggers on "handoff", "synthesize issues", "file open issues", "fix issues", "work the top issue", "pop an issue", "open-issues stack".
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

# wiki-issues — OPEN-ISSUES.md stack owner (push + pop)

One skill owns the full lifecycle of `wiki/meta/OPEN-ISSUES.md`: creating it, pushing synthesized
issues onto it (the old `/wiki:handoff`), and popping-and-working exactly one issue from it (the old
`/wiki:fix-issues`). Realizes **ADR-0005** (new dedicated skill) under **ADR-0001** (skills-only).
Deterministic core lives in a colocated script (`scripts/lint-open-issues.py`, ADR-0002); the LLM only
synthesizes issue prose and judges verification.

**Language:** German for chat and issue bodies; English only for code identifiers / commit conventions
where the repo already established it.

## Which flow?
- Signals "handoff", "synthesize", "file issues", end-of-session capture → **push flow**.
- Signals "fix issues", "work the top issue", "pop" → **pop flow**.
- `wiki/meta/OPEN-ISSUES.md` absent → run **init** first, then the requested flow.

## Data model (hybrid: YAML stack + body sections)

`wiki/meta/OPEN-ISSUES.md` carries a `stack:` array in the frontmatter — the ordered work queue.
Each item:

```yaml
- id: I-2026-NNN               # year-resetting counter, never recycled
  priority: P0|P1|P2|P3
  section: <whitelist>          # one of the 12 below
  title: "…"                    # identical to the H3 body header
  pushed: YYYY-MM-DD
  blocked_by: [I-2026-MMM, …]   # empty = ready
  inconclusive_since: YYYY-MM-DD # optional, paired with inconclusive_reason
  inconclusive_reason: "…"       # optional, paired with inconclusive_since
  aggregated_from: [I-…, …]      # optional, read-only (set by the aggregation path)
```

In the body, each item has a `### I-2026-NNN — Titel` section under its `## <section>` block, with a
meta line `**Priority:** … · **Pushed:** … · **WO:** …`. **Truth lives in the frontmatter**; body lines
(`**Blocked by:**`, `**Note:**`) mirror it.

**Section whitelist (12 — reconciled, audit V-6).** Detail + meanings in
[references/open-issues-template.md](references/open-issues-template.md):
`enforcement` · `lint` · `tooling` · `ci` · `hooks` · `docs` · `templates` · `skills` ·
`skill-plugin` · `vault-content` · `eval-observability` · `dragonscale`

**Sort invariant (4 keys, lint-enforced — never LLM-sorted):** priority ASC (P0 first) · ready-first
(empty `blocked_by`) · inconclusive-last within a priority group · `pushed` DESC (LIFO tiebreaker).

## Deterministic core — the validator
`scripts/lint-open-issues.py` (ported from the battle-tested `ai-secondbrain` reference, colocated per
ADR-0002) checks schema, stack↔body parity, `blocked_by` referential integrity + cycles,
inconclusive pairing, aggregated-from consistency, and the 4-key sort. It is also wired into
`scripts/run-lint.py` so `totals.error` gates CI. **Run it after every mutation** and before every
commit: `python3 skills/wiki-issues/scripts/lint-open-issues.py --json wiki/meta/OPEN-ISSUES.md`.
A non-zero error count means the file is broken — do not commit.

## Format-version guard (before ANY write)
Before mutating an existing `OPEN-ISSUES.md`, confirm it is the hybrid schema: the frontmatter MUST
carry a `stack:` array. If it does not (a legacy flat file, or a hand-edited hybrid that lost its
stack), **refuse to write** and surface the `lint-open-issues` diagnostics — do not blindly overwrite.
*(Reference failure I-2026-041: a stale flat command nearly corrupted the hybrid file.)* Recover by
migrating the file to hybrid by hand (or re-init if empty), then retry.

## Pre-conditions (hard guardrails — both flows)
1. `git status --porcelain wiki/meta/OPEN-ISSUES.md` — if **dirty**, ABORT: the user must commit or
   stash first, so the operation runs against a clean baseline. If clean, continue.
2. `git log -1 --oneline -- wiki/meta/OPEN-ISSUES.md` — note the current commit hash for the final report.

---

## init flow (scaffold when absent)
If `wiki/meta/OPEN-ISSUES.md` does not exist:
1. Copy the skeleton from [references/open-issues-template.md](references/open-issues-template.md) into
   `wiki/meta/OPEN-ISSUES.md` with an empty `stack: []`, `created`/`updated` = today.
2. Run the validator — a freshly scaffolded file MUST be lint-green (zero errors).
3. On a **pop** request against a just-initialized file, report "empty stack, nothing to do".

---

## push flow (was /wiki:handoff — synthesize session items → stack entries)

Goal: turn open todos, bugs, and non-trivial observations from the session into **synthesized** issues
so future sessions pop them by priority.

### P1 — read structure + determine the ID counter
`Read wiki/meta/OPEN-ISSUES.md` fully. Capture the frontmatter `stack:` and the body sections.
Compute the next id for the current year (`I-YYYY-NNN`, zero-padded 3 digits):
1. Collect all `stack[].id` + all `aggregated_from` ids (deleted numbers still count).
2. Scan `wiki/log.md` for resolve entries of the current year (`I-2026-(\d{3})`).
3. `next_id = max(observed NNN) + 1`; if the year has no ids yet → `I-2026-001`.

**No id recycling** — deleted or aggregated numbers are never re-assigned. First push of a new year
starts `I-<year>-001`.

### P2 — synthesize (not copy-paste)
Extract issues from the session (user messages, tool outputs, own observations) that are:
- **Concrete, not vague.** "X loses Y in `<file>:L42`" — accepted. "refactor should happen somewhere" — rejected.
- **Anchored (`WO:`).** A file, path, line, or clear area. Without an anchor it belongs in
  `wiki/questions/` or `wiki/decisions/`, not here.
- **Not raw session state.** "we were debugging X when context ran out" belongs in working notes.
- **Aggregated when convergent.** 3+ new issues sharing one root → one bundled issue, not near-duplicates.

Choose `section` from the 12-item whitelist. If an issue honestly fits none, **propose a new section to
the user before filing** — never invent one silently.

Per issue: one **stack item** (`priority` default P2, user may override e.g. "handoff P1"; `blocked_by`
default `[]`, set an id if prose says "only after X"; `pushed` = today) + one **body section** under the
matching `## <section>`:
```
### I-2026-NNN — <short title — WHAT>
**Priority:** Pn · **Pushed:** YYYY-MM-DD · **WO:** `<path[:line]>`

<one sentence: symptom or risk, WHY>.
```
Optional `**Blocked by:** [[#I-2026-MMM]]` line when `blocked_by` is set.

### P3 — insert (priority-sorted)
Insert each new stack item so the array stays sorted by the 4-key invariant (priority ASC, ready-first,
`pushed` DESC). Do **not** naively prepend — insert at the correct position. Append body sections to the
end of their `## <section>` block (body order is cosmetic; the work order lives in the stack).

### P4 — verify the edit
Before commit, `git diff wiki/meta/OPEN-ISSUES.md` and confirm: frontmatter `updated:` = today · no
existing item changed · `stack[].id` set == `### I-…` header set (no drift) · every new id unique +
`I-YYYY-NNN` · every `section` ∈ whitelist · every `blocked_by` target exists · sort correct. Then run
`lint-open-issues --json` — zero errors required.

### P5 — commit
Exactly one commit: `docs(meta): handoff <N> open issues from <session topic>` (+ optional 1–2 context
lines). Use the user's topic argument if given, else derive a terse description.

### P6 — final report (3 lines)
```
Filed: <N> new issues (IDs <I-…, I-…>) in sections: <X, Y, Z>.
Top of stack: <id + title of the now-top ready item>.
Commit: <short-hash> <subject>.
```

### push does NOT
Edit or move existing issues · file issues without a `WO:` anchor · set `aggregated_from` (that is the
pop aggregation path) · recycle ids · mass-reorganize sections (a structure change is a separate manual commit).

---

## pop flow (was /wiki:fix-issues — verify and work exactly ONE issue)

Goal: work **exactly one** issue per invocation. Verify against current repo state rather than blindly fixing.

### Hard rules (non-negotiable)
- **Exactly one issue per invocation.** For more, the user re-invokes.
- **Never edit OPEN-ISSUES.md without a clean git baseline.** Check before, commit after.
- **Never aggregate silently.** The aggregation path (F3/F7) needs explicit user consent.
- **Never delete an issue that could not be verified.** Inconclusive → the item stays (F4d).
- **Never let stack and body drift.** After every edit, `stack[].id` set must equal the `### I-…` header set. Drift = abort.

### F1 — read the file fully
`Read wiki/meta/OPEN-ISSUES.md`. Parse the frontmatter `stack:` and inventory body sections. Reconcile
the `stack[].id` set against the `### I-…` header set — on drift, ABORT immediately (run
`lint-open-issues` for the diagnostic). Apply the **format-version guard** here.

### F2 — identify top-of-stack
The top issue is the **first stack item whose `blocked_by` is empty**. The array is already sorted
(priority ASC / ready-first / `pushed` DESC), so the first ready entry is the highest-priority workable
issue. The body detail is its `### I-2026-NNN` section. Note the id, title, and `WO:` anchor verbatim.

Edges:
- **Empty stack** → "Keine offenen Issues. Nichts zu tun." Abort, no commit.
- **All items blocked** (every `blocked_by` non-empty) → "Stack hat nur blockierte Items: [<ids>]. Bitte Blocker zuerst auflösen." Abort, no commit.

### F3 — aggregation scan (MANDATORY, once, before any change)
Ask: would **one** larger fix (plugin update, script rewrite, fundamental rework) deterministically
resolve the top issue **plus at least two others**?
- **No** → continue to F4.
- **Yes** → STOP and present the choice, wait for the answer (never pick a default, never aggregate without consent):
  ```
  Aggregations-Vorschlag: Issues [<ids>] könnten gebündelt durch einen größeren Fix
  ([Plugin-Update X / Skript-Rewrite Y / Refactor Z]) gemeinsam erledigt werden.
  Optionen:
    (1) Nur Top-Issue fixen ("<top-titel>").
    (2) Aggregieren: die N Issues zu einem neuen Top-Issue "<Aggregations-Titel>"
        zusammenfassen; die anderen entfernen. Der Fix wird NICHT jetzt gemacht —
        das aggregierte Issue wird committet und später via pop bearbeitet.
  Antwort (1) oder (2) bitte.
  ```
  - **(1)** → F4 with the original top issue. **(2)** → jump to F7 (aggregation path). No answer → end without change.

### F4 — verify the top issue against the repo
Check the `WO:` anchor: file named → `ls`/`Read`, does it exist, is the symptom reproducible? line named
→ `Read <file>` ±5 lines, is the content still there? missing tooling → `ls`/`Glob`, still absent?
script/hook behavior → run it read-only and compare output to the claim. Four outcomes:

- **F4a — already resolved** (symptom gone): remove the stack item **and** its `### I-…` body section
  (both). Prepend a `wiki/log.md` entry (`## [YYYY-MM-DD] verify | resolved: <id> <titel>` with an
  evidence line + one-sentence root cause). `updated:` = today. Check stack/body sync. → F5.
- **F4b — stale but partly true** (line number / count drifted): do **not** remove. Patch the inaccurate
  part of the body section in place (fix the line number, update the count). Do not change `pushed`. No
  log entry (issue stays open). `updated:` = today. → F5.
- **F4c — still real** (valid and not done): perform the fix with conventional tools (Edit/Write). Then
  remove the stack item + `### I-…` section (both), prepend a `wiki/log.md` entry
  (`## [YYYY-MM-DD] fix | <id> <titel>` with Change + Why). `updated:` = today (both files). Check sync. → F5.
- **F4d — inconclusive** (verification without a clear result, e.g. sandbox / missing tool): do **not**
  remove. Set `inconclusive_since: <today>` + `inconclusive_reason: "<grund>"` on the stack item; add a
  `**Note:** inconclusive since <today> — <grund>` line to the body section (mirror). The sort invariant
  places it last within its priority group so the next pop does not re-snag on it. `updated:` = today. → F5.

### F5 — commit discipline
- **F4a (resolved, no code fix):** one commit `chore(meta): resolve "<id> <titel>"` (evidence + "removed from stack + body, logged in wiki/log.md").
- **F4b (stale patch):** one commit `chore(meta): patch stale ref in "<id> <titel>"`.
- **F4c (real fix):** up to two commits — (1) the code fix `fix(<scope>): <was>` or `feat(<scope>): <was>`; (2) the meta update `chore(meta): resolve "<id> <titel>"`.
- **F4d (inconclusive):** one commit `chore(meta): mark "<id> <titel>" inconclusive (since <YYYY-MM-DD>)`.
Never `--no-verify`, never `--amend` (build fresh commits for a clean history). Run `lint-open-issues`
before every commit — zero errors required.

### F6 — final report (3 lines)
```
Top-Issue: <id> <titel>.
Outcome: <resolved | patched-stale | fixed | inconclusive | aggregated>.
New top of stack: <id + titel of the next ready item>.
```
Optional 4th line with the commit hash of the final change.

### F7 — aggregation path (only when the user chose (2) in F3)
1. Remove all N affected stack items + their N `### I-…` body sections.
2. Create **one** new stack item with the next free id describing the bundled fix, plus its body section
   under the right `## <section>`. Set `aggregated_from: [<id-1>, …, <id-N>]`. `priority` = highest of the N.
3. `updated:` = today. Check stack/body sync.
4. Do **not** perform the fix — the point is consolidation, not immediate resolution.
5. One commit `chore(meta): aggregate <N> issues into "<id> <aggregations-titel>"` (lists the replaced ids + one-sentence rationale).
6. Final report as F6, Outcome = `aggregated`.

### pop edge cases
- `stack` empty → "Keine offenen Issues." Abort, no commit.
- All items blocked → list blocked ids, abort, no commit.
- `blocked_by` points to a non-existent id → hard abort, `lint-open-issues` hint, no edit.
- Stack/body out of sync → hard abort, no edit, lint hint.
- Verification fails for technical reasons (sandbox, missing tool) → that is F4d (inconclusive), not an abort.
- A fix touches more files than expected → show the diff and get user confirmation before committing.

---

## Resolution log (`wiki/log.md`)
Resolved and aggregated issues leave the live queue and are recorded at the **top** of `wiki/log.md`
(newest first). The live `OPEN-ISSUES.md` stays a queue, not a graveyard. Include the
`OPEN-ISSUES now <N> items, lint green.` line so the log doubles as a size/health trail.

## Security / privacy
Writes only into `wiki/meta/OPEN-ISSUES.md` and `wiki/log.md` — inside the path-safety whitelist.
Deterministic, no network, no secrets in issue bodies. `.raw/` is never touched.
