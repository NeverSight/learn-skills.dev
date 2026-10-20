---
name: documentation-impact
description: Check documentation impact before completing a change or declaring it ready to ship. Use when a change may affect user, operator, or developer instructions, when asked whether docs need updates, or for a documentation pass. Supports author and read-only review modes without requiring a PR or spec.
---

# Documentation impact

Match the documentation to the behavior people will use. Inspect the actual change and its callers before deciding which docs need work. A supported no-change conclusion is a complete result.

## Choose the mode and scope

Use `author` when the task authorizes documentation updates. Use `review` for an audit, independent review, status request, or other read-only task. Honor the caller's mode. If update authority is unclear, inspect and report in `review` mode.

- In `author` mode, update affected documentation within the authorized change. Leave unrelated edits alone.
- In `review` mode, inspect without editing the artifact you judge. Return findings to its author. Do not fix a document and certify your own fix.

The calling workflow owns delegation, model selection, continuation, and human gates. Do not spawn another coordinator or start a publication workflow here.

Use the accepted request, issue, or existing work brief. Do not require a new spec, ticket, docs tree, or work ledger.

Bind the pass to what you actually examine:

- For committed work, resolve and record the fixed base and head. Inspect the base-to-head diff and the surrounding implementation and documentation at those revisions.
- For local work, also inspect staged and unstaged changes and relevant untracked files. Record a content fingerprint or retained snapshot of those inputs. A clean-looking HEAD or a filename list does not identify dirty file contents.
- Outside Git, record an explicit content snapshot of the scoped implementation and docs. If a relevant input is unavailable, name the gap instead of claiming coverage.

Record the examined paths and either the fingerprint method or the retained snapshot location so another agent can reproduce the comparison. Recheck the inputs before returning the result. If concurrent edits changed them, refresh the affected checks or report that the result no longer describes the current artifact.

## Map the change to readers

Read the repository's instructions and discover where its maintained docs and examples live. Trace changed behavior to the people who use, run, upgrade, or develop the project. Include public workflow changes in skills and configuration, even when no application code changed.

Consider these document types where the change affects them:

| Changed behavior | Candidate documentation |
|---|---|
| Installation, onboarding, or basic usage | README, quickstarts, tutorials |
| Commands, APIs, flags, defaults, configuration, or environment variables | CLI and API reference, configuration guides, executable examples |
| Compatibility, storage, or upgrade behavior | Migration and upgrade instructions, deprecation notices |
| Release-visible behavior | Release notes or changelog, if the repository maintains them |
| Module boundaries, data flow, or operational behavior | Architecture explanations, diagrams, runbooks, developer guides |

Search for old names, old values, and contradictory examples beyond files already changed. Read the matched claims in context. A recent timestamp, a path match, generated prose, or a rendered diagram cannot establish factual accuracy.

For each affected reader task, identify the maintained document or explain why no document needs a change. Existing docs may already be correct. Internal refactoring may leave every documented contract unchanged. Do not create filler docs to make the pass appear productive.

## Update or inspect

In `author` mode, make the smallest corrections needed for the changed behavior. Follow the repository's documentation layout and generation commands. Update the source of generated docs instead of hand-editing generated output.

Use the **technical-writing** skill on documentation you write or review. Then use the **unslop** skill on it. Keep examples tied to real symbols, paths, flags, defaults, and supported versions. If an upgrade requires user action, state that action and the old-to-new behavior.

Trace documented effects through the implementation. Accepting or reporting a setting does not prove that the corresponding operation runs. If intended behavior and observed behavior disagree, report the mismatch as an implementation finding instead of documenting a defect as supported behavior.

In `review` mode, derive the affected reader tasks from the implementation yourself. Check the author's coverage decisions against the source, including claims that nothing changed. Treat the author's receipt as evidence to inspect, not as the verdict.

Use the repository's existing diagram format when a diagram explains an affected relationship better than prose. Check each changed actor, edge, direction, and boundary against the implementation. Optional visual tools can help present findings if available. Otherwise use Markdown or the existing diagram source. Do not install a visual dependency, require branding input, or wait for annotation feedback to complete this pass.

## Decide whether author mode requires review

An author pass returns exactly one result:

- `independent review required` when documentation changed, a public workflow or documented contract changed, or a documentation gap remains unresolved.
- `independent review not required` only when evidence shows that an internal change has no documentation impact.

`independent review not required` is invalid for a public workflow or documentation change. Record the evidence that supports the author result with the examined artifact. A completion or shipping workflow can start an independent review only when the author result is `independent review required`.

When independent review is required, a different agent reviews the resulting artifact without editing it. The independent review verdict is `pass`, `needs changes`, or `unverified`. After repairs, the reviewer checks the resulting artifact before returning `pass`. Reuse the verdict only while its examined change, docs, and relevant surrounding context still match. A matching stable patch-id after a rebase does not establish that the documentation context is unchanged. Recheck that context or rerun the pass.

## Verify and return the result

Run the relevant repository documentation checks and exercise changed examples against the actual implementation when safe within the task's authority. Use the **verify-commands** skill on commands used as completion evidence. In review mode, run checks without modifying the reviewed files, using a disposable copy if the check writes output.

Check factual meaning as well as syntax and rendering. An example that runs with the wrong default or a diagram that invents an approval step is still wrong. Report unsafe or unavailable checks as gaps. Never run a deployment, publish docs, or change external data just to verify an example.

Return a compact result in the conversation or the existing work record:

- The mode, scope, and examined revision or snapshot, including relevant local changes.
- The affected reader tasks and document paths, with updates made or evidence for leaving them unchanged.
- The checks actually run, their outcomes, and any remaining findings or verification gaps.
- In author mode, the author result and its evidence. In review mode, return `pass`, `needs changes`, or `unverified`. Use `needs changes` for established omissions or incorrect claims. Use `unverified` when missing evidence prevents a decision.

An author result is not an independent review verdict.
