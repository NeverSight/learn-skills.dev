---
name: verify-with-controls
description: Use when about to report a zero or absent reading, an alarming finding, a success claim, or stillness from a probe or status read, so the reading is evidence-bearing and controlled first.
license: SEE LICENSE IN LICENSE.md
metadata:
  author: Vivswan
---

# Verify With Controls

> A reading is not a finding. Before "no matches" (a zero), "half the checks vanished" (an alarm), "the work landed" (a success claim), or "nothing is running" (stillness) becomes a claim, the reading must survive its controls. Those are evidence attached, a positive control behind every zero, the instrument suspected, the postcondition checked, a re-measure at the moment of sending, and a checker that has been seen failing.

Six rules, each distilled from a false conclusion nearly shipped in production:

| # | Rule | The failure it kills |
| --- | --- | --- |
| 1 | Evidence or error, never a bare zero | one 0 for both "absent" and "I failed to look" |
| 2 | Positive control before trusting a zero | a blind instrument answering the wrong question truthfully |
| 3 | Suspect the instrument first | a plausible number measuring the wrong thing |
| 4 | The postcondition is the truth | success logs over a state that never changed |
| 5 | Two observations to look, re-measure to send | a report racing the state it describes |
| 6 | Negative control for checkers | a gate that cannot go red |

## 1. Evidence or error, never a bare zero

A probe that can return 0 both for "absent" and for "I failed to look" is broken by construction. No amount of care in reading its output fixes it. The two meanings arrive as the same byte.

```bash
$ git diff --numstat origin/main...HEAD -- src/fetaure/
$        # empty, exit 0: reads as "this branch touched nothing there"
```

One transposed letter, and the pathspec matches nothing that ever existed. "No changes under the path" and "I probed the wrong place" arrive as the same empty, successful reading. A run of zeros with this shape nearly reported real, landed work as missing.

A sound probe proves the question was answerable before trusting the zero, and errors on a reading it could not take. Validate the pathspec against the same endpoints the measurement reads. Three traps hide in that sentence:

- a three-dot diff compares the MERGE BASE with HEAD, not the two named tips
- a failed validation exiting 0 is just another bare zero
- a pipe returns only its last command's status, so `pipefail` keeps a failed `ls-tree` from hiding behind the other endpoint's match

```bash
$ set -o pipefail
$ base=$(git merge-base origin/main HEAD) &&
    { git ls-tree -r --name-only "$base" -- src/fetaure/ &&
      git ls-tree -r --name-only HEAD -- src/fetaure/; } | grep . ||
    { echo "ERROR: no trustworthy reading (instrument error above, or pathspec at neither endpoint)" >&2; exit 1; }
ERROR: no trustworthy reading (instrument error above, or pathspec at neither endpoint)    # and exit 1
```

The broken zero becomes a loud, non-zero error. On a pathspec present at either endpoint (including one the branch deleted entirely) the same probe prints the matched paths and exits 0, so a pass carries its evidence too, and only then is an empty diff a reading. Non-zero readings report their matched lines the same way, never the count alone.

Corollary: every narrowed variant of a working probe is a NEW probe. Prove the narrowed form returns non-empty on a case that must match before trusting its empty. Worked example: a stash was probed for work under one path by narrowing a command that had just worked:

```bash
$ git stash show --numstat 'stash@{0}'                          # works: prints the stash's files
$ files=$(git stash show --numstat 'stash@{0}' -- docs/ 2>/dev/null)
$ echo "${files:-nothing under docs/}"
nothing under docs/
```

The stash DID hold work under `docs/`. `git stash show` takes no pathspec, so the narrowed command measures nothing. Its complaint went to the discarded stderr, and the captured stdout was empty either way.

The control that exposes it: run the narrowed form on a path the stash MUST contain, and watch it read empty there too, before its empty means anything.

## 2. Positive control: one reading that must be non-zero

Before trusting any zero or absent reading, take one reading that MUST be non-zero through the same instrument. An empty world and a blind instrument produce the same zero. Only the control separates them.

A landing checker with the wrong repository root hardcoded reported two landed files as DROPPED. Every reading it took was internally consistent, a truthful answer to the wrong question: the tree it probed could never contain the files.

```bash
$ landed-check docs/new-guide.md   # 0 - alarming reading, do not report yet
$ landed-check README.md           # control: known present, must read non-zero
0                                  # it reads zero -> the instrument is blind
```

One extra command turns "the files are gone" into "my checker cannot see", before the alarm ships.

## 3. Could my instrument be the broken part?

