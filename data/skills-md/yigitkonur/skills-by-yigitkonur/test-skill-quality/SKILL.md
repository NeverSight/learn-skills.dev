---
name: test-skill-quality
description: Use skill if you are testing a skill's instructional quality by following its workflow literally on a real task, documenting friction points, and fixing ambiguities.
---

# Test Skill Quality

Test any skill's instructions by following them literally, documenting every moment they fail to guide the next action, and fixing the root causes.

## Trigger boundary

Use this skill when:

- testing whether a skill's instructions are complete and unambiguous
- auditing a skill for instructional quality before publishing
- dogfooding a skill by running its workflow on a real task
- improving a skill after receiving feedback that it's confusing or incomplete
- validating that fixes to a skill's instructions actually resolved the original friction

Do not use this skill for:

- building a new skill from scratch (use `build-skills`)
- evaluating the quality of a skill's *output* (use evaluation suites)
- reviewing code changes in a pull request (use `review-pr`)
- general documentation improvements not related to skill instructions

## Non-negotiable rules

1. **Follow literally, not intelligently.** Suppress domain knowledge. If the instructions don't specify it, record a friction point — even if you "know" the answer.
2. **Test on a real task.** Toy examples don't exercise branching logic, error handling, or cross-references. The task must be genuine and non-trivial.
3. **Every derailment gets an ID.** Friction points are numbered F-01, F-02, ... with P0/P1/P2 severity. No unnamed complaints.
4. **Fix the instructions, not the executor.** The remedy is always a text edit to the skill files, never "use a smarter agent."
5. **The derail notes are the primary deliverable.** Not a pass/fail verdict. A structured document showing what broke and why.
6. **Verify after fixing.** Run grep-based consistency checks and confirm routing integrity after edits.

## Required workflow

### 1. Select the test subject and task

Choose:
- **The skill to test** — any skill with a SKILL.md and optional references
- **The test task** — a real, representative task within the skill's trigger boundary

The test task must be:
- Genuinely within the skill's scope (not an edge case)
- Complex enough to exercise the full workflow (not a one-step operation)
- Executable in the current environment (required tools available)

Record the test metadata:

```
Skill under test: [name]
Test task: [one-line description]
Date: [YYYY-MM-DD]
Method: Follow SKILL.md steps N–M exactly as written
```

### 2. Pre-scan the skill

Before executing, read through the skill once:

- Read SKILL.md fully — note total steps, branching points, cross-references
- Tree the `references/` directory
- List external dependencies (tools, MCP servers, APIs)
- Note the skill's declared trigger boundary

Do NOT execute anything during this step. This is orientation only.

### 3. Execute literally (the core loop)

For each step in the skill's workflow:

1. **Read only the current step.** Do not look ahead.
2. **Attempt to execute** using only the information provided in the skill.
3. **Record the outcome:**
   - **Clean pass** — step was unambiguous and executable.
   - **Derailment** — you could not determine the next action from the instructions alone. Record a friction point.
   - **Implicit knowledge used** — you could execute, but only because you knew something not stated. Record a lower-severity friction point.

For each derailment, write:

```markdown
**F-[NN] — [short title]** (P[0-2])
[What happened, what the instructions said, what was missing or ambiguous.]
Fix: [Specific text edit that would prevent this derailment.]
```

See `references/friction-classification.md` for severity assignment rules.

### 4. Collect evidence

After completing all steps, calculate:

| Metric | Value |
|---|---|
| Total steps attempted | |
| Clean passes | |
| P0 (blocks progress) | |
| P1 (causes confusion) | |
| P2 (minor annoyance) | |

Build a derailment density map showing which workflow phases have the most friction.

Tag each friction point with a root cause code — see `references/root-cause-taxonomy.md`.

### 5. Write the derail notes

Write the report to `derail-notes/NN-dogfood-[topic].md` in the project root.

Structure:

```markdown
# Derailment Test: [skill-name] on "[task]"

Date: ...
Skill under test: ...
Test task: ...
Method: ...

---

## Friction points

### [Phase/step name]

**F-01 — [title]** (P0)
...

## What worked well

1. ...

## Priority summary

| Priority | Count | Friction points |
|---|---|---|
| P0 | N | F-xx, ... |
| P1 | N | F-xx, ... |
| P2 | N | F-xx, ... |
```

### 6. Apply fixes

