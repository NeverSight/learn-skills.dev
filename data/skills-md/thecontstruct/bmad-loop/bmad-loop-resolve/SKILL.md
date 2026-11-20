---
name: bmad-loop-resolve
description: 'Interactive escalation-resolution workflow for the bmad-loop orchestrator. A bmad-loop run paused on a CRITICAL escalation (a contradiction or gap a dev/review session could not safely resolve alone); you and the human disambiguate the frozen spec so the story can be re-driven. Invoked as /bmad-loop-resolve <story-key>. Unlike the automated dev/review sessions this session is interactive — a human is present and you SHOULD ask.'
---

# bmad-loop Escalation Resolution

A `bmad-loop` run drove a story through dev → review, a session raised a
**CRITICAL escalation** (work could not proceed safely — usually a contradiction
or an unanswered question in the _frozen spec_), and the orchestrator paused the
whole run for a human. The session that escalated is gone; you are a fresh
interactive session whose job is to **resolve the ambiguity with the human and
update the frozen spec**, so the orchestrator can re-arm the story and re-drive
it against a corrected spec.

This is **interactive**: a human IS present. Ask questions, present options,
recommend — but the human makes the call. (`$BMAD_LOOP_MODE` is intentionally
unset for this session; the never-ask automation rules do NOT apply.)

## Identity & I/O contract

These environment variables are set:

- `$BMAD_LOOP_RUN_DIR` — the paused run's directory.
- `$BMAD_LOOP_STORY_KEY` — the escalated story key (also your invocation argument).
- `$BMAD_LOOP_RESOLVE_CONTEXT` — path to a `context.json` written for you.

**Read `$BMAD_LOOP_RESOLVE_CONTEXT` FIRST.** Its schema:

```json
{
  "story_key": "6-4-cli-list-command",
  "run_id": "20260613-111429-6a14",
  "project_root": "/abs/path/to/bmad-project",
  "code_root": "/abs/path/to/code-repository",
  "spec_file": "/abs/path/to/_bmad-output/implementation-artifacts/spec-<story>.md",
  "spec_reaches_the_redrive": true,
  "redrive_base_ref": "<branch the re-drive reads, or HEAD>",
  "baseline_commit": "<sha>",
  "paused_reason": "CRITICAL escalation from review session: ...",
  "env_fault_site": null,
  "escalations": [
    {
      "type": "<kind>",
      "severity": "CRITICAL",
      "detail": "<what's ambiguous/contradictory>"
    }
  ],
  "resolution_path": "/abs/path/to/<run>/resolve/<story>/resolution.json"
}
```

The `escalations` array is ordered newest-first.
Across the entire gathered context, each distinct escalation appears exactly once.

The interactive session's working directory is always `project_root`. That tree holds
the BMAD artifacts and specs you inspect or clarify. `code_root` is the tree where the
run's code and git work belong; it may be different. When the roots differ, do not
mistake the session cwd for the code checkout: any code fix or commit the human must
make belongs under `code_root`, while artifact and spec work remains anchored under
`project_root` (or at the explicit absolute paths in this context). You still do not
implement or commit during this resolution session; name the correct tree when guiding
the human.

**`spec_reaches_the_redrive` says whether your edit has a future.** The re-drive
reads one tree; `spec_file` may name another. Under worktree isolation the run's mount
is discarded before the re-drive reads anything, so a spec inside that mount is
destroyed with it. When this field is `false`, every write to `spec_file` still
SUCCEEDS and is then thrown away — worse than not editing at all, because the session
looks resolved. `null` means there is no ordinary frozen spec to edit: either the task
has no spec on record, or stories mode recorded a sentinel path instead. In both cases
step 4 does not apply; follow the sentinel guidance below when that block is present.

**`redrive_base_ref` tells you which of the two remedies applies.** Read it before you
tell the human anything: a branch name and `HEAD` mean opposite things.

