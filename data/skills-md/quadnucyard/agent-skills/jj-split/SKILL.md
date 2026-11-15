---
name: jj-split
description: >
  Split one or more Jujutsu commits into semantic commits, putting fixes and
  refactors of existing features first. Follow a restack plan when available.
license: MIT
---

# Split Jujutsu Changes

Split selected changes into **independently valid semantic commits**, preserving
the combined final tree. Splitting does not authorize additional behavior fixes.
Selecting only some resulting features for the mainline, including routing
redundant work to residual side branches, is a restack extraction, not a split
with tree equality waived. Use `jj-plan-restack` and `jj-execute-restack` when
available, or an equivalent explicit selection/dependency plan and independently
validated retained-feature target. Preserve the split-only contract here.

## Choose boundaries

- **Use the plan.** Refer to an available `jj-plan-restack` or equivalent plan;
  verify its source snapshot and honor its boundaries and constraints. Otherwise
  inspect the selected parent diffs and meaningful intermediate states, then map
  every concern to an ordered destination. Use the planner for broader design
  questions when installed; a clear local split needs no full restack plan.
- **Verify purpose.** Trust only substantive descriptions, checked against code
  and consumers. A `refactor` may add a feature; split and order by actual effects.
- **Existing features first.** Order existing-feature fixes, preparatory
  refactors, then new behavior. Dependencies take precedence: a refactor needed
  by a fix comes first; a fix to newly introduced behavior belongs with that
  behavior. Keep implementation, integration, and tests together by purpose.
- **Explain complexity and coupling.** Distinguish inherent feature interactions
  from difficulty caused by the existing architecture, citing contracts and code
  and marking mixed or uncertain causes. Architectural entanglement does not make
  distinct outcomes one feature. Preserve actual dependencies; splitting alone
  does not authorize a refactor to remove them.
- **Keep fixtures with their implementation.** Reject fixture-only commits unless
  they add new fixtures to establish baseline behavior or contain a large test
  change with several new test modules. Harness or test-execution changes are
  not fixture-only. Otherwise, keep fixtures with the implementation they test.
- **Separate broad mechanical refactors.** When a change touches many files and
  a large portion contain only small, repetitive refactors (for example, an API
  migration), extract that refactor into a separate semantic commit so reviewers
  can assess the substantive changes independently. Include the supporting API
  changes and tests needed to keep the refactor valid; order it by dependency.
  Split hunks in mixed-purpose files rather than moving unrelated behavior with
  the mechanical edits. Preserve independently valid commits and the final tree.
- **Account for the whole change.** Include removals, compatibility stages, and
  meaningful states absent from the final tree. Reserve justified future
  extension boundaries without speculative implementation. Treat nonadjacent
  selections as separate groups unless intervening commits are in scope;
  resolve merge semantics before flattening a graph.
- **Route user-declared redundant work to residuals.** When the user identifies
  features or fixes as redundant, classify them as residuals outside the retained
  mainline. If they are to be kept for later reference, preserve them as separate
  semantic commits on side branches rooted at the milestone that supplies their
  dependencies. For a mainline `A -> B -> C`, a residual can branch from `B` or
  `C`; it need not follow the mainline tip. Keep its implementation, integration,
  and tests together, and keep dependencies needed by retained features on the
  mainline. Resolve any conflict between redundancy and a retained dependency
  in the extraction plan. Record each residual's purpose, branch point, and
  preservation destination; calling work redundant does not authorize deleting
  its history. Do not merge reference-only residuals back into the mainline.

Local plan files are deliberately untracked: do not check their tracking status
or reread them merely to confirm a write.

## Split

1. **Protect the source.** Verify `jj root`, explicit base/tip, and working-copy
   state. Record exact source IDs, refs, and the operation; pin the source with a
   fresh safety tag. Preserve unrelated edits, using a separate workspace if
   needed. Build a separate result line; keep original commits and refs intact
   unless replacement was explicitly requested.
2. **Choose per milestone.** Follow the [command recipes](references/recipes.md):
   - **Paths already final:** restore from the final state only when those paths
     reach that state here and have **no later changes**.
   - **Small early commits:** manually build them, then restore the final state
     for the last planned residual.
   - **Large early commits:** duplicate the bounded source unit, subtract, invert
     to extract the early part, then invert and squash to obtain the residual.
   Preserve intermediate milestones when a final snapshot would erase them.
3. **Operate explicitly.** Use noninteractive `jj --no-pager` commands, explicit
   revisions, and complete messages. Check installed help for flags. Mutate only
   workflow-owned revisions through jj; honor a restack plan's duplication
   limits. Temporary subtraction/inverse changes must not survive in the result.

## Verify and finish

- **Each boundary:** read the complete parent diff, check semantic ownership and
  dependencies, and run relevant behavior checks. Recheck affected descendants
  after rewrites. No broken commit may rely on a later repair. Review behavior
  and design adoption, not formatting or linter output.
- **Final result:** require no conflicts and an empty
  `jj diff --from SOURCE_TIP --to RESULT_TIP --summary`; verify source preservation
  and complete source-to-result mapping. Tree equality alone does not validate
  intermediate behavior. Track any separately authorized content fixes explicitly.
  For an extraction with residual branches, use the extraction workflow's
  independently validated retained-feature target for mainline verification;
  account for every excluded concern and validate each preserved residual
  against its own branch parent. Do not restore the source tree onto the
  mainline to force equality and thereby reintroduce redundant work.
- **Descriptions and handoff:** redescribe every result by its actual purpose
  and motivation, especially the residual. Advance only a fresh result bookmark
  after validation. Report ordered change IDs, mapping, safety tag/bookmark, and
  checks or limits, including each preserved residual's branch point and a fresh
  bookmark for later reference; leave a clean working copy. Keep the last validated milestone
  on failure and inspect intervening operations before recovery. Publish only
  when requested.