Fix priority: all P0, then all P1, then P2 if time allows.

For each friction point, apply the fix directly to the skill's source files. Read `references/fix-patterns.md` to match the derailment type to a proven fix pattern.

Fixes must be:
- **In-place** — edit the existing instruction, don't create errata
- **Self-contained** — the fix works without consulting the derail notes
- **Minimal** — add only what was missing

### 7. Verify fixes

After all edits:

1. **Terminology consistency** — grep for stale terms that should have been updated
2. **Routing integrity** — confirm every reference file is still reachable from SKILL.md
3. **Cross-reference consistency** — no contradictions between documents
4. **Size constraints** — SKILL.md still under 500 lines
5. **No regressions** — fixes didn't introduce new ambiguities

```bash
# Example verification commands
grep -r "old_term" skills/[skill-name]/    # should be zero
find skills/[skill-name]/references -type f -name "*.md" | while read f; do
  grep -q "$(basename "$f" .md)" skills/[skill-name]/SKILL.md || echo "ORPHAN: $f"
done
wc -l skills/[skill-name]/SKILL.md        # should be under 500
```

### 8. Optional: Re-run the test

The gold standard is re-running the test on the fixed skill with a different task. New derailments go into a new derail-notes file (`02-dogfood-[topic].md`). Compare metrics across runs to verify improvement.

## Decision rules

- If the skill has no references, test only SKILL.md steps
- If a derailment is actually a bug in an external tool (not the instructions), document it but tag it as `external` — don't fix the skill for someone else's bug
- If 3+ P1 items cluster in one step, treat the cluster as compound P0
- If the skill references other skills, test only the current skill's instructions — not the referenced skill's workflow
- If you discover the skill's trigger boundary is wrong (fires on wrong queries), record it as a friction point but also flag it separately as a trigger issue

## Do this, not that

| Do this | Not that |
|---|---|
| Follow each step literally as written | Fill in gaps from personal knowledge |
| Record every uncertainty as a friction point | Skip ambiguities that seem "minor" |
| Fix the source files directly | Create a separate errata or known-issues file |
| Test on a real task within the skill's scope | Use a toy example or hypothetical scenario |
| Write structured derail notes with IDs and severities | Write prose complaints without classification |
| Verify fixes with grep and routing checks | Assume fixes are correct without verification |
| Report what worked well alongside what broke | Write a purely negative report |

## Output contract

Deliver in this order:

1. Test metadata (skill, task, date)
2. Pre-scan summary (step count, branching, dependencies)
3. Friction point registry (F-01 through F-NN with severity and root cause)
4. Derailment density map
5. What worked well section
6. Priority summary table
7. Fixes applied (which file, which friction point)
8. Verification results

## Reference routing

| File | Read when |
|---|---|
| `references/friction-classification.md` | Assigning severity (P0/P1/P2) to a friction point or choosing between severity levels |
| `references/root-cause-taxonomy.md` | Tagging friction points with root cause codes for pattern analysis |
| `references/fix-patterns.md` | Matching a derailment type to a proven fix pattern |
| `references/metrics-and-iteration.md` | Tracking improvement across multiple test runs or building cross-run reports |
| `references/adaptation-domains.md` | Applying Derailment Testing to non-skill instruction sets (runbooks, SOPs, API docs) |

## Guardrails

- Do not skip the pre-scan. It prevents misidentifying "working as designed" as a derailment.
- Do not fix friction points without reading the root cause taxonomy. Fixes without root cause analysis recur.
- Do not create an errata file. Fixes go directly into the source.
- Do not declare the test complete without the "What worked well" section.
- Do not re-test with the same task. Use a different representative task for each run.
- Do not test a skill you are currently building. Build it first (with `build-skills`), then test it.

## Final checks

Before declaring the test complete:

- [ ] Derail notes file exists at `derail-notes/NN-dogfood-[topic].md`
- [ ] Every friction point has an ID (F-NN), severity (P0-P2), and root cause code
- [ ] All P0 fixes are applied
- [ ] All P1 fixes are applied (or deferred with justification)
- [ ] "What worked well" section is present
- [ ] Priority summary table is present
- [ ] Verification grep shows zero stale terms
- [ ] Routing integrity confirmed — no orphaned reference files in tested skill
- [ ] SKILL.md of tested skill is still under 500 lines after fixes