Do not skip the edit when it is `false` — the corrected spec is what gets carried
over, and it is the clearest statement of what you and the human agreed. Do step 4 as
usual, then tell the human, in the same breath as the resolution, **where the
correction has to land to be read** — which the field decides: when `redrive_base_ref`
names a branch, committed on `redrive_base_ref`; when it is `HEAD`, re-applied in the
main checkout, uncommitted. The two paragraphs below carry each arm.

Be precise about this, because the two obvious moves both fail silently:

- Committing from the **main checkout** cannot include the file you edited — it lives
  in a linked unit worktree, which is a separate working tree.
- Committing on the **unit's own branch** does not reach the re-drive either. The
  replacement worktree is cut fresh from `redrive_base_ref`, not from the branch of
  the mount that was discarded.

So the correction has to reach `redrive_base_ref` itself: make the same edit to that
tree's copy of the spec and commit it there. The orchestrator names the same ref when
it re-arms; say it here so they hear it before they close the session rather than
after.

**When `redrive_base_ref` is `HEAD`, do not tell them to commit anything.** That means
the re-drive runs in the **main checkout** and reads its WORKING TREE, so an edit there
is read as-is. `spec_reaches_the_redrive: false` beside a `HEAD` base is the opposite
problem from the one above: `spec_file` points into a worktree this run has STOPPED
using, because its isolation policy changed while the story sat escalated. The remedy
is to make the same edit to the main checkout's copy of the spec — no commit, no
branch. Telling them to commit here sends them to a tree the re-drive does not read,
which is the same lost work in the other direction.

In **stories mode** (folder+id dispatch) the context also carries a `stories`
block — the manifest intent for this story, so you can see WHAT it is meant to do
without hunting for it:

```json
{
  "stories": {
    "spec_folder": "_bmad-output/epic-1",
    "story": {
      "id": "6-4-cli-list-command",
      "title": "CLI list command",
      "description": "…",
      "spec_checkpoint": false,
      "done_checkpoint": false,
      "invoke_dev_with": "…free-text planner→dev note, or ''…"
    },
    "sentinel": {
      "kind": "unresolved",
      "path": ".../stories/6-4-cli-list-command-unresolved.md",
      "blocking_condition": "…the reason planning halted…"
    }
  }
}
```

The `sentinel` sub-block is present ONLY when the escalated story is a **sentinel**
(see the stories-mode section below); an ordinary escalation omits it.

In **tickets mode** (a BMAD v7 initiative ticket tree) `spec_file` is the ticket's
**plan**, and the context also carries a `tickets` block — the ticket and its plan
as they read now:

