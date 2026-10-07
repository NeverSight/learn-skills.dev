---
name: monomind-build
description: "Build or implement an approved specification or task inside an established task workspace, using thin verified vertical slices. Use for an already-isolated feature slice, behavior change, refactor, or fix that should run test-first through a public seam and repository-native checks."
---

# Monomind Build

Deliver the smallest complete behavior, prove it, then expand. Preserve the user's work and the repository's authority boundaries throughout.

## Orient the slice

1. If `.monomind/workflow.md` or a managed Monomind instruction block exists, require the installed workflow script's `check --gate build --repo <repository>` to pass before editing. A present profile is not enough: route a failed gate to `monomind-onboarding` when installed and obtain the repository owner/project lead decision. If the gate script is unavailable, inspect the profile directly and do not proceed with unresolved owner, task/workspace, naming, setup, focused/regression test, architecture, shared-resource, continuity, or mutation-authority fields.
2. Confirm this task's owned linked worktree and recorded authoritative base; never implement on `main`, the base branch, or another task's workspace. Reuse a valid task worktree and orientation record from the workflow. If isolation is missing, establish it through the repository convention before editing.
3. Discover repository-native build, test, type, lint, and formatting commands from checked-in configuration or CI. Do not substitute familiar defaults.
4. Detect exact dependency versions. For version-sensitive external APIs, consult current primary documentation for the specific pattern being used.
5. Name the slice's outcome, public test seam, scope boundary, and expected files before editing. If an unresolved choice would materially change the result, surface it first.

Reuse previously verified commands, approvals, and passing gate results from this
task until relevant policy, tooling, code, base, or environment changes. Do not
repeat the workflow's orientation or rerun an identical gate at each slice.

## Run the slice loop

For each slice:

1. **Red:** for a behavior change, add or select a focused test that fails for the missing behavior or reproduced bug. Test through a public seam and obtain expected values from the spec or another independent source of truth.
2. **Green:** implement the simplest complete change that makes the focused check pass. Avoid speculative abstractions, adjacent cleanup, and new dependencies without a concrete need.
3. **Clean:** while green, make small local improvements that clarify the slice. Keep architectural or wide refactors as separate planned work.
4. **Verify:** run the focused check, then the smallest relevant repository gates. Add runtime evidence when automated checks cannot prove the user-visible or operational claim.
5. **Inspect:** review the diff for scope, accidental files, weakened checks, secrets, and stale code introduced by this slice.

Keep the repository valid between slices. Use additive compatibility or a project-supported flag when incomplete work must coexist with the current behavior. Flags need an owner and removal condition; they are not the default for every change.

If an unexpected failure appears, stop extending the feature and switch to a root-cause loop. Do not weaken tests, suppress diagnostics, or broaden the edit merely to reach green.

For side-effecting workflows, keep actions or boundaries responsible for domain policy and why or when an operation runs. Put reusable provider, protocol, command, or SDK mechanics behind service/capability functions with explicit inputs, structured returns, and typed failures. Keep one-off mechanics local until reuse or a volatile boundary earns extraction.

Commits, pushes, tracker updates, dependency installation, and deployment follow the user's and project's explicit authority. A clean slice does not itself authorize those external or version-control mutations.

## Completion criteria

- The approved acceptance criteria are met through observable behavior.
- New or changed behavior has focused coverage at a public seam.
- Repository-native focused and regression checks passed after the final relevant edit.
- Runtime claims have revision-bound evidence where automated tests are insufficient.
- The final diff contains no unrelated cleanup, weakened quality gate, secret, or unaccounted file.
- Residual risks and deferred verification are stated plainly.
