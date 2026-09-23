---
name: claim-audit
description: A linter for AI answers that separates grounded, hedged, and bare factual claims — surfacing the unverified hard assertions most likely to be hallucinations. Use as a self-check gate before an agent ships a reply, or in CI over saved transcripts.
when_to_use: You want an agent to "show its work" before answering, or to flag which statements in a draft reply are hard factual assertions with no evidence and no hedge (the hallucination-prone ones). NOT a fact-checker — it finds claims to verify, it doesn't verify them.
version: 1.0.0
license: MIT
metadata:
  agentskills:
    tags: [hallucination, verification, reasoning, self-check, ci]
---

# Claim Audit

Make an answer show its work — or flag exactly where it didn't.

## Overview

A model is far likelier to be wrong on a **hard factual claim it asserted with no
evidence and no hedge** than on one it cited or qualified. `claim_audit.py` reads
an agent's answer and sorts every sentence into:

- **✓ grounded** — carries a citation, URL, quote, or source marker
- **~ hedged** — explicitly uncertain ("likely", "roughly", "I'm not sure")
- **⚠ bare** — a hard assertion (is/was/founded/numbers/dates) with neither → **verify this**
- **· opinion/meta** — recommendation or instruction, not a world-fact

It's a linter, not a fact-checker: it can't tell you a grounded claim is *true*,
but it reliably surfaces the bare assertions worth checking — the ones that
hallucinate. It reports a **BARE risk ratio** and can fail CI when that ratio is
too high.

Proven on a mixed answer: it flagged "The capital of Australia is Sydney" (false)
and "founded in 1788" as ⚠ bare, passed a `[1]`-cited census figure as ✓ grounded,
and let a hedged population estimate through as ~ — exactly the triage you want.

## When to use

- A pre-ship self-check: an agent audits its own draft, then goes and grounds or
  hedges the ⚠ claims before sending.
- CI over a transcript corpus: fail when >X% of checkable claims are bare.
- Reviewing an LLM feature's outputs for where it asserts without support.

Not for: verifying truth (it finds claims *to* verify), or auditing opinions/plans.

## The method

1. **Capture the answer** to a file or pipe it in.
2. **Audit it.**
   ```bash
   echo "$ANSWER" | python scripts/claim_audit.py -
   # or:  python scripts/claim_audit.py draft.txt --json
   ```
3. **Read the ⚠ bare list.** These are hard assertions with no evidence. For each,
   do one of three things: cite a source, hedge it honestly, or drop it.
4. **Gate it.** In an agent's reply pipeline or CI:
   ```bash
   python scripts/claim_audit.py draft.txt --fail-over 0.4   # exit!=0 if >40% bare
   ```
   Now an answer that's mostly unsupported assertions gets caught before it ships.
5. **Re-audit after grounding.** Watch the bare count drop to zero (or intentional,
   justified hedges). The ratio is the scoreboard.

## Anti-patterns

- **Treating grounded as true.** A cited claim can still be wrong; this tool only
  proves *support exists*, not *support is correct*. Verify the citations too.
- **Gaming the linter.** Sprinkling "likely" on real assertions to dodge ⚠ is
  lying, not hedging. The point is honesty, not a green check.
- **Auditing plans/opinions as facts.** Recommendations aren't world-claims; the
  tool already buckets them as `·` — don't force them to ground.
- **Zero-bare as the goal.** Some bare claims are fine (well-known, low-risk). The
  goal is *awareness and triage*, not a mechanical count of zero.

## Example

```
$ echo "Python was released in 1991. The GIL was removed in 2020." \
    | python scripts/claim_audit.py - --fail-over 0.4
⚠ [bare    ] Python was released in 1991.
⚠ [bare    ] The GIL was removed in 2020.
BARE risk = 100% of checkable claims

Verify these before shipping:
  ⚠ Python was released in 1991.
  ⚠ The GIL was removed in 2020.      # (false — worth catching)
$ echo $?
1
```