Before reporting an alarming reading, re-derive it a second way. An instrument defect produces a confident, plausible, wrong number, and nothing about a plausible number looks broken.

```bash
$ gh pr checks 123 | tr -s ' ' '\t' | awk -F'\t' '{print $2}' | grep -c pass
10        # of 14 known checks - four "missing"?
```

Check names containing spaces split into extra fields, so field two was not the status column on every row: 10 of 14 is a plausible number measuring the wrong thing. The second derivation skips the parse entirely and disagrees:

```bash
$ gh pr checks 123 --json state --jq 'map(.state) | group_by(.) | map({(.[0]): length})'
[{"SUCCESS":14}]
```

When two derivations disagree, suspect the instruments before the world, and keep the reading out of any report until they agree.

## 4. Logs approximate; the postcondition is the truth

Exit codes catch hard failures. Output verdicts catch soft aborts, where a tool prints its own failure and exits 0. Neither substitutes for verifying the state you needed.

Two production shapes:

```text
$ sync-tool push
  ERROR: Push failed (remote rejected)
Sync finished successfully.
$ echo $?
0         # the tool's verdict line and its exit code both read success
```

```text
$ merge-queue add 456
queued OK       # success means ENQUEUED; the commits are not on the mainline yet
```

Both messages are honest about the wrong thing. The claim you need is about the world, so check the world:

```bash
$ git fetch origin main && git merge-base --is-ancestor "$sha" FETCH_HEAD && echo landed
```

Is the ref actually where it must be? That is the postcondition. The log only ever approximates it.

Test `FETCH_HEAD`, the ref the fetch just wrote. Whether `origin/main` itself updates depends on the remote's configured fetch mapping, and a stale remote-tracking ref approximates the same way a log does.

Ancestry is conclusive only when the landing preserves commit ids. Squash, rebase, and cherry-pick landings all rewrite `$sha`, so there a failed ancestry check proves nothing by itself.

For those, the postcondition is the content itself at `FETCH_HEAD`: the changed files' exact content present at the fetched tip. A subject match is used at most to locate the landing, never as the check, since a squash can rewrite the subject too.

## 5. Two observations before a flag, re-measure before sending

State changes race your report. Two bars with different jobs:

- Two observations across an interval decide whether to LOOK: a single still reading is not stillness.
- A fresh re-measure immediately before sending decides whether to SEND. Every near-false-alarm in production died at that final re-measure, never at the first reading.

```text
reading 1                  no change      -> keep watching, not a flag yet
reading 2                  still no change -> the flag is earned on this evidence
re-measure before sending  changed 37 seconds ago -> withhold; the claim went stale
```

A flag that met the bar on genuine evidence can still be wrong by the time it sends. A conclusion is bound to the moment it was measured, and sending it asserts it NOW, so measure it now.

The same applies to retracting one: a retraction is a claim about current state too.

## 6. Negative control: prove the checker can fail

A gate that cannot go red verifies nothing, and a checker that has never been seen failing proves nothing when it passes. Feed it a sentinel that MUST fail, through the same assertion path the real checks use. A separate test-the-test path controls the wrong instrument.

```ts
// The real checks and the control share assertContains, so the control
// certifies the exact code path every green check ran through.
test("negative control: the shared assertion fails on an impossible token", () => {
  expect(() => assertContains(doc, "zzImpossibleToken414")).toThrow();
});
```

For a checker that verifies a landing or a deployment, run it against a state that must fail (the pre-landing ref, a tree without the files) and watch it go red there before trusting its green.

## At the moment of concluding

The rules compress into one pass, run right before the conclusion leaves your hands:

1. Zero or absent reading: is the probe evidence-or-error (1), and did a positive control pass through the same instrument (2)?
2. Alarming reading: re-derived a second, independent way (3)?
3. "It succeeded": checked the postcondition, or only a log that approximates it (4)?
4. Stillness or absence over time: two observations, then a re-measure immediately before sending (5)?
5. A green checker: has it ever been seen red (6)?

## Review Criteria

Skills that run code reviews (such as `/rubber-duck-review`) expand this section into their reviewer prompt when this skill is installed. Ask the reviewer to flag:

- probes or checks that can return the same value for "absent" and for "failed to look": swallowed errors, unvalidated paths, a grep or filter whose zero is trusted bare
- checkers and gates with no negative control: nothing proves they can fail through the same assertion path their green runs through
- success concluded from a log line or exit code where the postcondition itself is checkable

Triage the resulting findings with the pass in "At the moment of concluding" above.
