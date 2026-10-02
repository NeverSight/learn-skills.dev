---
name: craft-skills-and-memories
description: Use when creating a skill or memory, when one fails in practice, or when the user reports one misbehaving or stale.
license: SEE LICENSE IN LICENSE.md
metadata:
  author: Vivswan
---

# Craft Skills and Memories

One skill for both ends of the lifecycle of an agent's instruction sources: creating skills and memories worth keeping, and repairing them when they fail in practice.

A broken skill or a stale memory is a bug. Working around it and moving on re-breaks the next session.

Scope:

- **Skills are general-purpose.** Nothing in a skill should be project-specific. A fact that only holds for one project belongs in that project's own docs or memories, not in the skill.
- **Memories may be project-specific or common.** Create and fix a memory at the scope it belongs to: a project memory in that project's store, a common memory in the shared store.

## When to Apply

Creating:

- "Save this as a memory" / "make this a skill" / "remember this"
- The decision is made to encode a lesson or workflow for future sessions (deciding the response to a correction is `/never-twice`'s job, and its rung 3 hands off here)

Fixing:

- A documented flag, command, or file in a skill no longer exists
- A skill's copy-paste block breaks in a reproducible way
- A skill's extraction or verification rule misses what it is supposed to catch
- A recalled memory names a file, flag, or workflow that no longer exists or was superseded
- The user says a skill or memory is not working properly

## The Quality Bar (creating and fixing alike)

- **Example-, scenario-, or concept-led, never quote-led.** The concrete specimen (the failing command, the corrected block, a worked scenario) recalls far better in a future session than abstract explanation or the user's verbatim words.
  - Structure each entry specimen-first: what happened and where, then the rule it taught, then the boundary or exceptions.
  - Keep a short verbatim phrase only when the exact wording IS the directive (a ban, a naming rule). Otherwise paraphrase into the rule.
  - When touching an old quote-led entry, retrofit it.
- **Descriptions are triggers**: short, "Use when ...", stating the one moment the thing should fire, never summarizing contents. A summary-shaped description is an activation bug.
- **Skills** carry runnable copy-paste blocks and worked examples a cold agent can follow.
- **A skill roster stays lean and disjoint.** The design conditions for creating, combining, and splitting skills:
  - Every firing moment has exactly one home: a skill states its specific moments, and triggers across the roster are pairwise disjoint. An overlap is a defect, resolved by combining or sharpening, never tolerated. This skill's create-and-fix lifecycle is such a combination: its moments share one home, one reader.
  - Fewer skills beats more: combine two skills that serve the same reader at the same moment.
  - No skill becomes extremely complex or big: split by firing moment when one grows. A complex skill never absorbs a sibling even when triggers overlap. Sharpen the descriptions instead.
  - Skimmable throughout: short front-loaded paragraphs, no text blobs (the example-led rule above governs content order). Readability for the reader outranks style rules, and accuracy rules always bind.
  - Form follows the change in any section: no mandated format beyond this bar, never a visual plus prose re-explaining it, programmer register. The `/natural-writing` bullet below states when that skill applies to prose.
  - No backwards compatibility, folders included: splits, merges, and retirements are normal changes, with every deletion audited per the `/never-twice` skill (Deleting a Guard). A compatibility contract the hosting repo declares (such as published install paths) still binds folder moves there.
- **Memories** hold one fact per file, record the why, convert relative dates to absolute, and link related memories. A wrong memory gets deleted, not patched around.
- When rewriting prose, apply the `/natural-writing` skill if it is present and invocable. If your harness lets only the user invoke it, suggest they run `/natural-writing` rather than silently skipping the step.

## Creating

1. **Check for an existing home first.** A skill or memory that already covers the topic gets updated. Duplicates drift apart.
2. **Pick skill vs memory.**
   - General-purpose behavior any user could install: skill.
   - Personal or project fact, policy, or preference: memory, at the right scope.
   - A skill that encodes a personal workflow rather than an auto-detectable task should be explicit-invocation-only. That means `disable-model-invocation: true` in the frontmatter, and `policy.allow_implicit_invocation: false` in `agents/openai.yaml` for Codex.
3. **Write it to the quality bar above**, with the triggering incident as the specimen.
4. **Wire it in**: a skill follows its repository's authoring checklist (manifests, catalog, checks). A memory gets its index line.
5. **Run the gates** where they exist (repo checks, review). For a memory, re-read it asking "will a cold session act correctly from this?"

## Fixing

### 1. Rule out transient causes

Backend outages, sandbox restrictions, and local tool configuration are not skill defects. Only a failure whose root cause is the instructions themselves qualifies.

### 2. Finish the current task first

Work around the broken step to complete what the user actually asked for. The fix comes after, not instead.

### 3. Fix it at its canonical source

- Skill in its authoring repository: edit the affected sources directly (`SKILL.md`, `references/`, `scripts/`).
- Installed or vendored skill copy you are authorized to edit (e.g. a personal skills directory): edit that copy. Tell the user the upstream source still carries the defect if one exists.
- Memory: edit the memory file where it lives and keep its index line in sync. A memory that is wrong, as opposed to merely stale, gets deleted, not patched around.
- Not authorized to write: report the defect and your proposed fix to the user instead.

### 4. Fold the fix in, don't append a note

Rewrite the affected step so it is correct as written and meets the quality bar. Keep copy-paste blocks runnable.

A one-off warning bolted to the end leaves the broken instructions in place. A rewrite that deletes rules follows the deletion audit in the `/never-twice` skill (Deleting a Guard).

**Code first for mechanical failures.** Where each kind of fix lands:

- A skill's script-backed **mechanical** behavior fails in practice (a probe misreads, a command parses wrongly, an edge case crashes): the fix lands in the script, plus a regression test that reproduces the incident.
- **Incident-warning** prose is the scoped reservation: trap narratives and priors stay judgment-lesson-only, because the script embodies the mechanism.
- Public **contract** documentation (CLI shapes, schemas, output fields) is different: it moves together with the interface change it describes. Where a drift gate pins doc to source, the gate enforces exactly that pairing.
- **Documentation-only** defects (activation metadata, invocation examples, workflow prose) fix in their actual source, never by touching a script that was not the failure.

Why code first: a trap folded into a tested script cannot re-fire. A trap folded into prose regrows the catalog: each incident adds a warning paragraph, the file swells, and a future session hand-rolls the broken step anyway.

Worked case: a fleet-monitoring skill accumulated shell-probe trap prose (word-splitting, self-matching greps, a missing `timeout` binary) until the probes moved into tested scripts and the prose shrank to the judgment layer.

### 5. Put the edit through the normal gates

A skill or memory edit is a change like any other: run whatever checks and review process govern the place it lives. Where none exist (e.g. a plain installed copy), at least re-run the failing scenario to confirm the rewritten instructions work.

## Worked Examples

**A creation.** The user corrects the agent twice for hard-wrapping commit messages at 72 columns.

- That is a memory, not a skill: personal policy, applies across repos, nothing installable.
- Write `commit-message-rules.md` in the common store with the correction as the specimen and the why, then add its index line.
- Example-led, not quote-led: it records the rule and a concrete before/after, not the user's exact words.

**A skill defect.** While following a review skill, `claude -p --output-format stream-json` exits with an error and an empty output file.

1. Transient? No: it reproduces every run, and `claude --help` shows `--output-format stream-json` requires `--verbose`. The root cause is the skill's documented command.
2. Finish the review by re-running with `--verbose` added.
3. The skill's canonical source is a local checkout of its authoring repo: edit the copy-paste block in its `SKILL.md` to include `--verbose`.
4. The fix goes into the block itself, so it stays runnable as written. No footnote saying "note: also pass --verbose".
5. Run that repo's checks and include the edit in the same change set for review.

**A stale memory.** A recalled project memory says deploys go through `make release`, but the Makefile renamed the target to `make publish` months ago.

1. Verify against the current repo: the memory is stale, not the build.
2. Finish the deploy with the real target.
3. Update the memory file in that project's store (and its index line) to name `make publish`, keeping the rename as the concrete example.

**Not a defect.** The same command fails once with a backend overload error and succeeds on retry. That is transient. Finish the task and leave the skill alone.

## Using Skills

Fit is judged per invocation. When an invoked skill's guidance does not fit the task at hand, skip it (wholly or a specific rule) and tell the user why at the point of the decision.

- Never follow a skill mechanically against the task's needs.
- Never ignore one silently.
- Standing rules the user has set (e.g. a commit gate) still hold. This covers guidance that genuinely conflicts with the work.

## Reporting

Tell the user what you created or what failed, the root cause, and what changed in the skill or memory, separately from the outcome of their original task.
