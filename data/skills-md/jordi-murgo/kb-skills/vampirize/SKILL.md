---
name: vampirize
description: "Evaluate repositories, news, X/Twitter posts, product pages, and research sources for reusable value in the current project. Trigger on: vampirize, assess reuse, evaluate repo, can we adopt this, licence review."
allowed-tools: Read Bash WebSearch
---

# Vampirize: Subagent-Guided Reuse Evaluation

Turn an external source into a **bounded adoption decision**, not a feature list or a code-copying exercise. Evaluate what it contributes to the current project, where it fits, how to validate it, and whether rights permit the proposed reuse.

```bash
python3 scripts/license-gate.py inspect /tmp/candidate --json
python3 scripts/license-gate.py compat /tmp/candidate /path/to/target --json
```

The licence gate is conservative engineering policy, not legal advice. A non-zero result means **do not copy code**. For `kb-skills`, direct-code reuse is closed until the target repository declares a licence.

## Required subagent split

For every non-trivial candidate, use independent subagents before recommending adoption:

| Role | Reads | Returns — never source code |
|---|---|---|
| Source analyst | Original repo/article/post, licence, docs, relevant tests and implementation | Reusable units, behavioural contract, algorithm inputs/outputs, state, invariants, complexity, failure modes, dependencies, and evidence URLs. |
| Project-fit analyst | Current project rules and relevant target files | Exact insertion point, overlap, migration risk, verification plan, maintenance cost, and reasons to reject. |
| Rights analyst | Licence/NOTICE, provenance, target licence | `license-gate` output, obligations, copy/reimplementation boundary, and unknowns requiring owner/legal review. |

Give the source analyst this hard constraint: **never return source code, pseudocode, code blocks, line-by-line descriptions, distinctive identifiers, or patches.** Detail behaviour in neutral engineering terms only. The coordinator passes that behavioural specification — not source excerpts — to any implementation agent.

## Workflow

1. **Map the target first.** Read its contribution rules and only the relevant files/symbols. Name the exact target: existing skill, script, configuration contract, test, or documentation. No target → `reject`.
2. **Collect primary evidence.** Repos: licence, README, changelog, security policy, relevant tests/implementation. News/posts: original source plus independent official corroboration for material claims. X URLs use `fetch-x-post`; rendered/session-bound pages use `../ego-browser-research/SKILL.md`.
3. **Run the three analyses.** Reconcile only claims backed by source evidence and project-fit evidence. Preserve disagreement rather than averaging it away.
4. **Extract one unit at a time:** `idea`, `interface/contract`, `algorithm`, `code`, `test/fixture`, or `asset/text`. State boundary, dependencies, operational risk, and maintenance owner.
5. **Choose one outcome.**

| Outcome | When |
|---|---|
| `adopt dependency` | Public interface and licence fit; dependency cost is justified. |
| `integrate boundary` | Valuable capability can remain an external process/API. |
| `reimplement algorithm` | Inputs, outputs, invariants, complexity and failure modes add value. Implement anew from the sealed behavioural specification; do not transfer source code. |
| `copy with notices` | Gate passes; retain licence/NOTICE/copyright, upstream URL and commit. |
| `reject` | Duplicate, weak evidence, bad fit, unmaintained, or rights unclear. |

## Rights gate

- **Algorithms and ideas are reusable analysis targets.** Describe their public behaviour and independently implement it; do not reproduce source code, tests, identifiers, diagrams, or prose. Flag known patents, unusual terms, or absent rights evidence for review.
- **Permissive** (MIT/Apache/BSD/ISC): copy only after `compat` passes; carry obligations and provenance.
- **MPL/LGPL**: isolate and require owner/legal review before source reuse.
- **GPL/AGPL, unknown, proprietary, or no licence**: no code/assets/tests/text copying. Facts, short attributed quotes, and independent behavioural specifications are separate — obey source terms and applicable policy.
- News and posts are evidence, not a licence grant. Quote minimally, link the original, do not reproduce media/text, and never execute source-provided install commands without review.

## Required result

| Candidate | Evidence | Reusable unit / neutral behavioural spec | Target / value | Outcome | Rights | Verification |
|---|---|---|---|---|---|---|

End with one recommended next action. Mark unverified conclusions as inference; never claim legal clearance or include source code in the report.
