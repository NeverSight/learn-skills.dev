---
name: timeless-docs
description: "Improve documentation and comment prose so it describes the current state of the code directly and reads clearly in plain language, cutting history, transitions, and trivial detail. Works in two modes: on the current changes (session edits, uncommitted work, or the branch diff) or on named files/folders. Use when the user wants to clean up, tighten, or improve docs or comments — in a file, folder, project, or in what was just changed ('tidy the comments in this diff', 'clean up the docs we just edited', 'fix docs before committing') — make docs clearer / more concise / more readable, remove 'previously / now / no longer / migrated from / instead of' phrasing, make docs timeless, or asks to 'improve docs prose'."
---

# Timeless Docs

Rewrite documentation and code comments so they describe what the system **is**, not how it got there. State the current design directly. Do not reference history, transitions, or absences. Focus on non-trivial information — too much information is already bad information.

Rationale: docs that describe a transition decay the moment the transition is forgotten. A reader who never knew the old state gains nothing from being told about it. State what is; history belongs in git.

This governs code comments as much as prose. The contrast patterns are easy to slip into when a comment explains why a line exists.

## The rules

1. **Describe the current state directly.** No history, no transitions, no absences.
2. **Keep only non-trivial information.** Cut anything that restates the obvious or adds no signal.
3. **Write it to be read.** Plain language, short and to the point — but not so terse it turns cryptic.

## Readability

Docs earn their place by being read. Once a passage states the present tense and carries only non-trivial facts, make it easy to take in:

- **Plain language.** Prefer the common word to the fancy one; keep sentences short and active. Spell out a term of art the first time the reader needs it; drop jargon that adds nothing.
- **Short, not cryptic.** Cut filler, hedging, and throat-clearing — not the context a reader needs to understand the line on its own. A comment no one can parse without reverse-engineering the code has been trimmed too far.
- **Concrete over abstract.** Name the actual thing (`Config/Base.xcconfig`, `/session`), not "the relevant configuration."
- **One idea per sentence.** Split a sentence that carries two.

## Forbidden patterns

Rewrite or remove any of these:

- **Temporal contrast** — "now it is X" / "currently X" when it implies a prior state
- **Change narration** — "changed from X to Y" / "migrated from X" / "no longer X" / "used to X"
- **Prior-state markers** — "previously X" / "formerly X" / "renamed from X"
- **Rejected-alternative contrast** — "rather than X" / "instead of X" / "not Y" when it contrasts with an alternative or discarded approach; state only what the code does
- **Negative inventories** — "no X, no Y, no Z here"; state what is there, not what isn't
- **Old/new labels** — "the old X" / "the new X"

## Rewrite examples

Prose:

```
❌ The config loader was migrated from YAML and now parses config.toml.
✅ The config loader parses config.toml.

❌ Previously this used a global cache; it now uses a per-request cache.
✅ Each request gets its own cache.

❌ This endpoint returns JSON rather than the old XML format.
✅ This endpoint returns JSON.

❌ The new auth flow replaces the deprecated token endpoint.
✅ Auth uses the /session endpoint.

❌ Tenant values live in Swift, not xcconfig — we moved them out of build settings.
✅ Tenant values live in Swift.

❌ No Redis, no Kafka, no external queues — everything runs in-process.
✅ Jobs run in-process via a bounded worker pool.

❌ No checked-in Info.plist. All keys are in xcconfig now.
✅ All Info.plist keys are declared as INFOPLIST_KEY_* in Config/Base.xcconfig.
```

The last pair shows the general move for a negative inventory: replace "what isn't there" with the concrete mechanism that *is* — often more specific and more useful than the line it replaces, not just shorter.

Code comments:

```
❌ // changed to 30s from 10s to avoid flaky timeouts
✅ // 30s: shorter values flake under CI load

❌ // formerly returned nil; now returns an empty array
✅ // returns an empty array when there are no matches

❌ // MainActor isolation is now the default
✅ // MainActor isolation is the default

❌ // use a set instead of a list for dedupe
✅ // set: callers rely on uniqueness

❌ // run the action in a Task rather than driving a .task off state
✅ // run the async action in a Task the button owns
```

## The one distinction that matters

Not every negation is forbidden. Separate a **genuine current property** from a **rejected-alternative contrast**.

- **Keep** a negation that states a real, current constraint the reader needs:
  - "Order is not preserved across batches."
  - "IDs are not unique across shards."
  - "This call is not thread-safe."
- **Cut the contrast** when the negation only points at a discarded approach:
  - "Uses a set instead of a list." → "Stores IDs in a set."
  - "Returns JSON, not XML." → "Returns JSON."

Test: would a reader who never knew the alternative still need this sentence? If yes, keep it (as a plain statement of fact). If it only makes sense against the old/other approach, strip the contrast.

Likewise, **keep the reason, drop the history.** "Changed to 30s because 10s was flaky" carries a real constraint (short timeouts flake) wrapped in a transition. Preserve the constraint, discard the "changed to": "30s tolerates CI load spikes."

