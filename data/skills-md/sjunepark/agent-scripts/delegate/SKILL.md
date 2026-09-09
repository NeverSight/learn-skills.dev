---
name: delegate
description: "Orchestrate substantive code and file implementation through a GPT-5.6 Luna subagent, then review and iterate on the result. Explicit invocation only."
---

# Delegate

Treat the request supplied with `$delegate` as the desired implementation.
Keep the parent agent accountable for the complete requirement, decomposition,
decisions, review, validation, and final response while GPT-5.6 Luna workers
perform detailed edits to narrow slices.

## 1. Frame the Work

1. Inspect the request, applicable instructions, repository state, and relevant
   implementation surfaces far enough to define the work accurately. Resolve
   consequential product or authority questions before delegation; do not make
   the worker guess them.
2. Retain ownership of the complete user requirement and decompose substantive
   implementation into staged slices. Each slice must have one concrete
   outcome, bounded behavior and implementation ownership, and a validation
   target that can be reviewed independently. “Small” is behavioral, not a
   fixed file or line-count threshold. A source change and its directly coupled
   regression test may share a slice only when splitting them would make
   validation meaningless; never use that exception to smuggle in an
   end-to-end project requirement. Never send a broad feature, refactor,
   migration, or multi-surface requirement as one worker assignment.
3. Define the next slice's implementation contract: its outcome, owned
   behavior or files, constraints, acceptance criteria, validation, integration
   dependencies, and known unrelated changes to preserve. State how the slice
   contributes to the broader end state without transferring ownership of that
   broader requirement to the worker.
4. Delegate substantive implementation. The parent may instead perform a
   clearly correct, localized, low-risk change when preparing and reviewing a
   delegation would cost more than making and validating the change directly.

Framing is complete when a fresh worker can act on that one slice without
needing the parent conversation or making a consequential product decision.

## 2. Dispatch the Implementer

Spawn one primary implementation subagent for each slice with:

- `model: "gpt-5.6-luna"`;
- `reasoning_effort: "max"`; and
- `fork_turns: "none"`.

Give it a self-contained, slice-specific prompt. The prompt must reproduce the
original user request verbatim and include, without paraphrasing, compressing,
or omitting, every known requirement, constraint, acceptance criterion,
relevant decision, failure or error output, repository fact, and integration
dependency that can affect the slice. Include the exact files the worker must
read in full when needed. Distinguish the worker's narrow ownership from the
broader end state and explain how the slice fits it; omit unrelated background,
but never replace result-affecting context with a vague summary. Also include
the working directory, slice contract, applicable constraints, and validation
to run. Tell the worker to inspect before editing, preserve unrelated work,
avoid commits or publication unless authorized, and return a concise account
of changed files, validation, and unresolved issues.

Use one writer for overlapping files or behavior. Parallel workers are
appropriate only for independent slices whose file and behavior ownership
cannot overlap. Do not silently substitute another model or reasoning level
when the requested worker configuration is unavailable; report that limitation
and preserve the current state. Do not edit worker-owned files concurrently.

Once a slice is dispatched, coordinate it rather than duplicating its detailed
work. Wait for the slice, independently review and validate it, and decide the
next slice before dispatching any dependent work.

## 3. Review and Iterate

1. Wait for each implementer, then inspect its diff and validation evidence
   against the slice contract and repository instructions. The parent's review
   is an independent quality gate, not a restatement of the worker's report.
   Complete this review and proportionate validation before dispatching the
   next dependent slice.
2. Send material defects, missing coverage, or unclear decisions back to the
   same implementer as a precise follow-up. State what failed, the required
   outcome, and the validation to rerun. Repeat until the contract passes or a
   genuine blocker requires the user.
3. The parent may directly apply an obvious, localized correction found during
   review when another worker turn would be less efficient. Validate every
   direct correction and return broader or judgment-heavy rework to the
   implementer.
4. Run or independently confirm the proportionate final checks. Report the
   completed outcome, important decisions, changed files, validation results,
   and any residual risk.

The delegation is complete only when the parent has verified the complete
requested behavior and required checks across its slices, not merely when an
implementer reports success.
