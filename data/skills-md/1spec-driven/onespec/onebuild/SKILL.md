---
name: onebuild
description: Execute a planned build's patches in order — implement, verify, run pre-commit checks, commit each patch as exactly one atomic commit.
---

# Build Execute

Input: a planned build with ordered atomic patches (see `oneplan`). For each patch, in sequence:

Approval: if the build record still reads `Status: planned, awaiting author checkpoint`, this invocation is the author's approval. Set `Status: planned, approved <date>` before the first patch; it lands with that patch's checkbox.

1. **Implement** the patch. Stay within its planned scope.
2. **Verify** the patch demonstrates its planned change: where test-coverable, its test fails before the patch and passes after. The full test suite must be green — the project must be clean for a patch to commit. Green is necessary but not sufficient: if the patch claims a live or external effect (a provider calls us, a platform capability enabled, a credential provisioned), verify by observing that real effect — a synthetic stand-in proves the handler, not the claim. This holds equally when the patch depends on anything the repository does not control, for example another tool's logs or an API's responses: verify against the real thing in this patch, and build fixtures from captured real samples. Judge against the planned claim, not a narrowed post-hoc claim. If the real effect cannot be observed as true (never attempted, inconclusive, or denied), stop before commit — missing proof is a block, not a skip.
3. **Pre-commit checks**:
   - Confirm the worktree contains only the intended patch scope.
   - Every changed line traces to the patch's stated invariant or to machinery that invariant requires (imports, type plumbing, test setup). A line that traces to neither belongs to another patch: move it out, or report it to the author before committing.
   - Stop for blocking problems or unspecified UI/interaction surfaced by a dependency.
   - A live/external step that comes back denied, unavailable, or not-authorized — or whose claimed effect cannot be observed — is a blocker even with a green suite. Report it to the author verbatim and stop: do not commit this patch, do not start later patches — that report is the deliverable. Don't route around it: no silent continue, no "pending"/"skipped" status, no marking the patch done, no synthetic proof. Blocked ≠ done; the author decides next.
   - For user-facing work: check against mature desktop software quality, treat library defaults as implementation details, verify new limits at the limit, map tests across affected workflows and failure paths, and document non-default product choices in the change spec.
4. **Update status**  mark the current patch checkbox `[x]` in the build plan. Leave it unchecked if blocked.
5. **Commit** in one atomic step with message `<tag><build>.<patch>: <details>` (e.g. `LC1.2: …`).

Never batch multiple patches into one commit, and never let a patch span commits.

## Change spec record

A change spec is arranged in this order, and a new section goes where it belongs, not at the end:

1. Goal and design — what the change is and how it works.
2. Facts — what was verified, with dates.
3. `Builds` — one record per build, in order: executed builds, then the one planned build.
4. `Backlog` — always last.

An implementation line (for example, `--- Implemented / Next ---`) splits current state from planned deltas:

1. Text above the line is historical and may be inconsistent with later changes. This doesn't need fixing: the later version, and ultimately, code, wins.
2. Below the line, milestones are delta-only; they do not restate full behavior.

When reviewing a change spec:

1. Keep one canonical statement per behavior/default; later sections should reference it.
2. If duplicated rules disagree, flag drift; for current-state checks, code wins.

### Builds and numbers

The spec grows one build at a time. A build is numbered `<TAG><n>` when it is planned, never earlier, so only executed builds and the one planned build carry numbers. The backlog is a flat, unordered list of one-line items. Backlog items carry no build numbers. They have no acceptance checks, patches or ordering; anything beyond a one-line item is planned only when it becomes the next build. Outside a planning turn, add open questions and backlog items, never draft future builds.

Each build record begins with a `Status:` line:

- `Status: planned, awaiting author checkpoint`
- `Status: planned, approved <date>` — the author approved the plan at the checkpoint, by saying so or by invoking `onebuild` on it; the first patch lands it
- `Status: executed, pending author verification` — every patch is committed, but acceptance has a clause only the author can discharge
- `Status: implemented <date> (commits <TAG><n>.*)`

A patch is one coherent, verified change; inside a build it lands as exactly one commit named `<TAG><n>.<k>`, the same string as its commit subject. Patch numbers restart at 1 for each build.

A finished change spec is a record of what was built, not a plan: plan from this layout, never from a finished spec. Retiring a change spec keeps its `Status:` lines.


## Closing the build

These steps complete the build. Patches committed with this section unfinished
is a build not delivered.

6. **Run acceptance once on the final tree.** A gate that ran while verifying a
   patch is not this run: acceptance is one run over the committed head with
   provenance pinned (tree sha, script sha, environment, host). Run it even when
   every clause is covered by a gate — an empty per-build delta means the checks
   live in the gate, not that the run is redundant.
7. **Record the result in the change spec**: command, verdict, provenance,
   per-check outcome. The raw log or JSON goes to a shared location, not the
   repo; the record goes in the spec. Acceptance inherits the live/external
   rule — green alone does not pass a live claim.
8. **Name every live clause still open**, and what remains to observe it. A
   build whose live clause is unobserved is reported open, not complete.
9. **Hand off author-only clauses.** An acceptance clause only the author can
   discharge is handed back, never skipped or marked passed: list the build's
   "Author action required at completion" items, set the build's status to
   `executed, pending author verification`, and end with that stated hand-off.
   This is distinct from done and from blocked, where a patch could not be
   completed.

Fix acceptance failures and re-verify until it passes, keeping all fixes
**uncommitted** — report the fix diff with its verification. Commit nothing
beyond the planned patches; acceptance fixes are committed only at the
`oneplan` checkpoint on author approval.

