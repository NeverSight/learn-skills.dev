---
name: simplify-change
description: Use this skill when implementing or reviewing a change that may contain unnecessary code, abstractions, dependencies, configuration, indirection, or generated boilerplate.
---

# Simplify a Change

Prefer the smallest conventional solution that satisfies the current requirements. Optimize for fewer concepts, dependencies, branches, files, and special cases—not minimum line count.

## Procedure

1. **Establish the contract.** Identify the requested behavior, constraints, affected code, and relevant project conventions. Do not simplify behavior whose purpose or requirements are still unclear.
2. **Test whether each piece is needed.** Ask, in order:
   - Does a current requirement need it?
   - Does the project already provide it?
   - Does the language, standard library, platform, or an existing dependency provide it?
   - If not, what is the smallest clear local solution?
3. **Make the smallest coherent change.** Delete, inline, or reuse code when that preserves the contract. Avoid speculative extension points, wrappers, dependencies, configuration, and fallback paths. Keep code conventional and understandable; fewer lines are not automatically simpler.
4. **Review in proportion to risk.** For a small, local change with no meaningful new logic or concepts, review the diff directly. For substantial logic, generated code, or changes adding abstractions, dependencies, configuration, or indirection, seek two reviewers with fresh context when separate reviewers are available:
   - **Challenge necessity:** Assume each addition is unnecessary until a current requirement justifies it. Look for code that can be removed, inlined, reused, or replaced with existing project, language, platform, or dependency features. Report concrete findings and the requirement each addition fails to justify; do not propose new features or architecture.
   - **Review as a maintainer:** Inspect the repository and diff without relying on implementation rationale that is not recorded there. Flag hidden assumptions, unclear purpose, or unusual complexity. Report concrete findings.

   Treat reviewers as critics; make and verify any accepted changes yourself. If separate reviewers are unavailable, perform the two reviews yourself as distinct passes and do not describe them as independent.
5. **Verify the result.** Run the narrowest existing checks that can detect regressions, then broaden them according to risk. Inspect the final diff for accidental scope, broken contracts, stale comments, secrets, and unnecessary complexity. Resolve failures and rerun affected checks; if a check cannot be run, state that limitation rather than claiming verification.

## Preserve

Do not simplify away explicitly requested behavior, validation at trust boundaries, security controls, meaningful error handling, accessibility, project conventions, compatibility required by the current contract, or tests that materially protect behavior.