```json
{
  "tickets": {
    "ref": "1.2",
    "ticket_id": "2",
    "title": "List command",
    "epic": "epic-cli",
    "plan": "/abs/path/to/<initiative>/tickets/epic-cli/tickets/story-list-command-plan.md",
    "plan_status": "blocked",
    "blocked_reason": "intent gap",
    "auto_run_result": "…excerpt of the plan's `## Auto Run Result`…"
  }
}
```

`plan_status`, `blocked_reason` and `auto_run_result` are `null` when the plan has
no such value, is absent, or could not be read; `plan_status` and `blocked_reason`
are `null` too when the plan's frontmatter is missing or malformed (the orchestrator
journals an unreadable plan and a malformed frontmatter). The plan's `blocked_reason` is the condition build-auto halted on;
the orchestrator clears it when it re-arms the ticket.

Your **output marker** is the file at `resolution_path`. Writing it is the LAST
action of a successful resolution. Schema:

```json
{
  "story_key": "<key>",
  "decision": "<one or two sentences: the rule you and the human chose>",
  "spec_file": "<the spec you edited>",
  "spec_updated": true,
  "restore_patch": "<optional: path to a saved intent-gap patch to re-apply>"
}
```

`restore_patch` is **optional** and used only for the intent-gap patch-restore
case below — omit it entirely for an ordinary resolution.

## What you MUST do

1. **Read the context**, then read the **frozen spec** at `spec_file` in full —
   especially its `<intent-contract>` block (a v7 ticket plan;
   `<frozen-after-approval>` in an older spec) — the intent the dev/review
   sessions treat as authoritative. The escalation is almost always that this
   block is silent on, or contradicts, a case the implementation hit.
2. **Present the current pause evidence plainly** to the human:
   - When the `escalations` array is non-empty, present its recorded entries in
     their existing newest-first order. Do not replace recorded escalation
     detail with `paused_reason`.
   - When the `escalations` array is empty, first require `paused_reason` to be
     text containing at least one non-whitespace character. If it is missing,
     `null`, non-text, or blank after trimming, report a malformed resolve
     context and do not write the resolution marker. Otherwise, present
     `paused_reason` verbatim as the available evidence for the current pause
     and disclose that no newer recorded escalation detail is available. Do not
     read below the watermark, unfilter or recover an older artifact escalation,
     or synthesize an escalation object from `paused_reason`.

   Using the selected evidence, explain what is ambiguous or contradictory, why
   it blocks safe implementation, and offer **2–4 concrete resolution options**
   with a clear recommendation and its trade-offs. Keep it tight — quote the
   relevant spec lines.

3. **Get the human's decision.** Ask follow-ups if the choice is unclear. Do not
   invent requirements; if the human is unsure, help them reason, don't guess.
4. **Update the frozen spec** to encode the decision unambiguously: amend its
   `<intent-contract>` block (v7 plan; `<frozen-after-approval>` in an older
   spec) and any affected acceptance criteria / test
   matrix rows so a fresh dev session has exactly one correct reading. Make the
   smallest change that removes the ambiguity. If a larger change is warranted: in
   sprint or stories mode you MAY use the `bmad-spec` or `bmad-correct-course`
   skills (BMAD v6); in tickets mode use `bmad-agent-po` to refine or replan the
   ticket. **If
   `spec_reaches_the_redrive` is `false`, make the same edit and then say plainly
   that this copy is not the one the re-drive reads, and name the remedy that
   `redrive_base_ref` selects: on a branch, the correction must be
   committed on `redrive_base_ref`; on `HEAD`, it must be re-applied in the main
   checkout, uncommitted** — an unflagged edit here is lost work, and a commit in the
   wrong tree or on the wrong branch is lost work that looks done.
5. **Write the resolution marker** at `resolution_path` (schema above), then tell
   the human the resolution is recorded and they can exit this session — the
   orchestrator will offer to **re-arm the story and resume the run** (a clean
   rebuild against the corrected spec).

## Special case: a review-stage `intent gap` with a saved patch

When the escalation came from the **review step** halting on an `intent gap`, the
dev session first **saved its attempted change as a patch file** (in the
implementation-artifacts folder) before reverting the tree — the escalation
`detail` and the spec's `## Review Triage Log` reference the patch path. That
patch is concrete evidence: it shows exactly which reading of the intent the run
implemented. In tickets mode the patch sits **beside the plan**, named after it
with `.patch` for `.md`; name that path for `restore_patch`. The orchestrator moves
it out of the tree into the run directory when it re-arms the ticket (it would
otherwise fail the re-drive's clean-tree check) and latches the moved copy.

**First check `restore_supported` in the context file.** When it is `false`
(worktree-isolation runs: the re-drive discards and re-mounts the unit's
worktree, so an in-place restore can never land; an escalation with no recorded
spec: a restored patch has no review to resume; a pre-planning sentinel wedge:
there is no attempted implementation to restore), **never offer the restore
option and never record `restore_patch`** — the orchestrator would reject the
resolution and this whole session's negotiation would be wasted. The patch is
still available as evidence.

Use the patch two ways:

- **As evidence.** Read the patch (and the diff it represents) to see what the
  guessed reading produced — often clearer input for writing the clarification
  than the questions alone.
- **When the attempted reading was actually correct.** Sometimes the run's guess
  is the right one and only the _intent_ was silent. Present this as an explicit
  option to the human: _"the implementation read it as X, which is in fact what we
  want — amend the intent to say X, and resume **review** on the already-written
  change instead of re-implementing it."_ If the human chooses this:
  1. Still **amend the intent** in the spec so it unambiguously says X (step 4
     above is unchanged — the frozen intent must match the restored code).
  2. Add **`"restore_patch": "<the saved patch path>"`** to `resolution.json`
     (copy the path verbatim from the escalation detail / triage log).

  The orchestrator then re-arms the spec to `in-review`, re-applies the patch onto
  the baseline, and re-dispatches — the session resumes at the review step on the
  restored diff. **Do NOT `git apply` the patch yourself and do NOT set the spec
  status** — the orchestrator does both deterministically at re-arm.

  **The restore must not overlap resolution commits.** Re-arm advances the
  re-drive's baseline to the branch's post-resolve HEAD, but the saved patch was
  diffed from the ORIGINAL baseline — so if this session left commits that touch
  the patch's own files, the restore's `git apply` fails and the story
  re-escalates (loudly, by design: the orchestrator never silently merges the
  resolution with the stale attempt). If the resolution work already includes or
  supersedes the attempted change, **omit `restore_patch`** — the commits survive
  re-arm as the re-drive's starting point, so a from-scratch re-drive builds
  directly on them.

If the attempted reading was wrong (the common case), omit `restore_patch`
entirely: the orchestrator re-drives from scratch against the corrected intent.

## Special case: an environment-fault escalation

When `env_fault_site` in the context is **not** `null`, the run paused because the
**environment** failed, not the story: an operator `[environment]` probe failed (or
a verify command declared or hit an environment fault) at the site it names —
`verify:<role>`, `probe:decision:<role>`, `probe:claim:<role>` or
`probe:dispatch:<role>`. The attempt was **not** charged.

A `probe:claim:<role>` site means the dev, fix, review or workflow session wrote an
`Environment fault: <what is broken>` line in its final `## Auto Run Result` and
the orchestrator's own probe then failed. The line only triggered that probe — a
claim the probes did not confirm never pauses the run, so the failed probe, not
the session's prose, is the evidence. `paused_reason` quotes the claim on its
`session claim:` line.

- **No spec change is needed.** Do not clarify the intent or reinterpret the
  story to explain the failure; `paused_reason` names the probe or command that
  failed and its output tail.
- Tell the human to **fix the environment** (start the stopped service, container,
  emulator or database the probe checks) and confirm the probe passes by hand.
- Then **re-arm the escalation** as usual (record a resolution that says the
  environment was repaired); the attempt budget resets on re-arm. A plain re-arm
  re-drives a dev session from the baseline. When the attempt's work should be
  kept, the human can instead exit this session and run
  `bmad-loop resolve <run> --reverify`: it keeps the tree at HEAD (in place, or
  the story's kept worktree unit), replays verification on it and, when that
  passes, reviews and commits it (a unit merges) with no dev session. A
  `probe:dispatch:<role>` pause is not an escalation at all — no session ran, so
  the human fixes the environment and runs `bmad-loop resume <run>` (the probes
  re-run first); `resolve` refuses that pause.

## What you MUST NOT do

- **Do NOT** write the orchestrator's `result.json` — that is a dev/review
  artifact; this is not one of those sessions.
- **Do NOT** change `sprint-status.yaml`, and **do NOT** set the spec's `status:`
  field — the orchestrator deterministically re-arms the spec status on resume.
  Edit spec **content** only. In tickets mode, **never run `tickets.py mark`** and
  never set the plan's `status`, `blocked_at` or `blocked_reason` — the
  orchestrator re-arms the ticket through its own `mark` and clears them.
- **Do NOT** implement the story, write feature code, run tests, or commit. Your
  job ends at a corrected spec + the resolution marker. That holds when
  `spec_reaches_the_redrive` is `false` too: landing the corrected spec where the
  re-drive reads it is the HUMAN's step — committing it on `redrive_base_ref` when that
  names a branch, re-applying it in the main checkout when it is `HEAD`. Tell them it
  is required, and which one; do not do it yourself.
- **Do NOT** widen scope. Resolve exactly the escalated ambiguity; if you notice
  unrelated problems, note them to the human but leave them alone.

## Stories mode: sentinels and the preserved copy

In stories mode a story that could not even be **planned** — the dev session hit
a contradiction or gap before it could write a real spec — leaves a fixed-slug
**sentinel** file instead of a frozen spec: `<id>-unresolved.md` (the intent was
too ambiguous to plan) or `<id>-ambiguous.md` (more than one story spec matched
the id). The context's `stories.sentinel` block names it and carries the
`blocking_condition` the session recorded.

A sentinel is **not a spec you edit** — there is no plan or `<frozen-after-approval>`
block inside it. So for a sentinel:

- **Do not try to amend a frozen spec** (step 4's "edit the frozen spec" does not
  apply — there isn't one). Instead resolve the _upstream_ ambiguity so a fresh
  planning pass can succeed: usually that means clarifying `SPEC.md` (the epic
  spec) or this story's entry in `stories.yaml` — the `title` / `description` /
  `invoke_dev_with` the planner reads — with the human.
- **`redrive_base_ref` decides where that upstream edit has to land, exactly as it
  does for a spec.** `spec_reaches_the_redrive` does not answer this — it is about
  `spec_file`, which for a sentinel is the file being deleted. The artifacts you
  actually edit are `SPEC.md` / `stories.yaml`, and they face the same question: when
  `redrive_base_ref` names a **branch**, the re-drive mounts a fresh worktree and
  re-plans from that branch's COMMITTED tree, so an uncommitted edit is invisible and
  the re-plan mints the same sentinel again — tell the human it has to be committed
  there. When it is `HEAD`, the re-drive re-plans in the main checkout's working tree
  and the edit is read as-is — do not tell them to commit. The orchestrator re-arms on
  the same rule and will hold the resume until the branch carries it.
- On **re-arm** the orchestrator does NOT flip the sentinel to `ready-for-dev`
  (there is no plan to route to). It **preserves a copy** of the sentinel under
  `{run}/sentinels/<id>-<kind>.md` as a breadcrumb, **deletes** the sentinel, and
  the next dispatch re-plans the story from scratch (leg 1 again for a
  `spec_checkpoint` story). You do not touch the sentinel file yourself.
- Write the resolution marker as usual once the human has decided how to
  disambiguate; set `spec_file` to whatever you edited (e.g. `SPEC.md`), or omit
  it if the fix was entirely in `stories.yaml`.

### Not a sentinel: more than one file matches the id

Distinct from the single-file `<id>-ambiguous.md` sentinel above: when **more
than one** file in `stories/` matches `<id>-*.md` (say `3-login.md` AND
`3-signup.md`), the id itself is ambiguous _on disk_ and the orchestrator wedges
the story without picking either file. You can recognize this state by the
escalation reason (`ambiguous story file match: <names>`) and by what the
context does NOT have: no `stories.sentinel` block and no single spec path.

The auto-clear above does **not** apply — there is no sentinel to preserve and
delete, and re-arming alone just re-wedges on the same duplicates. The
resolution IS the cleanup: with the human, decide which file is the story's real
spec and remove or rename the other (merge content first if both carry real
work; renaming must move it out of the `<id>-*` pattern or to another id).
Exactly one match re-dispatches that spec; zero matches re-plans from scratch.
Then write the resolution marker as usual — re-arm + resume takes it from there.

## If you cannot resolve it

If the human defers, the information needed is genuinely unavailable, or the
right fix is out of scope for a spec edit (e.g. it needs a PRD/architecture
change), say so plainly and **do not** write the resolution marker. Exiting
without the marker leaves the story escalated and the run paused — the safe
default. The orchestrator will not re-arm a story with no recorded resolution.