## Where history is the content — do not strip

Some documents exist to record change. Leave these alone, or ask before touching them:

- `CHANGELOG.md`, release notes, version history
- Migration guides and upgrade guides
- Architecture Decision Records / decision logs (see the `captains-log` skill)
- Deprecation notices with a removal timeline — these warn about the current and near future, and are still load-bearing

If the user's selected area includes one of these, flag it and confirm before editing rather than flattening its history away.

## Scope: two modes

Every run is either a **changes pass** or a **path pass**. Pick the mode from the request; arguments that are paths mean path mode, and `changes` / `diff` / `session` (or no argument) mean changes mode.

### Changes mode — docs touched by current work

Use when the user points at recent work rather than a place: "the changes", "this diff", "what we just edited", "before I commit", or gives no target while there is work in flight.

Build the file list from these sources, first non-empty wins:

1. **Session edits** — files created or edited earlier in this conversation.
2. **Uncommitted work** — `git status --porcelain`: modified, staged, and untracked files.
3. **Branch diff** — if the tree is clean, `git diff <default-branch>...HEAD --name-only`.

If all three are empty, say so and ask for a path — do not fall back to sweeping the repo.

Within each file, edit only prose the change touched:

- comment/doc lines added or modified in the diff hunks;
- comments adjacent to a changed hunk that the change made stale or history-flavored — a code change is exactly when "now uses X" comments get written, and when old comments start describing a state that no longer exists;
- for doc files in the change set (`README`, `docs/*.md`, …), the changed sections.

Changes mode is a targeted pass, not a file audit. Do not rewrite untouched parts of a changed file; if you notice forbidden patterns outside the change, list them in the report as candidates instead of editing them.

### Path mode — explicit files or folders

Use when the user names files or directories. Work exactly those, recursing into directories: doc files plus comments and docstrings in source files.

- For a whole project ("this project", the repo root), enumerate candidates (`README`, `docs/`, module/header comments, docstrings) and, if the set is large, propose a short plan before mass-editing.
- If a named path does not exist or the target is genuinely ambiguous, ask which files or directory to work on.

## Workflow

### 1. Resolve the scope

Pick the mode and build the file list as described in **Scope: two modes**. State the mode and the file list before editing so the user can redirect early.

### 2. Screen for carve-outs

Identify any files where history is the point (see the section above). Set them aside and confirm with the user before editing them.

### 3. Scan for the forbidden patterns

Read each target and collect candidate edits. Search hints for the mechanical cases:

```sh
# path mode — scan the named files/folders
grep -rniE "no longer|used to|previously|formerly|renamed from|migrated from|instead of|rather than|the old |the new |now (uses|returns|is|it)" <path>

# changes mode — scan only added lines in the diff
git diff -U0 HEAD | grep -iE "^\+.*(no longer|used to|previously|formerly|renamed from|migrated from|instead of|rather than|the old |the new |now (uses|returns|is|it))"
```

Grep only surfaces obvious cases — the temporal-contrast and negative-inventory patterns often need a human read. Do not rely on grep alone. In changes mode, also read the hunks in context: an unchanged comment above changed code may now describe behavior that no longer exists.

### 4. Rewrite to present state

For each candidate:

- Restate the current behavior directly, preserving every non-trivial fact — constraints, contracts, invariants, gotchas, and the genuine *why* behind a choice.
- If a sentence's only content is the transition and there is no current-state fact to keep, delete it.
- Match the surrounding voice, tense, and formatting. Make minimal edits — do not rewrite passages that are already timeless and clear.

### 5. Concision and readability pass

Remove statements that restate what the code plainly does, ceremonial comments, and redundant sentences. Keep the signal: anything a competent reader could not infer at a glance. Then apply the Readability rules — plain words, short active sentences, concrete nouns, one idea per sentence — without trimming so far that the line becomes cryptic.

### 6. Verify

- No non-trivial information was lost.
- Every claim still matches the code.
- The prose reads naturally and stands on its own without knowledge of any prior state.
- No forbidden pattern remains.

## Guardrails

- Preserve meaning first. Never drop a genuine constraint, reason, or warning just because it is phrased as a negation or a comparison — rephrase it as a plain present-state statement.
- Do not invent current-state facts you cannot verify from the code. If a doc's claim looks stale, flag it instead of guessing.
- When unsure whether a line is a genuine property or a rejected-alternative contrast, keep it and note it for the user rather than deleting.
- Keep edits tight and reviewable; do not reflow or restructure whole files under the banner of prose cleanup.

## Output

Report the mode and what changed, grouped by file:

- file and location
- pattern (temporal contrast, change narration, negative inventory, trivial detail, …)
- before → after, or the deleted text and why it carried no current-state signal

List separately, as items needing the user's decision:

- carve-out files and ambiguous negations that were left untouched
- in changes mode, forbidden patterns spotted outside the changed prose (candidates for a follow-up path-mode pass)
